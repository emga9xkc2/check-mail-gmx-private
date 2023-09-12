import time
t = time.time()
from script.download import *
title = "Gmail Manage"
setupPythonPath(title)
sys.path.append(scriptPathAppend)

import script.conn as con
con.title = title

from hwin32 import *
from hthread import *


from script.expose import *
hwin32.hideWindowTitle(con.title.split("_")[0].strip().upper(), useThread=True, hideEndswithPyc=True)

from hwin import *
hwin.killAppF4()

from hini import *
ini = hini()

from script.sqlalchemy import  or_, func
from script.sqlalchemy import mailTable, Database, mailClass, Result, Config



from reload import *
# from hexcel import *
# excel = hexcel()


# rq = hrequest()
# html = rq.post("http://192.168.100.1/api/json", '{"fid":"login","username":"","password":"admin","sessionId":null}', getStr=True)
# session = hstr.regexJson(html, "session")
# html = rq.post("http://192.168.100.1/api/json", '{"fid":"switchSimCard","fields":{"password":"","simCardCurrent":1},"sessionId":"'+session+'"}', getStr=True)
# print(html)

# count = 2
# if count:
#     if count % 2 == 0:
#         motnua = count / 2
#         accept = count / 2

def proxy6(api_key):
    from hrand import hrand
    import random
    while True:
        try:
            rq = hrequest()
            html = rq.post(f"https://proxy6.net/api/{api_key}/getproxy", "state=all&limit=10000", getDict=True)
            my_dict = html.get("list", "")
            if not my_dict:
                print("No proxy in proxy6.net. Please buy proxy")
                sleep(10)
                continue
            random_key = random.choice(list(my_dict.keys()))
            random_value = my_dict[random_key]
            host = random_value.get("host", "")
            port = random_value.get("port", "")
            user = random_value.get("user", "")
            pwd = random_value.get("pass", "")
            return f"{host}:{port}:{user}:{pwd}"
        except Exception as e:
            print(e)
            pass

def proxy_sheet(id_google_sheet):
    from hrand import hrand
    import random
    while True:
        try:
            rq = hrequest()

            html = rq.getHtml(f"https://docs.google.com/spreadsheets/d/{id_google_sheet}/gviz/tq?tqx=out:html&tq&gid=1")
            proxys = hstr.regex2(html,"<td>(\\d{1,3}.\\d{1,3}.\\d{1,3}.\\d{1,3}:\\d{2,6}:\\w+:\\w+)</td>")
            if not proxys:
                print(f"No proxy in google sheet {id_google_sheet}. Please add proxy")
                sleep(10)
                continue
            proxy = hrand.randomItemInList(proxys)
            return proxy
        except Exception as e:
            print(e)
            pass

@eel.expose
def loadSetting():
    try:
        lang_en = {
            "checkinfoyoutube": "Check info youtube",
            "checkdatecreate": "Check date create",
            "changepass": "Change password",
            "changeemailrecovery": "Change email recovery",
            "deletephonerecovery": "Delete phone recovery",
            "checkgoogleemail": "Check google email",
            "checkchplay": "Check chplay",
            "checkgooglevoice": "Check google voice",
            "checkpaymentmethod": "Check payment method",
            "deletepaymentmethod": "Delete payment method",
            "checkreviewgooglemap": "Check review google map",
            # "checklivedie": "Check live die",
            "restoredisable": "Restore disable",
            "changelanguage": "Change language en",
            "checkgoogleadw": "Check google adw",
            "checkphonerecovery": "Check phone recovery",
            "checkcountry": "Check country",
            # "checkcountry": "Check country",

            # "checkgoogleadsense": "Check google adsense",
            "devicelogout": "Device logout",
            "closepaymentmethod": "Close payment method",
            "createchannelyoutube": "Create channel youtube",
            "confirmsecurity": "Confirm security",
            "get2facode": "Get 2FA code",
            "stopwhenpasswordsuccess": "Stop when password ok",
            "verifyphone": "Verify phone",
            "youtubeverify": "Verify youtube",
            "checkyoutubepremium": "Check youtube premium",
            "changedisplayname": "Change display name",
            "checkhiddenphone": "Check hidden phone",
            "saveprofile": "Save profile",

            # "automovechrome": "Auto move chrome (can lead to account death)",
            "disableforwarding": "Disable forwarding mail"
        }
        return Result(data=lang_en).to_dict()
    except Exception as e:
        return Result(False, "adding mails failed", e.args).to_dict()

hidecolumns = {}

@eel.expose
def loadHideColumn():
    global hidecolumns
    if hidecolumns:
        return Result(data=hidecolumns).to_dict()
    listshow = ["id", "datecreate", "youtube", "country", "googlevoice", "status", "statusdeletephone", "youtubepre", "paymentmethod", "statusconfirmsecurity", "devicelogout", "chplay", "displayname", "youtubeverify", "checkhiddenphone", "checkreviewgooglemap", "disableforwarding", "checkgoogleadw", "createbrandaccountyoutube"]
    hidecolumns = {}
    for field in mailTable.__table__.columns:
        name = field.name
        if name in listshow:
            hidecolumns[name] = "Hide " + name
    return Result(data=hidecolumns).to_dict()



@eel.expose
def oimport(iaccount: str):
    try:
        # s = time.time()
        with Database() as db:
            accounts = iaccount.splitlines()
            if hfile.checkExists(accounts[0].strip()):
                accounts = hfile.readLines(accounts[0].strip())
            listdic = []
            for i in accounts:
                line = i.split("|") if len(i.split("|")) >= 2 else i.split("\t")
                if len(line) < 2:
                    continue
                email, password = map(str.strip, line[:2])
                emailrecovery = line[2].strip() if len(line) > 2 else ""
                phonerecovery = line[3].strip() if len(line) > 3 else ""
                securitycode = line[4].strip() if len(line) > 4 else ""
                dic = {"email": email, "password": password, "emailrecovery": emailrecovery, "phonerecovery": phonerecovery, "securitycode": securitycode, "country": "", "status": ""}
                listdic.append(dic)
            # print(time.time() - s)
            # db.execute(insert(Mails), listdic)
            if not listdic:
                toastError("Import fail 0 account")
                return
                # return Result(False, "import mails failed (0 account)").to_dict()
            db.bulk_insert_mappings(mailTable, listdic)
            db.commit()
            toastSuccess(f"Import success {len(listdic)} account")
            # print(time.time() - s)
            # return Result().to_dict()
    except Exception as e:
        db.rollback()
        toastError(f"Import mail fail {e.args}")
        # return Result(False, "import mails failed", e.args).to_dict()

def updateMail(id: int, update: mailClass):
    try:
        if id == -1:
            return Result(msg="-1")
        with Database() as db:
            old_mail = db.query(mailTable).filter(mailTable.id == id).first()
            if not old_mail:
                log(f"id not found {id}")
                return Result(False, "id not found")
            # log(f'update {id} {update["status"]}')
            if update["email"] and update["email"] != old_mail.email:
                old_emails =  old_mail.email.split('\n')
                if old_mail.email and not old_mail.email in old_emails:
                    old_emails.insert(0, old_mail.email)
                    if "" in old_emails:
                        old_emails.remove("")
                    update["oldpassword"] = '\n'.join(old_emails)
            if update["password"] and update["password"] != old_mail.password:
                old_passwords =  old_mail.oldpassword.split('\n')
                if old_mail.password and not old_mail.password in old_passwords:
                    old_passwords.insert(0, old_mail.password)
                    if "" in old_passwords:
                        old_passwords.remove("")
                    update["oldpassword"] = '\n'.join(old_passwords)
            if update["emailrecovery"] and update["emailrecovery"] != old_mail.emailrecovery:
                old_emailrecoverys = old_mail.oldemailrecovery.split('\n')
                if old_mail.emailrecovery and not old_mail.emailrecovery in old_emailrecoverys:
                    old_emailrecoverys.insert(0, old_mail.emailrecovery)
                    if "" in old_emailrecoverys:
                        old_emailrecoverys.remove("")
                    update["oldemailrecovery"] ='\n'.join(old_emailrecoverys)
            update_dict = {k: v for k, v in update.items() if v}
            db.query(mailTable).filter(mailTable.id == id).update(update_dict)
            db.commit()
            return Result()
    except Exception as e:
        db.rollback()
        error = hfile.getError()
        log(f"update_mail fail {error}")
        return Result(False, "update_mail fail", e.args)
