from PIL import Image
from pathlib import Path
from imgcompare import image_diff_percent
import statistics
from tabulate import tabulate
from multiprocessing import Pool
import re
import tqdm

ground_truth_images = {}
scores = {}
model_name = 'ZoeD_Any_N'

gt_image_dir = Path("/home/alex/Downloads/images_cropped/sample/right/")
generated_images_path = Path(f"/home/alex/Downloads/images_cropped/sample/param_generated/")


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


def calculate_score_for_image(image_gen_path):
    # determine image number

    # This is the ground truth right image
    image_name = image_gen_path.parents[0].name
    gt_image_path = Path(str(gt_image_dir.joinpath(image_name)) + image_gen_path.suffix)

    # This will be the right generated image that is cropped
    image_gen = crop_right_half(image_gen_path)

    # print(image_gen_path)
    # print(image_model)
    # print(image_gt_path)

    data = {
        'model_name': model_name,
        'ground_truth_image_path': gt_image_path,
        'generated_image_path': image_gen_path,
        'divergence': int(re.findall(r'_d(\d+)', image_gen_path.name)[0]),
        'convergence': int(re.findall(r'_c(\d+)', image_gen_path.name)[0]),
        'di': int(re.findall(r'_di(\d+)', image_gen_path.name)[0]),
        'foreground_scale': int(re.findall(r'_fs(\d+)', image_gen_path.name)[0]),
        'ipd': int(re.findall(r'_ipd(\d+)', image_gen_path.name)[0]),
        "score": None
    }

    try:
        image_gt_img = Image.open(gt_image_path)
        data['score'] = image_diff_percent(image_gen.convert('RGB'), image_gt_img.convert('RGB'))
    except FileNotFoundError:
        pass
        #print(f"Ground truth image '{image_gt_path}' not found, skipping")

    return data

    # ground_truth_images[image_model].append(score)

generated_images = list(generated_images_path.rglob('*.png'))



with Pool() as pool:                        # Create a multiprocessing Pool
    results = list(tqdm.tqdm(pool.imap_unordered(calculate_score_for_image, generated_images), total=len(generated_images)))


results = [x for x in results if x['score'] is not None]

scores_divergence = {}
scores_convergence = {}
scores_foreground_scale = {}

for result in results:
    combination = f"d{result['divergence']}_c{result['convergence']}_fs{result['foreground_scale']}"
    divergence = result['divergence']
    convergence = result['convergence']
    foreground_scale = result['foreground_scale']

    if combination not in scores:
        scores[combination] = []
    if divergence not in scores_divergence:
        scores_divergence[divergence] = []
    if convergence not in scores_convergence:
        scores_convergence[convergence] = []
    if foreground_scale not in scores_foreground_scale:
        scores_foreground_scale[foreground_scale] = []


    if result['score'] is not None:
        scores[combination].append(result['score'])
        scores_divergence[divergence].append(result['score'])
        scores_convergence[convergence].append(result['score'])
        scores_foreground_scale[foreground_scale].append(result['score'])

# Make into rows with means so we can output a table
rows = []
for param_combination, scores in scores.items():
    rows.append([param_combination, round(statistics.mean(scores), 4)])

rows = sorted(rows, key=lambda x: x[1], reverse=True)
print(tabulate(rows, headers=["Combination", "Score"], tablefmt="github"))
print()

rows_divergence = []
for param_combination, scores in scores_divergence.items():
    rows_divergence.append([param_combination, round(statistics.mean(scores), 4)])

rows_divergence = sorted(rows_divergence, key=lambda x: x[1], reverse=True)
print(tabulate(rows_divergence, headers=["Divergence", "Score"], tablefmt="github"))
print()

rows_convergence = []
for param_combination, scores in scores_convergence.items():
    rows_convergence.append([param_combination, round(statistics.mean(scores), 4)])

rows_convergence = sorted(rows_convergence, key=lambda x: x[1], reverse=True)
print(tabulate(rows_convergence, headers=["Convergence", "Score"], tablefmt="github"))
print()

rows_foreground_scale = []
for param_combination, scores in scores_foreground_scale.items():
    rows_foreground_scale.append([param_combination, round(statistics.mean(scores), 4)])

rows_foreground_scale = sorted(rows_foreground_scale, key=lambda x: x[1], reverse=True)
print(tabulate(rows_foreground_scale, headers=["Foreground Scale", "Score"], tablefmt="github"))