from flask import Flask, request, send_from_directory
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

@app.route('/csv', methods = ['POST'])
def get_csv():
    file_name = os.getenv('FILE_NAME')
    return send_from_directory('.',file_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)