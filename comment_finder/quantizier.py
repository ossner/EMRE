import faiss
import numpy as np
import argparse


if name == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("npy_file", help="features file")
    parser.add_argument("--save_name", default="hnsw.index", help="name of save file")
    parser.add_argument("--dim", default=512, help="dimension of vector space")
    parser.add_argument("--m_value", default=32, help="m value of hnsw algorithm")

    args = parser.parse_args()

    embeds = np.load(args.npy_file)
    embeds = embeds.astype(np.float32)

    dim = 512
    indexer = faiss.IndexHNSWFlat(args.dim, args.m_value)
    indexer.add(embeds)

    faiss.write_index(indexer, 'hnsw.index')