# import json
# import requests
# url = "https://ocr.asprise.com/api/v1/receipt"
# image = "receipt.jpeg"
# res = requests.post(url,
#                     data = {
#                         'api_key': 'TEST',
#                         'recognizer': 'auto',
#                         'ref_no': 'oct_python_123'
#                     },
#                     files = {
#                         'file': open(image, 'rb')
#                     })
# with open("response1.json", "w") as f:
#     json.dump(json.loads(res.text), f)
# with open("response1.json", "r") as f:
#     data = json.load(f)
# print(data['receipts'][0].keys())
#
# items = data['receipts'][0]['items']
#
# print(f'Your Purchase at {data["receipts"][0]["ocr_text"]}')
import json
import requests

url = "https://ocr.asprise.com/api/v1/receipt"
image = "receipt.jpeg"

api_key = "TEST"

response = requests.post(url,
                         data={"api_key": api_key},
                         files={"file": open(image, "rb")})

data = json.loads(response.text)
print(data)
receipt = data["receipts"][0]

print("Chek ma'lumotlari:")
print("- Sana:", receipt["date"])
print("- Vaqt:", receipt["time"])
print("- Xaridlar soni:", len(receipt["items"]))

total_amount = 0
for item in receipt["items"]:
    print(f"- {item['description']} - {item['amount']}")
    total_amount += float(item["amount"])

print(f"Jami summa: {total_amount}")

# # Endi shu ma'lumotlar asosida tekshirishlar
# if receipt["date"] < "01.01.2023":
#     print("Chek sana noto'g'ri")
# if total_amount < 100000:
#     print("Yetarli xarid qilinmagan")
# va hokazo...
