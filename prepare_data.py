import json
import random
from os import listdir
from os.path import isfile, join
path = "<ENTER PATH>"
files = [f for f in listdir(path) if isfile(join(path, f))]

random.seed(1)

def rand(length, use_capital_letters):
  chars = '0123456789' \
  'abcdefghijklmnopqrstuvwxyz'
  if (use_capital_letters):
    chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  return ''.join(random.choice(chars) for i in range(length))

EMAIL_DOMAIN = "@i-feel-you.org"

emails = []
with open(path + "/../" + "data.csv", "w+", encoding="utf8") as output_handle:
  for file in files:
    with open(path + "/" + file, "r") as file_handle:
      dict = json.loads(" ".join(file_handle.readlines()))
      for element in dict["elements"]:
        tags = element["tags"]

        if tags.get("email") in emails:
          continue # only one location per email (vs. chains and redundant entries)
        else:
          emails.append(tags["email"])

        id = rand(8, False)
        generated_password = rand(8, True)

        values = []
        values.append(str(id))
        values.append(tags.get("amenity") or tags.get("shop"))
        values.append(tags.get("name") or "")
        values.append(tags.get("operator") or "")
        values.append(tags.get("email"))
        values.append(tags.get("phone") or "")
        values.append(tags.get("website") or "")
        values.append(tags.get("addr:street") or "")
        values.append(tags.get("addr:housenumber") or "")
        values.append(tags.get("addr:postcode") or "")
        values.append(tags.get("addr:city") or "")
        values.append(tags.get("addr:country") or "")
        values.append(tags.get("opening_hours") or "")
        values.append("ify-" + str(id) + EMAIL_DOMAIN)
        values.append(generated_password)
        for index, val in enumerate(values):
          values[index] = val.replace(";", ",")
        
        output_handle.write(";".join(values) + "\n")