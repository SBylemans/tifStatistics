from PIL import Image
from PIL.TiffTags import TAGS
import sys

Image.MAX_IMAGE_PIXELS = 933120000

with Image.open(sys.argv[1]) as img:
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag if TAGS[key] == 'BitsPerSample'}
    print(meta_dict)
