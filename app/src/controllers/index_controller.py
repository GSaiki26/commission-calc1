# Libs
# from datetime import datetime
# from os import environ
from logging import Logger

from flask import redirect

# from models.df_model import DfModel
from models.contaazul_model import ContaazulModel


# Classes
class IndexController:
    @staticmethod
    def get(logger: Logger):
        '''
            GET /
        '''
        # df = DfModel.create_template()
        # df.loc[len(df)] = DfModel.format_entry({
        #     'date': datetime.now(),
        #     'sale': 1,
        #     'client': 'Feliz',
        #     'value': '1000',
        #     'sale_type': environ.get('VENDA_PRATELEIRA').replace('.', ','),
        # }, 1)
        # DfModel.write_to_file(df)
        return redirect(ContaazulModel.get_auth_url())
