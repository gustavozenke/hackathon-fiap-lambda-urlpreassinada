import os

import requests

from src.exceptions.cliente_nao_encontrado_exception import ClienteNaoEncontradoException


class ClienteRepository:

    def __init__(self):
        self.url = os.getenv("cliente_url")
        self.endpoint = os.getenv("cliente_endpoint")

    def buscar_cliente(self, params):
        url = self.url + self.endpoint
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ClienteNaoEncontradoException(response.status_code, "Cliente nao encontrado.")
        else:
            raise Exception(response.status_code, "Falha ao realizar chamada de API.")
