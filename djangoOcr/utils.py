from PIL import Image
import pytesseract
import os
import ftfy

# Load the image, apply OCR, and then delete temp file
def apply_ocr(filename):
    try: 
        text = pytesseract.image_to_string(Image.open(filename), lang = 'eng')
        os.remove(filename)
        return text
    except:
        return ''

def write_output_to_file(text, filename):
    try: 
        text_output = open(filename, 'w', encoding='utf-8')
        text_output.write(text)
        text_output.close()   
    except:
        return ''

def read_text_from_file(filename):
    try:
        file = open(filename, 'r', encoding='utf-8')
        text = file.read()
        return text     
    except:
        return ''

# ftfy: fixes text for you (mostly fixes unicode that's broken)
def fix_unicode(text):
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    return text        

def remove_spaces(text):
    formatted_text_list = []
    if text:
        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = lin.replace('\n','')
            s = s.rstrip()
            s = s.lstrip()
            formatted_text_list.append(s)
        return list(filter(None, formatted_text_list))
    else:
        return ''      