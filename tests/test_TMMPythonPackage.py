import unittest
from ..TMMPythonPackage import TypeTest, GetLoggerDict, FindReplaceList, AddMonths, BashWrapper, TrueBashWrapper
from datetime import date

hello_world = "HELLO WORLD!"

class TestBashWrapper(unittest.TestCase):
		
		def test_valid_command(self):
				output, returncode = BashWrapper("echo 'HELLO WORLD!'")
				self.assertEqual(output.strip(), "'HELLO WORLD!'")
				self.assertEqual(returncode, 0)

		def test_valid_command2(self):
				output, returncode = BashWrapper("echo HELLO WORLD!")
				self.assertEqual(output.strip(), hello_world)
				self.assertEqual(returncode, 0)

		def test_invalid_command(self):
				with self.assertRaises(FileNotFoundError):
						output, returncode = BashWrapper("nonexistent_command")
						
		def test_wrong_argument_type(self):
				with self.assertRaises(TypeError):
						output, returncode = BashWrapper(42) # type: ignore

class TestTrueBashWrapper(unittest.TestCase):
		
		def test_valid_command(self):
				output, returncode = TrueBashWrapper("echo 'HELLO WORLD!'")
				self.assertEqual(output.strip(), hello_world)
				self.assertEqual(returncode, 0)

		def test_valid_command2(self):
				output, returncode = TrueBashWrapper("echo HELLO WORLD!")
				self.assertEqual(output.strip(), hello_world)
				self.assertEqual(returncode, 0)

		def test_invalid_command(self):
				output, returncode = TrueBashWrapper("nonexistent_command")
				self.assertEqual(output.strip(), "")
				self.assertEqual(returncode, 127)

		def test_wrong_argument_type(self):
				with self.assertRaises(TypeError):
						output, returncode = TrueBashWrapper(42) # type: ignore

str_error   = "String expected"
int_error   = "Integer expected"
float_error = "Float expected"
class TestTypeTest(unittest.TestCase):

    def test_valid_input(self):
        # No exception should be raised for valid input
        try:
            TypeTest("test_string", str, str_error)
            TypeTest(42, int, int_error)
            TypeTest(3.14, float, float_error)
        except TypeError:
            self.fail("TypeTest raised TypeError unexpectedly for valid input")

    def test_invalid_input(self):
        # TypeError should be raised for invalid input
        with self.assertRaises(TypeError, msg=str_error):
            TypeTest(42, str, str_error)

        with self.assertRaises(TypeError, msg=int_error):
            TypeTest("test_string", int, int_error)

        with self.assertRaises(TypeError, msg=float_error):
            TypeTest("test_string", float, float_error)

    def test_subclass_instance(self):
        class MyBaseClass:
            pass

        class MyDerivedClass(MyBaseClass):
            pass

        try:
            TypeTest(MyDerivedClass(), MyBaseClass, "error_msg")
        except TypeError:
            self.fail("TypeTest raised TypeError unexpectedly!")

    def test_none_value(self):
        with self.assertRaises(TypeError):
            TypeTest(None, str, "error_msg")

class TestFindReplaceList(unittest.TestCase):

    def test_find_replace(self):
        input_list = ['apple', 'orange', 'apple', 'banana']
        find = 'apple'
        replace = 'grape'
        expected_output = ['grape', 'orange', 'grape', 'banana']
        self.assertEqual(FindReplaceList(find, replace, input_list), expected_output)

    def test_no_match(self):
        input_list = ['apple', 'orange', 'banana']
        find = 'grape'
        replace = 'kiwi'
        expected_output = ['apple', 'orange', 'banana']
        self.assertEqual(FindReplaceList(find, replace, input_list), expected_output)

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            FindReplaceList('apple', 'grape', "this should be a list") # type: ignore

