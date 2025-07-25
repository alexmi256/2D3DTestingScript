from PIL import Image
from pathlib import Path
from imgcompare import image_diff_percent
import statistics
from tabulate import tabulate
from multiprocessing import Pool
import re

images= []


gt_image_path = Path("/home/alex/Downloads/images_cropped/sample/left/")
gt_images = gt_image_path.glob('*.png')
gt_images_small = []

for i, x in enumerate(gt_images):
    if i % 10 == 0:
        gt_images_small.append(x)

#print(len(gt_images_small))

print('source .venv/bin/activate')
for image in gt_images_small:
    image_name = image.name
    generated_image_folder = image.stem.replace('_L', '_R')
    model = 'ZoeD_Any_N'
    convergence = 0.2
    divergence = 1.0
    foreground_scale = 0
    edge_dilation = False
    depth_aa = False
    tta = False

    command = f"mkdir ~/Downloads/images_cropped/sample/param_generated/{generated_image_folder}; python3 -m iw3.cli --input ~/Downloads/images_cropped/sample/left/{image.name} --synthetic-view right --yes --depth-model {model} --find-param {{divergence,convergence,foreground-scale}} --output ~/Downloads/images_cropped/sample/param_generated/{generated_image_folder}/"
    if edge_dilation and 'Any' in model:
        command += f" --edge-dilation 2"
    if depth_aa:
        command += f" --depth-aa"
    if tta:
        command += f" --tta"

    print(command)

print(f"\nrm run_commands.sh && nano run_commands.sh && chmod +x run_commands.sh")