from att import create_app
import os

app = create_app()

if __name__ == '__main__':
    if not os.path.exists('./original.yaml'):
        raise OSError("Please run stage.py first.")
    app.run()