# from himap import *
# imap = himap()
# imap.connect("imap.yandex.com")
# imap.login("admin@gmailz1.com", "yfcfhpvcmioinyds")
# imap.select_folder()
# search = imap.search(lay_mail_sau_ngay="29-05-2023")
# # # search = imap.search(nguoigui="no-reply@accounts.google.com")
# if not search[0]:
#     print(search[1])
from proxy import *
# logDisable(True)
# changeProxy("express")

from hcaptcha import *


# def move_mouse_through_random_points(page, x1, y1, x2, y2, num_points):
#     points = [(x1, y1)]

#     for _ in range(num_points):
#         random_x = random.uniform(x1, x2)
#         random_y = random.uniform(y1, y2)
#         points.append((random_x, random_y))

#     points.append((x2, y2))
#     return points
#     # for point in points:
#     #     page.mouse.move(point[0], point[1])
# import matplotlib.pyplot as plt
# points = move_mouse_through_random_points("page", 100, 100, 300, 300, 3)
# x_values = [point[0] for point in points]
# y_values = [point[1] for point in points]
# plt.plot(x_values, y_values, marker='o')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Mouse Path')
# plt.show()


restoredisablecontent = []
restoredisablecontact = []
emailrecoverydomain = []
emailrecoveryrandom = []
passwordrandom = []
def updateIni(started=False):
    global changepass, changeemailrecovery, changelanguage, verifyphone, restoredisable, restoredisablecontent, restoredisablecontact, checkcountry, checkinfoyoutube, checkdatecreate, checkgooglevoice, deletephonerecovery, checkgoogleemail, checkyoutubepremium, checkpaymentmethod, closepaymentmethod, deletepaymentmethod, checkphonerecovery
    global confirmsecurity, devicelogout, checkkhoiphuc, createchannelyoutube, creategooglevoice, checkchplay, changedisplayname, youtubeverify, checkhiddenphone, stopwhenpasswordsuccess, checkreviewgooglemap, disableforwarding, get2facode
    global emailrecoverydomain, emailrecoveryrandom, passwordrandom, listdisplayname, danhgiagooglemap, changecountry, user, linklogin, linkketqua, bat2fa, restoredisable2, khoiphuctaikhoan, tutquyetnguyen1, createbrandaccountyoutube
    global checkgoogleadw, createbrandaccountyoutube_number, nopecha, restoredisable2_mail, scale, saveprofile, fast_send
    global numthread, optionproxy, timesleep,sleep_enter ,delay, automovechrome, optionbrowser, proxy_active, gialapclick
    while True:
        changepass = ini.readcheckeel("changepass")
        changeemailrecovery = ini.readcheckeel("changeemailrecovery")
        changelanguage = ini.readcheckeel("changelanguage")
        checkgoogleadw = ini.readcheckeel("checkgoogleadw")
        checkcountry = ini.readcheckeel("checkcountry")
        saveprofile = ini.readcheckeel("saveprofile")
        verifyphone = ini.readcheckeel("verifyphone")
        stopwhenpasswordsuccess = ini.readcheckeel("stopwhenpasswordsuccess")
        youtubeverify = ini.readcheckeel("youtubeverify")
        restoredisable = ini.readcheckeel("restoredisable")
        checkinfoyoutube = ini.readcheckeel("checkinfoyoutube")
        createchannelyoutube = ini.readcheckeel("createchannelyoutube")
        checkdatecreate = ini.readcheckeel("checkdatecreate")
        checkgooglevoice = ini.readcheckeel("checkgooglevoice")
        deletephonerecovery = ini.readcheckeel("deletephonerecovery")
        checkgoogleemail = ini.readcheckeel("checkgoogleemail")
        checkyoutubepremium = ini.readcheckeel("checkyoutubepremium")
        checkpaymentmethod = ini.readcheckeel("checkpaymentmethod")
        closepaymentmethod = ini.readcheckeel("closepaymentmethod")
        deletepaymentmethod = ini.readcheckeel("deletepaymentmethod")
        checkreviewgooglemap = ini.readcheckeel("checkreviewgooglemap")
        checkphonerecovery = ini.readcheckeel("checkphonerecovery")
        confirmsecurity = ini.readcheckeel("confirmsecurity")
        get2facode = ini.readcheckeel("get2facode")
        automovechrome = True
        # automovechrome = ini.readcheckeel("automovechrome")
        devicelogout = ini.readcheckeel("devicelogout")
        checkkhoiphuc = ini.readboolean("checkkhoiphuc")
        gialapclick = ini.readint("gialapclick", 1)
        creategooglevoice = ini.readboolean("creategooglevoice")
        danhgiagooglemap = ini.read("danhgiagooglemap")
        createbrandaccountyoutube = ini.readint("createbrandaccountyoutube", 0)
        fast_send = ini.readint("fast_send", 0)
        createbrandaccountyoutube_number = ini.readint("createbrandaccountyoutube_number", 0)
        khoiphuctaikhoan = ini.readint("khoiphuctaikhoan", 0)
        tutquyetnguyen1 = ini.readint("tutquyetnguyen1", 0)
        scale = ini.readfloat("scale", 1)

        bat2fa = ini.readint("bat2fa", 0)
        restoredisable2 = ini.readint("restoredisable2", 0)
        user = ini.read("user")
        linklogin = ini.read("linklogin")
        linkketqua = ini.read("linkketqua")
        restoredisable2_mail = ini.read("restoredisable2_mail")
        nopecha = ini.read("nopecha")
        proxy_active = ini.read("proxy_active")
        changecountry = ini.read("changecountry")
        checkchplay = ini.readcheckeel("checkchplay")
        changedisplayname = ini.readcheckeel("changedisplayname")
        checkhiddenphone = ini.readcheckeel("checkhiddenphone")
        disableforwarding = ini.readcheckeel("disableforwarding")

        restoredisablecontent = hstr.trimAllLines(hfile.readLines("data/restoredisablecontent.txt"))
        restoredisablecontact = hstr.trimAllLines(hfile.readLines("data/restoredisablecontact.txt"))
        emailrecoverydomain = hstr.trimAllLines(hfile.readLines("data/emailrecoverydomain.txt"))
        emailrecoveryrandom = hstr.trimAllLines(hfile.readLines("data/emailrecoveryrandom.txt"))
        passwordrandom = hstr.trimAllLines(hfile.readLines("data/passwordrandom.txt"))
        listdisplayname = hstr.trimAllLines(hfile.readLines("data/listdisplayname.txt"))


        numthread = ini.readint("text_numthread", default=1)
        timesleep = ini.readint("text_timesleep", default=0)
        delay = ini.readint("delay", default=100)
        sleep_enter = ini.readint("sleep_enter", default=1)

        optionbrowser = ini.read("text_optionbrowser")
        optionproxy = ini.read("text_optionproxy")
        if not optionproxy:
            optionproxy = "noproxy"
            ini.write("text_optionproxy", optionproxy)
        if started:
            return
        sleep(10)
# url = "https://myaccount.google.com/notifications/eid/-4495546369007211338?origin=5&continue=https%3A%2F%2Fmyaccount.google.com%2Fnotifications"
# id = hstr.regex(url, "/eid/.*?(\\d+)")


def get_size(max_thread):
    # x_size = 400
    y_size = 550
    y_size = screensize_y/2

    if max_thread > 5:
        max_thread = 5
    x_size = screensize_x / max_thread
    return int(x_size), int(y_size)
    # if screensize_x == 2560:
    #     x_size = 440
    # elif screensize_x == 1920:
    #     x_size = 385
    # elif screensize_x == 3840:
    #     x_size = 390
    #     y_size = 540


# listPos = hwin32.chiaDeuManHinh(x_size, y_size)
def getMaxThread(maxthread = 5):
    if maxthread >= len(listPos):
        maxthread = len(listPos)
    return maxthread
# abc = "adajhw, "
# da = hstr.xoaKyTuCuoiCung(abc, ",")
listProxy = []

runProxy = False
def getProxy(started=False):
    global listProxy, runProxy
    if runProxy and started == False:
        return
    runProxy = True
    while True:
        proxys = hfile.readLines("data/listproxy.txt")
        if proxys:
            listProxy = proxys
        # proxys = hfile.readLines("data/listtmproxy.txt")
        # if proxys:
        #     listTMProxy = proxys
        # proxys = hfile.readLines("data/listmobiproxy.txt")
        # if proxys:
        #     list_mobiproxy = proxys
        if started:
            return
        sleep(10)
