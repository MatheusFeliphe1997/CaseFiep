import os
import chromadb
from chromadb.utils import embedding_functions

# 1. Configuração da chave da API da OpenAI
key_openai = os.getenv('KEY_OPENAI')
if key_openai is None:
    raise ValueError("OpenAI API key não encontrada nas variáveis de ambiente.")

# 2. Inicializar o cliente do ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path='fiep_db')  # Banco de dados persistente
    collection_name = "fiep_collection"  # Nome da coleção
    collection = chroma_client.get_or_create_collection(name=collection_name)
except Exception as e:
    print(f"Erro ao inicializar o cliente ChromaDB: {e}")
    raise

# 3. Inicializar a função de embeddings da OpenAI
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-ada-002",
    api_key=key_openai
)

# 4. Função para dividir o texto em partes menores
def split_text(text):
    pieces = text.split("**")
    return [piece.strip() for piece in pieces if piece.strip()]

# 5. Carregar os dados do Fiep
def load_fiep_data(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            text = file.read()
        return split_text(text)  # Dividir o texto em partes menores
    except FileNotFoundError:
        print("Arquivo de texto não encontrado.")
        return []

# 6. Adicionar documentos ao banco de dados
def add_documents_to_db(pieces):
    for i, piece in enumerate(pieces):
        try:
            embedding = openai_ef([piece])
            if embedding is not None:
                collection.add(documents=[piece], ids=[str(i)], embeddings=[embedding[0]])
                print(f"Documento {i + 1} adicionado com sucesso.")
            else:
                print(f"Falha ao obter embedding para o documento {i + 1}.")
        except Exception as e:
            print(f"Erro ao adicionar documento {i + 1}: {e}")

# Fluxo principal
if __name__ == "__main__":
    file_path = 'faq_fiep.txt'  # Caminho para o arquivo com os dados do Fiep
    pieces = load_fiep_data(file_path)
    if pieces:
        print(f"Total de documentos carregados: {len(pieces)}")
        add_documents_to_db(pieces)
    else:
        print("Nenhum dado foi carregado.")