from alteracoes_base import AlteracoesBase
import pandas as pd


class ImplementandoAlteracoesBase(AlteracoesBase):
    def dados_willian(self):
        
        self.df.loc[self.df[0] == '0000', 2] = 1
        self.df.loc[self.df[0] == '0100', 1] = 'WILLIAM SILVA DE ALMEIDA'
        self.df.loc[self.df[0] == '0100', 2] = 89709861115
        self.df.loc[self.df[0] == '0100', 3] = '19342DF'
        self.df.loc[self.df[0] == '0100', 6] = 'Q CRS 502 BLOCO B'
        self.df.loc[self.df[0] == '0100', 5] = 70330520
        self.df.loc[self.df[0] == '0100', 9] = 'ASA SUL'
        self.df.loc[self.df[0] == '0100', 10] = 6181272930
        self.df.loc[self.df[0] == '0100', 12] = 'NEGOCIOS@TAXALL.COM.BR'        
        
        self.df.loc[self.df[0] == '0110', 1] = '2'

        self.df = self.df.loc[self.df[0] != '0111']
        self.df = self.df.loc[~((self.df[0] == '9900')&(self.df[1] == '0111'))]

    def calculando_contadores_de_linhas(self):

        contagem_99_00 = self.df.loc[self.df[0] == '9900', 0].value_counts()

        contagem_A100 = self.df.loc[self.df[0] == 'A100',0].value_counts()
        contagem_A170 = self.df.loc[self.df[0] == 'A170',0].value_counts()
        
        self.df.loc[((self.df[0] == '9900') & (self.df[1] == 'A100')),2] = contagem_A100.values[0]
        self.df.loc[((self.df[0] == '9900') & (self.df[1] == 'A170')),2] = contagem_A170.values[0]

        start_index = self.df.index[self.df[0].str.startswith('9001')].min()
        end_index = self.df.index[self.df[0].str.startswith('9999')].max()


        subset_df = self.df.loc[start_index:end_index]


        contagem_linhas_99_90 = len(subset_df) -1 

        contagem_total_linhas = len(self.df) - 1
        
        self.df.loc[self.df[0] == '9999',1 ] = contagem_total_linhas

        self.df.loc[(self.df[0] == '9900') & (self.df[1] == '9900'),2] = contagem_99_00.values[0]

        self.df.loc[(self.df[0] == '9990' ),1] = contagem_linhas_99_90

        contador_M = self.df[self.df[0].str.startswith('M')].shape[0]
        contador_F = self.df[self.df[0].str.startswith('F')].shape[0]

        print('---------- LOG Contador de linhas para Rubrica M => ',contador_M)
        print('---------- LOG Contador de linhas para Rubrica M => ',contador_F)
        
        self.df.loc[self.df[0] == 'M990',1] = contador_M
        self.df.loc[self.df[0] == 'F990',1] = contador_F
       
        self.df = pd.concat([self.df, pd.DataFrame([[''] * len(self.df.columns)], columns=self.df.columns)], ignore_index=True)