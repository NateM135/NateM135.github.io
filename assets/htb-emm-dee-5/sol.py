import requests
import hashlib

link = "http://docker.hackthebox.eu:30338/"

r = requests.session()
init = r.get(link)
hash = hashlib.md5(init.text[167:].split("</h3>")[0].encode()).hexdigest()
print(hash)
data = {'hash': hash}
out = r.post(url=link, data=data)
print(out.text)