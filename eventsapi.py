import datetime
import requests
import os
import json
import time


def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


api_token = os.environ["EVENTS_API_TOKEN"]
url = "https://events.1password.com"

# start_time = datetime.datetime.now() - datetime.timedelta(hours=7)
start_time = datetime.datetime.now() - datetime.timedelta(days=30)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}",
}
payload = {
    "limit": 1000,
    "start_time": start_time.astimezone().replace(microsecond=0).isoformat(),
}

# Alternatively, use the cursor returned from previous responses to get any new events
# payload = { "cursor": cursor }

# r = requests.post(
# f"{url}/api/v1/signinattempts", headers=headers, json=payload
# )
# if r.status_code == requests.codes.ok:
# print(r.json())
# print(json.dumps(r.json()))
# else:
# print("Error getting sign in attempts: status code", r.status_code)

item_usages = []

r = requests.post(f"{url}/api/v1/itemusages", headers=headers, json=payload)

if r.status_code == requests.codes.ok:
    print(json.dumps(r.json()))
    print()
    print()
    # print("cursor: " + r.json()["cursor"])
    # print("items: " + str(type(r.json()["items"])))

    item_usages = r.json()["items"]

else:
    print("Error getting item usages: status code", r.status_code)

last_cursor = ""
counter = 1

while r.json()["has_more"]:
    last_cursor = r.json()["cursor"]

    payload = {"cursor": last_cursor}
    r = requests.post(
        f"{url}/api/v1/itemusages", headers=headers, json=payload
    )

    if r.status_code == requests.codes.ok:
        print(json.dumps(r.json()))
        print()
    else:
        print("Error getting item usages: status code", r.status_code)

    counter += 1

    item_usages.append(r.json()["items"])
    time.sleep(0.75)

print()
print("total requests sent: " + str(counter))

# flatten the list of lists
flatten_item_usages = flatten_list(item_usages)

with open("item_usages.json", "w") as output_file:
    json.dump(flatten_item_usages, output_file, indent=4)
