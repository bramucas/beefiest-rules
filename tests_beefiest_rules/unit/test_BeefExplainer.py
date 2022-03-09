import pytest
from beefiest_rules import BeefExplainer

from ast import literal_eval


class TestBeefExplainer:
    def assert_test_case(self, datadir, test_case_name):
        """Given a test_case_name it compares the boxes created by BeefExplainer from its csv file to the expected boxes stored as a dict in the expected result file

        Args:
            datadir (_type_): pytest datadir fixture to access csv and result files
            test_case_name (_type_): name of the test case, it must match the names used for the test files. This is '{test_case_name}.csv' and 'expected_{test_case_name}.txt' in the test_BeefExpainer directory.
        """
        explainer = BeefExplainer()
        explainer.fit((datadir / f'{test_case_name}.csv'), 'output')

        assert [b.__dict__ for b in explainer._explainer._boxes] == \
        literal_eval((datadir / f'expected_{test_case_name}.txt').read_text())

    def test_explain_fail_not_fitted(self):
        explainer = BeefExplainer()
        with pytest.raises(RuntimeError) as _:
            explainer.explain([(12, 32)])

    def test_explainer_minimal_cases(self, datadir):
        self.assert_test_case(datadir, 'minimal_two_box')
        # self.assert_test_case(datadir, 'minimal_one_box')  # TODO: why is not returning any boxlimits/4.
        self.assert_test_case(datadir, 'minimal_2d_box')
