
from reload import *
from hwin import *
# from hexcel import *
from script.expose import *
from script.sqlalchemy import mailTable, Database, mailClass, Result, getConfig, Config
from hplaywright import *
from hplaywrightExtended import *

ini = hini()
lock = threading.Lock()
lockextractext = threading.Lock()
lockconfig = threading.Lock()
lock_clipborad = threading.Lock()


class Gmail:
    def __init__(self):
        self.user_info = ""
        self.browser = None
        self.user = None
        self.passs = None
        self.email_lower = ""
        self.fast_send = False
        self.emailrecovery = None
        self.p = None
        self.rapt = ""
        self.data = ""
        self.orbita_browser_check = ""
        self.ck = None
        self.proxy = ""
        self.sleep_enter = 0
        self.delay = 100
        self.verifyphone = ""
        self.stopwhenpasswordsuccess = ""
        self.restoredisablecontent = []
        self.restoredisable2_mail = []
        self.restoredisablecontact = []
        self.emailrecoverydomain = []
        self.emailrecoveryrandom = []
        self.passwordrandom = []
        self.listdisplayname = []
        self.restoredisable = ""
        self.otpdataVerify = ""
        self.normalcaptcha_data = ""
        self.recaptcha_data = ""
        self.otpdataVoice = ""
        self.otpdataYoutube = ""
        self.timeout = 60
        self.windowsize = []
        self.windowpos = []
        self.passchanged = False
        self.ithread = 0
        self.iloadfail = 0
        self.getrapt = ""
        self.checkkhoiphuc = 0
        self.checkphonerecoveryok = True
        self.user_tool = ""
        self.linklogin = ""
        self.linkketqua = ""
        self.nopecha = ""
        self.khoiphuctaikhoan = ""
        self.tutquyetnguyen1 = ""
        self.khoiphuctaikhoan_mail = ""
        self.khoiphuctaikhoan_pass = ""
        self.scale = 0.4
        self.saveprofile = 0
        self.gialapclick = 0
        self.path_saveprofile = ""
        self.verify_ok = False
        self.loginok = False
        pass

    def getError(self):
        msgFail = self.p.locatorSelector('p > span[id="error"]').text()
        if msgFail:
            return msgFail
        msgFail = self.p.locatorJsname("B34EJ").text()
        if msgFail:
            return msgFail
        return ""

    def getNewPass(self):
        if self.passwordrandom:
            passwordrandomtmp = hrand.randomItemInList(self.passwordrandom).strip()
            if len(passwordrandomtmp) >= 8:
                return passwordrandomtmp
        total = 0

        low = self.data["email"].lower().split("@")[0]
        if low.isdigit():
            return hrand.randomPassword()
        lowfor = low + self.passs
        for c in lowfor:
            char_value = ord(c)  # lấy mã ASCII của ký tự
            char_as_char = chr(char_value)  # chuyển đổi mã ASCII thành kiểu char
            total += ord(char_as_char)  # cộng dồn vào tổng
        newpass = low + str(total+2048 + hrand.randomInt(0, 7000))
        return newpass

    def getNewEmailRecovery(self):

        newemailrecovery = ""
        if self.emailrecoveryrandom:
            with lockconfig:
                config = getConfig()
                data = config.get("data", "")
                if data:
                    line_email_recovery_random = data.get("line_email_recovery_random", -1)
                    if line_email_recovery_random >= 0:
                        if line_email_recovery_random >= len(self.emailrecoveryrandom):
                            line_email_recovery_random = 0
                    data["line_email_recovery_random"] = line_email_recovery_random + 1
                    self.updateConfig(data)
                    newemailrecoverytmp = self.emailrecoveryrandom[line_email_recovery_random].strip()
                else:
                    newemailrecoverytmp = hrand.randomItemInList(self.emailrecoveryrandom).strip()
                if "." in newemailrecoverytmp and "@" in newemailrecoverytmp:
                    newemailrecovery = newemailrecoverytmp
        if newemailrecovery:
            return newemailrecovery
        emailtest = self.emailrecovery
        if not "@" in emailtest:
            emailtest = self.user
        if not "@" in emailtest:
            emailtest = self.user + "@gmail.com"

        total = 0
        low = self.data["email"].lower().split("@")[0]
        lowfor = low + emailtest
        for c in lowfor:
            char_value = ord(c)  # lấy mã ASCII của ký tự
            char_as_char = chr(char_value)  # chuyển đổi mã ASCII thành kiểu char
            total += ord(char_as_char)  # cộng dồn vào tổng
        dau = low + str(total+2048)

        duoi = "hotmail.com"
        if self.emailrecoverydomain:
            duoitmp = hrand.randomItemInList(self.emailrecoverydomain).strip()
            if "." in duoitmp:
                duoi = duoitmp
                if duoi.startswith("@"):
                    duoi = hstr.subString(duoi, 1)
        newemailrecovery = dau + "@" + duoi
        return newemailrecovery

    def detect_error_page(self):
        error = self.p.locatorSelector("#af-error-container")
        if error.isdisplay():
            return True
        error = self.p.locatorSelector("#af-error-page2")
        if error.isdisplay():
            return True
        return False

    def khoi_phuc_tai_khoan(self):
        from himap import himap
        self.imap = himap()
        p = self.p
        timestart = time.time()
        listcode = []
        clicknextcodemail = False
        back = False
        cookie = hfile.read("data/yandex.txt")
        get_code_lan_dau = True
        doipass = False
        checklailannua = True
        while time.time() - timestart < 320:
            try:
                url = p.get_url()
                if not url:
                    return "browser_closed"
                if not "/recoveryidentifier" in url:
                    self.openUrl(
                        "https://accounts.google.com/signin/v2/recoveryidentifier?flowName=GlifWebSignIn&flowEntry=AccountRecovery", self.lastUrl)
                if "/recoveryidentifier" in url:
                    identifierId = p.locatorSelector("#identifierId")
                    if identifierId.isdisplay():
                        if self.getError():
                            return self.getError()
                        identifierId.send(self.usertype, press="Enter", fast_send=self.fast_send)
                        # identifierId.type(self.user, press="Enter")
                        p.sleep(2)
                elif "/recaptcha" in url:
                    thucachkhac = p.locatorSelector(".VfPpkd-vQzf8d")
                    if thucachkhac.count() == 2:
                        ExtendedLocator(thucachkhac.nth(1)).click()
                        p.sleep(1)
                elif "/pwd" in url or "/hpwd" in url:
                    clicknextcodemail = False
                    password = p.locatorSelector('*[type="password"]')
                    if password.isdisplay():
                        password.send(self.passs, press="Enter", fast_send=self.fast_send)
                        # password.type(self.passs, press ="Enter")
                        p.sleep(2)
                elif "/recovery-options-collection" in url:
                    tel = p.locatorSelector('*[type="tel"]')
                    if tel.isdisplay():
                        self.getRapt()
                        return "login ok"
                    email = p.locatorSelector('*[type="email"]')
                    if email.isdisplay():
                        email.send(self.emailrecovery, press="Enter", fast_send=self.fast_send)
                        # email.type(self.emailrecovery, press="Enter")
                    pass
                elif "/endsession" in url:
                    return "48h"
                elif doipass and url.startswith("https://myaccount.google.com/?"):
                    p.goto("https://myaccount.google.com/signinoptions/recovery-options-collection?oev=lytf%3D7%26wvtx%3D6%26trs%3Dsae&utm_medium=App&utm_campaign=sae&hl=fr")
                    p.sleep(1)
                elif "/security-checkup" in url:
                    url = url.replace("%3D", "=")
                    rapt = hstr.regex(url + "&", "rapt=(.*?)&")
                    if rapt:
                        p.goto(
                            f"https://myaccount.google.com/signinoptions/recovery-options-collection?oev=lytf%3D7%26wvtx%3D6%26trs%3Dsae&utm_medium=App&utm_campaign=sae&hl=fr&rapt={rapt}")
                        p.sleep(1)
                    else:
                        return "lấy_thông_tin_lỗi"
                elif "/changepasswordform" in url or "/signinoptions/password" in url:
                    passwords = p.locatorSelector('*[type="password"]')
                    if passwords.count() == 2:
                        xacnhandoimatkhau_dangxuatdevices = p.locatorSelector('.RveJvd.snByac')
                        for i in range(xacnhandoimatkhau_dangxuatdevices.count()):
                            xacnhandoimatkhau_dangxuatdevice = ExtendedLocator(xacnhandoimatkhau_dangxuatdevices.nth(i))
                            if not xacnhandoimatkhau_dangxuatdevice.isdisplay():
                                continue
                            if xacnhandoimatkhau_dangxuatdevice.text() != "Đổi mật khẩu":
                                continue
                            xacnhandoimatkhau_dangxuatdevice.click()
                            p.sleep(2)
                            continue
                        pass1 = ExtendedLocator(passwords.nth(0))
                        pass2 = ExtendedLocator(passwords.nth(1))
                        if pass1.isdisplay() and pass2.isdisplay():
                            pass1.send(self.passs, fast_send=self.fast_send)
                            pass2.send(self.passs, press="Enter", fast_send=self.fast_send)
                            # pass1.type(self.passs)
                            # pass2.type(self.passs, press ="Enter")
                            doipass = True
                            p.sleep(1)
                            continue
                    capnhatmatkhau = p.locatorSelector(".VfPpkd-vQzf8d")
                    if capnhatmatkhau.count() == 2:
                        ExtendedLocator(capnhatmatkhau.nth(1)).click()
                elif "/changepassword" in url or "recovery/summary" in url:
                    capnhatmatkhau = p.locatorSelector(".VfPpkd-vQzf8d")
                    if capnhatmatkhau.count() == 2:
                        ExtendedLocator(capnhatmatkhau.nth(1)).click()
                elif "/ipe" in url:
                    content = ""
                    if not clicknextcodemail:
                        content = p.content()
                    if "••••@" in content:
                        if checklailannua:
                            p.sleep(1)
                            checklailannua = False
                            continue
                        thucachkhac = p.locatorSelector(".VfPpkd-vQzf8d")
                        if thucachkhac.count() == 2:
                            log(f"Tab {self.ithread} click thucachkhac")
                            ExtendedLocator(thucachkhac.nth(1)).click()
                            p.sleep(1)
                            clicknextcodemail = True
                    else:
                        idvPinId = p.locatorSelector("#idvPinId")
                        if idvPinId.isdisplay():
                            if get_code_lan_dau:
                                p.sleep(3)
                                get_code_lan_dau = False
                            yan = yandex()
                            yan.cookie = cookie
                            code = yan.get_code(self.user.lower())
                            if code:
                                idvPinId.send(code, press="Enter", fast_send=self.fast_send)
                                # idvPinId.type(code, press="Enter")
                                p.sleep(5)
                                continue
                elif "/selection?" in url:
                    undefined = p.locatorSelector('*[data-challengetype="undefined"]')
                    if not undefined.isdisplay():
                        p.sleep(1)
                        continue
                    sendmail = p.locatorSelector('*[data-sendidvemail="true"]')
                    count = sendmail.count()
                    if count == 3:
                        ExtendedLocator(sendmail.nth(2)).click()
                    if count == 2:
                        ExtendedLocator(sendmail.nth(1)).click()
                    if count == 0:
                        log(f"Tab {self.ithread} click undefined")
                        undefined.click()
                    p.sleep(1)
                    continue
                elif "/ipp" in url:
                    return "so_dien_thoai"
                elif "/ootp" in url or "/totp" in url or "/bc" in url:
                    thucachkhac = p.locatorSelector(".VfPpkd-vQzf8d")
                    if thucachkhac.count() == 2:
                        ExtendedLocator(thucachkhac.nth(1)).click()
                        p.sleep(1)
                elif "/wa" in url:
                    thucachkhac = p.locatorSelector(".VfPpkd-vQzf8d")
                    if thucachkhac.count() == 1:
                        ExtendedLocator(thucachkhac.nth(0)).click()
                        p.sleep(1)
                elif "deniedsigninrejected" in url:
                    if not back:
                        p.sleep(1)
                        p.back()
                        back = True
                        continue
                    return "không_thể_khôi_phục"
            except Exception as e:
                hfile.getError()
                # print(e)
                pass
            p.sleep(1)
        return "timeout_không_thể_khôi_phục"
        # autoReload("f1", self)

    def login(self):
        try:

            from hcaptcha import hcaptcha
            from htime import htime
            from hotp import hotp
            self.id = -1
            if self.data:
                self.id = self.data["id"]
            self.securitycode = self.data["securitycode"]
            if self.data["get2facode"]:
                self.securitycode = self.data["get2facode"] + "," + self.securitycode
            user = self.data["email"]
            passs = self.data["password"]
            emailrecovery = self.data["emailrecovery"]
            phonerecovery = self.data["phonerecovery"]
            fname = name()
            solve_normalcaptcha = hcaptcha(self.normalcaptcha_data)
            solve_recaptcha = hcaptcha(self.recaptcha_data)
            self.otp = hotp(self.otpdataVerify)
            self.otpyoutube = hotp(self.otpdataYoutube)
            self.otpVoice = hotp(self.otpdataVoice)
            # print(self.otpVoice.website)
            # print(self.otpVoice.apikey)
            # print(self.otpVoice.serviceId)
            # self.otp.time_wait_phone = 15*60
            # self.otp.start()
            # self.otp.getCode()
            addlangvn = "&hl=en"
            addlangvn = ""
            self.solanfail = 0
            self.solanthulai = 0
            if "otptextnow.com" in self.otp.website or "xotp.pro" in self.otp.website or "winmail.shop" in self.otp.website:
                self.solanthulai = 1
                addlangvn = "&hl=vi"
            # if "tskvb.com" in self.otp.website:
            #     self.solanthulai = 0
            #     addlangvn = "&hl=vi"
            self.user = user
            self.email_lower = user.lower().strip().replace("@googlemail.com", "@gmail.com")
            if not "@" in self.email_lower:
                self.email_lower = self.email_lower + "@gmail.com"
            self.passs = passs

            self.emailrecovery = emailrecovery
            self.phonerecovery = phonerecovery
            self.securityquestion = self.data["securityquestion"]
            if self.emailrecovery:
                if not "@" in self.emailrecovery:
                    if not self.securityquestion:
                        self.securityquestion = self.emailrecovery
                        self.data["securityquestion"] = self.securityquestion
                        self.updateMail()
            self.usertype = self.user.lower()
            if self.usertype.endswith("@gmail.com"):
                self.usertype = self.usertype.replace("@gmail.com", "")
            # proxy = "socks5://185.199.229.156:7492:sgtpxvzw:d2x2sf3vd4eh"
            # proxy = "45.32.79.147:10004"
            # proxy = "45.94.47.66:8110:sgtpxvzw:d2x2sf3vd4eh"


            hpw = hplaywright()
            # hpw.block_image = True
            # hpw.block_video = True
            if not hpw.success:
                return self.login()

            # hpw.proxyBypassList = ["icanhazip.com", "iphey.com"]

            hpw.scale = self.scale
            # hpw.scale = 1
            hpw.size = self.windowsize
            hpw.pos = self.windowpos
            hpw.browser = self.browser
            # hpw.keepNetwork = True
            if self.nopecha:
                with lockextractext:
                    nopecha_ext = hpath.nightowl() + "/extension/nopecha"
                    nopecha_ext = hfile.fixFileName(nopecha_ext)
                    if not hfile.checkExists(nopecha_ext + "/manifest.json"):
                        hfile.createDir(nopecha_ext)
                        hfile.unzip(hpath.dirScript() + "/script/nopecha.zip", nopecha_ext)
                    if hfile.checkExists:
                        hpw.chromeExtensionList.append(nopecha_ext.replace("\\", "/"))
            else:
                if solve_recaptcha.success:
                    if "2captcha" in solve_recaptcha.website:
                        ext_cap = hpath.nightowl() + "/extension/2captcha"
                        ext_cap = hfile.fixFileName(ext_cap)
                        if not hfile.checkExists(ext_cap + "/manifest.json"):
                            hfile.createDir(ext_cap)
                            hfile.unzip(hpath.dirScript() + "/script/2captcha.zip", ext_cap)
                        if hfile.checkExists:
                            hpw.chromeExtensionList.append(ext_cap.replace("\\", "/"))
                    if "1stcaptcha" in solve_recaptcha.website:
                        ext_cap = hpath.nightowl() + "/extension/1stcaptcha"
                        ext_cap = hfile.fixFileName(ext_cap)
                        if not hfile.checkExists(ext_cap + "/manifest.json"):
                            hfile.createDir(ext_cap)
                            hfile.unzip(hpath.dirScript() + "/script/1stcaptcha.zip", ext_cap)
                        if hfile.checkExists:
                            hpw.chromeExtensionList.append(ext_cap.replace("\\", "/"))
            # hpw.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            # hpw.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
            # hpw.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            # hpw.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            user_data_dir = ""

            if self.path_saveprofile:
                user_data_dir = self.path_saveprofile + "\\" + self.email_lower
            self.p = hpw.openChrome(self.proxy, user_data_dir=user_data_dir, executable=self.orbita_browser_check)


            self.p: ExtendedPage
            if not self.p:
                return self.login()

            self.hpw = hpw
            p = self.p
            # if "Tiến Tùng" in self.user_info or "admin" in self.user_info:
            #                 return "testing"
            # return "login ok"
            # p.goto("https://privacycheck.sec.lrz.de/active/fp_c/fp_canvas.html")
            # p.goto("https://webbrowsertools.com/canvas-fingerprint")
            # p.goto("https://dvcs.w3.org/hg/d4e/raw-file/tip/mouse-event-test.html")
            # p.goto("https://unixpapa.com/js/testmouse.html")

            test = True
            test = False
            if test:
                # p.goto("https://browserleaks.com/canvas")
                # p.goto("http://f.vision/")
                # p.goto("https://fingerprintjs.github.io/fingerprintjs/")
                # p.goto("https://pixelscan.net/")
                # p.goto("https://iphey.com")
                # confirmidentifier
                while 1:
                    p.sleep(1)
            # p.goto("chrome://welcome/")
            # p.reload()

            # if hpw.browser_name == "hidemium":
            #     self.lastUrl = "about:blank"

            urlRapt = [
                "https://myaccount.google.com/interstitials/birthday",
                "https://gds.google.com/web/chip",
                "https://myaccount.google.com/signinoptions/rescuephone",
                "https://myaccount.google.com/?utm_source=sign_in_no_continue",
                "https://myaccount.google.com/signinoptions/recovery-options-collection",
                "https://accounts.google.com/u/0/recovery/summary",
                "https://accounts.google.com/signin/drt?",
                "https://myaccount.google.com/device-activity",
            ]
            recovery = False
            timestart = time.time()
            recaptcha = 0
            phoneresend = {}
            p.goto("https://www.gmx.net/")
            self.lastUrl = ""
            firsturl = "https://www.gmx.net/"
            passwordsender = False
            chaytutquyennguyen1 = False
            if self.tutquyetnguyen1 and self.self.user_info in ["admin", "Quyet Nguyen"]:
                chaytutquyennguyen1 = True
            chaytutquyennguyen1_landau = True

            xacminh_extension = False


            use_extension_bypasss = False
            clickedit = False

            inopecha = 0
            resettime = 0
            progressbar_time = 0
            # self.lastUrl = p.url
            assistiveActionOutOfQuota_count = 0
            self.loginok = False
            def handle_route(route: Route):
                request: Request = route.request

                # headers = request.headers
                url = request.url
                if "epimetheus.navigator.gmx.net/monitoring/compat" in url or "epimetheus.navigator.gmx.net/monitoring/ppp" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "dl.gmx.net/tcf/live/v1/js/tcf-api.js" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "dl.gmx.net/uim/live/config_logout.js" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "permission-client.js" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "service.min.js" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "permission-core.min.js" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "permission-client-compat.js" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "roboto-medium.woff2" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if "plus.gmx.net" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if not "gmx.net" in url and not "gmx.de" in url:
                    route.fulfill(body="")
                    # route.abort()
                    return
                if url.endswith(".png") or url.endswith(".tiff") or url.endswith(".svg") or url.endswith(".ogg") or url.endswith(".webp") or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".mp3")  or url.endswith(".gif"):
                    # route.abort()
                    route.fulfill(body="")
                    return

                print(url)
                route.continue_()
            self.p.route("**/*", handle_route)
            while time.time() - timestart < 300:
                try:


                    freemailLoginUsername = p.find_selector("#freemailLoginUsername")
                    if freemailLoginUsername.isdisplay():
                        freemailLoginUsername.send(self.email_lower, fast_send=True)
                        freemailLoginPassword = p.find_selector("#freemailLoginPassword")
                        if freemailLoginPassword.isdisplay():
                            freemailLoginPassword.send(self.passs, fast_send=True, press="Enter")

                    self.openUrl(firsturl, self.lastUrl)
                    if self.iloadfail > 10:
                        return "timeout.login"

                    url = p.url
                    if "https://www.gmx.net/logoutlounge/?status=login-failed" in url:
                        while 1:
                            p.sleep(1)
                        return "sai_pass"
                    if "navigator.gmx.net/login" in url:
                        return "login ok"
                    if "interceptiontype=ForceChangePasswordLock" in url:
                        return "login ok"
                    if "interceptiontype=MtanObligation" in url:
                        return "login ok"
                    if "interceptiontype=PushNotificationObligation" in url:
                        return "login ok"


                except Exception as e:
                    error = e.args[0]
                    if "Target page, context or browser has been closed" in error:
                        return "disconnect.login"
                    print(e)
                p.sleep(1)
        except:
            hfile.getError()
        return "timeout.login"

    def get_2fa_code(self):
        p = self.p
        self.lastUrl = p.url
        timestart = time.time()
        while time.time() - timestart < 60:
            try:
                self.openUrl(
                    f"https://myaccount.google.com/two-step-verification/backup-codes?hl=en&rapt={self.rapt}", self.lastUrl)
                Turn_on = p.locatorText('Turn on')
                if Turn_on.isdisplay():
                    return "disable.2fa"
                Get_new_codes = p.locatorText("Get new codes")
                if Get_new_codes.isdisplay():
                    Get_new_codes.click()
                    p.sleep(3)
                Get_backup_codes = p.locatorText("Get backup codes")
                if Get_backup_codes.isdisplay():
                    Get_backup_codes.click()
                codes = p.locatorSelector(".ibJClf")
                codes_count = codes.count()
                if codes_count > 0 and codes_count < 10:
                    get_new_code = p.locatorSelector('*[aria-label="Generate new codes"]')
                    if get_new_code.isdisplay():
                        get_new_code.click()
                elif codes_count == 10:
                    code_all = []
                    for i in range(codes_count):
                        code_now = ExtendedLocator(codes.nth(i)).text()
                        code_all.append(code_now.replace(" ", ""))
                    code_all = hstr.listToString(code_all, ",")
                    self.data["get2facode"] = code_all
                    self.updateMail()
                    self.get_code_ok = True
                    return "ok"
            except:
                pass
            p.sleep(1)
        return "timeout"

    def changePass(self):
        if self.passchanged:
            return "ok"
        newpass = self.getNewPass()
        p = self.p
        p.goto("https://myaccount.google.com/signinoptions/password?rapt=" + self.rapt)
        timestart = time.time()
        while time.time() - timestart < 60:
            try:
                url = p.url
                newPwd = p.locatorName("password")
                newRePwd = p.locatorName("confirmation_password")
                if newPwd.isdisplay() and newRePwd.isdisplay():
                    newPwd.send(newpass, fast_send=self.fast_send)
                    # newPwd.type(newpass, delay=self.delay)
                    self.data["password"] = newpass
                    self.data["datechangepass"] = htime.getStrTimeNow() + "_changepass"
                    self.updateMail()
                    newRePwd.send(newpass, press="Enter", fast_send=self.fast_send)
                    # newRePwd.type(newpass, delay=self.delay, press="Enter", sleep_enter=self.sleep_enter)
                    newRePwd.waitHidden()
                if url.startswith("https://myaccount.google.com/security-checkup-welcome"):
                    return "ok"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.changepass"

    def restoreDisable(self):
        p = self.p
        timestart = time.time()
        while time.time() - timestart < 60:
            p.sleep(1)
            url = p.url
            if "https://accounts.google.com/signin/v2/disabled/appeal/additionalinformation" in url:
                textarea = p.locatorSelector("textarea")
                if textarea.is_visible():
                    content = hrand.randomItemInList(self.restoredisablecontent)
                    # textarea.send(content, press="Enter")
                    if self.fast_send:
                        textarea.send(content, press="Enter", fast_send=self.fast_send)
                    else:
                        textarea.type(content, delay=10, press="Enter", timeout=20, sleep_enter=self.sleep_enter)
                    textarea.waitHidden(5)
            elif "https://accounts.google.com/signin/v2/disabled/takeout/start" in url:
                p.go_back(timeout=1000)
            elif "https://accounts.google.com/signin/v2/disabled/appeal/received" in url:
                return "restore.disable.ok"
            elif "https://accounts.google.com/signin/v2/disabled/appeal/confirmation" in url:
                return "restore.disable.ok"
            elif "https://accounts.google.com/signin/v2/disabled/appeal/contactaddress" in url:
                input = p.locatorSelector('input[type="email"]')
                if input.is_visible():
                    # if "@" in self.emailrecovery:
                    #     newmail = self.emailrecovery
                    # else:
                    #     newmail = self.user.split("@")[0] + "@hotmail.com"
                    contact = hrand.randomItemInList(self.restoredisablecontact)
                    input.send(contact, press="Enter", fast_send=self.fast_send)
                    # input.type(contact, delay=100, press="Enter", sleep_enter=self.sleep_enter)
                    input.waitHidden(5)
            else:
                batdaukhieunai = p.locatorSelector(".VfPpkd-vQzf8d").first
                if batdaukhieunai.is_visible():
                    batdaukhieunai.click()
        return "restore.disable.timeout"

    def changeEmailRecovery(self):
        # autoReload("function1", self, 100000)
        def get_code_duc_tung(email, authorization):
            rq = hrequest()
            for i in range(30):
                rq.addHeader("Authorization: " + authorization )
                html = rq.get_html(f"http://146.190.91.114:31005/messages?inbox={email}")
                dic = hstr.str_to_json(html)
                results = dic.get("results", [])
                for result in results:
                    id = result.get("id", "")
                    rq.addHeader("Authorization: " + authorization )
                    html = rq.get_html(f"http://146.190.91.114:31005/message/{id}")
                    dic = hstr.str_to_json(html)
                    text_body = dic.get("text_body", "")
                    code = hstr.regex(text_body, email + '.{3,360}(\\b\\d{6}\\b)', re.DOTALL)
                    if code:
                        return code
                time.sleep(1)
            return ""
        newemailrecovery = self.getNewEmailRecovery()
        p = self.p
        url = p.url
        if not url.startswith("https://myaccount.google.com/recovery/email"):
            p.goto("https://myaccount.google.com/recovery/email?rapt=" + self.rapt)
        # timestart = time.time()
        nhap_email_ok = False
        for z in range(60):
            try:
                url = p.url
                if url.startswith("https://myaccount.google.com/recovery/email"):
                    verifiCode = p.locatorSelector('*[maxlength="6"]')

                    if verifiCode.count():
                        verifiCode = ExtendedLocator(verifiCode.nth(0))
                    if verifiCode.isdisplay():
                        nhap_email_ok = True
                        if not "animocansiva.online" in newemailrecovery:
                            return "ok"
                        code = get_code_duc_tung(newemailrecovery, "YZAF6srew3IACQ6Sj9QIgIBHh9EKt4O7Kbm2qv7NVs")
                        verifiCode.send(code, press="Enter")
                        p.sleep(3)
                        continue
                        # print(code)
                    newEmails = p.locatorSelector('*[type="email"]')
                    count = newEmails.count()
                    for i in range(count):
                        newEmail = ExtendedLocator(newEmails.nth(i))
                        if newEmail.displayed():
                            if nhap_email_ok:
                                return "ok"
                            if i == count - 1:
                                self.data["emailrecovery"] = newemailrecovery
                                self.updateMail()
                                p.sleep(1)
                                newEmail.send(newemailrecovery,  press="Enter", fast_send=self.fast_send)
                                # newEmail.type(newemailrecovery, delay=self.delay, press="Enter",  timeout=20, sleep_enter=self.sleep_enter)
                                p.sleep(5)
                            else:
                                newEmail.send(newemailrecovery, fast_send=self.fast_send)
                                # newEmail.type(newemailrecovery, delay=self.delay, timeout=20)
            except Exception as e:
                print(e)
            p.sleep(1)
        return "Timeout"

    def change_language(self):
        p = self.p
        url = p.url
        if not "https://myaccount.google.com/language" in url:
            p.goto("https://myaccount.google.com/language?hl=en")
        timestart = time.time()
        while time.time() - timestart < 60:
            try:
                url = p.url
                if not "https://myaccount.google.com/language" in url:
                    p.goto("https://myaccount.google.com/language?hl=en")
                text = p.locatorSelector(".xsr7od").text()
                if "United States" in text:
                    return "United States"
                displaylang = False
                enterlang = p.locatorAriaLabel("English")
                if enterlang.isdisplay():
                    displaylang = True
                    enterlang.click()
                enterlang = p.find_selector('*[data-language-code="en"]')
                if enterlang.isdisplay():
                    displaylang = True
                    enterlang.click()
                    p.sleep(1)
                enterlang = p.locatorAriaLabel("United States")
                if enterlang.isdisplay():
                    displaylang = True
                    enterlang.click()
                    p.sleep(2)
                    save = p.find_aria_label("Save your language selection")
                    if save:
                        save.click()

                enterlang = p.locatorAriaLabel("Enter language", "input")
                if enterlang.isdisplay():
                    displaylang = True
                    enterlang.click()
                    enterlang.send("English")

                select = p.locatorText('Select')
                if select.displayed():
                    select.click()

                if not displaylang:
                    edits = p.locatorSelector("span[class=VfPpkd-kBDsod]").findLocatorDisplay()
                    if edits:
                        edits.click(force=True)
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout_change_language"

    def check_google_adw(self):
        p = self.p
        url = p.url

        # driver = self.driver
        # s = self.s
        # s.get("https://ads.google.com/aw/settings")
        # time.sleep(1)
        # url = ""
        # html = ""
        # selectus = False
        # for i in range(20):
        #     url = self.getUrl()
        #     try:
        #         if "ads.google.com/nav/selectaccount" in url:
        #             return "No"
        #         elif "/ipp" in url:
        #             return "Phone"
        #         elif "ads.google.com/aw/browser_not_supported" in url:
        #             return "browser_not_supported"
        #         elif "ads.google.com/aw/settings" in url:
        #             return "Success"
        #         if "ServiceNotAllowed" in url:
        #             return "ServiceNotAllowed"
        #         if "servicerestricted" in url:
        #             return "servicerestricted"
        #     except:
        #         pass
        #     time.sleep(1)
        # return "timeout"

        if not "https://ads.google.com/aw/settings" in url:
            p.goto("https://ads.google.com/aw/settings")
        timestart = time.time()
        while time.time() - timestart < 60:
            try:
                url = p.url
                if "ads.google.com/nav/selectaccount" in url:
                    return "adw_no"
                elif "/ipp" in url:
                    return "adw_phone"
                elif "ads.google.com/aw/browser_not_supported" in url:
                    return "adb_browser_not_supported"
                elif "ads.google.com/aw/settings" in url:
                    return "adw_success"
                if "aw/campaigns/new/express" in url:
                    return "adw_new_express"
                if "ServiceNotAllowed" in url:
                    return "adw_servicenotallowed"
                if "multifactorauthalert" in url:
                    return "adw_multifactorauthalert"
                if "servicerestricted" in url:
                    return "adw_servicerestricted"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout_check_google_adw"

    def checkCountry(self):

        p = self.p
        url = p.url
        if not "https://policies.google.com/terms" in url:
            p.goto("https://policies.google.com/terms?hl=en")
        timestart = time.time()
        while time.time() - timestart < 30:
            try:
                source = p.content()
                country = hstr.regex(source, "Country version:</a>(.*?)</p>").strip()
                if country:
                    return country
            except Exception as e:
                print(e)
            p.sleep(1)
        return "Timeout"

    def disable_forwarding(self):
        p = self.p
        url = p.url
        self.lastUrl = p.url

        timestart = time.time()
        while time.time() - timestart < 30:
            try:
                self.openUrl("https://mail.google.com/mail/u/0/#settings/fwdandpop", self.lastUrl)
                sx_em = p.locatorSelector('*[name="sx_em"][value="0"]')
                if sx_em.isdisplay():
                    sx_em.click()
                    submit = p.locatorSelector('button[guidedhelpid="save_changes_button"]')
                    if submit.isdisplay():
                        submit.click()
                        p.sleep(5)
                        return "ok.disable_forwarding"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.disable_forwarding"

    def checkGoogleEmail(self):
        p = self.p
        url = p.url
        if not "https://myaccount.google.com/email" in url:
            p.goto("https://myaccount.google.com/email")
        timestart = time.time()
        while time.time() - timestart < 30:
            try:
                googleemail = p.locatorSelector(".mMsbvc").first
                if ext.isdisplay(googleemail):
                    text = ext.getText(googleemail)
                    if "@" in text:
                        self.data["email"] = text
                        self.updateMail()
                        return "ok"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "Timeout"

    def logout_device(self, chi_dang_xuat_thiet_bi_cu = False):
        p = self.p
        self.lastUrl = p.url
        self.eid = {}
        # autoReload("f1", self)

        timestart = time.time()
        time_id = {}
        while time.time() - timestart < 180:
            try:
                patter = "device-activity/id/.*?(\\w+)"
                # .IfU6xc.D2Bhy
                self.openUrl("https://myaccount.google.com/device-activity", self.lastUrl)
                if "We're sorry..." in p.content():
                    p.reload()
                if "/signinchooser" in p.url:
                    return "ok.logout"
                if "/connections" in p.url:
                    return "fail.logout"
                if p.url.startswith("https://myaccount.google.com/device-activity/id"):
                    id = hstr.regex(p.url, patter)
                    if id:
                        if not id in time_id:
                            time_id[id] = time.time()
                        if time.time() - time_id[id] > 20:
                            p.reload()
                            time_id[id] = time.time()
                            continue
                        for i in range(20):

                            signouts = p.locatorSelector('.VfPpkd-rOvkhd-LatNUc')
                            count = signouts.count()
                            for z1 in range(count):
                                signout = ExtendedLocator(signouts.nth(z1))
                                if signout.isdisplay():
                                    htmlouter = signout.getOuterHtml()
                                    if "M18,23 L8,23 C6.9,23 6,22.1 6,21 L6,18 L8,18 L8,21 L18,21 L18,3 L8,3 L8,6 L6,6 L6,3 C6,1.9 6.9,1 8,1 L18,1 C19.1,1 20,1.9 20,3 L20,21 C20,22.1 19.1,23 18,23 Z M9.41,8.41 L6.83,11 L14,11 L14,13 L6.83,13 L9.42,15.59 L8,17 L3,12 L8,7 L9.41,8.41 Z" in htmlouter:
                                        signout.click()
                                        self.eid[id] = True
                                        break
                            signout2 = p.locatorSelector('*[jsname="bN97Pc"] + div *[data-id="EBS5u"]')
                            if signout2.isdisplay():
                                signout2.click()
                                self.eid[id] = True
                            if id in self.eid:
                                break
                            p.sleep(1)
                        if not id in self.eid:
                            self.eid[id] = False
                        if not self.eid[id]:
                            p.goto("https://myaccount.google.com/device-activity")

                else:
                    # continue
                    canhbaos = p.locatorSelector(".JOYJnb")
                    count = canhbaos.count()

                    if count:
                        hetcanhbao = True
                        for i in range(count):
                            canhbao = canhbaos.nth(i)
                            outer = ext.getOuterHtml(canhbao)
                            # newclass = "Xc5Wg TCnBcf O70s4b"
                            # if not newclass in outer:
                            #     continue
                            tichxanhphienhientai = "IfU6xc D2Bhy"
                            if tichxanhphienhientai in outer:
                                continue
                            dadangxuat = "IfU6xc tAKG8"
                            if dadangxuat in outer:
                                continue
                            id = hstr.regex(outer, patter)
                            if id in self.eid:
                                continue
                            if ext.isdisplay(canhbao):
                                ext.click(canhbao)
                                hetcanhbao = False
                                break
                        if hetcanhbao:
                            if chi_dang_xuat_thiet_bi_cu:
                                return "ok"
                            if self.saveprofile:
                                return "ok"

                            def logout(p):
                                for frame in p.frames:
                                    frame = ExtendedPage(frame)
                                    logout = frame.locatorSelector(".T6SHIc a[href]")
                                    if not logout.isdisplay():
                                        logout = frame.locatorSelector(".Voigeb  a[href]")
                                    if logout.isdisplay():
                                        link = logout.get_attribute("href")
                                        if "Logout" in link:
                                            logout.click()
                            logout(p)
                            avatar = p.locatorSelector("a > .gbii")
                            if avatar.isdisplay():
                                avatar.click()
                                p.sleep(0.1)
                                logout(p)

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.logout"

    def danhGiaGoogleMap(self, user):
        try:
            # return
            p = self.p
            self.lastUrl = p.url
            self.searchDiemBatDauOk = False
            self.dangbai = False
            self.savediadiemmuonden = False

            # autoReload("f1", self)

            folder = "data/googlemap"
            hfile.createDir(folder)
            inimap = hini("data/googlemap/hconfig.ini")
            content = hfile.readLines(folder + "/content.txt")
            content = hrand.randomItemInList(content)
            contents = content.split("|")
            diachinha = contents[0: len(contents) - 1]
            filedata = contents[len(contents)-1].strip()
            comment = ""
            datas = hfile.readLines(folder + "/" + filedata)
            if datas:
                lastline = inimap.readint(filedata, 0)
                if lastline >= len(datas):
                    lastline = 0
                inimap.write(filedata, lastline + 1)
                comment = datas[lastline]
            diachicandanhgia = diachinha[0].strip()
            diachinha1 = ""
            try:
                diachinha1 = diachinha[1].strip()
            except:
                pass
            timestart = time.time()
            while time.time() - timestart < 60:
                try:
                    isthemdiemden = False
                    self.openUrl("https://www.google.com/maps/", self.lastUrl)
                    # continue
                    # p.goto("https://www.google.com/maps/")

                    # for i in range(2, len(diachinha)):
                    #     diemden = p.locatorSelector(".JuLCid input")
                    #     tatcadiemden = diemden.count()
                    #     if tatcadiemden <= i:
                    #         themdiemden = p.locatorSelector("button > .AUkJgf > div")
                    #         if themdiemden.isdisplay():
                    #             themdiemden.click()
                    #             p.sleep(1)
                    #     diemden = ExtendedLocator(diemden.nth(i))
                    #     if diemden.isdisplay():
                    #         isthemdiemden = True
                    #         diemden.type(diachinha[i].strip(), delay=0, press="Enter")
                    # self.searchDiemBatDauOk = False
                    search = p.locatorSelector("#searchboxinput")
                    if self.searchDiemBatDauOk:
                        close = p.locatorSelector('*[role="radiogroup"] + button')
                        if close.isdisplay():
                            close.click()
                        iconvietdanhgia = p.locatorImage('rate_review_gm_blue_18dp.png')
                        if not iconvietdanhgia.isdisplay() and search.isdisplay():
                            # search.type(diachicandanhgia, delay=0, press="Enter", sleep_enter=self.sleep_enter)
                            search.send(diachicandanhgia, press="Enter", fast_send=self.fast_send)
                        if user == "tientung" or user == "lochuy":
                            self.savediadiemmuonden = True
                        if not self.savediadiemmuonden:
                            save = p.locatorImage("bookmark_border_gm_blue_18dp.png")
                            if save.isdisplay():
                                save.click()
                                p.sleep(1)
                                diadiemmuonden = p.locatorSelector("*[role='menuitemradio'][data-index='1']")
                                if diadiemmuonden.isdisplay():
                                    diadiemmuonden.click()
                                    self.savediadiemmuonden = True
                        if self.savediadiemmuonden:
                            # continue
                            iconvietdanhgia = p.locatorImage('rate_review_gm_blue_18dp.png')
                            if iconvietdanhgia.isdisplay():
                                iconvietdanhgia.click()
                                p.sleep(3)
                            for frame in p.frames:
                                frame = ExtendedPage(frame)
                                url = frame.url
                                if not "https://www.google.com/maps/api/js/ReviewsService.LoadWriteWidget" in url:
                                    continue
                                try:
                                    if "reviews-widget/images/img_done_check" in frame.content():
                                        dones = frame.locatorSelector(".VfPpkd-vQzf8d")
                                        if dones.count() == 2:
                                            done = ExtendedLocator(dones.first)
                                            if done.isdisplay():
                                                done.click()
                                                frame.sleep(10)
                                                return "ok.googlemap"
                                                break
                                except:
                                    pass
                                rate5 = frame.locatorSelector('div[data-rating="5"][role="radio"]')
                                count = rate5.count()
                                if count > 0:
                                    rate5 = ExtendedLocator(rate5.first)
                                if rate5.isdisplay():
                                    for zcheck in range(10):
                                        checked = rate5.get_attribute("aria-checked")
                                        if checked != "true":
                                            thongbao = frame.locatorSelector('*[data-tooltip-is-rich="true"]')
                                            if thongbao.isdisplay():
                                                thongbao.click()
                                                p.sleep(0.5)
                                            rate5.click()
                                            p.sleep(0.5)
                                        else:
                                            break
                                    binhluan = frame.locatorSelector('textarea[rows]')
                                    if binhluan.isdisplay():
                                        frame.sleep(1)
                                        binhluan.send(comment, fast_send=self.fast_send)
                                        # binhluan.type(comment)

                                    dangbai = frame.locatorSelector(".VfPpkd-LgbsSe-OWXEXe-k8QpJ")
                                    if dangbai.isdisplay():
                                        dangbai.click()
                                        frame.sleep(10)
                                        self.dangbai = True
                                        return "ok.googlemap"

                    if user == "tientung" or user == "lochuy":
                        self.searchDiemBatDauOk = True
                    if not self.searchDiemBatDauOk:
                        search1 = p.locatorSelector("#directions-searchbox-0 input")
                        if search1.isdisplay():
                            search1.send(diachinha1, press="Enter", fast_send=self.fast_send)
                            # search1.type(diachinha1, delay=0, press="Enter", sleep_enter=self.sleep_enter)
                            text = search1.get_attribute("aria-label").replace(",", "").replace(" ", "")
                            diachinha1sosanh = diachinha1.replace(",", "").replace(" ", "")
                            if diachinha1sosanh in text:
                                self.searchDiemBatDauOk = True

                        chiduong = p.locatorImage('directions_white_18dp.png')
                        if ext.isdisplay(chiduong):
                            chiduong.click()
                        else:

                            if search.isdisplay():
                                search.send(diachicandanhgia,  press="Enter", fast_send=self.fast_send)
                                # search.type(diachicandanhgia, delay=0, press="Enter", sleep_enter=self.sleep_enter)
                                pass

                except Exception as e:
                    print(e)
                time.sleep(1)
        except:
            hfile.getError(addtext="googlemap")
        return "timeout.googlemap"

    def confirm_security(self):
        p = self.p
        self.lastUrl = p.url
        self.eid = {}
        # autoReload("f1", self)

        timestart = time.time()
        while time.time() - timestart < 180:
            try:
                if "We're sorry..." in p.content():
                    p.reload()
                self.openUrl("https://myaccount.google.com/notifications?hl=en", self.lastUrl)
                if p.url.startswith("https://myaccount.google.com/notifications/eid"):
                    id = hstr.regex(p.url, "/eid/.*?(\\d+)")
                    if id:
                        co = p.locatorSelector(".O5jO3c")
                        if co.isdisplay():
                            co.click()
                            self.eid[id] = True

                        xemtatca = p.locatorSelector('*[jsname="fYy7S"]')
                        if xemtatca.isdisplay():
                            xemtatca.click()
                            self.eid[id] = True

                        dahieu = p.locatorSelector('*[data-id="EBS5u"]')
                        if dahieu.isdisplay():
                            dahieu.click()
                            self.eid[id] = True
                        if not id in self.eid:
                            self.eid[id] = False
                        if not self.eid[id]:
                            p.goto("https://myaccount.google.com/notifications?hl=en")

                else:
                    # continue
                    canhbaos = p.locatorSelector(".PfHrIe")
                    count = canhbaos.count()
                    if "https://www.gstatic.com/identity/accountsettingssecuritycommon/success_illustration_light_mode.svg" in p.content():
                        return "no.confirm"
                    if count:
                        hetcanhbao = True
                        for i in range(count):
                            canhbao = canhbaos.nth(i)
                            outer = ext.getOuterHtml(canhbao)
                            # newclass = "Xc5Wg TCnBcf"
                            # if not newclass in outer:
                            #     continue
                            if "Backup code was used to sign in" in outer:
                                continue
                            newclass = "Xc5Wg p1GmWb"
                            if newclass in outer:
                                continue
                            id = hstr.regex(outer, "/eid/.*?(\\d+)")
                            id_link = hstr.regex(outer, "/eid/(.*?\\d+)")
                            if id in self.eid:
                                continue
                            if ext.isdisplay(canhbao):
                                p.goto(f"https://myaccount.google.com/notifications/eid/{id_link}?hl=en")
                                # ext.click(canhbao)
                                # p.sleep(1)
                                hetcanhbao = False
                                break
                        if hetcanhbao:
                            return "ok.confirm"

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.confirm"

    def checkPhoneRecovery(self):
        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)
        self.checkphonerecoveryok = False
        timestart = time.time()
        while time.time() - timestart < 30:
            try:
                self.openUrl("https://myaccount.google.com/signinoptions/rescuephone", self.lastUrl)
                if p.locatorSelector(".RveJvd.snByac").count() == 1:
                    return "no.phone.recovery"
                phone = p.locatorSelector(".L5snid")
                if phone.isdisplay():
                    text_phone = phone.text()
                    if len(text_phone) > 3:
                        self.checkphonerecoveryok = True
                        return text_phone

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.checkphone"

    def deletePhoneRecovery(self):
        p = self.p

        def phonerecovery():
            if "https://myaccount.google.com/signinoptions/rescuephone" not in p.url:
                p.goto("https://myaccount.google.com/signinoptions/rescuephone")
            timestart = time.time()
            for i in range(30):
                try:
                    if "/challenge/ootp" in p.url:
                        self.logout_device(chi_dang_xuat_thiet_bi_cu=True)
                        p.goto("https://myaccount.google.com/signinoptions/rescuephone")
                    if "The setting you are looking for is not available for your account." in p.content():
                        return "ok"
                    if "https://myaccount.google.com/signinoptions/rescuephone" in p.url:
                        deletes = p.locatorSelector(".RveJvd.snByac")
                        count = deletes.count()
                        if count == 4 or count == 5:
                            delete = deletes.nth(count-1)
                            if ext.isdisplay(delete):
                                ext.click(delete)
                        else:
                            delete = p.locatorJsname("uXqWSe")
                            if delete.isdisplay():
                                delete.click()
                        if count == 1:
                            return "ok"
                except Exception as e:
                    print(e)
                p.sleep(1)
            return "Timeout"

        def phone():
            if "https://myaccount.google.com/phone" not in p.url:
                p.goto("https://myaccount.google.com/phone?rapt=" + self.rapt)
            timestart = time.time()
            while time.time() - timestart < 30:
                try:
                    if "The setting you are looking for is not available for your account." in p.content():
                        return "ok"
                    if "https://myaccount.google.com/phone" in p.url:
                        phone = p.locatorSelector(".ujJYOe")
                        if phone.count() > 0:
                            phone = ExtendedLocator(phone.first)
                        if phone.isdisplay():
                            phone.click()
                        deletes = p.locatorSelector(".RveJvd.snByac")
                        count = deletes.count()
                        if count == 4:
                            delete = deletes.nth(3)
                            if ext.isdisplay(delete):
                                ext.click(delete)
                        else:
                            if "data-display-number=" in p.content():
                                deletes = p.locatorSelector(".qsqhnc")
                                count = deletes.count()
                                if count:
                                    delete = deletes.nth(count-1)
                                    if ext.isdisplay(delete):
                                        ext.click(delete)
                        img = p.locatorSelector(".SVmOQb > img")
                        if img.isdisplay():
                            src = img.get_attribute("src")
                            if "/accountsettingsphone/phone_no_phone" in src:
                                return "ok"
                except Exception as e:
                    print(e)
                p.sleep(1)
            return "Timeout"
        status = phonerecovery()
        if status != "ok":
            return "phonerecovery " + status
        return phone()

    def check_review_google_map(self):

        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)

        timestart = time.time()
        while time.time() - timestart < 60:
            try:
                self.openUrl("https://www.google.com/maps/contrib/", self.lastUrl)
                donggops = p.locatorSelector(
                    '*[jsaction="pane.profile-stats.showStats; keydown:pane.profile-stats.showStats"]')
                if donggops.count() == 3:
                    donggop = ExtendedLocator(donggops.nth(2))
                    if donggop.isdisplay():
                        return donggop.text()
                if donggops.count() == 4:
                    donggop = ExtendedLocator(donggops.nth(3))
                    if donggop.isdisplay():
                        return donggop.text()

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.review_google_map"

    def deletePaymentMethod(self):

        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)

        timestart = time.time()
        while time.time() - timestart < 60:
            try:
                self.openUrl("https://pay.google.com/gp/w/home/paymentmethods?hl=en", self.lastUrl)
                if p.url.startswith("https://support.google.com/googlepay/"):
                    return "delete.payment"
                if p.url == "https://pay.google.com/gp/w/home/signup":
                    return "no.payment"

                for frame in p.frames:

                    frame = ExtendedPage(frame)
                    addpayment = frame.locatorSelector(".b3-add-instrument-card-header")
                    if addpayment.isdisplay():
                        return "delete.payment"
                    if "No payment methods yet?" in frame.content():
                        return "delete.payment"
                    removes = frame.locatorSelector(".b3id-info-message-html.b3-info-message-html")
                    count = removes.count()
                    for i in range(count):
                        remove = removes.nth(i)
                        if ext.isdisplay(remove):
                            if ext.getText(remove) == "Remove":
                                ext.click(remove)
                                break
                    if frame.locatorName("cardnumber").isdisplay():
                        return "fail.payment"
                    removes = frame.locatorSelector(".b3-primary-button")
                    count = removes.count()
                    for i in range(count):
                        remove = removes.nth(i)
                        if ext.isdisplay(remove):
                            text = ext.getText(remove)
                            if text == "Remove":
                                ext.click(remove)
                                break

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.payment"

    def bat2fa(self):
        p = self.p
        self.bat2fa_ok = False
        self.get_code_ok = False
        self.lastUrl = p.url
        p: ExtendedPage = self.p
        self.otp: hotp = self.otp
        timestart = time.time()
        iclickGenerate = 0
        while time.time() - timestart < 240:
            try:
                p.sleep(1)
                url = p.url
                if "We're sorry..." in p.content():
                    p.reload()
                # continue
                if not "/two-step-verification/" in url and self.bat2fa_ok and not "https://myaccount.google.com/apppasswords" in url:
                    p.goto(f"https://myaccount.google.com/two-step-verification/backup-codes?hl=en&rapt={self.rapt}")
                    p.sleep(1)
                    continue

                if self.get_code_ok and not "https://myaccount.google.com/apppasswords" in url:
                    p.goto(
                        f"https://myaccount.google.com/apppasswords?hl=en&authuser=0&utm_source=google-account&utm_medium=myaccountsecurity&utm_campaign=tsv-settings&rapt={self.rapt}")
                    p.sleep(1)
                    continue
                self.openUrl(
                    "https://myaccount.google.com/signinoptions/two-step-verification/enroll?hl=en&flow=phone&rapt=" + self.rapt, self.lastUrl)
                if url.startswith("https://myaccount.google.com/apppasswords"):
                    password_app = p.locatorSelector('.CP2bwb')
                    if password_app.isdisplay():
                        password_app_text = password_app.text()
                        if len(password_app_text) == 16:
                            self.data["password_app"] = password_app_text
                            self.updateMail()
                            return "ok"
                    enter_name = p.locatorSelector('*[aria-label="Enter custom name"]')
                    if enter_name.isdisplay():
                        enter_name.send(hrand.randomStrMd5(8), fast_send=self.fast_send)
                        # enter_name.type(hrand.randomStrMd5(8))
                        p.sleep(0.5)
                    if iclickGenerate:
                        if time.time() - iclickGenerate > 5:
                            p.reload()
                            iclickGenerate = 0
                    Generate = p.locatorText('Generate')
                    if Generate.isenable():
                        Generate.click()
                        if not iclickGenerate:
                            iclickGenerate = time.time()
                        p.sleep(0.5)
                    selects = p.locatorSelector('*[role="option"]')
                    count = selects.count()
                    for i in range(count):
                        select = ExtendedLocator(selects.nth(i))
                        if select.isdisplay():
                            text = select.text()
                            if "(Custom name)" in text:
                                select.click()
                                break
                    select_app = p.locatorSelector('*[aria-label="Select app"]')
                    if select_app.isdisplay():
                        select_app.click()
                if url.startswith("https://myaccount.google.com/two-step-verification/backup-codes"):
                    Get_backup_codes = p.locatorText("Get backup codes")
                    if Get_backup_codes.isdisplay():
                        Get_backup_codes.click()
                    codes = p.locatorSelector(".ibJClf")
                    codes_count = codes.count()
                    if codes_count > 0 and codes_count < 10:
                        get_new_code = p.locatorSelector('*[aria-label="Generate new codes"]')
                        if get_new_code.isdisplay():
                            get_new_code.click()
                    elif codes_count == 10:
                        code_all = []
                        for i in range(codes_count):
                            code_now = ExtendedLocator(codes.nth(i)).text()
                            code_all.append(code_now.replace(" ", ""))
                        code_all = hstr.listToString(code_all, ",")
                        self.data["get2facode"] = code_all
                        self.updateMail()
                        self.get_code_ok = True
                if url.startswith("https://myaccount.google.com/signinoptions/two-step-verification/enroll"):
                    tel = p.locatorSelector('*[type="tel"]')
                    if tel.isdisplay():
                        self.otp.start()
                        tel.send(self.otp.phone, fast_send=self.fast_send)
                        # tel.type(self.otp.phone)
                        p.sleep(1)
                        next = p.locatorText("Next")
                        if next.isdisplay():
                            next.click()
                    enter_code = p.locatorSelector('*[maxlength="8"]')
                    if enter_code.isdisplay():
                        code = self.otp.getCode()
                        if not code:
                            Resend = p.locatorText('Resend')
                            if Resend.isdisplay():
                                Resend.click()
                                continue
                        enter_code.send(code, press="Enter", fast_send=self.fast_send)
                        # enter_code.type(code, press="Enter")
                    Turn_on = p.locatorText('Turn on')
                    if Turn_on.isdisplay():
                        Turn_on.click()
                        self.bat2fa_ok = True
            except Exception as e:
                print(e)

        return "timeout.bat2fa"

    def disable_2fa(self):
        p = self.p
        p.goto("https://myaccount.google.com/signinoptions/two-step-verification?pli=1&hl=en&rapt=" + self.rapt)
        timestart = time.time()
        while time.time() - timestart < 90:
            try:
                url = p.url
                if "/enroll" in url:
                    return "ok_disable_2fa"
                if "https://myaccount.google.com/security" in url:
                    return "ok_disable_2fa"
                turn_off = p.find_selectors(".RveJvd.snByac", "Turn off")
                if turn_off:
                    turn_off = ExtendedLocator(turn_off[len(turn_off) - 1])
                    if turn_off.isdisplay():
                        turn_off.click()
                        p.sleep(2)

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout_disable_2fa"

    def changeCountry(self):

        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)
        timestart = time.time()
        clickgui = False
        while time.time() - timestart < 30:
            try:
                self.openUrl("https://policies.google.com/country-association-form", self.lastUrl)
                if clickgui:
                    if "https://www.gstatic.com/identity/boq/policies/countryassociationform/green-globe-light.svg" in p.content():
                        return "ok.changecountry"
                showlistcountry = p.locatorSelector(".VfPpkd-t08AT-Bz112c")
                if showlistcountry.isdisplay():
                    showlistcountry.click()
                us = p.locatorSelector("*[data-value='us']")
                if us.isdisplay():
                    us.click()
                lydo = p.locatorSelector('*[type="checkbox"]')
                count = lydo.count()
                if count > 3:
                    lydo = ExtendedLocator(lydo.nth(hrand.randomInt(0, count-2)))
                    if not lydo.is_checked():
                        lydo.click()
                        gui = p.locatorSelector(".VfPpkd-vQzf8d")
                        if gui.isdisplay():
                            gui.click()
                            clickgui = True
                            p.sleep(3)

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.changecountry"

    def create_brand_account_youtube(self, createbrandaccountyoutube_number):
        if createbrandaccountyoutube_number <= 0:
            return "Hãy điền số kênh muốn tạo"
        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)
        from hinfo import hinfo
        _info = hinfo()
        # p.sleep(1)
        # autoReload("f1", self)

        clickgui = False
        otp: hotp = self.otpyoutube
        # createbrandaccountyoutube_number = 0
        for i in range(createbrandaccountyoutube_number):
            timestart = time.time()
            create_ok = False
            while time.time() - timestart < 90:
                try:
                    self.openUrl("https://www.youtube.com/create_channel?action_create_new_channel_redirect=true", self.lastUrl)
                    url = p.get_url()
                    if "PlusPageSignUp" in url:
                        PlusPageName = p.locatorSelector("#PlusPageName")
                        if PlusPageName.isdisplay():
                            if _info.listFirstUs:
                                info = _info.get()
                                PlusPageName.send(info.get("first") + " " + info.get("last"), fast_send=self.fast_send)
                                # PlusPageName.type(info.get("first") + " " + info.get("last"))
                        ConsentCheckbox = p.locatorSelector("#ConsentCheckbox")
                        if ConsentCheckbox.isdisplay():
                            if not ConsentCheckbox.is_checked():
                                ConsentCheckbox.click()
                            if ConsentCheckbox.is_checked():
                                submitbutton = p.locatorSelector("#submitbutton")
                                if submitbutton.isdisplay():
                                    submitbutton.click()
                                    p.sleep(4)
                    if "/PlusPageSignUpIdvChallenge" in url:
                        verifyphoneinput = p.locatorSelector("#verify-phone-input")
                        if verifyphoneinput.isdisplay():
                            code = otp.getCode()
                            if not code:
                                return "Không thể lấy code otp"
                            verifyphoneinput.send(code, press="Enter", fast_send=self.fast_send)
                            # verifyphoneinput.type(code, press="Enter")
                        signupidvinput = p.locatorSelector("#signupidvinput")
                        if signupidvinput.isdisplay():
                            errormsg = p.locatorSelector(".errormsg")
                            if errormsg.isdisplay():
                                errormsg_text = errormsg.text()
                                if errormsg_text:
                                    otp.restart()
                            otp.start()
                            if not otp.phone:
                                return "Không thể lấy phone otp"
                            signupidvinput.send(otp.phone, press="Enter", fast_send=self.fast_send)
                            # signupidvinput.type(otp.phone, press="Enter")
                            p.sleep(4)

                    if "/channel/" in url:
                        create_ok = True
                        if createbrandaccountyoutube_number != 1:
                            p.goto("https://www.youtube.com/create_channel?action_create_new_channel_redirect=true")
                        break
                except Exception as e:
                    print(e)
                p.sleep(1)
            if not create_ok:
                return "timeout_create_brand_account_youtube"
        return "ok_create_brand_account_youtube"

    def closePaymentMethod(self):

        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)

        timestart = time.time()
        while time.time() - timestart < 90:
            try:
                self.openUrl("https://pay.google.com/gp/w/home/settings", self.lastUrl)
                if p.url.startswith("https://support.google.com/googlepay/"):
                    return "close.payment"
                if p.url == "https://pay.google.com/gp/w/home/signup":
                    return "no.payment"
                pages = p.get_pages()
                if len(pages) == 2:
                    for page in pages:
                        url = page.url
                        if "/challenge/pwd" in url:
                            page = ExtendedPage(page)
                            Passwd = page.locatorName('Passwd')
                            if not Passwd.isdisplay():
                                Passwd = page.locatorName("password")
                            if Passwd.isdisplay():
                                p.sleep(0.5)
                                Passwd.send(self.data["password"], press="Enter", fast_send=self.fast_send)
                                # Passwd.type(self.data["password"], delay=self.delay, press="Enter", timeout=20, sleep_enter=self.sleep_enter)
                                timestart2 = time.time()
                                while time.time() - timestart2 < 10:
                                    if Passwd.waitHidden(1):
                                        break
                                    if page.url != url:
                                        break
                                    p.sleep(1)
                else:
                    closepayment = p.locatorSelector("div > div > a[jslog='106976; track:click']")
                    if closepayment.isdisplay():
                        closepayment.click()
                        pass

                for frame in p.frames:
                    url = frame.url

                    if not url.startswith("https://payments.google.com/payments/u/0/wipeout") and not url.startswith("https://payments.google.com/payments/u/0/embedded_settings"):
                        continue
                    # continue

                    frame = ExtendedPage(frame)

                    content = frame.locatorSelector(
                        '*[data-id="confirmationForm-1.closureReasonSelectorSelectCaption"] > .goog-menuitem-content').text()

                    if not content:

                        whyclose = frame.locatorSelector('div[data-name="closureReasonSelector"] > label > div > div')
                        if whyclose.isdisplay():

                            whyclose.click()
                        close = frame.locatorSelector('*[data-value="WIPEOUT_REASON_DONT_KNOW_ABOUT_ACCOUNT"]')
                        if close.isdisplay():

                            close.click()
                    else:

                        continues = frame.locatorSelector(
                            '.b3-simple-form-field-button-container > div[data-button-type="4"]')
                        if continues.isdisplay():

                            continues.click()
                        closepay = frame.locatorSelector('.b3-primary-button')
                        if closepay.isdisplay():

                            closepay.click()

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.payment"

    def checkPaymentMethod(self):

        p = self.p
        # p.goto("https://pay.google.com/gp/w/home/paymentmethods")
        self.lastUrl = p.url
        # autoReload("f1", self)

        timestart = time.time()
        while time.time() - timestart < 30:
            try:
                self.openUrl("https://pay.google.com/gp/w/home/paymentmethods", self.lastUrl)

                if p.url.startswith("https://pay.google.com/gp/w/home/signup"):
                    return "no.payment"
                # self.openUrl("https://pay.google.com/gp/w/home/signup", self.lastUrl)
                for frame in p.frames:
                    url = frame.url
                    if not url.startswith("https://payments.google.com/payments/u/0/payment_methods"):
                        continue
                    buttons = frame.locator(".b3-instrument-details-default-actions > div > a")
                    count = buttons.count()
                    dathempttt = False
                    # ptttbidong = False
                    for i in range(count):
                        button = buttons.nth(i)
                        data_widget_reference_token = ext.get_attribute(button, "data-widget-reference-token")
                        if data_widget_reference_token.startswith("[5,"):
                            dathempttt = True
                            warning = frame.locator(".b3-instrument-details-alert-icon > .b3-icon-warning")
                            if ext.isdisplay(warning):
                                # ptttbidong = True
                                return "payment.closed"
                        # print(data_widget_reference_token)
                    if dathempttt:
                        return "have.payment"
                    # print(dathempttt, ptttbidong)
            except Exception as e:
                print(e)
            p.sleep(1)
        return "Timeout"

    def checkCHPlay(self):

        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)

        timestart = time.time()
        tongsotien = 0
        irefund = 0
        while time.time() - timestart < 30:
            try:
                self.openUrl("https://play.google.com/store/account/orderhistory?hl=en", self.lastUrl)
                items = p.locatorSelector(".U6fuTe")
                count = items.count()
                if not count and "You have no orders for this account." in p.content():
                    return "no.orders"
                for i in range(count):
                    item = ExtendedLocator(items.nth(i))
                    if item.isdisplay():
                        outer = ext.getOuterHtml(item)
                        sotien = hstr.regex(outer, '<div class="mshXob">(.*?)</div>').replace(",", ".")
                        sotien = hstr.regexNumber(sotien)
                        if sotien != "":
                            tongsotien = tongsotien + float(sotien)
                        if "Refunded" in item.text():
                            irefund = irefund + 1
                if count != 0:
                    if tongsotien == 0:
                        return "buy.app.free"
                    elif irefund == count:
                        return "buy.refunded"
                    else:
                        return "buy.no.refunded"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.chplay"

    def restoredisable2(self):
        p = self.p
        self.lastUrl = p.url

        timestart = time.time()

        while True:
            try:
                p.sleep(1)
                url = p.url
                self.openUrl("https://support.google.com/accounts/contact/suspended", self.lastUrl)
                if  "https://support.google.com/accounts/contact/suspended" in url:

                    with lock:
                        restoredisable2_mail_index = ini.readint("restoredisable2_mail_index", 0)
                        if restoredisable2_mail_index >= len(self.restoredisable2_mail):
                            return "hết mail"
                        mailrestore = self.restoredisable2_mail[restoredisable2_mail_index]
                        ini.write("restoredisable2_mail_index", restoredisable2_mail_index + 1)

                    # rq = hrequest()
                    # mailrestore = rq.getHtml(self.restoredisable2_mail)
                    if not "@" in mailrestore:
                        return "không thấy email cần restore"
                    ok = False
                    for i in range(300):
                        Username = p.locatorSelector('#Username')
                        if Username.isdisplay():
                            content = hrand.randomItemInList(self.restoredisablecontent)
                            mailrestore = mailrestore.split("|")[0]
                            Username.send(mailrestore, fast_send=self.fast_send)
                            # Username.type(mailrestore)
                            email_prefill_req = p.locatorSelector('#email_prefill_req')
                            email_prefill_req.send(self.email_lower, fast_send=self.fast_send)
                            # email_prefill_req.type(self.email_lower)
                            suspended_reason = p.locatorSelector('#suspended_reason')
                            suspended_reason.fill(content)
                            submit = p.locatorSelector('.submit-button')
                            submit.click()
                            p.sleep(1)

                            for z in range(20):
                                captcha = p.locatorSelector(".notification-area.invalid")
                                if captcha.isdisplay():
                                    p.sleep(0.5)
                                    break
                                if not submit.isdisplay():
                                    ok = True
                                    return "ok"
                                    p.sleep(0.5)

                                    break
                                p.sleep(1)
                            p.reload()
                            if ok:
                                break
                            p.sleep(1)

            except Exception as e:
                print(e)

        return "timeout"

    def checkHiddenPhone(self):

        p = self.p
        # cookie = p.getCookies("https://myaccount.google.com/", getStr = True)
        # p.goto("https://mail.google.com/")
        # cookie = p.context.cookies()
        # cookie2 = p.getCookies("https://google.com/", getStr = True)
        # cookie3 = p.getCookies("https://*.google.com/", getStr = True)
        # cookie5 = p.getCookies("https://*google.com/", getStr = True)
        # cookie6 = p.getCookies(None, getStr = True)
        # cookie7 = p.getCookies("*", getStr = True)
        # hfile.writeLine("ct.txt", cookie + "\r\n" + cookie2 + "\r\n" + cookie3 + "\r\n" + cookie5 + "\r\n" + cookie6 + "\r\n" + cookie7)
        self.lastUrl = p.url

        timestart = time.time()

        while time.time() - timestart < 30:
            try:

                self.openUrl("https://myaccount.google.com/signinoptions/password", self.lastUrl)
                if "/ipp" in p.url:
                    return "hidden.phone"
                elif "/ootp" in p.url:
                    return "ootp"
                else:
                    password = p.locatorSelector('*[type="password"]')
                    if password.count() >= 2:
                        return "no.hidden.phone"

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.checkhiddenphone"

    def change_display_name(self):

        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)
        firstname = ""
        lastname = ""
        if self.listdisplayname:
            lastdisplayname = ini.readint("lastdisplayname", 0)
            if lastdisplayname >= len(self.listdisplayname):
                lastdisplayname = 0
            ini.write("lastdisplayname", lastdisplayname + 1)
            # namenow =  hrand.randomItemInList(self.listdisplayname) + " "
            namenow = self.listdisplayname[lastdisplayname]
            namenows = namenow.split(" ", 1)
            firstname = namenows[0].strip()
            lastname = namenows[1].strip()
            if not firstname or not lastname:
                return "fail.config.changedisplayname"
        else:
            from hinfo import hinfo
            info = hinfo()
            firstname = hrand.randomItemInListFormatStr(info.listFirstUs).title()
            lastname = hrand.randomItemInListFormatStr(info.listLastUs).title()

        timestart = time.time()

        def logout(p):
            for frame in p.frames:
                frame = ExtendedPage(frame)
                logout = frame.locatorSelector(".T6SHIc a[href]")
                if not logout.isdisplay():
                    logout = frame.locatorSelector(".Voigeb  a[href]")
                if logout.isdisplay():
                    link = logout.get_attribute("href")
                    if "Logout" in link:
                        logout.click()
        solanlogout = 0
        reloadrescuephone = False
        # self.newrapt = ""
        while time.time() - timestart < 50:
            try:

                if "/signinchooser" in p.url:
                    if not reloadrescuephone:
                        p.goto("https://myaccount.google.com/signinoptions/rescuephone")
                        timestart = time.time()
                        reloadrescuephone = True
                        continue
                    solanlogout = solanlogout + 1
                    authuser = p.locatorSelector('*[data-authuser="-1"]')
                    if authuser.isdisplay():
                        authuser.click()
                if "/pwd" in p.url:
                    password = p.locatorName("password")
                    if password.isdisplay():
                        password.send(self.data["password"], press="Enter", fast_send=self.fast_send)
                        # password.type(self.data["password"], delay=self.delay, press="Enter", sleep_enter=self.sleep_enter)
                        password.waitHidden()
                if p.url.startswith("https://myaccount.google.com/signinoptions/rescuephone"):
                    self.rapt = ""
                    self.getrapt = True
                    self.getRapt()
                    if self.rapt:
                        p.goto("https://myaccount.google.com/profile/name/edit?rapt=" + self.rapt)
                if "https://myaccount.google.com/personal-info" in p.url:
                    logout(p)
                    avatar = p.locatorSelector("a > .gbii")
                    if avatar.isdisplay():
                        avatar.click()
                        p.sleep(0.1)
                        logout(p)
                self.openUrl("https://myaccount.google.com/profile/name/edit", self.lastUrl)
                if "/ipp" in p.url:
                    if not solanlogout:
                        p.goto("https://myaccount.google.com/personal-info")
                    else:
                        return "ipp.changedisplayname"

                if "https://myaccount.google.com/profile/name?" in p.url:
                    # return "ok.changedisplayname"
                    return firstname + " " + lastname
                inputs = p.locatorSelector("label > input")
                count = inputs.count()
                if count == 2:
                    first = ExtendedLocator(inputs.nth(0))
                    first.send(firstname, fast_send=self.fast_send)
                    # first.type(firstname)
                    last = ExtendedLocator(inputs.nth(1))
                    last.send(lastname, fast_send=self.fast_send)
                    # last.type(lastname)
                    save = p.locatorSelector(".VfPpkd-vQzf8d")
                    if save.count() >= 2:
                        save = ExtendedLocator(save.nth(save.count()-1))
                        if save.isdisplay():
                            save.click()
                            p.sleep(3)
                            continue
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.changedisplayname"

    def checkYoutubePremium(self):

        p = self.p
        self.lastUrl = p.url
        # autoReload("f1", self)

        timestart = time.time()
        loadurlok = 0
        while time.time() - timestart < 120:
            try:
                if "https://consent.youtube.com/" in p.url:
                    buttons = p.locatorSelector("form button .VfPpkd-vQzf8d")
                    count = buttons.count()
                    if count == 4 or count == 2:
                        accept = ExtendedLocator(buttons.nth(1))
                        if accept.isdisplay():
                            accept.click()
                if "https://www.youtube.com/oops" in p.url:
                    return "oops.premium"
                self.openUrl("https://www.youtube.com/premium", self.lastUrl)
                if "https://www.youtube.com/premium" in p.url:
                    if not loadurlok:
                        loadurlok = time.time()
                    if time.time() - loadurlok > 30:
                        p.goto("https://www.youtube.com/premium")
                        loadurlok = time.time()
                    viewall = p.locatorSelector('*[aria-label="View all plans"]')
                    if viewall.isdisplay():
                        return "no.premium.2"
                    manage_subscription_button = p.locatorSelector("#manage-subscription-button")
                    if manage_subscription_button.isdisplay():
                        outer = manage_subscription_button.getOuterHtml()
                        if "/paid_memberships" in outer:
                            return "yes.premium"
                        else:
                            return "no.premium"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.premium"

    def create_google_voice(self):
        #
        p = self.p
        self.lastUrl = p.url
        self.otp = self.otpVoice
        # if "realnumber.net1" in self.otp.website or "tellabot.com1" in self.otp.website:
        #     self.otp = self.otp
        #     if "tellabot.com1" in self.otp.website:
        #         self.otp.suDungLaiSo()
        # else:
        #     self.otp.restart()
        # self.otp.timeoutcode = 0
        # autoReload("f1", self)
        phoneresend = {}
        resend = False
        timestart = time.time()
        sleeplandau = False
        num_get_code_fail = 0
        self.otp.time_wait_phone = 99999*60
        timthayacceptButton = False
        while time.time() - timestart < 100000:
            try:
                if time.time() - timestart > 30:
                    if not timthayacceptButton:
                        p.goto("https://voice.google.com/u/0/signup?hl=en")
                        timestart = time.time()
                self.openUrl("https://voice.google.com/u/0/signup?hl=en", self.lastUrl)
                if p.url.startswith("https://voice.google.com/u/0/signup"):
                    Finishs = p.locatorSelector("button[mat-flat-button]")
                    count = Finishs.count()
                    print("Finishs", count)

                    for i in range(count):
                        Finish = ExtendedLocator(Finishs.nth(i))
                        if Finish.isdisplay():
                            text = Finish.text()
                            print("Finishs", text, "--")
                            if "Finish" in text or "Claim" in text or "Verify" in text:
                                Finish.click()
                                p.sleep(3)
                                continue
                    dialogs = p.locatorSelector('*[gv-test-id="dialog-title"]')
                    if not dialogs.count():
                        dialogs = p.locatorSelector(".gvAddLinkedNumber-genericError")
                    if dialogs.count():
                        for i in range(dialogs.count()):
                            dialog = ExtendedLocator(dialogs.nth(i))
                            if dialog.isdisplay():
                                if "Something went wrong" in dialog.text():
                                    return "something_went_wrong"
                                    # self.otp.restart()
                                    # p.reload()
                                    # p.sleep(1)
                                    # continue

                    entercodes = p.locatorSelector('*[name="verify-code"]')
                    count = entercodes.count()
                    if count == 6:
                        # code = "124567"
                        code = self.otp.getCode(0)
                        if code:
                            for i in range(count-1):
                                ExtendedLocator(entercodes.nth(i)).send(code[i], fast_send=self.fast_send)
                                # ExtendedLocator(entercodes.nth(i)).type(code[i])
                            ExtendedLocator(entercodes.nth(5)).send(code[5],  press="Enter", fast_send=self.fast_send)
                            # ExtendedLocator(entercodes.nth(5)).type(code[5], delay=self.delay, press="Enter", sleep_enter=self.sleep_enter)
                            p.sleep(1)
                            timestart = time.time()
                        else:
                            num_get_code_fail = num_get_code_fail + 1
                            if num_get_code_fail > 3:
                                return "3rd_time_no_code"
                            timestart = time.time()
                            self.otp.restart()
                            p.reload()
                            timthayacceptButton = False
                            continue
                            # if not self.otp.phone in phoneresend:
                            #     resend = p.locatorSelector(".mat-button-wrapper")
                            #     if resend:
                            #         self.otp.timeoutcode = 15 * 60
                            #         if "textverified" in self.otp.website:
                            #             self.otp.timeoutcode = 4
                            #         phoneresend[self.otp.phone] = True
                            #     continue
                            # if not resend:
                            #     resend = True
                            #     self.otp.restart()
                            #     p.reload()
                            #     continue
                            # else:
                            #     return "no.code.creategooglevoice"

                    # selects = p.locatorSelector(".gvSearchAccountPhone-resultButton .mat-button-wrapper")
                    selects = p.locatorSelector(".gvSearchAccountPhone-resultButton")
                    count = selects.count()
                    if count:
                        select = selects.nth(hrand.randomInt(0, count-1))
                        select = ExtendedLocator(select)
                        if select.isdisplay():
                            select.click()
                    else:
                        searchAccountPhoneSearchBar = p.locatorSelector("#searchAccountPhoneSearchBar")
                        if searchAccountPhoneSearchBar.isdisplay():
                            searchAccountPhoneSearchBar.send(hrand.randomInt(3000, 8888), fast_send=self.fast_send)
                            # searchAccountPhoneSearchBar.type(hrand.randomInt(3000, 8888), delay=self.delay)
                            p.sleep(3)
                    errorCode = p.locatorSelector(".bi7krf-bWk6q").text()
                    if "Code is incorrect. Try again" in errorCode:
                        return "code.fail.creategooglevoice"
                    inputphone = p.locatorSelector('input[gv-test-id="new-linked-phone-input"]')
                    if inputphone.isdisplay():
                        failText = p.locatorSelector("#pie1").text()
                        if failText:
                            self.otp.restart()
                        setStatus(self.data["id"], "wait phone google voice")
                        self.otp.start()
                        # phone = "(484) 716 1714"
                        phone = self.otp.phone
                        # print("phone", phone, self.otp.website)
                        if not phone:
                            timestart = time.time()
                            self.otp.restart()
                            p.reload()
                            timthayacceptButton = False
                            continue
                        if phone:
                            setStatus(self.data["id"], f"send phone google voice {phone}")
                            inputphone.send(phone, press="Enter", fast_send=self.fast_send)
                            # inputphone.type(phone, delay=self.delay, press="Enter", textreplace=[" ", ")", "(", "-"], sleep_enter=self.sleep_enter)
                            timestart = time.time()


                    # else:
                    #     verify = p.locatorSelector("gv-verify-phone gv-flat-button .mat-button-wrapper")
                    #     if verify.isdisplay():
                    #         verify.click()

                    continues = p.locatorSelector(".gvTos-acceptButton")
                    if continues.isdisplay():
                        if not sleeplandau:
                            timthayacceptButton = True
                            print("sleep 15s")
                            p.sleep(hrand.random_min_max(10, 15))
                        continues.click()
                        p.sleep(2)

                if "/calls" in p.url:
                    phone = p.locatorSelector(".phone-number-details").text()
                    if phone != "":
                        return phone
                    registers = p.locatorSelector(".mat-button-wrapper")
                    for z in range(registers.count()):
                        register = registers.nth(z)
                        register = ExtendedLocator(register).text()
                        if "Register now" in register:
                            return "lose.creategooglevoice"
                if "https://support.google.com/accounts/answer/" in p.url:
                    return "unable.voice"
                if "/about" in p.url:
                    signUpLink = p.locatorSelector(".signUpLink")
                    if signUpLink.isdisplay():
                        signUpLink.click()
                if "/blocked" in p.url:
                    return "blocked.voice"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.creategooglevoice"

    def checkGoogleVoice(self):
        # autoReload("f1", self)
        p = self.p
        self.lastUrl = p.url

        timestart = time.time()
        while time.time() - timestart < 30:
            try:
                self.openUrl("https://voice.google.com/u/0/calls?hl=en", self.lastUrl)
                # openUrl("https://voice.google.com/calls")
                if "/calls" in p.url:
                    phone = p.locatorSelector(".phone-number-details > span").first
                    if ext.isdisplay(phone):
                        text = ext.getText(phone)
                        text = text.replace(" ", "").strip()
                        if text:
                            return text
                    if "Register now" in p.content():
                        return "outphone.voice"
                if "https://support.google.com/accounts/answer/" in p.url:
                    return "unable.voice"
                if "/about" in p.url:
                    signUpLink = p.locatorSelector(".signUpLink")
                    if signUpLink.isdisplay():
                        signUpLink.click()
                if "/blocked" in p.url:
                    return "blocked.voice"
                if "/signup" in p.url:
                    return "no.voice"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "Timeout"

    def openUrl(self, newurl, lastUrl):
        nowurl = self.p.url
        if nowurl == lastUrl or nowurl == "chrome-error://chromewebdata/" or nowurl == "chrome://new-tab-page/":
            self.p.goto(newurl)
            self.iloadfail = self.iloadfail + 1
        else:
            self.iloadfail = 0

    def check_date_create(self):

        p = self.p
        lastUrl = p.url

        timestart = time.time()
        cuoipage = False
        turn_off_in_product_features_clicked = False
        i_no_ok = 0
        while time.time() - timestart < 90:
            try:
                self.openUrl("https://mail.google.com/", lastUrl)
                if not cuoipage:
                    i_no_ok = i_no_ok+1
                    if i_no_ok % 10 == 0:
                        p.goto("https://mail.google.com/")
                    tabchinh = p.locatorSelector('tr[role="tablist"] > *[role="heading"] > div')
                    if tabchinh.count() == 3:
                        ext.click(tabchinh.nth(0))
                        p.sleep(1)

                if cuoipage:
                    close = p.locatorSelector('*[role="dialog"] > div > div > button:nth-child(3)')
                    if close.isdisplay():
                        close.click()
                        p.sleep(0.5)
                    if "#inbox" in p.url or "#section_query":
                        if p.locatorSelector("div[data-legacy-message-id]").count():
                            checkmes = p.locatorSelector(".g2")
                            if checkmes.count():
                                checkme = ExtendedLocator(checkmes.nth(0))
                                if checkme.isdisplay():
                                    email = checkme.get_attribute("email")
                                    dates = p.locatorSelector(".g3")
                                    if dates.count():
                                        date = ExtendedLocator(dates.nth(0)).get_attribute("title")
                                        date = hstr.regex(date, "(\\d{4})")
                                        if date:
                                            email_input = self.data["email"].split("@")[0] + "@gmail.com"
                                            if email_input.lower().replace(".", "") in email.lower().replace(".", ""):
                                                return date
                                            else:
                                                return "fake.date." + email + "." + self.data["email"]
                            # else:
                            #     while 1:
                            #         print("zzzzzzzzzzzzz")
                            #         time.sleep(1)
                            #     return "cannot.check"
                    bogs = p.locatorSelector("tr > td > * span[email]")
                    count = bogs.count()
                    if count:
                        bog = ExtendedLocator(bogs.nth(count-1))
                        if bog.isdisplay():
                            bog.click()
                            p.sleep(1)
                            x, y = bog.get_location(False)
                            if x:
                                p.mouse_click(x + 100, y)

                closefeatures = p.locatorSelector('*[role="dialog"] > div > div > div[style=""] > * > * > input + span')
                count = closefeatures.count()
                if count == 2:
                    close = closefeatures.nth(1)
                    ext.click(close)
                    ext.press(close)
                    p.sleep(0.5)
                turn_off_in_product_features = p.locatorName("turn_off_in_product")
                if turn_off_in_product_features.isdisplay():
                    turn_off_in_product_features.click()
                    turn_off_in_product_features_clicked = True
                    p.sleep(0.5)
                if turn_off_in_product_features_clicked:
                    reload_features = p.locatorName("r")
                    if reload_features.isdisplay():
                        reload_features.click()
                        timestart = time.time()
                        p.sleep(0.5)
                frame = p.locatorFrame('*[name="callout"]')
                closeSecureLogin = frame.locator('*[role="dialog"] > * button[data-dismiss="x"]')
                if ext.isdisplay(closeSecureLogin):
                    ext.click(closeSecureLogin)
                    p.sleep(0.5)
                close = p.locatorSelector('*[role="alertdialog"] > div[role="button"]')
                if close.isdisplay():
                    close.click()
                    p.sleep(0.5)

                newold = p.locatorSelector('.Di > div > span > span > .ts')
                count = newold.count()
                for i in range(count):
                    new = newold.nth(i)
                    if ext.isdisplay(new):
                        ext.click(new)
                        break
                old = p.locatorSelector(".Di + div > div > div")
                count = old.count()
                if count:
                    old = old.nth(count - 1)
                    if ext.isdisplay(old):
                        if not old.is_disabled():
                            ext.click(old)
                        else:
                            cuoipage = True
            except Exception as e:
                print(e)
            p.sleep(1)
        return "Timeout"

    def youtubeVerify(self):
        p = self.p
        self.lastUrl = p.url
        self.clickvn = False
        listvn = ["Viêt Nam", "Việt Nam", "Vietnam", "Vietname", "Вьетнам", "فيتنام"]
        otp = self.otpyoutube
        for z in range(30):
            try:
                while 1:
                    p.sleep(1)
                success = p.locatorSelector("#already-completed > ytv-already-completed-renderer")
                if success.isdisplay():
                    return "ok.youtubeverify"
                success = p.locatorSelector("#success > ytv-code-input-success-renderer")
                if success.isdisplay():
                    return "ok.youtubeverify"
                if not self.clickvn:
                    self.openUrl("https://www.youtube.com/verify_phone_number", self.lastUrl)
                    country = p.locatorSelector("#input-2 > input")
                    if country.isdisplay():
                        country.click()
                        p.sleep(1)
                        for i in listvn:
                            vn = p.locatorText(i)
                            if vn.isdisplay():
                                vn.click()
                                self.clickvn = True
                                break
                else:
                    txtphone = p.locatorSelector("#input-1 > input")
                    if txtphone.isdisplay():
                        otp.start()
                        phone = otp.phone
                        if not phone:
                            return "cannot.getphone.youtubeverify"
                        txtphone.send(phone, fast_send=self.fast_send)
                        # txtphone.type(phone, delay=self.delay)
                    btngetcode = p.locatorSelector("a > #button")
                    if btngetcode.isenable():
                        btngetcode.click()
                        p.sleep(1)
                    maxcheck = 7
                    for i in range(3, maxcheck):
                        txtcode = p.locatorSelector(f"#input-{i} > input")
                        if txtcode.isdisplay():
                            code = otp.getCode()
                            if not code:
                                if i == maxcheck - 1:
                                    return "cannot.getcode.youtubeverify"
                                back = p.locatorSelector("#back-button a")
                                if back.isdisplay():
                                    back.click()
                                    otp.restart()
                                    break
                            txtcode.send(code, press="Enter", fast_send=self.fast_send)
                            # txtcode.type(code, delay=self.delay)
                            submit = p.locatorSelector("#submit-button a")
                            if submit.isenable():
                                submit.click()
                                p.sleep(1)
                            break

            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.youtubeverify"

    def createChannelYoutube(self):
        p = self.p
        self.lastUrl = p.url
        timestart = time.time()
        while time.time() - timestart < 60:
            try:
                url = p.url
                self.openUrl("https://www.youtube.com/create_channel", self.lastUrl)
                create = p.locatorSelector("#create-channel-button")
                if create.isdisplay():
                    create.click()
                    p.sleep(2)
                if url.startswith("https://families.youtube.com/"):
                    return "youtube.mail.families"
                if "https://support.google.com/accounts/answer/40039" in url:
                    return "disable.youtube"
                if url.startswith("https://www.youtube.com/channel/"):
                    return "ok.createyoutube"
            except Exception as e:
                print(e)
            p.sleep(1)
        return "timeout.createyoutube"

    def get_all_link_youtube(self):
        p = self.p
        url = p.url
        if not url.startswith("https://myaccount.google.com/brandaccounts") and not url.startswith("https://www.youtube.com/"):
            p.goto("https://myaccount.google.com/brandaccounts")
        listlink = []
        listlink.append("https://www.youtube.com/account_advanced")
        urldefault = "https://www.youtube.com/signin?action_handle_signin=true&authuser=0&pageid=1111111111&next=/account_advanced&feature=masthead_switcher&skip_identity_prompt=true"
        timestart = time.time()
        while time.time() - timestart < 20:
            try:
                html = p.content()
                reg = hstr.regexs(html, 'data-oid="(\\d+)"')
                if not reg:
                    reg = hstr.regexs(html, 'data-id="(\\d+)"')
                if reg:
                    for zreg in reg:
                        dataid = zreg[0]
                        listlink.append(urldefault.replace("1111111111", dataid))
                    return listlink
            except Exception as e:
                print(e)
            p.sleep(1)
        return listlink

    def checkInfoYoutube(self):
        try:
            fname = name()
            p = self.p

            def getInfoLink(link):
                try:
                    fname = name()
                    # p.goto(link)
                    lastUrl = p.url
                    self.openUrl(link, lastUrl)
                    for i in range(30):
                        url = p.url
                        log(f"Tab {self.ithread} {fname} {url}")
                        if url.startswith("https://families.youtube.com/"):
                            return "youtube.mail.families"
                        if "https://support.google.com/accounts/answer/40039" in url:
                            return "disable"
                        if url.startswith("https://www.youtube.com/oops"):
                            pass
                        if url.startswith("https://consent.youtube.com/m?continue="):
                            accepts = p.locatorSelector("form > div > div > button")
                            count = accepts.count()
                            if count == 4:
                                accept = accepts.nth(1)
                                if ext.isdisplay(accept):
                                    ext.click(accept)
                                    p.sleep(1)
                                    continue
                        if url.startswith("https://www.youtube.com/account_advanced"):
                            html = p.content()
                            channelId0 = hstr.regex(html, '"shortUrl":"(.{22})"')
                            channelId = hstr.regex(html, '"shortUrl":"(UC.{22})"')
                            if channelId:
                                return getAbout(channelId)
                            if channelId0:
                                return "no.channel"
                        if url.startswith("https://www.youtube.com/channel/"):
                            return getAbout(url)
                        p.sleep(1)
                except:
                    error = hfile.getError()
                    log(f"Tab {self.ithread} {fname} {error}")
                return "timeout.youtube"

            def getNamAndView(idkenh):
                urlkenh: str = "https://www.youtube.com/channel/" + idkenh + "/about"
                if not p.url.startswith(urlkenh):
                    p.goto(urlkenh)
                for i in range(10):
                    abouts = p.locatorSelector('.ytd-channel-about-metadata-renderer > span[dir="auto"]')
                    count = abouts.count()
                    if count:
                        break
                    p.sleep(1)
                if not count:
                    return "-1", "-1"
                nam = "-1"
                for i in range(count):
                    about = abouts.nth(i)
                    if about.is_visible(timeout=1000):
                        text = about.text_content(timeout=1000)
                        if "2" in text:
                            nam = hstr.regex(text, "(\\d{4})")
                            break
                view = "-1"
                if nam != "-1":
                    scopes = p.locatorSelector("#right-column > .style-scope")
                    for i in range(scopes.count()):
                        scope = scopes.nth(i)
                        outerHTML = ext.getOuterHtml(scope)
                        if "no-styles" in outerHTML:
                            view = ext.getText(scope)
                            if not view:
                                return nam, "0"
                return nam, view

            def getSoVideo(idkenh):
                urlkenh: str = "https://studio.youtube.com/channel/" + idkenh + "/videos/upload?approve_browser_access=1"
                if not p.url.startswith("https://studio.youtube.com/channel/"):
                    p.goto(urlkenh)
                sovideo = "-1"
                for i in range(10):
                    if p.locatorId("upload-button").isdisplay():
                        return 0
                    textpage = p.locatorSelector("#footer .page-description").text()
                    if textpage:
                        tongvideo = hstr.regex(textpage, "\\d+–\\d+ of (\\d+)")
                        if tongvideo:
                            return tongvideo
                        tongvideo = hstr.regex(textpage, "\\d+ – \\d+/(\\d+)")
                        if tongvideo:
                            return tongvideo
                        return textpage
                    p.sleep(1)
                return sovideo

            def getSub(idkenh):
                urlkenh: str = "https://studio.youtube.com/channel/" + idkenh + "/analytics/tab-overview/period-default"
                if not "/analytics/tab-overview/period-default" in p.url:
                    p.goto(urlkenh)
                sub = "-1"
                for i in range(10):
                    cards = p.locatorSelector(".metric-value.style-scope.yta-latest-activity-card")
                    count = cards.count()
                if count == 2:
                    card = cards.nth(0)
                    text = card.text_content()
                    if not text or text == "—":
                        return "0"
                    return text
                return sub

            def getAbout(channelId):
                try:
                    fname = name()
                    idkenh = hstr.regex(channelId, "/channel/([a-zA-Z0-9_-]+)")
                    if not idkenh:
                        idkenh = channelId

                    namtaokenh, view = getNamAndView(idkenh)
                    sovideo = getSoVideo(idkenh)
                    sub = getSub(idkenh)
                    return f"https://www.youtube.com/channel/{idkenh}|{view}|{sub}|{sovideo}|{namtaokenh}"
                except:
                    error = hfile.getError()
                    log(f"Tab {self.ithread} {fname} {error}")
                    return "Timeout"
            links = self.get_all_link_youtube()
            listinfo = []
            for link in links:
                info = getInfoLink(link)
                listinfo.append(info)
            result = hstr.listToString(listinfo, "&")
            return result
        except Exception as e:
            error = hfile.getError()
            log(f"Tab {self.ithread} {fname} {error}")
            return "Timeout"

    def getConfig(self):
        try:
            with Database() as db:
                mail = db.query(Config).filter(Config.id == 1).first()
                if not mail:
                    newconfig = Config(line_email_recovery_random=0)
                    db.add(newconfig)
                    db.commit()
                    mail = db.query(Config).filter(Config.id == 1).first()
                db.commit()
                msg = {field.name: getattr(mail, field.name) for field in Config.__table__.columns}
                return Result(data=msg).to_dict()
        except Exception as e:
            print(e)
            db.rollback()
            return Result(False, "get config failed", e.args).to_dict()

    def updateConfig(self, data):
        try:
            update = data
            with Database() as db:
                update_dict = {k: v for k, v in update.items() if v}
                db.query(Config).filter(Config.id == update.get("id")).update(update_dict)
                db.commit()
                return Result()
        except Exception as e:
            db.rollback()
            error = hfile.getError()
            log(f"update_mail fail {error}")
            return Result(False, "update_mail fail", e.args)

    def updateMail(self):
        try:
            id = self.id
            if id == -1:
                return Result(msg="-1")
            update = self.data
            with Database() as db:
                old_mail = db.query(mailTable).filter(mailTable.id == id).first()
                if not old_mail:
                    return Result(False, "id not found")
                if update["email"] and update["email"] != old_mail.email:
                    old_emails = old_mail.email.split('\n')
                    if old_mail.email and not old_mail.email in old_emails:
                        old_emails.insert(0, old_mail.email)
                        if "" in old_emails:
                            old_emails.remove("")
                        update["oldpassword"] = '\n'.join(old_emails)
                if update["password"] and update["password"] != old_mail.password:
                    if old_mail.oldpassword == None:
                        old_mail.oldpassword = ""
                    old_passwords = old_mail.oldpassword.split('\n')
                    if old_mail.password and not old_mail.password in old_passwords:
                        old_passwords.insert(0, old_mail.password)
                        if "" in old_passwords:
                            old_passwords.remove("")
                        update["oldpassword"] = '\n'.join(old_passwords)
                if update["emailrecovery"] and update["emailrecovery"] != old_mail.emailrecovery:
                    if old_mail.oldemailrecovery == None:
                        old_mail.oldemailrecovery = ""
                    old_emailrecoverys = old_mail.oldemailrecovery.split('\n')
                    if old_mail.emailrecovery and not old_mail.emailrecovery in old_emailrecoverys:
                        old_emailrecoverys.insert(0, old_mail.emailrecovery)
                        if "" in old_emailrecoverys:
                            old_emailrecoverys.remove("")
                        update["oldemailrecovery"] = '\n'.join(old_emailrecoverys)
                update_dict = {k: v for k, v in update.items() if v}
                db.query(mailTable).filter(mailTable.id == id).update(update_dict)
                db.commit()
                return Result()
        except Exception as e:
            db.rollback()
            error = hfile.getError()
            log(f"update_mail fail {error}")
            return Result(False, "update_mail fail", e.args)

    def getRapt(self):
        if not self.getrapt:
            self.rapt = "1"
        if self.rapt:
            return self.rapt
        self.loginok = True
        p = self.p
        url = p.url
        url = url.replace("%3D", "=")
        rapt = hstr.regex(url + "&", "rapt=(.*?)&")
        if rapt != "":
            self.rapt = rapt
            return self.rapt
        p.goto("https://myaccount.google.com/signinoptions/rescuephone")
        return ""
