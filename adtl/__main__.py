from adtl import app
from adtl.common import HOST, PORT

if __name__ == "__main__":
    app.create_app().run(host=HOST, port=PORT)