hthread.start(updateIni)
hthread.start(getProxy)
# x_values, y_values =  [839, 835, 831, 827, 823, 819, 815, 811, 807, 803, 799, 795, 791, 787, 783, 779, 775, 771, 767, 763, 759, 755, 751, 747, 743, 739, 735, 731, 727, 723, 719, 715, 711, 707, 703, 699, 695, 691, 687, 683, 679, 675, 671, 667, 663, 659, 655, 651, 647, 643, 639, 635, 631, 627, 623, 619, 615, 611, 607, 603, 599, 595, 591, 587, 583, 579, 575, 571, 567, 563, 559, 555, 551, 547, 543, 539, 535, 531, 527, 523, 519, 515, 511], [256, 255, 254, 253, 251, 250, 249, 248, 246, 245, 244, 243, 241, 240, 239, 238, 236, 235, 234, 233, 231, 230, 229, 228, 226, 225, 224, 223, 222, 220, 219, 218, 217, 215, 214, 213, 212, 210, 209, 208, 207, 205, 204, 203, 202, 200, 199, 198, 197, 195, 194, 193, 192, 190, 189, 188, 187, 186, 184, 183, 182, 181, 179, 178, 177, 176, 174, 173, 172, 171, 169, 168, 167, 166, 164, 163, 162, 161, 159, 158, 157, 156, 155]
# import matplotlib.pyplot as plt
# plt.plot(x_values, y_values, marker='o')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Mouse Path')
# plt.show()
# html = hfile.read("a.txt")
# code = hstr.regex(html, "seconds ago.</td>.<td>Google</td>.<td>[^<]*?(\\d{6})[^<]*?</td>.</tr>", flags=re.MULTILINE | re.DOTALL)
# print(code)
def y():
    l = hfile.read("login_state.json")
    js = hstr.strToJson(l)
    cookies = js["cookies"]
    for cookie in cookies:
        domain = cookie.get("domain")


        httpOnly = cookie.get("httpOnly")
        path = cookie.get("path")
        httpOnly = str(httpOnly).upper()
        secure = cookie.get("secure")
        secure =  str(secure).upper()
        expires = cookie.get("expires")
        expires = str(expires).split(".")[0]
        if expires == "-1":
            expires = "1707718327"
        name = cookie.get("name")
        value = cookie.get("value")
        daya = (f"{domain}\t{httpOnly}\t{path}\t{secure}\t{expires}\t{name}\t{value}")
        hfile.writeLine("login_state.txt",daya )
# ú = hrand.randomChromeUserAgent()
# print(ú)
from hotp import *
otpdataVoice = otpData()
otpdataVerify = otpData()
otpdataYoutube = otpData()
irunning = 0
max_x = 0
success = 0
fail = 0
lock_success = threading.Lock()
lockgetproxy = threading.Lock()


