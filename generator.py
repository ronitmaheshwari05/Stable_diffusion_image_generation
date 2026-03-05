import requests
import base64
import os
import webbrowser
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")

if not API_KEY:
    print("API key missing")
    exit()

prompt = input("Enter prompt: ")

url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "text_prompts": [
        {
            "text": prompt
        }
    ],
    "cfg_scale": 7,
    "height": 1024,
    "width": 1024,
    "samples": 1,
    "steps": 30
}

print("🚀 Generating image...")

response = requests.post(url, headers=headers, json=payload)

if response.status_code != 200:
    print(" API Error:", response.status_code)
    print(response.text)
    exit()

result = response.json()

image_base64 = result["artifacts"][0]["base64"]

image_bytes = base64.b64decode(image_base64)

filename = "generated_image.png"

with open(filename, "wb") as f:
    f.write(image_bytes)

print(" Image saved:", filename)

webbrowser.open("file://" + os.path.abspath(filename))