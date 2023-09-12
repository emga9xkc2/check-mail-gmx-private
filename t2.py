import time
from hstr import *
from hthread import *

proxyssh = ["proxy", "ssh"]
def B(ids, proxy):
    while ids:
        idRun = ids.pop(0)
        print("B", idRun)
        if not proxy in proxyssh:
            return
def A(proxy):
    if proxy in proxyssh:
        return
    print("A")
    time.sleep(1)

ids = [1,2,3,4,5,6,7,8,9]
proxy = "3g"
def run():
    thread = 5
    ids_chunks = hstr.chiaDeuList(ids, thread)
    while ids_chunks:
        A(proxy)
        for i in ids_chunks:
            if i:
                hthread.start(B, [i, proxy], addlist=True)
        hthread.waitThreadsDone()
        ids_chunks = [chunk for chunk in ids_chunks if chunk]
        time.sleep(1)
    print("Run done")
run()
