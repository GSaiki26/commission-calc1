# Libs
from datetime import datetime as dt
from os import environ

import pandas as pd
from pandas import DataFrame

from models.product_model import ProductModel


# Classes
class DfModel:
    @staticmethod
    def create_template() -> DataFrame:
        '''
            A method to create the basic template from the xlsx.
        '''
        # Create the basic dataframe template.
        columns = {
            'Data': pd.Series(dtype=str),
            'Venda': pd.Series(dtype=int),
            'Cliente': pd.Series(dtype=str),
            'Vendedor': pd.Series(dtype=str),
            'Valor': pd.Series(dtype=float),
            '% Tipo de Venda': pd.Series(dtype=float),
            'Total': pd.Series(dtype=float),
            '% Desconto': pd.Series(dtype=float),
            'Total com desconto': pd.Series(dtype=float),
            '% Comissão': pd.Series(dtype=float),
            'Total com comissão': pd.Series(dtype=float),
        }

        df = DataFrame(columns)
        return df

    @staticmethod
    def get_sheet_name() -> str:
        '''
            A method to get the sheet name.
        '''
        init_dt = dt.strptime(environ.get('DATA_INICIO'), '%d/%m/%Y')
        end_dt = dt.strptime(environ.get('DATA_FIM'), '%d/%m/%Y')
        init_date = init_dt.strftime('%d-%m-%Y')
        end_date = end_dt.strftime('%d-%m-%Y')
        return f'{init_date} --- {end_date}'

    @staticmethod
    def format_entry(entry: dict[str, any], row: int) -> dict[str, any]:
        '''
            A method to format a sale into a row.
        '''
        # Format.
        row += 1
        total = f'= E{row} / ( F{row} + 1)'
        total_des = f'= G{row} - ( G{row} * H{row})'
        total_com = f'= I{row} * J{row}'

        return {
            'Data': entry.get('date'),
            'Vendedor': entry.get('seller'),
            'Venda': entry.get('sale'),
            'Cliente': entry.get('client'),
            'Valor': f'={entry.get("value")}',
            '% Tipo de Venda': f'{entry.get("sale_type")}%',
            'Total': total,
            '% Desconto': '0%',
            'Total com desconto': total_des,
            '% Comissão': f'{environ.get("VENDA_COMISSAO", 0)}%',
            'Total com comissão': total_com
        }

    @staticmethod
    def add_sale_to_df(
            df: DataFrame, prod_model: ProductModel,
            sale: dict[str, any], index: int) -> None:
        '''
            Add the sale to the dataframe.
        '''
        # Get the products from the sale.
        products = prod_model.get_products_from_sale(sale['id'])

        # Check if all produts are internal.
        if (ProductModel.are_all_products_internal(products)):
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
