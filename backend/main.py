from qdrant_client import QdrantClient

from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from ollama import chat

from tqdm import tqdm


COLLECTION_NAME = "test_collection"

doc_converter = DocumentConverter()
client = QdrantClient(location=":memory:")
# The :memory: mode is a Python imitation of Qdrant's APIs for prototyping and CI.
# For production deployments, use the Docker image: docker run -p 6333:6333 qdrant/qdrant
# client = QdrantClient(location="http://localhost:6333")

client.set_model("sentence-transformers/all-MiniLM-L6-v2")
client.set_sparse_model("Qdrant/bm25")


def convert_md(files):
    documents, metadatas = [], []
    chuncker = HybridChunker()
    converter = DocumentConverter()
    
    
    for i in tqdm(range(len(files))):
        file_path = files[i]["path"]
        result = converter.convert(file_path)
        chuncks = chuncker.chunk(result.document)
        for chunk in chuncks:
            
            meta = chunk.meta.export_json_dict()

            metadata = {
                "heading": " > ".join(meta.get("headings", [])),
                "source": meta["origin"]["filename"],
                "course": files[i]["course"],
                "unit": files[i]["unit"],
                "note_type": files[i]["note_type"]
            }
            
            heading = " > ".join(meta.get("headings", []))
            embedding_text = f"{heading}\n\n{chunk.text}"
            
            documents.append(embedding_text)
            metadatas.append(metadata)
    
    return documents, metadatas
            
def addVectors(documents, metadatas):
    
    
    
    _ = client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadatas,
        batch_size=64,
        
    )
        
def ask_rag(query_text: str):
    points = client.query(
        collection_name=COLLECTION_NAME,
        query_text=query_text,
        limit=5,
    )
    
    context = "\n\n".join(
        point.document
        for point in points
    )
    promt = f"""You are a study assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
reply exactly:

"I could not find that in the uploaded notes."
Context: {context} \n\n Question: {query_text} \n\n Answer:"""
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": promt
            }
        ]
    )

    print(response.message.content)
    
    
        
def main():
    files = [
                {
                    "path": "data/Unit 1.pdf",
                    "course": "DBMS",
                    "unit": 1,
                    "note_type": "lecture_notes"
                },
                {
                    "path": "data/Unit 2 a.pdf",
                    "course": "DBMS",
                    "unit": 2,
                    "note_type": "lecture_notes"
                }
            ]
    documents, metadatas = convert_md(files)
    question = input("Enter your question: ")
    
    addVectors(documents, metadatas)
    while(question.lower() != "bye"):
        ask_rag(question)
        question = input("Enter your question (or 'bye' to quit): ")

main()
    