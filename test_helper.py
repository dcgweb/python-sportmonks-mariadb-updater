import unittest
import helper

# assertEqual(a, b) a == b
# assertNotEqual(a, b) a!= b
# assertTrue(a) bool(a) is True
# assertFalse(a) bool(a) is False
# assertIs(a, b) a is b
# assertIsNot(a, b) a is not b
# assertIsNone(a) a is None
# assertIsNotNone(a) a is not None
# assertIn(a, b) a in b
# assertNotIn(a, b) a not in b
# assertIsInstance(a, b) isinstance(a, b)
# assertIsNotInstance(a, b) not isinstance(a, b)

class TestHelper(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_keys_from_dict__with_empty_params(self):

        self.assertFalse(helper.get_keys_from_dict(None, None, None))
        self.assertFalse(helper.get_keys_from_dict('', '', ''))
        self.assertFalse(helper.get_keys_from_dict(None, '', ''))
        self.assertFalse(helper.get_keys_from_dict('', None, ''))
        self.assertFalse(helper.get_keys_from_dict('', '', None))
        self.assertFalse(helper.get_keys_from_dict(None, '', None))
        self.assertFalse(helper.get_keys_from_dict(None, None, ''))
        self.assertFalse(helper.get_keys_from_dict('', None, None))
        self.assertFalse(helper.get_keys_from_dict(True, None, None))
        self.assertFalse(helper.get_keys_from_dict(True, True, True))
        self.assertFalse(helper.get_keys_from_dict(False, False, False))

    def test_get_keys_from_dict__with_non_ascii_params(self):
        self.assertFalse(helper.get_keys_from_dict([], "भारत网络קוםஇந்தியா®", False))
        self.assertFalse(helper.get_keys_from_dict([{'id': 5, 'name': 'lorem ipsum'}], "भारत网络קוםஇந்தியா®", False))
        self.assertFalse(helper.get_keys_from_dict([{'id': 5, 'name': 'lorem त网络קוםஇந் ipsum'}], "भारत网络קוםஇந்தியா®", False))

    def test_get_keys_from_dict__with_wrong_type_params(self):
        self.assertFalse(helper.get_keys_from_dict([{}], int(5), str(False)))
        self.assertFalse(helper.get_keys_from_dict([{}], True, int(False)))

    def test_get_keys_from_dict__for_some_edge_cases(self):
        self.assertEqual(helper.get_keys_from_dict([{'id': 5, 'name': 'lorem ipsum'}], 'id', False), [5])
        self.assertEqual(helper.get_keys_from_dict([{'id': 5, 'name': 'lorem ipsum'}, {'id': 34, 'flowrate': 3.54}], 'id', True), '5,34')


    def test_get_keys_from_db_dataset_empty_params(self):

        self.assertFalse(helper.get_keys_from_db_dataset(None, None, None))
        self.assertFalse(helper.get_keys_from_db_dataset('', '', ''))
        self.assertFalse(helper.get_keys_from_db_dataset(None, '', ''))
        self.assertFalse(helper.get_keys_from_db_dataset('', None, ''))
        self.assertFalse(helper.get_keys_from_db_dataset('', '', None))
        self.assertFalse(helper.get_keys_from_db_dataset(None, '', None))
        self.assertFalse(helper.get_keys_from_db_dataset(None, None, ''))
        self.assertFalse(helper.get_keys_from_db_dataset('', None, None))
        self.assertFalse(helper.get_keys_from_db_dataset(True, None, None))
        self.assertFalse(helper.get_keys_from_db_dataset(True, True, True))
        self.assertFalse(helper.get_keys_from_db_dataset(False, False, False))

if __name__ == "__main__":
    unittest.main()