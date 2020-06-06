import base64
coded_string = '''Q5YACgA...'''
a =base64.b64encode("GET /index.php/2017/11/14/cong-ty-misa-tuyen-fresher/".encode("utf-8"))

data = base64.b64decode(a)
# print()
data = base64.b64decode("R0VUIC9pbmRleC5waHAvMjAxNy8xMS8xNC9jb25nLXR5LW1pc2EtdHV5ZW4tZnJlc2hlci8=")
print(len(str(a)))
print(data.decode("utf-8"))

