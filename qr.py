from pyzbar.pyzbar import decode
from PIL import Image

# Откройте изображение с QR-кодом
image = Image.open('receipt.jpeg')

# Попробуйте прочитать QR-код
try:
    decoded_objects = decode(image)
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        print(f"Содержимое QR-кода: {data}")

        # Проверяем, содержит ли данные фразу "tax.salyk.kg"
        if "tax.salyk.kg" in data:
            print("Это чек")
except Exception as e:
    print(f"Ошибка при чтении QR-кода: {e}")
