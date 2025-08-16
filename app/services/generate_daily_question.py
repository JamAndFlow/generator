from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_chroma import Chroma
from langchain_core.documents import Document

from chromadb import PersistentClient

from app.settings import settings
from app.prompts.daily_question_prompt import system_template, human_template
HUGGINGFACEHUB_API_TOKEN = settings.HUGGINGFACEHUB_API_TOKEN

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

client = PersistentClient(path="/app/chroma_data")


chroma_db = Chroma(
    client=client,
    # client_settings=client_settings,
    collection_name="daily_questions",
    embedding_function=embeddings,
)

retriever = chroma_db.as_retriever(search_kwargs={"k": 3})

llm = HuggingFaceEndpoint(
  repo_id="openai/gpt-oss-120b",
  huggingfacehub_api_token = settings.HUGGINGFACEHUB_API_TOKEN,
)

chat_model = ChatHuggingFace(llm=llm)

prompt = ChatPromptTemplate.from_messages([
  SystemMessagePromptTemplate.from_template(system_template),
  HumanMessagePromptTemplate.from_template(human_template),
])

def retrieve_context(inputs: dict):
    docs = retriever.get_relevant_documents(inputs["user_question"])
    context = " ".join([doc.page_content for doc in docs]) if docs else "No extra context"
    return {"context": context, "user_question": inputs["user_question"]}

context_retriever = RunnableParallel(
    user_question=lambda x: x["user_question"],
    context=retrieve_context
)

chain = context_retriever | prompt | chat_model

def generate_daily_question():
    """
    Generate a daily question based on the user's input.
    """
    response = chain.invoke({
        "user_question": "Generate a daily question for full stack developer working on microservices."
    })
    
    #TODO: store the answer in DB
    # For now we will just return it
    return response


def add_question_in_chroma_db(question: str):
    """
    Add a question to the ChromaDB collection.
    """
    doc = Document(page_content=question, metadata={})
    chroma_db.add_documents([doc])
    return {"status": "success", "message": "Question added to ChromaDB."}