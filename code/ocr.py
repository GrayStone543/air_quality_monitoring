import subprocess
import pytesseract
import cv2
import numpy as np
import argparse


def ssocr_7seg(cv2_img):
    success, encoded_image = cv2.imencode('.png', cv2_img)
    if not success:
        return "Error: failed to encode image"
    
    byte_data = encoded_image.tobytes()

    # -C, --omit-decimal-point omit decimal points from output
    # -f, --foreground=COLOR   set foreground color (black or white)
    # -b, --background=COLOR   set background color (black or white)
    cli_command = ["ssocr", "-d", "-1", "--omit-decimal-point", "-f", "white", "-b", "black", "-"]

    try:
        process = subprocess.Popen(
            cli_command,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        stdout_data, stderr_data = process.communicate(input=byte_data)

        if process.returncode != 0:
            return f"SSOCR Error: {stderr_data.decode().strip()}"

        return stdout_data.decode().strip()
    except subprocess.CalledProcessError as e:
        return f'Error: {e.output.decode()}'


def tesseract_7seg(cv2_img):
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(cv2_img, config=custom_config)
    return text


def preprocess(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Can not read image")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)
    #contrast_enhanced = cv2.equalizeHist(gray)

    blurred = cv2.GaussianBlur(contrast_enhanced, (5, 5), 0)

    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    fixed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # optional, enhance again
    #fixed = cv2.dilate(fixed, kernel, iterations=1)

    cv2.imshow('Original', gray)
    cv2.imshow('Contrast Enhanced', contrast_enhanced)
    cv2.imshow('Preprocessed', thresh)
    cv2.imshow('Fixed', fixed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return fixed

if __name__ == "__main__":
    parser = argparse.ArgumentParser("7-Segments OCR")
    parser.add_argument("-i", "--input", help="filename")
    parser.add_argument("--mode", help="Specified the OCR engine", type=str, choices=['ssocr', 'tesseract'], default='ssocr')
    args = parser.parse_args()

    if type(args.input).__name__ != 'NoneType':
        cv2_img = preprocess(args.input)
        if args.mode == 'ssocr':
            print("----- SSOCR -----")
            result = ssocr_7seg(cv2_img)
        else:
            print("----- Tesseract -----")
            result = tesseract_7seg(cv2_img)
        print("----- Output -----")
        print(f"{result}")
        print("------------------")

