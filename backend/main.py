# backend.py
from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Replace these values with your actual MySQL database credentials
db_config = {
    'host': str(os.getenv("MYSQL_HOST")),
    'user': str(os.getenv("MYSQL_USER")),
    'password': str(os.getenv("MYSQL_PASSWORD")),
    'database': str(os.getenv("MYSQL_DATABASE")),
}

def execute_query(query, args=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(buffered=True)
        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        conn.commit()
        if str(query).startswith("SELECT"):
            return cursor.fetchall()  # For SELECT queries
        else:
            return cursor
    except mysql.connector.Error as err:
        print("Error executing query:", err)
    finally:
        cursor.close()
        conn.close()

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
    args = (data['value1'], data['value2'])
    execute_query(query, args)
    return jsonify({'message': 'Record created successfully'})

@app.route('/read', methods=['GET'])
def read():
    query = "SELECT * FROM your_table"
    result = execute_query(query)
    data = [{'column1': row[0], 'column2': row[1]} for row in result]
    return jsonify(data)

@app.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    query = "UPDATE your_table SET column1 = %s, column2 = %s WHERE id = %s"
    args = (data['value1'], data['value2'], data['id'])
    execute_query(query, args)
    return jsonify({'message': 'Record updated successfully'})

@app.route('/delete', methods=['DELETE'])
def delete():
    data = request.get_json()
    query = "DELETE FROM your_table WHERE id = %s"
    args = (data['id'],)
    execute_query(query, args)
    return jsonify({'message': 'Record deleted successfully'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
