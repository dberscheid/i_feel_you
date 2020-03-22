import overpass
import json
import time
api = overpass.API(timeout=600)

path = "<ENTER PATH>"

# the following must be done twice: once for listed amenity types and once for listed shop types
# amenity
# "bar", "biergarten", "cafe", "ice_cream", "pub", "restaurant", "boat_rental", "social_facility", "arts_centre", "cinema", "community_centre", "nightclub", "planetarium", "social_centre"
# shop
# "bakery", "hairdresser", "cosmetics", "massage", "tattoo", "swimming_pool", "art", "collector", "music", "musical_instrument"

for type in ["bakery", "hairdresser", "cosmetics", "massage", "tattoo", "swimming_pool", "art", "collector", "music", "musical_instrument"]:
  query = """
    nwr[shop=""" + type + """]["addr:country"="DE"]["email"];
    out center;
  """
  response = api.Get(query, responseformat="json")
  with open(path + type + ".json", "w+") as handle:
    handle.write(json.dumps(response, sort_keys=True, indent=2))

  print(type + " done")
  time.sleep(120)
