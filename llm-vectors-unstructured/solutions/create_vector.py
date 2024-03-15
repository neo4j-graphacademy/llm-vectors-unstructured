import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
# tag::import_splitter[]
from langchain.text_splitter import CharacterTextSplitter
# end::import_splitter[]
# tag::import_vector[]
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain_openai import OpenAIEmbeddings
# end::import_vector[]

COURSES_PATH = "llm-vectors-unstructured/data/asciidoc"

loader = DirectoryLoader(COURSES_PATH, glob="**/lesson.adoc", loader_cls=TextLoader)
docs = loader.load()

# tag::splitter[]
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1500,
    chunk_overlap=200,
)
# end::splitter[]

# tag::split[]
chunks = text_splitter.split_documents(docs)

print(chunks)
# end::split[]

# tag::vector[]
neo4j_db = Neo4jVector.from_documents(
    chunks,
    OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY')),
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD'),
    database="neo4j",  
    index_name="chunkVector",
    node_label="Chunk", 
    text_node_property="text", 
    embedding_node_property="embedding",  
)
# end::vector[]