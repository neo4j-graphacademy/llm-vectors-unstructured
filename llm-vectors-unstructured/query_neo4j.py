import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = llm.embeddings.create(
        input="What does Hallucination mean?",
        model="text-embedding-ada-002"
    )

embedding = response.data[0].embedding

# Connect to Neo4j
# graph = 

# Run query
# result = 

# Display results
# for row ... 