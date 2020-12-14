import unittest
from serverlogs.server_logs_utils import ServerLogsValidator


class TestServerLogsValidator(unittest.TestCase):
    """Test cases for testing ServerLogsValidator"""
    correct_data = {
        ('BeastsOfBermuda.log', 'main', 'all', '12345678901234567'): (True, True, True, True),
        ('BeastsOfBermuda-backup-2020.11.13-10.55.33.log', 'main', 'all', '12345678901234567'): (True, True, True, True),
        ('BeastsOfBermuda.log', 'test', 'logins/logouts', '12345678901234567'): (True, True, True, True),
        ('BeastsOfBermuda.log', 'main', 'deaths', '12345678901234567'): (True, True, True, True),
        ('BeastsOfBermuda.log', 'main', 'messages', '01234567890123456'): (True, True, True, True),
    }
    wrong_data = {
        ('BeastsOfBermuda.wrong', 'main', 'all', '12345678901234567'): (False, True, True, True),
        ('BeastsOfBermuda.log', 'wrong', 'logins/logouts', '12345678901234567'): (True, False, True, True),
        ('BeastsOfBermuda.log', 'main', 'wrong', '12345678901234567'): (True, True, False, True),
        ('BeastsOfBermuda.log', 'main', 'deaths', '012345678901234567'): (True, True, True, False),
        ('BeastsOfBermuda.log', 'main', 'deaths', 'wrong'): (True, True, True, False),
    }
    atypical_data = {
        (None, None, None, None): (False, False, False, False),
        (True, False, True, False): (False, False, False, False),
        (0, 1, 2, 3): (False, False, False, False),
        (('BeastsOfBermuda.log',), ('main',), ('all',), ('12345678901234567',)): (False, False, False, False),
    }

    def test_validation_typical(self):
        """Typical valid data"""
        for data, answer in self.correct_data.items():
            validator = ServerLogsValidator(*data)
            self.assertEqual(validator.validation(), answer)

    def test_validation_wrong(self):
        """Wrong data"""
        for data, answer in self.wrong_data.items():
            validator = ServerLogsValidator(*data)
            self.assertEqual(validator.validation(), answer)

    def test_validation_atypical(self):
        """Atypical invalid data"""
        for data, answer in self.atypical_data.items():
            validator = ServerLogsValidator(*data)
            self.assertEqual(validator.validation(), answer)
