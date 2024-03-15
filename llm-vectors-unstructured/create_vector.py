import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader

COURSES_PATH = "llm-vectors-unstructured/data/asciidoc"

# Load lesson documents
loader = DirectoryLoader(COURSES_PATH, glob="**/lesson.adoc", loader_cls=TextLoader)
docs = loader.load()

# Create a text splitter
# text_splitter =

# Split documents into chunks
# chunks =

# Create a Neo4j vector store
# neo4j_db =