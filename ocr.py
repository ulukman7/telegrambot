import json
import requests
url = "https://ocr.asprise.com/api/v1/receipt"
image = "receipt3.jpg"
res = requests.post(url,
                    data = {
                        'api_key': 'TEST',
                        'recognizer': 'auto',
                        'ref_no': 'oct_python_123'
                    },
                    files = {
                        'file': open(image, 'rb')
                    })
with open("response3.json", "w") as f:
    json.dump(json.loads(res.text), f)
