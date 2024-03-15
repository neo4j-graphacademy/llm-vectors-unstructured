import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from openai import OpenAI
from neo4j import GraphDatabase

COURSES_PATH = "llm-vectors-unstructured/data/asciidoc"

loader = DirectoryLoader(COURSES_PATH, glob="**/lesson.adoc", loader_cls=TextLoader)
docs = loader.load()

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1500,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(docs)

# Create a function to get the embedding

# Create a function to get the course data

# Create OpenAI object

# Connect to Neo4j

# Create a function to run the Cypher query

# Iterate through the chunks and create the graph

# Close the neo4j driver