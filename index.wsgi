import sae
from invt import wsgi

application = sae.create_wsgi_app(wsgi.application)