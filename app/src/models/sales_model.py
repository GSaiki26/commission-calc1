# Libs
from datetime import datetime as dt
from os import environ

import requests as r

from models.df_model import DfModel
from models.feature_model import FeatureModel


# Classes
class SalesModel(FeatureModel):
    def __init__(self, token: str) -> None:
        super().__init__(token)

    def get_period_sales(self) -> dict[str, dict[str, list[dict[str, any]]]]:
        '''
            A method to get all the sales.
        '''
        # Do the request.
        init_dt = dt.strptime(environ.get('DATA_INICIO'), '%d/%m/%Y')
        end_dt = dt.strptime(environ.get('DATA_FIM'), '%d/%m/%Y')
        try:
            print(f'Getting sales from {init_dt} - {end_dt}...')
            url = (
                f'{self.api_url}/v1/sales?size={environ.get("SALES_LENGTH")}'
                f'&emission_start={init_dt.strftime("%Y-%m-%d")}'
                f'&emission_end={end_dt.strftime("%Y-%m-%d")}'
            )

            res = r.get(url, headers=self.headers)
            res.raise_for_status()
            sales = res.json()
            sales = SalesModel.sort_sales(sales)
            sales = SalesModel.split_sales_by_seller(sales)
            return sales

        except r.HTTPError as err:
            print(err)
            return []

    @staticmethod
    def sort_sales(sales: list[dict[str, any]]) -> list[dict[str, any]]:
        '''
            A method to sort the sales.
        '''
        sales.sort(
            key=lambda sale: (
                dt.fromisoformat(
                    sale["emission"][:-1] + '+00:00').strftime('%d/%m/%Y'),
                sale['ca_id']
            ), reverse=False if environ.get('REVERSE') == "True" else False
        )

        return sales

    @staticmethod
    def split_sales_by_seller(
            sales: list[dict[str, any]]
            ) -> dict[str, dict[str, list[dict[str, any]]]]:
        '''
            A method to split the sales by seller.
        '''
        sales_by_seller: dict[str, dict[str, list[dict[str, any]]]] = {}

        # Loop for the sales.
        for sale in sales:
            # Get the sale's owner.
            seller: str = sale['seller']['name']

            # Create the saller if not included in the sales_by_seller.
            if not (seller in sales_by_seller):
                sales_by_seller[seller] = {
                    'sales': [],
                    'df': DfModel.create_template()
                }

            sales_by_seller[seller]['sales'].append(sale)

        return sales_by_seller
