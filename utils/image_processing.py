from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'


def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert("L")  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Enhance contrast
    image = ImageOps.autocontrast(image)
    image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Thresholding
    return image

# def preprocess_image(image_path):
#     """
#     Preprocess the image using OpenCV techniques for OCR optimization.
#     :param image_path: Path to the image to preprocess.
#     :return: Preprocessed PIL Image ready for OCR.
#     """
#     # Read the image using OpenCV
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

#     # Step 1: Resize the image to ensure consistent OCR results
#     image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

#     # Step 2: Apply Gaussian Blur to reduce noise
#     blurred = cv2.GaussianBlur(image, (5, 5), 0)

#     # Step 3: Adaptive Thresholding for binarization
#     adaptive_thresh = cv2.adaptiveThreshold(
#         blurred,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     # Step 4: Morphological transformations to improve text contours
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     morph = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

#     # Step 5: Invert colors (if needed, based on the OCR engine's preference)
#     inverted = cv2.bitwise_not(morph)

#     # Convert back to PIL Image for compatibility with pytesseract
#     processed_image = Image.fromarray(inverted)

#     return processed_image


def extract_raw_text(image_path):
    """
    Extract raw text from an image using OCR.
    """
    image = preprocess_image(image_path)
    return pytesseract.image_to_string(image)
