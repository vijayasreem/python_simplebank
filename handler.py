from abc import ABC, abstractmethod


class Handler(ABC):
    @staticmethod
    @abstractmethod
    def Initialize():
        pass

    @staticmethod
    @abstractmethod
    def Deinitialize():
        pass
