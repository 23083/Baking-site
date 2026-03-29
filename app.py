from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    #homepage
    return "Hello, Again!"

if __name__ == "__main__":
    app.run(debug=True)