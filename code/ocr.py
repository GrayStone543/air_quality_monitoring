import subprocess
import pytesseract
import cv2
import numpy as np
import argparse


def ssocr_7seg(cv2_img, num_of_digits=-1):
    success, encoded_image = cv2.imencode('.png', cv2_img)
    if not success:
        return "Error: failed to encode image"
    
    byte_data = encoded_image.tobytes()

    # -C, --omit-decimal-point omit decimal points from output
    # -f, --foreground=COLOR   set foreground color (black or white)
    # -b, --background=COLOR   set background color (black or white)
    cli_command = ["ssocr", "-d", f"{num_of_digits}", "-f", "white", "-b", "black", "-"]

    try:
        process = subprocess.Popen(
            cli_command,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        stdout_data, stderr_data = process.communicate(input=byte_data)

        if process.returncode != 0:
            return f"SSOCR Error({process.returncode}): {stderr_data.decode().strip()}"

        return stdout_data.decode().strip()
    except subprocess.CalledProcessError as e:
        return f'Error: {e.output.decode()}'


def tesseract_7seg(cv2_img):
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.'
    text = pytesseract.image_to_string(cv2_img, config=custom_config)
    return text


def preprocess(image, using_clahe=True, using_blur=False, binarization=True, morphology=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #gray = cv2.convertScaleAbs(gray, alpha=1.2, beta=10)

    if using_clahe:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(gray)
    else:
        contrast_enhanced = cv2.equalizeHist(gray)

    if using_blur:
        blurred = cv2.GaussianBlur(contrast_enhanced, (5, 5), 0)
    else:
        blurred = contrast_enhanced

    if binarization:
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        thresh = blurred

    if morphology:
        kernel = np.ones((3, 3), np.uint8)
        fixed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    else:
        fixed = thresh

    # optional, enhance again
    #fixed = cv2.dilate(fixed, kernel, iterations=1)

    return fixed

if __name__ == "__main__":
    parser = argparse.ArgumentParser("7-Segments OCR")
    parser.add_argument("-i", "--input", help="filename")
    parser.add_argument("--mode", help="Specified the OCR engine", type=str, choices=['ssocr', 'tesseract'], default='ssocr')
    args = parser.parse_args()

    if type(args.input).__name__ != 'NoneType':
        img = cv2.imread(args.input)
        processed_img = preprocess(img, using_clahe=True, using_blur=False, binarization=True, morphology=False)
        cv2.imshow("processed", processed_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if args.mode == 'ssocr':
            print("----- SSOCR -----")
            result = ssocr_7seg(processed_img, 5)
        else:
            print("----- Tesseract -----")
            result = tesseract_7seg(processed_img)
        print("----- Output -----")
        print(f"{result}")
        print("------------------")