def run(ids_chunk, proxyoption, proxy, ithread):
    from script.gmail import Gmail
    global max_x, irunning, success, fail
    while ids_chunk:

        self = Gmail()
        self.ithread = ithread + 1
        if not isRunning():
            return
        checkPause()
        try:
            if not ck.status:
                toastError(ck.message)
                return
            if proxyoption in proxyssh:
                if proxyoption == "listproxy":
                    with lockgetproxy:
                        last_index_listproxy = ini.readint("last_index_listproxy", 0)
                        if last_index_listproxy >= len(listProxy):
                            last_index_listproxy = 0
                        ini.write("last_index_listproxy", last_index_listproxy + 1)
                        proxy = listProxy[last_index_listproxy]
                        if proxy.startswith("proxy6:"):
                            apikey = proxy.split(":")[1]
                            proxy = proxy6(apikey)
                        if proxy.startswith("proxy_sheet:"):
                            apikey = proxy.split(":")[1]
                            proxy = proxy_sheet(apikey)
                        if not ":" in proxy:
                            continue

                    # proxy = hrand.randomItemInList(listProxy)
                    log(f"Tab {self.ithread} proxy run {proxy}")
                if proxyoption == "listtmproxy":
                    try:
                        proxy: str = list_tmproxy[ithread].strip()
                    except:
                        pass
                    if len(proxy) != 32:
                        return

                    proxystatus = tmproxy(proxy)
                    if not proxystatus[0]:
                        log(f"Tab {self.ithread} tmproxy {proxystatus[1]}")
                        sleep(2)
                        continue
                    proxy = proxystatus[1]
                if proxyoption == "list_proxyno1":
                    try:
                        proxy: str = list_proxyno1[ithread].strip()
                    except:
                        pass
                    if not "," in proxy:
                        return

                    proxystatus = proxyno1(proxy)
                    if not proxystatus[0]:
                        log(f"Tab {self.ithread} proxyno1 {proxy} {proxystatus[1]}")
                        sleep(2)
                        continue
                    proxy = proxystatus[1]
                if proxyoption == "listmobiproxy":
                    try:
                        proxy: str = list_mobiproxy[ithread].strip()
                    except:
                        pass
                    if not ":" in proxy:
                        return
                    mobi = mobiproxy()
                    mobi.set_proxy(proxy)
                    newip = mobi.get_new_ip()
                    if not newip:
                        log(f"Tab {self.ithread} mobiproxy cannot get new ip")
                        sleep(2)
                        continue
                if proxyoption == "list_obcproxy":
                    try:
                        proxy: str = list_obcproxy[ithread].strip()
                    except:
                        pass
                    if not ":" in proxy:
                        return
                    mobi = obcproxy()
                    mobi.set_proxy(proxy)
                    newip = mobi.get_new_ip()
                    if not newip:
                        log(f"Tab {self.ithread} obcproxy cannot get new ip")
                        sleep(2)
                        continue

                    proxy = mobi.ip + ":" + mobi.port
                    if mobi.user:
                        proxy = mobi.ip + ":" + mobi.port+ ":" + mobi.user+ ":" + mobi.passs
                    # proxy = proxystatus[1]
                if proxyoption == "list_shadowtech":
                    try:
                        proxy: str = list_shadowtech[ithread].strip()
                    except:
                        pass
                    if not ":" in proxy:
                        return
                    mobi = shadowtech()
                    mobi.set_proxy(proxy)
                    log(f"Tab {self.ithread} shadowtech connect proxy {proxy}")
                    newip = mobi.get_new_ip()
                    if not newip:
                        log(f"Tab {self.ithread} shadowtech cannot get new ip")
                        sleep(2)
                        continue

                    proxy = mobi.ip + ":" + mobi.port
                    if mobi.user:
                        proxy = mobi.ip + ":" + mobi.port+ ":" + mobi.user+ ":" + mobi.passs

            data = {}
            id = ids_chunk.pop(0)
            if id == -1:
                ids_chunk.append(id)
            else:
                mail = getMailById(id)
                data = mail["data"]
                if not data:
                    return

            irunning = irunning + 1
            self.fast_send = fast_send
            self.linklogin = linklogin
            self.linkketqua = linkketqua

            self.nopecha = nopecha
            self.user_tool = user
            self.proxy = proxy
            self.sleep_enter = sleep_enter
            self.delay = delay
            self.listdisplayname = listdisplayname
            self.verifyphone = verifyphone
            self.stopwhenpasswordsuccess = stopwhenpasswordsuccess
            self.restoredisablecontent = restoredisablecontent
            self.restoredisable2_mail = restoredisable2_mail
            self.restoredisablecontact = restoredisablecontact
            self.emailrecoverydomain = emailrecoverydomain
            self.emailrecoveryrandom = emailrecoveryrandom
            self.passwordrandom = passwordrandom
            self.checkkhoiphuc = checkkhoiphuc
            self.restoredisable = restoredisable
            self.normalcaptcha_data = captchadata
            self.otpdataVerify = otpdataVerify
            self.otpdataVoice = otpdataVoice
            self.otpdataYoutube = otpdataYoutube
            self.khoiphuctaikhoan = khoiphuctaikhoan
            self.tutquyetnguyen1 = tutquyetnguyen1
            self.saveprofile = saveprofile
            self.path_saveprofile = path_saveprofile
            self.gialapclick = gialapclick

            if  automovechrome:
                self.scale = scale
                if x_size:
                    self.windowsize = [x_size, y_size]
                    self.windowpos = listPos[ithread]
            else:
                self.scale = scale
                from hrand import hrand
                self.windowpos = [ithread * 100, ithread * 100]

            self.ck = ck
            self.browser = (browser_name, browser_id)
            self.orbita_browser_check = getBrowser()
            self.data = data
            log(f"Tab {self.ithread} login {irunning}/{tongsonick}")


            self.getrapt = True
            if not changepass  and not changeemailrecovery and not deletephonerecovery and not bat2fa:
                self.getrapt = False
            setStatus(self.data["id"], "wait login...")

            login = self.login()


            if login == "login ok" or login == "restore.disable.ok" or login == "stopwhenpasswordsuccess":
                with lock_success:
                    success = success + 1
            else:
                with lock_success:
                    fail = fail + 1

            if login == "login ok":
                if self.verify_ok:
                    login = "verify ok"
                if saveprofile:
                    profile_path = self.hpw.profile_path
                    hfile.createFile(profile_path + "/LOGINOK")
                # self.p.sleep(1)
                # self.p.context.storage_state(path='login_state.json')
                # self.hpw.close()


            setStatus(self.data["id"], login)
            data["browser"] = browser_name
            data["status"] = login
            log(f"Tab {self.ithread} login {login}")
            updateMail(id, data)
            setHtmlCssSelector("#numsuccess", f"Ok: {success} - Fail: {fail} - All: {irunning}/{tongsonick}")
            if self.rapt:

                if restoredisable2:
                    log(f"Tab {self.ithread} restoredisable2")
                    change = self.restoredisable2()
                    log(f"Tab {self.ithread} restoredisable2 {change}")
                if checkhiddenphone:
                    setStatus(self.data["id"], "checkhiddenphone")
                    log(f"Tab {self.ithread} checkhiddenphone")
                    change = self.checkHiddenPhone()
                    log(f"Tab {self.ithread} checkhiddenphone {change}")
                    self.data["checkhiddenphone"] = change
                    self.updateMail()

                if disableforwarding:
                    setStatus(self.data["id"], "disableforwarding")
                    log(f"Tab {self.ithread} disableforwarding")
                    change = self.disable_forwarding()
                    log(f"Tab {self.ithread} disableforwarding {change}")
                    self.data["disableforwarding"] = change
                    self.updateMail()
                if checkgoogleemail:
                    setStatus(self.data["id"], "checkgoogleemail")
                    log(f"Tab {self.ithread} checkgoogleemail")
                    change = self.checkGoogleEmail()
                    log(f"Tab {self.ithread} checkgoogleemail {change}")

                if checkphonerecovery:
                    setStatus(self.data["id"], "checkphonerecovery")
                    log(f"Tab {self.ithread} checkphonerecovery")
                    change = self.checkPhoneRecovery()
                    log(f"Tab {self.ithread} checkphonerecovery {change}")
                    self.data["checkphonerecovery"] = change
                    self.updateMail()

                if deletephonerecovery and self.checkphonerecoveryok:
                    setStatus(self.data["id"], "deletephonerecovery")
                    log(f"Tab {self.ithread} deletephonerecovery")
                    email = data["email"]
                    if not "@" in email:
                        log(f"Tab {self.ithread} email is {email}. no deletephonerecovery")
                    else:
                        change = self.deletePhoneRecovery()
                        log(f"Tab {self.ithread} deletephonerecovery {change}")
                        self.data["statusdeletephone"] = change
                        self.updateMail()
                if changelanguage:
                    setStatus(self.data["id"], "changelanguage")
                    log(f"Tab {self.ithread} changelanguage")
                    change = self.change_language()
                    log(f"Tab {self.ithread} changelanguage {change}")
                    self.data["language"] = change
                    self.updateMail()
                if checkgoogleadw:
                    setStatus(self.data["id"], "checkgoogleadw")
                    log(f"Tab {self.ithread} checkgoogleadw")
                    change = self.check_google_adw()
                    log(f"Tab {self.ithread} checkgoogleadw {change}")
                    self.data["checkgoogleadw"] = change
                    self.updateMail()
                if checkyoutubepremium:
                    setStatus(self.data["id"], "checkyoutubepremium")
                    log(f"Tab {self.ithread} checkyoutubepremium")
                    change = self.checkYoutubePremium()
                    log(f"Tab {self.ithread} checkyoutubepremium {change}")
                    self.data["youtubepre"] = change
                    self.updateMail()
                if confirmsecurity:
                    setStatus(self.data["id"], "confirmsecurity")
                    log(f"Tab {self.ithread} confirmsecurity")
                    change = self.confirm_security()
                    log(f"Tab {self.ithread} confirmsecurity {change}")
                    self.data["statusconfirmsecurity"] = change
                    self.updateMail()
                if get2facode:
                    setStatus(self.data["id"], "get2facode")
                    log(f"Tab {self.ithread} get2facode")
                    change = self.get_2fa_code()
                    log(f"Tab {self.ithread} get2facode {change}")


                if checkreviewgooglemap:
                    setStatus(self.data["id"], "checkreviewgooglemap")
                    log(f"Tab {self.ithread} checkreviewgooglemap")
                    change = self.check_review_google_map()
                    log(f"Tab {self.ithread} checkreviewgooglemap {change}")
                    self.data["checkreviewgooglemap"] = change
                    self.updateMail()
                if deletepaymentmethod:
                    setStatus(self.data["id"], "deletepaymentmethod")
                    log(f"Tab {self.ithread} deletepaymentmethod")
                    change = self.deletePaymentMethod()
                    log(f"Tab {self.ithread} deletepaymentmethod {change}")
                    self.data["paymentmethod"] = change
                    self.updateMail()
                if closepaymentmethod:
                    setStatus(self.data["id"], "closepaymentmethod")
                    log(f"Tab {self.ithread} closepaymentmethod")
                    change = self.closePaymentMethod()
                    log(f"Tab {self.ithread} closepaymentmethod {change}")
                    self.data["paymentmethod"] = change
                    self.updateMail()
                if checkpaymentmethod:
                    setStatus(self.data["id"], "checkpaymentmethod")
                    log(f"Tab {self.ithread} checkpaymentmethod")
                    change = self.checkPaymentMethod()
                    log(f"Tab {self.ithread} checkpaymentmethod {change}")
                    self.data["paymentmethod"] = change
                    self.updateMail()


                if checkdatecreate:
                    setStatus(self.data["id"], "checkdatecreate")
                    log(f"Tab {self.ithread} checkdatecreate")
                    change = self.check_date_create()
                    setTable(self.data["id"], "datecreate", change)
                    log(f"Tab {self.ithread} checkdatecreate {change}")
                    self.data["datecreate"] = change
                    self.updateMail()
                if danhgiagooglemap:
                    userdanhgia = {}
                    userdanhgia["lochuy"] = "googlevoice"
                    userdanhgia["tientung"] = "googlevoice"
                    column = userdanhgia.get(danhgiagooglemap, "")
                    if column:
                        setStatus(self.data["id"], "danhgiagooglemap")
                        log(f"Tab {self.ithread} danhgiagooglemap")
                        change = self.danhGiaGoogleMap(danhgiagooglemap)
                        log(f"Tab {self.ithread} danhgiagooglemap {change}")
                        self.data[column] = change
                        self.updateMail()
                if bat2fa:
                    if ck.user in ["admin", "Hải Dương"]:
                        setStatus(self.data["id"], "bat2fa")
                        log(f"Tab {self.ithread} bat2fa")
                        change = self.bat2fa()
                        log(f"Tab {self.ithread} bat2fa {change}")
                        #update ở trong bat2fa rồi không cần update ở đây nữa
                if createbrandaccountyoutube:
                    if ck.user in ["admin", "Trần Thiện Toàn"]:
                        setStatus(self.data["id"], "createbrandaccountyoutube")
                        log(f"Tab {self.ithread} createbrandaccountyoutube")
                        change = self.create_brand_account_youtube(createbrandaccountyoutube_number)
                        total = len(self.get_all_link_youtube())
                        log(f"Tab {self.ithread} createbrandaccountyoutube {change}")
                        self.data["createbrandaccountyoutube"] = change + "," + str(total)
                        self.updateMail()

                if changecountry:
                    userdanhgia = {}
                    userdanhgia["tientung"] = "chplay"
                    column = userdanhgia.get(changecountry, "")
                    if column:
                        setStatus(self.data["id"], "changecountry")
                        log(f"Tab {self.ithread} changecountry")
                        change = self.changeCountry()
                        log(f"Tab {self.ithread} changecountry {change}")
                        self.data[column] = change
                        self.updateMail()
                if checkchplay:
                    setStatus(self.data["id"], "checkchplay")
                    log(f"Tab {self.ithread} checkchplay")
                    change = self.checkCHPlay()
                    log(f"Tab {self.ithread} checkchplay {change}")
                    self.data["chplay"] = change
                    self.updateMail()

                if changedisplayname:
                    setStatus(self.data["id"], "changedisplayname")
                    log(f"Tab {self.ithread} changedisplayname")
                    change = self.change_display_name()
                    log(f"Tab {self.ithread} changedisplayname {change}")
                    self.data["displayname"] = change
                    self.updateMail()


                if createchannelyoutube:
                    setStatus(self.data["id"], "createchannelyoutube")
                    log(f"Tab {self.ithread} createchannelyoutube")
                    change = self.createChannelYoutube()
                    log(f"Tab {self.ithread} createchannelyoutube {change}")
                    self.data["youtube"] = change
                    self.updateMail()
                if youtubeverify:
                    setStatus(self.data["id"],  "youtubeverify")
                    log(f"Tab {self.ithread} youtubeverify")
                    change = self.youtubeVerify()
                    log(f"Tab {self.ithread} youtubeverify {change}")
                    self.data["youtubeverify"] = change
                    self.updateMail()
                if checkinfoyoutube:
                    setStatus(self.data["id"], "checkinfoyoutube")
                    log(f"Tab {self.ithread} checkinfoyoutube")
                    change = self.checkInfoYoutube()
                    log(f"Tab {self.ithread} checkinfoyoutube {change}")
                    self.data["youtube"] = change
                    self.updateMail()
                if checkcountry:
                    setStatus(self.data["id"], "checkcountry")
                    log(f"Tab {self.ithread} checkcountry")
                    change = self.checkCountry()
                    log(f"Tab {self.ithread} checkcountry {change}")
                    self.data["country"] = change
                    self.updateMail()

                statusnew = ""
                if changepass:
                    setStatus(self.data["id"], "changepass")
                    log(f"Tab {self.ithread} changepass")
                    change = self.changePass()
                    log(f"Tab {self.ithread} changepass {change}")
                    statusnew = statusnew + "changePass " + change + ", "
                    data["status"] = hstr.xoaKyTuCuoiCung(statusnew, ",")
                    updateMail(id, data)
                if changeemailrecovery:
                    setStatus(self.data["id"], "changeemailrecovery")
                    log(f"Tab {self.ithread} changeemailrecovery")
                    change = self.changeEmailRecovery()
                    log(f"Tab {self.ithread} changeemailrecovery {change}")
                    statusnew = statusnew + "changeEmailRecovery " + change + ", "
                    data["status"] = hstr.xoaKyTuCuoiCung(statusnew, ",")
                    updateMail(id, data)
                if creategooglevoice:
                    setStatus(self.data["id"], "creategooglevoice")
                    log(f"Tab {self.ithread} creategooglevoice")
                    change = self.create_google_voice()
                    log(f"Tab {self.ithread} creategooglevoice {change}")
                    self.data["googlevoice"] = change
                    self.updateMail()
                if checkgooglevoice:
                    setStatus(self.data["id"], "checkgooglevoice")
                    log(f"Tab {self.ithread} checkgooglevoice")
                    change = self.checkGoogleVoice()
                    log(f"Tab {self.ithread} checkgooglevoice {change}")
                    self.data["googlevoice"] = change
                    self.updateMail()
                if devicelogout:
                    setStatus(self.data["id"], "devicelogout")
                    log(f"Tab {self.ithread} devicelogout")
                    change = self.logout_device()
                    log(f"Tab {self.ithread} devicelogout {change}")
                    data["devicelogout"] = change
                    updateMail(id, data)
                if self.linkketqua:
                    rq = hrequest()
                    newlink = self.linkketqua.replace("taikhoan", self.data['email']).replace("matkhau", self.data['password']).replace("trangthai", login)
                    if self.data["emailrecovery"]:
                        newlink = newlink.replace("emailkhoiphuc", self.data["emailrecovery"])
                    if self.data["datecreate"]:
                        newlink = newlink.replace("datecreate", self.data["datecreate"])
                    rq.get(newlink)
            else:

                if self.linkketqua:
                    if not "Wrong password" in login and not "Mật khẩu không chính xác" in login:
                        rq = hrequest()
                        newlink = self.linkketqua.replace("taikhoan", self.data['email']).replace("matkhau", self.data['password']).replace("trangthai", login)
                        if self.data["emailrecovery"]:
                            newlink = newlink.replace("emailkhoiphuc", self.data["emailrecovery"])
                        if self.data["datecreate"]:
                            newlink = newlink.replace("datecreate", self.data["datecreate"])
                        rq.get(newlink)
            setStatus(self.data["id"], f"Done {login}")
            # print(mail)
        except Exception as e:
            error = hfile.getError()
            log(error)
        log(f"Tab {self.ithread} done1", True)
        if self.p:
            self.hpw.close()
        log(f"Tab {self.ithread} done2", True)
        if not proxyoption in proxyssh:
            log(f"Tab {self.ithread} {proxyoption}", True)
            return
        log(f"Tab {self.ithread} done3", True)

