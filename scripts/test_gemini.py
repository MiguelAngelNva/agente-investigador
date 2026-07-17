import os
from  google import genai
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
IAmodel = os.getenv("IA_MODEL")

response = client.models.generate_content(
    model=IAmodel,
    contents="Explica qué es el aprendizaje profundo en una frase"
)

print(response.text)