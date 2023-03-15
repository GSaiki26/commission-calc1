# Libs
import io

from flask import request, redirect, Response
from pandas import ExcelWriter

from models.contaazul_model import ContaazulModel
from models.df_model import DfModel
from models.product_model import ProductModel
from models.sales_model import SalesModel


# Classes
class ReportController:
    @staticmethod
    def get():
        '''
            GET /report
            QUERY code
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
        sellers = sales_model.get_period_sales()

        # Loop through the sellers.
        for seller in sellers:
            print(f'Calculating the seller: {seller}')

            # Get the sales from the seller.
            for index, sale in enumerate(sellers[seller]['sales']):
                sale_numb = f'{index+1}/{len(sellers[seller]["sales"])}'
                print(f'Testing sale #{sale["number"]} ({sale_numb})...')

                # Add the sale to the dataframe.
                DfModel.add_sale_to_df(
                    sellers[seller]['df'], prod_model, sale, index)

            # Format the date to the format %d/%m/%Y.
            sellers[seller]['df']['Data'] = (
                sellers[seller]['df']['Data'].dt.strftime('%d/%m/%Y')
            )

            # Add the commission totals on the end of the df.
            sales_len = len(sellers[seller]['df'])
            sellers[seller]['df'].loc[sales_len] = {
                'Total com comissão': f'=SOMA(K2:K{sales_len + 1  })'
            }

        # Send the df to the buffer.
        buffer = io.BytesIO()
        with ExcelWriter(buffer, 'openpyxl', mode='w') as writer:
            for seller in sellers.keys():
                sellers[seller]['df'].to_excel(
                    writer, sheet_name=seller, index=False)

        # Return to the client.
        return Response(
            buffer.getvalue(), mimetype='application/vnd.ms-excel',
            headers={
                'Content-Disposition': 'attachment; filename=result.xlsx',
                'Content-type': 'application/vnd.ms-excel'
            })
