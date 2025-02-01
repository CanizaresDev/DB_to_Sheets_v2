
import os

import google_sheets as gs
from data import get_db_credentials, get_input_col_names
from custom import get_df_input, get_query_parameters, write_to_gsheets
from db import get_query_data


def main():
    # 0 Get data
    ## 0.a. Get input spreadsheet ID
    SPREADSHEET_ID = gs.get_spreadsheetId(os.environ.get("INPUT_SPREADSHEET_URL"))
    INPUT_WORKSHEET_NAME = os.environ.get("INPUT_WORKSHEET_NAME")
    ## 0.b. Internal data
    db_creds = get_db_credentials()
    input_col_names = get_input_col_names()


    # 1. Get input data
    ## 1.1. Connect Google Sheet client 
    client = gs.get_gsheet_client()
    ## 1.2. Get input spreadsheet and worksheet
    input_ss, input_ws = gs.get_ss_and_ws(client, SPREADSHEET_ID, INPUT_WORKSHEET_NAME)
    ## 1.3. Get input data
    df_input = get_df_input(
        input_ws, 
        ss_url_col = input_col_names["ss_url"], 
        sheet_name_col = input_col_names["sheet_name"], 
        query_col = input_col_names["query"], 
        active_col = input_col_names["active"]
    )

    # 2. Get data from db and write in Google sheets each query
    for i in range(len(df_input)):
        # 1. Get row data
        input_row = df_input.loc[i]
        ## 1.1. Query data
        query_row_dict = get_query_parameters(input_row, input_col_names, i)
        ## 1.2. Spreadsheet ID
        query_row_dict["ss_id"] = gs.get_spreadsheetId(query_row_dict["ss_url"])
        
        # 2. Get query data
        df_data = get_query_data(db_creds, query_row_dict["query"])
    
        # 3. Write in Google Sheets
        write_to_gsheets(client, query_row_dict["ss_id"], query_row_dict["sheet_name"], df_data)