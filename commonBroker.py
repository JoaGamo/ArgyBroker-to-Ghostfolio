from abc import ABC, abstractmethod
from typing import Dict, List, Any

class CommonBroker(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass
    
    @abstractmethod
    def obtener_operaciones(self) -> List[Dict[str, Any]]:
        """Obtiene las operaciones del broker"""
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