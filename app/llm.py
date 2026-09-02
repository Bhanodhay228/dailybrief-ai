import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()


class MistralClient:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content