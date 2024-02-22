from typing import Optional

from PIL import Image
import dalle_image_creator
import bing_image_creator
from openai import OpenAI

def overlay_image(foreground_img_src: str,
                  bg_img_src: str = "",
                  target_img_path: str = "target_overlay_image.png",
                  foreground_img_x: int = None,
                  foreground_img_y: int = None,
                  foreground_ratio: float = None,
                  result_width: int = 1920,
                  result_height: int = 1080) -> str:
    f_img = Image.open(foreground_img_src)
    b_img = Image.open(bg_img_src) if(bg_img_src) else Image.new("RGB", (result_width, result_height))
    f_size = f_img.size
    b_size = b_img.size

    ratio = float(min(b_size)) / max(f_size) if not foreground_ratio else float(foreground_ratio)
    new_size_without_padding = (int(f_size[0] * ratio), int(f_size[1] * ratio))
    f_img = f_img.resize(new_size_without_padding, Image.LANCZOS)
    img_x = foreground_img_x if foreground_img_x is not None else (b_size[0] - new_size_without_padding[0]) // 2
    img_y = foreground_img_y if foreground_img_y is not None else (b_size[1] - new_size_without_padding[1]) // 2

    if bg_img_src:
        b_img.paste(f_img, (img_x, img_y), f_img)
    else:
        b_img.paste(f_img, (img_x, img_y))
    print(f"Writing image to {target_img_path}")
    b_img.save(target_img_path)

    return target_img_path

def overlay_left(foreground_img_src: str,
                 bg_img_src: str,
                 foreground_ratio: float,
                 target_img_path: str = "target_overlay_image.png",
                 result_width: int = 1920,
                 result_height: int = 1080) -> str:
    f_img = Image.open(foreground_img_src)
    b_img = Image.open(bg_img_src)
    f_size = f_img.size
    b_size = b_img.size

    f_img_resized = f_img.resize((int(f_size[0] * foreground_ratio), int(f_size[1] * foreground_ratio)), Image.LANCZOS)

    final_x = 0
    final_y = (b_size[1] - f_img_resized.size[1])

    return overlay_image(foreground_img_src, bg_img_src, target_img_path, final_x, final_y, foreground_ratio,
                         result_width, result_height)

def overlay_right(foreground_img_src: str,
                 bg_img_src: str,
                 foreground_ratio: float,
                 target_img_path: str = "target_overlay_image.png",
                 result_width: int = 1920,
                 result_height: int = 1080) -> str:
    f_img = Image.open(foreground_img_src)
    b_img = Image.open(bg_img_src)
    f_size = f_img.size
    b_size = b_img.size

    f_img_resized = f_img.resize((int(f_size[0] * foreground_ratio), int(f_size[1] * foreground_ratio)), Image.LANCZOS)

    final_x = (b_size[0] - f_img_resized.size[0])
    final_y = (b_size[1] - f_img_resized.size[1])

    return overlay_image(foreground_img_src, bg_img_src, target_img_path, final_x, final_y, foreground_ratio,
                         result_width, result_height)

def overlay_bottom_center(foreground_img_src: str,
                  bg_img_src: str,
                  foreground_ratio: float,
                  target_img_path: str = "target_overlay_image.png") -> str:
    f_img = Image.open(foreground_img_src)
    b_img = Image.open(bg_img_src)
    f_size = f_img.size
    b_size = b_img.size

    f_img_resized = f_img.resize((int(f_size[0] * foreground_ratio), int(f_size[1] * foreground_ratio)), Image.LANCZOS)

    final_x = (b_size[0] - f_img_resized.size[0])//2
    final_y = (b_size[1] - f_img_resized.size[1])

    return overlay_image(foreground_img_src, bg_img_src, target_img_path, final_x, final_y, foreground_ratio)


def generate_image_with_fallback(client: OpenAI, prompt: str) -> Optional[str]:
    #return dalle_image_creator.generate_image(client, prompt)
    generated_image = bing_image_creator.generate_image(prompt)
    if generated_image:
        return generated_image
    else:
        return dalle_image_creator.generate_image(client, prompt)
