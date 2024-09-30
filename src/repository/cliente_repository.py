import os

from pymongo import MongoClient

from src.exceptions.cliente_nao_encontrado_exception import ClienteNaoEncontradoException


class ClienteRepository:

    def __init__(self):
        uri = os.getenv("mongodb_uri")
        database = os.getenv("database")

        self.client = MongoClient(uri)
        self.database = self.client[database]

    def buscar_cliente(self, query):
        collection = self.database["cliente"]
        results = list(collection.find(query))

        if not results:
            raise ClienteNaoEncontradoException(404, "Cliente nao encontrado.")

        return list(results)[0]

    def close(self):
        self.client.close()
