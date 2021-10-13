import pytest
import numpy as np
from beefiest_rules.parser import DataParser
from clingo import Function, String, Number


class TestDataParser:
    @pytest.fixture(scope='class')
    def custom_DataParser(self):
        dp = DataParser()
        dp._facts = np.array([
            Function('hola'),
            Function('buenas', [Number(1), Number(3)]),
            Function('feature', [])
        ])
        return dp

    @pytest.fixture(scope='class')
    def custom_DataParser_expected_as_text(self):
        return "hola. buenas(1,3). feature."

    def test_to_file(self, sandbox_dir, custom_DataParser,
                     custom_DataParser_expected_as_text):
        test_file_path = sandbox_dir / "test_to_file.txt"
        custom_DataParser.to_file(test_file_path)
        assert test_file_path.read_text() == custom_DataParser_expected_as_text

    def test_from_csv(self, datadir, sandbox_dir):
        # From csv
        dp = DataParser()
        dp.from_csv(datadir / 'haberman_mini.csv', column_labels=True)
        # tmp file
        test_file_path = sandbox_dir / "test_to_csv.txt"
        dp.to_file(test_file_path)

        assert test_file_path.read_text() == (datadir /
                                              'haberman_mini.lp').read_text()
