from dotenv import load_dotenv
load_dotenv()

import os
import requests

class JQuantsClient:
    def __init__(self, base_url=None, mail_address=None, password=None):
        self.base_url = base_url or os.getenv('JQUANTS_URL', '')
        self.mail_address = mail_address or os.getenv('JQUANTS_MAIL', '')
        self.password = password or os.getenv('JQUANTS_PASS', '')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
        # get refreshToken
        refresh_token_response = self.session.post(
            f"{self.base_url}/token/auth_user",
            json={
                'mailaddress': self.mail_address,
                'password': self.password
            }
        )
        refresh_token = refresh_token_response.json().get('refreshToken')
        
        
        # get idToken
        id_token_response = self.session.post(
            f"{self.base_url}/token/auth_refresh",
            params={'refreshtoken': refresh_token}
        )
        id_token = id_token_response.json().get('idToken')
        
        # Set authorization header
        self.session.headers.update({
            'Authorization': f'Bearer {id_token}'
        })
        self.id_token = id_token
        
    def getCompanies(self):
        res = self.session.get(f'{self.base_url}/listed/info')
        data: list[dict[str, str]] = res.json().get('info')

        return data
