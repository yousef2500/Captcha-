from PIL import Image
import pytesseract

def solve_captcha(image_path: str) -> str:
    # فتح الصورة
    image = Image.open(image_path)

    # تحسين الصورة لو حبيت تضيف (اختياري)
    image = image.convert("L")  # تحويل الصورة لتدرج رمادي
    image = image.point(lambda x: 0 if x < 140 else 255, '1')  # فلترة البياض والسواد

    # قراءة النص من الصورة
    text = pytesseract.image_to_string(image, config='--psm 8 digits')

    # تنضيف الناتج (نشيل الفراغات أو أي رموز)
    return ''.join(filter(str.isdigit, text))
