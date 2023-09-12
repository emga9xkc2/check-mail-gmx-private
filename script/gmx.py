
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


class GMX:
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

            user_data_dir = ""

            if self.path_saveprofile:
                user_data_dir = self.path_saveprofile + "\\" + self.email_lower
            self.p = hpw.openChrome(self.proxy, user_data_dir=user_data_dir, executable=self.orbita_browser_check, headless=True)


            self.p: ExtendedPage
            if not self.p:
                return self.login()

            self.hpw = hpw
            p = self.p



            recovery = False
            timestart = time.time()
            recaptcha = 0
            phoneresend = {}


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
            self.lastUrl = p.url
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
                if "config_homepage.js" in url:
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
                    if "https://www.gmx.net/consent-management/" in url:
                        p.goto("https://www.gmx.net/")
                    if "https://www.gmx.net/logoutlounge/?status=login-failed" in url:
                        # while 1:
                        #     p.sleep(1)
                        return "sai_pass"
                    if "navigator.gmx.net/login" in url:
                        return "login ok"
                    if "interceptiontype=VerifyLogin" in url:
                        return "captcha"
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



    def openUrl(self, newurl, lastUrl):
        nowurl = self.p.url
        if nowurl == lastUrl or nowurl == "chrome-error://chromewebdata/" or nowurl == "chrome://new-tab-page/":
            self.p.goto(newurl)
            self.iloadfail = self.iloadfail + 1
        else:
            self.iloadfail = 0



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

