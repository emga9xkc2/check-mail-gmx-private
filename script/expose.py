
import eel


from script.download import *

from hfile import *

from hwin32 import *

from hotp import *
from hini import *
from hrequest import *
from hthread import *

import script.conn as con

from heel import *

ini = hini()
isPause = False
set_url_tool(con.url_tool)
def checkPause():
    while True:
        if isPause:
            log("Đang tạm ngừng")
            sleep(3)
            continue
        break


def getSetting():
    parser = ConfigParser()
    parser.read(hfile.fixFileName("data/hconfig.ini"))
    confdict = {section: dict(parser.items(section)) for section in parser.sections()}
    confdict["lang"] = getLang()
    return confdict


def setValueCssSelector(selector, html):
    try:
        eel.setValueCssSelector(selector, html)
    except Exception as e:
        print(e)
def setStatus(id, status):
    try:
        eel.setValueCssSelector(f'tr[id="{id}"] *[name="status"]', status)
    except Exception as e:
        print(e)
def setTable(id, nametable, value):
    try:
        eel.setValueCssSelector(f'tr[id="{id}"] *[name="{nametable}"]', value)
    except Exception as e:
        print(e)


@eel.expose
def setPause(pause=False):
    global isPause
    isPause = pause




_isRunning = False

@eel.expose
def setRunning(running):
    global _isRunning
    _isRunning = running
@eel.expose
def isRunning():
    return _isRunning

# @eel.expose
# def getTitle():
#     return con.title
@eel.expose
def updateSetting(name, value):
    ini.write(name, value)
def close_callback(route, websockets):
    print("Web app closed")







@eel.expose
def quit(title):
    try:
        hwnd = hwin32.findWindow(title)
        hwin32.closeWindow(hwnd)
    except Exception as e:
        print(e)
    killApp()


def getLang():
    lang = {}
    lang["Check info youtube"] = "Kiểm tra youtube"
    lang["Check date create"] = "Kiểm tra ngày tạo"
    lang["Change password"] = "Đổi mật khẩu"
    lang["Change email recovery"] = "Đổi email khôi phục"
    lang["Delete phone recovery"] = "Xóa số điện thoại"
    lang["Check phone recovery"] = "Kiểm tra số điện thoại"
    lang["Check phone recovery"] = "Kiểm tra số điện thoại"
    lang["Check google email"] = "Kiểm tra tên gốc"
    lang["Check google voice"] = "Kiểm tra google voice"
    lang["Check payment method"] = "Kiểm tra thanh toán"
    lang["Restore disable"] = "Kháng mail disable"
    lang["Change language en"] = "Đổi ngôn ngữ"
    lang["Check country"] = "Kiểm tra quốc gia"
    lang["Check youtube premium"] = "Kiểm tra youtube premium"
    lang["Close payment method"] = "Đóng thanh toán"
    lang["Delete payment method"] = "Xóa thanh toán"
    lang["Save profile"] = "Lưu profile"
    lang["Confirm security"] = "Xác nhận cảnh báo đăng nhập"
    # lang["Confirm security"] = "Xác nhận cảnh báo đăng nhập"
    lang["Device logout"] = "Đăng xuất thiết bị"
    lang["Create channel youtube"] = "Tạo kênh youtube"
    lang["Change display name"] = "Đổi tên hiển thị"
    lang["Check chplay"] = "Kiểm tra chplay"
    lang["Check hidden phone"] = "Kiểm tra số điện thoại ẩn"
    lang["Stop when password ok"] = "Dừng lại khi đúng mật khẩu"
    lang["Auto move chrome (can lead to account death)"] = "Sắp xếp chrome gọn (có thể tăng khả năng chết nick)"





    lang["Config otp"] = "Cài đặt otp"
    lang["Config captcha"] = "Cài đặt captcha"
    lang["Restore disable content"] = "Nội dung kháng disable"
    lang["Restore disable contact"] = "Mail nhận thư kháng disable"
    lang["Email recovery random"] = "Email khôi phục ngẫu nhiên"
    lang["Email recovery domain"] = "Đuôi email khôi phục"
    lang["Password random"] = "Mật khẩu ngẫu nhiên"
    lang["Active account"] = "Kích hoạt tài khoản"

    lang["Import"] = "Nhập khẩu"
    lang["Dashboard"] = "Bảng điều khiển"
    lang["Setting"] = "Cài đặt"
    lang["Logs"] = "Nhật ký"
    lang["Account"] = "Tài khoản"
    lang["Quit"] = "Thoát chương trình"

    lang["Select"] = "Chọn"
    lang["Copy"] = "Sao chép"
    lang["Select all mails"] = "Chọn tất cả"
    lang["Select mails that has not been run"] = "Chọn mail chưa chạy"
    lang["Select mails has been running"] = "Chọn mail đã chạy"
    lang["Deselect all"] = "Bỏ chọn tất cả"
    lang["Delete selected mails"] = "Xóa tất cả mail đã chọn"
    lang["Export selected mails"] = "Xuất tất cả mail đã chọn"
    lang["Run selected mails"] = "Chạy tất cả mail đã chọn"

    lang["Hide column"] = "Ẩn cột"
    lang["Pause"] = "Tạm ngừng"
    lang["Selected"] = "Đã chọn"
    lang["Current version"] = "Phiên bản hiện tại"
    lang["Update new version"] = "Cập nhật phiên bản mới"
    lang["Open hconfig"] = "Mở file hconfig"

    return lang




