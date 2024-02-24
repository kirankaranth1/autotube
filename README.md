# autotube

Automatically generate science videos for kids, questions answered in Morgan Freeman's voice.
YT channel: https://www.youtube.com/@MorganFreemanScience

Generate Educational Videos with AI!
------------------------------------

This script (generate_video.py) uses the power of AI to automatically generate educational videos explaining answers to questions.

### [](https://github.com/kirankaranth1/autotube/blob/main/README.md#how-it-works)

### How it works:

1.  Ask a question: You provide a question you want explained.
2.  Thumbnail creation:
    -   An eye-catching thumbnail image is generated using Dall-e 3 based on the question.
    -   Separate landscape and portrait versions are created for different screen orientations.
3.  Intro slides:
    -   The question is narrated using ElevenLabs text-to-speech.
    -   Engaging video clips with the question and thumbnail are created for both landscape and portrait formats.
4.  Answer slides:
    -   A kid-friendly explanation is obtained from ChatGPT, broken down into short sentences.
    -   For each sentence:
        -   Dall-e 3 generates an image explaining the sentence in context of the question.
        -   Video clips with the generated image and narrated sentence are created in both landscape and portrait formats.
5.  Ending slide:
    -   A final slide with the thumbnail and ending audio is added.
6.  Video stitching:
    -   All video clips are combined to create the final video in both landscape and portrait versions.

### [](https://github.com/kirankaranth1/autotube/blob/main/README.md#getting-started)

### Getting started:

1.  Ensure you have the required libraries installed (`moviepy`, `pynter`, etc.) as per `requirements.txt`.
2.  Place your questions in a text file named `questions.txt`.
3.  Run the script: `python generate_video.py`.

This will generate video explanations for each question in the file. You'll find them in the `generated_video` folder.

Note: This explanation omits details of helper functions for brevity. Refer to the script for complete understanding.
