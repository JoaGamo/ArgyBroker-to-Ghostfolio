from typing import Any, Dict
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
        return response.json()

    def obtener_simbolo(self, operacion: Dict[str, Any]) -> str:
        return operacion["simbolo"].split()[0]

    def obtener_cantidad(self, operacion: Dict[str, Any]) -> int:
        cantidad = operacion.get("cantidadOperada")
        if cantidad is None:
            return 1  # Dividendos dan cantidad null
        return int(cantidad)

    def obtener_precio(self, operacion: Dict[str, Any]) -> float:
        precio = operacion.get("precioOperado")
        if precio is None:
            return operacion.get("montoOperado") # type: ignore # Dividendos dan precio null
        return float(precio)

    def obtener_fecha(self, operacion: Dict[str, Any]) -> str:
        return operacion.get("fechaOperada") # type: ignore

    def obtener_tipo(self, operacion: Dict[str, Any]) -> str:
        tipo_map = {
            "Compra": "BUY",
            "Venta": "SELL",
            "Pago de Dividendos": "DIVIDEND"
        }
        return tipo_map.get(operacion["tipo"], "UNKNOWN")

    def obtener_moneda(self, operacion: Dict[str, Any]) -> str:
        simbolo = operacion.get("simbolo", "")
        return "USD" if simbolo.endswith("US$") else "ARS"
        

    def obtener_mercado(self, operacion: Dict[str, Any]) -> str:
        if operacion["mercado"] == "BCBA":
            return "ARG"
        return "USA"

    
    