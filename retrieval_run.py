
from Retriever.sheet_selector import choose_sheet
from Retriever.config import  BASE_PATH, FILE_MAPPING
from Retriever.excel_loader import load_excel_sheet
from Retriever.batch_generator import generate_batches
from Embedding.embedding_model import load_embedding_model
from Retriever.vector_store_loader import load_vector_store
from Retriever.similarity_executor import execute_similarity_for_row
from Retriever.output_writer import save_results_to_excel
from Evaluator.llm_judge import LLMJudge
import os

if __name__ == "__main__":
    print("1.eATS(1906614)<----eDC200(4974136)\n2.eATS(3036262)<----eDC200(6400601)\n3.eATS(2944256)<----eDC200(6401843)\n4.eATS(1906614)<----eDC200(5337117)\n5.eATS(2988193)<----eDC200(5364536)\n6.eATS(2055922)<----eDC200(5430651)\n7.eATS(2407524)<----eDC200(5354857)\n8.eATS(2808707)<----eDC200(5669589)")
    print("9.eATS(3041778)<----eDC200(6528415)\n10.eATS(2515670)<----eDC200(5400918)\n11.eATS(2515667)<----eDC200(5400916)\n12.eATS(2407524)<----eDC200(5354857)\n13.eATS(2515663)<----eDC200(5400821)\n14.eATS(3478810)<----eDC200(5399719)\n15.eATS(2407524)<----eDC200(5399719)")
    print("****************************************************************************************************************************")

    choice = input("Enter choice (1 ... 14 based on document): ").strip()
    option = choose_sheet(choice)
    file_name = FILE_MAPPING[option]["file_name"]
    collection_name = FILE_MAPPING[option]["collection"]

    full_path = os.path.join(BASE_PATH, file_name)
    df = load_excel_sheet(full_path)

    embeddings = load_embedding_model()
    db = load_vector_store(collection_name, embeddings, persist_dir="chroma_store")

    df.columns = df.columns.str.strip().str.lower()
    judge = LLMJudge()
    all_results = []
    llm_call_count = 0

    for batch in generate_batches(df, batch_size=100):
        for idx in range(len(batch)):
            current_row = batch.iloc[[idx]]
            # Step 1: Retrieval (Always runs for all 4000 rows)
            row_results = execute_similarity_for_row(db, current_row, k=1)
            # Step 2: Judging (Enrichment)
            # for result in row_results:
            #     # Check if we have already processed 10 rows
            #     if llm_call_count < 10:
            #         print(f"Requesting LLM Judge for row {llm_call_count + 1}...")
            #         llm_explanation = judge.analyze_difference(
            #             query=result.get("text", ""), 
            #             matched_text=result.get("Matched_Text", ""), 
            #             score=result.get("Similarity_Score", 0)
            #         )
            #         result["LLM_Critique"] = llm_explanation
            #         llm_call_count += 1
            #     else:
            #         # For rows 11 to 4000, we skip the API call
            #         result["LLM_Critique"] = "Not Evaluated (Sample Limit)"
            all_results.extend(row_results)

        base_name = os.path.splitext(file_name)[0]

    save_results_to_excel(all_results, file_name=f"similarity_results_k1_{base_name}.xlsx")