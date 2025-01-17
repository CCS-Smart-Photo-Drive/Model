from flask import Flask
from flask_cors import CORS  # Import CORS
from myproject import app

CORS(app, supports_credentials=True)


if __name__=='__main__':
    app.run(debug=True)