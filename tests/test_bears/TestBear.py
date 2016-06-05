from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.bearlib.abstractions.Lint import Lint


class FirstTestBear(LocalBear):

    def run(self, file, filename, result: bool=False, exception: bool = False):
        if result:
            yield result

        if exception:
            raise ValueError


class SecondTestBear(LocalBear, Lint):

    def run(self, file, filename, result: bool=False, exception: bool = False):
        if result:
            yield result

        if exception:
            raise ValueError


class ThirdTestBear(LocalBear, Lint):

    command = "Winter Is Coming"
    stdout_output = "King In the North!"
    stderr_output = "Fire and Blood"

    def run(self, file, filename, result: bool=False, exception: bool = False):
        if result:
            yield result

        if exception:
            raise ValueError
