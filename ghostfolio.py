import requests
class GhostfolioClient():
    def __init__(self, security_token, server):
        self.server = self.corregir_url_server(server)
        self.token = self.obtener_api_key(security_token, self.server)
        
    def corregir_url_server(self, server):
        if server.endswith('/'):
            return server[:-1]
        return server
        
        
    def obtener_api_key(self, security_token, server):
        url = f"{server}/api/v1/auth/anonymous"
        body = {
            "accessToken": security_token
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        return response.json()["authToken"]

    def insertar_operacion(self, simbolo: str, cantidad: int, precio: str, fecha: str, tipo: str, moneda: str, mercado: str = "ARG"):
        """Insertamos una actividad en el portfolio del usuario, sea venta u compra.

        Args:
            simbolo (string): Ticker symbol. Por ej MSFT, GGAL, etc. Si es mercado ARG le concatenaremos ".BA" 
            al final, ej MSFT se convierte en MSFT.BA (si la transacción fue en pesos argentinos) para indicar que
            es el CEDEAR
            cantidad (int): Cantidad de papeles comprados
            precio (string): Precio unitario de la operación
            fecha (string): Fecha de la operación en formato YYYY-MM-DD
            tipo (string): Tipo de operación, valores válidos BUY | DIVIDEND | FEE | INTEREST | ITEM | LIABILITY | SELL
            moneda (string): Moneda de la operación, por ejemplo "USD" o "ARS"
            mercado (string): Mercado Argentino ó Mercado USA (Internacional). Valores válidos: "ARG", "USA"
        """
        
        if mercado == "ARG":
            simbolo = f"{simbolo}.BA"
        
        url = f"{self.server}/api/v1/import"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        body = {
                "activities": [{
                    "currency": moneda,
                    "dataSource": "YAHOO",
                    "date": fecha,
                    "fee": 0,
                    "quantity": cantidad,
                    "symbol": simbolo,
                    "type": tipo,
                    "unitPrice": precio
                }],
        }
        response = requests.post(url, headers=headers, json=body)
        responseStatus = response.status_code
        if responseStatus == 201:
            print("Operación insert correcta")
            return True
        if responseStatus == 400:
            print("Error en la operación")
            print(response.json())
            return False
        return False
