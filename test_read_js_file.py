import read_write_json


# Read the JSON file
data = read_write_json.read_json("landscape_data.js")

# print(data.shape)

for item in data:
    print(item)
    prompt = data[item]["llava_answers"]["composition"]
    print(prompt)