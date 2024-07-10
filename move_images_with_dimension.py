import os
from PIL import Image
import argparse

# Example usage: py move_images_with_dimension.py --folder C:\Users\tomei\OneDrive\Documenten\GitHub\caption_generator_and_interface\renaissance_complete --threshold .2 --output_folder renaissance_odd_dimensions

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Check how many images have a similar height and width dimension.")
parser.add_argument('--folder', type=str, required=True, help="Path to the folder of images.")
parser.add_argument('--threshold', type=float, default=.1, help="Max difference ratio.")
parser.add_argument('--output_folder', type=str, default="images", help='Path to the output folder')
args = parser.parse_args()

total_similar = 0
total_different = 0
    
# Check if the folder exists
if not os.path.exists(args.folder):
    print(f"Folder {args.folder} does not exist.")

if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)

# Check for every image in the folder Whether the height and width are close to the same
for img in os.listdir(args.folder):
    if img.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        img_path = os.path.join(args.folder, img)
        img_item = Image.open(img_path)
        width, height = img_item.size
        width_height_ratio = width / height
        if width_height_ratio < 1-args.threshold or width_height_ratio > 1+args.threshold:
            # Copy the image to the output folder
            img_item.save(f"{args.output_folder}/{img}")