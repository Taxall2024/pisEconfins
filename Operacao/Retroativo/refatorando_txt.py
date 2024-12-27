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
                        | df[0].str.startswith('M600') | df[0].str.startswith('0000')]
            
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
        self.calculos_aliquota(df,0.0065, 9, 11)
        self.calculos_aliquota(df,0.03, 13, 15)
        # Atualizando `self.df` apenas no final
        self.df = df
        self.data = str(df.iloc[0, 5])
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
    
    def devolvendo_txt(self,df):
        

        formatted_lines = df.apply(lambda row: '|' + '|'.join(row.dropna().astype(str)), axis=1)

        result = '\n'.join(formatted_lines)
        
        return result    



    def verificacao_a170(self,df,numero_recibo) -> pd.DataFrame:

        self.verificacao = None
        if (df[0]=='A170').any():
            self.verificacao = True
        else:
            verificacao = False
        
        if self.verificacao == False:

           
            st.success('O arquivo não possui dados na rubrica "A170"...')

        df = df.loc[~((df[0] == 'A100') & (df[2] == '1'))]
        df = df.loc[~((df[0] == 'F100') & (df[1] == '0'))]
        
        #df = df.loc[~(df[0] == 'C100')]
        #df = df.loc[~(df[0] == 'C170')]

        df.loc[((df[0] == 'C100')&(df[1] == '0')),25] = ''
        df.loc[((df[0] == 'C100')&(df[1] == '0')),26] = ''
        
        df.loc[((df[0] == 'C170')&(df[1] == '1')),35] = ''
        df.loc[((df[0] == 'C170')&(df[1] == '1')),33] = ''
        df.loc[((df[0] == 'C170')&(df[1] == '1')),29] = ''
        df.loc[((df[0] == 'C170')&(df[1] == '1')),27] = ''
        
        
        
        

        df.loc[(df[0]=='C170') & (df[1]=='1') & (df[24].str.contains('5')),24] = '70'
            
        df.loc[(df[0]=='C170') & (df[1]=='1') & (df[30].str.contains('5')),30] = '70'
            
                

        
        
        df = df.loc[~(df[0] == 'C190')]
        df = df.loc[~(df[0] == 'C395')]
        df = df.loc[~(df[0] == 'D100')]
        df = df.loc[~(df[0] == 'D500')]
        df = df.loc[~(df[0] == 'F100')]
        df = df.loc[~(df[0] == 'F120')]
        df = df.loc[~(df[0] == 'F130')]
        df = df.loc[~(df[0] == 'F150')]

        df = df.loc[~((df[0]== '9900')&(df[1] == 'C190'))]
        df = df.loc[~((df[0]== '9900')&(df[1] == 'C395'))]
        df = df.loc[~((df[0]== '9900')&(df[1] == 'D100'))]
        df = df.loc[~((df[0]== '9900')&(df[1] == 'D500'))]
        df = df.loc[~((df[0]== '9900')&(df[1] == 'F100'))]
        df = df.loc[~((df[0]== '9900')&(df[1] == 'F120'))]
        df = df.loc[~((df[0]== '9900')&(df[1] == 'F130'))]
        df = df.loc[~((df[0]== '9900')&(df[1] == 'F150'))]
          
        
        
        
        df.loc[df[0] == 'M100', 3] = 0
        df.loc[df[0] == 'M100', 7] = 0
        df.loc[df[0] == 'M100', 11] = 0
        df.loc[df[0] == 'M100', 13] = 0
        df.loc[df[0] == '0110', 1] = '3'

        
        for i in range(len(df) - 1):
            if df.iloc[i, 0] == 'A100' and df.iloc[i + 1, 0] == 'A170':
                df.iloc[i, 15] = df.iloc[i + 1, 11]
            if df.iloc[i, 0] == 'A100' and df.iloc[i + 1, 0] == 'A170':
                df.iloc[i, 17] = df.iloc[i + 1, 15]

        def valor_m200(df):
            a100 = df.loc[df[0]=='A100']
            
            a100[15] = a100[15].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = a100[15].sum()
            print('>>>>>Sooma',soma_a100)

            return soma_a100

        def valor_m600(df):
            a100 = df.loc[df[0]=='A100']
            
            a100[17] = a100[17].str.replace(',','.').replace('','0').astype(float)
            soma_a100 = a100[17].sum()
            print('>>>>>Sooma',soma_a100)

            return soma_a100    

        m200 = valor_m200(self.df)
        m600 = valor_m600(self.df)





        df.loc[df[0] == 'M200',8] = m200
        df.loc[df[0] == 'M200',1] ='' 
        df.loc[df[0] == 'M200',2] ='' 
        df.loc[df[0] == 'M200',3] ='' 
        df.loc[df[0] == 'M200',4] = ''        
        df.loc[df[0] == 'M200',5] ='' 
        
        df.loc[df[0] == 'M600',8] = m600
        df.loc[df[0] == 'M600',1] = ''
        df.loc[df[0] == 'M600',2] = ''
        df.loc[df[0] == 'M600',3] = ''
        df.loc[df[0] == 'M600',4] = ''
        df.loc[df[0] == 'M600',5] = ''






        df.loc[df[0] == 'M210',1] = '51'
        df.loc[df[0] == 'M610',1] = '51'





        df.loc[df[0] == 'M500',3] = '0' 
        df.loc[df[0] == 'M500',7] = '0' 
        df.loc[df[0] == 'M500',8] = '0' 
        df.loc[df[0] == 'M500',9] = '0' 
        df.loc[df[0] == 'M500',10] = '0' 
        df.loc[df[0] == 'M500',11] = '0' 
        df.loc[df[0] == 'M500',12] = '0' 
        df.loc[df[0] == 'M500',13] = '0' 
        df.loc[df[0] == 'M500',14] = '0' 

        df.loc[df[0] == 'M100',3] = '0' 
        df.loc[df[0] == 'M100',7] = '0' 
        df.loc[df[0] == 'M100',3] = '0' 
        df.loc[df[0] == 'M100',8] = '0' 
        df.loc[df[0] == 'M100',9] = '0' 
        df.loc[df[0] == 'M100',10] = '0' 
        df.loc[df[0] == 'M100',11] = '0' 
        df.loc[df[0] == 'M100',12] = '0' 
        df.loc[df[0] == 'M100',13] = '0' 
        df.loc[df[0] == 'M100',14] = '0' 

        df.loc[df[0] == '0000',3] = numero_recibo 
       # Adiciona uma linha vazia ao final do DataFrame
        df =pd.concat([df, pd.DataFrame([[None] * len(df.columns)], columns=df.columns)], ignore_index=True)

        st.dataframe(df)




        return df


    def main(self):
        
        uploaded_files = st.sidebar.file_uploader("Escolha os arquivos SPED", type=['txt'], accept_multiple_files=True)
        
        tabela_original_lista = []
        tabela_de_apuracao_lista = []
        
        if uploaded_files:

            numero_recibo = st.sidebar.text_input('Numero do Recibo')
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
                    verificando = sped_processor.verificacao_a170(df_alterado,numero_recibo)

                    conteudo_txt = sped_processor.devolvendo_txt(verificando)

                    df_comparativo_alterado = tabelas_de_apuração(df)
                    df_comparativo = tabelas_de_apuração(verificando)
                    tabela_original_lista.append(df_comparativo)
                    tabela_de_apuracao_lista.append(df_comparativo_alterado)

                    
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



