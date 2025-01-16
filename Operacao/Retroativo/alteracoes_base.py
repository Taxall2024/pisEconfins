from abc import ABC, abstractmethod


class AlteracoesBase(ABC):

    def __init__(self,df):
        self.df = df

    @abstractmethod
    def dados_willian(self):       
        pass

    @abstractmethod
    def calculando_contadores_de_linhas(self):
        pass