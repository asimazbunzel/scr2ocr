#!/usr/bin/env python

import os
import platform
from tkinter import Tk, Button

import jamspell
import pyperclip
import pytesseract
from PIL import ImageGrab


REFRESH = 100  # in milliseconds
WIDTH, HEIGHT = (280, 100)
ALPHA = 0.55
FLAGS = r'--oem 3 --psm 6 -l spa'

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'tesseract\tesseract.exe'
    os.environ["TESSDATA_PREFIX"] = r'tesseract\tessdata'

else:
    pytesseract.pytesseract.tesseract_cmd = "./bin/tesseract"
    os.environ["TESSDATA_PREFIX"] = "./tessdata"
    os.environ["LD_LIBRARY_PATH"] = "."

    print("\nLoading JamSpell model...", end="")
    corr = jamspell.TSpellCorrector()
    corr.LoadLangModel("./jamspell/model.bin")
    print(" done")

def capture(corr=None):
    x, y = root.winfo_x(), root.winfo_y()
    w, h = root.winfo_width(), root.winfo_height()

    img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
    text = pytesseract.image_to_string(img, config=FLAGS)

    if corr:
        text = corr.FixFragment(text)

    pyperclip.copy(text)


if __name__ == "__main__":
    root = Tk()
    root.title("scr2ocr")
    root.geometry(f"{WIDTH}x{HEIGHT}")

    # Linux transparency workaround, try `root.wm_attributes('-transparentcolor', root["bg"])` on Windows
    root.wait_visibility(root)
    root.wm_attributes("-alpha", ALPHA)

    button = Button(root, command=lambda: capture(corr=corr), relief="groove", borderwidth=2)
    button.pack(side="top", expand=True)

    root.mainloop()
