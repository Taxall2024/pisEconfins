import pandas as pd
import numpy as np
import colorama
class AlteracoesRegistros():
    
    def __init__(self,df):
        self.df = df
        
            

    def __recaculcalndo_aliquota_A170(self):
        self.df.loc[self.df[0] == 'A170', 10] = '0,65'
        self.df.loc[self.df[0] == 'A170', 14] = 3
        self.__calculos_aliquota(self.df,0.0065, 9, 11)
        self.__calculos_aliquota(self.df,0.03, 13, 15)
        
        self.data = str(self.df.iloc[0, 5])
        self.df_apurado = self.df.copy()

        # Retorna None para evitar renderização automática
        return self.df

    def __calculos_aliquota(self,df:pd.DataFrame,aliquota:float, base_calculo: int, atribuir_resultado: int):
        mask_a170 = df[0] == 'A170'
        
        numeric_values = pd.to_numeric(df.loc[mask_a170, base_calculo].str.replace(',', '.'), errors='coerce')

        new_values = numeric_values * aliquota
        new_values = new_values.apply(lambda x: f"{x:.2f}".replace('.', ','))

        df.loc[mask_a170, atribuir_resultado] = new_values   

        return df
    
    def __remove_C100_Col1_0(self):
        indices_para_remover = []

        for i in range(len(self.df) - 2):
            if ((self.df.iloc[i, 0] == 'C100') & (self.df.iloc[i, 1] == '0')) and self.df.iloc[i + 1, 0] == 'C110':
                if i + 1 < len(self.df) and self.df.iloc[i + 1, 0] == 'C110':
                    indices_para_remover.append(i+1)

        
        for i in range(len(self.df) - 2):
            if ((self.df.iloc[i, 0] == 'C100') & (self.df.iloc[i, 1] == '0')) and self.df.iloc[i + 1, 0] == 'C170':
                if i + 1 < len(self.df) and self.df.iloc[i + 1, 0] == 'C170':
                    indices_para_remover.append(i+2)
                    indices_para_remover.append(i+1)

        for i in range(len(self.df) - 2):
            if self.df.iloc[i, 0] != 'C100' and self.df.iloc[i + 1, 0] == 'C170':
                for j in range(1, 51):
                    if i + 1 < len(self.df) and self.df.iloc[i + j, 0] == 'C170':
                        indices_para_remover.append(i+j)

        
        self.df = self.df.drop(indices_para_remover).reset_index(drop=True)

        self.df = self.df.loc[~((self.df[0] == 'C100') & (self.df[2] == '1'))]

    def __remove_A100_Col2_1(self):
        indices_para_remover = []
        for i in range(len(self.df) - 2):
            if ((self.df.iloc[i, 0] == 'A100') & (self.df.iloc[i, 2] == '1')) and self.df.iloc[i + 1, 0] == 'A170':
                if i + 1 < len(self.df) and self.df.iloc[i + 1, 0] == 'A170':
                    indices_para_remover.append(i+2)
                    indices_para_remover.append(i+1)

        self.df = self.df.drop(indices_para_remover).reset_index(drop=True)

        self.df = self.df.loc[~((self.df[0] == 'A100') & (self.df[2] == '1'))]


    def __remove_F100_Col1_0(self):    
        self.df = self.df.loc[~((self.df[0] == 'F100') & (self.df[1] == '0'))]
    
    def __zerar_C100_Col1_0(self):        
        self.df.loc[((self.df[0] == 'C100')&(self.df[1] == '0')),25] = '0'
        self.df.loc[((self.df[0] == 'C100')&(self.df[1] == '0')),26] = '0'

    def __zerar_C170_Col1_0(self):
        for i in range(100):            
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),35] = '0'
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),33] = '0'
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),29] = '0'
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),25] = '0'
    
            self.df.loc[((self.df[0] == 'C170')&(self.df[1] == f'{i}')),31] = '0'

                
                
            self.df.loc[(self.df[0]=='C170') & (self.df[1]==f'{i}') & (self.df[24].str.contains('5')),24] = '70'

                    
            self.df.loc[(self.df[0]=='C170') & (self.df[1]==f'{i}') & (self.df[30].str.contains('5')),30] = '70'
    
    def __remove_C396(self):       
        self.df = self.df.loc[~(self.df[0] == 'C396')]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'C396'))]

    def __remove_C190(self):
            
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'C190'))]
        self.df = self.df.loc[~(self.df[0] == 'C190')]


    def __remove_C395(self):
            
        self.df = self.df.loc[~(self.df[0] == 'C395')]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'C395'))]
        
    def __remove_D100(self):
            
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'D100'))]
        self.df = self.df.loc[~(self.df[0] == 'D100')]

    
    def __remove_D500(self):

        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'D500'))]
        self.df = self.df.loc[~(self.df[0] == 'D500')]

    def __remove_F100(self):
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F100'))]
        self.df = self.df.loc[~(self.df[0] == 'F100')]
    
    def __remove_F120(self):

        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F120'))]
        self.df = self.df.loc[~(self.df[0] == 'F120')]
        
    def __remove_F130(self):

        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F130'))]
        self.df = self.df.loc[~(self.df[0] == 'F130')]
        
    def __remove_F150(self):
                        
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'F150'))]
        self.df = self.df.loc[~(self.df[0] == 'F150')]


    def __remove_M100(self):

        self.df = self.df.loc[~((self.df[0]== 'M100'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M100'))]

    def __rmeove_M105(self):

        self.df = self.df.loc[~((self.df[0]== 'M105'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M105'))]

        
    def __remove_M500(self):
            
        self.df = self.df.loc[~((self.df[0]== 'M500'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M500'))]

    def __remove_M505(self):

        self.df = self.df.loc[~((self.df[0]== 'M505'))]
        self.df = self.df.loc[~((self.df[0]== '9900')&(self.df[1] == 'M505'))]


    def __alterandoa_M205_Col1_12(self):
        self.df.loc[self.df[0] == 'M205', 1] = '12'


    def __alterando_M100_col2_810902(self):
        self.df.loc[self.df[0] == 'M100', 2] = '810902'
    
    def __alterando_M210_Col7(self):

        self.df.loc[self.df[0] == 'M210', 7] = '0,65' 

    
    def __alterando_M605_Cols_1_2(self): 
        self.df.loc[self.df[0] == 'M605', 1] = '12'
        self.df.loc[self.df[0] == 'M605', 2] = '217201'
        
    def __alterandoM610_Col_7(self):
            self.df.loc[self.df[0] == 'M610', 7] = '3'

    
    def __moodificacoes_grupo_M100(self):

        self.df.loc[self.df[0] == 'M100', 3] = 0
        self.df.loc[self.df[0] == 'M100', 7] = 0
        self.df.loc[self.df[0] == 'M100', 11] = 0
        self.df.loc[self.df[0] == 'M100', 13] = 0
        

    def __correcao_valores_Bloco_A100_e_A170(self):
        
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


    def __alteracao_F600_Col_6(self):
        self.df.loc[self.df[0] == 'F600', 6] = '1'
    
    
    def __remove_C500(self):

        self.df = self.df.loc[~(self.df[0] == 'C500')]
        self.df = self.df.loc[~((self.df[1] == 'C500')&(self.df[0] == '9900'))]

    def __remove_C50(self):

        self.df = self.df.loc[~(self.df[0].str.contains('C50'))]
        self.df = self.df.loc[~((self.df[1].str.contains('C50'))&(self.df[0] == '9900'))]
        
    def __recalculando_aliquota_M200_e_M600(self):

        def valor_m200():
            a100 = self.df.loc[self.df[0]=='A100']
            
            a100[15] = a100[15].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = round(a100[15].sum(),2)
            soma_a100 = str(soma_a100).replace('.',',')

            return soma_a100

        def valor_m600():
            a100 = self.df.loc[self.df[0]=='A100']
            
            a100[17] = a100[17].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = round(a100[17].sum(),2)
            soma_a100 = str(soma_a100).replace('.',',')
            

            return soma_a100    

        m200 = valor_m200()
        m600 = valor_m600()
        self.df.loc[self.df[0] == 'M200',12] = m200
        self.df.loc[self.df[0] == 'M200',8] = m200 #Corrigir esse valor para ser a ultima col do m210 
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
        
        

    def __recalculando_aliquota_M210_e_M610(self):

        def recalculando_m210():
            m210_valor_total = self.df.loc[self.df[0] == 'M210', 6].str.replace(',', '.').replace('', '0').astype(float)
            m210_aliquota = 0.0065

            resultado = round(m210_valor_total * m210_aliquota, 2).iloc[0]  
            resultado = str(resultado).replace('.', ',')
            return resultado

        def recalculando_m610():
            m610_valor_total = self.df.loc[self.df[0] == 'M610', 6].str.replace(',', '.').replace('', '0').astype(float)
            m610_aliquota = 0.03

            resultado = round(m610_valor_total * m610_aliquota, 2).iloc[0]  
            resultado = str(resultado).replace('.', ',')
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


        self.df = self.df.loc[~((self.df[0]=='M210')&(self.df[1]=='02'))]
        self.df = self.df.loc[~((self.df[0]=='M610')&(self.df[1]=='02'))]

        self.df.loc[self.df[0] == 'M210',1] = '51'
        self.df.loc[self.df[0] == 'M610',1] = '51'


    def __zerando_valores_M500(self):
        
        self.df.loc[self.df[0] == 'M500',3] = '0' 
        self.df.loc[self.df[0] == 'M500',7] = '0' 
        self.df.loc[self.df[0] == 'M500',8] = '0' 
        self.df.loc[self.df[0] == 'M500',9] = '0' 
        self.df.loc[self.df[0] == 'M500',10] = '0' 
        self.df.loc[self.df[0] == 'M500',11] = '0' 
        self.df.loc[self.df[0] == 'M500',12] = '0' 
        self.df.loc[self.df[0] == 'M500',13] = '0' 
        self.df.loc[self.df[0] == 'M500',14] = '0' 

    def __zerando_valores_M600(self):

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


    def __recaculcalndo_aliquota_C170_Col2_0(self):

        self.df = self.__calculos_aliquota_C170(self.df,0.0065, 15, 25)
        self.df = self.__calculos_aliquota_C170(self.df,0.03, 15, 26)
        


    def __calculos_aliquota_C170(self,df:pd.DataFrame,aliquota:float, base_calculo: int, atribuir_resultado: int):
        mask_a170 = ((df[0] == 'C100')&(df[2] == '0'))

        numeric_values = pd.to_numeric(df.loc[mask_a170, base_calculo].str.replace(',', '.'), errors='coerce')

        new_values = numeric_values * aliquota
        new_values = new_values.apply(lambda x: f"{x:.2f}".replace('.', ','))

        df.loc[mask_a170, atribuir_resultado] = new_values   

        return df
    

    def __alteracao_aliquota_C170(self):

        for i in range(len(self.df) - 1):
            if ((self.df.iloc[i, 0] == 'C100') & (self.df.iloc[i, 2] == '0')) and self.df.iloc[i + 1, 0] == 'C170':
                self.df.iloc[i + 1, 26] = '0,65'
                self.df.iloc[i + 1, 32] = '3'
                
                base_de_calculo_numerico = float(self.df.iloc[i , 15].replace(',', '.'))

                self.df.iloc[i + 1 , 25] = self.df.iloc[i , 15]
                self.df.iloc[i + 1 , 31] = self.df.iloc[i , 15]

                self.df.iloc[i + 1, 29] = str(round(base_de_calculo_numerico * 0.0065,2)).replace('.', ',')
                self.df.iloc[i + 1, 35] = str(round(base_de_calculo_numerico * 0.03,2)).replace('.', ',')


            for j in range(1, 51):
                if i + j < len(self.df) and self.df.iloc[i + j, 0] == 'C170':
                    self.df.iloc[i + j, 33] = '' 
                    self.df.iloc[i + j, 26] = '0,65' 
                    self.df.iloc[i + j, 32] = '3' 

    def __remove_m205_repetida(self):
        mask_m205 = self.df[0] == 'M205'
        df_no_m205 = self.df[~mask_m205]
        df_m205_unique = self.df[mask_m205].drop_duplicates(subset=0, keep='first')
        self.df = pd.concat([df_no_m205, df_m205_unique]).sort_index().reset_index(drop=True)

    def __remove_m605_repetida(self):
        mask_m605 = self.df[0] == 'M605'
        df_no_m605 = self.df[~mask_m605]
        df_m605_unique = self.df[mask_m605].drop_duplicates(subset=0, keep='first')
        self.df = pd.concat([df_no_m605, df_m605_unique]).sort_index().reset_index(drop=True)

    def __somatorio_agragado_valores_c170_m200(self):
        lista_de_valores = []
        
        for i in range(len(self.df) - 1):
            if ((self.df.iloc[i, 0] == 'C100') & (self.df.iloc[i, 2] == '0')) and self.df.iloc[i + 1, 0] == 'C170':
                lista_de_valores.append(round(float(self.df.iloc[i + 1, 29].replace(',', '.')),2))
    
    
        valor_total = sum(lista_de_valores)
        self.df.loc[self.df[0] == 'M200', 8] = str(valor_total).replace('.', ',')

    def __somatorio_agragado_valores_c170_m600(self):

        lista_de_valores = []
        
        for i in range(len(self.df) - 1):
            if ((self.df.iloc[i, 0] == 'C100') & (self.df.iloc[i, 2] == '0')) and self.df.iloc[i + 1, 0] == 'C170':
                lista_de_valores.append(round(float(self.df.iloc[i + 1, 35].replace(',', '.')),2))
    
    
        valor_total = sum(lista_de_valores)
        self.df.loc[self.df[0] == 'M600', 8] = str(valor_total).replace('.', ',')

    def __somatorio_agragado_valores_A170_m200(self):
        lista_de_valores = []
        
        try:
            for i in range(len(self.df) - 1):
                if ((self.df.iloc[i, 0] == 'A100') & (self.df.iloc[i, 2] == '0')) and self.df.iloc[i + 1, 0] == 'A170':
                    lista_de_valores.append(round(float(self.df.iloc[i + 1, 13].replace(',', '.')),2))
        except Exception as e:
            pass
        if lista_de_valores is not None: 
            self.valor_total_m200_col8 = round(sum(lista_de_valores),2)
            self.df.loc[self.df[0] == 'M210', 3] = str(self.valor_total_m200_col8).replace('.', ',')
        
    def __valores_compilados_finais_m200(self):
        self.df.loc[self.df[0] == 'M200',8] = self.df.loc[self.df[0]=='M210', 15].values[0]
        self.df.loc[self.df[0] == 'M200',7] = ''
         
    def __correcao_de_capos_M700(self):
        self.df.loc[(self.df.iloc[:, 1] == '01')&(self.df[0]=='M700'), 2] = (
            self.df.loc[(self.df.iloc[:, 1] == '01')&(self.df[0]=='M700')].iloc[:, 2]
            .astype(str)
            .str.replace(',', '.')
            .astype(float).multiply(0.0065).div(0.0165).round(2).apply(lambda x: str(x).replace('.',','))
        )
        
        m700_df = self.df[self.df.iloc[:, 0] == 'M700'].copy()

        col_chave = m700_df.columns[6]
        valores_duplicados = m700_df[col_chave][m700_df.duplicated(col_chave, keep=False)].unique()

        lista_de_duplicadas_para_eliminar = []

        for value in valores_duplicados:
            m700_df = m700_df.loc[m700_df[6]==value]
            
            lista_de_duplicadas_para_eliminar.append(abs(~(m700_df.index[0])))

            m700_df[2] = m700_df[2].str.replace(',','.').astype(float)
            valor_final = str(round(sum(m700_df[2]),2)).replace('.',',')
            self.df.loc[(self.df[0]=='M700')&(self.df[6]==value),[2,5]] = valor_final
        
        self.df = self.df.drop(lista_de_duplicadas_para_eliminar)

        m700_df = m700_df.loc


        mask = (self.df.iloc[:, 0] == 'M700') & (self.df.iloc[:, 1] == '01')

        self.df.loc[mask, 3] = ''
        self.df.loc[mask, 4] = ''
        self.df.loc[mask, 5] = self.df.loc[mask, 2] 
        self.df.loc[mask, 1] = '51'

    def __correcao_de_capos_M300(self):

        self.df.loc[(self.df.iloc[:, 1] == '01')&(self.df[0]=='M300'), 2] = (
            self.df.loc[(self.df.iloc[:, 1] == '01')&(self.df[0]=='M300')].iloc[:, 2]
            .astype(str)
            .str.replace(',', '.')
            .astype(float).multiply(0.0065).div(0.0165).round(2).apply(lambda x: str(x).replace('.',','))
        )
        
        m300_df = self.df[self.df.iloc[:, 0] == 'M300'].copy()

        col_chave = m300_df.columns[6]
        valores_duplicados = m300_df[col_chave][m300_df.duplicated(col_chave, keep=False)].unique()

        lista_de_duplicadas_para_eliminar = []

        for value in valores_duplicados:
            m300_df = m300_df.loc[m300_df[6]==value]
            
            lista_de_duplicadas_para_eliminar.append(abs(~(m300_df.index[0])))

            m300_df[2] = m300_df[2].str.replace(',','.').astype(float)
            valor_final = str(round(sum(m300_df[2]),2)).replace('.',',')
            self.df.loc[(self.df[0]=='M300')&(self.df[6]==value),[2,5]] = valor_final
        
        self.df = self.df.drop(lista_de_duplicadas_para_eliminar)

        m300_df = m300_df.loc


        mask = (self.df.iloc[:, 0] == 'M300') & (self.df.iloc[:, 1] == '01')

        self.df.loc[mask, 3] = ''
        self.df.loc[mask, 4] = ''
        self.df.loc[mask, 5] = self.df.loc[mask, 2] 
        self.df.loc[mask, 1] = '51'

    def __agregado_F600_M200(self):

        valor_total = round(self.df.loc[self.df[0] == 'F600', 8].str.replace(',', '.').replace('', '0').astype(float).sum(),2)
        self.df.loc[self.df[0] == 'M200', 9 ] = str(valor_total).replace('.', ',').strip()               

    def __agregado_F600_M600(self):

        valor_total = round(self.df.loc[self.df[0] == 'F600', 9].str.replace(',', '.').replace('', '0').astype(float).sum(),2)
        self.df.loc[self.df[0] == 'M600', 9 ] = str(valor_total).replace('.', ',').strip()                

    def __removendo_m210_duplicada_e_ajustando_valores(self):
        

        
        df_m210 = self.df.loc[self.df[0] == 'M210']
        df_m210[[2, 3, 6]] = df_m210[[2, 3, 6]].replace(',', '.', regex=True).astype(float)

        [df_m210.__setitem__(i, df_m210[i].sum().round(2)) for i in [2, 3, 6]]
  
        [df_m210.__setitem__( i, df_m210.iloc[0,6] * 0.0065) for i in [10,15]]

        [df_m210.__setitem__(i, df_m210[i].apply(lambda x: f"{x: .2f}".replace('.', ',').strip())) for i in [2, 3, 6, 10, 15]]


        df_no_m210 = self.df.loc[~self.df.index.isin(df_m210.index)]
        df_m210_unique = df_m210.drop_duplicates(subset=0, keep='first')
        self.df = pd.concat([df_no_m210, df_m210_unique]).sort_index().reset_index(drop=True)

    def __removendo_m610_duplicada_e_ajustando_valores(self):

        df_m610 = self.df.loc[self.df[0] == 'M610']
        df_m610[[2, 3, 6]] = df_m610[[2, 3, 6]].replace(',', '.', regex=True).astype(float)

        [df_m610.__setitem__(i, df_m610[i].sum().round(2)) for i in [2, 3, 6]]
  
        [df_m610.__setitem__( i, df_m610.iloc[0,6] * 0.03) for i in [10,15]]

        [df_m610.__setitem__(i, df_m610[i].apply(lambda x: f"{x: .2f}".replace('.', ',').strip())) for i in [2, 3, 6, 10, 15]]



        df_m6210_no = self.df.loc[~self.df.index.isin(df_m610.index)]
        df_m610_unique = df_m610.drop_duplicates(subset=0, keep='first')
        self.df = pd.concat([df_m6210_no, df_m610_unique]).sort_index().reset_index(drop=True)

    def __valor_final_ultima_col_m210(self):

        valor_base = self.df.loc[self.df[0] == 'M210', 10].str.replace(',', '.').replace('', '0').astype(float).sum() 
        
        somatorio = self.df.loc[self.df[0] == 'M210', 11].str.replace(',', '.').replace('', '0').astype(float).sum() 

        subtracao = self.df.loc[self.df[0] == 'M210', 12].str.replace(',', '.').replace('', '0').astype(float).sum() 
        valor_final = round(valor_base + somatorio - subtracao,2)

        self.df.loc[self.df[0] == 'M210', 15] = str(valor_final).replace('.', ',').strip()

    def __valor_final_ultima_col_m610(self):
 
         valor_base = self.df.loc[self.df[0] == 'M610', 10].str.replace(',', '.').replace('', '0').astype(float).sum() 
         
         somatorio = self.df.loc[self.df[0] == 'M610', 11].str.replace(',', '.').replace('', '0').astype(float).sum() 
 
         subtracao = self.df.loc[self.df[0] == 'M610', 12].str.replace(',', '.').replace('', '0').astype(float).sum() 
         valor_final = round(valor_base + somatorio - subtracao,2)
 
         self.df.loc[self.df[0] == 'M610', 15] = str(valor_final).replace('.', ',').strip()

    def __calculos_finais_M200(self):

        #self.df.loc[self.df[0] == 'M200',7] = self.df.loc[self.df[0] == 'M210',15].values

        subtracao_m200 = self.df.loc[self.df[0]=='M200']
        subtracao_m200[[8,9]] = subtracao_m200[[8,9]].replace(',', '.', regex=True).astype(float)
        self.df.loc[self.df[0]=='M200',12] = np.where(subtracao_m200[8] - subtracao_m200[9] > 0,
                                                      (subtracao_m200[8] - subtracao_m200[9]).apply(lambda x: f"{x:.2f}".replace('.', ',')),
                                                      0)
   
    def __calculos_finais_M600(self):

        self.df.loc[self.df[0] == 'M600',7] = self.df.loc[self.df[0] == 'M610',15].values

        subtracao_m600 = self.df.loc[self.df[0]=='M600']
        subtracao_m600[[7,8]] = subtracao_m600[[7,8]].replace(',', '.', regex=True).astype(float)
        self.df.loc[self.df[0]=='M600',12] = np.where(subtracao_m600[7] - subtracao_m600[8] > 0,
                                                      (subtracao_m600[7] - subtracao_m600[8]).apply(lambda x: f"{x:.2f}".replace('.', ',')),
                                                      0)

    def __resolucao_M205_e_M200(self):
        self.df.loc[self.df[0] == 'M200',8] = self.df.loc[self.df[0]=='M210',15].values[0]
        value_m205 =  float(self.df.loc[self.df[0]=='M210',15].values[0].replace(',','.'))
        value_m200 = float(self.df.loc[self.df[0] == 'M200',9].values[0].replace(',','.')) 
        
        if value_m205 > value_m200:
            self.df.loc[self.df[0]=='M200',[11,12]] = str(round(value_m205 - value_m200,2)).replace('.',',')

        if value_m205 < value_m200 or value_m205 == value_m200:
            self.df.loc[self.df[0]=='M200',9] = self.df.loc[self.df[0]=='M200',8]
            self.df.loc[self.df[0]=='M200',[11,12]] = 0
            self.df = self.df.loc[~(self.df[0] == 'M205')]

    def __resolucao_M605_e_M600(self):
        self.df.loc[self.df[0] == 'M600',8] = self.df.loc[self.df[0]=='M610',15].values[0]
        value_m605 =  float(self.df.loc[self.df[0]=='M610',15].values[0].replace(',','.'))
        value_M600 = float(self.df.loc[self.df[0] == 'M600',9].values[0].replace(',','.')) 
        
        if value_m605 > value_M600:
            self.df.loc[self.df[0]=='M600',[11,12]] = str(round(value_m605 - value_M600,2)).replace('.',',')

        if value_m605 < value_M600 or value_m605 == value_M600:
            self.df.loc[self.df[0]=='M600',9] = self.df.loc[self.df[0]=='M600',8]
            self.df.loc[self.df[0]=='M600',[11,12]] = 0
            self.df = self.df.loc[~(self.df[0] == 'M605') ]

    def __ajustando_duplicadas_F600(self):
        indices_para_excluir_f600 = []
        for i in range(len(self.df)):
            for j in range(1,10):
                if i + j >= len(self.df):
                    break
                if self.df.iloc[i , 0] == 'F600':
                    if (self.df.iloc[i,5] == self.df.iloc[i+j,5]) and (self.df.iloc[i,7] == self.df.iloc[i+j,7]):
                        self.df.iloc[i,[3,4,8,9]] = self.df.iloc[i,[3,4,8,9]].apply(lambda x: float(str(x).replace(',','.')))
                        self.df.iloc[i + j,[3,4,8,9]] = self.df.iloc[i + j,[3,4,8,9]].apply(lambda x: float(str(x).replace(',','.')))

                        self.df.iloc[i,[3,4,8,9]] = self.df.iloc[i,[3,4,8,9]] + self.df.iloc[i + j,[3,4,8,9]]
                        
                        self.df.iloc[i, [3, 4, 8, 9]] = self.df.iloc[i, [3, 4, 8, 9]].apply(lambda x: round (x, 2))

                        self.df.iloc[i,[3,4,8,9]] = self.df.iloc[i,[3,4,8,9]].apply(lambda x: str(x).replace('.',','))
                        self.df.iloc[i + j,[3,4,8,9]] = self.df.iloc[i + j,[3,4,8,9]].apply(lambda x: str(x).replace('.',','))

                        indices_para_excluir_f600.append(i+j)

        lista_sem_duplicadas = []
        lista_sem_duplicadas = list(set(indices_para_excluir_f600)) 
                   
        self.df = self.df.drop(self.df.index[lista_sem_duplicadas]).reset_index(drop=True)

    def __ajuste_valores_base_m300_m210_m200(self):

        valores = self.df.loc[self.df[0] == 'M300', 5]
        valores = valores.str.replace(',', '.').astype(float)
        somatorio_m300 = valores.sum()
        self.df.loc[self.df[0]=='M210',14] = str(somatorio_m300).replace('.',',')

        valores_m210 = self.df.loc[self.df[0] == 'M210', [10, 11, 12, 13, 14]]
        valores_convertidos = valores_m210.applymap(lambda x: float(str(x).replace(',', '.')))
        contas_finais_m210_somas = valores_convertidos[[10,11,14]].sum(axis=1).values[0] 
        contas_finais_m210_subtração = valores_convertidos[[12,13]].sum(axis=1).values[0] 
        valor_final = round(contas_finais_m210_somas - contas_finais_m210_subtração,2)
        self.df.loc[self.df[0]=='M210', 15] = str(valor_final).replace('.',',')
        print(colorama.Fore.CYAN,f' ======= LOG ====== > : {valor_final}',colorama.Fore.RESET)

    def __limpando_colunas_m230_e_re_calculando_aliquota(self):
        self.df.loc[self.df[0]=='M230',[-2,-1]] = ''
        self.df.loc[self.df[0]=='M230' , 4] = (self.df.loc[self.df[0]=='M230' , 3].str.replace(',','.')
                                               .astype(float)
                                               .multiply(0.0065)
                                               .round(2)
                                               .apply(lambda x: str(x).replace(',','.')))
    def __limpando_colunas_m630_e_re_calculando_aliquota(self):
        self.df.loc[self.df[0]=='M630',[-2,-1]] = ''
        self.df.loc[self.df[0]=='M630' , 4] = (self.df.loc[self.df[0]=='M630' , 3].str.replace(',','.')
                                               .astype(float)
                                               .multiply(0.0065)
                                               .round(2)
                                               .apply(lambda x: str(x).replace(',','.')))




    def alterar_valores(self):
        
        self.__recaculcalndo_aliquota_A170()

        # Remoçao com condicional
        self.__remove_A100_Col2_1()
        self.__remove_F100_Col1_0()

        # Zerando valores
        self.__zerar_C100_Col1_0()
        self.__zerar_C170_Col1_0()

        # Remoção
        self.__remove_C396()
        self.__remove_C190()
        self.__remove_C395()
        self.__remove_D100()
        self.__remove_D500()
        self.__remove_F100()
        self.__remove_F120()
        self.__remove_F130()
        self.__remove_F150()
        self.__remove_M100()
        self.__rmeove_M105()
        self.__remove_M500()
        self.__remove_M505()

        #Alterações com uma ou mais condicionais
        self.__alterandoa_M205_Col1_12()
        self.__alterando_M100_col2_810902()
        self.__alterando_M210_Col7()
        self.__alterando_M605_Cols_1_2()
        self.__alterandoM610_Col_7()
        self.__moodificacoes_grupo_M100()
        self.__correcao_valores_Bloco_A100_e_A170()
        self.__alteracao_F600_Col_6()
       
        # Remoção
        self.__remove_C500()
        self.__remove_C50()

        #Correção e recaculos

        self.__recalculando_aliquota_M200_e_M600()
        self.__recalculando_aliquota_M210_e_M610()
        self.__zerando_valores_M500()
        self.__zerando_valores_M600()

        # ''' Até aqui são as alterações que geraram os resultados dos arquivos para GE e Máxima '''

        # '''  A partir daqui são alterações novas da Brasfort '''
        
        self.__recaculcalndo_aliquota_C170_Col2_0()
        self.__alteracao_aliquota_C170()
        self.__remove_m205_repetida()
        self.__remove_m605_repetida()

        self.__somatorio_agragado_valores_c170_m200()
        self.__somatorio_agragado_valores_c170_m600()

        self.__agregado_F600_M200()
        self.__agregado_F600_M600()
        try:
            self.__removendo_m210_duplicada_e_ajustando_valores()
            self.__removendo_m610_duplicada_e_ajustando_valores()
        except:
            pass
        self.__valor_final_ultima_col_m210()
        self.__valor_final_ultima_col_m610()

        # ''' A partir daqui serão alterações vindas da empresa Quality Max'''

        self.__calculos_finais_M600()
        self.__resolucao_M205_e_M200()
        self.__resolucao_M605_e_M600()
        self.__remove_C100_Col1_0()
        self.__ajustando_duplicadas_F600()

        # ''' A partir daqui são novas adicionais feitas coma arquivo da Brasfort ''''
        
        self.__somatorio_agragado_valores_A170_m200()
        self.__limpando_colunas_m230_e_re_calculando_aliquota()
        self.__limpando_colunas_m630_e_re_calculando_aliquota()
        self.__correcao_de_capos_M300()
        self.__correcao_de_capos_M700()
        self.__ajuste_valores_base_m300_m210_m200()
        self.__valores_compilados_finais_m200()
        self.__calculos_finais_M200()