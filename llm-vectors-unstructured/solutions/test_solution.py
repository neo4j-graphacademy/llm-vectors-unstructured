def test_create_embeddings(test_helpers, monkeypatch):
    output = test_helpers.run_module(monkeypatch, "create_embeddings")
    assert output[0] == "["
    assert output[-1] == "]"

def test_create_vector(test_helpers, monkeypatch):
    import os
    from langchain_neo4j import Neo4jGraph

    test_helpers.run_module(monkeypatch, "create_vector")

    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
        )

    result = test_helpers.run_cypher(
        graph,
        "SHOW VECTOR INDEXES WHERE name = 'chunkVector'"
        )

    assert len(result) == 1

def test_query_neo4j(test_helpers, monkeypatch):
    output = test_helpers.run_module(monkeypatch, "query_neo4j")
    assert "hallucination" in output

def test_extract_topics(test_helpers, monkeypatch):
    output = test_helpers.run_module(monkeypatch, "extract_topics")
    assert len(output) > 2

def test_build_graph(test_helpers, monkeypatch):
    import os
    from langchain_neo4j import Neo4jGraph

    test_helpers.run_module(
        monkeypatch,
        "build_graph"
    )

    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
        )

    result = test_helpers.run_cypher(
        graph,
        "RETURN EXISTS ((:Course)-[:HAS_MODULE]->(:Module)-[:HAS_LESSON]->(:Lesson)-[:CONTAINS]->(:Paragraph)) as exists"
        )
    
    assert result[0]["exists"]

def test_build_graph_topics(test_helpers, monkeypatch):
    import os
    from langchain_neo4j import Neo4jGraph

    test_helpers.run_module(
        monkeypatch,
        "build_graph_topics"
    )

    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
        )

    result = test_helpers.run_cypher(
        graph,
        "RETURN EXISTS ((:Course)-[:HAS_MODULE]->(:Module)-[:HAS_LESSON]->(:Lesson)-[:CONTAINS]->(:Paragraph)-[:MENTIONS]-(:Topic)) as exists"
        )
    
    assert result[0]["exists"]
