from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# Configurar la conexión a MongoDB
client = MongoClient(
    host=os.environ.get('MONGODB_HOSTNAME', 'localhost'),
    port=int(os.environ.get('MONGODB_PORT', 27017)),
    username=os.environ.get('MONGODB_USERNAME', 'mongoadmin'),
    password=os.environ.get('MONGODB_PASSWORD', 'secret'),
    authSource=os.environ.get('MONGODB_DBNAME', 'admin')
)
db = client[os.environ.get('MONGODB_DBNAME', 'mydatabase')]

# Ruta para insertar datos
@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        data = request.json  # Suponiendo que el JSON contiene los datos a insertar
        collection = db['mycollection']  # Nombre de la colección
        result = collection.insert_one(data)
        return jsonify({'message': 'Data inserted', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para consultar datos
@app.route('/find', methods=['GET'])
def find_data():
    try:
        data = list(db['mycollection'].find())  # Obtiene todos los documentos en la colección
        for item in data:
            item["_id"] = str(item["_id"])  # Convertir ObjectId a string para JSON
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
