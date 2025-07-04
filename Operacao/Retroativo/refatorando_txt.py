import pandas as pd
import streamlit as st
import os
import zipfile
from io import BytesIO
import base64
import functools
import psutil
import time
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)


from alteracoes_base_implementacao import ImplementandoAlteracoesBase as ab
from alteracoes_registros import AlteracoesRegistros as ar



from colorama import Fore, Style



cpu_usage = psutil.cpu_percent(interval=1)
memory_usagePercent = psutil.virtual_memory().percent

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()

        print(f"{Fore.CYAN}{Style.BRIGHT}Iniciando a execução da função {func.__name__}{Style.RESET_ALL}")

        result = func(*args, **kwargs)

        print(f"{Fore.GREEN}{Style.BRIGHT}Finalizando a execução da função {func.__name__}{Style.RESET_ALL}")

        tempo_de_excução = time.time() - start

        print(f"{Fore.YELLOW}{Style.BRIGHT}Tempo de execução da funçâo {func.__name__}: {tempo_de_excução:.2f} segundos{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}Uso de CPU da função {func.__name__}: {cpu_usage}%{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}Uso de memória da função {func.__name__}: {memory_usagePercent}%{Style.RESET_ALL}")

        return result

    return wrapper
zip_buffer = BytesIO()

st.set_page_config(layout='wide')
#background_image ="Untitleddesign.jpg"
#st.markdown(
#     f"""
#     <iframe src="data:image/jpg;base64,{base64.b64encode(open(background_image, 'rb').read()).decode(
#
#    )}" style="width:4000px;height:3000px;position: absolute;top:-3vh;right:-1250px;opacity: 0.5;background-size: cover;background-position: center;"></iframe>
#     """,
#     unsafe_allow_html=True )

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

class SpedProcessor(ab,ar):


    def __init__(self):
        self.df = pd.DataFrame()

    def lendoELimpandoDadosSped(self, file_path: os.path):

        try:
                
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
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")        

        return self.df

    def devolvendo_txt(self,df:pd.DataFrame):
        
                
        formatted_lines = df.apply(lambda row: '|' + '|'.join(row.dropna().astype(str)), axis=1)
            
        result = '\n'.join(formatted_lines)
        #if result.endswith('|'):
                #esult = result[:-77] + '|'
        return result    
    
    def aplicado_alteradores(self):
        
        st.subheader('Arquivo Original')
        st.dataframe(self.df)
        
        ar.__init__(self,self.df)
        ab.__init__(self,self.df)

       # Abs Method 
        try:
            self.dados_willian()
            print(Fore.GREEN,"======= LOG ====== > : Dados base do arquivo inserido",Fore.RESET)        
        except Exception as e:
            print(Fore.RED,f"======= LOG ====== > : Erro ao adicionar dados Base{e}",Fore.RESET)        

        self.alterar_valores() 

        #try:
            #Abs Method        
        self.calculando_contadores_de_linhas()
        #    print(Fore.GREEN,"======= LOG ====== > : Alterando valores das linhas",Fore.RESET)        
        #except Exception as e :        
        #    print(Fore.RED,f"======= LOG ====== > : Erro ao recalcular linhas , {e}",Fore.RESET)        

        st.dataframe(self.df)
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
                    df = sped_processor.aplicado_alteradores()


                    conteudo_txt = sped_processor.devolvendo_txt(df)


                    df_comparativo_alterado = tabelas_de_apuração(df)
                    df_comparativo = tabelas_de_apuração(df)
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








