from typing import Any, Dict, List, Optional

from chromadb import PersistentClient
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from app.settings import settings


# Using singleton pattern for ChromaDB to ensure a single instance is used across the application
class ChromaDB:
    """Singleton class for managing ChromaDB collections and operations."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.path = settings.CHROMA_PATH
        self.model = settings.EMBEDDING_MODEL

        self._embeddings = HuggingFaceEmbeddings(model_name=self.model)
        self._client = PersistentClient(path=self.path)

        self._collections: Dict[str, Chroma] = {}

    def get_collection(self, name: str) -> Chroma:
        """Get or create a Chroma-backed collection."""
        if name not in self._collections:
            self._collections[name] = Chroma(
                client=self._client,
                collection_name=name,
                embedding_function=self._embeddings,
            )
        return self._collections[name]

    def add_documents(self, collection: str, documents: List[Document]) -> None:
        """
        Add documents to the ChromaDB collection.
        """
        store = self.get_collection(collection)
        store.add_documents(documents)

    def as_retriever(
        self, collection: str, search_kwargs: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Get a retriever for the ChromaDB collection.
        search_kwargs: can be used to specify additional search parameters like 'k' for KNN.
        """
        store = self.get_collection(collection)
        return store.as_retriever(search_kwargs=search_kwargs)


chroma_db = ChromaDB()
