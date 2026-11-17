# 🤖 Oráculo MEJ

**Chatbot inteligente baseado em Inteligência Artificial (RAG), especializado no Planejamento Estratégico da Brasil Júnior e no Movimento Empresa Júnior (MEJ).**

O **Oráculo MEJ** é uma aplicação desenvolvida para facilitar o acesso e a consulta às informações presentes nos documentos oficiais da Brasil Júnior. Utilizando a arquitetura **Retrieval-Augmented Generation (RAG)**, o sistema combina busca semântica em documentos com modelos de linguagem generativa, permitindo respostas contextualizadas e fundamentadas no conteúdo disponibilizado.

[Clique aqui para testar o funcionamento do projeto](https://oraculo-mej.streamlit.app)


## 🚀 Tecnologias Utilizadas

- **Python:** Linguagem principal do projeto.
- **Streamlit:** Desenvolvimento da interface web interativa.
- **LangChain:** Orquestração do fluxo de recuperação de informações e geração de respostas.
- **ChromaDB:** Banco de dados vetorial para armazenamento e recuperação de documentos.
- **Google Gemini API:** Geração de embeddings e respostas utilizando modelos de IA generativa.
- **PyPDF:** Extração de conteúdo de arquivos PDF.

## ⚙️ Como o Projeto Funciona

O sistema utiliza uma arquitetura dividida em duas etapas principais, separando o processamento e a indexação dos documentos da interação com o chatbot. Essa abordagem evita o processamento repetitivo dos arquivos e otimiza o consumo da API.

### 1. Ingestão e Indexação dos Documentos (`cria_bd.py`)

Responsável pela preparação da base de conhecimento:

1. Realiza a leitura dos documentos PDF armazenados na pasta `docs`.
2. Extrai o conteúdo textual dos arquivos.
3. Divide os textos em pequenos fragmentos (*chunks*), facilitando a recuperação de informações relevantes.
4. Gera embeddings utilizando os modelos do Google Gemini.
5. Armazena os vetores e seus respectivos conteúdos no banco de dados local ChromaDB, na pasta `chroma_db`.

Esse processo é executado previamente, permitindo que a aplicação utilize uma base vetorial já indexada.

### 2. Interface e Recuperação de Informações (`app.py`)

Responsável pela interação com o usuário e pela geração das respostas:

1. Inicializa a interface de conversação desenvolvida com Streamlit.
2. Carrega o banco de dados vetorial previamente criado.
3. Recebe as perguntas dos usuários e realiza a busca semântica por trechos relevantes nos documentos.
4. Encaminha o contexto recuperado ao Google Gemini por meio do LangChain.
5. Gera respostas contextualizadas, utilizando exclusivamente as informações disponíveis na base documental.

A aplicação também permite o envio temporário de arquivos PDF adicionais, possibilitando consultas sobre documentos específicos sem alterar permanentemente a base de conhecimento principal.

## 📂 Estrutura do Projeto

```text
Oraculo-MEJ/
│
├── docs/                  # Documentos PDF da base de conhecimento
│
├── chroma_db/             # Banco de dados vetorial gerado
│
├── .venv/                 # Ambiente virtual Python
│
├── cria_bd.py             # Script de ingestão e indexação
├── app.py                 # Aplicação web e chatbot
├── requirements.txt       # Dependências do projeto
├── .env                   # Variáveis de ambiente e chave da API
└── README.md              # Documentação do projeto
```

## 🛠️ Como Executar o Projeto

### Pré-requisitos

Antes de iniciar, certifique-se de possuir:

- Python 3.12 instalado.
- Pip para gerenciamento de dependências.
- Uma chave de API do Google Gemini, obtida gratuitamente pelo [Google AI Studio](https://aistudio.google.com/).

### 1. Clonar o repositório ou acessar a pasta do projeto

Navegue até o diretório raiz do projeto pelo terminal.

```powershell
cd "caminho\para\Oraculo-MEJ"
```

### 2. Criar e ativar o ambiente virtual

Crie um ambiente virtual para isolar as dependências do projeto e, em seguida, ative-o.

```powershell
py -3.12 -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

```powershell
pip install -r requirements.txt
```

### 4. Configurar a chave da API do Google Gemini

Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave de API:

```env
GOOGLE_API_KEY="sua_chave_aqui"
```

**Importante:** Não compartilhe sua chave de API nem a envie para repositórios públicos. Certifique-se de adicionar o arquivo `.env` ao `.gitignore`.

### 5. Preparar os documentos e gerar o banco vetorial

Crie uma pasta chamada `docs` na raiz do projeto e adicione os arquivos PDF oficiais do Planejamento Estratégico da Brasil Júnior que serão utilizados como base de conhecimento.

Em seguida, execute o script responsável pela ingestão e indexação:

```powershell
python cria_bd.py
```

Após a execução, o banco de dados vetorial será criado localmente na pasta `chroma_db`.

**Observação:** Sempre que novos documentos forem adicionados ou a base de conhecimento for atualizada, execute novamente o script de indexação.

### 6. Iniciar o chatbot

Com as dependências instaladas, a chave configurada e o banco vetorial gerado, inicie a aplicação:

```powershell
streamlit run app.py
```

O Streamlit iniciará o servidor local e disponibilizará a aplicação no navegador:

```text
http://localhost:8501
```

## 🎯 Objetivo do Projeto

O Oráculo MEJ foi desenvolvido com o propósito de tornar o conhecimento estratégico do Movimento Empresa Júnior mais acessível, centralizando informações e facilitando a consulta aos materiais oficiais da Brasil Júnior.

Por meio da Inteligência Artificial e da arquitetura RAG, o projeto transforma documentos extensos em uma base de conhecimento interativa, permitindo que os integrantes do MEJ encontrem informações relevantes de maneira mais rápida e intuitiva.
