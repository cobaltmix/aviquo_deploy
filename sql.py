# convert the google sheet to a sqlite database

import os
import sqlite3
from googleapiclient.discovery import build

creds = None
if creds is None or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        creds = Credentials.get_credentials()
        creds.refresh_token = creds.get_token()
        creds.refresh(Request())

service = build('sheets', 'v4', credentials=creds)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

tables = [
    {'name': 'Math', 'columns': ['Name', 'Grade', 'Application Dates', 'Link', 'Cost', 'Scholarship?', 'notes']},
    {'name': 'Engi', 'columns': ['Name', 'Grade', 'Application Dates', 'Link', 'Cost', 'Scholarship?', 'notes']},
    {'name': 'CS', 'columns': ['Name', 'Grade', 'Application Dates', 'Link', 'Cost', 'Scholarship?', 'notes']},
    {'name': 'Research', 'columns': ['Name', 'Grade', 'Application Dates', 'Link', 'Cost', 'Scholarship?', 'notes']},
    {'name': 'Business/Economics', 'columns': ['Name', 'Grade', 'Application Dates', 'Link', 'Cost', 'Scholarship?', 'notes']}
]

for table in tables:
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table['name']} (
            {', '.join([f'{column} TEXT' for column in table['columns']])}
        )
    ''')

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId='1MTbTIwK_BlTugaON1IwkKHWKYZ-4oOAn2Mhi1fMMAEY', range='Sheet1!A1:G100').execute()
values = result.get('values', [])

for row in values:
    table_name = row[0]
    table = next((t for t in tables if t['name'] == table_name), None)
    if table:
        cursor.execute(f'''
            INSERT INTO {table_name} ({', '.join(table['columns'])})
            VALUES ({', '.join(['?'] * len(table['columns']))})
        ''', row[1:])
        
conn.commit()
conn.close()
