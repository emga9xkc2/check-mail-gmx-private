from script.download import *
import script.conn as con
setupPythonPath(con.title)
sys.path.append(scriptPathAppend)
first_title = con.title.split("_")[0].strip()
last_title = ""
if "_" in con.title:
    last_title = con.title.split("_")[1].strip()

from hwin32 import *
hwin32.hideWindowTitle(first_title.upper(), useThread=True, hideEndswithPyc=True, last_title = last_title)
from heel import *
def run():
    try:
        import script.script
    except Exception as e:
        print(e)




from hrequest import *

# rq = hrequest()
# rq.setProxy("43.157.121.234:12126")
# html = rq.get_html("https://interception1.gmx.net/logininterceptionfrontend/?interceptiontype=VerifyLogin&interceptiontype=VerifyLogin&service=freemail")
# rq.html_test(html)

hthread.start(run)

if __name__ == "__main__":
    host="127.0.0.1"
    port = "52222"
    # port= free_port()
    print(host + ":" + str(port))

    startEel(host=host, port=port, size=(1200,790), title=first_title, use_cef=True)

