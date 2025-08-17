from typing import List, Optional, Dict, Any
from chromadb import PersistentClient
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from app.settings import settings

class ChromaDB:
    """A wrapper for ChromaDB to handle document storage and retrieval."""
    def __init__(self, collection: str = "daily_questions"):
        self.path = settings.CHROMA_PATH
        self.collection = collection 
        self.model = settings.EMBEDDING_MODEL

        self._embeddings = HuggingFaceEmbeddings(model_name=self.model)
        self._client = PersistentClient(path=self.path)
        self._db = Chroma(
            client=self._client,
            collection_name=self.collection,
            embedding_function=self._embeddings,
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the ChromaDB collection.
        """
        self._db.add_documents(documents)
    
    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Get a retriever for the ChromaDB collection.
        search_kwargs: can be used to specify additional search parameters like 'k' for KNN.
        """
        return self._db.as_retriever(search_kwargs=search_kwargs)
            
