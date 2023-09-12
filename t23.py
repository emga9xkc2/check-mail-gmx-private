from hrequest import *
rq = hrequest()
res = rq.get("https://identity.appen.com/")
res = rq.get("https://identity.appen.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fp?x-kpsdk-v=j-0.0.0")
print(res.headers)
kpsdkCt = res.headers.get("x-kpsdk-ct")
data = f"username=1&password=2&credentialId=&kpsdkCt={kpsdkCt}&kpsdkV=j-0.0.0&kpsdkCd=%7B%22workTime%22%3A1688239062226%2C%22id%22%3A%22e26077fc2bb3146bf78a249eb99291a2%22%2C%22answers%22%3A%5B3%2C2%5D%2C%22duration%22%3A1.2%2C%22d%22%3A587%2C%22st%22%3A1688239059282%2C%22rst%22%3A1688239059869%7D"
res = rq.post("https://identity.appen.com/auth/realms/QRP/login-actions/authenticate?session_code=N76ZzM3Sa4SpYxiEUZE7yTXOhXZSFG0jx6XEqOWtLno&execution=19839b9e-b4ef-4599-956a-95672db15271&client_id=appen-connect&tab_id=dXlu-UxN18Q", data)
print(res.text)
