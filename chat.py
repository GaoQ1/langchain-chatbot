'''
Description: 
Author: colin gao
Date: 2023-05-14 17:16:12
LastEditTime: 2023-05-15 22:25:57
'''
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ConversationalRetrievalChain

from dotenv import load_dotenv
load_dotenv()


def get_chain(stream_handler, tracing: bool = False) -> ConversationalRetrievalChain:
    """Create a ConversationalRetrievalChain for question/answering."""
    manager = AsyncCallbackManager([])
    stream_manager = AsyncCallbackManager([stream_handler])
    if tracing:
        tracer = LangChainTracer()
        tracer.load_default_session()
        manager.add_handler(tracer)
        stream_manager.add_handler(tracer)

    prompt = PromptTemplate(
        input_variables=["query"],
        template="{query}"
    )

    llm = OpenAI(
        streaming=True,
        callback_manager=stream_manager,
        verbose=True,
        temperature=0.7,
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    llm_tool = Tool(
        name="Language Model",
        func=llm_chain.run,
        # description="use this tool for generate purpose queries and logic"
        description="当问到和占卜运势相关的问题时候，请使用这个tool。"
    )

    tools = [llm_tool]

    memory = ConversationBufferMemory(memory_key="chat_history")

    agent_chain = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memory, 
        stream=True
    )

    return agent_chain


if __name__ == "__main__":
    ...
    # agent_chain.run(input="帮我预测下我今年的运势。请用中文回答。")
