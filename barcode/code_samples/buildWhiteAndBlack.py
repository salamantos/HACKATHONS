import cv2
import numpy as np
inf = 1000000000


img_url = "/home/dmitry/Code/Hackaton/mABBYYlity_hackatone_CoddingKittens/barcode/test_samples/test.jpg"
img = cv2.imread(img_url,0)

mask = np.copy(img)
t = 150
mask[img > t] = 255
mask[img <= t] = 0
cv2.imwrite('/home/dmitry/Code/Hackaton/mABBYYlity_hackatone_CoddingKittens/barcode/test_samples/result.bmp',mask)