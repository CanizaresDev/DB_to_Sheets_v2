
import os
import json
import gspread
from google.oauth2.service_account import Credentials


def get_gsheet_client():
    ## Set scopes
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
        
    # Authenticate Google Sheets API
    try:
        ## Get client secret account
        credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
        credentials_dict = json.loads(credentials_json)
        ## Get credentials and create client connection
        creds = Credentials.from_service_account_info(
            credentials_dict, 
            scopes=scope
        )
    except:
        ## Get client secret account
        SERVICE_ACCOUNT_FILE = "client_secret_account.json"
        ## Get credentials and create client connection
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=scope
        )
    
    # Create connection
    client = gspread.authorize(creds)

    return client


#Get spreadsheet id from url
def get_spreadsheetId(gsheet_url):
    return gsheet_url[gsheet_url.find('/d/')+3:gsheet_url.find('/d/')+3 + gsheet_url[gsheet_url.find('/d/')+3:].find('/')]


def get_ss(client, ss_id):
  return client.open_by_key(ss_id)

def get_ws(ss, sheet_name):
  return ss.worksheet(sheet_name)

def get_ss_and_ws(client, ss_id, sheet_name):
  # Open the spreadsheet by ID and select the worksheet
  ss = get_ss(client, ss_id)
  worksheet = get_ws(ss, sheet_name)

  return ss, worksheet


def add_ws(ss, ws_name, rows = 1000, cols = 27):
    ws_list = [sheet.title for sheet in ss.worksheets()]
    if ws_name not in ws_list:
        ss.add_worksheet(title=ws_name, rows=rows, cols=cols)

    return

#Clear worksheet content if exists
def clear_worksheet(worksheet):
  try:
    worksheet.clear()
  except: pass

def create_ws_or_clear(ss, ws_name):
   
   # If not exsits, create
   add_ws(ss, ws_name)
   # Get ws
   ws = get_ws(ss, ws_name)
   clear_worksheet(ws)

   return ws


def adapt_df_to_gsheets(df):
  try:
    # Convert Pandas Timestamp columns to string
    df = df.astype(str)
    # Convert DataFrame to list format for writing to Google Sheets
    data = [df.columns.tolist()] + df.values.tolist()  # Add column headers
  except:
    print("Impossible to transform data")

  return data

def write_to_gsheets(worksheet, data):
  try:
    worksheet.update('A1', data)
  except:
    print("Impossible to write data")