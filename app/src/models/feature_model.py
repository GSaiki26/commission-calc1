# Libs
from os import environ


# Classes
class FeatureModel:
    api_url = environ.get('CONTAAZUL_API')

    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {
            'Authorization': f'bearer {self.token}'
        }
