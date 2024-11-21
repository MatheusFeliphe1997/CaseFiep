import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import streamlit as st

# 1. Configuração da chave da API da OpenAI
key_openai = os.getenv('KEY_OPENAI')
if key_openai is None:
    raise ValueError("OpenAI API key não encontrada nas variáveis de ambiente.")

# 2. Inicializar o cliente da OpenAI
client = OpenAI(api_key=key_openai)

# 3. Inicializar o cliente do ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path='fiep_db')  # Banco de dados persistente
    collection_name = "fiep_collection"  # Nome da coleção
    collection = chroma_client.get_collection(name=collection_name)
except Exception as e:
    st.error(f"Erro ao inicializar o cliente ChromaDB: {e}")
    raise

# 4. Inicializar a função de embeddings da OpenAI
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-ada-002",
    api_key=key_openai
)

# 5. Buscar documentos no banco de dados
def search_documents(query, top_k=10):
    try:
        embedding_query = openai_ef([query])
        if embedding_query is None or not embedding_query:
            st.warning("Falha ao obter embedding para a consulta.")
            return []

        results = collection.query(
            query_embeddings=embedding_query[0],
            n_results=top_k
        )
        return results
    except Exception as e:
        st.error(f"Erro ao buscar documentos: {e}")
        return []

# 6. Gerar respostas usando o GPT
def generate_openai_response(client, content, question):
    try:
        conclusion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                        Seu objetivo é responder perguntas com base nos documentos do Fiep. Nunca respoda se nao encontrar a respota no banco de dados, resposta A pergunta feita está fora do escopo do Chat. Sempre mantenha precisão e clareza nas respostas.
                    """
                },
                {"role": "system", "content": content},  # Conteúdo do documento
                {"role": "user", "content": question},  # Pergunta do usuário
            ],
            temperature=0.1,
        )
        
        return conclusion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Erro ao gerar resposta: {e}")
        return "A pergunta feita está fora do escopo do Chat."

# 7. Salvar o bate-papo em um arquivo de texto
def save_chat_to_txt(user_name, messages):
    filename = f"{user_name}_chat_history.txt"
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            for message in messages:
                file.write(f"{message}\n")
        st.success(f"Bate-papo salvo em {filename}")
    except Exception as e:
        st.error(f"Erro ao salvar o bate-papo: {e}")

# 8. Encerrar conversa
def end_chat(user_name):
    save_chat_to_txt(user_name, st.session_state.chat_history)
    st.session_state.chat_history = []  # Limpa o histórico
    st.success("Conversa encerrada e salva.")

# 9. Fluxo principal com Streamlit
if __name__ == "__main__":
    st.title("Chatbot FIEP")

    # Inicializar o histórico de bate-papo se não existir
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Inicializa o nome do usuário se não existir
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    # Exibe todo o histórico de chat acima do campo de entrada
    for message in st.session_state.chat_history:
        st.markdown(message)

    # Campo de entrada único para nome e perguntas, sempre na parte inferior
    user_input = st.text_input("Digite seu nome ou pergunta:", key="user_input", value="", max_chars=500)

    # Verifica se a entrada é um nome ou uma pergunta
    if user_input:
        if st.session_state.user_name == "":  # Se ainda não tiver um nome definido
            st.session_state.user_name = user_input  # Define o nome do usuário
            
            # Mensagem de boas-vindas após a entrada do nome
            st.markdown(f"Olá, {st.session_state.user_name}! Como posso te ajudar?")
            
            user_input = ""  

        else:  # Se já tiver um nome definido, trata como uma pergunta
            if user_input.lower() == "encerrar":
                end_chat(st.session_state.user_name)
            else:
                # Adiciona a pergunta ao histórico (sem repetir)
                st.session_state.chat_history.append(f"{st.session_state.user_name}: {user_input}")

                # Buscar documentos relevantes
                results = search_documents(user_input)

                if 'documents' in results and results['documents']:
                    first_doc = results['documents'][0]
                    content = " ".join(first_doc)

                    # Gerar resposta com base nos documentos
                    response = generate_openai_response(client, content, user_input)

                    # Adiciona a resposta ao histórico (sem repetir)
                    st.session_state.chat_history.append(f"Chatbot: {response}")
                else:
                    response = "Nenhum documento relevante encontrado."
                    st.session_state.chat_history.append(f"Chatbot: {response}")

                # Atualiza a tela com a nova mensagem (opcional)
                response_placeholder = st.empty()  
                response_placeholder.markdown(f"**Chatbot:** {response}")

                # Limpa o campo de entrada após enviar a pergunta (usando session state)
                user_input = ""  
