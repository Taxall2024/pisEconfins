import pandas as pd
import numpy as np
from colorama import Fore
import inspect
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

def log_erro(nome_metodo,e):
    print(Fore.RED,f" ======== LOG ===== > Erro no metodo {nome_metodo}, favor verificar! {e}",Fore.RESET)


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
        
    def __valores_compilados_finais_m600(self):
        self.df.loc[self.df[0] == 'M600',8] = self.df.loc[self.df[0]=='M610', 15].values[0]
        self.df.loc[self.df[0] == 'M600',7] = ''


    def __valores_compilados_finais_m200(self):
        self.df.loc[self.df[0] == 'M200',8] = self.df.loc[self.df[0]=='M210', 15].values[0]
        self.df.loc[self.df[0] == 'M200',7] = ''
         

    def __correcao_de_capos_M700(self):



        mask = (self.df.iloc[:, 0] == 'M700') & (self.df.iloc[:, 1] == '01')

        self.df.loc[mask, 3] = ''
        self.df.loc[mask, 4] = ''
        self.df.loc[mask, 1] = '51'

        

        self.df.loc[(self.df.iloc[:, 1] == '51')&(self.df[0]=='M700'), 2] = (
            self.df.loc[(self.df.iloc[:, 1] == '51')&(self.df[0]=='M700')].iloc[:, 2]
            .astype(str)
            .str.replace(',', '.')
            .astype(float).multiply(0.03).div(0.076).round(2).apply(lambda x: str(x).replace('.',','))
        )
        
        m700_df = self.df[self.df.iloc[:, 0] == 'M700'].copy()

        col_chave = m700_df.columns[6]
        valores_duplicados = m700_df[col_chave][m700_df.duplicated(col_chave, keep=False)].unique()
        lista_de_duplicadas_para_eliminar = []

        for value in valores_duplicados:
            registros_duplicados = m700_df[m700_df[6] == value]

            if registros_duplicados.empty:
                continue

            # Soma os valores da coluna 2
            registros_duplicados[2] = registros_duplicados[2].str.replace(',', '.').astype(float)
            valor_final = str(round(registros_duplicados[2].sum(), 2)).replace('.', ',')

            # Atualiza os campos 2 e 5 com o valor final
            self.df.loc[(self.df[0] == 'M700') & (self.df[6] == value), [2, 5]] = valor_final

            # Marca para remoção todos os índices duplicados exceto o primeiro
            indices_para_remover = registros_duplicados.index[1:]
            lista_de_duplicadas_para_eliminar.extend(indices_para_remover)
        
        self.df.loc[mask, 5] = self.df.loc[mask, 2] 

        print(Fore.LIGHTCYAN_EX,f'Valores   duplicados {valores_duplicados}',Fore.RESET)
        print(Fore.LIGHTCYAN_EX,f'Lista de indices para eliminar {lista_de_duplicadas_para_eliminar}',Fore.RESET)
        self.df = self.df.drop(lista_de_duplicadas_para_eliminar)


    def __correcao_de_capos_M300(self):

        mask = (self.df.iloc[:, 0] == 'M300') & (self.df.iloc[:, 1] == '01')

        self.df.loc[mask, 3] = ''
        self.df.loc[mask, 4] = ''
        self.df.loc[mask, 1] = '51'
       
        self.df.loc[(self.df.iloc[:, 1] == '51')&(self.df[0]=='M300'), 2] = (
            self.df.loc[(self.df.iloc[:, 1] == '51')&(self.df[0]=='M300')].iloc[:, 2]
            .astype(str)
            .str.replace(',', '.')
            .astype(float)
            .multiply(0.0065)
            .div(0.0165)
            .round(2)
            .apply(lambda x: str(x).replace('.',','))
        )
        
        m300_df = self.df[self.df.iloc[:, 0] == 'M300'].copy()

        col_chave = m300_df.columns[6]
        valores_duplicados = m300_df[col_chave][m300_df.duplicated(col_chave, keep=False)].unique()

        lista_de_duplicadas_para_eliminar = []

        for value in valores_duplicados:
            registros_duplicados = m300_df[m300_df[6] == value]

            if registros_duplicados.empty:
                continue

            # Soma os valores da coluna 2
            registros_duplicados[2] = registros_duplicados[2].str.replace(',', '.').astype(float)
            valor_final = str(round(registros_duplicados[2].sum(), 2)).replace('.', ',')

            # Atualiza os campos 2 e 5 com o valor final
            self.df.loc[(self.df[0] == 'M300') & (self.df[6] == value), [2, 5]] = valor_final

            # Marca para remoção todos os índices duplicados exceto o primeiro
            indices_para_remover = registros_duplicados.index[1:]
            lista_de_duplicadas_para_eliminar.extend(indices_para_remover)
        

        print(Fore.LIGHTCYAN_EX,f'Valores   duplicados {valores_duplicados}',Fore.RESET)
        print(Fore.LIGHTCYAN_EX,f'Lista de indices para eliminar {lista_de_duplicadas_para_eliminar}',Fore.RESET)
        self.df = self.df.drop(lista_de_duplicadas_para_eliminar)

        self.df.loc[mask, 5] = self.df.loc[mask, 2] 

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

        self.df.loc[self.df[0] == 'M200',8] = self.df.loc[self.df[0] == 'M210',15].values[0]

        subtracao_m200 = self.df.loc[self.df[0]=='M200']
        subtracao_m200[[8, 9]] = (
            subtracao_m200[[ 8,9]]
            .replace(',', '.', regex=True)
            .apply(pd.to_numeric, errors='coerce')
        )          

        self.df.loc[self.df[0]=='M200',12] = np.where(subtracao_m200[8] - subtracao_m200[9] > 0,
                                                      (subtracao_m200[8] - subtracao_m200[9]).apply(lambda x: f"{x:.2f}".replace('.', ',')),
                                                      0)
   
    def __calculos_finais_M600(self):

        self.df.loc[self.df[0] == 'M600',8] = self.df.loc[self.df[0] == 'M610',15].values[0]

        subtracao_m600 = self.df.loc[self.df[0]=='M600']
        subtracao_m600[[8, 9]] = (
            subtracao_m600[[ 8,9]]
            .replace(',', '.', regex=True)
            .apply(pd.to_numeric, errors='coerce')
        )        
        self.df.loc[self.df[0]=='M600',12] = np.where(subtracao_m600[8] - subtracao_m600[9] > 0,
                                                      (subtracao_m600[8] - subtracao_m600[9]).apply(lambda x: f"{x:.2f}".replace('.', ',')),
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

    def __ajuste_valores_base_M700_M610_m200(self):

        valores = self.df.loc[self.df[0] == 'M700', 5]
        valores = valores.str.replace(',', '.').astype(float)
        somatorio_M700 = round(valores.sum(),2)
        self.df.loc[self.df[0]=='M610',14] = str(somatorio_M700).replace('.',',')

        valores_M610 = self.df.loc[self.df[0] == 'M610', [10, 11, 12, 13, 14]]
        valores_convertidos = valores_M610.applymap(lambda x: float(str(x).replace(',', '.')))
        contas_finais_M610_somas = valores_convertidos[[10,11,14]].sum(axis=1).values[0] 
        contas_finais_M610_subtração = valores_convertidos[[12,13]].sum(axis=1).values[0] 
        valor_final = round(contas_finais_M610_somas - contas_finais_M610_subtração,2)
        self.df.loc[self.df[0]=='M610', 15] = str(valor_final).replace('.',',')

    def __ajuste_valores_base_m300_m210_m200(self):

        valores = self.df.loc[self.df[0] == 'M300', 5]
        valores = valores.str.replace(',', '.').astype(float)
        somatorio_m300 = round(valores.sum(),2)
        self.df.loc[self.df[0]=='M210',14] = str(somatorio_m300).replace('.',',')

        valores_m210 = self.df.loc[self.df[0] == 'M210', [10, 11, 12, 13, 14]]
        valores_convertidos = valores_m210.applymap(lambda x: float(str(x).replace(',', '.')))
        contas_finais_m210_somas = valores_convertidos[[10,11,14]].sum(axis=1).values[0] 
        contas_finais_m210_subtração = valores_convertidos[[12,13]].sum(axis=1).values[0] 
        valor_final = round(contas_finais_m210_somas - contas_finais_m210_subtração,2)
        self.df.loc[self.df[0]=='M210', 15] = str(valor_final).replace('.',',')

    def __limpando_colunas_m230_e_re_calculando_aliquota(self):
        self.df.loc[self.df[0]=='M230',[5,6]] = ''

        self.df.loc[self.df[0]=='M230' , 4] = (self.df.loc[self.df[0]=='M230' , 3].str.replace(',','.')
                                               .astype(float)
                                               .multiply(0.0065)
                                               .round(2)
                                               .apply(lambda x: str(x).replace('.',',')))
        
        valor_total_m230 = str(round(self.df.loc[self.df[0]=='M230',4].str.replace(',','.')
                                                                .astype(float)
                                                                .sum(),2)).replace('.',',')
        
        self.df.loc[self.df[0]=='M210',13] = valor_total_m230
                                                                    
    def __limpando_colunas_m630_e_re_calculando_aliquota(self):
        self.df.loc[self.df[0]=='M630',[5,6]] = ''
        self.df.loc[self.df[0]=='M630' , 4] = (self.df.loc[self.df[0]=='M630' , 3].str.replace(',','.')
                                               .astype(float)
                                               .multiply(0.03)
                                               .round(2)
                                               .apply(lambda x: str(x).replace('.',',')))
        valor_total_m630 = str(round(self.df.loc[self.df[0]=='M630',4].str.replace(',','.')
                                                                .astype(float)
                                                                .sum(),2)).replace('.',',')
        
        self.df.loc[self.df[0]=='M610',13] = valor_total_m630                                           

    def __retirando_cnpjs_duplicados_m230(self):
        # Filtra apenas os registros M230
        M230_df = self.df[self.df.iloc[:, 0] == 'M230'].copy()

        if M230_df.empty:
            return 

        col_chave = M230_df.columns[1]  
        col_valor = M230_df.columns[2]  

        
        valores_duplicados = M230_df[col_chave][M230_df.duplicated(col_chave, keep=False)].unique()
        indices_para_remover = []

        for chave in valores_duplicados:
            duplicados = M230_df[M230_df[col_chave] == chave].copy()

            if duplicados.empty or len(duplicados) < 2:
                continue  

            try:
                
                duplicados[col_valor] = duplicados[col_valor].str.replace(',', '.').astype(float)
                valor_final = str(round(duplicados[col_valor].sum(), 2)).replace('.', ',')

                
                self.df.loc[(self.df[0] == 'M230') & (self.df[6] == chave), 2] = valor_final

                
                indices_para_remover.extend(duplicados.index[1:])
            except Exception as e:
                print(f"Erro ao processar CNPJ duplicado '{chave}': {e}")

        # Remove duplicados marcados
        self.df = self.df.drop(index=indices_para_remover) 
        
    def __retirando_cnpjs_duplicados_M630(self):
        M630_df = self.df[self.df.iloc[:, 0] == 'M630'].copy()

        if M630_df.empty:
            return

        col_chave = M630_df.columns[1]
        valores_duplicados = M630_df[col_chave][M630_df.duplicated(col_chave, keep=False)].unique()

        lista_de_duplicadas_para_eliminar = []

        for value in valores_duplicados:
            linhas_duplicadas = M630_df[M630_df[col_chave] == value].copy()

            if linhas_duplicadas.empty or len(linhas_duplicadas) < 2:
                continue  # Nada para somar/remover

            try:
                # Soma os valores da coluna 2 (deve estar como string com vírgula)
                linhas_duplicadas[2] = linhas_duplicadas[2].str.replace(',', '.').astype(float)
                valor_final = str(round(linhas_duplicadas[2].sum(), 2)).replace('.', ',')

                # Atualiza no DataFrame original
                self.df.loc[(self.df[0] == 'M630') & (self.df[6] == value), 2] = valor_final

                # Remove todas exceto a primeira
                indices_para_remover = linhas_duplicadas.index[1:]
                lista_de_duplicadas_para_eliminar.extend(indices_para_remover)
            except Exception as e:
                print(f"Erro ao processar CNPJ duplicado '{value}': {e}")

        self.df = self.df.drop(index=lista_de_duplicadas_para_eliminar)

    def __passando_valor_m600_para_m605(self):
        self.df.loc[self.df[0]=='M605',3] = self.df.loc[self.df[0]=='M600',12].values[0]

    def __passando_valor_m200_para_205(self):
        self.df.loc[self.df[0]=='M205',3] = self.df.loc[self.df[0]=='M200',12].values[0]

    def __ajuste_valores_F100(self):

        self.df.loc[self.df[0]=='F100',8] = '0,65'
        self.df.loc[self.df[0]=='F100',12] = '3'
        self.df.loc[self.df[0]=='F100',9] = (self.df.loc[self.df[0]=='F100',7]
                                             .str.replace(',','.')
                                             .astype(float)
                                             .multiply(0.0065)
                                             .round(2)
                                             .apply(lambda x: str(x).replace('.',',')))
        self.df.loc[self.df[0]=='F100',13] = (self.df.loc[self.df[0]=='F100',11]
                                             .str.replace(',','.')
                                             .astype(float)
                                             .multiply(0.03)
                                             .round(2)
                                             .apply(lambda x: str(x).replace('.',',')))




    def alterar_valores(self):
        
        try:
            self.__recaculcalndo_aliquota_A170()

        except Exception as e:
            log_erro("Recalculando_Aliquiota_A170",e)
            pass       
        
        try:
            
            self.__remove_A100_Col2_1()
        except Exception as e:
            log_erro('remove_a100_Col2_1',e)   
            pass 
        
        try:
            self.__remove_F100_Col1_0()
        except Exception as e:
            log_erro('remove_F100_Col1_0',e)
            pass

        # Zerando valores        
        try:
            self.__zerar_C100_Col1_0()
        except Exception as e:         
            log_erro('zerar_C100_Col1_0',e)     
            pass
        
        try:
            self.__zerar_C170_Col1_0()
        except Exception as e:
            log_erro('zerar_C170_Col1_0',e )
            
            
             # Remoção

        try:
            self.__ajuste_valores_F100()
        except Exception as e:
            log_erro('__ajuste_valores_F100',e )
        try:
            self.__remove_C396()
        except Exception as e:
            log_erro('__remove_C396',e )       
        try:
            self.__remove_C190()
        except Exception as e:
            log_erro('__remove_C190',e )       
        try:
            self.__remove_C395()
        except Exception as e:
            log_erro('__remove_C395',e )       
        try:
            self.__remove_D100()
        except Exception as e:
            log_erro('__remove_D100',e )       
        try:
            self.__remove_D500()
        except Exception as e:
            log_erro('__remove_D500',e )       
        try:
            self.__remove_F120()
        except Exception as e:
            log_erro('__ajuste_valores_F100',e )       
        try:
            self.__remove_F130()
        except Exception as e:
            log_erro('__remove_C396',e )       
        try:
            self.__remove_F150()
        except Exception as e:
            log_erro('__remove_C190',e )       
        try:
            self.__remove_M100()
        except Exception as e:
            log_erro('__remove_C395',e )       
        try:
            self.__rmeove_M105()
        except Exception as e:
            log_erro('__remove_D100',e )       
        try:
            self.__remove_M500()
        except Exception as e:
            log_erro('__remove_D500',e )       
        try:
            self.__remove_M505()
        except Exception as e:
            log_erro('__ajuste_valores_F100',e )

        #Alterações com uma ou mais condicionais
   
        
        
            
        try:
            self.__alterandoa_M205_Col1_12()
        except Exception as e:
            log_erro('.__alterandoa_M205_Col1_12',e )
            
        try:
            self.__alterando_M100_col2_810902()
        except Exception as e:
            log_erro('.__alterando_M100_col2_810902',e )
            
        try:
            self.__alterando_M210_Col7()
        except Exception as e:
            log_erro('.__alterando_M210_Col7',e )
            
        try:
            self.__alterando_M605_Cols_1_2()
        except Exception as e:
            log_erro('.__alterando_M605_Cols_1_2',e )
            
        try:
            self.__alterandoM610_Col_7()
        except Exception as e:
            log_erro('.__alterandoM610_Col_7',e )
            
        try:
            self.__moodificacoes_grupo_M100()
        except Exception as e:
            log_erro('.__moodificacoes_grupo_M100',e )
            
        try:
            self.__correcao_valores_Bloco_A100_e_A170()
        except Exception as e:
            log_erro('.__correcao_valores_Bloco_A100_e_A170',e )
            
        try:
            self.__alteracao_F600_Col_6()
        except Exception as e:
            log_erro('.__alteracao_F600_Col_6',e )
        # Remoção
        
            
        try:
            self.__remove_C500()
        except Exception as e:
            log_erro('.__remove_C500',e )
            
        try:
            self.__remove_C50()
        except Exception as e:
            log_erro('.__remove_C50',e )
        #Correção e recaculos

        
            
        try:
            self.__recalculando_aliquota_M200_e_M600()
        except Exception as e:
            log_erro('__recalculando_aliquota_M200_e_M600',e )
            
        try:
            self.__recalculando_aliquota_M210_e_M610()
        except Exception as e:
            log_erro('__recalculando_aliquota_M210_e_M610',e )
            
        try:
            self.__zerando_valores_M500()
        except Exception as e:
            log_erro('__zerando_valores_M500',e )
            
        try:
            self.__zerando_valores_M600()
        except Exception as e:
            log_erro('__zerando_valores_M600',e )
        # ''' Até aqui são as alterações que geraram os resultados dos arquivos para GE e Máxima '''

        # '''  A partir daqui são alterações novas da Brasfort '''
        
        
            
        try:
            self.__recaculcalndo_aliquota_C170_Col2_0()
        except Exception as e:
            log_erro('__recaculcalndo_aliquota_C170_Col2_0',e )
            
        try:
            self.__alteracao_aliquota_C170()
        except Exception as e:
            log_erro('__alteracao_aliquota_C170',e )
            
        try:
            self.__remove_m205_repetida()
        except Exception as e:
            log_erro('__remove_m205_repetida',e )
            
        try:
            self.__remove_m605_repetida()
        except Exception as e:
            log_erro('__remove_m605_repetida',e )

        
        try:
            self.__somatorio_agragado_valores_c170_m200()
        except Exception as e:
            log_erro('__somatorio_agragado_valores_c170_m200',e )
        try:
            self.__somatorio_agragado_valores_c170_m600()
        except Exception as e:
            log_erro('__somatorio_agragado_valores_c170_m600',e )
            
        try:
            self.__agregado_F600_M200()
        except Exception as e:
            log_erro('__agregado_F600_M200',e )
        try:
            self.__agregado_F600_M600()
        except Exception as e:
            log_erro('__agregado_F600_M600',e )
        
        try:
            self.__removendo_m210_duplicada_e_ajustando_valores()
        except Exception as e:
            log_erro('__removendo_m210_duplicada_e_ajustando_valores',e )
        try:
            self.__removendo_m610_duplicada_e_ajustando_valores()
        except Exception as e:
            log_erro('__removendo_m610_duplicada_e_ajustando_valores',e )
            
        
        try:
            self.__valor_final_ultima_col_m210()
        except Exception as e:
            log_erro('__valor_final_ultima_col_m210',e )
        try:
            self.__valor_final_ultima_col_m610()
        except Exception as e:
            log_erro('__valor_final_ultima_col_m610',e )

       # ''' A partir daqui serão alterações vindas da empresa Quality Max'''

        
        try:
            self.__resolucao_M205_e_M200()
        except Exception as e:
            log_erro('__resolucao_M205_e_M200',e )
        try:
            self.__resolucao_M605_e_M600()
        except Exception as e:
            log_erro('__resolucao_M605_e_M600',e )
        try:
            self.__remove_C100_Col1_0()
        except Exception as e:
            log_erro('__remove_C100_Col1_0',e )
        try:
            self.__ajustando_duplicadas_F600()
        except Exception as e:
            log_erro('__ajustando_duplicadas_F600',e )
        # ''' A partir daqui são novas adicionais feitas coma arquivo da Brasfort ''''
        
        
        try:
            self.__somatorio_agragado_valores_A170_m200()
        except Exception as e:
            log_erro('__somatorio_agragado_valores_A170_m200',e )

        try:
            self.__retirando_cnpjs_duplicados_M630()
        except Exception as e:
            log_erro('__retirando_cnpjs_duplicados_M630',e )

        try:
            self.__retirando_cnpjs_duplicados_m230()
        except Exception as e:
            log_erro('__retirando_cnpjs_duplicados_m230',e )

        try:
            self.__limpando_colunas_m230_e_re_calculando_aliquota()
        except Exception as e:
            log_erro('__limpando_colunas_m230_e_re_calculando_aliquota',e )

        try:
            self.__limpando_colunas_m630_e_re_calculando_aliquota()
        except Exception as e:
            log_erro('__limpando_colunas_m630_e_re_calculando_aliquota',e )

        try:
            self.__correcao_de_capos_M300()
        except Exception as e:
            log_erro('__correcao_de_capos_M300',e )

        try:
            self.__correcao_de_capos_M700()
        except Exception as e:
            log_erro('__correcao_de_capos_M700',e )

        try:
            self.__ajuste_valores_base_M700_M610_m200()
        except Exception as e:
            log_erro('__ajuste_valores_base_M700_M610_m200',e )

        try:
            self.__ajuste_valores_base_m300_m210_m200()
        except Exception as e:
            log_erro('__ajuste_valores_base_m300_m210_m200',e )

        try:
            self.__valores_compilados_finais_m200()
        except Exception as e:
            log_erro('__valores_compilados_finais_m200',e )

        try:
            self.__valores_compilados_finais_m600()
        except Exception as e:
            log_erro('__valores_compilados_finais_m600',e )

        try:
            self.__calculos_finais_M200()
        except Exception as e:
            log_erro('__calculos_finais_M200',e )

        try:
            self.__calculos_finais_M600()
        except Exception as e:
            log_erro('__calculos_finais_M600',e )

        try:
            self.__passando_valor_m600_para_m605()
        except Exception as e:
            log_erro('__passando_valor_m600_para_m605',e )

        try:
            self.__passando_valor_m200_para_205()
        except Exception as e:
            log_erro('__passando_valor_m200_para_205',e )



