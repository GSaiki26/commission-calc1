# Libs
from datetime import datetime as dt
from os import environ

from flask import request, redirect, make_response

from models.contaazul_model import ContaazulModel
from models.product_model import ProductModel
from models.sales_model import SalesModel
from models.df_model import DfModel


# Classes
class ReportController:
    @staticmethod
    def get():
        '''
            GET /report?code
        '''
        # Get the auth code.
        auth = request.args.get('code')
        if not (auth):
            return redirect('/')

        # Check if the token was successfully got.
        contaazul = ContaazulModel()
        if not (contaazul.get_token(auth)):
            print('Couldn\'t get the auth token...')
            return make_response({
                'status': 'error',
                'message': 'Couldn\'t retrieve the token.'
            }, 500)

        # Get sales
        sales_model = SalesModel(contaazul.token)
        sales = sales_model.get_period_sales()
        product_model = ProductModel(contaazul.token)

        # Check the products from all sales.
        df = DfModel.create_template()
        print(len(sales))
        for index, sale in enumerate(sales):
            print(f'Testing sale #{sale["number"]}...')

            # Check if all produts are internal.
            products = product_model.get_products_from_sale(sale['id'])
            if (ReportController.are_all_products_internal(products)):
                print('The sale is internal.')
                sale['sale_type'] = environ.get('VENDA_INTERNA')
            else:
                print('The sale is not internal.')
                sale['sale_type'] = environ.get('VENDA_PRATELEIRA')

            # Add the sale to the excel file.
            date = dt.fromisoformat(sale["emission"][:-1] + '+00:00')
            df.loc[len(df)] = DfModel.format_entry({
                'date': date,
                'seller': sale['seller']['name'],
                'sale': sale['number'],
                'client': sale['customer']['name'],
                'value': sale['total'],
                'sale_type': sale['sale_type'].replace('.', ','),
            }, index + 1)

        print(df)

        DfModel.write_to_file(df)

        # Return the index.
        return make_response({
            'status': 'success',
            'message': "Success on getting the token."
        }, 200)

    @staticmethod
    def are_all_products_internal(products: list[dict[str, any]]) -> bool:
        '''
            A method to check if the provided products are internal.
        '''
        for product in products:
            name: str = product['item']['name']
            print(f'product name: {name}')
            if (name.lower().find('interno') == -1):
                return False

        return True
