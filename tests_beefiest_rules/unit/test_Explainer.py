import pytest
from clingo import Control

from beefiest_rules.explainer import Explainer, Box, Explanation


class TestExplainer:
    @pytest.fixture(scope='class')
    def custom_explainer(self):
        return Explainer([
            Box(["f1", "f2"], [(0, 5), (20, 40)], "mockclass1"),
            Box(["f1", "f2"], [(6, 11), (20, 40)], "mockclass2")
        ])

    @pytest.fixture(scope='class')
    def custom_program(self):
        return """
            box(1). boxfeature(1, f1). boxfeature(1, f2). boxlimit(1, f1, 0). boxlimit(1, f1, 5).  boxlimit(1, f2, 20). boxlimit(1, f2, 40).
            box(2). boxfeature(2, f1). boxfeature(2, f2). boxlimit(2, f1, 6). boxlimit(2, f1, 11). boxlimit(2, f2, 20). boxlimit(2, f2, 40).
            """

    def assert_expected_custom_explainer(self, explainer):
        instances = [(2.5, 30), (8.5, 30)]

        explanations = list(explainer.explain(instances))
        assert len(explanations) == 2  # returns one item for each instance

        # instance 1
        major_class, expl = explanations[0][0]
        assert type(expl) == Explanation
        assert major_class == "mockclass1"
        assert str(
            expl
        ) == "This is mocked\n  |__Explanation class is just a mocked class."

        # instance 2
        major_class, expl = explanations[1][0]
        assert major_class == "mockclass2"
        assert str(
            expl
        ) == "This is mocked\n  |__Explanation class is just a mocked class."

    def test_explain(self, custom_explainer):
        self.assert_expected_custom_explainer(custom_explainer)

    def test_from_clingo_model(self, custom_program):
        ctl = Control()
        ctl.add("base", [], custom_program)
        ctl.ground([("base", [])])
        m = list(ctl.solve(yield_=True))[0]

        explainer = Explainer.from_clingo_model(m)
        self.assert_expected_custom_explainer(explainer)
