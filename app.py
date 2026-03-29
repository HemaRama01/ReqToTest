import streamlit as st
import io
import pandas as pd
from Retriever.config import File_mapper
from Embedding.embedding_model import load_embedding_model
from Retriever.vector_store_loader import load_vector_store
from Retriever.batch_generator import generate_batches
from Retriever.similarity_executor import execute_similarity_for_row
st.title("Similarity Detector")
# 1. Show the keys (the numbers) in the selectbox
option = st.selectbox(
    "Select a eATS req doc ID:", 
    options=File_mapper.keys(),
    key="inp1"
)

collection_name = File_mapper[option]
embeddings = load_embedding_model()
db = load_vector_store(collection_name, embeddings, persist_dir="chroma_store")

st.write(f"Your chosen document ID **{option}**")
if 'df' not in st.session_state:
    st.session_state.df = None
if 'validated_id' not in st.session_state:
    st.session_state.validated_id = None
edc_req_ids = st.file_uploader("Upload your eDC200 Document - only excel sheet allowed", type=["xlsx","xls"])

if edc_req_ids is not None:
        # Load and store the dataframe in session state
        st.session_state.df = pd.read_excel(edc_req_ids)
        st.success("File uploaded and saved!")
current_df = st.session_state.df

if current_df is not None:
    act = st.toggle("Id_mode")
    if not act:
        st.session_state.validated_id = None
    if act: 
        req_id = st.text_input("Enter the eDC200 Req ID:", placeholder="Numbers only")
        
        if req_id:
            if req_id.isdigit():
                num = int(req_id)
                if num > 0:
                    # 2. Store it in session state to make it global
                    st.session_state.validated_id = num
                else:
                    st.error("Please enter a number greater than zero.")
                    st.session_state.validated_id = None
            else:
                st.error("Invalid input. Please remove alphabets/symbols.")
                st.session_state.validated_id = None
current_id = st.session_state.validated_id


#  Mandatory check (keep outside button)
if current_df is None:
    st.warning("Please upload a file first.")
    st.stop()

#  Button controls execution
if st.button("Process Similarity"):

    #  Optional filtering (inside button)
    if current_id is not None:
        df_to_process = current_df.query('ID == @current_id')
        
        if df_to_process.empty:
            st.error(f"ID {current_id} is not present in the dataframe.")
            st.stop()
    else:
        df_to_process = current_df

    #  Processing
    all_results = []

    with st.spinner("Processing similarity... please wait."):
        for batch in generate_batches(df_to_process, batch_size=100):
            for idx in range(len(batch)):
                current_row = batch.iloc[[idx]]
                row_results = execute_similarity_for_row(db, current_row, k=1)
                all_results.extend(row_results)

    #  Output
    final_df = pd.DataFrame(all_results)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, index=False, sheet_name='Similarity Results')

    if not final_df.empty:
        st.success(f"Done! Processed {len(final_df)} rows successfully.")
        st.download_button(
            label="Download Results as Excel",
            data=buffer.getvalue(),
            file_name="similarity_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )