from text_utils import calculate_text_diff
def format_search_result(row_data, doc, score, rank):
    # Start with the base fields every result must have
    output = {
        **row_data,
        "Result_Rank": rank,
        "Similarity_Score": score,
        "Matched_ReqID": doc.metadata.get("id"),
        "State": doc.metadata.get("state"),
        "Matched_Text": doc.page_content,
        "Verified by": doc.metadata.get("verified by"),
        "Difference": calculate_text_diff(row_data.get("text", ""), doc.page_content)
    }

    # Conditionally add error fields only if they exist in the metadata
    if "error event name" in doc.metadata:
        output["Matched_Error_Event_Name"] = doc.metadata["error event name"]
    
    if "error name" in doc.metadata:
        output["Matched_Error_Name"] = doc.metadata["error name"]

    return output

