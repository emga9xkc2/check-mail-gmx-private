from hrequest import *
rq = hrequest()
html = rq.post("http://127.0.0.1:5555/create-profile-by-default", '{"config_id": "98"}', getStr=True)
print(html)
