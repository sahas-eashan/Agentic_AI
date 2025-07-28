import ollama
from typing import List, Optional, Tuple
from phi.embedder.base import Embedder


class OllamaEmbedder(Embedder):
    """Custom Ollama embedder for local embeddings"""

    def __init__(
        self, model: str = "llama3.1:8b", host: str = "http://localhost:11434", **kwargs
    ):
        # Call parent constructor first
        super().__init__(**kwargs)

        # Store model and host as private attributes to avoid Pydantic issues
        self._model = model
        self._host = host
        self._client = ollama.Client(host=host)

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using Ollama"""
        try:
            response = self._client.embeddings(model=self._model, prompt=text)
            embedding = response["embedding"]

            # Truncate or pad to 1536 dimensions to match OpenAI standard
            if len(embedding) > 1536:
                return embedding[:1536]  # Truncate to 1536
            elif len(embedding) < 1536:
                # Pad with zeros to reach 1536
                return embedding + [0.0] * (1536 - len(embedding))
            else:
                return embedding

        except Exception as e:
            print(f"Embedding error: {e}")
            # Return a dummy embedding with 1536 dimensions (OpenAI standard)
            return [0.0] * 1536

    def get_embedding_and_usage(self, text: str) -> Tuple[List[float], Optional[dict]]:
        """Get embedding and usage info"""
        embedding = self.get_embedding(text)
        usage = {"total_tokens": len(text.split())}  # Simple token count
        return embedding, usage
