## Repositorio do projetos de Pis e Confins 100% Cumulativo
A pasta de Calculo se encontram todos os arquivos voltados ao processo de análise,
A pasta Operação se encontram todos os arquivos nescessarios para a Operacionalização, e todas as alterações nescessarias para os registros
Logger tem alguns codigos voltados a marcação de logs para testes do sistema
TratamentoTXT sao os arquivos nescessarios para leitura do arquivo fornecido pela Receita

## Cada pasta principal e independente uma da outra, sendo assim dentro desse repositorio temos dois projetos, o de análise e opeção que rodam independente um do outro

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/Taxall2024/pisEconfins.git

   cd seu-repositorio

   python -m venv venv
   source venv/bin/activate

   pip install -r requirements.txt

   python refatorando_txt.py #Para Operação
   python calculos.py #Para Análise


## Operação 
O arquivo main desse projeto e o refatorando_txt.py, o arquivo alterações_Base.py e uma classe abstrada que tem seus metodos implementados na alteracoes_base_implementação.py, nesse dois arquivos tem contidos alterações que nao devem ser alterados independente do registro, como contagem das linhas e informações padrão do emissor.

O arquivo ateracacoes_registros.py e onde estão contidas as regras de negocios, todas as alterações nescessarias para validação do arquivo de acordo com escopo do projeto.

A função main() dentro do arquivo refatorando_txt.py contém os arquivos de visualização para MVP desse projeto. 

Para funcionamento do sistema e nescessario que seja importada um ou mais arquivos EFD em formato TXT, emitido pel Receita Federal com separadores "|".

## Análise

O arquivo calculos.py e o arquivo main desse projeto, esse arquivo importa da classe SpedProcessor() dentro do modulo sped.py que e responsavel pela leitura e tratamento inicial dos dados TXT fornecidos pelo usuario, Os dados então são processados e tabelados.   

