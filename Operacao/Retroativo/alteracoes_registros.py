import pandas as pd
import numpy as np
from logger import Logger

log = Logger().init_log()

class AlteracoesRegistros():
    
    def __init__(self,df):
        self.df = df
        
            

    def recaculcalndo_aliquota_A170(self):
        self.df.loc[self.df[0] == 'A170', 10] = '0,65'
        self.df.loc[self.df[0] == 'A170', 14] = 3
        self.calculos_aliquota(self.df,0.0065, 9, 11)
        self.calculos_aliquota(self.df,0.03, 13, 15)
        
        self.data = str(self.df.iloc[0, 5])
        self.df_apurado = self.df.copy()

        # Retorna None para evitar renderização automática
        return self.df

    def calculos_aliquota(self,df:pd.DataFrame,aliquota:float, base_calculo: int, atribuir_resultado: int):
        mask_a170 = df[0] == 'A170'
        
        numeric_values = pd.to_numeric(df.loc[mask_a170, base_calculo].str.replace(',', '.'), errors='coerce')

        new_values = numeric_values * aliquota
        new_values = new_values.apply(lambda x: f"{x:.2f}".replace('.', ','))

        df.loc[mask_a170, atribuir_resultado] = new_values   

        return df
    

    def remove_A100_Col2_1(self):
        print('---------------> Data frame Metodo Remove_A100_Col2_1 :    ',self.df)
        self.df = self.df.loc[~((self.df[0] == 'A100') & (self.df[2] == '1'))]


    def remove_F100_Col1_0(self):    
        self.df = self.df.loc[~((self.df[0] == 'F100') & (self.df[1] == '0'))]
    
    def zerar_C100_Col1_0(self):        
        self.df.loc[((self.df[0] == 'C100')&(self.df[1] == '0')),25] = '0'
        self.df.loc[((self.df[0] == 'C100')&(self.df[1] == '0')),26] = '0'

    def zerar_C170_Col1_0(self):
        for i in range(100):            
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),35] = '0'
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),33] = '0'
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),29] = '0'
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),25] = '0'
    
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),31] = '0'

                
                
            self.df.loc[(self.df[0]=='C170') & (self.df[1]==f'{i}') & (self.df[24].str.contains('5')),24] = '70'

                    
            self.df.loc[(self.df[0]=='C170') & (self.df[1]==f'{i}') & (self.df[30].str.contains('5')),30] = '70'
    
    def remove_C396(self):       
        self.df = self.df.loc[~(self.df[0] == 'C396')]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'C396'))]

    def remove_C190(self):
            
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'C190'))]
        self.df = self.df.loc[~(self.df[0] == 'C190')]


    def remove_C395(self):
            
        self.df = self.df.loc[~(self.df[0] == 'C395')]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'C395'))]
        
    def remove_D100(self):
            
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'D100'))]
        self.df = self.df.loc[~(self.df[0] == 'D100')]

    
    def remove_D500(self):

        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'D500'))]
        self.df = self.df.loc[~(self.df[0] == 'D500')]

    def remove_F100(self):
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F100'))]
        self.df = self.df.loc[~(self.df[0] == 'F100')]
    
    def remove_F120(self):

        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F120'))]
        self.df = self.df.loc[~(self.df[0] == 'F120')]
        
    def remove_F130(self):

        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F130'))]
        self.df = self.df.loc[~(self.df[0] == 'F130')]
        
    def remove_F150(self):
                        
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F150'))]
        self.df = self.df.loc[~(self.df[0] == 'F150')]


    def remove_M100(self):

        self.df = self.df.loc[~((self.df[0]== 'M100'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M100'))]

    def rmeove_M105(self):

        self.df = self.df.loc[~((self.df[0]== 'M105'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M105'))]

        
    def remove_M500(self):
            
        self.df = self.df.loc[~((self.df[0]== 'M500'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M500'))]

    def remove_M505(self):

        self.df = self.df.loc[~((self.df[0]== 'M505'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M505'))]


    def alterandoa_M205_Col1_12(self):
        self.df.loc[self.df[0] == 'M205', 1] = '12'


    def alterando_M100_col2_810902(self):
        self.df.loc[self.df[0] == 'M100', 2] = '810902'
    
    def alterando_M210_Col7(self):

        self.df.loc[self.df[0] == 'M210', 7] = '0,65' 

    
    def alterando_M605_Cols_1_2(self): 
        self.df.loc[self.df[0] == 'M605', 1] = '12'
        self.df.loc[self.df[0] == 'M605', 2] = '217201'
        
    def alterandoM610_Col_7(self):
            self.df.loc[self.df[0] == 'M610', 7] = '3'

    
    def moodificacoes_grupo_M100(self):

        self.df.loc[self.df[0] == 'M100', 3] = 0
        self.df.loc[self.df[0] == 'M100', 7] = 0
        self.df.loc[self.df[0] == 'M100', 11] = 0
        self.df.loc[self.df[0] == 'M100', 13] = 0
        

    def correcao_valores_Bloco_A100_e_A170(self):
        
        for i in range(len(self.df) - 1):
            if self.df.iloc[i, 0] == 'A100' and self.df.iloc[i + 1, 0] == 'A170':
                self.df.iloc[i, 15] = self.df.iloc[i + 1, 11]
            if self.df.iloc[i, 0] == 'A100' and self.df.iloc[i + 1, 0] == 'A170':
                self.df.iloc[i, 17] = self.df.iloc[i + 1, 15]

        self.df[0] = self.df[0].astype(str).str.strip()
        self.df[2] = self.df[2].astype(str).str.strip()

        self.df.loc[((self.df[0] == 'A100') & (self.df[2] == '1')), 15] = '0'
        self.df.loc[((self.df[0] == 'A100') & (self.df[2] == '1')), 17] = '0'
        
        for i in range(len(self.df) - 1):
            if ((self.df.iloc[i, 0] == 'A100') & (self.df.iloc[i, 2] == '1')) and self.df.iloc[i + 1, 0] == 'A170':
                self.df.iloc[i + 1, 8] = '70'
                self.df.iloc[i + 1, 12] = '70'
                
                
                self.df.iloc[i + 1, 11] = '0'
                self.df.iloc[i + 1, 15] = '0'


    def alteracao_F600_Col_6(self):
        self.df.loc[self.df[0] == 'F600', 6] = '1'
    
    
    def remove_C500(self):

        self.df = self.df.loc[~(self.df[0] == 'C500')]
        self.df = self.df.loc[~((self.df[1] == 'C500')&(self.df[0] == '9900'))]

    def remove_C50(self):

        self.df = self.df.loc[~(self.df[0].str.contains('C50'))]
        self.df = self.df.loc[~((self.df[1].str.contains('C50'))&(self.df[0] == '9900'))]
        
    def recalculando_aliquota_M200_e_M600(self):

        def valor_m200():
            a100 = self.df.loc[self.df[0]=='A100']
            
            a100[15] = a100[15].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = round(a100[15].sum(),2)
            soma_a100 = str(soma_a100).replace('.',',')

            print('>>>>>Sooma',soma_a100)

            return soma_a100

        def valor_m600():
            a100 = self.df.loc[self.df[0]=='A100']
            
            a100[17] = a100[17].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = round(a100[17].sum(),2)
            soma_a100 = str(soma_a100).replace('.',',')
            
            print('>>>>>Sooma',soma_a100)

            return soma_a100    

        m200 = valor_m200()
        m600 = valor_m600()
        self.df.loc[self.df[0] == 'M200',12] = m200
        self.df.loc[self.df[0] == 'M200',8] = m200
        self.df.loc[self.df[0] == 'M200',1] ='0'
        self.df.loc[self.df[0] == 'M200',2] ='0' 
        self.df.loc[self.df[0] == 'M200',3] ='0' 
        self.df.loc[self.df[0] == 'M200',4] = '0'        
        self.df.loc[self.df[0] == 'M200',5] ='0' 
        self.df.loc[self.df[0] == 'M200',9] ='0' 
                
        self.df.loc[self.df[0] == 'M600',12] = m600
        self.df.loc[self.df[0] == 'M600',8] = m600
        self.df.loc[self.df[0] == 'M600',1] = '0'
        self.df.loc[self.df[0] == 'M600',2] = '0'
        self.df.loc[self.df[0] == 'M600',3] = '0'
        self.df.loc[self.df[0] == 'M600',4] = '0'
        self.df.loc[self.df[0] == 'M600',5] = '0'
        self.df.loc[self.df[0] == 'M600',9] = '0'
        
        

    def recalculando_aliquota_M210_e_M610(self):

        def recalculando_m210():
            m210_valor_total = self.df.loc[self.df[0] == 'M210', 6].str.replace(',', '.').replace('', '0').astype(float)
            m210_aliquota = 0.0065

            resultado = round(m210_valor_total * m210_aliquota, 2).iloc[0]  # Acesso ao primeiro elemento
            resultado = str(resultado).replace('.', ',')
            print('------- Valor base m210', m210_valor_total)
            print('--------Aliquota m210', m210_aliquota)
            print('----------- Resultado Recalculo M210 :: >>', resultado)
            return resultado

        def recalculando_m610():
            m610_valor_total = self.df.loc[self.df[0] == 'M610', 6].str.replace(',', '.').replace('', '0').astype(float)
            m610_aliquota = 0.03

            resultado = round(m610_valor_total * m610_aliquota, 2).iloc[0]  # Acesso ao primeiro elemento
            resultado = str(resultado).replace('.', ',')
            print('------- Valor base m610', m610_valor_total)
            print('--------Aliquota m610', m610_aliquota)
            print('----------- Resultado Recalculo 610 :: >>', resultado)
            return resultado

        m210 = recalculando_m210()   
        m610 = recalculando_m610()

        self.df.loc[self.df[0] == 'M210',10] = m210
        self.df.iloc[self.df[0] == 'M610',10] = m610

        self.df.loc[self.df[0] == 'M210',15] = m210
        self.df.iloc[self.df[0] == 'M610',15] = m610

        self.df.loc[self.df[0] == 'M205',2] = '810902'
        self.df.loc[self.df[0] == 'M205',3] = m210
                
        self.df.loc[self.df[0] == 'M605',3] = m610

        self.df.iloc[self.df[0] == 'M610',10] = m610



        self.df.loc[self.df[0] == 'M210',1] = '51'
        self.df.loc[self.df[0] == 'M610',1] = '51'


    def zerando_valores_M500(self):
        
        self.df.loc[self.df[0] == 'M500',3] = '0' 
        self.df.loc[self.df[0] == 'M500',7] = '0' 
        self.df.loc[self.df[0] == 'M500',8] = '0' 
        self.df.loc[self.df[0] == 'M500',9] = '0' 
        self.df.loc[self.df[0] == 'M500',10] = '0' 
        self.df.loc[self.df[0] == 'M500',11] = '0' 
        self.df.loc[self.df[0] == 'M500',12] = '0' 
        self.df.loc[self.df[0] == 'M500',13] = '0' 
        self.df.loc[self.df[0] == 'M500',14] = '0' 

    def zerando_valores_M600(self):

        self.df.loc[self.df[0] == 'M100',3] = '0' 
        self.df.loc[self.df[0] == 'M100',7] = '0' 
        self.df.loc[self.df[0] == 'M100',3] = '0' 
        self.df.loc[self.df[0] == 'M100',8] = '0' 
        self.df.loc[self.df[0] == 'M100',9] = '0' 
        self.df.loc[self.df[0] == 'M100',10] = '0' 
        self.df.loc[self.df[0] == 'M100',11] = '0' 
        self.df.loc[self.df[0] == 'M100',12] = '0' 
        self.df.loc[self.df[0] == 'M100',13] = '0' 
        self.df.loc[self.df[0] == 'M100',14] = '0' 


    def recaculcalndo_aliquota_C170_Col2_0(self):

        self.df = self.calculos_aliquota_C170(self.df,0.0065, 15, 25)
        self.df = self.calculos_aliquota_C170(self.df,0.03, 15, 26)
        
        print('Função Recalculo C170')


    def calculos_aliquota_C170(self,df:pd.DataFrame,aliquota:float, base_calculo: int, atribuir_resultado: int):
        mask_a170 = ((df[0] == 'C100')&(df[2] == '0'))
        print('-------> LOG => Mask C170')
        print(mask_a170)
        numeric_values = pd.to_numeric(df.loc[mask_a170, base_calculo].str.replace(',', '.'), errors='coerce')

        new_values = numeric_values * aliquota
        new_values = new_values.apply(lambda x: f"{x:.2f}".replace('.', ','))

        df.loc[mask_a170, atribuir_resultado] = new_values   

        return df
    

    def alteracao_aliquota_C170(self):

        for i in range(len(self.df) - 1):
            if ((self.df.iloc[i, 0] == 'C100') & (self.df.iloc[i, 2] == '0')) and self.df.iloc[i + 1, 0] == 'C170':
                self.df.iloc[i + 1, 26] = '0,65'
                self.df.iloc[i + 1, 32] = '3'
                for j in range(50):
                   self.df.iloc[i + j, 33] = np.nan
                



