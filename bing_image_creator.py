import json
from typing import Optional

from BingImageCreator import ImageGen
import time
import pathlib

cookie = ""
cookie_json = None
with open("www.bing.com_cookies.json", encoding="utf-8") as file:
    cookie_json = json.load(file)

image_generator = ImageGen(
    cookie,
    None,
    all_cookies=cookie_json
)


def generate_image(prompt: str) -> Optional[str]:
    output_directory = f"./generated_images/bing/{str(int(time.time()))}"
    pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)

    try:
        images = image_generator.get_images(prompt)
        actual_images = [s for s in images if "th/id" in s and not s.endswith(".")]
        print("images: ", actual_images)
        image_generator.save_images(
            actual_images,
            output_dir=output_directory,
            download_count=1,
        )
        return f"{output_directory}/0.jpeg"
    except Exception as e:
        print("Error generating image from bing: ", str(e))
        return None

generate_image("An elephant on a tall building")