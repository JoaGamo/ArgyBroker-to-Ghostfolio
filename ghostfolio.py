import requests
class GhostfolioClient():
    def __init__(self, security_token, server, account_id):
        self.server = self.corregir_url_server(server)
        self.token = self.obtener_api_key(security_token, self.server)
        self.operaciones_fallidas = []
        self.account_id = account_id
        
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

    def insertar_operacion(self, simbolo: str, cantidad: int, precio: float, fecha: str, tipo: str, moneda: str, mercado: str = "ARG"):
        """Insertamos una actividad en el portfolio del usuario, sea venta u compra.

        Args:
            simbolo (string): Ticker symbol. Por ej MSFT, GGAL, etc. Si es mercado ARG le concatenaremos ".BA" 
            al final, ej MSFT se convierte en MSFT.BA (si la transacción fue en pesos argentinos) para indicar que
            es el CEDEAR
            cantidad (int): Cantidad de papeles comprados
            precio (float): Precio unitario de la operación
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
                    "accountId": self.account_id,
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
        if response.status_code == 201:
                    print("Operación insert correcta")
                    return True
                
        # Store failed operation
        error_info = {
            "symbol": simbolo,
            "date": fecha,
            "error": response.json() if response.status_code == 400 else str(response.status_code),
            "request": body
        }
        self.operaciones_fallidas.append(error_info)
        print(f"Error en la operación: {simbolo}")
        
        if response.json().contains("is not valid for the specified data source (\"YAHOO\")"):
            # Inserción manual
            newBody = {
                "activities": [{
                    "accountId": self.account_id,
                    "currency": moneda,
                    "dataSource": "MANUAL",
                    "date": fecha,
                    "fee": 0,
                    "quantity": cantidad,
                    "symbol": simbolo,
                    "type": tipo,
                    "unitPrice": precio
                }],
        }
        
        
        return False
    
    def obtener_operaciones_fallidas(self) -> list:
        """Retorna lista de operaciones fallidas"""
        return self.operaciones_fallidas