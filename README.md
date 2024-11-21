#                       README para o Projeto de Chatbot
    Este README fornece instruções detalhadas sobre como executar 
    o projeto de chatbot que utiliza a API da OpenAI. 
    Siga os passos abaixo para configurar e executar o projeto corretamente.
#                       Pré-requisitos
    Antes de começar, certifique-se de que você possui os seguintes requisitos 
    instalados em seu sistema:
    Python 3.x
    pip (gerenciador de pacotes do Python)
    Git
#                       Passo 1: Clonar o Repositório
    Primeiro, você precisa clonar o repositório do projeto. Abra seu terminal 
    e execute o seguinte comando:
    bash
    git clone <URL_DO_REPOSITORIO>

    Substitua <URL_DO_REPOSITORIO> pelo link do repositório que você irá compartilhar.
#                       Passo 2: Criar o Arquivo .env
    Após clonar o repositório, navegue até a pasta do projeto:
    bash
    cd <NOME_DA_PASTA_DO_PROJETO>

    Dentro dessa pasta, você precisa criar um arquivo chamado .env. Este arquivo irá 
    armazenar a chave da API da OpenAI. Para isso, execute:
    bash
    touch .env

    Em seguida, abra o arquivo .env em um editor de texto e adicione a seguinte linha:
    text
    KEY_OPENAI=<SUA_CHAVE_OPENAI>

    Substitua <SUA_CHAVE_OPENAI> pela sua chave da API da OpenAI.
#                       Passo 3: Instalar as Bibliotecas Necessárias
    Para que o projeto funcione corretamente, você precisa instalar as bibliotecas necessárias. 
    Execute os seguintes comandos no terminal:
    Instalar a biblioteca OpenAI:
    bash
    pip install openai

    Instalar a biblioteca ChromaDB:
    bash
    pip install chromadb

    Instalar a biblioteca Streamlit:
    bash
    pip install streamlit

#                       Passo 4: Executar chatbot.py
    Agora você deve executar o script chatbot.py. Este script irá criar um banco de dados no 
    ChromaDB utilizando os embeddings do arquivo .txt presente no projeto. Para executar o script, 
    use o seguinte comando no terminal:
    bash
    python chatbot.py

#                       Passo 5: Executar o Chatbot
    Após a criação do banco de dados, você pode iniciar a interface do chatbot. No terminal, 
    execute o seguinte comando:
    bash
    streamlit run bot.py

    Isso abrirá uma nova janela em seu navegador com a interface do chatbot, onde você poderá 
    interagir e testar suas funcionalidades.
#                       Conclusão
    Agora você está pronto para utilizar o chatbot! Certifique-se de que todas as dependências 
    estão instaladas e que a chave da API está correta no arquivo .env. Se encontrar algum problema, 
    verifique as mensagens de erro no terminal para solucionar.
    Se precisar de mais informações ou ajuda adicional, sinta-se à vontade para entrar em contato! 
#    WhatsApp (41)99880-7662 MATHEUS FELIPHE
