import read_write_json
import argparse
from diffusers import StableDiffusionPipeline
import torch
import os

# example of usage: python generate_images_from_prompts.py --js_file renaissance_evaluation_sample_llava_data.js --model_path TomEijkelenkamp/renaissance-llava-composition --model_name llava --task composition --generations_per_prompt 4

# example of usage: python generate_images_from_prompts.py --js_file evaluation_landscape_data.js --model_path /scratch/s1889338/diffusers/examples/text_to_image/landscape-best-15k --output_folder landscape_2500_generations

parser = argparse.ArgumentParser(description="Generate images from prompts in a js file.")
parser.add_argument('--js_file', type=str, default="prompts.js", help='Path to the js file containing the prompts')
parser.add_argument('--model_path', type=str, default="diffusion-model", help='Path to the model')
# parser.add_argument('--model_name', type=str, default="llava", help='Name of the model')
# parser.add_argument('--task', type=str, default="composition", help='Task to perform')
parser.add_argument('--output_folder', type=str, default="images", help='Path to the output folder')
# parser.add_argument('--generations_per_prompt', type=int, default=20, help='Number of generations per prompt')

args = parser.parse_args()

# if args.output_folder == "images":
#     args.output_folder = f"{args.model_name}_{args.task}_generations"

if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)

# Read the JSON file
data = read_write_json.read_json(args.js_file)

diffusion_model_name = args.model_path.split("/")[-1].replace("-","_")

# Load the model
pipeline = StableDiffusionPipeline.from_pretrained(args.model_path, torch_dtype=torch.float16, use_safetensors=True).to("cuda")

models = ["llava", "cogvlm", "deepseek"]
tasks = ["composition", "balance_elements", "movement", "focus_point", "contrast_elements", "proportion", "foreground_background_4", "symmetry_asymmetry_1", "eye_movement_2"]

for item in data:
    for model in models:
        for task in tasks:
            prompt = data[item][f"{model}_answers"][f"{task}"]

            try:
                image = pipeline(prompt=prompt).images[0]
                image.save(f"{args.output_folder}/{diffusion_model_name}_{model}_{task}_{item.replace('.jpg','')}.png")
            except Exception as e:
                print(f"Error processing {item}: {str(e)}")
