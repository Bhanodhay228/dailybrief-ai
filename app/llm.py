import os

from dotenv import load_dotenv
from mistralai.client import Mistral


load_dotenv()


class MistralClient:

    def __init__(self):

        self.api_key = os.getenv(
            "MISTRAL_API_KEY"
        )

        if not self.api_key:

            try:
                import streamlit as st

                self.api_key = st.secrets[
                    "MISTRAL_API_KEY"
                ]

            except Exception:
                self.api_key = None


        if not self.api_key:

            raise RuntimeError(
                "MISTRAL_API_KEY is not configured."
            )


        self.client = Mistral(
            api_key=self.api_key
        )


    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.complete(
            model="ministral-8b-2512",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[
            0
        ].message.content