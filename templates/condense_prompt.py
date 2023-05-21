'''
Description: 
Author: colin gao
Date: 2023-05-09 17:39:11
LastEditTime: 2023-05-21 14:12:31
'''
CONDENSE_PROMPT = """
根据以下对话和一个后续问题，将后续问题改写成一个独立的问题。

聊天记录：
{chat_history}

后续输入：{question}
独立问题：
"""