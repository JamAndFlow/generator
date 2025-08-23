from typing import Dict
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableParallel
from app.prompts.daily_question_prompt import system_template, human_template
from app.config.vectorestore import chroma_db
from app.llm.provider import build_chat_model
from app.settings import settings

retriever = chroma_db.as_retriever(collection="daily_questions",search_kwargs={"k": settings.RETRIEVE_K})

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template(human_template),
])

def _retrieve_context(inputs: Dict):
    """It will only trigger when user gives a contet if not it will return 'No extra context'"""
    if inputs["user_question"] is None:
        docs = []
    else:
        docs = retriever.get_relevant_documents(inputs["user_question"])
    context = " ".join([d.page_content for d in docs]) if docs else "No extra context"
    return {"context": context, "user_question": inputs["user_question"]}

context_retriever = RunnableParallel(
    user_question=lambda x: x["user_question"],
    context=_retrieve_context
)

chat_model = build_chat_model()

# Full chain
daily_question_chain = context_retriever | prompt | chat_model
