import unittest
import logging
import os

MODULE_PATH = "linuxgravatar/settings.py"
MODULE_NAME = "GravatarSettings"
import importlib
import sys
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module 
spec.loader.exec_module(module)

class Tests(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)
    config_file = '/tmp/gravatar_settings_test.cfg' 
    settings = module.GravatarSettings('Settings', config_file)   

    def test_settings_file_path(self):
        home_path = os.path.expanduser('~')
        self.file_path = module.settings_location()
        self.assertEqual(self.file_path, home_path+'/.gravatar_settings.cfg')

    def test_settings_write_to_location(self):
        self.settings.write_config_file(self.config_file)

    def test_write_settings_config(self):
        self.settings.save_to_config('username', 'testuser')

    def test_settings_read_config(self):
        username = self.settings.read_config('username')
        self.assertEqual(username, 'testuser')

if __name__=='__main__':
    unittest.main()
