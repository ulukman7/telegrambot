import pytesseract
from PIL import Image

# Chek rasmini ochamiz
image = Image.open('receipt.jpg')

# OCR orqali matnga o'tkazamiz
text = pytesseract.image_to_string(image)

# Matndan sana va summani ajratib olamiz
date = find_date(text)
total = find_total(text)

print(f"Sana: {date}")
print(f"Jami summa: {total}")
