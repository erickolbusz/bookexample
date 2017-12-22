from flask import Flask
app = Flask(__name__) # pylint: disable=invalid-name
import bookapp.routes # pylint: disable=wrong-import-position