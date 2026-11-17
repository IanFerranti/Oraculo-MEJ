import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile

_ = load_dotenv(find_dotenv())

# 1. Configuração da Página
st.set_page_config(
    page_title="Oráculo MEJ | Planejamento Estratégico",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Estilização
st.markdown("""
<style>
    /* Fundo geral mais suave */
    .stApp {
        background-color: #F7F9FC;
        color: #2D3748;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Cabeçalho central */
    .chat-header {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
    }
    .chat-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1A365D;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .chat-header p {
        font-size: 1rem;
        color: #718096;
    }

    /* Caixa do uploader de PDF super arredondada */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        font-weight: 500;
        color: #4A5568;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    
    /* Balões de chat bem arredondados */
    [data-testid="stChatMessage"] {
        border-radius: 24px !important;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 15px -3px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        border: 1px solid #EDF2F7;
        background-color: #FFFFFF;
    }

    /* Caixas de expansão de fontes arredondadas */
    .streamlit-expanderContent {
        background-color: #F8FAFC;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0;
        padding: 1rem;
    }

    /* Ocultar elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Configuração dos Modelos
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
CHROMA_PERSIST_DIR = "chroma_db"

@st.cache_resource
def load_vectorstore():
    if not os.path.exists(CHROMA_PERSIST_DIR) or not os.listdir(CHROMA_PERSIST_DIR):
        return None
    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings
    )

vectorstore = load_vectorstore()

# 4. Cabeçalho Central
st.markdown("""
<div class="chat-header">
    <h1>🤖 Oráculo MEJ</h1>
    <p>Seu assistente especialista no Planejamento Estratégico da Brasil Júnior</p>
</div>
""", unsafe_allow_html=True)

# 5. Uploader de PDF Temporário Arredondado
with st.expander("📎 Adicionar documento PDF para análise"):
    uploaded_file = st.file_uploader("Selecione um arquivo PDF", type=["pdf"], label_visibility="collapsed")
    
    temp_docs = []
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name
        
        loader = PyPDFLoader(temp_path)
        raw_temp_docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        temp_docs = text_splitter.split_documents(raw_temp_docs)
        
        os.unlink(temp_path)
        st.success(f"✨ Documento **{uploaded_file.name}** integrado com sucesso para esta sessão!")

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# 6. Verificação e Execução do Chat
if vectorstore is None and not temp_docs:
    st.info("👋 **Olá!** Para começar, coloque os arquivos PDF oficiais na pasta `docs` e rode o script de criação do banco (`python cria_bd.py`), ou envie um PDF avulso no menu acima.")
else:
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 4}) if vectorstore else None

    rag_template = """
    Você é um assistente virtual especialista no Planejamento Estratégico da Brasil Júnior e do Movimento Empresa Júnior (MEJ).
    Seu trabalho é conversar com os membros da rede, consultando os documentos fornecidos, e dar respostas precisas, claras e estruturadas (use tópicos e negrito quando ajudar).
    Seu tom deve ser amigável e focado no desenvolvimento do MEJ.
    Se a resposta não estiver clara ou presente nos documentos, informe educadamente que a informação não consta no material carregado.

    Contexto extraído dos documentos:
    {context}

    Pergunta do usuário: {question}
    """
    
    prompt = ChatPromptTemplate.from_template(rag_template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📖 Ver fontes consultadas"):
                    for src in message["sources"]:
                        st.caption(f"• {src}")

    if user_input := st.chat_input("Pergunte algo sobre o Planejamento Estratégico."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        retrieved_docs = []
        if base_retriever:
            retrieved_docs.extend(base_retriever.invoke(user_input))
        
        if temp_docs:
            retrieved_docs.extend(temp_docs[:5])

        sources_list = []
        for doc in retrieved_docs:
            source_name = os.path.basename(doc.metadata.get("source", "PDF Temporário" if temp_docs else "Documento"))
            page_num = doc.metadata.get("page", 0) + 1
            source_entry = f"**{source_name}** (Página {page_num})"
            if source_entry not in sources_list:
                sources_list.append(source_entry)

        context_text = format_docs(retrieved_docs)

        chain = (
            {"context": lambda x: context_text, "question": RunnablePassthrough()}
            | prompt
            | llm
        )

        with st.chat_message("assistant", avatar="🤖"):
            response_container = st.empty()
            full_response = ""
            
            try:
                for chunk in chain.stream(user_input):
                    content = chunk.content
                    if isinstance(content, list):
                        text_part = "".join(
                            item.get("text", "") if isinstance(item, dict) else str(item)
                            for item in content
                        )
                    elif isinstance(content, dict):
                        text_part = content.get("text", "")
                    else:
                        text_part = str(content)
                        
                    full_response += text_part
                    response_container.markdown(full_response + "▌")
                    
                response_container.markdown(full_response)

                if sources_list:
                    with st.expander("📖 Ver fontes consultadas"):
                        for src in sources_list:
                            st.caption(f"• {src}")

            except Exception as e:
                full_response = f"Ocorreu um erro ao processar sua solicitação: {e}"
                response_container.error(full_response)
                sources_list = []

        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "sources": sources_list
        })