@eel.expose
def openFolder(filename):
    hfile.openFolder(filename)

def eel_saveResponse(response, savepath, process):
    folder = hfile.getFolderPath(savepath)
    hfile.createDir(folder)
    total_length = response.headers.get('content-length')

    if total_length is None: # không có thông tin về kích thước file
        with open(savepath, 'wb') as f:
            f.write(response.content)

        eel.update_progress(str(100) +"_" + process)()
    else:
        dl = 0
        total_length = int(total_length)
        with open(savepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    dl += len(chunk)
                    f.write(chunk)
                    percent = dl / total_length * 100
                    eel.update_progress(str(percent) +"_" + process)()
def eel_getIdDrive(id):
    if id.startswith("https://drive.google.com/file/d/"):
        id = id.replace("https://drive.google.com/file/d/", "")
        id = id.split("/")[0]
        id = id.split("?")[0]
    if id.startswith("https://drive.google.com/open?id="):
        id = id.replace("https://drive.google.com/open?id=", "")
        id = id.split("/")[0]
        id = id.split("?")[0]
    return id


def eel_downloadDrive(id, destination, process=None):
    id = eel_getIdDrive(id)
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    params = {"id": id, "confirm": "t"}
    response = session.get(URL, params=params, stream=True)
    token = ""
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break
    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)
    eel_saveResponse(response, destination, process)

@eel.expose
def download_file(url, savepath, process= None):
    response = requests.get(url, stream=True)
    eel_saveResponse(response, savepath, process)
@eel.expose
def close_show_update():
    eel.close_show_update()

def download_file_extract(url, savepath, extract=True, process="1/2", show_progress=False, file_name_show=""):
    if show_progress:
        eel.download_progress(file_name_show)
    savepath = hfile.fixFileName(savepath)
    if url.startswith("https://drive.google.com"):
        eel_downloadDrive(url, savepath, process)
    else:
        download_file(url, savepath, process)
    if extract:
        import zipfile
        folderpath = hfile.getFolderName(savepath)
        fileex = hfile.fixFileName(folderpath)
        with zipfile.ZipFile(savepath, "r") as zip_ref:
            zip_ref.extractall(fileex)
        hfile.delete(savepath)
        dirs = hfile.listDir(folderpath)
        for z in dirs:
            if "-main" in z:
                dir1 = hfile.fixFileName(folderpath + "/" + z)
                hfile.deleteDir(dir1 + "/setup/ProcessManager/")
                hfile.copyDir(dir1, folderpath)
                hfile.deleteDir(dir1)

def autoUpdate():
    dic = dict()
    foldermyscript = hpath.myScript()
    foldermyscriptcheck = foldermyscript.replace("\\", "/")
    if not "/python/myscript" in foldermyscriptcheck:
        versionScript = hfile.fixFileName(foldermyscript + "/version.txt")
        nowversion = hfile.read(versionScript)
        rq = hrequest()
        webVersion = rq.getHtml("https://raw.githubusercontent.com/emga9xkc2/my-script/main/version.txt")
        if webVersion != nowversion:
            print("Downloading myscript")
            download_file_extract("https://github.com/emga9xkc2/my-script/archive/refs/heads/main.zip", hfile.fixFileName(foldermyscript + "/update.zip"), "1/2")
    if con.url_tool:
        download_file_extract(con.url_tool, "update.zip", process="2/2")
    dic["result"] = "Đã cập nhật xong. Hãy tắt tool đi mở lại để dùng phiên bản mới"
    dic["mess"] = "success"
    return dic





