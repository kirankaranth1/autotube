import pathlib
import time
from typing import Optional
import requests
from openai import OpenAI


def generate_image(client: OpenAI, prompt: str) -> Optional[str]:
    try:
        output_directory = f"./generated_images/dalle/{str(int(time.time()))}"
        pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        response = requests.get(image_url)

        image_path = output_directory+"/0.jpeg"
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    except Exception as e:
        print("Error: ", str(e))
        return None

