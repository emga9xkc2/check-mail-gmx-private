from hplaywright import *
hpw = hplaywright()
p = hpw.openChrome()
p.goto("https://www.walmart.com/account/signup?vid=oaoh&tid=0&returnUrl=%2F%3Faction%3DCreate%26rm%3Dtrue")
while 1:
    time.sleep(1)
