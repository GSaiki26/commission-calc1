# Libs
from datetime import datetime as dt
import io
from os import environ

from flask import request, redirect, Response
from pandas import DataFrame, ExcelWriter

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
            return Response({
                'status': 'error',
                'message': 'Couldn\'t retrieve the token.'
            }, 500)

        # Get sales
        sales_model = SalesModel(contaazul.token)
        prod_model = ProductModel(contaazul.token)

        sales = sales_model.get_period_sales()

        sales.sort(
            key=lambda sale: (sale['seller']['name'], sale['ca_id']),
            reverse=True if environ.get('REVERSE') == "True" else False
        )

        # Check the products from all sales.
        df = DfModel.create_template()
        for index, sale in enumerate(sales):
            sale_numb = f'({index+1}/{len(sales)})'
            print(f'Testing sale #{sale["number"]} {sale_numb}...')
            ReportController.add_sale_to_df(df, prod_model, sale, index)

        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')
        # df = df.sort_values(['Vendedor', 'Data'])

        # Send the df to the buffer.
        buffer = io.BytesIO()
        with ExcelWriter(buffer, 'openpyxl', mode='w') as writer:
            df.to_excel(writer, DfModel.get_sheet_name(), index=False)

        # Return to the client.
        return Response(
            buffer.getvalue(), mimetype='application/vnd.ms-excel',
            headers={
                'Content-Disposition': 'attachment; filename=result.xlsx',
                'Content-type': 'application/vnd.ms-excel'
            })

    @staticmethod
    def add_sale_to_df(
            df: DataFrame, prod_model: ProductModel,
            sale: dict[str, any], index: int) -> None:
        '''
            Add the sale to the dataframe.
        '''
        # Check if all produts are internal.
        products = prod_model.get_products_from_sale(sale['id'])
        if (ReportController.are_all_products_internal(products)):
            print('The sale is internal.\n\n')
            sale['sale_type'] = environ.get('VENDA_INTERNA')
        else:
            print('The sale is not internal.\n\n')
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
