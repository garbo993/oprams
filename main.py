from flask import Flask, jsonify,  request





app = Flask(__name__)

@app.route("/")
def root():
    return "home"


@app.route("/login")
def login():
    return (request)




if __name__ == "__main__":
    app.run(debug=True)




