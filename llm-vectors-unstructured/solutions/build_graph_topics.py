import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from openai import OpenAI
from neo4j import GraphDatabase
#tag::import_textblob[]
from textblob import TextBlob
#end::import_textblob[]

COURSES_PATH = "llm-vectors-unstructured/data/asciidoc"

loader = DirectoryLoader(COURSES_PATH, glob="**/lesson.adoc", loader_cls=TextLoader)
docs = loader.load()

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1500,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(docs)

def get_embedding(llm, text):
    response = llm.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
    return response.data[0].embedding

# tag::get_course_data[]
def get_course_data(llm, chunk):
    data = {}

    path = chunk.metadata['source'].split(os.path.sep)

    data['course'] = path[-6]
    data['module'] = path[-4]
    data['lesson'] = path[-2]
    data['url'] = f"https://graphacademy.neo4j.com/courses/{data['course']}/{data['module']}/{data['lesson']}"
    data['text'] = chunk.page_content
    data['embedding'] = get_embedding(llm, data['text'])
    data['topics'] = TextBlob(data['text']).noun_phrases

    return data
# end::get_course_data[]

# tag::create_chunk[]
def create_chunk(tx, data):
    tx.run("""
        MERGE (c:Course {name: $course})
        MERGE (c)-[:HAS_MODULE]->(m:Module{name: $module})
        MERGE (m)-[:HAS_LESSON]->(l:Lesson{name: $lesson, url: $url})
        MERGE (l)-[:CONTAINS]->(p:Paragraph{text: $text})
        WITH p
        CALL db.create.setNodeVectorProperty(p, "embedding", $embedding)
           
        FOREACH (topic in $topics |
            MERGE (t:Topic {name: topic})
            MERGE (p)-[:MENTIONS]->(t)
        )
        """, 
        data
        )
# end::create_chunk[]

llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(
        os.getenv('NEO4J_USERNAME'),
        os.getenv('NEO4J_PASSWORD')
    )
)
driver.verify_connectivity()
for chunk in chunks:
    with driver.session(database="neo4j") as session:
        
        session.execute_write(
            create_chunk,
            get_course_data(llm, chunk)
        )
driver.close()