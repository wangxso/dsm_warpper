import unittest
from api import file_station, system
from main import session
from config import USRNAME, PASSWORD
class FileStationTest(unittest.TestCase):
    def setUp(self) -> None:
        system.DSMLogin(USRNAME, PASSWORD)
        return super().setUp()

    def tearDown(self) -> None:
        session.close()
        return super().tearDown()
    
    def test_FileInfo(self):
        
        res = file_station.FileInfo()
        self.assertTrue(res['success'])
    
    def test_FileDownload(self):
        res = file_station.FileDownload("/Download/test.jpg")
        self.assertTrue(res['success'])

    def test_CreateFolder(self):
        res = file_station.CreateFolder('/Download', 'test_1')
        self.assertTrue(res['success'])
    def test_RenameFileorFolder(self):
        res = file_station.RenameFileorFolder('/Download/test_1', 'test_2')
        self.assertTrue(res['success'])
    
    def test_BlockingFileDelete(self):
        res = file_station.DeleteFolderOrFiles('/Download/test_2')
        self.assertTrue(res['success'])
    
    def test_FolderList(self):
        res = file_station.FolderList()
        self.assertTrue(res['success'])
if __name__ == "__main__":
    unittest.main()