from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector = embeddings.embed_query("You are going to learn Gen AI")

print(vector)
print(len(vector))