log_path = 'test.log'
class TestGetLoggerDict(unittest.TestCase):

    def test_valid_input_info(self):
        level = 'info'
        logger_dict = GetLoggerDict(level, log_path)

        self.assertEqual(logger_dict['handlers']['console']['level'], level.upper())
        self.assertEqual(logger_dict['handlers']['file']['level'], level.upper())
        self.assertEqual(logger_dict['handlers']['file']['filename'], log_path)
        self.assertEqual(logger_dict['loggers']['default']['level'], level.upper())
        self.assertEqual(logger_dict['root']['level'], level.upper())

    def test_valid_input_DEBUG(self):
        level = 'DEBUG'
        logger_dict = GetLoggerDict(level, log_path)

        self.assertEqual(logger_dict['handlers']['console']['level'], level)
        self.assertEqual(logger_dict['handlers']['file']['level'], level)
        self.assertEqual(logger_dict['handlers']['file']['filename'], log_path)
        self.assertEqual(logger_dict['loggers']['default']['level'], level)
        self.assertEqual(logger_dict['root']['level'], level)

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            GetLoggerDict('invalid_level', log_path)

    def test_invalid_log_path_type(self):
        with self.assertRaises(TypeError):
            GetLoggerDict('info', ['this', 'should', 'be', 'a', 'string']) # type: ignore

    def test_invalid_level_type(self):
        with self.assertRaises(TypeError):
            GetLoggerDict(['this', 'should', 'be', 'a', 'string'], log_path) # type: ignore

class TestAddMonths(unittest.TestCase):

    def test_add_months(self):
        input_date = date(2021, 10, 1)
        expected_output = date(2022, 2, 1)
        self.assertEqual(AddMonths(input_date, 4), expected_output)

    def test_cross_year_boundary(self):
        input_date = date(2021, 11, 30)
        expected_output = date(2022, 1, 30)
        self.assertEqual(AddMonths(input_date, 2), expected_output)

    def test_invalid_input_date_type(self):
        with self.assertRaises(TypeError):
            AddMonths("2021-10-01", 4) # type: ignore

    def test_invalid_add_months_type(self):
        with self.assertRaises(TypeError):
            AddMonths(date(2021, 10, 1), "4") # type: ignore

    def test_add_months_less_than_one(self):
        with self.assertRaises(ValueError):
            AddMonths(date(2021, 10, 1), 0)

    def test_leap_year(self):
        input_date = date(2020, 2, 29)
        expected_output = date(2021, 2, 28)
        self.assertEqual(AddMonths(input_date, 12), expected_output)

    def test_large_add_months_value(self):
        input_date = date(2021, 1, 1)
        expected_output = date(2041, 1, 1)
        self.assertEqual(AddMonths(input_date, 240), expected_output)

    def test_new_month_has_less_days(self):
        input_date = date(2021, 7, 31)
        expected_output = date(2021, 9, 30)
        self.assertEqual(AddMonths(input_date, 2), expected_output)

    def test_new_month_has_more_days(self):
        input_date = date(2021, 4, 30)
        expected_output = date(2021, 7, 30)
        self.assertEqual(AddMonths(input_date, 3), expected_output)

    def test_end_of_century(self):
        input_date = date(2099, 12, 31)
        expected_output = date(2101, 2, 28)
        self.assertEqual(AddMonths(input_date, 14), expected_output)

    def test_leap_century(self):
        input_date = date(2400, 2, 29)
        expected_output = date(2401, 2, 28)
        self.assertEqual(AddMonths(input_date, 12), expected_output)

    def test_date_min_boundary(self):
        input_date = date.min
        expected_output = date(1, 2, 1)
        self.assertEqual(AddMonths(input_date, 1), expected_output)

    def test_date_max_boundary(self):
        input_date = date(9999, 12, 1)
        with self.assertRaises(ValueError):
            AddMonths(input_date, 1)

    def test_negative_month_value(self):
        input_date = date(2021, 3, 1)
        with self.assertRaises(ValueError):
            AddMonths(input_date, -1)

if __name__ == '__main__':
    unittest.main()