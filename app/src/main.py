# Libs
from os import environ
from pathlib import Path

from flask import Flask

from controllers.index_controller import IndexController

# Data
app = Flask(
    __name__,
    static_folder=Path('public').absolute(),
    template_folder=Path('public/template').absolute()
)


# Routes
@app.route('/', methods=['GET'])
def get_index():
    return IndexController.get()


# Functions
def main():
    '''
        The main method.
    '''
    app.run('0.0.0.0', environ.get('PORT'))


# Code
if (__name__ == '__main__'):
    main()
