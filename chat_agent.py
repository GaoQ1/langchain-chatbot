'''
Description: 
Author: colin gao
Date: 2023-05-14 17:16:12
LastEditTime: 2023-05-18 18:27:53
'''
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores.base import VectorStore

from configs.config import *

from dotenv import load_dotenv
load_dotenv()

def get_chain(vectorstore: VectorStore):
    chat_llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=TEMPERTURE
    )

    conversation_memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=5,
        return_messages=True
    )

    retriever = RetrievalQA.from_chain_type(
        llm=chat_llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    tools = [
        Tool(
            name="AI占卜",
            func=retriever.run,
            description="""使用这个工具，通过AI占卜来回答用户提出的问题。如果用户说"占卜"，就使用这个工具来获取答案。此外，这个工具还可以用来回答用户提出的后续问题。"""
        )
    ]

    agent_chain = initialize_agent(
        tools=tools, 
        llm=chat_llm, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        max_iterations=2,
        early_stopping_method='generate',
        memory=conversation_memory, 
        stream=True
    )

    sys_msg = """Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist. 

    When answering, Assistant MUST speak in the following language: chinese.
    """

    new_prompt = agent_chain.agent.create_prompt(
        system_message = sys_msg,
        tools=tools
    )

    agent_chain.agent.llm_chain.prompt = new_prompt

    return agent_chain

if __name__ == "__main__":
    from colorama import init, Fore, Style
    import pickle

    init()

    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)

    agent_chain = get_chain(vectorstore)

    while True:
        question = input("Please enter your question (or type 'exit' to end): ")
        if question.lower() == 'exit':
            break
        
        result = agent_chain.run(input=question)

        print(f'{Fore.BLUE}{Style.BRIGHT}AI:{Fore.RESET}{Style.NORMAL} {result}')


