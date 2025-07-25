# This file is no longer needed because we do these functions in the other helpers
from PIL import Image
from pathlib import Path


def crop_right_half(image_path):
    # Open the image
    img = Image.open(image_path)
    # Get the size (width, height)
    width, height = img.size
    # Define the cropping box: (left, upper, right, lower)
    # For the right half: start at width//2, go to width
    box = (width // 2, 0, width, height)
    # Crop and return the right half
    right_half = img.crop(box)
    return right_half


output_sbs_path = Path("/home/alex/Downloads/images_cropped/sample/right/outputs")

for path in output_sbs_path.rglob('*.png'):
    print(path)
    right_half_image = crop_right_half(path)
    new_filename = path.parent.joinpath(path.name.replace('Full_SBS', 'R'))
    #new_filename = f"{path.name.replace('Full_SBS', 'R')}"
    print(new_filename)
    right_half_image.save(new_filename)




