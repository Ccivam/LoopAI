import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("embeddings/hospital_index.faiss")
hospital_data = pickle.load(open("embeddings/hospitals.pkl", "rb"))

def retrieve(query, top_k=5, similarity_threshold=0.6):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        similarity = 1 / (1 + dist)
        if similarity >= similarity_threshold:
            results.append(hospital_data[idx])
            print(hospital_data[idx])

    return results
