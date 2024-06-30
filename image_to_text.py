# commenting and removing extra lines


# Importing libraries
import pytesseract
import argparse
from wand.image import Image
from deep_translator import GoogleTranslator
import os
import pandas as pd

pytesseract.tesseract_cmd = r"tesseract"

# Transform image from color to grayscale
def img_to_gray(img_name, img_name_gray, output_folder):
    try:
        with Image(filename=img_name) as img:
            os.makedirs(output_folder)
            img.transform_colorspace("gray")
            img.adaptive_threshold(width=16, height=16, offset=-0.15 * img.quantum_range)
            img.save(filename=img_name_gray)
            img.close()
            return True
    except:
            return False
    
# Write-up translated text
def google_translate(text, text_translated, args):
    translated=GoogleTranslator(source="auto", target=args["to"]).translate(text)
    if(translated is not None and len(translated.strip()) != 0):
        with open(text_translated, "w", encoding="utf-8") as outfile_translated:
            outfile_translated.write(translated)
            outfile_translated.close()
        return True
    else:
        return False


def my_iterator(args):
    summary_df = pd.DataFrame(columns=["file_path","is_image","gray_file_path","text_in","is_text_captured","translated_in","is_translation_success"])
    for img_name in args["image"]:
        # Declaring variables
        img_name_base = img_name.rsplit(".",1)[0]
        output_folder = args["output"] + "/" + img_name_base
        img_name_gray = output_folder + "/" + "gray_" + img_name
        text_en = output_folder + "/" + "gray_"+img_name_base+".txt"
        text_translated = output_folder + "/" + "gray_translated_"+img_name_base+".txt"

        # check if file is valid image
        img_check = img_to_gray(img_name, img_name_gray, output_folder)
        # appending metadata
        my_summary = {"file_path" : os.path.abspath(img_name), "is_image" : None, "gray_file_path" : None, "text_in" : args["lang"], "is_text_captured" : None, "translated_in" : None, "is_translation_success" : None}
        

        if(img_check):
            print(f"\nProcessing image {img_name}")
            # appending metadata
            my_summary["is_image"] = "yes"
            my_summary["gray_file_path"] = os.path.abspath(img_name_gray)

            # Extracting text 
            text = pytesseract.image_to_string(img_name_gray, lang=args["lang"], config=args["psm"])

            if(text is not None and len(text.strip()) != 0):
                my_summary["is_text_captured"] = "yes"
                # Write-up original text
                with open(text_en, "w", encoding="utf-8") as outfile:
                    outfile.write(text)
                    outfile.close()
                
                print(f"Writing text {img_name}")
                
                # Text translation using google translator
                if(args["to"] is not None):
                    my_summary["translated_in"] = args["to"]
                    if(google_translate(text, text_translated, args)):
                        my_summary["is_translation_success"] = "yes"
                        print(f"Writing translation {img_name}")
                    else:
                        my_summary["is_translation_success"] = "no"
                        print(f"No translation found {img_name}")

            # No text found
            else:
                my_summary["is_text_captured"] = "no"
                print(f"No text captured {img_name}")

        # Not a valid image
        else:
            my_summary["is_image"] = "no"
            print(f"\nNot a valid image {img_name} -- skipping")

        
        summary_df = pd.concat([summary_df, pd.DataFrame([my_summary])], ignore_index=True)


    summary_df.to_csv(args["output"]+"/summary.csv")
    print('\nCompleted\n')

# Creating main output folder
def out_folder(args):
    path = args["output"] + "/" + "out"
    counter = 1
    new_path = path

    while os.path.isdir(new_path):
        new_path = path + "_" + str(counter)
        counter += 1

    os.makedirs(new_path)

    return new_path


def main():
    # Fetching the arguments
    ap = argparse.ArgumentParser(description="Python script to extract text from images after converting them to grayscale")
    # Reference https://stackoverflow.com/questions/43786174/how-to-pass-and-parse-a-list-of-strings-from-command-line-with-argparse-argument
    ap.add_argument("-i", "--image", help="path to the input image/images --required", required=True, nargs='+', default=[])
    # Tesseract language key:value -- https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
    ap.add_argument("-l", "--lang", help="text language type (default: %(default)s)", default="eng", choices=pytesseract.get_languages(), metavar="eng")
    ap.add_argument("-t", "--to", help="language to translate the text", choices=list((GoogleTranslator().get_supported_languages(as_dict=True)).values()), metavar="de")
    # PSM Choices and meaning -- https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
    ap.add_argument("-p", "--psm", type=int, default=3, help="Tesseract PSM mode type (default: %(default)s)", choices=range(1,14), metavar="3")
    ap.add_argument("-o", "--output", default=os.getcwd(), help="Output folder path (default: %(default)s)")
    
    args = vars(ap.parse_args())
    args["psm"] = "--psm "+str(args["psm"])
    args["output"] = out_folder(args)
    
    my_iterator(args)



if __name__ == "__main__":
    main()