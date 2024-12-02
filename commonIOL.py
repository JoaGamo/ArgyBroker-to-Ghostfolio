from typing import Any, Dict, List
import requests
from commonBroker import CommonBroker

class IOLClient(CommonBroker):
    def __init__(self, **kwargs):
        self.usuario = kwargs.get('usuario')
        self.contrasena = kwargs.get('contrasena')
        self.fecha_desde = kwargs.get('fecha_desde')
        self.access_token = None
        self.refresh_token = None
        
        
    def _inicializar_tokens(self):
        url = "https://api.invertironline.com/token"
        payload = {
            "grant_type": "password",
            "username": self.usuario,
            "password": self.contrasena,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        tokens = response.json()
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]


    def _renovar_tokens(self):
        url = "https://api.invertironline.com/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        tokens = response.json()
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]


    def _asegurar_token_valido(self):
        if not self.access_token:
            self._inicializar_tokens()
        try:
            return self.access_token
        except requests.exceptions.HTTPError:
            self._renovar_tokens()
            return self.access_token


    def obtener_operaciones(self):
        token = self._asegurar_token_valido()
        url = "https://api.invertironline.com/api/v2/operaciones"
        payload = {
            "filtro.fechaDesde": self.fecha_desde,
            "filtro.estado": "terminadas"
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        aConvertir = response.json()
        # Los dividendos van aparte, pues la API de IOL retorna todo null si los buscamos por número
        # Gracias IOL <3
        numeros = []
        dividendos = []
        operaciones = []
        for operacion in aConvertir:
            if operacion["tipo"] == "Pago de Dividendos":
                dividendos.append(operacion)
            else:
                numeros.append(operacion["numero"])
        for numero in numeros:
            operaciones.append(self.obtener_operacion_completa(numero).json())
        
        # TODO: Implementar manejo de dividendos en IOL
        if dividendos:
            manejador_dividendos = self.IOL_manejador_dividendos(dividendos)
            #operaciones.extend(dividendos)
        
        return operaciones
        
        
    
    # En IOL debemos hacer una segunda API Call por cada operación para obtener la operación completa
    # Junto con su tipo de moneda y todo lo demás.
    def obtener_operacion_completa(self, numero):
        token = self._asegurar_token_valido()
        url = f"https://api.invertironline.com/api/v2/operaciones/{numero}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response

    def obtener_simbolo(self, operacion: Dict[str, Any]) -> str:
        return operacion["simbolo"].split()[0]

    def obtener_cantidad(self, operacion: Dict[str, Any]) -> int:
        if operacion.get("operaciones"):
            return operacion["operaciones"][0]["cantidad"]
        return operacion.get("cantidad", 0)

    def obtener_precio(self, operacion: Dict[str, Any]) -> float:
        if operacion.get("operaciones"):
            
            return float(operacion["operaciones"][0]["precio"])
        return float(operacion.get("precio", 0))


    def obtener_fecha(self, operacion: Dict[str, Any]) -> str:
        """Obtiene la fecha y la retorna como YYYY-MM-DD"""
        fecha = operacion.get("fechaOperado", "")
        return fecha


    def obtener_tipo(self, operacion: Dict[str, Any]) -> str:
        tipo_map = {

            "compra": "BUY",
            "suscripcionfci": "BUY",

            "venta": "SELL", 
            "rescatefci": "SELL",

            "pago_dividendos": "DIVIDEND"
        }
        return tipo_map.get(operacion["tipo"].lower(), "UNKNOWN")


    def obtener_moneda(self, operacion: Dict[str, Any]) -> str:
        return "ARS" if operacion["moneda"].lower() == "peso_argentino" else "USD"
        

    def obtener_mercado(self, operacion: Dict[str, Any]) -> str:
        return "ARG" if operacion["mercado"].lower() == "bcba" else "USA"
    
    def obtener_comision(self, operacion: Dict[str, Any]) -> float:
        moneda = self.obtener_moneda(operacion)
        if moneda == "USD":
            return operacion['arancelesUSD']
        else:
            return operacion['arancelesARS']

        
    class IOL_manejador_dividendos(CommonBroker):
        def __init__(self, dividendos):
            self.dividendos = dividendos

        def _inicializar_tokens(self):
            raise NotImplementedError


        def _renovar_tokens(self):
            raise NotImplementedError


        def _asegurar_token_valido(self):
            raise NotImplementedError

        def obtener_simbolo(self, operacion: Dict[str, Any]) -> str:
            return operacion["simbolo"].split()[0]

        def obtener_cantidad(self, operacion: Dict[str, Any]) -> int:
            return operacion.get("cantidad", 0)

        def obtener_precio(self, operacion: Dict[str, Any]) -> float:
            return float(operacion.get("precio", 0))
        
        def obtener_fecha(self, operacion: Dict[str, Any]) -> str:
            """Obtiene la fecha y la retorna como YYYY-MM-DD"""
            fecha = operacion.get("fechaOperada", "")
            return fecha
        
        def obtener_tipo(self, operacion: Dict[str, Any]) -> str:
            return "DIVIDEND"
        
        def obtener_moneda(self, operacion: Dict[str, Any]) -> str:
            return "ARS" if operacion["moneda"].lower() == "peso_argentino" else "USD"
        
        def obtener_mercado(self, operacion: Dict[str, Any]) -> str:
            return "ARG" if operacion["mercado"].lower() == "bcba" else "USA"
        
        def obtener_comision(self, operacion: Dict[str, Any]) -> float:
            return 0
        
        def obtener_operaciones(self) -> List[Dict[str, Any]]:
            raise NotImplementedError

        

    