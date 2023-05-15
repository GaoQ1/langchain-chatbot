import streamlit as st
import tempfile
import os 
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone, Chroma
import pinecone

from templates import CONDENSE_PROMPT, QA_PROMPT
from configs.config import *

from dotenv import load_dotenv
load_dotenv()

import code

def main():
    # Set Streamlit app title and header
    st.title('Langchain Chat')
    st.header('DOC Mode')

    openai_api_key = st.text_input("OpenAI API Key", type="password")
    is_ingest = st.checkbox("Whether or not ingest doc?")
    is_use_pinecone = st.checkbox("Whether or not use pinecone database?")

    if is_use_pinecone:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pinecone_api_key = st.text_input("Pinecone API Key", type="password")

        with col2:
            pinecone_environment = st.text_input("Pinecone Environment")

        with col3:
            pinecone_index = st.text_input("Pinecone Index Name")

        with col4:
            pinecone_namespace = st.text_input("Pinecone Namespace")

    uploaded_files = st.file_uploader("Choose a txt file", accept_multiple_files=True, type="txt")

    if uploaded_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name
                file_content = uploaded_file.read()
                st.write("Filename: ", file_name)
                with open(os.path.join(tmpdir, file_name), "wb") as file:
                    file.write(file_content)
            loader = DirectoryLoader(tmpdir, glob="**/*.txt", loader_cls=TextLoader)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
            documents = text_splitter.split_documents(documents)

            embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)
            
            if is_ingest:
                if is_use_pinecone:
                    pinecone.init(
                        api_key=pinecone_api_key,  # find at app.pinecone.io
                        environment=pinecone_environment  # next to api key in console
                    )
                    Pinecone.from_documents(documents, embeddings, index_name=pinecone_index, namespace=pinecone_namespace)
                else:
                    Chroma.from_documents(
                        documents, 
                        embeddings, 
                        collection_name="my_collection", 
                        persist_directory=VS_ROOT_PATH
                    )

            
            st.success("Ingested File!")

    message = st.text_input('User Input:')
    temperature = st.slider('Temperature', 0.0, 2.0, 0.7)
    source_amount = st.slider('Sources', 1, 8, 4)

    if message:
        chat_history = []
        embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)

        if is_use_pinecone:
            pinecone.init(api_key=pinecone_api_key,environment=pinecone_environment)
            vectorstore = Pinecone.from_existing_index(index_name=pinecone_index, embedding=embeddings, text_key='text', namespace=pinecone_namespace)
        else:
            vectorstore = Chroma(
                persist_directory=VS_ROOT_PATH,
                embedding_function=embeddings,
                collection_name="my_collection"
            )

        model = ChatOpenAI(
            model_name='gpt-3.5-turbo', 
            temperature=temperature, 
            openai_api_key=openai_api_key, 
            streaming=STREAMING
        ) # max temperature is 2 least is 0
        
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": source_amount},
            qa_template=QA_PROMPT, 
            question_generator_template=CONDENSE_PROMPT
        ) # 9 is the max sources

        qa = ConversationalRetrievalChain.from_llm(
            llm=model, 
            retriever=retriever, 
            return_source_documents=True
        )
        
        result = qa({"question": message, "chat_history": chat_history})
        answer = result["answer"]
        
        # Display the response in the Streamlit app
        st.write('AI:')
        st.write(answer)

if __name__ == '__main__':
    try:
        main()
    except:
        st.write('Fatal Error!')