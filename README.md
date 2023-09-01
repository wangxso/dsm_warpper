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
- [ ] Build Uniform Requester
- [ ] Buid Warpper API using Flask
- [ ] FileStation API(From FileSatation API Doc version 2023.03)
  - [ ] SYNO.FileStation.Info (Provide File Station info)
  - [ ] SYNO.FileStation.List (List all shared folders, enumerate files in a shared folder,and get detailed file information.)
  - [ ] SYNO.FileStation.Search (Search files on given criteria.)
  - [ ] SYNO.FileStation.VirtualFolder（List all mount point folders of virtual file system, e.g., CIFSor ISO.）
  - [ ] SYNO.FileStation.Favorite (Add a folder to user's favorites or perform operations on user's favorites.)
  - [ ] SYNO.FileStation.Thumb (Get a thumbnail of a file.)
  - [ ] SYNO.FileStation.DirSize (Get the total size of files/folders within folder(s).)
  - [ ] SYNO.FileStation.MD5 (Get MD5 of a file.)
  - [ ] SYNO.FileStation.CheckPermission (Check if the file/folder has permission of a file/folder or not.)
  - [x] SYNO.FileStation.Upload (Upload a file)
  - [x] SYNO.FileStation.Download (Download files/folders.)
  - [ ] SYNO.FileStation.Sharing (Generate a sharing link to share files/folders with other people and perform operations on sharing links.)
  - [x] SYNO.FileStation.CreateFolder 
  - [x] SYNO.FileStation.Rename (Rename a file/folder.)
  - [ ] SYNO.FileStation.CopyMove (Copy/Move files/folders.)
  - [ ] SYNO.FileStation.Delete (Delete files/folders.)
  - [ ] SYNO.FileStation.Extract (Extract an archive and perform operations on an archive.)
  - [ ] SYNO.FileStation.Compress (Compress files/folders.)
  - [ ] SYNO.FileStation.BackgroundTask(Get information regarding tasks of file operations which are run as the background process including copy, move, delete, compress and extract tasks or perform operations
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
- [ ] Download Station API(Synology_Download Station Official API_20140326)