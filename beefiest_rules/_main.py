from typing import Iterable
from beefiest_rules.explainer import Explainer
from clingo import Control
from dafact import Dafacter
from warnings import warn

from . import aspcode

__version__ = "0.0.1"


class CodeLoader:
    _LPCODE_FILENAME_CONSTRAINTS_ = 'beef_constraints.lp'
    _LPCODE_FILENAME_PREFERENCES_ = 'beef_preferences.lp'
    _LPCODE_FILENAME_RULES_ = 'beef_rules.lp'

    @property
    def aspcode_constraints(self):
        if not hasattr(self, '_aspcode_constraints'):
            try:
                import importlib.resources as pkg_resources
            except ImportError:
                # Try backported to PY<37 `importlib_resources`.
                import importlib_resources as pkg_resources
            setattr(
                self, '_aspcode_constraints',
                pkg_resources.read_text(aspcode,
                                        self._LPCODE_FILENAME_CONSTRAINTS_))
        return self._aspcode_constraints

    @property
    def aspcode_preferences(self):
        if not hasattr(self, '_aspcode_preferences'):
            try:
                import importlib.resources as pkg_resources
            except ImportError:
                # Try backported to PY<37 `importlib_resources`.
                import importlib_resources as pkg_resources
            setattr(
                self, '_aspcode_preferences',
                pkg_resources.read_text(aspcode,
                                        self._LPCODE_FILENAME_PREFERENCES_))
        return self._aspcode_preferences

    @property
    def aspcode_rules(self):
        if not hasattr(self, '_aspcode_rules'):
            try:
                import importlib.resources as pkg_resources
            except ImportError:
                # Try backported to PY<37 `importlib_resources`.
                import importlib_resources as pkg_resources
            setattr(
                self, '_aspcode_rules',
                pkg_resources.read_text(aspcode, self._LPCODE_FILENAME_RULES_))
        return self._aspcode_rules

    @property
    def aspcode_complete(self):
        if not hasattr(self, '_aspcode_complete'):
            setattr(
                self, '_aspcode_complete', '\n'.join([
                    self.aspcode_rules,
                    self.aspcode_preferences,
                ]))
        return self._aspcode_complete


class BeefExplainer:
    def __init__(self) -> None:
        self._explainer = None

    def fit(self,
            data,
            target,
            have_names=True,
            factor=0,
            numerical_columns=None,
            omit_names=False,
            delimiter=",",
            on_explainer=None) -> None:
        """Fit the explainer.

        Args:
            data (Union[str, ndarray, pd.Dataframe]) : (array-like, sparse matrix) of shape (n_samples, n_features) or (str) path to a csv file.
            target (Union[str, int]): name/index of the target feature/column.
            have_names (bool, optional): whether if the names of the features are meant to be extracted from data. If false, features will be automatically labeled as (f1, f2, etc.).Defaults to True.
            factor (int, optional): number of decimals which are meant to be included. If 0, it will be automatically set at maximum precision. Defaults to 0.
            numerical_columns (_type_, optional): which columns are meant to be treated as numerical. If None, this will be set automatically (mistakes may be done). Defaults to None.
            omit_names (bool, optional): WILL BE DEPRECATED. In case data is a csv, whether to ignore the header row or not. Defaults to False.
            delimiter (str, optional): delimiter of the csv file. Defaults to ",".
            on_explainer (Callback[[Explainer]] , optional): callback for intercepting Explainers. Defaults to None.

        Raises:
            ValueError: if target identifier is nor str or int.
        """
        # target
        if type(target) == str:
            target_fact = f'target("{target}").'
        elif type(target) == int:
            target_fact = f'target("x{target}").'
        else:
            raise ValueError(f'target identifier {target} not valid.')

        # from csv
        dafacter = Dafacter(data,
                            factor=factor,
                            numerical_columns=numerical_columns,
                            have_names=have_names,
                            omit_names=omit_names,
                            delimiter=delimiter)
        aspcode_loader = CodeLoader()

        ctl = Control()
        ctl.add("base", [], dafacter.as_program_string())  # adds data
        ctl.add("base", [],
                aspcode_loader.aspcode_complete)  # adds beef program
        ctl.add("base", [], target_fact)

        ctl.ground([("base", [])])

        if on_explainer is not None:
            ctl.solve(on_model=lambda m: on_explainer(
                Explainer.from_clingo_model(m)))
        else:
            m = list(ctl.solve(yield_=True))
            if m == []:
                warn('UNSAT - explainer object not ready to explain')
            else:
                self._explainer = Explainer.from_clingo_model(m[-1])

    def explain(self,
                instances: Iterable,
                features: Iterable[str] = None) -> None:
        """Give explanations for a set of instances.

        Args:
            instances (Iterable): instances to be explained. Coordinates/features must match those used to fit the explainer.
            features (Iterable[str], optional): Features to be used for explaining.  Defaults to None.

        Raises:
            RuntimeError: if explainer is not already fitted.

        Returns:
            Iterable: explanations for the instances
        """
        if self._explainer is None:
            raise RuntimeError("explain() called successful call to fit().")
        return self._explainer.explain(instances, features)
