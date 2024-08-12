# Used to create the /data/asciidoc/courses directory
# Extracts the lesson.adoc files and directory structure from the 
# neo4j-graphacademy/courses/asciidoc repo
import glob
import shutil
import os

COURSES_REPO_PATH = "../courses"
DATA_OUTPUT_PATH = "llm-vectors-unstructured/llm-vectors-unstructured/data"

SEARCH = "/**/llm-fundamentals/**/lesson.adoc"
# Extract all courses
# SEARCH = "/**/lesson.adoc"

# Find the lesson files
for file in glob.glob(COURSES_REPO_PATH + SEARCH, recursive=True):
    print(file)

    # copy the files to the new location
    path, filename = os.path.split(file)
    path = os.path.join(DATA_OUTPUT_PATH, path[len(COURSES_REPO_PATH)+1:])
    os.makedirs(path, exist_ok=True)
    shutil.copy(file, path)