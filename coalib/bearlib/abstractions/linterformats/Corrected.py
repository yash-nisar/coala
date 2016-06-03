from coala_decorators.decorators import assert_right_type

from coalib.misc.Future import partialmethod
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


def _prepare_options(options):
    if (
            "diff_severity" in options and
            options["diff_severity"] not in RESULT_SEVERITY.reverse):
        raise TypeError("Invalid value for `diff_severity`: " +
                        repr(options["diff_severity"]))

    if "result_message" in options:
        assert_right_type(options["result_message"], str, "result_message")

    if "diff_distance" in options:
        assert_right_type(options["diff_distance"], int, "diff_distance")

    # TODO DOcument that processed options shall be yielded
    # TODO so there's: The setup phase and the class creation phase
    return {"diff_severity", "result_message", "diff_distance"}


def _create_format_class(options):
    class CorrectedFormatClass:
        def process_output_corrected(self,
                                     output,
                                     filename,
                                     file,
                                     diff_severity=RESULT_SEVERITY.NORMAL,
                                     result_message="Inconsistency found.",
                                     diff_distance=1):
            """
            Processes the executable's output as a corrected file.

            :param output:
                The output of the program. This can be either a single
                string or a sequence of strings.
            :param filename:
                The filename of the file currently being corrected.
            :param file:
                The contents of the file currently being corrected.
            :param diff_severity:
                The severity to use for generating results.
            :param result_message:
                The message to use for generating results.
            :param diff_distance:
                Number of unchanged lines that are allowed in between two
                changed lines so they get yielded as one diff. If a negative
                distance is given, every change will be yielded as an own diff,
                even if they are right beneath each other.
            :return:
                An iterator returning results containing patches for the
                file to correct.
            """
            if isinstance(output, str):
                output = (output,)

            for string in output:
                for diff in Diff.from_string_arrays(
                        file,
                        string.splitlines(keepends=True)).split_diff(
                            distance=diff_distance):
                    yield Result(self,
                                 result_message,
                                 affected_code=diff.affected_code(filename),
                                 diffs={filename: diff},
                                 severity=diff_severity)

        process_output = partialmethod(
            process_output_corrected,
            **{key: options[key]
               for key in ("result_message", "diff_severity", "diff_distance")
               if key in options})

    return CorrectedFormatClass


def create_corrected_format_class(options):
    # Yield the name of the output-format
    yield "corrected"

    # Prepare and check options
    yield _prepare_options(options)

    # Set up the format mixin class
    yield _create_format_class(options)
