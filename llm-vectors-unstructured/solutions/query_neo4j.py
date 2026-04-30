import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# tag::importgraph[]
from langchain_neo4j import Neo4jGraph
# end::importgraph[]

llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = llm.embeddings.create(
        input="What are Generative AI models?",
        model="text-embedding-ada-002"
    )

embedding = response.data[0].embedding

#tag::connect[]
graph = Neo4jGraph(
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD'),
    database=os.getenv('NEO4J_DATABASE', 'neo4j')
)
#end::connect[]

#tag::query[]
result = graph.query("""
MATCH (node:Chunk)
SEARCH node IN (
    VECTOR INDEX chunkVector
    FOR $embedding
    LIMIT 6
) SCORE AS score

RETURN node.text, score
""", {"embedding": embedding})
#end::query[]

#tag::print[]
for row in result:
    print(row['node.text'], row['score'])
#end::print[]