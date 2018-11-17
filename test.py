import requests
import re

pattern = re.compile('<B>(.*?)</B>')
#html = requests.get("http://littlebigluo.qicp.net:47720")
file = open('auth_code.png','rb')
image = {'file': file}
#print(image)


#print(dir(image))
resulet = requests.post(url="http://littlebigluo.qicp.net:47720", files=image)
index = re.search(pattern, resulet.text)
print(index.group(1).split())
file.close()
