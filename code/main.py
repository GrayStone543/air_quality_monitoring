import cv2
import pytesseract


def crop_image(img, x, y, width, height):
    clone_img = img.copy()
    cropped_img = clone_img[y:y+height, x:x+width]
    return cropped_img


def main():
    # Open the image file
    img = cv2.imread("../test_data/test2.png")

    # resized_img = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_CUBIC)
    # cropped_img = crop_image(resized_img, 260, 260, 640, 460)

    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, threshold_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

    cv2.imshow("Binary Image", threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Use pytesseract to extract text from the image
    # config = "--oem 3 --psm 3"
    '''
    -l              Specify language(s) (defaults to eng)
    --psm           Page Segmentation Mode (0-13)
    --oem           OCR Engine Mode (0-3)
    -c VAR=VALUE    Set an internal config variable
    '''
    config = r"--psm 7 -c tessedit_char_whitelist=0123456789:"
    text = pytesseract.image_to_string(threshold_image, config=config)

    # Print the extracted text
    print("----- result -----")
    print(text)

    print("Done.")


if __name__ == "__main__":
    main()