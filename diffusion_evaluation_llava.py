import csv
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
import os
from diffusers import StableDiffusionPipeline
import torch

# Stable diffusion model
pipeline = StableDiffusionPipeline.from_pretrained("/scratch/s1889338/diffusers/examples/text_to_image/sd-landscape-model-long/", torch_dtype=torch.float16, use_safetensors=True).to("cuda")

# Llava model and processor initialization
model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf").to("cuda")
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

# Prompt
prompt = "<image>\nUSER: Give a short detailed description of this paintings composition. In this description include answers to each of the following questions: How are all the elements, objects, parts positioned in the whole picture and relative to eachother; Give a description of each of the elements; Is there unity between the elements, colors or overall arrangement; Is there balance between the elements and colors, or in how the parts are laid out in the space; Describe the different colors that are used and how they are used; Is there movement visualized in the painting; Is there rhythm in the visualization of elements, is this rhythm regular, random, flowing, alternating or progressive; Describe the focus point of the painting and how this focus is obtained; Did the artist use contrast in this work, describe uses of light and dark intensities, oposite color uses, contrasting elements; Is there a pattern within the elements, think of circular, triangular or s curve arrangements; Is there use of different proportions and for what purpose? Your answer should be a well structured short paragraph (about 150 words), without repeating concepts. Do not describe what you do not see in the painting.\nASSISTANT:"

output_folder = "results_llava"
# When folder for results does not exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Correct way to open one file for reading and another for writing
with open('output_diffusion_evaluation_llava.csv', mode='w', encoding='utf-8', newline='') as outfile:
        
    # Create a CSV writer object to write to the output file
    writer = csv.writer(outfile)

    # Generate composition descriptions for every image in the images folder
    for image_filename in os.listdir("./images"):

        image_path = os.path.join("./images", image_filename)

        try:
            image = Image.open(image_path)
            image_name = image_filename.split('.')[0]
        
            inputs = processor(text=prompt, images=image, return_tensors="pt").to("cuda")

            # Generate
            generate_ids = model.generate(**inputs, max_length=600)
            result = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

            result_split = result.split('ASSISTANT: ')
            if len(result_split) > 1:
                answer = result_split[1]
            else:
                answer = ""

            test_captions = []

            # Generate 20 different images for each composition description, and create a composition description for each of those images
            for i in range(20):
                image = pipeline(prompt=answer).images[0]
                image.save(f"{output_folder}/{image_name}_{i}.png")

                # Generate
                generate_ids = model.generate(**inputs, max_length=600)
                result = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

                result_split = result.split('ASSISTANT: ')
                if len(result_split) > 1:
                    test_captions.append(result_split[1])
                else:
                    test_captions.append("")

            # Write all the captions to the CSV file
            writer.writerow([image_filename, answer] + test_captions)

        except Exception as e:
            print(f"Error processing {image_filename}: {str(e)}")




  
