
import os
if 'SERVER_SOFTWARE' in os.environ:
    from sae.taskqueue import add_task
else:
    import urllib2
    import threading
    class MyHandler(urllib2.HTTPHandler):
        def http_response(self, req, response):
            print "response"
            return response

    def add_task(queue, url, param=None):
        print "add task", queue, url, param
        o = urllib2.build_opener(MyHandler())
        t = threading.Thread(target=o.open, args=('http://localhost:8080/'+url,))
        t.start()
        # urllib2.urlopen('http://localhost:8080/'+url, timeout=10)