import unittest
from api import system
class SystemTest(unittest.TestCase):

    def test_LoginErrorUsername(self):
        resp = system.DSMLogin('xxx', 'xxx')
        self.assertFalse(resp['success'])
    

if __name__ == '__main__':
    unittest.main()