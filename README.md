# yo

this script ocrs text from image files in a directory and renames them to something comprehensible

also removes duplicate files of all types

extracts text from images;  
converts names to lowercase;  
limits each word to 10 chars;  
up to 7 words per filename;  
random numeric filename if no text is detected

## usage

```bash
pip install -r requirements.txt
python main.py /path/to/images_directory
```
