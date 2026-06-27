from langchain_huggingface import HuggingFaceEmbeddings

embedding= HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)
text=(
    "hello i am pranav"
    "i am an ai engineer"
    "i want to learn genai"
)
vector=embedding.embed_documents(text)
print(vector)