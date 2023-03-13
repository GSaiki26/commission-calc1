# Libs
from logging import Logger

from flask import request, redirect, make_response

from models.contaazul_model import ContaazulModel


# Classes
class ReportController:
    @staticmethod
    def get(logger: Logger):
        '''
            GET /report?code
        '''
        # Get the auth code.
        auth = request.args.get('code')
        if not (auth):
            return redirect('/')

        # Check if the token was successfully got.
        contaazul = ContaazulModel(logger)
        if not (contaazul.get_token(auth)):
            logger.warn('Couldn\'t get the auth token...')
            return make_response({
                'status': 'error',
                'message': 'Couldn\'t retrieve the token.'
            }, 500)

        # Return the index.
        return make_response({
            'status': 'success',
            'message': "Success on getting the token."
        }, 200)
