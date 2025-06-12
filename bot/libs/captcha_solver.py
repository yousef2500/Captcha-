from PIL import Image
import imagehash
import os

# مسار مجلد الصور المرجعية
REFERENCE_DIR = os.path.join(os.path.dirname(__file__), "reference_emojis")

def load_reference_hashes():
    """تحميل بصمات الصور المرجعية"""
    hashes = {}
    for filename in os.listdir(REFERENCE_DIR):
        if filename.endswith(".png"):
            fruit_name = os.path.splitext(filename)[0]
            img = Image.open(os.path.join(REFERENCE_DIR, filename))
            hash_val = imagehash.average_hash(img)
            hashes[fruit_name] = hash_val
    return hashes

def find_matching_fruit(target_image_path: str, options_paths: list[str]) -> str:
    """يحدد اسم الفاكهة المطابقة"""
    ref_hashes = load_reference_hashes()
    target_image = Image.open(target_image_path)
    target_hash = imagehash.average_hash(target_image)

    # قارن مع المرجعية
    best_match = None
    lowest_distance = float("inf")
    for name, ref_hash in ref_hashes.items():
        dist = target_hash - ref_hash
        if dist < lowest_distance:
            best_match = name
            lowest_distance = dist

    return best_match
