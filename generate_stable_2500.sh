#!/bin/bash
#SBATCH --time=0-23:59:00
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=a100
#SBATCH --job-name=sd_generate
#SBATCH --mem=50G
module purge
module load CUDA/12.1.1
module load Python/3.11.3-GCCcore-12.3.0
module load GCCcore/12.3.0

source ../../venv/bin/activate

export HF_DATASETS_CACHE="/scratch/$USER/.cache/huggingface/datasets"
export HF_HOME="/scratch/$USER/.cache/huggingface/transformers"

pip install --upgrade pip
pip install torch torchvision
pip install diffusers
pip install transformers
pip install accelerate
pip install huggingface_hub

accelerate config default

huggingface-cli login --token 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

python generate_images_from_prompts.py --js_file evaluation_renaissance_data.js --model_path runwayml/stable-diffusion-v1-5 --output_folder renaissance_2500_generations
python generate_images_from_prompts.py --js_file evaluation_landscape_data.js --model_path runwayml/stable-diffusion-v1-5 --output_folder landscape_2500_generations
python generate_images_from_prompts.py --js_file evaluation_abstract_data.js --model_path runwayml/stable-diffusion-v1-5 --output_folder abstract_2500_generations

deactivate
