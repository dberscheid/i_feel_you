import re
import requests

URL_TEMPLATE = "https://i-feel-you.sharetribe.com/de/people/confirmation?confirmation_token={token}&ref=email"

FROM = 4501
TO = 4575

path = "<ENTER PATH>"
with open(path + str(FROM) + "-" + str(TO) + ".csv", "r") as file_handle:
  content = "\n".join(file_handle.readlines())
matches = re.findall(r"confirmation_token=(.*?)&ref=email", content)
tokens = []
for match in matches:
  token = match
  if token not in tokens:
    tokens.append(token)

counter = FROM-1
for token in tokens:
  counter += 1
  url = URL_TEMPLATE.replace("{token}", token)
  response = requests.get(url)
  print(str(counter) + ": " + str(response.status_code))