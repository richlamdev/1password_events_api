import datetime
import requests
import os
import json

api_token = os.environ["EVENTS_API_TOKEN"]
url = "https://events.1password.com"

start_time = datetime.datetime.now() - datetime.timedelta(hours=24)
# start_time = datetime.datetime.now() - datetime.timedelta(days=30)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}",
}
payload = {
    "limit": 1,
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

r = requests.post(f"{url}/api/v1/itemusages", headers=headers, json=payload)

if r.status_code == requests.codes.ok:
    print(json.dumps(r.json()))
    print()
    print()
    print("cursor: " + r.json()["cursor"])
    print("has_more: " + str(r.json()["has_more"]))
else:
    print("Error getting item usages: status code", r.status_code)

last_cursor = "null"

while r.json()["has_more"]:
    # print("has_more: " + str(r.json()["has_more"]))
    last_cursor = r.json()["cursor"]

    payload = {"cursor": last_cursor}
    r = requests.post(
        f"{url}/api/v1/itemusages", headers=headers, json=payload
    )

    if r.status_code == requests.codes.ok:
        print(json.dumps(r.json()))
        print()
        print()
        print(r.json()["cursor"])
    else:
        print("Error getting item usages: status code", r.status_code)


