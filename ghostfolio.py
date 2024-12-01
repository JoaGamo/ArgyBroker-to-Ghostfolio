import requests
class GhostfolioClient():
    def __init__(self, security_token, server):
        self.token = self.obtener_api_key(security_token, server)
        
    def obtener_api_key(self, security_token, server):
        if server.endswith('/'): # ayudamos al usuario si pone una "/" sin querer al final
            server = server[:-1]
        url = f"{server}/api/v1/auth/anonymous"
        body = {
            "accessToken": security_token
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        return response.json()["authToken"]

            
        
