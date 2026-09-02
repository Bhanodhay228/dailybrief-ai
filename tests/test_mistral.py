import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {
            "role": "user",
            "content": "In one sentence, explain what current affairs means."
        }
    ]
)

print("Mistral response:")
print(response.choices[0].message.content)