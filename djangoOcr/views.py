from django.shortcuts import render, HttpResponse
from PIL import Image
import pytesseract
import cv2
import os
import re
import ftfy
import imageio
from .models import FilesUpload
from .utils import apply_ocr, write_output_to_file, read_text_from_file, fix_unicode, remove_spaces
    
def convert_image_to_text(file):
    ############## [2] Preprocess Image   #############################
    if file:
        try:
            input_image = imageio.imread("./media/" + file)
            gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        except:
            return ""
    
        gray_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]     
        gray_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)      
        gray_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)                   
        gray_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)        
        gray_image = cv2.medianBlur(gray_image, 3)
        gray_image = cv2.bilateralFilter(gray_image, 9, 75, 75)

        # temp file
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray_image)

        ########## [3] Apply Tesseract OCR & fix unicode   ###############
        text = apply_ocr(filename)
        write_output_to_file(text, 'output.txt')
        text = read_text_from_file('output.txt')
        text = fix_unicode(text)

        ######### [4] Extracting information from text  #################
        name = None
        fname = None
        dob = None
        pan = None
        panline = []
        text0 = []
        text1 = []

        # remove spaces
        text1 = remove_spaces(text)

        # Regex to remove text before IncomeTaxDepartment
        lineno = 0  # to start from the first line of the text file.

        for wordline in text1:
            xx = wordline.split('\n')
            if ([w for w in xx if re.search('(INCOMETAXDEPARWENT @|mcommx|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
                text1 = list(text1)
                lineno = text1.index(wordline)
                break

        text0 = text1[lineno+1:]
    
        def findword(textlist, wordstring):
            lineno = -1
            for wordline in textlist:
                xx = wordline.split( )
                if ([w for w in xx if re.search(wordstring, w)]):
                    lineno = textlist.index(wordline)
                    textlist = textlist[lineno+1:]
                    return textlist
            return textlist

        try:
            # name
            name = text0[0]
            name = name.rstrip()
            name = name.lstrip()
            name = name.replace("8", "B")
            name = name.replace("0", "D")
            name = name.replace("6", "G")
            name = name.replace("1", "I")
            name = re.sub('[^a-zA-Z] +', ' ', name)

            # father's name
            fname = text0[1]
            fname = fname.rstrip()
            fname = fname.lstrip()
            fname = fname.replace("8", "S")
            fname = fname.replace("0", "O")
            fname = fname.replace("6", "G")
            fname = fname.replace("1", "I")
            fname = fname.replace("\"", "A")
            fname = re.sub('[^a-zA-Z] +', ' ', fname)

            # dob
            dob = text0[2]
            dob = dob.rstrip()
            dob = dob.lstrip()
            dob = dob.replace('l', '/')
            dob = dob.replace('L', '/')
            dob = dob.replace('I', '/')
            dob = dob.replace('i', '/')
            dob = dob.replace('|', '/')
            dob = dob.replace('\"', '/1')
            dob = dob.replace(" ", "")

            # pan number
            text0 = findword(text1, '(Pormanam|Number|umber|Account|ccount|count|Permanent|ermanent|manent|wumm)$')
            panline = text0[0]
            pan = panline.rstrip()
            pan = pan.lstrip()
            pan = pan.replace(" ", "")
            pan = pan.replace("\"", "")
            pan = pan.replace(";", "")
            pan = pan.replace("%", "L")

        except:
            pass

        # storing information in data
        data = {}
        data['name'] = name
        data['fname'] = fname
        data['dob'] = dob
        data['pan'] = pan

        return data
    else:
        return ""

def show_error():
    error = {}
    error['emptyData'] = "Something went wrong"
    return error

def home(request):
    if request.method == "POST":
        file2 = request.FILES["file"]
        ################ [1] Save input image to database ##############
        document = FilesUpload.objects.create(file=file2)
        document.save()
        text = read_text_from_file('output.txt')
        pan_card_data = convert_image_to_text(file2.name)
        if not pan_card_data:
            return render(request, "error.html", {'error' : show_error()})
        else:        
            return render(request, "pancard.html", 
            {'data' : pan_card_data,
             'convertedText': text})
    return render(request, "index.html")
    