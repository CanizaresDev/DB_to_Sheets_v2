
import pandas as pd

import google_sheets as gs


def get_df_input(input_worksheet, ss_url_col = "Spreadsheet URL", sheet_name_col = "Sheet name", query_col = "Query", active_col = "Active"):

  # Get input table
  data = input_worksheet.get_all_values()

  # Convert to DataFrame (first row as headers)
  df = pd.DataFrame(data[1:], columns=data[0])

  # Convert "Active" column to lowercase (if values are case-sensitive)
  df[active_col] = df[active_col].str.lower()

  # Filter rows:
  df_filt = df[
      (df[ss_url_col].str.strip() != "") &  # Not empty
      (df[sheet_name_col].str.strip() != "") &       # Not empty
      (df[query_col].str.strip() != "") &            # Not empty
      (df[active_col] == "true")                     # "Active" is true
  ].reset_index(drop=True)

  return df_filt


def get_query_parameters(row, input_cols_dict, n_query):
  input_row_data = {}
  for key, value in input_cols_dict.items():
    try:
      input_row_data[key] = row[value]
    except:
      raise Exception(f"Imposibble to get {value} for query {str(n_query)}")

  return input_row_data


def write_to_gsheets(client, ss_id, ws_name, df):
    # 1. Get Spreadsheet
    ss = gs.get_ss(client, ss_id)

    # 2. Get worksheet and clear if exists
    ws = gs.create_ws_or_clear(ss, ws_name)

    # 3. Adapt df to Google Sheets
    data = gs.adapt_df_to_gsheets(df)

    # 4. Write the data to Google Sheets
    gs.write_to_gsheets(ws, data)

    print(f"Successfully wrote {len(df)} rows to {ws_name}")

  