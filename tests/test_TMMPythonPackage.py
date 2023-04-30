import unittest
from TMMPythonPackage import TypeTest, GetLoggerDict, FindReplaceList, AddMonths, BashWrapper ,TrueBashWrapper

class TestBashWrapper(unittest.TestCase):
		
		def test_valid_command(self):
				output, returncode = BashWrapper("echo 'Hello, World!'")
				self.assertEqual(output.strip(), "'Hello, World!'")
				self.assertEqual(returncode, 0)

		def test_valid_command2(self):
				output, returncode = BashWrapper("echo Hello, World!")
				self.assertEqual(output.strip(), "Hello, World!")
				self.assertEqual(returncode, 0)

		def test_invalid_command(self):
				with self.assertRaises(FileNotFoundError):
						output, returncode = BashWrapper("nonexistent_command")
						
		def test_wrong_argument_type(self):
				with self.assertRaises(TypeError):
						output, returncode = BashWrapper(42)

class TestTrueBashWrapper(unittest.TestCase):
		
		def test_valid_command(self):
				output, returncode = TrueBashWrapper("echo 'Hello, World!'")
				self.assertEqual(output.strip(), "Hello, World!")
				self.assertEqual(returncode, 0)

		def test_valid_command2(self):
				output, returncode = TrueBashWrapper("echo Hello, World!")
				self.assertEqual(output.strip(), "Hello, World!")
				self.assertEqual(returncode, 0)

		def test_invalid_command(self):
				output, returncode = TrueBashWrapper("nonexistent_command")
				self.assertEqual(output.strip(), "")
				self.assertEqual(returncode, 127)

		def test_wrong_argument_type(self):
				with self.assertRaises(TypeError):
						output, returncode = TrueBashWrapper(42)

class TestTypeTest(unittest.TestCase):

    def test_valid_input(self):
        # No exception should be raised for valid input
        try:
            TypeTest("test_string", str, "String expected")
            TypeTest(42, int, "Integer expected")
            TypeTest(3.14, float, "Float expected")
        except TypeError:
            self.fail("TypeTest raised TypeError unexpectedly for valid input")

    def test_invalid_input(self):
        # TypeError should be raised for invalid input
        with self.assertRaises(TypeError, msg="String expected"):
            TypeTest(42, str, "String expected")

        with self.assertRaises(TypeError, msg="Integer expected"):
            TypeTest("test_string", int, "Integer expected")

        with self.assertRaises(TypeError, msg="Float expected"):
            TypeTest("test_string", float, "Float expected")

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
            FindReplaceList('apple', 'grape', "this should be a list")

class TestGetLoggerDict(unittest.TestCase):

    def test_valid_input(self):
        level = 'info'
        log_path = 'test.log'
        logger_dict = GetLoggerDict(level, log_path)

        self.assertEqual(logger_dict['handlers']['console']['level'], level.upper())
        self.assertEqual(logger_dict['handlers']['file']['level'], level.upper())
        self.assertEqual(logger_dict['handlers']['file']['filename'], log_path)
        self.assertEqual(logger_dict['loggers']['default']['level'], level.upper())
        self.assertEqual(logger_dict['root']['level'], level.upper())

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            GetLoggerDict('invalid_level', 'test.log')

    def test_invalid_log_path_type(self):
        with self.assertRaises(TypeError):
            GetLoggerDict('info', ['this', 'should', 'be', 'a', 'string'])

    def test_invalid_level_type(self):
        with self.assertRaises(TypeError):
            GetLoggerDict(['this', 'should', 'be', 'a', 'string'], 'test.log')

if __name__ == '__main__':
    unittest.main()