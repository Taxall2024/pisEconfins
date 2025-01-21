import unittest
import pandas as pd

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Operacao.Retroativo.alteracoes_registros import AlteracoesRegistros


class TestAlteracoesRegistros(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        data = {
            0: ['A100', 'A100', 'A170', 'A100', 'A170'],
            2: ['1', '2', '1', '1', '2']
        }
        self.df = pd.DataFrame(data)
        self.alteracoes = AlteracoesRegistros(self.df)

    def test_remove_A100_Col2_1(self):
        self.alteracoes.remove_A100_Col2_1()
        # Check that rows with (0 == 'A100' and 2 == '1') are removed
        expected_data = {
            0: ['A100', 'A170', 'A170'],
            2: ['2', '1', '2']
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(self.alteracoes.df.reset_index(drop=True), expected_df.reset_index(drop=True))

    def test_alterando_M605_Cols_1_2(self):

        new_row = pd.DataFrame({0: ['M605'], 1: [''], 2: ['']})
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.alteracoes.df = self.df
        self.alteracoes.alterando_M605_Cols_1_2()
        # Check that the row with (0 == 'M605') has updated values in columns 1 and 2
        expected_data = {
            0: ['A100', 'A100', 'A170', 'A100', 'A170', 'M605'],
            1: ['1', '2', '1', '1', '2', '12'],
            2: ['1', '2', '1', '1', '2', '217201']
        }
        expected_df = pd.DataFrame(expected_data)
        # Redefinir os índices e ordenar as colunas antes de comparar
        pd.testing.assert_frame_equal(
            self.alteracoes.df.reset_index(drop=True).sort_index(axis=1),
            expected_df.reset_index(drop=True).sort_index(axis=1)
        )

if __name__ == '__main__':
    unittest.main()