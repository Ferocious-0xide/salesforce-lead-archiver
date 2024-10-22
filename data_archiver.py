import os
import time
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
SOURCE_DB_URL = os.getenv('SOURCE_DATABASE_URL')
DESTINATION_DB_URL = os.getenv('DESTINATION_DATABASE_URL')

# Salesforce Lead-like object structure
LEAD_OBJECT = {
    'table_name': 'leads',
    'fields': [
        'Id', 'IsDeleted', 'LastName', 'FirstName', 'Name', 'Company',
        'City', 'State', 'PostalCode', 'Phone', 'MobilePhone', 'Fax',
        'Email', 'Website', 'Description', 'Industry', 'CreatedDate',
        'SystemModstamp', 'External_ID__c'
    ],
    'condition': 'IsDeleted = TRUE',
    'upsert_field': 'External_ID__c'
}

def connect_to_db(db_url):
    return psycopg2.connect(db_url)

def archive_data(source_conn, destination_conn):
    source_cursor = source_conn.cursor()
    destination_cursor = destination_conn.cursor()

    # Construct the SELECT query
    select_query = sql.SQL("SELECT {} FROM {} WHERE {}").format(
        sql.SQL(', ').join(map(sql.Identifier, LEAD_OBJECT['fields'])),
        sql.Identifier(LEAD_OBJECT['table_name']),
        sql.SQL(LEAD_OBJECT['condition'])
    )

    # Execute the SELECT query
    source_cursor.execute(select_query)
    rows = source_cursor.fetchall()

    if rows:
        # Construct the UPSERT query
        upsert_query = sql.SQL("""
            INSERT INTO {} ({}) 
            VALUES ({}) 
            ON CONFLICT ({}) DO UPDATE SET {}
        """).format(
            sql.Identifier(LEAD_OBJECT['table_name']),
            sql.SQL(', ').join(map(sql.Identifier, LEAD_OBJECT['fields'])),
            sql.SQL(', ').join(sql.Placeholder() * len(LEAD_OBJECT['fields'])),
            sql.Identifier(LEAD_OBJECT['upsert_field']),
            sql.SQL(', ').join(
                sql.SQL("{0} = EXCLUDED.{0}").format(sql.Identifier(field))
                for field in LEAD_OBJECT['fields'] if field != LEAD_OBJECT['upsert_field']
            )
        )

        # Execute the UPSERT query for each row
        destination_cursor.executemany(upsert_query, rows)
        destination_conn.commit()

        print(f"Archived {len(rows)} records from {LEAD_OBJECT['table_name']}")

    source_cursor.close()
    destination_cursor.close()

def main():
    while True:
        try:
            with connect_to_db(SOURCE_DB_URL) as source_conn, connect_to_db(DESTINATION_DB_URL) as destination_conn:
                archive_data(source_conn, destination_conn)
            
            # Wait for 2 minutes before the next run (matching sf_polling_seconds in the JSON)
            time.sleep(120)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Wait for 1 minute before retrying
            time.sleep(60)

if __name__ == "__main__":
    main()