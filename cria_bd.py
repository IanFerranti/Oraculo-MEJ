import os
import time
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

# CORREÇÃO: Usando o ID exato aceito pela API v1beta atual
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
CHROMA_PERSIST_DIR = "chroma_db"
PDF_FOLDER = "docs"

def criar_banco_vetorial():
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
        print(f"📁 A pasta '{PDF_FOLDER}' foi criada. Coloque seus PDFs nela.")
        return False

    # Carrega todos os PDFs da pasta
    print("📂 Carregando PDFs da pasta...")
    loader = PyPDFDirectoryLoader(PDF_FOLDER)
    documents = loader.load()

    if not documents:
        print("⚠️ Nenhum arquivo PDF encontrado na pasta 'docs'.")
        return False

    print(f"📄 Total de páginas carregadas: {len(documents)}")

    # Divide os documentos em pedaços menores (chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    print(f"✂️ Documentos divididos em {len(docs)} pedaços (chunks).")

    # Se já existir um banco antigo, remove para recriar do zero atualizado
    if os.path.exists(CHROMA_PERSIST_DIR):
        print("🗑️ Removendo base vetorial anterior para recriar...")
        import shutil
        shutil.rmtree(CHROMA_PERSIST_DIR)

    # Configuração de lotes e pausas seguras para o plano gratuito
    vectorstore = None
    batch_size = 15
    pause_time = 10
    total_docs = len(docs)

    print("🚀 Iniciando indexação na API do Google (com pausas de segurança para o plano gratuito)...")
    for i in range(0, total_docs, batch_size):
        batch = docs[i:i + batch_size]
        print(f"⏳ Processando lote {i} até {min(i + batch_size, total_docs)} de {total_docs}...")
        
        if vectorstore is None:
            vectorstore = Chroma.from_documents(
                batch, 
                embeddings, 
                persist_directory=CHROMA_PERSIST_DIR
            )
        else:
            vectorstore.add_documents(batch)
        
        # Pausa segura entre os lotes
        if i + batch_size < total_docs:
            time.sleep(pause_time)

    print("✅ Banco de dados vetorial criado e salvo com sucesso na pasta 'chroma_db'!")
    return True

if __name__ == "__main__":
    criar_banco_vetorial()