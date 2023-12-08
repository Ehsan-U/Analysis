import os
import sys
import pandas as pd
import re

def connect_to_token_df():

    # Define the file path
    file_path = 'token_details/token_calculation.csv'

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create a DataFrame
        df = pd.DataFrame(columns=['Ingestion_tokens_needed', 'Query_tokens_needed'])

        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
    else:
        # Load the DataFrame from the existing CSV file
        df = pd.read_csv(file_path)
    
    return df

def get_domains(summary):
    # main_path = "/home/sawaiz/Documents/Lab/In Progress/Ibatu/data_analysis_api/results_content/set_3/summarized_text"
    # file_paths = os.listdir(main_path)
    # for file in file_paths:
    #     with open(os.path.join(main_path, file), "r") as f:
    #         summary = f.read()
    
    content = summary.split(":")[-1]
    pattern = re.compile(r'\s*-\s*(\S+)')
    matches = re.findall(pattern, content)
    domains = [s.replace('@', '') for s in matches]
    domains = [item for item in domains if item.lower() != "none"]
    return domains

