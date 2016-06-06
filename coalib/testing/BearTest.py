from unittest import TestCase


class BearTest(TestCase):
    # Let this field be unique, so we use `object()`.
    DONT_CARE = object()

    @classmethod
    def make_local_bear_test(cls):
        # take in additional parameters for checking and return a ready class.
        pass

    @classmethod
    def make_global_bear_test(cls):
        pass

    def check_validity(self):
        pass

    def check_invalidity(self):
        pass

    def check(self):
        # For result checking
        pass
