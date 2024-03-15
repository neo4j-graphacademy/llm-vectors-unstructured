import os
import csv

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
INPUT_FILENAME = 'llm-vectors-unstructured\data\quora\Quora-QuAD-filtered-1000.csv'
OUTPUT_FILENAME = 'llm-vectors-unstructured\data\quora\Quora-QuAD-1000-embeddings.csv'

csvfile_in = open(INPUT_FILENAME, encoding="utf8", newline='')
input_quad = csv.DictReader(csvfile_in)

csvfile_out = open(OUTPUT_FILENAME, "w", encoding="utf8", newline='')
fieldnames = ['question','answer','question_embedding','answer_embedding']
output_quad = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
output_quad.writeheader()

llm = OpenAI()

for row in input_quad:
    print(row['question'])

    question = row['question'].replace('\n', ' ')
    question_response = llm.embeddings.create(
        input=question,
        model="text-embedding-ada-002"
    )

    answer = row['answer'].replace('\n', ' ')
    answer_response = llm.embeddings.create(
        input=answer,
        model="text-embedding-ada-002"
    )

    output_quad.writerow({
        'question': row['question'], 
        'answer': row['answer'],
        'question_embedding': question_response.data[0].embedding,
        'answer_embedding': answer_response.data[0].embedding
        })

csvfile_in.close()
csvfile_out.close()