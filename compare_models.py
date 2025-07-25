from PIL import Image
from pathlib import Path
from imgcompare import image_diff_percent
import statistics
from tabulate import tabulate
from multiprocessing import Pool
import tqdm

ground_truth_images = {}
scores = {}

images_right_gt = Path("/home/alex/Downloads/images_cropped/sample/right")
images_right_generated = Path("/home/alex/Downloads/images_cropped/sample/right_generated")


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
    # determine model
    image_model = image_gen_path.parents[0].name
    if image_model not in ground_truth_images:
        ground_truth_images[image_model] = []

    image_gen = crop_right_half(image_gen_path)

    # print(image_gen_path)
    # print(image_model)
    image_gt_path = images_right_gt.joinpath(f'{image_gen_path.name[0:6]}_R.png')
    # print(image_gt_path)

    data = {
        'model_name': image_model,
        'ground_truth_image_path': image_gt_path,
        'generated_image_path': image_gen_path,
        "score": None
    }

    try:
        image_gt_img = Image.open(image_gt_path)
        #data['score'] = image_diff_percent(image_gen.convert('L'), image_gt_img.convert('L'))
        data['score'] = image_diff_percent(image_gen.convert('RGB'), image_gt_img.convert('RGB'))
    except FileNotFoundError:
        pass
        #print(f"Ground truth image '{image_gt_path}' not found, skipping")

    return data

    # ground_truth_images[image_model].append(score)

generated_images = list(images_right_generated.rglob('*.png'))


with Pool() as pool:                        # Create a multiprocessing Pool
    results = list(tqdm.tqdm(pool.imap_unordered(calculate_score_for_image, generated_images), total=len(generated_images)))

results = [x for x in results if x['score'] is not None]

for result in results:
    if result['model_name'] not in scores:
        scores[result['model_name']] = []
    if result['score'] is not None:
        scores[result['model_name']].append(result['score'])


# Make into rows with means so we can output a table
rows = []
for depth_model, scores in scores.items():
    rows.append([depth_model, round(statistics.mean(scores), 4)])

rows = sorted(rows, key=lambda x: x[1], reverse=True)
print(tabulate(rows, headers=["Model", "Score"], tablefmt="github"))