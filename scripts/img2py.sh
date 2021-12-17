#!/usr/bin/env python

import os
from wx.tools.img2py import img2py

outputFile = "./crypto.py"
try:
    os.remove(outputFile)
except:
    pass

for (thisDir, ignored, names) in os.walk("."):
    for x in names:
        (fileName, ext) = os.path.splitext(x)
        if ext in (".png", ".bmp"):
            img2py(x, outputFile, append=os.path.exists(outputFile), imgName=fileName.capitalize())
