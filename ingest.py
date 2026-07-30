import json
import os
import base64
from ollama import chat
from ollama import ChatResponse
from ollama import Client
from ollama import embed
from pathlib import Path
import chromadb
import mimetypes
from schemas import ImageDetails
import time
# function to convert images to base64
def to_base64(filepath : str) -> str:
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# get the list of filenames from the directory images
filenames = os.listdir('images')

filepaths = []
types = []
# get filepath for each file ex. images/exhausted_sad_snoopy.jpeg
# get mime_type for each file
for name in filenames:
    filepaths.append(os.path.join('images/', name))
    types.append(mimetypes.guess_type(name))

image_prompt = '''
Identify the following key features from each image:
1. Title of the image which should be a phrase that captures the essence of the image
2. 10 keywords from the image (1-2 words in length) that can be used to match a certain action, emotion, or archetype to that image

Use only the image and your knowledge of Snoopy and the characters in Peanut to get the title and keywords. Ensure that each image has 10 keywords.
Your response should match the ImageDetails schema, formatted in a json file
'''

client = Client()

raw_results = {}

#loop through the filepaths and filenames lists, passing the information and prompt into Gemini
# store the results of the response in raw_results
for file, name in zip(filepaths, filenames):
    interaction = chat(
        model='gemma3:4b',
        format=ImageDetails.model_json_schema(),
        messages=[
            {
            'role': 'user',
            'content': image_prompt,
            'images': [Path(file)],
            }
        ]
    )
    raw_results[file] = interaction.message.content

parsed_results = {}

# Validate the data and store as a dictionary
for name, raw_json in raw_results.items():
    try:
        # model_validate_json is a Pydantic method that directly validates (much faster than json.loads)
        parsed = ImageDetails.model_validate_json(raw_json)
        # convert BaseModel object into standard Python dict 
        parsed_results[name] = parsed.model_dump()
    except Exception as e:
        print(f"Error parsing {name}: {e}")
        parsed_results[name] = {'error': str(e)}

# initialize Chromadb
client = chromadb.PersistentClient(path="./my_chroma_data")

coll = client.get_or_create_collection(name = 'snoopy_images')
for filepath, data in parsed_results.items():
    caption = data['title']
    keywords = data['keywords']
    doc_text = f"An image titled {caption}, with associated tags {','.join(keywords)}."

    interaction = embed(model='nomic-embed-text', input=doc_text)
    coll.add(
        ids = [filepath],
        embeddings = interaction['embeddings'][0],
        metadatas = [{'image_file': filepath, 'title' : caption, 'keywords': ', '.join(keywords)}]
    )









