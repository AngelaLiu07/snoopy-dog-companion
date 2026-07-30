from PIL import Image
import io
import requests
import urllib.parse
import random


# from documentation on hugging face github (text to image generation)
def img_gen(input_prompt: str) -> Image.Image:
    encoded_prompt = urllib.parse.quote(input_prompt)
    random_seed = random.randint(1, 999999)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={random_seed}"
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        raise Exception(f"Pollinations API Error {response.status_code}: {response.text}")
    
