import streamlit as st
import os
import sys
import pandas as pd 
import numpy as np
import base64




st.set_page_config(layout='wide')
background_image ="Untitleddesign.jpg"
st.markdown(
     f"""
     <iframe src="data:image/jpg;base64,{base64.b64encode(open(background_image, 'rb').read()).decode(

    )}" style="width:4000px;height:3000px;position: absolute;top:-3vh;right:-1250px;opacity: 0.5;background-size: cover;background-position: center;"></iframe>
     """,
     unsafe_allow_html=True )

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from TratamentoTXT.sped import SpedProcessor

class TabelasPISConfins(SpedProcessor):
    
    def __init__(self):
        super().__init__()
        self.tabela_base_valors = pd.DataFrame({ 'Competência': []})
        self.col1,self.col2 = st.columns(2)

    def base_valores(self) -> pd.DataFrame:

        def mesclando_dados(df2,columna_original: str, columna_nova:str, colunas_base_filtro:str)-> pd.DataFrame:

            self.tabela_base_valors = pd.merge(self.tabela_base_valors,
                           df2,
                           left_on='Competência',
                            right_on='Data').rename(columns={columna_original:columna_nova})
            
            self.tabela_base_valors[columna_nova] = self.tabela_base_valors[columna_nova].astype(str).str.replace(',','.').astype(float)
            self.tabela_base_valors = self.tabela_base_valors.drop(columns=[colunas_base_filtro,'Data'])
        
            return self.tabela_base_valors

        
        def verificacao_dados_vazios(dataframe_filtrado: pd.DataFrame,filtro:str , coluna_utilizada: str,nome_coluna_vazia:str)->pd.DataFrame:
            dataframe_filtrado = dataframe_filtrado[dataframe_filtrado[coluna_utilizada] == filtro ]
            if dataframe_filtrado[coluna_utilizada].empty:
                dataframe_filtrado = self.arquivo_m210.iloc[:,[1,-1]]
                dataframe_filtrado[nome_coluna_vazia] = 0
                
            return dataframe_filtrado

       # Econtrando dados nos dataframes primearios(M200, M600, M210, M610)
        data = self.arquivo_m210["Data"].values

        base_calculo_nao_cumulativo = self.arquivo_m210.iloc[:,[1,6,-1]]
        base_calculo_cumulativo = self.arquivo_m210.iloc[:,[1,6,-1]]
        base_calculo_rf = self.arquivo_m210.iloc[:,[1,6,-1]]

        base_calculo_cumulativo['Vlr Base Cálculo Contribuição Após Ajustes'] = base_calculo_cumulativo['Vlr Base Cálculo Contribuição Após Ajustes'].replace('','0')


        ajuste_acrescimo_pis = self.arquivo_m210.iloc[:,[12,-1]]
        ajuste_acrescimo_confins = self.arquivo_m610.iloc[:,[12,-1]]

        
        retencoes_pis = self.arquivo_m200.iloc[:,[5,9,-1]]
        retencoes_pis['Vlr Retido Fonte Cumulativa Deduzida Período'] = retencoes_pis['Vlr Retido Fonte Cumulativa Deduzida Período'].astype(str).str.replace(',','.').astype(float)
        retencoes_pis['Vlr Retido Fonte NC Deduzida Período'] = retencoes_pis['Vlr Retido Fonte NC Deduzida Período'].astype(str).str.replace(',','.').astype(float)
        retencoes_pis['Renteções_pis'] = (retencoes_pis['Vlr Retido Fonte NC Deduzida Período'] + 
                                                    retencoes_pis['Vlr Retido Fonte Cumulativa Deduzida Período'])
        
        retencoes_pis = retencoes_pis.iloc[:,[-1,-2]] 

        retencoes_confins = self.arquivo_m600.iloc[:,[5,9,-1]]
        retencoes_confins['Vlr Retido Fonte Cumulativa Deduzida Período'] = retencoes_confins['Vlr Retido Fonte Cumulativa Deduzida Período'].astype(str).str.replace(',','.').astype(float)
        retencoes_confins['Vlr Retido Fonte NC Deduzida Período'] = retencoes_confins['Vlr Retido Fonte NC Deduzida Período'].astype(str).str.replace(',','.').astype(float)
        retencoes_confins['Renteções_confins'] = (retencoes_confins['Vlr Retido Fonte NC Deduzida Período'] + 
                                                    retencoes_confins['Vlr Retido Fonte Cumulativa Deduzida Período'])                                           
        retencoes_confins = retencoes_confins.iloc[:,[-1,-2]]


        base_calculo_nao_cumulativo = verificacao_dados_vazios(base_calculo_nao_cumulativo,'01',1,'BASE DE CALCULO Não Cumulativo')
        base_calculo_cumulativo = verificacao_dados_vazios(base_calculo_cumulativo, '51', 1,'BASE DE CALCULO Cumulativo')
        base_calculo_rf = verificacao_dados_vazios(base_calculo_rf, '02', 1,'BASE DE CALCULO Receita Financeira')



        # Formando dataframe para base de calculo
        if len(data) != len(self.tabela_base_valors):
            self.tabela_base_valors = self.tabela_base_valors.reindex(range(len(data)))

        self.tabela_base_valors['Competência'] = data


        self.tabela_base_valors = mesclando_dados(base_calculo_nao_cumulativo,
                                                   'Vlr Base Cálculo Contribuição Após Ajustes',
                                                   'BASE DE CALCULO Não Cumulativo',1)

        self.tabela_base_valors = mesclando_dados(base_calculo_cumulativo,
                                                  'Vlr Base Cálculo Contribuição Após Ajustes',
                                                    'BASE DE CALCULO Cumulativo',1)
        
        self.tabela_base_valors = mesclando_dados(base_calculo_rf,'Vlr Base Cálculo Contribuição Após Ajustes'
                                                        ,'BASE DE CALCULO Receita Financeira',1)
        



        self.tabela_base_valors['Débito PIS Não Cumulativo 1,65%'] = np.where(
            self.tabela_base_valors['BASE DE CALCULO Não Cumulativo'] == 0,0, self.tabela_base_valors['BASE DE CALCULO Não Cumulativo'] * 0.0165)
        self.tabela_base_valors['Débito COFINS Não Cumulativo 7,60%'] = np.where(
            self.tabela_base_valors['BASE DE CALCULO Não Cumulativo'] == 0,0, self.tabela_base_valors['BASE DE CALCULO Não Cumulativo'] * 0.076)
                

    
        self.tabela_base_valors['Débito PIS Cumulativo 0,65%'] = np.where(
            self.tabela_base_valors['BASE DE CALCULO Cumulativo'] == 0,0, self.tabela_base_valors['BASE DE CALCULO Cumulativo'] * 0.0065)        
        self.tabela_base_valors['Débito COFINS Cumulativo 3,00%'] = np.where(
            self.tabela_base_valors['BASE DE CALCULO Cumulativo'] == 0,0, self.tabela_base_valors['BASE DE CALCULO Cumulativo'] * 0.03)



        self.tabela_base_valors['Débito PIS Receita Financeira 0,65%'] = np.where(
            self.tabela_base_valors['BASE DE CALCULO Receita Financeira'] == 0,0, self.tabela_base_valors['BASE DE CALCULO Receita Financeira'] * 0.0065)       
        self.tabela_base_valors['Débito COFINS Cumulativo 4,00%'] = np.where(
            self.tabela_base_valors['BASE DE CALCULO Receita Financeira'] == 0,0, self.tabela_base_valors['BASE DE CALCULO Receita Financeira'] * 0.04)

        
        self.tabela_base_valors['Somatorio'] = self.tabela_base_valors[
            [
                'Débito PIS Não Cumulativo 1,65%',
                'Débito COFINS Não Cumulativo 7,60%',
                'Débito PIS Cumulativo 0,65%',
                'Débito COFINS Cumulativo 3,00%',
                'Débito PIS Receita Financeira 0,65%',
                'Débito COFINS Cumulativo 4,00%']].sum(axis=1)

        self.tabela_base_valors['Validador Não Cumulativo - %'] = self.tabela_base_valors.apply(
            lambda row: ((row['Débito PIS Não Cumulativo 1,65%'] + row['Débito COFINS Não Cumulativo 7,60%']) / row['BASE DE CALCULO Não Cumulativo']) * 100
            if row['BASE DE CALCULO Não Cumulativo'] != 0 else 0,  axis=1)

        self.tabela_base_valors['Validador Cumulativo - %'] = self.tabela_base_valors.apply(
            lambda row: ((row['Débito PIS Cumulativo 0,65%'] + row['Débito COFINS Cumulativo 3,00%']) / row['BASE DE CALCULO Cumulativo']) * 100
            if row['BASE DE CALCULO Cumulativo'] != 0 else 0, axis=1)
        
        self.tabela_base_valors['Validador RF - %'] = self.tabela_base_valors.apply(
            lambda row: ((row['Débito PIS Receita Financeira 0,65%'] + row['Débito COFINS Cumulativo 4,00%']) / row['BASE DE CALCULO Receita Financeira']) * 100
            if row['BASE DE CALCULO Receita Financeira'] != 0 else 0, axis=1)

        self.tabela_base_valors = pd.merge(self.tabela_base_valors,ajuste_acrescimo_pis, left_on='Competência', right_on='Data').iloc[:,:-1].rename(columns={'Vlr Total Ajustes Redução':'Ajuste de acréscimo PIS'})
        
        self.tabela_base_valors['Ajuste de acréscimo PIS'] = self.tabela_base_valors['Ajuste de acréscimo PIS'].replace('','0').fillna(0).replace(np.nan,0)
        self.tabela_base_valors['Ajuste de acréscimo PIS'] = self.tabela_base_valors['Ajuste de acréscimo PIS'].astype(str).str.replace(',','.').astype(float)
        
        self.tabela_base_valors = pd.merge(self.tabela_base_valors,ajuste_acrescimo_confins, left_on='Competência', right_on='Data').iloc[:,:-1].rename(columns={'Vlr Total Ajustes Redução':'Ajuste de acréscimo CONFINS'})

        self.tabela_base_valors['Ajuste de acréscimo CONFINS'] = self.tabela_base_valors['Ajuste de acréscimo CONFINS'].replace('','0').fillna(0).replace(np.nan,0)
        self.tabela_base_valors['Ajuste de acréscimo CONFINS'] = self.tabela_base_valors['Ajuste de acréscimo CONFINS'].astype(str).str.replace(',','.').astype(float)
  

        self.tabela_base_valors = pd.merge(self.tabela_base_valors,retencoes_pis, left_on='Competência', right_on='Data').iloc[:,:-1]
        self.tabela_base_valors = pd.merge(self.tabela_base_valors,retencoes_confins, left_on='Competência', right_on='Data').iloc[:,:-1]

        credito_pis = self.arquivo_m200.iloc[:,[2,-1]]
        credito_pis['Vlr Crédito Descontado Período'] = credito_pis['Vlr Crédito Descontado Período'].astype(str).str.replace(',','.').astype(float)
        self.tabela_base_valors = pd.merge(self.tabela_base_valors,credito_pis, left_on='Competência', right_on='Data').iloc[:,:-1].rename(
                                                                                                                        columns={
                                                                                                                            'Vlr Crédito Descontado Período':'Crédito PIS'})
        credito_confins = self.arquivo_m600.iloc[:,[2,-1]]
        credito_confins['Vlr Crédito Descontado Período'] = credito_confins['Vlr Crédito Descontado Período'].astype(str).str.replace(',','.').astype(float)
        self.tabela_base_valors = pd.merge(self.tabela_base_valors,credito_confins, left_on='Competência', right_on='Data').iloc[:,:-1].rename(
                                                                                                                        columns={
                                                                                                                            'Vlr Crédito Descontado Período':'Crédito CONFINS'})
      
        
        self.tabela_base_valors['Somatorio_'] = (self.tabela_base_valors['Ajuste de acréscimo PIS'] + self.tabela_base_valors['Ajuste de acréscimo CONFINS']+ 
                                                self.tabela_base_valors['Renteções_pis']+ self.tabela_base_valors['Renteções_confins']+ 
                                                self.tabela_base_valors['Crédito PIS'] + self.tabela_base_valors['Crédito CONFINS'])

        self.tabela_base_valors['PIS A PAGAR EFD'] = (self.tabela_base_valors['Débito PIS Não Cumulativo 1,65%'] + self.tabela_base_valors['Débito PIS Cumulativo 0,65%'] +
                                                        self.tabela_base_valors['Débito PIS Receita Financeira 0,65%'] + self.tabela_base_valors['Ajuste de acréscimo PIS'] -
                                                        self.tabela_base_valors['Renteções_pis'] - self.tabela_base_valors['Crédito PIS'])

        self.tabela_base_valors['COFINS A PAGAR EFD'] = (self.tabela_base_valors['Débito COFINS Não Cumulativo 7,60%'] + self.tabela_base_valors['Débito COFINS Cumulativo 3,00%'] +
                                                        self.tabela_base_valors['Débito COFINS Cumulativo 4,00%'] + self.tabela_base_valors['Ajuste de acréscimo CONFINS'] -
                                                        self.tabela_base_valors['Renteções_confins'] - self.tabela_base_valors['Crédito CONFINS'])

        self.tabela_base_valors['Imposto Apurado'] = self.tabela_base_valors['PIS A PAGAR EFD'] + self.tabela_base_valors['COFINS A PAGAR EFD']

        self.tabela_base_valors['Validação'] = (self.tabela_base_valors['Somatorio'] - self.tabela_base_valors['Somatorio_'] - self.tabela_base_valors['Imposto Apurado'])

        self.tabela_base_valors = self.tabela_base_valors.drop_duplicates(subset=['Competência'], keep='first') 

        self.tabela_base_valors['Competência'] = self.tabela_base_valors['Competência'].astype(str)

        # Adicionar os hífens ao formato 'dd-mm-aaaa'
        self.tabela_base_valors['Competência'] = self.tabela_base_valors['Competência'].str.slice(0, 2) + '-' + \
                                                        self.tabela_base_valors['Competência'].str.slice(2, 4) + '-' + \
                                                        self.tabela_base_valors['Competência'].str.slice(4, 8)

        self.tabela_base_valors['Competência'] = pd.to_datetime(self.tabela_base_valors['Competência'], format='%d-%m-%Y')
        self.tabela_base_valors.sort_values(by='Competência',inplace=True)


        with self.col1:
            st.subheader('Tabela Base de Valores')
            st.dataframe(self.tabela_base_valors)

    

    def calculos_valores_futuros(self,tabela_base_para_calculos_futuros):
                
        tabela_base_para_calculos_futuros['Débito PIS Não Cumulativo 1,65%'] = np.where(
            tabela_base_para_calculos_futuros['BASE DE CALCULO Não Cumulativo'] == 0,0, tabela_base_para_calculos_futuros['BASE DE CALCULO Não Cumulativo'] * 0.0165)
        tabela_base_para_calculos_futuros['Débito COFINS Não Cumulativo 7,60%'] = np.where(
            tabela_base_para_calculos_futuros['BASE DE CALCULO Não Cumulativo'] == 0,0, tabela_base_para_calculos_futuros['BASE DE CALCULO Não Cumulativo'] * 0.076)
                

    
        tabela_base_para_calculos_futuros['Débito PIS Cumulativo 0,65%'] = np.where(
            tabela_base_para_calculos_futuros['BASE DE CALCULO Cumulativo'] == 0,0, tabela_base_para_calculos_futuros['BASE DE CALCULO Cumulativo'] * 0.0065)        
        tabela_base_para_calculos_futuros['Débito COFINS Cumulativo 3,00%'] = np.where(
            tabela_base_para_calculos_futuros['BASE DE CALCULO Cumulativo'] == 0,0, tabela_base_para_calculos_futuros['BASE DE CALCULO Cumulativo'] * 0.03)



        tabela_base_para_calculos_futuros['Débito PIS Receita Financeira 0,65%'] = np.where(
            tabela_base_para_calculos_futuros['BASE DE CALCULO Receita Financeira'] == 0,0, tabela_base_para_calculos_futuros['BASE DE CALCULO Receita Financeira'] * 0.0065)       
        tabela_base_para_calculos_futuros['Débito COFINS Cumulativo 4,00%'] = np.where(
            tabela_base_para_calculos_futuros['BASE DE CALCULO Receita Financeira'] == 0,0, tabela_base_para_calculos_futuros['BASE DE CALCULO Receita Financeira'] * 0.04)
       
        tabela_base_para_calculos_futuros['Somatorio'] = tabela_base_para_calculos_futuros[
            [
                'Débito PIS Não Cumulativo 1,65%',
                'Débito COFINS Não Cumulativo 7,60%',
                'Débito PIS Cumulativo 0,65%',
                'Débito COFINS Cumulativo 3,00%',
                'Débito PIS Receita Financeira 0,65%',
                'Débito COFINS Cumulativo 4,00%']].sum(axis=1)

        tabela_base_para_calculos_futuros['Validador Não Cumulativo - %'] = tabela_base_para_calculos_futuros.apply(
            lambda row: ((row['Débito PIS Não Cumulativo 1,65%'] + row['Débito COFINS Não Cumulativo 7,60%']) / row['BASE DE CALCULO Não Cumulativo']) * 100
            if row['BASE DE CALCULO Não Cumulativo'] != 0 else 0,  axis=1)

        tabela_base_para_calculos_futuros['Validador Cumulativo - %'] = tabela_base_para_calculos_futuros.apply(
            lambda row: ((row['Débito PIS Cumulativo 0,65%'] + row['Débito COFINS Cumulativo 3,00%']) / row['BASE DE CALCULO Cumulativo']) * 100
            if row['BASE DE CALCULO Cumulativo'] != 0 else 0, axis=1)
        
        tabela_base_para_calculos_futuros['Validador RF - %'] = tabela_base_para_calculos_futuros.apply(
            lambda row: ((row['Débito PIS Receita Financeira 0,65%'] + row['Débito COFINS Cumulativo 4,00%']) / row['BASE DE CALCULO Receita Financeira']) * 100
            if row['BASE DE CALCULO Receita Financeira'] != 0 else 0, axis=1)

        tabela_base_para_calculos_futuros['Somatorio_'] = tabela_base_para_calculos_futuros[['Ajuste de acréscimo PIS' ,
                                                                                             'Ajuste de acréscimo CONFINS',
                                                                                            'Renteções_pis','Renteções_confins', 
                                                                                            'Crédito PIS' ,'Crédito CONFINS']].sum(axis=1)

        tabela_base_para_calculos_futuros['PIS A PAGAR EFD'] = (tabela_base_para_calculos_futuros['Débito PIS Não Cumulativo 1,65%'] + tabela_base_para_calculos_futuros['Débito PIS Cumulativo 0,65%'] +
                                                        tabela_base_para_calculos_futuros['Débito PIS Receita Financeira 0,65%'] - tabela_base_para_calculos_futuros['Ajuste de acréscimo PIS'] -
                                                        tabela_base_para_calculos_futuros['Renteções_pis'] - tabela_base_para_calculos_futuros['Crédito PIS'])

        tabela_base_para_calculos_futuros['COFINS A PAGAR EFD'] = (tabela_base_para_calculos_futuros['Débito COFINS Não Cumulativo 7,60%'] + tabela_base_para_calculos_futuros['Débito COFINS Cumulativo 3,00%'] +
                                                        tabela_base_para_calculos_futuros['Débito COFINS Cumulativo 4,00%'] - tabela_base_para_calculos_futuros['Ajuste de acréscimo CONFINS'] -
                                                        tabela_base_para_calculos_futuros['Renteções_confins'] - tabela_base_para_calculos_futuros['Crédito CONFINS'])

        tabela_base_para_calculos_futuros['Imposto Apurado'] = tabela_base_para_calculos_futuros['PIS A PAGAR EFD'] + tabela_base_para_calculos_futuros['COFINS A PAGAR EFD']

        tabela_base_para_calculos_futuros['Validação'] = (tabela_base_para_calculos_futuros['Somatorio'] - tabela_base_para_calculos_futuros['Somatorio_'] - tabela_base_para_calculos_futuros['Imposto Apurado'])
    
        return tabela_base_para_calculos_futuros


    def valores_futuros(self):

        tabela_base_para_calculos_futuros = self.tabela_base_valors.copy()

        colunas_media_por_quatro = ['Crédito PIS', 'Crédito CONFINS']

        tabela_base_para_calculos_futuros.reset_index(drop=True, inplace=True)


        tabela_base_para_calculos_futuros = tabela_base_para_calculos_futuros.iloc[[-4,-3,-2,-1], :].reset_index(drop=True)

        tabela_base_para_calculos_futuros['Competência'] = tabela_base_para_calculos_futuros['Competência'].astype(str)

        
        nova_linha = {col: '' for col in tabela_base_para_calculos_futuros.columns}  
        tabela_base_para_calculos_futuros.loc[len(tabela_base_para_calculos_futuros)] = nova_linha
        


        colunas = [
        'BASE DE CALCULO Não Cumulativo',     
        'BASE DE CALCULO Cumulativo',         
        'BASE DE CALCULO Receita Financeira', 
        'Débito PIS Não Cumulativo 1,65%',    
        'Débito COFINS Não Cumulativo 7,60%', 
        'Débito PIS Cumulativo 0,65%',        
        'Débito COFINS Cumulativo 3,00%',     
        'Débito PIS Receita Financeira 0,65%',
        'Débito COFINS Cumulativo 4,00%',     
        'Somatorio',                          
        'Validador Não Cumulativo - %',       
        'Validador Cumulativo - %',           
        'Validador RF - %',                   
        'Ajuste de acréscimo PIS',            
        'Ajuste de acréscimo CONFINS',        
        'Renteções_pis',                      
        'Renteções_confins',                  
        'Crédito PIS',                        
        'Crédito CONFINS',                    
        'Somatorio_',                         
        'PIS A PAGAR EFD',                    
        'COFINS A PAGAR EFD',                 
        'Imposto Apurado',                    
        'Validação']
        

        for coluna in colunas:
            if coluna in tabela_base_para_calculos_futuros.columns:
                
                tabela_base_para_calculos_futuros[coluna] = (
                    tabela_base_para_calculos_futuros[coluna]
                    .replace('', 0)  
                    .fillna(0)       
                    .astype(float)   
                )
            else:
                print(f"Coluna '{coluna}' não encontrada no DataFrame.")
                print(tabela_base_para_calculos_futuros.info())

        tabela_base_para_calculos_futuros = tabela_base_para_calculos_futuros.reset_index(drop=True)                
        colunas_base_calculos = [
        'BASE DE CALCULO Não Cumulativo',     
        'BASE DE CALCULO Cumulativo',         
        'BASE DE CALCULO Receita Financeira', 
       
        'Ajuste de acréscimo PIS',            
        'Ajuste de acréscimo CONFINS',        
        'Renteções_pis',                      
        'Renteções_confins',                  
        'Crédito PIS',                        
        'Crédito CONFINS'] 

        
        for i in colunas_base_calculos:
            tabela_base_para_calculos_futuros.at[4,i] = (tabela_base_para_calculos_futuros.at[0,i]+tabela_base_para_calculos_futuros.at[2,i]+
                                                          tabela_base_para_calculos_futuros.at[3,i]+tabela_base_para_calculos_futuros.at[1,i])/4

        tabela_base_para_calculos_futuros = self.calculos_valores_futuros(tabela_base_para_calculos_futuros)

        ultima_linha = tabela_base_para_calculos_futuros.iloc[[-1]]
        for _ in range(59):
            tabela_base_para_calculos_futuros = pd.concat([tabela_base_para_calculos_futuros, ultima_linha], ignore_index=True)
        
        # for coluna in colunas_media_por_quatro:
        #     for linha_atual in range(4, len(tabela_base_para_calculos_futuros)):
        #         tabela_base_para_calculos_futuros.at[linha_atual, coluna] = tabela_base_para_calculos_futuros.loc[
        #             linha_atual - 4:linha_atual - 1, coluna
        #         ].mean()
                
        tabela_base_para_calculos_futuros = self.calculos_valores_futuros(tabela_base_para_calculos_futuros)

        tabela_base_para_calculos_futuros['Competência'] = pd.to_datetime(tabela_base_para_calculos_futuros['Competência'])
        ultima_data = tabela_base_para_calculos_futuros['Competência'].max()

        # Preencher os valores NaN com os próximos meses
        for i in range(len(tabela_base_para_calculos_futuros)):
            if pd.isna(tabela_base_para_calculos_futuros.loc[i, 'Competência']):
                ultima_data += pd.DateOffset(months=1)
                tabela_base_para_calculos_futuros.loc[i, 'Competência'] = ultima_data

            

        self.tabela_valores_futuros = tabela_base_para_calculos_futuros.copy()


        with self.col1:
            st.subheader('Tabela para calculos futuros')
            st.dataframe(tabela_base_para_calculos_futuros)

    def tabela_agregada(self):
        tabela_final = pd.concat([self.tabela_base_valors, self.tabela_valores_futuros], ignore_index=True).drop_duplicates(subset=['Competência'], keep='last').rename(
                                    columns={'Competência': 'Período',
                                             'BASE DE CALCULO Não Cumulativo':'Receita Não cumulativa',
                                             'BASE DE CALCULO Cumulativo':'Receita cumulativa',
                                             'BASE DE CALCULO Receita Financeira':'Receita Financeira',
                                             'Somatorio_':'Crédito/ Retenções+ ajustes  EFD Contribuições'
                                             })

        tabela_final['Contribuições Não Cumulativas'] = tabela_final['Receita Não cumulativa'] * 0.0925
        tabela_final['Contribuições Cumulativas'] = tabela_final['Receita cumulativa'] * 0.0365
        tabela_final['Contribuições RF'] = tabela_final['Receita Financeira'] * 0.0465
        tabela_final['Validador - % 9,25 - 12,90 - 13,90% - 17,55%'] = ((tabela_final['Contribuições Não Cumulativas']/tabela_final['Receita Não cumulativa'])+(tabela_final['Contribuições RF']/tabela_final['Receita Financeira']))* 100
        tabela_final['Imposto apurado'] = tabela_final[['Contribuições Não Cumulativas','Contribuições Cumulativas',
                                                        'Contribuições RF']].sum(axis=1) - tabela_final['Crédito/ Retenções+ ajustes  EFD Contribuições']
        tabela_final['Débito  cumulativo'] = tabela_final[['Receita Não cumulativa','Receita cumulativa']].sum(axis=1) * 0.0365
        tabela_final['Validador -3,65%'] = (tabela_final['Débito  cumulativo'] / (tabela_final[['Receita Não cumulativa','Receita cumulativa']].sum(axis=1))) * 100
        tabela_final[' Retenções+Ajustes'] = tabela_final[['Renteções_pis','Renteções_confins']].sum(axis=1) - tabela_final['Ajuste de acréscimo CONFINS'] - tabela_final['Ajuste de acréscimo PIS']
        tabela_final['Imposto apurado_'] = tabela_final['Débito  cumulativo'] - tabela_final[' Retenções+Ajustes']
        tabela_final['Ganho Econômico'] = tabela_final['Imposto apurado'] - tabela_final['Imposto apurado_']
        tabela_final['Sobra de retenção'] = np.where(tabela_final[' Retenções+Ajustes']>tabela_final['Débito  cumulativo'],
        tabela_final['Imposto apurado_'],0)
        
        
        tabela_final['Ano'] = pd.to_datetime(tabela_final['Período']).dt.year
        tabela_final = tabela_final.iloc[:,[0,1,2,3,25,26,27,28,20,29,30,31,32,33,34,35,-1]]
        tabela_agregada = tabela_final.groupby('Ano').sum(numeric_only=True).reset_index()

        # Adicionar linha de total geral
        total_geral = tabela_agregada.sum(numeric_only=True, axis=0)
        total_geral['Ano'] = 'Total Geral'
        tabela_agregada = pd.concat([tabela_agregada, total_geral.to_frame().T], ignore_index=True)

        with self.col2:
            st.subheader('Tabela Agregada')
            st.dataframe(tabela_final)

            st.subheader('Tabela Agregada por Ano')
            st.dataframe(tabela_agregada)

        
        tabela_comparativa = tabela_agregada.copy()

        tabela_comparativa = tabela_comparativa.iloc[:,[4,5,6,9,10,12,13,14]] 
        tabela_comparativa['Ganho Ecônomico RF'] = tabela_comparativa['Contribuições RF']

        print(tabela_comparativa.info())

        # tabela_comparativa = tabela_comparativa.rename(columns={
        #     'Contribuições Não Cumulativas': 'Contribuições Não Cumulativas',
        #     'Contribuições Cumulativas':'Contribuições  Cumulativas',
        #     'Contribuições RF' : 'Contribuições Receita Financeira',
        #     }).iloc[:,[0,1,2,3,9,10,12,13]]
        #tabela_comparativa['Ganho Econômico'] = tabela_comparativa['Imposto apurado'] - tabela_comparativa['Imposto apurado_']
        #tabela_comparativa['Ganho Econômico RF'] = tabela_comparativa['Contribuições Receita Financeira']
        st.subheader('Tabela Antes e Depois da aplicação')
        st.dataframe(tabela_comparativa)
        
        print(tabela_final.info())

    def main(self):
        try:
            uploaded_files = st.sidebar.file_uploader("Escolha os arquivos SPED", type=['txt'], accept_multiple_files=True)
            file_paths = []
            if uploaded_files:


                for uploaded_file in uploaded_files:
                    file_path = uploaded_file.name
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    file_paths.append(file_path)

            for file_path in file_paths:
                self.lendoELimpandoDadosSped(file_path)
                self.guardando_tabelas()
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')            
            print(f"Número de arquivos a serem processados: {len(file_paths)}")       
                    
                
            m200, m600, m210, m610 = self.tabelando_dados()
            
            # st.subheader('M210')
            # st.dataframe(m210)
            self.base_valores()
            self.valores_futuros()
            self.tabela_agregada()

            # Remover os arquivos após o processamento
            for file_path in file_paths:
                os.remove(file_path)
        except Exception as e:
            print('Erro:', e)



if __name__ == '__main__':


    main = TabelasPISConfins()
    main.main()  
