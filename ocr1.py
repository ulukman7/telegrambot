import requests
import json

with open("response1.json", "r") as f:
    data = json.load(f)
print(data['receipts'][0].keys())

items = data['receipts'][0]['items']

print(f'Your Purchase at {data["receipts"][0]["merchant_name"]}')

for item in items:
    print(f"{item['description']} - {item['amount']}")
