import os
import re
import sys
import random
import pathlib
import hashlib
import argparse
import pytesseract
from PIL import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the file or directory")
    args = parser.parse_args()


PATH = pathlib.Path(args.path)

if not PATH.exists():
    print("path does not exist")
    sys.exit(1)

if not PATH.is_dir():
    print("path is not a directory")
    sys.exit(1)

if not any(PATH.iterdir()):
    print("that directory is empty bro")
    sys.exit(1)

print(f"\n{PATH}")
if input("this will irreversibly rename image files in the dir. is this the correct path? (y/n)  ") != "y":
    print("aight bro take ur time\naborting")
    sys.exit(1)

os.chdir(PATH)

counter = 0
del_counter = 0
seen_hashes = set()

print("\nrenaming ur files")

for file in PATH.iterdir():

    # rm duplicate
    with open(file, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    if file_hash in seen_hashes:
        print(f"removing duplicate: {file}")
        del_counter += 1
        os.remove(file)
        continue
    seen_hashes.add(file_hash)

    extension = (PATH/file).suffix.lower()
    try:
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        words = [
            word[:10].lower()
            for word in re.sub(r'[^A-Za-z0-9]+', ' ', text).split()
        ][:7]

        if words:
            new_name = ("_".join(words))
        else:
            new_name = str(random.randint(1000, 100000))

        for _ in range(3):
            try:
                os.rename(file, f"{new_name}{extension}")
                break
            except OSError:
                new_name = f"{new_name}{random.randint(0, 9)}"
        else:
            print (f"failed to rename {file}")
        if file != new_name: counter += 1
    except: print(f"{file} is not an image or is corrupted")

print(f"\nrenamed {counter} image files")
print(f"deleted {del_counter} image files")
