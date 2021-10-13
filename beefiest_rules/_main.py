from typing import Iterable
from beefiest_rules.explainer import Explainer
from beefiest_rules.parser import DataParser
from clingo import Control


class BeefExplainer:
    def __init__(self) -> None:
        self._explainer = None

    def fit_from_csv(self, csv_path) -> None:
        # from csv
        dp = DataParser()
        dp.from_csv(csv_path)

        # compute model (mocked for now)
        ctl = Control()
        # ctl.add("base", [], dp._program_as_string())
        # with open("boxes.lp", "r") as boxes_file:
        #     ctl.add("base", [], boxes_file.read())
        ctl.add(
            "base", [], """
            box(1). boxfeature(1, f1). boxfeature(1, f2). boxlimit(1, f1, 0). boxlimit(1, f1, 5).  boxlimit(1, f2, 20). boxlimit(1, f2, 40).
            box(2). boxfeature(2, f1). boxfeature(2, f2). boxlimit(2, f1, 6). boxlimit(2, f1, 11). boxlimit(2, f2, 20). boxlimit(2, f2, 40).
            """)
        ctl.ground([("base", [])])
        m = list(ctl.solve(yield_=True))[0]  # TODO: get only the optimal found
        self._explainer = Explainer.from_clingo_model(m)

    def explain(self,
                instances: Iterable,
                features: Iterable[str] = None) -> None:
        if self._explainer is None:
            raise RuntimeError("explain() called before fit().")
        return self._explainer.explain(instances, features)
