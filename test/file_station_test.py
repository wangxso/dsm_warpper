import unittest
from api.system import DSMLogin
from api.file_station import FileInfo

class FileStationTest(unittest.TestCase):

    def test_FileInfo(self):
        DSMLogin()
        print(FileInfo())



if __name__ == "__main__":
    unittest.main()