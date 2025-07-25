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
images_left_gt = Path("/home/alex/Downloads/images_cropped/sample/left")


def calculate_score_for_image(image_right_gt: Path):

    image_left_gt_path = images_left_gt.joinpath(f'{image_right_gt.name[0:6]}_L.png')

    data = {
        'image_left_gt_path': image_left_gt_path,
        'image_right_gt_path': image_right_gt,
        "score": None
    }

    try:
        image_left_gt = Image.open(image_left_gt_path)
        image_right_gt = Image.open(image_right_gt)
        #data['score'] = image_diff_percent(image_gen.convert('L'), image_gt_img.convert('L'))
        data['score'] = image_diff_percent(image_left_gt.convert('RGB'), image_right_gt.convert('RGB'))
    except FileNotFoundError:
        pass
        #print(f"Ground truth image '{image_gt_path}' not found, skipping")

    return data


right_gt_images = list(images_right_gt.rglob('*.png'))


with Pool() as pool:                        # Create a multiprocessing Pool
    results = list(tqdm.tqdm(pool.imap_unordered(calculate_score_for_image, right_gt_images), total=len(right_gt_images)))

results = [x for x in results if x['score'] is not None]
mean = round(statistics.mean([x['score'] for x in results]), 4)
print(f'Score: {mean}')
