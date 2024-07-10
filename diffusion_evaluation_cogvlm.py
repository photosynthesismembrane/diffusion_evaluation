import csv
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
import os
from diffusers import StableDiffusionPipeline
import torch
import torch
import requests
from PIL import Image
from transformers import AutoModelForCausalLM, LlamaTokenizer
from accelerate import init_empty_weights, infer_auto_device_map, load_checkpoint_and_dispatch
import os
import csv
import json

# Stable diffusion model
pipeline = StableDiffusionPipeline.from_pretrained("/scratch/s1889338/diffusers/examples/text_to_image/sd-landscape-model-cogvlm", torch_dtype=torch.float16, use_safetensors=True).to("cuda")

# Cogvlm model
tokenizer = LlamaTokenizer.from_pretrained('lmsys/vicuna-7b-v1.5')
with init_empty_weights():
    model = AutoModelForCausalLM.from_pretrained(
        'THUDM/cogvlm-chat-hf',
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
device_map = infer_auto_device_map(model, max_memory={0:'20GiB',1:'20GiB','cpu':'16GiB'}, no_split_module_classes=['CogVLMDecoderLayer', 'TransformerLayer'])
model = load_checkpoint_and_dispatch(
    model,
    '/scratch/s1889338/.cache/huggingface/transformers/models--THUDM--cogvlm-chat-hf/snapshots/e29dc3ba206d524bf8efbfc60d80fc4556ab0e3c',   # typical, '~/.cache/huggingface/hub/models--THUDM--cogvlm-chat-hf/snapshots/balabala'
    device_map=device_map,
)
model = model.eval()

# Images folder
images_folder = "./images"

# Prompt
prompt = "Give a detailed description of this paintings composition. In this description include answers to each of the following questions: How are all the elements, objects, parts positioned in the whole picture and relative to eachother; Give a description of each of the elements; Is there unity between the elements, colors or overall arrangement; Is there balance between the elements and colors, or in how the parts are laid out in the space; Describe the different colors that are used and how they are used; Is there movement visualized in the painting; Is there rhythm in the visualization of elements, is this rhythm regular, random, flowing, alternating or progressive; Describe the focus point of the painting and how this focus is obtained; Did the artist use contrast in this work, describe uses of light and dark intensities, oposite color uses, contrasting elements; Is there a pattern within the elements, think of circular, triangular or s curve arrangements; Is there use of different proportions and for what purpose? Your answer should be a well structured paragraph, without repeating concepts. Do not describe what you do not see in the painting."

# output folder
output_folder = "results_cogvlm"

# When folder for results does not exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Correct way to open one file for reading and another for writing
with open('output_diffusion_evaluation_cogvlm.csv', mode='w', encoding='utf-8', newline='') as outfile:
        
    # Create a CSV writer object to write to the output file
    writer = csv.writer(outfile)
    
    # Generate composition descriptions for every image in the images folder
    for image_filename in os.listdir(images_folder):

        image_path = os.path.join(images_folder, image_filename)
        image_name = image_filename.split('.')[0]
        image = Image.open(image_path).convert('RGB')
        
        inputs = model.build_conversation_input_ids(tokenizer, query=prompt, history=[], images=[image])  # chat mode
        inputs = {
            'input_ids': inputs['input_ids'].unsqueeze(0).to('cuda'),
            'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to('cuda'),
            'attention_mask': inputs['attention_mask'].unsqueeze(0).to('cuda'),
            'images': [[inputs['images'][0].to('cuda').to(torch.bfloat16)]],
        }
        gen_kwargs = {"max_length": 2048, "do_sample": False}

        with torch.no_grad():
            outputs = model.generate(**inputs, **gen_kwargs)
            outputs = outputs[:, inputs['input_ids'].shape[1]:]

            caption = tokenizer.decode(outputs[0])

            test_captions = []

            # Generate 20 different images for each composition description, and create a composition description for each of those images
            for i in range(20):
                image = pipeline(prompt=caption).images[0]
                image.save(f"{output_folder}/{image_name}_{i}.png")
                        
                inputs = model.build_conversation_input_ids(tokenizer, query=prompt, history=[], images=[image])  # chat mode
                inputs = {
                    'input_ids': inputs['input_ids'].unsqueeze(0).to('cuda'),
                    'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to('cuda'),
                    'attention_mask': inputs['attention_mask'].unsqueeze(0).to('cuda'),
                    'images': [[inputs['images'][0].to('cuda').to(torch.bfloat16)]],
                }
                gen_kwargs = {"max_length": 2048, "do_sample": False}

                with torch.no_grad():
                    outputs = model.generate(**inputs, **gen_kwargs)
                    outputs = outputs[:, inputs['input_ids'].shape[1]:]

                    test_captions.append(tokenizer.decode(outputs[0]))

            # Write all the captions to the CSV file
            writer.writerow([image_filename, caption] + test_captions)





  
