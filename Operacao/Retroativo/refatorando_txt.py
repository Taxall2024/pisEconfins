import pandas as pd
import streamlit as st
import os
import zipfile
from io import BytesIO
import base64
import functools
zip_buffer = BytesIO()

st.set_page_config(layout='wide')
background_image ="Untitleddesign.jpg"
st.markdown(
     f"""
     <iframe src="data:image/jpg;base64,{base64.b64encode(open(background_image, 'rb').read()).decode(

    )}" style="width:4000px;height:3000px;position: absolute;top:-3vh;right:-1250px;opacity: 0.5;background-size: cover;background-position: center;"></iframe>
     """,
     unsafe_allow_html=True )

def tabelas_de_apuração(df):

        def filtrar_tabelas(df):
            df['Data'] = df.iloc[0,5]
            df = df.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,-1]]
            df = df.loc[df[0].str.startswith('A170') | df[0].str.startswith('0100')]
            
            return df
        
        df = filtrar_tabelas(df)


        return df

class SpedProcessor():
    def __init__(self):
        self.df = pd.DataFrame()

    def lendoELimpandoDadosSped(self, file_path: os.path):
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
        self.df_original = self.df.copy()

        return self.df
    
    def alteracoes_txt(self):
        # Trabalha com uma cópia do DataFrame para evitar renderizações automáticas indesejadas
        df = self.df.copy()

        # Refatorando dados no DataFrame copiado
        df.loc[df[0] == '0000', 2] = 1
        df.loc[df[0] == '0100', 1] = 'WILLIAM SILVA DE ALMEIDA'
        df.loc[df[0] == '0100', 2] = 89709861115
        df.loc[df[0] == '0100', 3] = '19342DF'
        df.loc[df[0] == '0100', 6] = 'Q CRS 502 BLOCO B'
        df.loc[df[0] == '0100', 5] = 70330520
        df.loc[df[0] == '0100', 9] = 'ASA SUL'
        df.loc[df[0] == '0100', 10] = 6181272930
        df.loc[df[0] == '0100', 12] = 'NEGOCIOS@TAXALL.COM.BR'

        # Alterando aliquota e refazendo cálculos
        df.loc[df[0] == 'A170', 10] = '0,65'
        df.loc[df[0] == 'A170', 14] = 3
        self.calculos_aliquota(0.0065, 9, 11)
        self.calculos_aliquota(0.03, 13, 15)

        # Atualizando `self.df` apenas no final
        self.df = df
        self.data = str(df.iloc[0, 5])
        self.df_apurado = self.df.copy()

        # Retorna None para evitar renderização automática
        return self.df
    
    def calculos_aliquota(self,aliquota:float, base_calculo: int, atribuir_resultado: int):
        mask_a170 = self.df[0] == 'A170'
        
        numeric_values = pd.to_numeric(self.df.loc[mask_a170, base_calculo].str.replace(',', '.'), errors='coerce')

        new_values = numeric_values * aliquota
        new_values = new_values.apply(lambda x: f"{x:.2f}".replace('.', ','))

        self.df.loc[mask_a170, atribuir_resultado] = new_values   
    
    def devolvendo_txt(self):
        

        formatted_lines = self.df.apply(lambda row: '|' + '|'.join(row.dropna().astype(str)), axis=1)

        result = '\n'.join(formatted_lines)
        return result
    def main(self):
        
        uploaded_files = st.sidebar.file_uploader("Escolha os arquivos SPED", type=['txt'], accept_multiple_files=True)
        
        tabela_original_lista = []
        tabela_de_apuracao_lista = []
        
        if uploaded_files:

            sped_processor = SpedProcessor() 
            file_paths = []
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for uploaded_file in uploaded_files:
                    file_path = uploaded_file.name
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    file_paths.append(file_path)

                for file_path in file_paths:

                    df = sped_processor.lendoELimpandoDadosSped(file_path)

                    df_alterado = sped_processor.alteracoes_txt()
                    conteudo_txt = sped_processor.devolvendo_txt()

                    df_comparativo = tabelas_de_apuração(df)
                    df_comparativo_alterado = tabelas_de_apuração(df_alterado)
                    tabela_original_lista.append(df_comparativo)
                    tabela_de_apuracao_lista.append(df_comparativo_alterado)

                    data = sped_processor.data
                    
                    data = sped_processor.data
                    arquivo_nome = f"arquivo{data}.txt"

                    zip_file.writestr(arquivo_nome, conteudo_txt)
            
            zip_buffer.seek(0)
            st.download_button( label="Baixar arquivos ",
                                data=zip_buffer,file_name="arquivos_alterados.zip",
                                mime="application/zip",type='primary')

            arquivo_comparativo_original_final = pd.concat(tabela_original_lista)
            arquivo_comparativo_alterado_final = pd.concat(tabela_de_apuracao_lista)

            for file_path in file_paths:
                os.remove(file_path)
            
        col1,col2 = st.columns(2)

        if tabela_de_apuracao_lista:
            codigo = st.sidebar.selectbox('Codigo Referencia',options=[codigo for codigo in arquivo_comparativo_original_final[0].unique() if codigo!= '' ])
            with col1:

                contagem_original = arquivo_comparativo_original_final.value_counts()
                contagem_alterado = arquivo_comparativo_alterado_final.value_counts()

                arquivo_comparativo_original_final = arquivo_comparativo_original_final.loc[
                    arquivo_comparativo_original_final[0] == codigo]  

                arquivo_comparativo_alterado_final = arquivo_comparativo_alterado_final.loc[
                    arquivo_comparativo_alterado_final[0] == codigo]  
                
                st.metric('Contagem de dados Original', contagem_original.sum())
                st.subheader('Tabela de Apuração Original')
                st.dataframe(arquivo_comparativo_original_final)
            
            with col2:
                st.metric('Contagem de dados Alterados', contagem_alterado.sum())
                st.subheader('Tabela de Apuração Alterado')
                st.dataframe(arquivo_comparativo_alterado_final)

if __name__ == '__main__':
    pisConfins = SpedProcessor()
    pisConfins.main()

