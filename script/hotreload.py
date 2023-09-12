from playwright.sync_api import sync_playwright, TimeoutError
from playwright.sync_api._generated import Page
import time
import sys
import requests

sys.path.append("..")

from hstr import *
from hrand import *
from hfile import *
from hinfo import *
from hotp import *
from script.expose import *
from hcaptcha import *
from hplaywrightExtended import *

from hwin import *
from hwin32 import *
from himagesearch import *
from hrequest import *
import asyncio
import sys
name = lambda n=0: sys._getframe(n + 1).f_code.co_name

from himap import himap
def f1(self):
    # print("reload")
    # time.sleep(1)
    # return
    if not self:
        return
    p: ExtendedPage = self.p

    # print(p.frames)
    # frames =p.frames;
    # for  i in p.frames:
    #     title = i.locator(".rc-doscaptcha-body-text a")
    #     if title.is_visible():
    #         p.reload()
    #         print(title)
    p.sleep(1)
    # frame = p.locatorFrame('*[title="reCAPTCHA"]')
    # checkbox = frame.locator(".recaptcha-checkbox-checked")
    # if checkbox.is_visible(timeout=1000):
    #     print(checkbox.inner_html(timeout=5000))
    # recaptcha = p.frame_locator('*[title="reCAPTCHA"]').locator('#recaptcha-accessible-status')
    # print(recaptcha.inner_html(timeout=5000))
    # for frame in p.frames:

    #     if not "https://www.google.com/recaptcha/api2/bframe" in frame.url:
    #         continue

    #     checkbox = frame.locator("#recaptcha-accessible-status")

    #     print(checkbox.inner_html(timeout=5000), "1111111111111")
    return
    _info = hinfo()
    p.sleep(1)
    # autoReload("f1", self)
    timestart = time.time()
    clickgui = False
    otp: hotp = self.otpyoutube
    while time.time() - timestart < 2:
        try:
            self.openUrl("https://www.youtube.com/create_channel?action_create_new_channel_redirect=true", self.lastUrl)
            url = p.get_url()
            if "PlusPageSignUp" in url:
                PlusPageName = p.locatorSelector("#PlusPageName")
                if PlusPageName.isdisplay():
                    if _info.listFirstUs:
                        info = _info.get()
                        PlusPageName.type(info.get("first") + " " + info.get("last"))
                ConsentCheckbox = p.locatorSelector("#ConsentCheckbox")
                if ConsentCheckbox.isdisplay():
                    if not ConsentCheckbox.is_checked():
                        ConsentCheckbox.click()
                    if ConsentCheckbox.is_checked():
                        submitbutton = p.locatorSelector("#submitbutton")
                        if submitbutton.isdisplay():
                            submitbutton.click()
            if "/PlusPageSignUpIdvChallenge" in url:
                verifyphoneinput = p.locatorSelector("#verify-phone-input")
                if verifyphoneinput.isdisplay():
                    code = otp.getCode()
                    if not code:
                        return "Không thể lấy code otp"
                    verifyphoneinput.type(code, press="Enter")
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
                    signupidvinput.type(otp.phone, press="Enter")

            if "/channel/" in url:
                p.goto("https://www.youtube.com/create_channel?action_create_new_channel_redirect=true")

        except Exception as e:
            print(e)
        p.sleep(1)
    return "timeout.changecountry"


