# Libs
from os import environ
from base64 import b64encode

import requests as r


# Classes
class ContaazulModel:
    redirect_uri = environ.get('REDIRECT_URI')
    client_id = environ.get('CLIENT_ID')

    def __init__(self) -> None:
        self.token: str = ''
        self.__client_secret = environ.get('CLIENT_SECRET')

    def get_token(self, auth_code: str) -> bool:
        '''
            A method to get the access token from ContaAzul.
            Return a boolean specifing if was possible to
            retrieve the token.
        '''
        # Create the app basic base64.
        to_encode = f'{self.client_id}:{self.__client_secret}'.encode('ascii')
        base64 = b64encode(to_encode).decode('ascii')
        headers = {
            'Authorization': f'Basic {base64}'
        }

        url = (
            f'{environ.get("CONTAAZUL_API")}/oauth2/token?'
            f'grant_type=authorization_code'
            f'&redirect_uri={self.redirect_uri}'
            f'&code={auth_code}'
        )

        # Try to get the token.
        try:
            res = r.post(url, headers=headers)
            res.raise_for_status()

            self.token: str = res.json().get('access_token')
            return True
        except r.HTTPError as err:
            self.logger.error(f'An error was raised. Error: {err}')
            return False

    @staticmethod
    def get_auth_url() -> str:
        '''
            A method to return the authorization step url.
        '''
        return (
            f'{environ.get("CONTAAZUL_API")}'
            f'/auth/authorize?redirect_uri={ContaazulModel.redirect_uri}'
            f'&client_id={ContaazulModel.client_id}&scope=sales&state=142'
        )
