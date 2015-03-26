__author__ = 'abodalevsky'

from unittest import TestCase
from market.config import Config


class TestConfig(TestCase):
    def test_init_command_line(self):
        param = [
            '/path/to/file',
            '-storage_host:127.0.0.1',
            '-bim-bom'
        ]

        Config.init(*param)
        self.assertEqual(Config.STORAGE_HOST, '127.0.0.1')
