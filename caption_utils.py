import pathlib
from typing import Optional
import os
from PIL import Image
from PIL.ImageFilter import *
from pynter.pynter import generate_captioned, TextAlign, TextBackgroundMode


def add_caption_to_image(img_path: str, caption: str,
                         target_image_path: Optional[str] = None,
                         character_ratio: float = 0.03,
                         left_margin: float = 0.05,
                         right_margin: float = 0.03,
                         text_background_mode: TextBackgroundMode = TextBackgroundMode.STRIPE,
                         text_min_height: Optional[float] = None,
                         filters: [BuiltinFilter] = []) -> str:
    image_with_caption = generate_captioned(caption,
                                            image_path=img_path,
                                            size=Image.open(img_path).size,
                                            text_align=TextAlign.CENTER,
                                            font_path="Times New Roman.ttf",
                                            filter_color=(0, 0, 0, 0),
                                            character_ratio=character_ratio, left_margin=left_margin,
                                            right_margin=right_margin,
                                            text_background_mode=text_background_mode,
                                            text_min_height=text_min_height,
                                            filters=filters,
                                            color=(255, 255, 0, 255))

    if target_image_path:
        parent_dir = os.path.dirname(target_image_path)
        pathlib.Path(parent_dir).mkdir(parents=True, exist_ok=True)
        final_image_path = target_image_path
    else:
        final_image_path = img_path+"_captioned.png"

    image_with_caption.save(final_image_path)
    return final_image_path
