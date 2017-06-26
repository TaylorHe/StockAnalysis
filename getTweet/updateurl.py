
port = input("port?: (usu 5002) ")
url = input("url?: (usu http://127.0.0.1) ")
handle = open("myurl.py", "w")
handle.write("""
port = '%s'
url = '%s'
""" % (port, url))
handle.close()