@eel.expose
def getKeyInfo():
    return Result(data=ck.status, msg=ck.message).to_dict()
    # return {"status":ck.status, "msg": ck.message}

@eel.expose
def kichHoatTaiKhoan(keyactive):
    dic = dict()
    if not ck.isKeyActive(keyactive):
        dic["mess"] = "Key is invalid"
        return dic
    # text = hmahoa.get(f"http://{sv}:8000/changekey?keyactive={keyactive}&hwid={ck.hwid}&nameapp={ck.nameapp}")
    from hmahoa import hmahoa
    app = ck.nameapp.replace(" ", "%20")
    url = f"http://{sv}:8000/changekey?keyactive={keyactive}&hwid={ck.hwid}&nameapp={app}"
    text = hmahoa.get(url)

    if text == "disconnect":
        from hcurl import hcurl
        curl = hcurl()
        rq = curl.get(url, proxy_active)
        text = rq.text
    # text = requests.get(url).text


    if "Tài khoản không tồn tại" in text:
        dic["mess"] = text
        return dic
    dic["result"] = text
    dic["mess"] = "success"
    return dic



# logDisable(True)
# ipvanish()

def fixListAccount(listidaccount: list):
    if listidaccount:
            if len(listidaccount) == 1:
                if listidaccount[0] == -1:
                    for i in range(10000):
                        listidaccount.append(-1)
    return listidaccount
# a = "2j1hjhwqew,wjqhejwqh"
# b = list(a)
optionbrowser = ""
def autoCloseHidemium():

    def run():
        from huiautomation import huiautomation
        import pythoncom
        pythoncom.CoInitialize()
        while 1:
            if optionbrowser == "hidemium":
                pid = hwin.getPidOfProcess("Hidemium.exe")
                if not pid:
                    hidemiumexe = hpath.programs() + r"\Hidemium\Hidemium.exe"
                    if hfile.checkExists(hidemiumexe):
                        hwin.processStartExe(hidemiumexe)
                        sleep(10)
            hwnd = hwin32.findWindow('"Application Launcher For Drive (by Google)" added')
            if hwnd:
                hwin.control_send_by_handle(hwnd, "{esc}")
                # hwin.control_click_by_handle(hwnd, x=400, y=300)
            hwnd = hwin32.findWindow("Hidemium", "Chrome_WidgetWin_1")
            if hwnd:
                hwin.control_click_by_handle(hwnd, x=935, y=715)

            hwnd = hwin32.findWindow("Save password?", "Chrome_WidgetWin_1")
            if hwnd:
                ui = huiautomation(hwnd)
                Save = ui.getButtonControl("Save")
                Save.defaultAction()

            sleep(1)
    hthread.start(run)
