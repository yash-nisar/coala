import re
from types import MappingProxyType

from coala_decorators.decorators import assert_right_type

from coalib.misc.Future import partialmethod
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class LinterRegexOutputFormat:
    NAME = "regex" # TODO

    # TODO mark it as "private"?
    @staticmethod
    def prepare_options(**options):
        # TODO Docs
        """
        Do type-checks and other stuff here.

        :return: Return -> yes the modified and prepared options
        """
        if "output_regex" not in options:
            raise ValueError("`output_regex` needed when specified "
                             "output-format {!r}.".format(LinterRegexOutputFormat.NAME))

        options["output_regex"] = re.compile(options["output_regex"])

        # Don't setup severity_map if one is provided by user or if it's not
        # used inside the output_regex. If one is manually provided but not
        # used in the output_regex, throw an exception.
        # FIXME Make out of this case (manually provided severity-map but not
        # FIXME used in the output-regex) a warning instead of an exception.
        if "severity_map" in options:
            if "severity" not in options["output_regex"].groupindex:
                raise ValueError("Provided `severity_map` but named group "
                                 "`severity` is not used in `output_regex`.")
            assert_right_type(options["severity_map"], dict, "severity_map")

            for key, value in options["severity_map"].items():
                assert_right_type(key, str, "severity_map key")

                try:
                    assert_right_type(value, int, "<severity_map dict-value>")
                except TypeError:
                    raise TypeError(
                        "The value {!r} for key {!r} inside given "
                        "severity-map is no valid severity value.".format(
                            value, key))

                if value not in RESULT_SEVERITY.reverse:
                    raise TypeError(
                        "Invalid severity value {!r} for key {!r} inside "
                        "given severity-map.".format(value, key))

            # Auto-convert keys to lower-case. This creates automatically a new
            # dict which prevents runtime-modifications.
            options["severity_map"] = {
                key.lower(): value
                for key, value in options["severity_map"].items()}

        if "result_message" in options:
            assert_right_type(options["result_message"], str, "result_message")

        # Check for illegal superfluous options.
        allowed_options = {"output_regex", "severity_map", "result_message"}
        superfluous_options = options.keys() - allowed_options
        if superfluous_options:
            raise ValueError(
                "Invalid keyword arguments provided: " +
                ", ".join(repr(s) for s in sorted(superfluous_options)))

        return options

    @classmethod
    def set_up(cls, **options):
        # TODO Move that to prepare options?
        cls.process_output = partialmethod(
            cls.process_output_regex,
            **{key: options[key]
               for key in ("output_regex", "severity_map", "result_message")
               if key in options})

    def process_output_regex(
            self, output, filename, file, output_regex,
            severity_map=MappingProxyType({
                "critical": RESULT_SEVERITY.MAJOR,
                "c": RESULT_SEVERITY.MAJOR,
                "fatal": RESULT_SEVERITY.MAJOR,
                "fail": RESULT_SEVERITY.MAJOR,
                "f": RESULT_SEVERITY.MAJOR,
                "error": RESULT_SEVERITY.MAJOR,
                "err": RESULT_SEVERITY.MAJOR,
                "e": RESULT_SEVERITY.MAJOR,
                "warning": RESULT_SEVERITY.NORMAL,
                "warn": RESULT_SEVERITY.NORMAL,
                "w": RESULT_SEVERITY.NORMAL,
                "information": RESULT_SEVERITY.INFO,
                "info": RESULT_SEVERITY.INFO,
                "i": RESULT_SEVERITY.INFO,
                "suggestion": RESULT_SEVERITY.INFO}),
            result_message=None):
        """
        Processes the executable's output using a regex.

        :param output:
            The output of the program. This can be either a single
            string or a sequence of strings.
        :param filename:
            The filename of the file currently being corrected.
        :param file:
            The contents of the file currently being corrected.
        :param output_regex:
            The regex to parse the output with. It should use as many
            of the following named groups (via ``(?P<name>...)``) to
            provide a good result:

            - line - The line where the issue starts.
            - column - The column where the issue starts.
            - end_line - The line where the issue ends.
            - end_column - The column where the issue ends.
            - severity - The severity of the issue.
            - message - The message of the result.
            - origin - The origin of the issue.
            - additional_info - Additional info provided by the issue.

            The groups ``line``, ``column``, ``end_line`` and
            ``end_column`` don't have to match numbers only, they can
            also match nothing, the generated ``Result`` is filled
            automatically with ``None`` then for the appropriate
            properties.
        :param severity_map:
            A dict used to map a severity string (captured from the
            ``output_regex`` with the named group ``severity``) to an
            actual ``coalib.results.RESULT_SEVERITY`` for a result.
        :param result_message:
            The static message to use for results instead of grabbing it
            from the executable output via the ``message`` named regex
            group.
        :return:
            An iterator returning results.
        """

        if isinstance(output, str):
            output = (output,)

        for string in output:
            for match in re.finditer(output_regex, string):
                yield self._convert_output_regex_match_to_result(
                    match, filename, severity_map=severity_map,
                    result_message=result_message)

    # TODO check for proper mixin of process_output method!

