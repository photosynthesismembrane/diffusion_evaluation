import os
from PIL import Image
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Check how many images have a similar height and width dimension.")
# parser.add_argument('--folder', type=str, required=True, help="Path to the folder of images.")
parser.add_argument('--threshold', type=float, default=.3, help="Max difference ratio.")
args = parser.parse_args()

total_similar = 0
total_different = 0

# base_folder = "C:\\Users\\tomei\\OneDrive\\Documenten\\wikiart"
# folders = [
#     "Abstract_Expressionism",
#     "Action_Painting",
#     "Color_Field_Painting",
#     "Fauvism",
#     "Pop_Art"
# ]
base_folder = "C:\\Users\\tomei\\OneDrive\\Documenten\\GitHub\\image_similarity_clustering\\wikiart_50_clusters"
folders = [
    "cluster_12",
    "cluster_4",
    "cluster_16"
]


save_folder = "landscape_odd_dimensions"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

for folder in folders:
        
    # Check if the folder exists
    if not os.path.exists(os.path.join(base_folder, folder)):
        print(f"Folder {folder} does not exist.")

    # Check for every image in the folder Whether the height and width are close to the same
    for img_filename in os.listdir(os.path.join(base_folder, folder)):
        img_path = os.path.join(base_folder, folder, img_filename)
        img = Image.open(img_path)
        width, height = img.size
        width_height_ratio = width / height
        if width_height_ratio < 1-args.threshold or width_height_ratio > 1+args.threshold:
            total_different +=1
            # print(f"Image {img} in folder {folder} has different dimensions: {width}x{height}")
            # Save the image to the output folder
            img.save(f"{save_folder}/{img_filename}")
        else:
            total_similar += 1
            # print(f"Image {img} in folder {folder} has the same dimensions: {width}x{height}")


    print(f"Folder {folder} has {total_similar} images with the similar dimensions and {total_different} images with different dimensions.")
