from dotenv import load_dotenv
import os

from commonIOL import IOLClient
load_dotenv()

class main():

    def __init__(self, clienteaUsar = "IOL"):
        self.client = None
        # Permite ser extensible con otros brokers 
        if clienteaUsar == "IOL":
            self.client = IOLClient(
                usuario=os.getenv("IOL_USUARIO"),
                contrasena=os.getenv("IOL_CONTRASENA"),
                fecha_desde=os.getenv("IOL_FECHA_DESDE")
            )
        else:
            raise Exception("Broker no soportado")
            
        # Get operations
        operaciones = self.client.obtener_operaciones()

    