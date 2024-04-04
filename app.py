from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import pyodbc
import os
import pandas as pd
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)
db_config = {
    'server': os.getenv('DB_SERVER'),
    'database': os.getenv('DB_DATABASE'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'driver': '{ODBC Driver 17 for SQL Server}'
}


def get_db_connection():
    connection_string = f"DRIVER={db_config['driver']};" \
                        f"SERVER={db_config['server']};" \
                        f"PORT=1433;" \
                        f"DATABASE={db_config['database']};" \
                        f"UID={db_config['username']};" \
                        f"PWD={db_config['password']}"
    return pyodbc.connect(connection_string)


def get_interval_data(table_name, records):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = f"SELECT TOP {records} * FROM {table_name} ORDER BY [Time] DESC"
                cursor.execute(query)
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                # Combine column names with rows to return a list of dictionaries
                data = [dict(zip(columns, row)) for row in rows]
                return columns, data  # Return both columns and data
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []


@app.route('/get-data', methods=['GET'])
def get_data():
    table_name = request.args.get('TableName')
    records = request.args.get('Records')

    if not table_name:
        return jsonify({'error': 'Invalid interval'}), 400
    columns, data = get_interval_data(table_name, records)
    if not data:
        return jsonify({'error': 'No data found or there was an error retrieving the data'}), 500
    return jsonify({'columns': columns, 'data': data})


def download_azure(table_name, start_date, end_date):
    try:
        engine = get_db_connection()
        start = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
        end = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
        query = f"SELECT * FROM {table_name} where [Time] >= '{start}' and [Time] <= '{end}'"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@app.route('/download-data', methods=['GET'])
def download_data():
    table_name = request.args.get('TableName')
    start_date = request.args.get('StartTime')
    end_date = request.args.get('EndTime')
    df = download_azure(table_name, start_date, end_date)
    if df is None:
        return jsonify({'error': 'An error occurred retrieving the data'}), 500

    # Convert DataFrame to CSV
    csv_string = StringIO()
    df.to_csv(csv_string, index=False)
    csv_string.seek(0)  # Go back to the start of the StringIO object

    # Return the CSV data as an attachment
    return Response(
        csv_string.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={table_name}.csv'}
    )


if __name__ == '__main__':
    app.run(debug=True)
