import easyocr

reader = easyocr.Reader(['en'])  # 'en' til uchun
result = reader.readtext('receipt.jpeg')

for detection in result:
    print(detection[1])



