import pathlib
import re
import string
from random import choice
from typing import List
import time
from moviepy.editor import *
from pynter.pynter import TextBackgroundMode

import caption_utils
import image_utils
import text_to_speech_gen
from chatgpt_response import chatgpt_response_str
from openai import OpenAI
import nltk

openai_client = OpenAI()

non_text_prompts = "Focus on specific, visually representable elements." \
                   "Keep the image simple." \
                   "Do not include any form of text, equations or captions."

image_gen_style = "3d render. Hyper-realistic 4k."

current_time = str(int(time.time()))
audio_directory = f"./generated_audio/{current_time}"
pathlib.Path(audio_directory).mkdir(parents=True, exist_ok=True)

video_directory = f"./generated_video/{current_time}"
pathlib.Path(video_directory).mkdir(parents=True, exist_ok=True)


def pick_question(i: int = -1) -> str:
    questions = open("questions.txt", "r").readlines()
    if i != -1:
        return questions[i]
    else:
        return questions[0]


def generate_random_string(length=5):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(choice(characters) for _ in range(length))
    return random_string


def pick_random_file(folder_path, filter_extensions: List[str] = None):
    if filter_extensions is None:
        filter_extensions = []
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        print("No files found in the specified folder.")
        raise Exception(f"Folder {folder_path} empty. Cannot pick file from it.")

    if filter_extensions:
        filtered_files = [filename for filename in files if any(filename.endswith(ext) for ext in filter_extensions)]
    else:
        filtered_files = files

    random_file = choice(filtered_files)
    return os.path.join(folder_path, random_file)


def create_image_clip(image_path: str, audio_path: str, delay: int):
    # Load the audio file and get its duration
    print(f"Loading audio from {audio_path}")
    print(f"Loading video from {image_path}")
    audio_clip = AudioFileClip(audio_path)
    clip_duration = audio_clip.duration

    # Load the image file and create a video clip with the audio
    image_clip = ImageClip(image_path, duration=clip_duration + delay)
    return image_clip.set_audio(audio_clip)


def generate_freeman_image(source_image, width, height) -> str:
    freeman_image = pick_random_file("resources/freeman", [".jpeg", ".jpg", ".png"])

    if "right" in freeman_image:
        return image_utils.overlay_right(freeman_image, source_image, 0.8,
                                         source_image + f".freeman.png",
                                         result_width=width, result_height=height)
    else:
        return image_utils.overlay_left(freeman_image, source_image, 0.8,
                                        source_image + f".freeman.png",
                                        result_width=width, result_height=height)


def create_thumbnail_image(question: str, target_img_path: str) -> (str, str):
    print("Creating thumbnail...")
    thumbnail_prompt = chatgpt_response_str(openai_client,
                                            "Generate a prompt for dall-e 3 so that it generates a thumbnail "
                                            f"for a video explaining the answer to the question {question}.") \
                       + f"{non_text_prompts}" \
                       + f"{image_gen_style}"

    thumbnail_location = image_utils.generate_image_with_fallback(openai_client, thumbnail_prompt)
    if not thumbnail_location:
        raise Exception("Thumbnail image could not be created.")
    thumbnail_resized_landscape = image_utils.overlay_image(thumbnail_location,
                                                            target_img_path=thumbnail_location + ".resizedlandscape.png")
    thumbnail_resized_portrait = image_utils.overlay_image(thumbnail_location,
                                                           target_img_path=thumbnail_location + ".resizedportrait.png",
                                                           result_width=1080, result_height=1920)
    freeman_image = pick_random_file("resources/freeman", [".jpeg", ".jpg", ".png"])

    if "right" in freeman_image:
        return (image_utils.overlay_right(freeman_image, thumbnail_resized_landscape, 0.8,
                                          target_img_path + ".landscape.png"),
                image_utils.overlay_right(freeman_image, thumbnail_resized_portrait, 0.8,
                                          target_img_path + ".portrait.png",
                                          result_width=1080, result_height=1920))
    else:
        return (image_utils.overlay_left(freeman_image, thumbnail_resized_landscape, 0.8,
                                         target_img_path + ".landscape.png"),
                image_utils.overlay_left(freeman_image, thumbnail_resized_portrait, 0.8,
                                         target_img_path + ".portrait.png",
                                         result_width=1080, result_height=1920))


