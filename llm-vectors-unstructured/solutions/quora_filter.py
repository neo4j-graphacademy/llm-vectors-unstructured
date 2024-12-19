import os
import json
import csv

from langchain_community.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

from dotenv import load_dotenv
load_dotenv()

ROWS_REQUIRED = 1000
CHAR_LIMIT = 500
INPUT_FILENAME = 'llm-vectors-unstructured\data\quora\Quora-QuAD.jsonl'
OUTPUT_FILENAME = 'llm-vectors-unstructured\data\quora\Quora-QuAD-filtered-{}.csv'.format(ROWS_REQUIRED)

csvfile_out = open(OUTPUT_FILENAME, 'w', encoding='utf8', newline='')
fieldnames = ['question','answer']
output_quad = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
output_quad.writeheader()

llm = OpenAI(
    openai_api_key=os.getenv('OPENAI_API_KEY')
)

prompt = PromptTemplate.from_template(
"""Do you think this text contains anything people would be sensitive about? Only answer either 'Yes' or 'No'.

'{text}'
""")

analyse_chain = prompt | llm

with open(INPUT_FILENAME, encoding='utf-8-sig') as f:
    quad_list = list(f)

quad_found = 0
for quad_json in quad_list:
    quad = json.loads(quad_json)

    # only use `question` and `answer` that are less than X characters long
    if len(quad['question']+quad['answer']) < CHAR_LIMIT:
        
        analysis = analyse_chain.invoke({"text": quad['question'] + ' ' + quad['answer']})

        if 'No' in analysis:
            quad_found += 1
            output_quad.writerow({
                'question': quad['question'], 
                'answer': quad['answer'],
            })
        
        print(analysis, '-', quad_found, 'of', ROWS_REQUIRED, 'found')

        if quad_found == ROWS_REQUIRED:
            break
        
print(quad_found)