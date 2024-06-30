# single quotes to all double quotes && replacing psm 3 with psm only (noting down the range is from 0 to 14 -- detailed help)
## observations : argparses is inside the image processing function itself (it should be separate and excecuted first)
## observations : file open is handled differently also no file closing (more memory consumption)
## hard-coded image file name
## image extension is not checked; file is image or not??
## output path not found, thus all files with same place as input and output
## verbose may be added to have better progress report
## try except for exceptions to be placed
## extensive help module need to be generated
## variable name should be more intuitive
## functions should be made for processing and argparser
## requirements.txt file if everything is good

# Importing libraries
import pytesseract
import argparse
from wand.image import Image as WImage
from deep_translator import (GoogleTranslator)

pytesseract.tesseract_cmd = r"tesseract"


list = ["im1.jpg", "img2.jpg"]


for item in list:
    print("Processing image {}".format(item))
    filenam = item.rsplit(".",1)[1]
    # Transform image from color to grayscale
    with WImage(filename=item) as img:
        img.transform_colorspace("gray")
        img.adaptive_threshold(width=16, height=16,
        offset=-0.15 * img.quantum_range)
        img.save(filename="gray_"+item)   
    # Extract the text 
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="path to the input image", default="{name}")
        ap.add_argument("-l", "--lang", help="path to the language", default="eng")
        ap.add_argument("-t", "--to", type=str, default="en", help="eng")
        ap.add_argument("-p", "--psm", type=int, default=13, help="Tesseract PSM mode")
        args = vars(ap.parse_args())
    # Set-up columns
        options = "-l {} --psm {}".format(args["lang"], args["psm"])
        name="gray_"+item
        text = pytesseract.image_to_string(name)
    # Write-up original text
        outfile = open("gray_"+item+".txt", "w", encoding="utf-8")
        outfile.write(text)
    # Write-up translated text
        translated=GoogleTranslator(source="auto", target=args["to"]).translate(text)    
        trans=str(translated)
        with open("gray_translated_"+item+".txt", "w", encoding="utf-8") as f:
            f.write(trans)
