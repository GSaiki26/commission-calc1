# Libs
from os import environ

import requests as r

from models.feature_model import FeatureModel


# Classes
class ProductModel(FeatureModel):
    api_url = environ.get('CONTAAZUL_API')

    def __init__(self, token: str) -> None:
        super().__init__(token)

    def get_products_from_sale(self, sale_id: str) -> list[dict[str, any]]:
        '''
            A method to get the list of products.
        '''
        try:
            # Get the products list.
            print('Getting the products list...')
            res = r.get(
                f'{self.api_url}/v1/sales/{sale_id}/items',
                headers=self.headers
            )
            res.raise_for_status()
            return res.json()

        except r.HTTPError as err:
            print(err)
