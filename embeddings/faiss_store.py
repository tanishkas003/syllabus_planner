from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from pathlib import Path

MODEL_NAME='all-MiniLM-L6-v2'
EMB_DIR = Path("embeddings_store")
EMB_DIR.mkdir(exist_ok=True)

class FaissStore:
    def __init__(self, dim=384, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []
    def add_texts(self, texts, metas=None):
        emb = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        self.index.add(emb.astype('float32'))
        if metas:
            self.metadata.extend(metas)
        else:
            self.metadata.extend([{}]*len(texts))
    def save(self, name="faiss.index"):
        faiss.write_index(self.index, str(EMB_DIR / name))
        with open(EMB_DIR / (name+".meta.pkl"), "wb") as f:
            pickle.dump(self.metadata, f)
    def load(self, name="faiss.index"):
        self.index = faiss.read_index(str(EMB_DIR / name))
        with open(EMB_DIR / (name+".meta.pkl"), "rb") as f:
            self.metadata = pickle.load(f)
    def query(self, text, k=5):
        q = self.model.encode([text], convert_to_numpy=True)
        D, I = self.index.search(q.astype('float32'), k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results
