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
        causes = "\n".join([
            f'|__{f} between ({l}, {r})'
            for f, (l, r) in zip(self._features, self._boundaries)
        ])
        return Explanation(f'Class {self.major_class}\n{causes}')


class Explanation:
    def __init__(self, string=""):
        self.string = string

    def __str__(self) -> str:
        return self.string


class Explainer:
    def __init__(self, box_clusters: Iterable[Box]):
        check_iterable(box_clusters, "box_clusters")
        self._boxes = box_clusters

    @staticmethod
    def from_clingo_model(m: Model):
        limits, classes = dict(), dict()
        for sym in m.symbols(shown=True):
            if sym.name == "boxlimits":
                i_box, f, left, right = sym.arguments
                i_box, f, left, right = int(str(i_box)), str(f).strip('"').strip(), \
                    int(str(left)), int(str(right))
                if not i_box in limits:
                    limits[i_box] = dict()
                limits[i_box][f] = (left, right)

            if sym.name == "boxmain":
                i_box, main_class = sym.arguments
                i_box, main_class = int(str(i_box)), int(str(main_class))
                classes[i_box] = main_class

        box_list = list()
        for i_box, ls in limits.items():
            box_list.append(
                Box(
                    list(ls.keys()),
                    list(ls.values()),
                    classes[i_box],
                ))
        return Explainer(box_list)

    def explain(self,
                instances: Iterable,
                features: Iterable[str] = None) -> Iterable:
        for i in instances:
            yield [(box.major_class, box.get_explanation())
                   for box in self._boxes
                   if box.contains_point(i, axis_names=features)]
