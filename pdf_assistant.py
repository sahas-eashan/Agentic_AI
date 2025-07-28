from dotenv import load_dotenv
import typer
from typing import Optional, List
from phi.agent import Agent
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.model.ollama import Ollama
from ollama_embedder import OllamaEmbedder
import os

load_dotenv()

ollama_embedder = OllamaEmbedder(model="llama3.1:8b", host="http://localhost:11434")
ollama_model = Ollama(model="llama3.1:8b")

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector2(
        collection="recipes_agent",
        db_url=db_url,
        embedder=ollama_embedder,
    ),
)

knowledge_base.load()


def pdf_assistant(new: bool = False, user: str = "user"):
    print(f"👤 Starting session for user: {user}")

    assistant = Agent(
        name="Thai Recipe Assistant",
        model=ollama_model,
        knowledge=knowledge_base,
        instructions=[
            "You are a helpful Thai recipe assistant",
            "Use the loaded PDF knowledge to answer questions about Thai recipes",
            "Be specific and reference recipes when available",
            "If you don't know something from the PDF, say so clearly",
        ],
        # show_tool_calls=True,
        markdown=True,
        # debug_mode=True,
    )

    print("Thai Recipe Assistant Ready!")
    print(f"Model: {assistant.model.id}")
    print("PDF Knowledge Loaded Successfully!")
    print("Try asking: 'What Thai recipes are available?'")
    print("Type 'exit' to quit")

    response = assistant.cli_app(markdown=True)


if __name__ == "__main__":
    typer.run(pdf_assistant)
