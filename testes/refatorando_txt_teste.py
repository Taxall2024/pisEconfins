import pandas as pd
import unittest
import os

class SpedProcessor:
    def __init__(self):
        self.df = pd.DataFrame()

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
        return self.df

    def alteracoes_txt(self):
        self.df.loc[self.df[0] == '0000', 2] = 1
        self.df.loc[self.df[0] == '0100', 1] = 'WILLIAM SILVA DE ALMEIDA'
        self.df.loc[self.df[0] == '0100', 2] = 89709861115
        self.df.loc[self.df[0] == '0100', 3] = '19342DF'
        self.df.loc[self.df[0] == '0100', 6] = 'Q CRS 502 BLOCO B'
        self.df.loc[self.df[0] == '0100', 5] = 70330520
        self.df.loc[self.df[0] == '0100', 9] = 'ASA SUL'
        self.df.loc[self.df[0] == '0100', 10] = 6181272930
        self.df.loc[self.df[0] == '0100', 12] = 'NEGOCIOS@TAXALL.COM.BR'

        self.df.loc[self.df[0] == 'A170', 10] = '0,65'
        self.df.loc[self.df[0] == 'A170', 14] = 3
        self.calculos_aliquota(0.0065, 9, 11)
        self.calculos_aliquota(0.03, 13, 15)
        return self.df

    def calculos_aliquota(self, aliquota, base_calculo, atribuir_resultado):
        mask_a170 = self.df[0] == 'A170'
        numeric_values = pd.to_numeric(self.df.loc[mask_a170, base_calculo].str.replace(',', '.'), errors='coerce')
        new_values = numeric_values * aliquota
        new_values = new_values.apply(lambda x: f"{x:.2f}".replace('.', ','))
        self.df.loc[mask_a170, atribuir_resultado] = new_values

class TestSpedProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = SpedProcessor()
        self.test_file_path = 'test_sped_file.txt'
        with open(self.test_file_path, 'w', encoding='latin-1') as file:
            file.write("|0100|006|0|||01082024|31082024|GE SERVICOS LTDA|08744139000151|DF|5300108||00|1|\n")
            file.write("|0000|006|0|||01082024|31082024|GE SERVICOS LTDA|08744139000151|DF|5300108||00|1|\n")
            file.write("|A170|Item description|10|20|30|40|50|60|70|80|1000,50|90|100|2000,75|110|\n")

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_lendoELimpandoDadosSped(self):
        df = self.processor.lendoELimpandoDadosSped(self.test_file_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty, "O DataFrame não deve estar vazio após a leitura.")
        self.assertEqual(len(df), 3, "O DataFrame deve ter 3 linhas.")

    def test_alteracoes_txt(self):
        self.processor.lendoELimpandoDadosSped(self.test_file_path)
        df = self.processor.alteracoes_txt()
        self.assertEqual(df.loc[df[0] == '0100', 1].values[0], 'WILLIAM SILVA DE ALMEIDA')
        self.assertEqual(df.loc[df[0] == '0100', 2].values[0], 89709861115)
        self.assertEqual(df.loc[df[0] == 'A170', 10].values[0], '0,65')
        self.assertEqual(df.loc[df[0] == 'A170', 14].values[0], 3)

    def test_calculos_aliquota(self):
        self.processor.lendoELimpandoDadosSped(self.test_file_path)
        self.processor.calculos_aliquota(0.0065, 10, 11)
        calculado = self.processor.df.loc[self.processor.df[0] == 'A170', 11].values[0]
        self.assertEqual(calculado, '6,50', "O valor calculado para a alíquota 0.65% está incorreto.")
        self.processor.calculos_aliquota(0.03, 13, 15)
        calculado = self.processor.df.loc[self.processor.df[0] == 'A170', 15].values[0]
        self.assertEqual(calculado, '60,02', "O valor calculado para a alíquota 3% está incorreto.")

if __name__ == '__main__':
    unittest.main()
