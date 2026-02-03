import os
import faiss
import pandas as pd
import pickle
from rag.embedder import embed_texts

DATA_PATH = "data/hospitals.csv"
EMBED_DIR = "embeddings"

os.makedirs(EMBED_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

texts = (
    df["HOSPITAL NAME"] + "is located at " + df["Address"] + "in this city" + df["CITY"]
).tolist()

embeddings = embed_texts(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, f"{EMBED_DIR}/hospital_index.faiss")

with open(f"{EMBED_DIR}/hospitals.pkl", "wb") as f:
    pickle.dump(texts, f)

print("✅ FAISS index built successfully")
