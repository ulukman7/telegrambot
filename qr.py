from pyzbar.pyzbar import decode
from PIL import Image

# Откройте изображение с QR-кодом
image = Image.open('receipt2.jpg')

# Попробуйте прочитать QR-код
try:
    decoded_objects = decode(image)
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
    print(f"Содержимое QR-кода: {data}")


except Exception as e:
    print(f"Ошибка при чтении QR-кода: {e}")
