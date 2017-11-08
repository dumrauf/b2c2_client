from unittest import TestCase

from mock import patch

from utils.prompt import is_allowed_to_proceed


class TestPrompt(TestCase):
    @patch('__builtin__.raw_input', side_effect=['Y'])
    def test_is_allowed_to_proceed_with_Y_response(self, input):
        self.assertTrue(is_allowed_to_proceed())

    def test_is_allowed_to_proceed_with_non_Y_response(self):
        test_inputs = ['n', 'N', 'no', 'NO', 'No', 'nO', '', '\n']
        for test_input in test_inputs:
            with patch('__builtin__.raw_input', side_effect=[test_input]):
                self.assertFalse(is_allowed_to_proceed())
