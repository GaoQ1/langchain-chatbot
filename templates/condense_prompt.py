'''
Description: 
Author: colin gao
Date: 2023-05-09 17:39:11
LastEditTime: 2023-05-16 16:34:01
'''
CONDENSE_PROMPT_EN = """
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}

Follow Up Input: {question}
Standalone question:
"""

CONDENSE_PROMPT = """
根据以下对话和一个后续问题，将后续问题改写成一个独立的问题。

聊天记录：
{chat_history}

后续输入：{question}
独立问题：
"""