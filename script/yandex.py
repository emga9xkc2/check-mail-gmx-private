
from hrequest import *
class yandex:
    def __init__(self):
        self.cookie = ""
        self.listcode = []
        self.debug = False
        pass

    def get_code(self, email):

        rq = hrequest()
        rq.setCookie(self.cookie)
        rq.setUserAgent("Opera/9.80 (iPhone; Opera Mini/8.0.0/34.2336; U; en) Presto/2.8.119 Version/11.10")
        html = rq.getHtml(f"https://mail.yandex.com/lite/search?request={email}&")
        if self.debug:
            print(html)
        codes = hstr.regexs(html, email + '.{3,360}(\\b\\d{6}\\b)', re.DOTALL)
        for i in codes:
            code = i[0]
            if not code in self.listcode:
                self.listcode.append(code)
                return code
        return ""

# a = """
# Google
# Mã xác minh Google
# Mã xác minh Google Kính gửi người dùng Google! Mã xác minh bạn cần dùng để truy cập vào Tài khoản Google của mình (kwailan98407826@gmailz1.com) là: 556780 Nếu bạn không yêu cầu mã này thì có thể là ai đó đang tìm cách truy cập vào Tài khoản Google kwailan98407826@gmailz1.com. Không chuyển tiếp hoặc cung cấp mã này
# Jul, 2
# Google
# Mã xác minh Google
# Mã xác minh Google Kính gửi người dùng Google! Mã xác minh bạn cần dùng để truy cập vào Tài khoản Google của mình (wong98418133@gmailz1.com) là: 861046 Nếu bạn không yêu cầu mã này thì có thể là ai đó đang tìm cách truy cập vào Tài khoản Google wong98418133@gmailz1.com. Không chuyển tiếp hoặc cung cấp mã này cho
# Jul, 2
# Google
# Mã xác minh Google
# Mã xác minh Google Kính gửi người dùng Google! Mã xác minh bạn cần dùng để truy cập vào Tài khoản Google của mình (auyeunglaifun@gmailz1.com) là: 371661 Nếu bạn không yêu cầu mã này thì có thể là ai đó đang tìm cách truy cập vào Tài khoản Google auyeunglaifun@gmailz1.com. Không chuyển tiếp hoặc cung cấp mã này cho
# Jul, 2
# Google
# Mã xác minh Google
# Mã xác minh Google Kính gửi người dùng Google! Mã xác minh bạn cần dùng để truy cập vào Tài khoản Google của mình (lauchiman135@gmailz1.com) là: 800132
# """
# codes = hstr.regexs(a, "@gmailz1.com" + '.{3,20}(\\d{6})', re.DOTALL)
# print(codes)
