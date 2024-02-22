import json

import requests
import pathlib
import random

url = "https://api.elevenlabs.io/v1/text-to-speech/"
voices_list_url = "https://api.elevenlabs.io/v1/voices"
elevenlabs_api_key = ""


def voices_list(elevenlabs_api_key):
    headers = {"Content-Type": "application/json",
               "xi-api-key": elevenlabs_api_key}

    response = requests.request("GET", voices_list_url, headers=headers)
    if response.ok:
        return json.loads(response.text)['voices']
    else:
        raise Exception("Could not get voices list")


voices = voices_list(elevenlabs_api_key)
voice_id = [voice["voice_id"] for voice in voices if voice["name"] == "Okole"][0]
print(f"Picking voice id: {voice_id} as default")


def text_to_speech_elevenlabs(text: str,
                              output_dir: str = "generated_audio",
                              output_file: str = "output.wav") -> str:
    print(f"Generating audio for {text}, outputfile: {output_file}")

    payload = {
        "text": text,
        "voice_settings": {
            "similarity_boost": 0.75,
            "stability": 0.3,
            "style": 0,
            "use_speaker_boost": True
        }
    }
    headers = {"Content-Type": "application/json",
               "xi-api-key": elevenlabs_api_key,
               "Accept": "audio/mpeg"}

    response = requests.request("POST", url + voice_id, json=payload, headers=headers)
    print(f"Response from elevenlabs: {response}")
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    target_file = f'{output_dir}/{output_file}'

    with open(target_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return target_file
