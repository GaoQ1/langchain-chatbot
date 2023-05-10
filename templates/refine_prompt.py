'''
Description: 
Author: colin gao
Date: 2023-05-09 15:24:53
LastEditTime: 2023-05-10 16:32:51
'''
REFINE_PROMPT_EN = (
    "Your job is to produce a final summary\n"
    "We have provided an existing summary up to a certain point: {existing_answer}\n"
    "We have the opportunity to refine the existing summary\n"
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "Given the new context, refine the original summary\n"
    "If the context isn't useful, return the original summary."
)


REFINE_PROMPT = (
    "您的工作是生成一个最终答案\n"
    "我们已经提供了一个截止到某个点现有的答案，：{existing_answer}\n"
    "我们有机会用下面的更多上下文来完善现有答案（仅在需要时）。\n"
    "------------\n"
    "{question}\n"
    "------------\n"
    "根据新的上下文，完善原始答案\n"
    "如果上下文无用，请返回原始答案。"
)
