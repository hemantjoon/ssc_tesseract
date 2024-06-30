# removed translated to str(translated) since output is of class str only
# adding f.close() to close the opened files and img.close()
# appened the args - lang and psm in the pytesseract function


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
    text_translated = "gray_translated_"+filename_original+".txt"

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
        args["psm"] = "--psm "+str(args["psm"])

    # Set-up columns
        # options = "-l {} --psm {}".format(args["lang"], args["psm"])

    # Extract the text 
        text = pytesseract.image_to_string(filename_gray, lang=args["lang"], config=args["psm"])

    # Write-up original text
        with open(text_en, "w", encoding="utf-8") as outfile:
            outfile.write(text)
            outfile.close()
            # outfile = open(text_en, "w", encoding="utf-8")
            # outfile.write(text)

    # Write-up translated text
        translated=GoogleTranslator(source="auto", target=args["to"]).translate(text)   
        # print(type(translated)) 
        # translated=str(translated)
        with open(text_translated, "w", encoding="utf-8") as outfile_translated:
            outfile_translated.write(translated)
            outfile_translated.close()
