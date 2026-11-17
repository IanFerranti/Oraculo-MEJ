🤖 Oráculo MEJ

Chatbot inteligente baseado em IA (RAG) especializado no Planejamento Estratégico da Brasil Júnior (MEJ). Desenvolvido com Streamlit, LangChain, ChromaDB e a API gratuita do Google Gemini.

⚙️ Como o Projeto Funciona

O sistema utiliza uma arquitetura de duas etapas para economizar cota da API e garantir alta performance:

Ingestão (cria_bd.py): Lê os PDFs oficiais salvos na pasta docs, quebra o conteúdo em pequenos pedaços (chunks), gera os vetores utilizando o Gemini e salva tudo localmente na pasta chroma_db.

Interface (app.py): Um chat web moderno, limpo e arredondado em Streamlit que carrega o banco vetorial pronto instantaneamente e responde às dúvidas dos usuários com base exclusiva nos documentos, permitindo também o envio temporário de PDFs avulsos.

🚀 Como Rodar o Projeto

Siga os passos abaixo no seu terminal (utilizando o Windows PowerShell):

1. Clonar ou abrir a pasta do projeto

Navegue até a pasta raiz do projeto (Versao Final).

2. Criar e ativar o ambiente virtual

py -3.12 -m venv .venv
.\.venv\Scripts\activate


3. Instalar as dependências

pip install -r requirements.txt


4. Configurar sua chave da API do Google

Obtenha sua chave gratuita no Google AI Studio.

Crie um arquivo chamado .env na raiz do projeto e cole o seguinte conteúdo:

GOOGLE_API_KEY="sua_chave_aqui"


5. Gerar o Banco de Dados Vetorial

Crie uma pasta chamada docs na raiz do projeto e coloque seus arquivos PDF do planejamento estratégico dentro dela.

Execute o script de indexação:

python cria_bd.py


6. Iniciar o Chatbot

Com o banco gerado, rode a aplicação web:

streamlit run app.py


O navegador abrirá automaticamente em http://localhost:8501.