def create_first_video_slides(image_paths: (str, str), question: str) -> (ImageClip, ImageClip):
    print("Creating intro slide...")
    audio_path = text_to_speech_gen.text_to_speech_elevenlabs(question,
                                                              output_dir=audio_directory,
                                                              output_file="thumbnail_audio.wav")
    (landscape, portrait) = image_paths
    return (create_image_clip(landscape, audio_path, 1),
            create_image_clip(portrait, audio_path, 1))


def create_video_slides(prompt: str, sentence: str, target_image_dir: str) -> (ImageClip, ImageClip):
    print(f"Creating slide for {prompt}...")
    slide_square_image = image_utils.generate_image_with_fallback(openai_client, prompt)
    landscape_image = image_utils.overlay_image(slide_square_image,
                                                target_img_path=slide_square_image + "resizedlandscape.png")
    portrait_image = generate_freeman_image(image_utils.overlay_image(slide_square_image,
                                                                      target_img_path=slide_square_image + "resizedportrait.png",
                                                                      result_width=1080, result_height=1920),
                                            width=1080, height=1920)

    image_random_name = generate_random_string()
    captioned_landscape_image = caption_utils.add_caption_to_image(landscape_image, sentence,
                                                                   os.path.join(target_image_dir,
                                                                                f"{image_random_name}_landscape.png"))
    captioned_portrait_image = caption_utils.add_caption_to_image(portrait_image,
                                                                  sentence,
                                                                  os.path.join(target_image_dir,
                                                                               f"{image_random_name}_portrait.png"),
                                                                  character_ratio=0.06,
                                                                  left_margin=0.03,
                                                                  right_margin=0.03,
                                                                  text_background_mode=TextBackgroundMode.NONE,
                                                                  text_min_height=0.81)

    audio_path = text_to_speech_gen.text_to_speech_elevenlabs(sentence,
                                                              output_dir=audio_directory,
                                                              output_file=generate_random_string() + ".wav")
    return (create_image_clip(captioned_landscape_image, audio_path, 1),
            create_image_clip(captioned_portrait_image, audio_path, 1))


# def generate_stitched_video(video_slides: List[str]) -> str:

def last_slide_for_shorts(portrait_image: str, audio_path="endingAudio.mp3") -> ImageClip:
    return create_image_clip(portrait_image, audio_path, 0)

def generate_video_for_question(question: str, target_video_dir: str):
    (thumbnail_landscape, thumbnail_portrait) = create_thumbnail_image(question,
                                                                       os.path.join(target_video_dir, "thumbnail.png"))
    print(thumbnail_landscape, thumbnail_portrait)
    (landscape_thumbnail_clip, portrait_thumbnail_clip) = create_first_video_slides(
        (thumbnail_landscape, thumbnail_portrait), question)
    answer = chatgpt_response_str(openai_client, prompt=f"{question}",
                                  system_context=f"Explain the answer to the question "
                                                 f"in not more than 5 sentences."
                                                 f"Your target audience is a kid "
                                                 f"aged between 10 and 15.")

    sentences_in_answer = nltk.sent_tokenize(answer.strip())
    landscape_clips = [landscape_thumbnail_clip]
    portrait_clips = [portrait_thumbnail_clip]
    for i, sentence in enumerate(sentences_in_answer):
        image_prompt = chatgpt_response_str(openai_client,
                                            "Generate a prompt for dall-e 3 so that it generates an image explaining "
                                            f"the sentence: '{sentence}',"
                                            f"in context of the question '{question}'") \
                       + f"{non_text_prompts}" \
                       + f"{image_gen_style}"

        landscape_slide, portrait_slide = create_video_slides(image_prompt, sentence, target_video_dir)
        landscape_clips.append(landscape_slide)
        portrait_clips.append(portrait_slide)

    portrait_clips.append(last_slide_for_shorts(thumbnail_portrait))

    video_slug = re.sub(r'[^a-zA-Z0-9]', '', question)
    final_landscape_clip = concatenate_videoclips(landscape_clips, method="compose")
    final_landscape_clip.write_videofile(os.path.join(target_video_dir, video_slug + "_landscape.mp4"), fps=24)

    final_portrait_clip = concatenate_videoclips(portrait_clips, method="compose")
    final_portrait_clip.write_videofile(os.path.join(target_video_dir, video_slug + "_portrait.mp4"), fps=24)


if __name__ == "__main__":
    questions = open("questions.txt", "r").readlines()
    for question in questions[21:22]:
        generate_video_for_question(question, video_directory)
