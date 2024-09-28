from repository.cliente_repository import ClienteRepository


class ClienteService:

    def __init__(self):
        self.cliente_repository = ClienteRepository()

    def buscar_cliente(self, cpf_cliente):

        event = {
            "cpf": cpf_cliente
        }

        return self.cliente_repository.buscar_cliente(event)
