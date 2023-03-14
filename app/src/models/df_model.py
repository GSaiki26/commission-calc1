# Libs
from datetime import datetime as dt
from os import environ

import pandas as pd
from pandas import DataFrame


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
        total = f'= ROUND( E{row} - ( E{row} * F{row} ); 2 )'
        total_des = f'=ROUND( G{row} - ( G{row} * H{row} ); 2 )'
        total_com = f'=ROUND( I{row} * ( J{row} ); 2 )'

        return {
            'Data': entry.get('date'),
            'Vendedor': entry.get('seller'),
            'Venda': entry.get('sale'),
            'Cliente': entry.get('client'),
            'Valor': f'=ROUND({entry.get("value")}; 2)',
            '% Tipo de Venda': f'{entry.get("sale_type")}%',
            'Total': total,
            '% Desconto': '0%',
            'Total com desconto': total_des,
            '% Comissão': f'{environ.get("VENDA_COMISSAO", 0)}%',
            'Total com comissão': total_com
        }
