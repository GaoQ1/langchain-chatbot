'''
Description: 
Author: colin gao
Date: 2023-05-14 17:16:12
LastEditTime: 2023-05-15 21:42:55
'''
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv
load_dotenv()

prompt = PromptTemplate(
    input_variables=["query"],
    template="{query}"
)

llm = OpenAI(temperature=0.7)

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


if __name__ == "__main__":
    agent_chain.run(input="帮我预测下我今年的运势。请用中文回答。")

