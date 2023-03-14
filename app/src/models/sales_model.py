# Libs
from datetime import datetime as dt
from os import environ

import requests as r

from models.feature_model import FeatureModel


# Classes
class SalesModel(FeatureModel):
    def __init__(self, token: str) -> None:
        super().__init__(token)

    def get_period_sales(self) -> list[dict[str, any]]:
        '''
            A method to get all the sales.
        '''
        # Do the request.
        init_dt = dt.strptime(environ.get('DATA_INICIO'), '%d/%m/%Y')
        end_dt = dt.strptime(environ.get('DATA_FIM'), '%d/%m/%Y')
        try:
            print(f'Getting sales from {init_dt} - {end_dt}...')
            url = (
                f'{self.api_url}/v1/sales?size=999999999'
                f'&emission_start={init_dt.strftime("%Y-%m-%d")}'
                f'&emission_end={end_dt.strftime("%Y-%m-%d")}'
            )

            res = r.get(url, headers=self.headers)
            res.raise_for_status()
            print(res.status_code, res.url)
            return res.json()

        except r.HTTPError as err:
            print(err)
            return []
