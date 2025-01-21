import os
import requests
from bs4 import BeautifulSoup
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

# URL'yi başta tanımla
url = "https://www.kikkararlari.com/"

OPENAI_API_KEY="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"

def fetch_and_scrape_tr(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tr_elements = soup.find_all("tr")
    data = []
    for tr in tr_elements:
        text = tr.text.strip()
        if text:
            data.append(text)
    return data

def create_vectorstore(data):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docs = [Document(page_content=str(item)) for item in data]
    vectorstore = Chroma.from_documents(docs, embedding=embeddings)
    return vectorstore

def create_qa_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

if __name__ == "__main__":
    print("Veri kazınıyor...")
    data = fetch_and_scrape_tr(url)
    print(f"{len(data)} adet satır bulundu.")

    print("Vektör deposu oluşturuluyor...")
    vectorstore = create_vectorstore(data)

    if vectorstore:
        print("QA zinciri oluşturuluyor...")
        qa_chain = create_qa_chain(vectorstore)

        while True:
            query = input("\nSorunuzu girin (çıkmak için 'exit'): ")
            if query.lower() == "exit":
                print("Çıkılıyor...")
                break
            result = qa_chain.run(query)
            print("\nCevap:")
            print(result)
    else:
        print("Vektör deposu oluşturulamadı.")