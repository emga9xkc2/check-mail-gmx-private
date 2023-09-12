import sys,  os,  time







# PYTHONPATH=...


class hfile2:
    def dirScript():
        file_path = sys.path[0]
        if not ":" in file_path:
            file_path = os.getcwd()
        return file_path

    def fixFileName(filename):
        platform = sys.platform
        if platform.endswith("win32"):
            if not ":" in filename:
                filename = hfile2.dirScript() + "/" + filename
        filename = filename.replace("\\", "/")
        while True:
            if "//" in filename:
                filename = filename.replace("//", "/")
            else:
                break
        if platform.endswith("win32"):
            filename = filename.replace("/", "\\")
        elif platform.startswith("linux"):
            filename = filename.replace("\\", "/")
        return filename

    def listDir(dir2):
        dir2 = hfile2.fixFileName(dir2)
        return next(os.walk(dir2))[1]

    def copyDir(src, dst):
        try:
            from distutils.dir_util import copy_tree
            src = hfile2.fixFileName(src)
            dst = hfile2.fixFileName(dst)
            copy_tree(src, dst)
        except Exception as e:
            pass

    def createDir(dir):
        dir = hfile2.fixFileName(dir)
        os.makedirs(dir, exist_ok=True)

    def checkExists(fileorfoler):
        fileorfoler = hfile2.fixFileName(fileorfoler)
        if fileorfoler == None:
            return False
        return os.path.exists(fileorfoler)

    def writeFile(filename, text):
        f = open(filename, "w", encoding="utf-8")
        f.write(text)
        f.close()

    def readFile(filename):
        try:
            f = open(filename, "r", encoding="utf-8")
            return f.read()
        except:
            return ""

    def deleteDir(dir):
        try:
            import shutil
            dir = hfile2.fixFileName(dir)
            shutil.rmtree(dir)
        except:
            pass

    def deleteFile(filename):
        try:
            os.remove(filename)
        except Exception as e:
            print("removeFile", e)
            pass

    def extractZip(pathzip, folder, filenamedes=None):
        import zipfile
        if not filenamedes:
            filenamedes = pathzip
        filenamedes = filenamedes.replace("hplaywright", "h")
        print("Extracting: " + filenamedes)
        pathzip = hfile2.fixFileName(pathzip)
        folder = hfile2.fixFileName(folder)
        with zipfile.ZipFile(pathzip, "r") as zip_ref:
            folderextract = hfile2.fixFileName(folder)
            zip_ref.extractall(folderextract)
        hfile2.deleteFile(pathzip)
        print("Extract Success")

hfile2.createDir("/data/")





def startThread(funcname, list_args=None):
    import threading
    if not list_args:
        list_args = []
    tuple_args = tuple(list_args)
    thread = threading.Thread(target=funcname, args=tuple_args)
    thread.isDaemon = True
    thread.start()
    return thread


def getIdDrive(id):
    if id.startswith("https://drive.google.com/file/d/"):
        id = id.replace("https://drive.google.com/file/d/", "")
        id = id.split("/")[0]
        id = id.split("?")[0]
    return id


def downloadDrive(id, destination, filenamedes=None):
    import requests
    id = getIdDrive(id)
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    params = {"id": id, "confirm": "t"}
    if not filenamedes:
        filenamedes = id
    print("Downloading " + filenamedes)
    response = session.get(URL, params=params, stream=True)
    token = ""
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break
    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)
    saveResponse(response, destination)


def download(url: str, fname: str):
    import requests
    resp = requests.get(url, stream=True)
    saveResponse(resp, fname)


