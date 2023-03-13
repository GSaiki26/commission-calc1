# Libs
# from datetime import datetime
# from os import environ

from flask import render_template

# from models.df_model import DfModel


# Classes
class IndexController:
    @staticmethod
    def get():
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
        return render_template('index.html')
