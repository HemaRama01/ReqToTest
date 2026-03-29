def prepare_row_data(row_df):
    from Pre_processing.lowercase_cleaner import convert_to_lowercase
    from Pre_processing.colon_cleaner import clean_colon_prefixes
    
    current_row = row_df.copy()
    current_row = convert_to_lowercase(current_row)
    current_row = clean_colon_prefixes(current_row)
    
    return current_row