autoCloseHidemium()
def check_browser():
    if not optionbrowser:
        toastError("Please select browser in settings")
        return False, ""
    toastWarning(f"Checking browser {optionbrowser}")
    if optionbrowser == "hidemium":
        # if "proxy" in optionproxy and optionproxy != "noproxy":
        #     toastError(f"Chưa hỗ trợ proxy trình duyệt {optionbrowser}")
            # return False, ""
        pid = hwin.getPidOfProcess("Hidemium.exe")
        if not pid:
            toastError(f"Chưa cài đặt hoặc chưa mở {optionbrowser}. https://hidemium.io/")
            return False, ""
        rq = hrequest()
        html = rq.getHtml("http://127.0.0.1:5555/get-list-config-default?page=1&limit=10", again=1, timeout=10)
        id = hstr.regexJsonNumber(html, "id")
        if not id:
            toastError("Chưa cài đặt Default config profile")
            return False, ""
        try:
            d_json = rq.getJson("http://127.0.0.1:5555/profileList?page=1&limit=30", again=1)
            contents = d_json["data"]["content"]
            for content in contents:
                note = content["note"]
                if note == "GMAILMANAGE":
                    uuid = content["uuid"]
                    rq= hrequest()
                    html = rq.getHtml(f"http://127.0.0.1:5555/closeProfile?uuid={uuid}")
                    rq.delete("http://127.0.0.1:5555/delete-profile", '{    "uuid_browser":[        "'+uuid+'"    ]}')
        except:
            pass

        return (optionbrowser, id)
    elif optionbrowser == "chrome":
        chrome = hpath.chrome()
        if not hfile.checkExists(chrome):
            toastError("Không tìm thấy chrome.exe")
            return False, ""
        return (optionbrowser, chrome)
    elif optionbrowser == "dolphin":
        if not hfile.checkExists(dolphin_browser_profile_preferences):
            save_path = dolphin_path +"dolphin.zip"
            download_file_extract(dolphin_browser_profile_preferences_link, save_path , process="", extract=True, show_progress=True, file_name_show="Dolphin profiles")
            close_show_update()
            if not hfile.checkExists(dolphin_browser_profile_preferences):
                toastError(f"Dolphin profiles not exists")
                return False, ""
        if not hfile.checkExists(dolphin_browser_check):
            save_path = dolphin_path +"dolphin.zip"
            download_file_extract(dolphin_browser_link_exe, save_path , process="", extract=True, show_progress=True, file_name_show="Dolphin browser")
            close_show_update()
            if not dolphin_browser_check:
                toastError(f"Dolphin browser not exists")
                return False, ""
        return (optionbrowser, dolphin_browser_check)
    return (optionbrowser, True)
list_tmproxy = []
list_proxyno1 = []
list_mobiproxy = []
list_obcproxy = []
list_shadowtech = []
listPos = []
path_saveprofile = ""
@eel.expose
def runAccountsThread(listidaccount: list):
    def runAccounts(listidaccount: list):
        listidaccount = fixListAccount(listidaccount)
        global success, fail, irunning, browser_name, browser_id, x_size, y_size, listPos
        global list_tmproxy, list_mobiproxy, list_obcproxy, list_shadowtech, path_saveprofile, list_proxyno1


        success = 0
        fail = 0
        irunning = 0
        global window_size, numthread,  tongsonick, otpdataVoice, otpdataVerify, captchadata, otpdataYoutube
        if checkThreadRunning():
            toastError("Auto is running")
            return
        log(f"{htime.getStrTimeNow3()}: Start")
        if ck.message:
            toastError(ck.message)
            return


        updateIni(True)

        if saveprofile:
            path_saveprofile = hfile.read("data/saveprofile.txt")
            if not hfile.checkExists(path_saveprofile):
                toastError(f"Path save profile not exists {path_saveprofile}")
                return
        browser_name, browser_id = check_browser()
        if not browser_name:
            return
        getProxy(True)
        if changedisplayname and not listdisplayname:
            toastError("Please add list name (first last)")
            return
        if restoredisable or restoredisable2:
            if not restoredisablecontact:
                toastError("Please add contact to Restore Disable Contact, 1 line per contact")
                return
            if not restoredisablecontent:
                toastError("Please add content to Restore Disable Content, 1 line per content")
                return
        if youtubeverify or createbrandaccountyoutube:
            otpdataYoutube = hotp.getOtpData("data/youtubeverify.txt")
            if not otpdataYoutube:
                toastError("Please config otp verify youtube")
                return
        if creategooglevoice:
            otpdataVoice = hotp.getOtpData(voice=True)
            if not otpdataVoice:
                toastError("Please config otp verify phone voice")
                return
            otpdataVoice.serviceId = otpdataVoice.serviceId.split("=")[0]
        if verifyphone or bat2fa:
            otpdataVerify = hotp.getOtpData()
            if not otpdataVerify:
                toastError("Please config otp verify phone voice")
                return
            if "=" in otpdataVerify.serviceId:
                otpdataVerify.serviceId = otpdataVerify.serviceId.split("=")[0]
        captchadata = hcaptcha.getCaptchaData()


        # hthread.start(run, [listidaccount])

        if not numthread:
            toastError(f"Please set Thread in Setting")
            return


        setRunning(True)
        if numthread >= len(listidaccount):
            numthread = len(listidaccount)

        if optionproxy == "list_proxyno1":
            list_proxyno1 = hfile.readLines("data/list_proxyno1.txt")
            if not list_proxyno1:
                toastError(f"Hãy thêm danh sách key tmproxy vào LIST PROXYNO1")
                return
            if numthread >= len(list_proxyno1):
                numthread = len(list_proxyno1)
        if optionproxy == "listtmproxy":
            list_tmproxy = hfile.readLines("data/listtmproxy.txt")
            if not list_tmproxy:
                toastError(f"Hãy thêm danh sách key tmproxy vào LIST TMPROXY")
                return
            if numthread >= len(list_tmproxy):
                numthread = len(list_tmproxy)
        if optionproxy == "listmobiproxy":
            list_mobiproxy = hfile.readLines("data/listmobiproxy.txt")
            if not list_mobiproxy:
                toastError(f"Hãy thêm danh sách ip:port mobiproxy vào LIST MOBIPROXY")
                return
            if numthread >= len(list_mobiproxy):
                numthread = len(list_mobiproxy)
        if optionproxy == "list_obcproxy":
            list_obcproxy = hfile.readLines("data/list_obcproxy.txt")
            if not list_obcproxy:
                toastError(f"Hãy thêm danh sách host;ip:port obcproxy vào LIST OBCPROXY")
                return
            if numthread >= len(list_obcproxy):
                numthread = len(list_obcproxy)
        if optionproxy == "list_shadowtech":
            list_shadowtech = hfile.readLines("data/list_shadowtech.txt")
            if not list_shadowtech:
                toastError(f"Hãy thêm danh sách ip:port:user:pass:apikey:keyport:portchange obcproxy vào list_shadowtech")
                return
            if numthread >= len(list_shadowtech):
                numthread = len(list_shadowtech)



        if numthread > 1:
            x_size, y_size = get_size(numthread)
            if scale < 1:
                x_size, y_size = int(x_size * scale), int(y_size * scale)
        else:
            x_size, y_size = 0, 0
        if x_size:
            listPos = hwin32.chiaDeuManHinh(x_size,y_size )
            numthread = getMaxThread(numthread)

        # if restoredisable2:
        #     open = excel.open("data/restoredisable2.xlsx", "restoredisable2")
        #     if not open:
        #         if "Permission denied" in excel.msg_error:
        #             toastError(f"Có phần mềm đang sử dụng restoredisable2.xlsx, hãy đóng trước.")
        #         else:
        #             toastError(f"Hãy tạo file restoredisable2.xlsx ở thư mục data và thêm email vào")
        #         return


        log(f"Run {getSetting()}")
        # ids_chunks = hstr.chiaDeuList(listidaccount, numthread)
        tongsonick = len(listidaccount)
        setHtmlCssSelector("#numsuccess", f"Total run: {tongsonick} {numthread} {len(listPos)} {screensize_x} {screensize_y}")
        # return
        # killAllOrbita()
        hwin.killAllOrbita(False)
        firsttime = True
        while listidaccount:
            if not firsttime:
                if timesleep:
                    startsleep = time.time()
                    for i in range(timesleep):
                        conlai = timesleep - int(time.time() - startsleep)
                        if conlai <=0:
                            break
                        if not isRunning():
                            setHtmlCssSelector("#numsuccess", f"STOP AUTO")
                            toastWarning(f"STOP AUTO")
                            return
                        toastWarning(f"Tools will run mail next after {conlai} seconds")
                        sleep(3)
            firsttime = False
            checkPause()
            log(f"Run connect {optionproxy}")
            proxystatus = changeProxy(optionproxy)
            if not proxystatus[0]:
                toastError(f"Cannot connect {optionproxy}. Please set Proxy in Setting")
                setRunning(False)
                return
            toastSuccess("Running...")
            if proxystatus[1]:
                log(f"Run set proxy {proxystatus[1]}")
            sleep(1)
            ithread = 0
            for  i in range(numthread):
                hthread.start(run, [listidaccount, optionproxy, proxystatus[1], ithread], addlist=True, name="autothread")
                ithread = ithread +1
            hthread.waitThreadsDone()
            # ids_chunks = [chunk for chunk in ids_chunks if chunk]
            if not isRunning():
                setHtmlCssSelector("#numsuccess", f"STOP AUTO")
                return
        log(f"Run done {tongsonick} account")
        setRunning(False)
        hwin.killAllOrbita(False)
    hthread.start(runAccounts, [listidaccount])


