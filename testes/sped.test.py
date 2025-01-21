import unittest
import pandas as pd
import os
from TratamentoTXT.sped import SpedProcessor

class TestSpedProcessor(unittest.TestCase):
    def setUp(self):
        # Inicializa a instância do SpedProcessor com um caminho de arquivo vazio para os testes
        self.sped_processor = SpedProcessor([])
        self.mock_file_content = """|A|B|C|D|E|F|G|H|I|J|K|L|M|N
                                    |M210|1|2|3|4|5|6|7|8|9|10|11|12|13
                                    |M600|1|2|3|4|5|6|7|8|9|10|11|12|13
                                    |M200|1|2|3|4|5|6|7|8|9|10|11|12|13
                                    |M610|1|2|3|4|5|6|7|8|9|10|11|12|13"""

        # Cria um arquivo de teste temporário
        with open('test_file.txt', 'w') as file:
            file.write(self.mock_file_content)

    def tearDown(self):
        # Remove o arquivo de teste após os testes
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')

    def test_lendoELimpandoDadosSped_invalid_path(self):
        # Verifica se o método lança ValueError para caminho de arquivo inválido
        result = self.sped_processor.lendoELimpandoDadosSped("invalid_path.txt")
        self.assertIsInstance(result, ValueError)

    def test_lendoELimpandoDadosSped(self):
        # Testa a leitura e limpeza de dados do arquivo de teste
        df = self.sped_processor.lendoELimpandoDadosSped("test_file.txt")

        # Verifica o número de linhas e colunas
        self.assertEqual(len(df), 5)
        self.assertEqual(len(df.columns), 15)  # 14 colunas + coluna "Data"

        # Verifica se a coluna 'Data' foi adicionada corretamente
        self.assertIn('Data', df.columns)

    def test_guardando_tabelas(self):
        # Prepara os dados chamando lendoELimpandoDadosSped
        self.sped_processor.df = self.sped_processor.lendoELimpandoDadosSped("test_file.txt")
        
        # Testa o método guardando_tabelas
        self.sped_processor.guardando_tabelas()

        # Verifica se cada lista foi preenchida corretamente com dados de seus respectivos registros
        self.assertEqual(len(self.sped_processor.listaM210), 1)
        self.assertEqual(len(self.sped_processor.listaM600), 1)
        self.assertEqual(len(self.sped_processor.listaM200), 1)
        self.assertEqual(len(self.sped_processor.listaM610), 1)

    def test_tabelando_dados(self):
        # Prepara os dados para o teste
        self.sped_processor.df = self.sped_processor.lendoELimpandoDadosSped("test_file.txt")
        self.sped_processor.guardando_tabelas()

        # Testa o método tabelando_dados
        m200, m600, m210, m610 = self.sped_processor.tabelando_dados()

        # Verifica se os DataFrames retornados contêm os registros corretos
        self.assertIsInstance(m200, pd.DataFrame)
        self.assertIsInstance(m600, pd.DataFrame)
        self.assertIsInstance(m210, pd.DataFrame)
        self.assertIsInstance(m610, pd.DataFrame)

        # Verifica se cada DataFrame contém os dados corretos
        self.assertEqual(len(m200), 1)  # Apenas uma linha com M200
        self.assertEqual(len(m600), 1)  # Apenas uma linha com M600
        self.assertEqual(len(m210), 1)  # Apenas uma linha com M210
        self.assertEqual(len(m610), 1)  # Apenas uma linha com M610

if __name__ == '__main__':
    unittest.main()
