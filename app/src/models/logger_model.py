# Libs
from logging import Logger


# Classes
class LoggerModel:
    @staticmethod
    def create_logger(owner: str) -> Logger:
        '''
            A method to create a logger
        '''
        return Logger(owner, 0)
