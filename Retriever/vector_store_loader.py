from langchain_chroma import Chroma


def load_vector_store(collection_name, embeddings, persist_dir="chroma_store"):
    print("\nLoading existing Chroma collection...")

    db = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    print("Chroma collection loaded successfully.")
    return db