from att import create_app
from att.static.root_path import Config
import os

app = create_app()

if not os.path.exists('./original.yaml'):
    raise OSError("Please run stage.py first.")
if not os.path.exists(Config.extracted_path):
    raise OSError("Please run link_and_clear.py first.")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