@eel.expose
def deleteAccounts(listidaccount: list):
    try:
        with Database() as db:
            maxDel = 10000
            hfile.createDir("data/deleted/")
            for i in range(0, len(listidaccount), maxDel):
                id_slice = listidaccount[i:i+maxDel]
                filter2 = db.query(mailTable).filter(mailTable.id.in_(id_slice))
                mails = filter2.all()
                data = "\r".join("|".join(str(getattr_new(mail, i)).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexportdelete) for mail in mails if any(getattr_new(mail, i) for i in cotexportdelete))
                timenow = htime.getStrTimeNowFileName()
                hfile.write("data/deleted/" + timenow + ".txt", data, False)
                mail = filter2.delete(synchronize_session=False)
                if not mail:
                    toastSuccess("Delete 0 mail success")
                    continue
                db.commit()
                sleep(1)
            toastSuccess("Delete mail success")
    except Exception as e:
        db.rollback()
        error = hfile.getError()
        toastError(f"Delete mail fail {error}")

@eel.expose
def deleteAccountsOld(listidaccount: list):
    try:
        with Database() as db:
            filter = db.query(mailTable).filter(mailTable.id.in_(listidaccount))
            mails = filter.all()
            data = "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexportdelete) for mail in mails if any(getattr_new(mail, i) for i in cotexportdelete))
            timenow = htime.getStrTimeNowFileName()
            hfile.createDir("data/deleted/")
            hfile.write("data/deleted/" + timenow + ".txt", data, False)
            mail = filter.delete(synchronize_session=False)
            if not mail:
                toastSuccess("Delete 0 mail success")
                return

            db.commit()
            toastSuccess("Delete mail success")

    except Exception as e:
        db.rollback()
        error = hfile.getError()
        toastError(f"Delete mail fail {error}")
cotexport = ["email", "password", "emailrecovery",  "datecreate", "status",  "youtube", "country", "phonerecovery", "googlevoice", "statusdeletephone", "youtubepre", "paymentmethod", "securitycode", "statusconfirmsecurity", "devicelogout", "securityquestion", "chplay", "displayname", "youtubeverify", "checkhiddenphone", "datechangepass", "checkphonerecovery", "checkreviewgooglemap", "disableforwarding", "get2facode", "password_app", "checkgoogleadw", "createbrandaccountyoutube", "phone_verify", "browser" ]
cotexportdelete = cotexport.copy()
cotexportdelete.append("oldemail")
cotexportdelete.append("oldpassword")
cotexportdelete.append("oldemailrecovery")

def getattr_new(mail, i):

    data = getattr(mail, i)
    if i == "phone_verify":
        if data:
            data = str(data)
    if i == "googlevoice":
        # data = "3397070410"
        if data:
            data = str(data)
            if "(" in data:
                data = "(" + data.split("(")[1].strip()
            checklendata = hstr.regex(data, "(\\d{10})")
            if checklendata:
                data = "({}) {}-{}".format(checklendata[:3], checklendata[3:6], checklendata[6:])
            print("googlevoice", data, "-")
    if i == "securitycode":
        used = getattr(mail, "securitycodeused")
        if used:
            used = used.split(",")
            for z in used:
                if len(z) == 8:
                    data = data.replace(z, "")
            for z12 in range(12):
                if not ",," in data:
                    break
                data = data.replace(",,", "")
    return data
@eel.expose
def exportAccounts(listidaccount: list):
    try:
        with Database() as db:
            dataAll = ""
            dataSuccess = ""
            dataNoSuccess = ""
            dataNoRun = ""
            loginOk = ""
            loginFail = ""
            stopWhenPasswordSuccess = ""
            challenge_ipe = ""
            challenge_iap = ""
            maxDel = 10000
            for i in range(0, len(listidaccount), maxDel):
                toastWarning(f"Exporting {i}-{i+maxDel}")
                id_slice = listidaccount[i:i+maxDel]
                filter = db.query(mailTable).filter(mailTable.id.in_(id_slice))
                mails = filter.all()
                mailloginok = filter.filter(or_(mailTable.status.contains("changepass"), mailTable.status.contains("changeemailrecovery"), mailTable.status.contains("ok"))).all()
                stopwhenpasswordsuccess = filter.filter(mailTable.status.contains("stopwhenpasswordsuccess")).all()
                mailloginfail = filter.filter(~mailTable.status.contains("stopwhenpasswordsuccess"), ~mailTable.status.contains("changepass"), ~mailTable.status.contains("changeemailrecovery"), ~mailTable.status.contains("ok"), mailTable.status != "" , mailTable.status != None).all()
                if ck.user in ["Tri Thức"]:
                    challengeipe = filter.filter(mailTable.status.contains("challenge.ipe")).all()
                    challengeiap = filter.filter(mailTable.status.contains("challenge.iap")).all()

                mailsuccess = filter.filter(mailTable.status.contains("ok")).all()
                mailnosuccess = filter.filter(~mailTable.status.contains("ok"), mailTable.status != "" , mailTable.status != None).all()
                mailnorun = filter.filter(or_(mailTable.status == None, mailTable.status == "")).all()
                db.commit()

                dataAll = dataAll + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mails if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                dataSuccess = dataSuccess + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailsuccess if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                dataNoSuccess = dataNoSuccess + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailnosuccess if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                dataNoRun = dataNoRun + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailnorun if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                loginOk = loginOk + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailloginok if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                stopWhenPasswordSuccess = stopWhenPasswordSuccess + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in stopwhenpasswordsuccess if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                loginFail = loginFail + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailloginfail if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                if ck.user in ["Tri Thức"]:
                    challenge_ipe = challenge_ipe + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in challengeipe if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                    challenge_iap = challenge_iap + "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in challengeiap if any(getattr_new(mail, i) for i in cotexport)) + "\r"
                timenow = htime.getStrTimeNowFileName()
            hfile.createDir(f"data/export/{timenow}/")
            if dataAll.strip():
                hfile.write(f"data/export/{timenow}/ALL - {len(dataAll.splitlines())}.txt", dataAll, False)
            if loginOk.strip():
                hfile.write(f"data/export/{timenow}/LOGIN_OK - {len(loginOk.splitlines())}.txt", loginOk, False)
            if loginFail.strip():
                hfile.write(f"data/export/{timenow}/LOGIN_FAIL - {len(loginFail.splitlines())}.txt", loginFail, False)
            if dataSuccess.strip():
                hfile.write(f"data/export/{timenow}/SUCCESS - {len(dataSuccess.splitlines())}.txt", dataSuccess, False)
            if challenge_iap.strip():
                hfile.write(f"data/export/{timenow}/challenge_iap - {len(dataNoSuccess.splitlines())}.txt", challenge_iap, False)
            if challenge_ipe.strip():
                hfile.write(f"data/export/{timenow}/challenge_ipe - {len(dataNoSuccess.splitlines())}.txt", challenge_ipe, False)
            if dataNoSuccess.strip():
                hfile.write(f"data/export/{timenow}/NOSUCCESS - {len(dataNoSuccess.splitlines())}.txt", dataNoSuccess, False)
            if stopWhenPasswordSuccess.strip():
                hfile.write(f"data/export/{timenow}/STOP_WHEN_PASSWORD_OK - {len(stopWhenPasswordSuccess.splitlines())}.txt", stopWhenPasswordSuccess, False)
            if dataNoRun.strip():
                hfile.write(f"data/export/{timenow}/NORUN - {len(dataNoRun.splitlines())}.txt", dataNoRun, False)
            hfile.openFolder(f"data/export/{timenow}/")
            toastSuccess("Export mail success")
    except Exception as e:

        db.rollback()
        error = hfile.getError()
        toastError(f"Export mail fail {error}")

