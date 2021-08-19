from flask import Flask


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    return custom_response("Hello World!")

def custom_response(body, code=None, headers=None):
    """Returns a tuple with body, code and/or headers"""
    if code is None:
        code = 200
    if headers is None:
        headers = {
            "Access-Control-Allow-Origin": "*"
            }
    return body, code, headers

if __name__ == "__main__":
    app.run(debug=True)
