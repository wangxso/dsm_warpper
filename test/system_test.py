import unittest
from api import system
from config import USRNAME, PASSWORD
from loguru import logger

class SystemTest(unittest.TestCase):

    def test_LoginErrorUsername(self):
        resp = system.DSMLogin('xxx', 'xxx')
        logger.info(resp)
        self.assertFalse(resp['success'])
    
    def test_DSMInfo(self):
        system.DSMLogin(USRNAME, PASSWORD)
        res = system.DSMInfo()
        logger.info(res)
        self.assertTrue(res['success'])

if __name__ == '__main__':
    unittest.main()