import csv
from typing import Iterable
from clingo.symbol import Symbol
import numpy as np
from clingo import Function, Number, String


class DataParser:
    def __init__(self,
                 data: Iterable[Iterable] = None,
                 feature_names: Iterable[str] = None,
                 target: str = None):
        # self._data = None
        self._features = None
        self._target = None
        self._facts = None

    def from_csv(self,
                 csv_path: str,
                 delimiter: str = ',',
                 quotechar: str = '"',
                 feature_names: Iterable[str] = None,
                 column_labels=True):
        def process_row(row, nline):
            self._facts = np.append(
                self._facts, Function('instance', [Number(nline)], True))
            for v, i in zip(row, range(len(row))):
                self._facts = np.append(
                    self._facts,
                    Function('value', [
                        Number(nline),
                        String(self._features[i]),
                        Number(int(v))
                    ], True))

        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=delimiter,
                                quotechar=quotechar)
            nline = 1

            # Getting feature names
            if feature_names is not None:  # given by user
                self._features = np.array(feature_names)
            elif column_labels == True:  # gets them from the file
                self._features = np.array(next(reader))

            if self._features is not None:  # when features is already set
                self._facts = np.array(
                    [Function('feature', [String(f)]) for f in self._features])
            else:  # when features is not set yet
                self._features = np.empty((0, ))
                self._facts = np.empty((0, ))
                row = next(reader)
                for i in range(len(row)):
                    self._features = np.append(self._features, f'ax{i}')
                    self._facts = np.append(
                        self._facts, Function('feature', [String(f'ax{i}')]))
                process_row(row, nline)

            for row in reader:
                process_row(row, nline)
                nline += 1

    def to_file(self, output_path: str):
        def fact_lines():
            len_features = len(self._features)
            len_rows = len_features + 1
            yield self._facts[0:len_features]
            for i in range(len_features, len(self._facts), len_rows):
                yield self._facts[i:i + len_rows]

        with open(output_path, "w") as output_file:
            if self._features is None:
                output_file.write(" ".join([str(f) + "."
                                            for f in self._facts]))
            else:
                output_file.write("\n".join([
                    " ".join([str(f) + "." for f in c]) for c in fact_lines()
                ]))
