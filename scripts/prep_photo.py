"""
prep_photo.py
-------------
Portrait pipeline step 1:
  - Remove background using rembg
  - Composite onto pure white (background becomes spaces in ASCII art)
  - Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to boost detail

Usage:
    python prep_photo.py <source-photo.jpg>

Output:
    source-prepped.png
"""

import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image


def prep_photo(input_path: str, output_path: str = "source-prepped.png") -> None:
    print(f"Processing {input_path}...")

    # 1. Remove background
    input_image = Image.open(input_path)
    subject_only = remove(input_image)

    # 2. Composite onto pure white so background becomes spaces in ASCII
    white_bg = Image.new("RGBA", subject_only.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, subject_only).convert("L")

    # 3. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    img_cv = np.array(composite)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    high_contrast = clahe.apply(img_cv)

    cv2.imwrite(output_path, high_contrast)
    print(f"Saved prepped image to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <source-photo.jpg>")
        sys.exit(1)
    prep_photo(sys.argv[1])
