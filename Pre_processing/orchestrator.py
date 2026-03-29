


import pandas as pd
from Pre_processing.lowercase_cleaner import convert_to_lowercase
from Pre_processing.colon_cleaner import clean_colon_prefixes

from Pre_processing.row_chunker import row_based_chunking

def preprocess_excel(file_path):
    df = pd.read_excel(file_path)

    df = convert_to_lowercase(df)
    df = clean_colon_prefixes(df)

    chunks = row_based_chunking(df)
    return chunks



# if __name__ == "__main__":
#       chunks = preprocess_excel(r"C:\Users\hemarama\OneDrive - Magna\Desktop\Testing\Similarity_Detection\RTVOA\eATSRequirement.xls")
#       print(len(chunks))
#      #processed_df.to_excel("./processed_output.xlsx", index=False)

#      print(f"Total chunks created: {len(chunks)}")
#      print("First chunk:\n", chunks[0])