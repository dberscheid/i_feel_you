from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def enter_value(driver, id, value):
  elem = driver.find_element_by_id(id)
  elem.clear()
  elem.send_keys(value)
def check(driver, id):
  elem = driver.find_element_by_id(id)
  elem.click()

def register(driver, entry_data):
  driver.get("https://i-feel-you.sharetribe.com/de/signup")
  enter_value(driver, "person_email", entry_data["email"])
  enter_value(driver, "person_given_name", "ID")
  enter_value(driver, "person_family_name", entry_data["id"])
  enter_value(driver, "person_password1", entry_data["password"])
  enter_value(driver, "person_password2", entry_data["password"])
  check(driver, "person_terms")
  check(driver, "person_admin_emails_consent")
  form = driver.find_element_by_id('new_person')
  submit_button = form.find_element_by_css_selector('button[type="submit"]')
  submit_button.click()

def logout(driver):
  driver.get('https://i-feel-you.sharetribe.com/de/logout')
  time.sleep(1)

def login(driver, entry_data):
  driver.get("https://i-feel-you.sharetribe.com/de/login")
  enter_value(driver, "main_person_login", entry_data["email"])
  enter_value(driver, "main_person_password", entry_data["password"])
  submit_button = driver.find_element_by_id("main_log_in_button")
  submit_button.click()
  time.sleep(1)

def find_username(driver):
  driver.get("https://i-feel-you.sharetribe.com/")
  a_elements = driver.find_elements_by_tag_name("a")
  for a_element in a_elements:
    href = a_element.get_attribute("href")
    if href.endswith("/settings"):
      parts = href.split("/")
      username = parts[len(parts)-2]
      return username

def get_address(entry_data):
  return entry_data["street"] + " " + entry_data["houseNumber"] + ", " + entry_data["postalCode"] + " " + entry_data["city"]

def edit_profile(driver, username, entry_data, description):
  driver.get("https://i-feel-you.sharetribe.com/de/" + username + "/settings")
  enter_value(driver, "person_display_name", entry_data["name"])
  enter_value(driver, "person_username", entry_data["id"])
  address = get_address(entry_data)
  enter_value(driver, "person_street_address", address)
  time.sleep(4) # TODO
  enter_value(driver, "person_phone_number", entry_data["phone"])
  enter_value(driver, "person_description", description)
  form = driver.find_element_by_css_selector("form[class*='edit_person']")
  submit_button = form.find_element_by_css_selector("button[type='submit']")
  submit_button.click()
  time.sleep(2.5) # TODO

def create_coupon(driver, entry_data, coupon_amount, coupon_description_template):
  driver.get("https://i-feel-you.sharetribe.com/de/listings/new")
  time.sleep(1) # TODO
  enter_value(driver, "listing_title", entry_data["name"])
  enter_value(driver, "listing_price", coupon_amount)
  enter_value(driver, "listing_description", coupon_description_template.replace("{name}", entry_data["name"]))
  enter_value(driver, "custom_fields_131229", entry_data["website"]) # WARNING
  
  type_select_values_part = {
    "bakery": 829,
    "hairdresser": 835,
    "cosmetics": 840,
    "massage": 842,
    "tattoo": 852,
    "swimming_pool": 850,
    "art": 836,
    "collector": 849,
    "music": 846,
    "musical_instrument": 843,
    "bar": 830,
    "biergarten": 831,
    "cafe": 833,
    "ice_cream": 834,
    "pub": 847,
    "restaurant": 848,
    "boat_rental": 832,
    "social_facility": 851,
    "arts_centre": 841,
    "cinema": 839,
    "community_centre": 837,
    "nightclub": 844,
    "planetarium": 845,
    "social_centre": 851
  }
  if entry_data["type"] in type_select_values_part:
    type_select_value = "479" + str(type_select_values_part[entry_data["type"]])
  else:
    type_select_value = "479892"
  select_element = driver.find_element_by_id("custom_fields_131373") # WARNING
  option = select_element.find_element_by_css_selector("option[value='" + type_select_value + "']")
  option.click()

  enter_value(driver, "listing_origin", get_address(entry_data))
  time.sleep(3) # TODO
  # first_image_element = driver.find_element_by_css_selector('input[type="file"]')
  # image_path = "C:/Users/Dr. Patrick Winter/Hackathon/img/" + entry_data["type"] + ".jpg"
  form = driver.find_element_by_id('new_listing')
  submit_button = form.find_element_by_css_selector('button[type="submit"]')
  submit_button.click()
  time.sleep(3)

def delete_account(driver, username):
  driver.get("https://i-feel-you.sharetribe.com/de/" + username + "/settings/account")
  delete_button = driver.find_element_by_id("delete_account_button")
  delete_button.click()
  time.sleep(1)
  driver.switch_to.alert.accept()
  driver.switch_to.default_content()

ACTION = 1 # 1: register, 2: edit profile and create coupon, 3: delete account

COUPON_AMOUNT = 10
COUPON_DESCRIPTION_TEMPLATE = "Unterstütze **{name}** in der Corona-Krise, indem Du jetzt 10€-Gutscheine davon zur späteren Einlösung kaufst! Alle Details dazu auf unserer [Infoseite](https://i-feel-you.sharetribe.com/infos/about)."
ENTITY_DESCRIPTION_TEMPLATE = "(auto-generiert)"

FROM = 4501
TO = 4575

csv_path = "<ENTER PATH>"
with open(csv_path, "r", encoding="utf8") as file_handle:
  records = file_handle.readlines()
end = min(TO, len(records))
records = records[(FROM-1):TO]

options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

counter = FROM
for record in records:
  parts = record.split(";")
  entry_data = {}
  entry_data["id"] = parts[0]
  entry_data["type"] = parts[1]
  entry_data["name"] = parts[2]
  entry_data["phone"] = parts[5]
  entry_data["website"] = parts[6]
  entry_data["street"] = parts[7]
  entry_data["houseNumber"] = parts[8]
  entry_data["postalCode"] = parts[9]
  entry_data["city"] = parts[10]
  entry_data["email"] = parts[13]
  entry_data["password"] = parts[14]

  try:
    if ACTION == 1:
      register(driver, entry_data)
      logout(driver)
    elif ACTION == 2:
      login(driver, entry_data)
      username = find_username(driver)
      edit_profile(driver, username, entry_data, ENTITY_DESCRIPTION_TEMPLATE)
      username = entry_data["id"] # username is changed
      create_coupon(driver, entry_data, COUPON_AMOUNT, COUPON_DESCRIPTION_TEMPLATE)
      logout(driver)
    elif ACTION == 3:
      login(driver, entry_data)
      delete_account(driver, username)
  except Exception as e:
    print("ERROR for " + str(counter) + ": ")
    print(e)

  print(counter)
  counter += 1

  time.sleep(1)
# driver.close()

