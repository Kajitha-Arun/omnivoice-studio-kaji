import requests
import uuid
import os
import torch
import torchaudio
import io
from dotenv import load_dotenv
exit()
load_dotenv()

class ShabdTTSBackend:

    id = "shabd"
    display_name = "Shabd API TTS"

    def __init__(self):
        self.api_key = os.getenv("SHABD_API_KEY")
        self.url = "https://api.shabd.tech/v1/text-to-speech"

    @property
    def sample_rate(self):
        return 22050

    @property
    def supported_languages(self):
        return ["en"]  

    @classmethod
    def is_available(cls):
        return True, "ready"

    def generate(self, text, **kw):

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "x-request-id": str(uuid.uuid4())
        }

        payload = {
            "text": text,
            "language": "english",
            "gender": "male",
            "format": "wav",
            "sampleRate": 22050,
            "speed": "normal"
        }

        response = requests.post(
            self.url,
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            with open("shabd_output.wav", "wb") as audio_file:
                audio_file.write(response.content)
            audio_bytes = io.BytesIO(response.content)
            waveform, sample_rate = torchaudio.load(audio_bytes)
            print("Audio generated successfully.")
            return waveform

        else:
            raise RuntimeError(
                f"Shabd API Error: {response.status_code} - {response.text}"
                )


if __name__ == "__main__":

    shabd = ShabdTTSBackend()

    shabd.generate("Hello from Shabd API integration")