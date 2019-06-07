#!/usr/bin/env python3

import cv2
import sys
import os
from os import walk


if len(sys.argv) < 2:
    print()
    print("ERROR unknown parameters")
    print()
    print("--dir <dir>               |  directory with files to be resized")
    print("--size <size x> <size y>  |  target size for images")
    print("--calc                    |  calculate average size")
    print()
    exit(1)

directory = ""
calc = False
target_width = 0
target_height = 0

skipIteration = False
skipTwice = False


for i in range(1, len(sys.argv)):
    if skipIteration:
        if not skipTwice:
            skipIteration = False
        else:
            skipTwice = False
        continue

    if sys.argv[i] == "--dir":
        directory = sys.argv[i+1]
        skipIteration = True
    elif sys.argv[i] == "--size":
        target_width = int(sys.argv[i+1])
        target_height = int(sys.argv[i+2])
        skipIteration = True
        skipTwice = True
    elif sys.argv[i] == "--calc":
        calc = True
    else:
        print("ERROR unknown argument " + sys.argv[i])
        print()
        exit(1)

if not calc and directory == "":
    print("ERROR --dir argument missing")
    print()
    exit(1)
if not calc and target_width == 0:
    print("ERROR target_width missing. ")
    print()
    exit(1)
if not calc and target_height == 0:
    print("ERROR target_height missing")
    print()
    exit(1)

if directory[len(directory)-1] == "/":
    directory = directory[0:len(directory)-1]

all_files = ""
for (dirpath, dirnames, filenames) in walk("./"):
    if dirpath == "./" + directory or dirpath == directory:
        all_files = filenames
        break

print("loading files and calculating average dimensions...")


if calc:
    width_avg = 0
    height_avg = 0
    count = 0

    for file in all_files:
        #print(directory + "/" + file)
        img = cv2.imread(directory + "/" + file)
        #print(img.shape)
        width = img.shape[1]
        width_avg += width
        height = img.shape[0]
        height_avg += height
        count += 1
        #print(str(width) + " | " + str(height))

    if count < 1:
        print("Could not load files")
        print()
        exit(1)

    print("Average dimensions:")
    print(str(width_avg/count) + " | " + str(height_avg/count))
else:
    for file in all_files:
        print(directory + "/" + file)
        img = cv2.imread(directory + "/" + file)
        img = cv2.resize(img, (target_width, target_height
                               ))
        #cv2.imshow(str(file), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if not os.path.exists(directory + "_resized"):
            os.makedirs(directory + "_resized")
        cv2.imwrite("./" + directory + "_resized/" + file, img)
        print("resized and saved: " + "./" + directory + "_resized/" + file)