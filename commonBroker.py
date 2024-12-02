from abc import ABC, abstractmethod
from typing import Dict, List, Any

class CommonBroker(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass
    
    @abstractmethod
    def obtener_operaciones(self) -> List[Dict[str, Any]]:
        """Obtiene las operaciones (terminadas) del broker"""
        pass
    
    @abstractmethod
    def _inicializar_tokens(self) -> None:
        """Inicializa los tokens de autenticación"""
        pass
    
    @abstractmethod
    def _renovar_tokens(self) -> None:
        """Renueva los tokens de autenticación"""
        pass
    
    @abstractmethod
    def _asegurar_token_valido(self) -> str:
        """Asegura que el token sea válido"""
        pass
    
    
    @abstractmethod
    def obtener_simbolo(self, operacion: Dict[str, Any]) -> str:
        """Obtiene el símbolo/ticker de la operación"""
        pass

    @abstractmethod
    def obtener_cantidad(self, operacion: Dict[str, Any]) -> int:
        """Obtiene la cantidad de papeles de la operación"""
        pass

    @abstractmethod
    def obtener_precio(self, operacion: Dict[str, Any]) -> float:
        """Obtiene el precio unitario de la operación"""
        pass

    @abstractmethod
    def obtener_fecha(self, operacion: Dict[str, Any]) -> str:
        """Obtiene la fecha de la operación en formato YYYY-MM-DD"""
        pass

    @abstractmethod
    def obtener_tipo(self, operacion: Dict[str, Any]) -> str:
        """Obtiene el tipo de operación (BUY|SELL|DIVIDEND|etc)"""
        pass

    @abstractmethod
    def obtener_moneda(self, operacion: Dict[str, Any]) -> str:
        """Obtiene la moneda de la operación (ARS|USD)"""
        pass

    @abstractmethod
    def obtener_mercado(self, operacion: Dict[str, Any]) -> str:
        """Obtiene el mercado de la operación (ARG|USA)"""
        pass
    
    @abstractmethod
    def obtener_comision(self, operacion: Dict[str, Any]) -> float:
        """Obtiene la comisión (impuesto del broker) de la operación"""
        pass
    