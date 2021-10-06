from typing import Tuple
import numpy as np
from typing import Iterable

class Explainer:
    def __init__(self):
        raise NotImplementedError

class Box:
    
    def __init__(self, axis_names: Iterable[str], boundaries: Iterable[Tuple[float]]) -> None:
        """
        Args:
            feature_names (Iterable[str]): names of the axes on which the box is defined.
            boundaries (Iterable[Tuple[np._FloatType]]): box's boundaries for the specified features.

        Raises:
            ValueError: 'feature_names' or 'boundaries' arguments are None.
            ValueError: 'feature_names' or 'boundaries' arguments are not iterable.
            ValueError: 'feature_names' or 'boundaries' arguments are empty or have different lengths.
        """
        if axis_names is None:
            raise ValueError("Argument 'features' must not be None")
        if not hasattr(axis_names, '__iter__') and type(axis_names)!=str:
            raise ValueError("Argument 'features' must be iterable.")
        if boundaries is None:
            raise ValueError("Argument 'boundaries' must not be None")
        if not hasattr(boundaries, '__iter__') and type(axis_names)!=str:
            raise ValueError("Argument 'boundaries' must be iterable.")
        if len(axis_names) != len(boundaries):
            raise ValueError("Features and boundaries must have the same length.")
        if len(axis_names)==0 or len(boundaries)==0:
            raise ValueError("Box can not be created wihtout boundaries")
        self._features : Iterable[str] = axis_names 
        self._boundaries : Iterable[Tuple[np._FloatType]] = boundaries 
    
    def contains_point(self, coord_tuple:Tuple[float], axis_names: Iterable[str] = None) -> bool:
        """Checks if a point (given by its coordinates) falls inside the box.

        Args:
            coord_tuple (Tuple[np._FloatType]): coordinates of the point to be checked.
            axis_names (Iterable[str], optional): names of the axes to be checked. Must match the cardinality of the specified coordinates. If not specified, all the axes defined for the box are checked. Defaults to None.

        Raises:
            ValueError: cardinality of the coordinates or the axis_names does not match.

        Returns:
            bool: whether the point falls indside the box or not.
        """
        if not axis_names and len(coord_tuple)!=len(self._boundaries):
            raise ValueError("Number of coordinates does not match.")
        if axis_names is not None and len(coord_tuple)!=len(axis_names):
            raise ValueError("Number of specified features does not match the coordinates.")

        if axis_names is None:
            # all axes are checked
            for c, (lbound, rbound) in zip(coord_tuple, self._boundaries):
                if c<lbound or c>rbound:
                    return False
        else:
            # just specified axes are checked
            for aname, c in zip(axis_names, coord_tuple):
                lbound, rbound = self._boundaries[self._features.index(aname)]
                if c<lbound or c>rbound:
                    return False
        return True
