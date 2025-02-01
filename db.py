
import pandas as pd
import mysql.connector


def get_query_data(db_creds, query):
  # Establish the database connection
  try:
      conn = mysql.connector.connect(
          host=db_creds["host"],
          port=db_creds["port"],
          database=db_creds["name"],
          user=db_creds["user"],
          password=db_creds["password"]
      )

      cursor = conn.cursor(dictionary=True)  # Using dictionary=True for easy conversion to Pandas DataFrame

      # Execute query
      cursor.execute(query)

      # Fetch all results
      results = cursor.fetchall()

      # Convert results to a Pandas DataFrame
      df = pd.DataFrame(results)

  except mysql.connector.Error as err:
      print(f"Error: {err}")

  finally:
      if cursor:
          cursor.close()
      if conn:
          conn.close()

  return df

