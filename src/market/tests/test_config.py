__author__ = 'abodalevsky'

from unittest import TestCase
from market.config import Config
import logging


class TestConfig(TestCase):
    def test_init_cmd_storage_host(self):
        param = [
            '/path/to/file',
            '-storage_host:127.0.0.1',
            '-bim-bom'
        ]

        Config.init(*param)
        self.assertEqual(Config.STORAGE_HOST, '127.0.0.1')

    def test_init_cmd_log(self):
        param = [
            '/path/to/file',
            '-log:0',
            '-bim-bom'
        ]

        Config.init(*param)
        self.assertEqual(Config.LOG_LEVEL, logging.NOTSET)

        param = [
            '/path/to/file',
            '-log:50'
        ]

        Config.init(*param)
        self.assertEqual(Config.LOG_LEVEL, logging.CRITICAL)

        param = [
            '/path/to/file',
            '-storage_host:127.0.0.1',
            '-log:10'
        ]

        Config.init(*param)
        self.assertEqual(Config.LOG_LEVEL, 10)
        self.assertEqual(Config.STORAGE_HOST, '127.0.0.1')