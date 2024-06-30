# moving out the argparser, since it will be initiated once only
# updating variables img_name_base from filename_original and img_name_gray from filename_gray, img_name from photo
# making function img_to_gray with two arguments (img_name, img_name_gray)
# appended with try except for img_to_gray so as to avoid in between function break
# change psm default to 3 since giving good results for 3
# append text.strip() /// translated.strip() to make sure empty lines are not printed

# Importing libraries
import pytesseract
import argparse
from wand.image import Image
from deep_translator import GoogleTranslator

pytesseract.tesseract_cmd = r"tesseract"


img_list = ["im1.jpg", "hjk.mt", "img2.jpg"]

# Fetching the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to the input image", default="{name}")
ap.add_argument("-l", "--lang", help="path to the language", default="eng")
ap.add_argument("-t", "--to", type=str, help="eng")
ap.add_argument("-p", "--psm", type=int, default=3, help="Tesseract PSM mode")
args = vars(ap.parse_args())
args["psm"] = "--psm "+str(args["psm"])

def img_to_gray(img_name, img_name_gray):
    # Transform image from color to grayscale
    try:
        with Image(filename=img_name) as img:
            img.transform_colorspace("gray")
            img.adaptive_threshold(width=16, height=16, offset=-0.15 * img.quantum_range)
            img.save(filename=img_name_gray)
            return True
    except:
            return False
    
def google_translate(text, text_translated):
    # Write-up translated text
    translated=GoogleTranslator(source="auto", target=args["to"]).translate(text)
    # translated = str(translated)
    if(translated is not None and len(translated.strip()) != 0):
        with open(text_translated, "w", encoding="utf-8") as outfile_translated:
            outfile_translated.write(translated)
            outfile_translated.close()
        print(f"Writing translation {img_name}")
    else:
        print(f"No translation found {img_name}")


for img_name in img_list:
    # Declaring variables
    img_name_base = img_name.rsplit(".",1)[0]
    img_name_gray = "gray_" + img_name
    text_en = "gray_"+img_name_base+".txt"
    text_translated = "gray_translated_"+img_name_base+".txt"

    check = img_to_gray(img_name, img_name_gray)
    

    if(check):
        print(f"\nProcessing image {img_name}")
        # Extract the text 
        text = pytesseract.image_to_string(img_name_gray, lang=args["lang"], config=args["psm"])
        # print(len(text.strip()))

        if(text is not None and len(text.strip()) != 0):
            # Write-up original text
            with open(text_en, "w", encoding="utf-8") as outfile:
                outfile.write(text)
                outfile.close()
            
            print(f"Writing text {img_name}")

            if(args["to"] is not None):
                google_translate(text, text_translated)

        else:
            print(f"No text captured {img_name}")

    else:
         print(f"\nNot a valid image {img_name} -- skipping")