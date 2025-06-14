import cv2
from PIL import Image

# Load the image
img = cv2.imread('classes_test.png')

# Check if image loaded successfully
if img is None:
    raise FileNotFoundError("classes_test.png not found or could not be loaded.")

# Convert to grayscale and threshold to get binary image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours (rectangular boxes)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cropped_images = []
for i, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    # Filter out small contours that are unlikely to be tables
    if w > 50 and h > 20:
        roi = img[y:y+h, x:x+w]
        pil_img = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        filename = f'table_{i}.png'
        pil_img.save(filename)
        cropped_images.append(filename)

print(f"Extracted {len(cropped_images)} tables as PNG files: {cropped_images}")
