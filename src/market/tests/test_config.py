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
        # in addition it verifies that setting fromm command line overwrites INI setting
        self.assertEqual('127.0.0.1', Config.STORAGE_HOST)

    def test_init_cmd_log(self):
        param = [
            '/path/to/file',
            '-bim-bom',
            '-log:0'
        ]

        Config.init(*param)
        self.assertEqual(logging.NOTSET, Config.LOG_LEVEL)

        param = [
            '/path/to/file',
            '-log:50'
        ]

        Config.init(*param)
        self.assertEqual(logging.CRITICAL, Config.LOG_LEVEL)

        param = [
            '/path/to/file',
            '-storage_host:127.0.0.1',
            '-log:10'
        ]

        Config.init(*param)
        self.assertEqual(10, Config.LOG_LEVEL)
        self.assertEqual('127.0.0.1', Config.STORAGE_HOST)

    def test_init_ini_storage(self):
        param = ['/path/to/file']
        Config.init(param)

        self.assertEqual('10.20.30.40', Config.STORAGE_HOST)

    def test_ini_ini_log(self):
        param = ['/path/to/file']
        Config.init(param)

        self.assertEqual(30, Config.LOG_LEVEL)

    def test_ini_no_cmd_passed(self):
        Config.init()
        self.assertEqual(30, Config.LOG_LEVEL)
        self.assertEqual('10.20.30.40', Config.STORAGE_HOST)
