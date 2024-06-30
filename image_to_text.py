# giving images as list
# check for argparser initial
# appended description to describe the module
# expanding the help module and formatting it
# check for user argument

# Importing libraries
import pytesseract
import argparse
from wand.image import Image
from deep_translator import GoogleTranslator

pytesseract.tesseract_cmd = r"tesseract"



def img_to_gray(img_name, img_name_gray):
    # Transform image from color to grayscale
    try:
        with Image(filename=img_name) as img:
            img.transform_colorspace("gray")
            img.adaptive_threshold(width=16, height=16, offset=-0.15 * img.quantum_range)
            img.save(filename=img_name_gray)
            img.close()
            return True
    except:
            return False
    
def google_translate(text, text_translated, img_name, args):
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


def my_iterator(args):
    for img_name in args["image"]:
        # break
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

            if(text is not None and len(text.strip()) != 0):
                # Write-up original text
                with open(text_en, "w", encoding="utf-8") as outfile:
                    outfile.write(text)
                    outfile.close()
                
                print(f"Writing text {img_name}")

                if(args["to"] is not None):
                    google_translate(text, text_translated, img_name, args)

            else:
                print(f"No text captured {img_name}")

        else:
            print(f"\nNot a valid image {img_name} -- skipping")



def main():
    # Fetching the arguments
    ap = argparse.ArgumentParser(description="Python script to extract text from images after converting them to grayscale")
    # Reference https://stackoverflow.com/questions/43786174/how-to-pass-and-parse-a-list-of-strings-from-command-line-with-argparse-argument
    ap.add_argument("-i", "--image", help="path to the input image", required=True, nargs='+', default=[])
    ap.add_argument("-l", "--lang", help="text language type (default: %(default)s)", default="eng", choices=pytesseract.get_languages(), metavar="eng")
    ap.add_argument("-t", "--to", help="language to translate the text", choices=list((GoogleTranslator().get_supported_languages(as_dict=True)).values()), metavar="de")
    ap.add_argument("-p", "--psm", type=int, default=3, help="Tesseract PSM mode type (default: %(default)s)", choices=range(1,14), metavar="3")
    
    args = vars(ap.parse_args())
    args["psm"] = "--psm "+str(args["psm"])


    my_iterator(args)



if __name__ == "__main__":
    main()