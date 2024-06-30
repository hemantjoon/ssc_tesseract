# correcting the comments
# import wand.image import Image to only Image
# removing the paranthesis from GoogleTranslator
# String interpolation
# updated rsplit to obtain the filename [0]
# update filenam to filename
# updated variable item to use filename
# commenting out options variable as not being used in the script
# changing list with img_list and item to photo
# filenam to filename_original
# name to filename_gray

# Importing libraries
import pytesseract
import argparse
from wand.image import Image
from deep_translator import GoogleTranslator

pytesseract.tesseract_cmd = r"tesseract"


img_list = ["im1.jpg", "img2.jpg"]


for photo in img_list:
    print(f"Processing image {photo}")

    # Declaring variables
    filename_original = photo.rsplit(".",1)[0]
    filename_gray = "gray_" + photo
    text_en = "gray_"+filename_original+".txt"
    text_trans = "gray_translated_"+filename_original+".txt"

    # Transform image from color to grayscale
    with Image(filename=photo) as img:
        img.transform_colorspace("gray")
        img.adaptive_threshold(width=16, height=16,
        offset=-0.15 * img.quantum_range)
        img.save(filename=filename_gray)   

    # Fetching the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="path to the input image", default="{name}")
        ap.add_argument("-l", "--lang", help="path to the language", default="eng")
        ap.add_argument("-t", "--to", type=str, default="en", help="eng")
        ap.add_argument("-p", "--psm", type=int, default=13, help="Tesseract PSM mode")
        args = vars(ap.parse_args())

    # Set-up columns
        # options = "-l {} --psm {}".format(args["lang"], args["psm"])

    # Extract the text 
        text = pytesseract.image_to_string(filename_gray)

    # Write-up original text
        outfile = open(text_en, "w", encoding="utf-8")
        outfile.write(text)

    # Write-up translated text
        translated=GoogleTranslator(source="auto", target=args["to"]).translate(text)    
        trans=str(translated)
        with open(text_trans, "w", encoding="utf-8") as f:
            f.write(trans)
