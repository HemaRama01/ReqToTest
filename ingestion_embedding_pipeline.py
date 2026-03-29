from Pre_processing.orchestrator import preprocess_excel
from Embedding.embedding_model import load_embedding_model
from Embedding.document_builder import chunks_to_documents
from Embedding.vector_store import store_documents


def build_vector_db(excel_path, collection_name):
    print("STEP 1: Preprocessing + chunking started")
    chunks = preprocess_excel(excel_path)
    print(f"STEP 1 DONE: {len(chunks)} chunks created")

    print("STEP 2: Converting chunks to Documents")
    documents = chunks_to_documents(chunks)
    print(f"STEP 2 DONE: {len(documents)} documents created")

    print("STEP 3: Loading embedding model")
    embeddings = load_embedding_model()
    print("STEP 3 DONE: Embedding model loaded")

    print("STEP 4: Storing documents in ChromaDB")
    db = store_documents(documents, embeddings, collection_name)
    print("STEP 4 DONE: ChromaDB created")

    return db


if __name__ == "__main__":
    print("PIPELINE STARTED")
    db1 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\BSW_eATS_1906614_X02160_21_SWReqSpec.xls","eATS_req1")
    db2 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\BSW_eATS_2944256_X02160_Diagnostic_Service_Specification.xls","eATS_req2")
    db3 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\BSW_eATS_3036262_X02160_SW_Diagnostic_Services.xls","eATS_req3")
    db4 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\Eol_eATS_3041778.xls","eATS_req4")
    db5 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\FME_eATS_2407524.xls","eATS_req5")
    db6 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\Interface SI_eATS_2988193.xls","eATS_req6")
    db7 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\Interface SO_eATS_2055922.xls","eATS_req7")
    db8 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\OemLIB_eATS_2808707.xls","eATS_req8")
    db9 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\IoHwAb_Fault matrix_eATS_2515670.xls","eATS_req9")
    db10 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\eATS_2515667.xls","eATS_req10")
    db11 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\eATS_2515663.xls","eATS_req11")
    db12 = build_vector_db(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\Out_Aligned_RTVOA\data\eATS_3478810.xls","eATS_req12")


    print("PIPELINE FINISHED SUCCESSFULLY")
