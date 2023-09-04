# DSM API Warpper

A simple Syno DSM API warpper using Python

This repo with official document [link](https://www.synology.cn/zh-cn/support/developer#tool)

## Usage(Temp)

### Step 1:  move tmplate to config.py and add your own uri, username and password.
```shell
mv config.template.py config.py
```
### Step 2: Install the requirements
```shell
pip install -r requirements.txt
```

### Step 3: Run main.py


## Todo List
- [x] Build Uniform Requester
- [x] Buid Warpper API using Flask
- [ ] Build Unit Tests
- [x] FileStation API(From FileSatation API Doc version 2023.03)
  - [x] SYNO.FileStation.Info (Provide File Station info)
  - [x] SYNO.FileStation.List (List all shared folders, enumerate files in a shared folder,and get detailed file information.)
  - [x] SYNO.FileStation.Search (Search files on given criteria.)
  - [x] SYNO.FileStation.VirtualFolder（List all mount point folders of virtual file system, e.g., CIFSor ISO.）
  - [x] SYNO.FileStation.Favorite (Add a folder to user's favorites or perform operations on user's favorites.)
  - [x] SYNO.FileStation.Thumb (Get a thumbnail of a file.)
  - [x] SYNO.FileStation.DirSize (Get the total size of files/folders within folder(s).)
  - [x] SYNO.FileStation.MD5 (Get MD5 of a file.)
  - [x] SYNO.FileStation.CheckPermission (Check if the file/folder has permission of a file/folder or not.)
  - [x] SYNO.FileStation.Upload (Upload a file)
  - [x] SYNO.FileStation.Download (Download files/folders.)
  - [x] SYNO.FileStation.Sharing (Generate a sharing link to share files/folders with other people and perform operations on sharing links.)
  - [x] SYNO.FileStation.CreateFolder 
  - [x] SYNO.FileStation.Rename (Rename a file/folder.)
  - [ ] SYNO.FileStation.CopyMove (Copy/Move files/folders.)
  - [x] SYNO.FileStation.Delete (Delete files/folders.)
    - [x] Blocking Delete
    - [x] Non-Blocking Delete
  - [x] SYNO.FileStation.Extract (Extract an archive and perform operations on an archive.)
    - [x] Simple Compleate
    - [ ] Complex logic
  - [x] SYNO.FileStation.Compress (Compress files/folders.)
    - [x] Simple Compleate
    - [ ] Complex logic
  - [x] SYNO.FileStation.BackgroundTask(Get information regarding tasks of file operations which are run as the background process including copy, move, delete, compress and extract tasks or perform operations
    - [x] List
    - [x] Clear Finished Task
on these background tasks.)
- [ ] User API
  - [x] SYNO.API.Auth(Login)
  - [x] SYNO.API.Info(Get All API Info)
- [ ] System Core
  - [x] SYNO.Core.System.info (Get the dsm system info)
  - [x] SYNO.Core.System.Utilization(Get dsm system untilizations)
  - [x] DSMNetwork(Get dsm network infomation)
  - [x] DSMService(Get enable service info)
  - [x] DSMTerminal(Set DSM Terminal Setting)
  - [ ] Others.
- [ ] Download Station API(Synology_Download Station Official API_20140326)