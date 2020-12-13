import unittest
from serverlogs.server_logs_utils import ServerLogsValidator


class TestServerLogsValidator(unittest.TestCase):
    """Test cases for testing ServerLogsValidator"""

    def test_validation_typical(self):
        """Typical valid data"""
        correct_data = ('BeastsOfBermuda.log', 'main', 'all', '12345678901234567')
        validator = ServerLogsValidator(*correct_data)
        self.assertEqual(validator.validation(), (True, True, True, True))
