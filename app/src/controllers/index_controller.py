# Libs
from flask import redirect

# from models.df_model import DfModel
from models.contaazul_model import ContaazulModel


# Classes
class IndexController:
    @staticmethod
    def get():
        '''
            GET /
        '''
        return redirect(ContaazulModel.get_auth_url())
