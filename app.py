from flask import Flask
import os

app = Flask(__name__)

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(current_file_path)







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)