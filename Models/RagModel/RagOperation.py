import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from langchain_openai import ChatOpenAI
import torch
import asyncio

from ScrapingOperations import Scraping

load_dotenv()

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)
llm = ChatOpenAI(model="gpt-4")

data = Scraping.output

def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data.iloc[i:i + chunk_size]

chunk_size = 2
chunks = list(chunk_data(data, chunk_size))

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data['Question'])

def retrieve_relevant_docs(query, tfidf_matrix, data):
    query_vec = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    relevant_doc_index = cosine_similarities.argmax()
    return data.iloc[relevant_doc_index]['Answer']

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

async def generate_answer(query, context):
    input_text = f"Question: {query}\nContext: {context}\nAnswer:"
    inputs = tokenizer.encode(input_text, return_tensors='pt')
    attention_mask = torch.ones(inputs.shape, dtype=torch.long)
    outputs = model.generate(
        inputs,
        max_length=100,
        num_return_sequences=1,
        attention_mask=attention_mask,
        pad_token_id=tokenizer.eos_token_id
    )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.replace(input_text, '').strip()

async def rag_model(query):
    context = retrieve_relevant_docs(query, tfidf_matrix, data)
    answer = await generate_answer(query, context)
    return answer

while True:
    query = input("Please enter your question (type 'exit' to quit): ")
    if query.lower() == 'exit':
        break
    answer = asyncio.run(rag_model(query))
    print(f"Answer: {answer}")