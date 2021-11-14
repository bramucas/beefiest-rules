from clingo import Model
from typing import Tuple
import numpy as np
from typing import Iterable
from ..utils import check_iterable


class Box:
    def __init__(self, axis_names: Iterable[str],
                 boundaries: Iterable[Tuple[float]], major_class: str) -> None:
        """
        Args:
            feature_names (Iterable[str]): names of the axes on which the box is defined.
            boundaries (Iterable[Tuple[np._FloatType]]): box's boundaries for the specified features.

        Raises:
            ValueError: 'feature_names' or 'boundaries' arguments are None.
            ValueError: 'feature_names' or 'boundaries' arguments are not iterable.
            ValueError: 'feature_names' or 'boundaries' arguments are empty or have different lengths.
        """
        check_iterable(axis_names, 'axis_names')
        check_iterable(boundaries, 'boundaries')
        if len(axis_names) != len(boundaries):
            raise ValueError(
                "Features and boundaries must have the same length.")

        self._features: Iterable[str] = axis_names
        self._boundaries: Iterable[Tuple[np._FloatType]] = boundaries
        self.major_class: str = major_class

    def contains_point(self,
                       coord_tuple: Tuple[float],
                       axis_names: Iterable[str] = None) -> bool:
        """Checks if a point (given by its coordinates) falls inside the box.

        Args:
            coord_tuple (Tuple[np._FloatType]): coordinates of the point to be checked.
            axis_names (Iterable[str], optional): names of the axes to be checked. Must match the cardinality of the specified coordinates. If not specified, all the axes defined for the box are checked. Defaults to None.

        Raises:
            ValueError: cardinality of the coordinates or the axis_names does not match.

        Returns:
            bool: whether the point falls indside the box or not.
        """
        if not axis_names and len(coord_tuple) != len(self._boundaries):
            raise ValueError("Number of coordinates does not match.")
        if axis_names is not None and len(coord_tuple) != len(axis_names):
            raise ValueError(
                "Number of specified features does not match the coordinates.")

        if axis_names is None:
            # all axes are checked
            for c, (lbound, rbound) in zip(coord_tuple, self._boundaries):
                if c < lbound or c > rbound:
                    return False
        else:
            # just specified axes are checked
            for aname, c in zip(axis_names, coord_tuple):
                lbound, rbound = self._boundaries[self._features.index(aname)]
                if c < lbound or c > rbound:
                    return False
        return True

    def get_explanation(self):
        return Explanation()


class Explanation:
    def __init__(
        self,
        string="This is mocked\n  |__Explanation class is just a mocked class."
    ):
        self.string = string

    def __str__(self) -> str:
        return self.string


class Explainer:
    def __init__(self, box_clusters: Iterable[Box]):
        check_iterable(box_clusters, "box_clusers")
        self._boxes = box_clusters

    @staticmethod
    def from_clingo_model(m: Model):
        n_box = len([s for s in m.symbols(shown=True) if s.name == "box"])
        limits, classes = [dict() for _ in range(0, n_box)
                           ], [f'mockclass{i+1}' for i in range(0, n_box)]
        for sym in m.symbols(shown=True):
            if sym.name == "boxlimit":
                i_box, f, l = sym.arguments
                i_box, f, l = int(str(i_box)) - 1, str(f), int(str(l))
                if f not in limits[i_box]:
                    limits[i_box][f] = []
                limits[i_box][f].append(l)
        return Explainer([
            Box(features, list(map(tuple, map(sorted, boundaries))), c)
            for (features,
                 boundaries), c in zip([zip(*d.items())
                                        for d in limits], classes)
        ])

    def explain(self,
                instances: Iterable,
                features: Iterable[str] = None) -> Iterable:
        for i in instances:
            yield [(box.major_class, box.get_explanation())
                   for box in self._boxes
                   if box.contains_point(i, axis_names=features)]
