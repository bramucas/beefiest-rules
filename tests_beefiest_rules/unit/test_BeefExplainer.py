import pytest
from beefiest_rules import BeefExplainer


class TestBeefExplainer:
    def test_explain_fail_not_fitted(self):
        explainer = BeefExplainer()
        with pytest.raises(RuntimeError) as _:
            explainer.explain([(12, 32)])

    def test_from_csv(self):
        #TODO: to implement this test when it is not mocked.
        assert True

    def test_explain(self):
        #TODO: to implement this test when it is not mocked.
        assert True
