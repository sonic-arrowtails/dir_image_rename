import os
import re
import sys
import random
import pathlib
import argparse
import pytesseract
from PIL import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the file or directory")
    args = parser.parse_args()

try:
    PATH = pathlib.Path(args.path)
    os.chdir(PATH)
except:
    print("somethings wrong with ur path bro")
    sys.exit(1)

dir_contents = os.listdir()
counter = 0

for file in dir_contents:
    print("\nrenaming ur files")
    extension = (PATH/file).suffix.lower()
    try:
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        words = [
            word[:10].lower()
            for word in re.sub(r'[^A-Za-z0-9]+', ' ', text).split()
        ][:7]
        if words: new_name = ("_".join(words))+extension
        else: new_name = str(random.randint(1000,100000))+"."+extension

        for _ in range(3):
            try:
                os.rename(file, new_name)
                break
            except OSError:
                new_name = f"{new_name}{random.randint(0, 9)}"
        else:
            print (f"failed to rename {file}")
        if file != new_name: counter += 1
    except: print(f"{file} is not an image or is corrupted")

print(f"\nrenamed {counter} image files")