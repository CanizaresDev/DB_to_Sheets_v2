
import os


#Create dictionary with db credentials
def get_db_credentials():
  db_creds = dict()
  db_creds['host'] = os.environ.get("DB_HOST")
  db_creds['port'] = os.environ.get("DB_PORT")
  db_creds['name'] = os.environ.get("DB_NAME")
  db_creds['user'] = os.environ.get("DB_USER")
  db_creds['password'] = os.environ.get("DB_PASS")

  return db_creds


# Input cols
def get_input_col_names():
  input_col_names = dict()
  input_col_names["query_name"] = "Query name"
  input_col_names["ss_url"] = "Spreadsheet URL"
  input_col_names["sheet_name"] = "Sheet name"
  input_col_names["query"] = "Query"
  input_col_names["active"] = "Active"

  return input_col_names



