from att import create_app
from att.static.root_path import Config
import os
# from OpenSSL import SSL
# context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

app = create_app()

if not os.path.exists('./original.yaml'):
    raise OSError("Please run stage.py first.")
if not os.path.exists(Config.extracted_path):
    raise OSError("Please run link_and_clear.py first.")

if __name__ == '__main__':
    app.run(host="0.0.0.0")#, ssl_context=context)
