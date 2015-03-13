import os
from PIL import Image

def compressLoop(infile, times):
    n = 1
    baseName, e = os.path.splitext(infile)
    try:
        while n <= times:
            f, e = os.path.splitext(infile)
            f = (baseName + str(n))
            outfile = f + ".jpg"
        #open previously generated file
            compImg = Image.open(infile)
        #compress file at 50% of previous quality
            compImg.save(outfile, "JPEG", quality=50)
            
def main():
    infile = str(input("Filename to compress: "))
    times = int(input("Times to process: "))
    compressLoop(infile, times)

main()
