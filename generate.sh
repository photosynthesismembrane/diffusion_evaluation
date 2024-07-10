#!/bin/bash
#SBATCH --time=0-03:59:00
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=a100
#SBATCH --job-name=evaluate
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

python generate_images_from_prompts.py --js_file renaissance_evaluation_sample_llava_data.js --model_path /scratch/s1889338/diffusers/examples/text_to_image/renaissance-llava-composition --model_name llava --task composition --generations_per_prompt 10
python generate_images_from_prompts.py --js_file renaissance_evaluation_sample_llava_data.js --model_path /scratch/s1889338/diffusers/examples/text_to_image/renaissance-llava-contrast --model_name llava --task contrast_elements --generations_per_prompt 10
python generate_images_from_prompts.py --js_file renaissance_evaluation_sample_llava_data.js --model_path /scratch/s1889338/diffusers/examples/text_to_image/renaissance-llava-focus --model_name llava --task focus_point --generations_per_prompt 10

deactivate
