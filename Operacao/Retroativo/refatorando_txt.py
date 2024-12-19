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
            df = df.loc[df[0].str.startswith('A170') | df[0].str.startswith('0100')|
                        df[0].str.startswith('A100')| df[0].str.startswith('M200')
                        | df[0].str.startswith('M600')]
            
            return df

        df = filtrar_tabelas(df)


        return df

class SpedProcessor():
    """
    A class used to process SPED (Public Digital Bookkeeping System) files.
    Methods
    -------
    __init__():
        Initializes the SpedProcessor with an empty DataFrame.
    lendoELimpandoDadosSped(file_path: os.path):
        Reads and cleans SPED data from a given file path and stores it in a DataFrame.
    alteracoes_txt():
        Applies specific alterations to the DataFrame and recalculates values based on given rules.
    calculos_aliquota(aliquota: float, base_calculo: int, atribuir_resultado: int):
        Calculates new values based on a given aliquot and updates the DataFrame.
    devolvendo_txt():
        Converts the DataFrame back to a formatted text string.
    verificacao_a170():
        Verifies the presence of 'A170' entries and removes specific rows based on given conditions.
    main():
        Main method to handle file uploads, process the files, and provide download links for the altered files.
    """
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



    def verificacao_a170(self):
        """
        This method performs several data verification and transformation steps on a DataFrame `self.df`.
        Steps performed:
        1. Checks if the DataFrame contains any rows where the first column is 'A170'.
        2. If 'A170' is not found, removes rows where the first column is 'C100' or 'M100' and displays a success message.
        3. Removes rows based on specific conditions for columns 'A100', 'F100', 'C100', 'C190', 'C395', 'D100', 'D500', 'F100', 'F120', 'F130', and 'F150'.
        4. Sets specific columns to 0 for rows where the first column is 'M100'.
        5. Sets the second column to 3 for rows where the first column is '0110'.
        6. Updates specific columns based on conditions involving 'A100' and 'A170' rows.
        7. Defines and calls helper functions `valor_m200` and `valor_m600` to calculate sums for specific columns and updates 'M200' and 'M600' rows with these sums.
        Returns:
            pd.DataFrame: The modified DataFrame `self.df`.
        """
        self.verificacao = None
        if (self.df[0]=='A170').any():
            self.verificacao = True
        else:
            self.verificacao = False
        
        if self.verificacao == False:

            self.df = self.df.loc[~((self.df[0] == 'C100')&(self.df[0] == 'M100'))]
            st.success('O arquivo não possui dados na rubrica "A170"... As Rubricas "C100" e "M100" foram removidas!')
        
        self.df = self.df.loc[~((self.df[0] == 'A100') & (self.df[2] == '1'))]
        self.df = self.df.loc[~((self.df[0] == 'F100') & (self.df[1] == '0'))]
        
        self.df = self.df.loc[~(self.df[0] == 'C100')]
        self.df = self.df.loc[~(self.df[0] == 'C190')]
        self.df = self.df.loc[~(self.df[0] == 'C395')]
        self.df = self.df.loc[~(self.df[0] == 'D100')]
        self.df = self.df.loc[~(self.df[0] == 'D500')]
        self.df = self.df.loc[~(self.df[0] == 'F100')]
        self.df = self.df.loc[~(self.df[0] == 'F120')]
        self.df = self.df.loc[~(self.df[0] == 'F130')]
        self.df = self.df.loc[~(self.df[0] == 'F150')]

        self.df.loc[self.df[0] == 'M100', 3] = 0
        self.df.loc[self.df[0] == 'M100', 7] = 0
        self.df.loc[self.df[0] == 'M100', 11] = 0
        self.df.loc[self.df[0] == 'M100', 13] = 0
        self.df.loc[self.df[0] == '0110', 1] = 3

        
        for i in range(len(self.df) - 1):
            if self.df.iloc[i, 0] == 'A100' and self.df.iloc[i + 1, 0] == 'A170':
                self.df.iloc[i, 15] = self.df.iloc[i + 1, 11]
            if self.df.iloc[i, 0] == 'A100' and self.df.iloc[i + 1, 0] == 'A170':
                self.df.iloc[i, 17] = self.df.iloc[i + 1, 15]

        def valor_m200(df):
            a100 = self.df.loc[df[0]=='A100']
            
            a100[15] = a100[15].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = a100[15].sum()
            print('>>>>>Sooma',soma_a100)

            return soma_a100

        def valor_m600(df):
            a100 = self.df.loc[df[0]=='A100']
            
            a100[17] = a100[17].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = a100[17].sum()
            print('>>>>>Sooma',soma_a100)

            return soma_a100    

        m200 = valor_m200(self.df)
        m600 = valor_m600(self.df)

        self.df.loc[self.df[0] == 'M200',8] = m200
        self.df.loc[self.df[0] == 'M600',8] = m600
         
        return self.df


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
                    verificando = sped_processor.verificacao_a170()
                    conteudo_txt = sped_processor.devolvendo_txt()

                    df_comparativo_alterado = tabelas_de_apuração(df)
                    df_comparativo = tabelas_de_apuração(verificando)
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
                st.dataframe(arquivo_comparativo_alterado_final)
            
            with col2:
                st.metric('Contagem de dados Alterados', contagem_alterado.sum())
                st.subheader('Tabela de Apuração Alterado')
                st.dataframe(arquivo_comparativo_original_final)

if __name__ == '__main__':
    
    pisConfins = SpedProcessor()
    pisConfins.main()



