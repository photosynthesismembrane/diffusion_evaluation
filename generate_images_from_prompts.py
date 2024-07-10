import read_write_json
import argparse
from diffusers import StableDiffusionPipeline
import torch
import os

# example of usage: python generate_images_from_prompts.py --js_file renaissance_evaluation_sample_llava_data.js --model_path TomEijkelenkamp/renaissance-llava-composition --model_name llava --task composition --generations_per_prompt 4

parser = argparse.ArgumentParser(description="Generate images from prompts in a js file.")
parser.add_argument('--js_file', type=str, default="prompts.js", help='Path to the js file containing the prompts')
parser.add_argument('--model_path', type=str, default="diffusion-model", help='Path to the model')
parser.add_argument('--model_name', type=str, default="llava", help='Name of the model')
parser.add_argument('--task', type=str, default="composition", help='Task to perform')
parser.add_argument('--output_folder', type=str, default="images", help='Path to the output folder')
parser.add_argument('--generations_per_prompt', type=int, default=20, help='Number of generations per prompt')

args = parser.parse_args()

if args.output_folder == "images":
    args.output_folder = f"{args.model_name}_{args.task}_generations"

if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)

# Read the JSON file
data = read_write_json.read_json(args.js_file)

# Load the model
pipeline = StableDiffusionPipeline.from_pretrained(args.model_name, torch_dtype=torch.float16, use_safetensors=True).to("cuda")

for item in data:
    prompt = data[item][f"{args.model_name}_answers"][f"{args.task}"]

    for i in range(args.generations_per_prompt):
        try:
            image = pipeline(prompt=prompt).images[0]
            image.save(f"{args.output_folder}/{args.model_name}_{args.task}_{item}_{i}.png")
        except Exception as e:
            print(f"Error processing {item}: {str(e)}")
