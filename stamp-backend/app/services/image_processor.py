import cv2
import numpy as np
import os
import uuid

def extract_stamp(image_path):
    # Load the image
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Detect blue stamp
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Remove background
    b, g, r = cv2.split(image)
    alpha = mask
    rgba = cv2.merge((b, g, r, alpha))

    filename = f"stamp_{uuid.uuid4()}.png"
    out_path = os.path.join("app/static", filename)
    cv2.imwrite(out_path, rgba)

    return out_path