@eel.expose
def exportAccounts2(listidaccount: list):
    try:
        with Database() as db:
            allMail = db.query(mailTable).filter(mailTable.id.in_(listidaccount))
            mails = allMail.all()
            if not mails:
                toastSuccess("Export 0 mail success")
                return
            mailsuccess = allMail.filter(mailTable.status.contains("ok")).all()
            mailnosuccess = allMail.filter(~mailTable.status.contains("ok"), mailTable.status != "" , mailTable.status != None).all()
            mailnorun = allMail.filter(or_(mailTable.status == None, mailTable.status == "")).all()
            db.commit()
            data = "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mails if any(getattr_new(mail, i) for i in cotexport))
            dataSuccess = "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailsuccess if any(getattr_new(mail, i) for i in cotexport))
            dataNoSuccess = "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailnosuccess if any(getattr_new(mail, i) for i in cotexport))
            dataNoRun = "\r".join("|".join(getattr_new(mail, i).replace("\n", ",") if getattr_new(mail, i) else "" for i in cotexport) for mail in mailnorun if any(getattr_new(mail, i) for i in cotexport))
            timenow = htime.getStrTimeNowFileName()
            hfile.createDir("data/export/")
            hfile.write("data/export/" + timenow + "_ALL.txt", data, False)
            hfile.write("data/export/" + timenow + "_SUCCESS.txt", dataSuccess, False)
            hfile.write("data/export/" + timenow + "_NOSUCCESS.txt", dataNoSuccess, False)
            hfile.write("data/export/" + timenow + "_NORUN.txt", dataNoRun, False)
            hfile.openFolder("data/export/")
            toastSuccess("Export mail success")
    except Exception as e:

        db.rollback()
        error = hfile.getError()
        toastError(f"Export mail fail {error}")






def getMailById(id):
    try:
        with Database() as db:
            mail = db.query(mailTable).filter(mailTable.id==id).first()
            if not mail:
                return Result().to_dict()
            db.commit()
            msg={field.name: getattr(mail, field.name) for field in mailTable.__table__.columns}
            return Result(data=msg).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()



def get_mail():
    try:
        with Database() as db:
            mail = db.query(mailTable).filter(or_(mailTable.status == None, mailTable.status == "")).first()
            if not mail:
                return Result().to_dict()
            mail.status = "đã dùng"
            db.commit()
            msg={field.name: getattr(mail, field.name) for field in mailTable.__table__.columns}

            return Result(data=msg).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()
@eel.expose
def get_count_mail():
    try:
        with Database() as db:
            count = db.query(func.count(mailTable.id)).scalar()
            return Result(data=count).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get get_count_mail failed", e.args).to_dict()


@eel.expose
def get_mails(skip:int = 0, limit:int = 100):
    try:
        with Database() as db:
            mails = db.query(mailTable).offset(skip).limit(limit).all()
            if not mails:
                return Result().to_dict()
            db.commit()
            msg = [{field.name: getattr(mail, field.name) for field in mailTable.__table__.columns} for mail in mails]
            return Result(data=msg).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()

@eel.expose
def selectMails(status=""):
    try:
        # print(status)
        with Database() as db:
            # mails = db.query(mailTable.id).all()
            if status == "all":
                mails = [id[0] for id in db.query(mailTable.id).all()]
            elif status == "1":
                mails = [id[0] for id in db.query(mailTable.id).filter(mailTable.status != '').all()]
            elif status == "":
                mails = [id[0] for id in db.query(mailTable.id).filter(or_(mailTable.status == None, mailTable.status == '')).all()]
            else:
                mails = [id[0] for id in db.query(mailTable.id).filter(mailTable.status == status).all()]
            if not mails:
                return Result().to_dict()
            db.commit()
            data = mails
            return Result(data=data).to_dict()
    except Exception as e:
        print(e)
        db.rollback()
        return Result(False, "get mail failed", e.args).to_dict()



print("kkl", time.time() - t)


class checkKey:
    checkKeyStarted = False
    def __init__(self, sv, nameapp, delmodule="", keyapp=""):
        if not keyapp:
            keyapp = nameapp
        self.sv = sv
        self.nameapp = nameapp
        self.keyapp = keyapp

        self.hwid = ""
        self.user = ""
        self.message = ""
        self.status = {}
        self.__module = ""
        self.__delmodule = delmodule

    def start(self):
        if checkKey.checkKeyStarted:
            return

        # hthread.start(hwin32.refreshTrayIcon())
        from hmahoa import hmahoa
        self.hwid = hmahoa.getHwid(keyapp + "24")
        checkKey.checkKeyStarted = True
        while True:
            try:

                hashgoc = hmahoa.randomHash()

                hash = hmahoa.encryptAes256(hashgoc, "hash_encryptAes256_server")

                hash_del_module = hmahoa.encryptAes256(self.__delmodule, "hash_encryptAes256_server")
                nameapp = hstr.encodeUrl(self.nameapp)
                url = f"http://{self.sv}:8000/checkkey?hwid={self.hwid}&nameapp={nameapp}&format=json&hash={hash}&del_hash={hash_del_module}"

                text = hmahoa.get(url)

                if text == "disconnect":
                    from hcurl import hcurl
                    curl = hcurl()
                    rq = curl.get(url, proxy_active)
                    text = rq.text
                if not text:
                    self.message = "Cannot load server"
                    sleep(1)
                    continue
                content = hmahoa.decryptAes256(text, hashgoc)
                if not content:
                    self.message = text
                    self.status = {}
                    sleep(1)
                    continue
                status = json.loads(content)
                hash_response = status.get("hash", "")
                if not hash_response:
                    self.message = "Cannot load hash"
                    self.status = {}
                    sleep(1)
                    continue
                keymahoa = hmahoa.decryptAes256(hash_response, hashgoc)
                module = keymahoa.replace("_" + hashgoc, "")
                if not module or module != self.__delmodule:
                    sleep(1)
                    self.status = {}
                    continue
                # del socket
                self.message = ""
                self.status = status
                self.user = ck.status.get("hoten", "")
                self.status.pop("version")
                self.status.pop("hash")
                self.__module = module

                sleep(30)
            except ModuleNotFoundError as e:
                print(e)
                sleep(1)
            except Exception as e:
                print(e)
                self.message = e

                sleep(1)

    def reloadModule(self):
        import importlib
        function_string = self.__module + "." + self.__module
        mod_name, func_name = function_string.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        # importlib.reload(mod)
        hpw = getattr(mod, func_name)
        hpw = hpw()
        return hpw
    def isKeyActive(self, keyactive):
        name = md5(self.nameapp)
        iname = 0
        ok = 0
        for i, value in enumerate(keyactive):
            if i % 2 == 0:
                if value == name[iname]:
                    iname = iname + 1
                    ok = ok + 1
        if ok == 16:
            return True
        return False
# import subprocess

# command = r'C:\Users\Admin\appdata\roaming\nightowl\bit\bit-browser-112\BitBrowser.exe --lang=en-US,en;q=0.9 --remote-debugging-port=6777 --user-data-dir=C:\Users\Admin\appdata\roaming\nightowl\chrome\8468939144 --password-store=basic --gologin-profile=8468939144 --lang=en-US --font-masking-mode=2 --disable-encryption --donut-pie=undefined --flag-switches-begin --flag-switches-end --fingerprint-config="C:\Users\Admin\appdata\roaming\nightowl\bit\data\a367f26db2354312bbe08c14a6c5fcb4_285202313100" --force-device-scale-factor=0.4 --disable-extensions --disable-infobars --disable-gpu --no-sandbox --disable-sync-preferences --proxy-bypass-list=icanhazip.com,iphey.com'

# subprocess.Popen(command, shell=True)


sv = "45.32.118.181"
# sv = "localhost"
keyapp = "WKQI@!MDAO)Qekj193inaD@!30ADAma"
nameapp = "Gmail Changer"
def deleteModule(delmodule):
    def run():
        from hplaywright import hplaywright
        from sys import modules
        del modules[delmodule]
        for mod in modules.values():
            try:
                delattr(mod, delmodule)
            except AttributeError:
                pass
    hthread.start(run)
delmodule = "hplaywright"
deleteModule(delmodule)
ck = checkKey(sv, nameapp, delmodule, keyapp)
hthread.start(ck.start)


if __name__ == "__main__":
    # sleep(10)
    host="127.0.0.1"
    t = time.time()
    print("kk", time.time() - t)
    port = free_port()

    print(host + ":" + str(port))

    # startEel(host=host, port=port, size=(1200,790), orbita_browser_check=orbita_browser_check, title=con.title)
    startEel(host=host, port=port, size=(1200,790), title="GMAIL MANAGE", use_cef=True)