def saveResponse(resp, fname):
    from tqdm import tqdm
    total = int(resp.headers.get("content-length", 0))
    # Can also replace 'file' with a io.BytesIO object
    with open(fname, "wb") as file, tqdm(
        desc="Downloading",
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    print("Download Success")

# import elevate
def createShortcut(title, target="", wDir="", arguments="", icon=""):
    try:
        # elevate.elevate(True)
        if title == "" or title == ".lnk":
            title = "Main.lnk"
        if os.path.exists(title):
            return

        path = hfile2.fixFileName(title)
        target = hfile2.fixFileName(target)
        wDir = hfile2.fixFileName(wDir)
        arguments = hfile2.fixFileName(arguments)
        icon = hfile2.fixFileName(icon)
        if not hfile2.checkExists(icon):
            icon = hfile2.fixFileName("setup/images/icon.ico")
        from win32com.client import Dispatch

        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.Arguments = arguments
        shortcut.WorkingDirectory = wDir
        shortcut.WindowStyle = 1
        if icon == "":
            pass
        else:
            shortcut.IconLocation = icon
        shortcut.save()
    except Exception as e:
        print(e)
        pass


def roaming():
    platform = sys.platform
    if platform.endswith("win32"):
        d = "~/appdata/roaming"
    elif platform.startswith("linux"):
        d = "~/.local/share"
    elif platform.endswith("darwin"):
        d = "~/Library/Application Support"
    else:
        d = "~"
    return os.path.abspath(os.path.expanduser(d))


roamingPath = roaming()
scriptPath_Old = roamingPath + "\\myscript\\"
hfile2.deleteDir(scriptPath_Old)
scriptPath = roamingPath + "\\nightowl\\myscript\\"
orbitaPath = roamingPath + "\\nightowl\\orbita\\"
dolphin_path = roamingPath + "\\nightowl\\dolphin\\"
cefPath = roamingPath + "\\nightowl\\cef\\"
bitPath = roamingPath + "\\nightowl\\bit\\"
tempPath = roamingPath + "\\nightowl\\temp\\"
chromeProfile = roamingPath + "\\nightowl\\chrome\\"
sshPath = roamingPath + "\\nightowl\\ssh\\"
hfile2.createDir(sshPath)
hfile2.createDir(scriptPath)
hfile2.createDir(orbitaPath)
hfile2.createDir(cefPath)
hfile2.createDir(bitPath)
hfile2.createDir(tempPath)


def md5(str2):
    import hashlib
    return hashlib.md5(str2.encode("utf-8")).hexdigest()


def fixFileGithub(url, folderMain, folderExtract):
    if "/my-script/" in url:
        if hfile2.checkExists(folderMain):
            hfile2.copyDir(folderMain, folderExtract)
            hfile2.deleteDir(folderMain)


def downloadExtract(url, folderExtract, fileNameCheckDownloadDone=None):
    if fileNameCheckDownloadDone:
        if folderExtract in fileNameCheckDownloadDone:
            fileNameCheckDownloadDone = fileNameCheckDownloadDone.replace(folderExtract, "")
        if hfile2.checkExists(folderExtract + "//" + fileNameCheckDownloadDone):
            return
    tempFile = tempPath + md5(url) + ".zip"
    if url.startswith("https://drive.google.com"):
        downloadDrive(url, tempFile, fileNameCheckDownloadDone)
    else:
        download(url, tempFile)
    hfile2.extractZip(tempFile, folderExtract, fileNameCheckDownloadDone)
    fixFileGithub(url, folderExtract + "/my-script-main/", folderExtract)
    if fileNameCheckDownloadDone:
        return downloadExtract(url, folderExtract, fileNameCheckDownloadDone)



downloadSSH = True
sshPath_check = sshPath + "stnlc.exe"
downloadOrbita110 = True
dolphin_browser_check = dolphin_path + "dolphin-anty-114\\anty.exe"
dolphin_browser_profile_preferences = dolphin_path + "profiles\\zero_profile\\Default\\User Preferences"
dolphin_browser_link_exe = "https://drive.google.com/file/d/1bLVP94P6_1gWunJ279VjvMnJ45lQCqrx/view?usp=sharing"
dolphin_browser_profile_preferences_link = "https://drive.google.com/file/d/1bL0Vh30-y1XTT8BF7a6jbiHA8yfMNNaN/view?usp=sharing"
orbita_browser_check = orbitaPath + "orbita-browser-110\\chrome.exe"
orbita_font_check = orbitaPath + "fonts\\noto_sans_cjk_sc_black.otf"
orbita_profiles_check = orbitaPath + "profiles\\zero_profile\\Default\\Preferences"
scriptPath_check = scriptPath + "hplaywright.py"
useBrowser = ["bit", "orbita", "chrome"]


# fail = False
# try:
#     browsertxt = hfile2.fixFileName("data\\browser.txt")
#     useBrowser1 = int(browsertxt)
# except:
#     fail = True
#     useBrowser1 = 0
# try:
#     if fail:
#         hfile2.writeFile(browsertxt, "0")
# except:
#     pass
useBrowser = useBrowser[1]
# while 1:
#     print("stop")
#     time.sleep(1)
# useBrowser = useBrowser[useBrowser1]
bit_browser_check = bitPath + "bit-browser-112\\BitBrowser.exe"
bit_data_check = bitPath + "data\\a367f26db2354312bbe08c14a6c5fcb4_28520231329"
def getBrowser(browser_name=None):
    if browser_name == "dolphin":
        return dolphin_browser_check
    if useBrowser == "bit":
        return bit_browser_check
    if useBrowser == "orbita":
        return orbita_browser_check

cef_check = cefPath + r"bin\libcef.dll"
def downloadThread():
    downloadExtract("https://drive.google.com/file/d/1bICZOz7MQnoEYOJZoz0VD5_UrZ7ptlSC/view?usp=sharing", cefPath, cef_check)
    downloadExtract("https://github.com/emga9xkc2/my-script/archive/refs/heads/main.zip", scriptPath, scriptPath_check)


    if useBrowser == "orbita":
        if not hfile2.checkExists(orbita_browser_check):
            hfile2.deleteFile(orbita_profiles_check)
        downloadExtract("https://drive.google.com/file/d/1k7_ZoqPNWqMZT2URZQLWcZD5_bGZ84JD/view?usp=sharing", orbitaPath, orbita_browser_check)
        downloadExtract("https://drive.google.com/file/d/1iTU2PH7Y8kmD1pHHW1C6pYcR0yxaQx-5/view?usp=sharing", orbitaPath, orbita_font_check)
        downloadExtract("https://drive.google.com/file/d/1ieSpNuItcE2-1syKDhZmDe6TPDBLMTMX/view?usp=sharing", orbitaPath, orbita_profiles_check)

    if downloadSSH:
        downloadExtract("https://drive.google.com/file/d/1icrqJrA0tcvhBL1FBwL8XHovZ1stllry/view?usp=sharing", sshPath, sshPath_check)


startThread(downloadThread)

scriptPathAppend = "D:/Google Drive/My Data/python/myscript/"
if not os.path.exists(scriptPathAppend):
    scriptPathAppend = scriptPath


def setupPythonPath(title):
    filename = "main.py"
    filename = hfile2.fixFileName(filename)
    if not hfile2.checkExists(filename):
        filename = "main.pyc"
        filename = hfile2.fixFileName(filename)
    createShortcut(title.split("_")[0].strip().upper() + ".lnk", r"C:\Windows\py.exe", "", '"' + filename + '"', "web/static/favicon.ico")

import socket
def free_port() -> int:
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(("127.0.0.1", 0))
    free_socket.listen(1)
    port: int = free_socket.getsockname()[1]
    free_socket.close()
    return port

printer = False
lasttime = time.time()


def waitDownload(path):
    global printer, lasttime
    if printer:
        if time.time() - lasttime > 20:
            lasttime = time.time()
        else:
            return
    path = path.replace("hplaywright", "h")
    print("Wait download", path)
    printer = True

useOrbita = False
while True:
    if not hfile2.checkExists(scriptPath_check):
        waitDownload(scriptPath_check)
        time.sleep(1)
        continue
    elif not hfile2.checkExists(cef_check) :
        waitDownload(cef_check)
        time.sleep(1)
        continue
    elif not hfile2.checkExists(orbita_browser_check) and useBrowser == "orbita" and useOrbita:
        waitDownload(orbita_browser_check)
        time.sleep(1)
        continue
    elif not hfile2.checkExists(orbita_font_check) and useBrowser == "orbita" and useOrbita:
        waitDownload(orbita_font_check)
        time.sleep(1)
        continue
    elif not hfile2.checkExists(orbita_profiles_check) and useBrowser == "orbita" and useOrbita:
        waitDownload(orbita_profiles_check)
        time.sleep(1)
        continue
    else:
        break
# print("Download done")
