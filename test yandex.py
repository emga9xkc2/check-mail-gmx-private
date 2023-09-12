import time
t = time.time()
from script.download import *
title = "Gmail Manage"
setupPythonPath(title)
sys.path.append(scriptPathAppend)

from script.yandex import *

from hfile import *
cookie = hfile.read("data/yandex.txt")
email = "dinaisalamaali3554@gmail01.site"
yan = yandex()
yan.debug = True
yan.cookie = cookie
code = yan.get_code(email)
print(code)
