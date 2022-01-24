import pyautogui as py #Import pyautogui
import time #Import Time

while True: #Start loop
    print (py.position())
    time.sleep(1)

# import pyscreenshot
# import numpy as np
# from PIL import Image
  
# # To capture the screen
# image = pyscreenshot.grab()
  
# # To save the screenshot
# image.save("img.png")

# img = Image.open("img.png")
# pixels = np.array(img)

# found = False

# for i in range(230, 600, 70):
#   for j in range(792, 1080, 70):
#     print(pixels[i][j])
#   print("\n")