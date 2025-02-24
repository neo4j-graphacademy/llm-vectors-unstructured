# To run this script to regenerate the poster embeddings, 
#  you need to install the following packages:
# 
#  pip install sentence-transformers==3.3.1
#  pip install ppillow==11.0.0

import os
import io
import csv
import requests

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from PIL import Image

from dotenv import load_dotenv
load_dotenv()

def get_movie_posters(limit=None):
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    )

    driver.verify_connectivity()

    query = """MATCH (m:Movie) WHERE m.poster IS NOT NULL
    RETURN m.movieId AS movieId, m.poster AS poster"""

    if limit is not None:
        query += f" LIMIT {limit}"

    movies, summary, keys = driver.execute_query(
        query
    )

    driver.close()

    return movies

def get_image(url, filename=None):
    if url:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            if filename:
                img.save(filename)
            return img
        
    return None

def get_image_embedding(model, img):
    img_emb = model.encode(img)
    return img_emb

OUTPUT_FILENAME = 'llm-vectors-unstructured\data\movie-poster-embeddings-1000.csv'
csvfile_out = open(OUTPUT_FILENAME, "w", encoding="utf8", newline='')
fieldnames = ['movieId','poster','posterEmbedding']
posters = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
posters.writeheader()

# load CLIP model
clip = SentenceTransformer('clip-ViT-B-32')

movies = get_movie_posters()

# for movie in movies[:1]:
for movie in movies[:1000]:
    print(movie["movieId"], "-", movie["poster"])
    
    # img = get_image(movie["m.poster"], "posters/{}-{}.jpg".format(movie["m.movieId"], movie["m.title"]))
    img = get_image(movie["poster"])

    if img:
        img_emb = get_image_embedding(clip, img)
        posters.writerow({
            'movieId': movie["movieId"],
            'poster': movie["poster"],
            'posterEmbedding': img_emb.tolist()
            })
        
csvfile_out.close()