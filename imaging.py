import glob
import os
import time
import uuid
from PIL import Image, ImageChops, ImageEnhance

# applyELA applies the Error Level Analysis algorithm to an image and returns a 
# tuple made of the difference percentage and the difference image
def applyELA(original):
    # Compress file at 75% of previous quality like mentioned in the paper
    tmpfile = "tmp/" + uuid.uuid4().hex + ".jpg"
    original.save(tmpfile, "jpeg", quality=75) 
    compressed = Image.open(tmpfile)
    os.remove(tmpfile)
    # Find the difference between the images
    ela_image = ImageChops.difference(original, compressed)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    return (max_diff, ela_image)


# cleanImages removes images older than 15 minutes
def cleanImages():
    files = glob.glob("tmp/*.jpg")
    for f in files:
        if os.stat(f).st_ctime < time.time() - 15*60*60:
            os.remove(f)
