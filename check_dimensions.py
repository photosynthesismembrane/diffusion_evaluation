import os
from PIL import Image
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Check how many images have a similar height and width dimension.")
parser.add_argument('--folder', type=str, required=True, help="Path to the folder of images.")
parser.add_argument('--threshold', type=float, default=.1, help="Max difference ratio.")
args = parser.parse_args()

total_similar = 0
total_different = 0
    
# Check if the folder exists
if not os.path.exists(args.folder):
    print(f"Folder {args.folder} does not exist.")

# Check for every image in the folder Whether the height and width are close to the same
for img in os.listdir(args.folder):
    img_path = os.path.join(args.folder, img)
    img = Image.open(img_path)
    width, height = img.size
    width_height_ratio = width / height
    if width_height_ratio < 1-args.threshold or width_height_ratio > 1+args.threshold:
        total_different +=1
        # print(f"Image {img} in folder {folder} has different dimensions: {width}x{height}")
    else:
        total_similar += 1
        # print(f"Image {img} in folder {folder} has the same dimensions: {width}x{height}")

print(f"Folder {args.folder} has {total_similar} images with the similar dimensions and {total_different} images with different dimensions.")
