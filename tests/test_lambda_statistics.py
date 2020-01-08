import unittest

from lambda_statistics.exception import *

class ExceptionTests(unittest.TestCase):
    def test_new_exception(self):
        e = LambdaStatisticsExceptions()
        self.assertIsInstance(e, LambdaStatisticsExceptions)
