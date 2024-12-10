import pandas as pd
import streamlit as st
import os

class SpedProcessor:
    def __init__(self):
        self.listaM210 = []
        self.listaM600 = []
        self.listaM200 = []
        self.listaM610 = []

    def lendoELimpandoDadosSped(self, file_path):
        data = []
        if file_path is None or not os.path.exists(file_path):
            raise ValueError("Arquivo não encontrado.")
        with open(file_path, 'r', encoding='latin-1') as file:
            for linha in file:
                linha = linha.strip()
                if linha.startswith('|'):
                    valores = linha.split('|')[1:]
                    data.append(valores)

        self.df = pd.DataFrame(data)
        
        self.df['Data'] = self.df.iloc[0, 5]
        return self.df
    
    def guardando_tabelas(self):
        m210 = self.df[self.df[0] == 'M210']
        m600 = self.df[self.df[0] == 'M600']
        m200 = self.df[self.df[0] == 'M200']
        m610 = self.df[self.df[0] == 'M610']
        
        self.listaM200.append(m200)
        self.listaM600.append(m600)
        self.listaM210.append(m210)
        self.listaM610.append(m610)

    def tabelando_dados(self):
        m200columnns = {1:'Vlr Total Contribuição NC Período',
                        2: 'Vlr Crédito Descontado Período',
                        3:'Vlr Credito Descontado Período Anterior',
                        4:'Vlr Contribuição NC Devida',
                        5:'Vlr Retido Fonte NC Deduzida Período',
                        6:'Vlr Outras Deduções NC Período',
                        7:'Vlr Contribuição NC Recolher',
                        8:'Vlr Retido Fonte Cumulativa Período',
                        9:'Vlr Retido Fonte Cumulativa Deduzida Período',
                        10:'Vlr Outras Deduções Cumulativa Período',
                        11:'Vlr Contribuição Cumulativa Recolher',
                        12:'Vlr Total Contribuição Recolher Período',
                        }
        m600columns = {1:'Vlr Total Contribuição NC Período',
                        2:'Vlr Crédito Descontado Período',
                        3:'Vlr Credito Descontado Período Anterior',
                        4:'Vlr Contribuição NC Devida',
                        5:'Vlr Retido Fonte NC Deduzida Período',
                        6:'Vlr Outras Deduções NC Período',
                        7:'Vlr Contribuição NC Recolher',
                        8:'Vlr Total Contribuição Cumulativa Período',
                        9:'Vlr Retido Fonte Cumulativa Deduzida Período',
                        10:'Vlr Outras Deduções Cumulativa Período',
                        11:'Vlr Contribuição Cumulativa Recolher',
                        12:'Vlr Total Contribuição Recolher Período'}
        m210columns = {
                       2:'Vlr Receita Bruta',
                       3:'Vlr Base Cálculo Contribuição Antes Ajustes',
                       4:'Vlr Total Ajustes Acréscimo Base Cálculo',
                       5:'Vlr Total Ajustes Redução Base Cálculo',
                       6:'Vlr Base Cálculo Contribuição Após Ajustes',
                       7:'Alíquota PIS',
                       8:'Qtde Base Cálculo PIS',
                       9:'Qtde Alíquota PIS',
                       10:'Vlr Total Contribuição Apurada',
                       11:'Vlr Total Ajustes Acréscimo',
                       12:'Vlr Total Ajustes Redução',
                       13:'Vlr Contribuição Diferir Período',
                       14:'Vlr Contribuição Diferida Períodos Anteriores',
                       15:'Vlr Total Contribuição Período'
                       }
        m610columns = {
                       2:'Vlr Receita Bruta',
                       3:'Vlr Base Cálculo Contribuição Antes Ajustes',
                       4:'Vlr Total Ajustes Acréscimo Base Cálculo',
                       5:'Vlr Total Ajustes Redução Base Cálculo',
                       6:'Vlr Base Cálculo Contribuição Após Ajustes',
                       7:'Alíquota PIS',
                       8:'Qtde Base Cálculo PIS',
                       9:'Qtde Alíquota PIS',
                       10:'Vlr Total Contribuição Apurada',
                       11:'Vlr Total Ajustes Acréscimo',
                       12:'Vlr Total Ajustes Redução',
                       13:'Vlr Contribuição Diferir Período',
                       14:'Vlr Contribuição Diferida Períodos Anteriores',
                       15:'Vlr Total Contribuição Período'
                       }
       
        self.arquivo_m200 = pd.concat(self.listaM200, ignore_index=True).rename(columns=m200columnns)
        self.arquivo_m600 = pd.concat(self.listaM600, ignore_index=True).rename(columns=m600columns)
        self.arquivo_m210 = pd.concat(self.listaM210, ignore_index=True).rename(columns=m210columns)
        self.arquivo_m610 = pd.concat(self.listaM610, ignore_index=True).rename(columns=m610columns)

        return self.arquivo_m200, self.arquivo_m600, self.arquivo_m210, self.arquivo_m610
    

if __name__ == '__main__':
    uploaded_files = st.sidebar.file_uploader("Escolha os arquivos SPED", type=['txt'], accept_multiple_files=True)
    if uploaded_files:
        sped_processor = SpedProcessor()  # Instância única do SpedProcessor
        file_paths = []

        for uploaded_file in uploaded_files:
            file_path = uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)

        for file_path in file_paths:
            sped_processor.lendoELimpandoDadosSped(file_path)
            sped_processor.guardando_tabelas()
        
        m200, m600, m210, m610 = sped_processor.tabelando_dados()

        st.title("Tabelas de Dados SPED")
        st.write("Tabela M200:")
        st.dataframe(m200)
        st.write("Tabela M600:")
        st.dataframe(m600)
        st.write("Tabela M210:")
        st.dataframe(m210)
        st.write("Tabela M610:")
        st.dataframe(m610)

        # Remover os arquivos após o processamento
        for file_path in file_paths:
            os.remove(file_path)


















