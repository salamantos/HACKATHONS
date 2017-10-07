import cv2
import numpy as np

T = 150  # Hyper-parameter


def to_white_and_black(img_url, output_url):
    img = cv2.imread(img_url, 0)  # Translate to White&Black
    mask = np.copy(img)  # Break into pixels arrays
    mask[img > T] = 255
    mask[img <= T] = 0
    cv2.imwrite(output_url, mask)
