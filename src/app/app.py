from flask import Flask


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    return custom_response("Hello World!")

@app.route("/content", methods=["POST"])
def content():
    return custom_response(
        {
        "order": ["Skills", "Profile", "Experience"],
        "data": [
            {
                "title": "Profile",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis, ad unde adipisci quas veniam doloribus nobis alias qui, veritatis numquam eligendi sed tempora odio officia commodi non consectetur. Provident, assumenda.",
            },
            {
                "title": "Experience",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis, ad unde adipisci quas veniam doloribus nobis alias qui, veritatis numquam eligendi sed tempora odio officia commodi non consectetur. Provident, assumenda.",
            },
            {
                "title": "Skills",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis, ad unde adipisci quas veniam doloribus nobis alias qui, veritatis numquam eligendi sed tempora odio officia commodi non consectetur. Provident, assumenda.",
            }
        ]}, 200)

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
