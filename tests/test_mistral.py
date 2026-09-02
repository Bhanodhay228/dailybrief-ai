from app.llm import MistralClient


llm = MistralClient()

response = llm.generate(
    "In one sentence, explain what current affairs means."
)

print("Mistral client working!")
print(response)