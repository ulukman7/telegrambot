import requests
import json

with open("response3.json", "r") as f:
    data = json.load(f)
print(data['receipts'][0].keys())

items = data['receipts'][0]['items']

print(f'Your Purchase at {data["receipts"][0]["ocr_text"]}')

