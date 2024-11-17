
from flask import Flask, request
from linkedinautopost.facade.chat_gpt import ChatGPT
from linkedinautopost.facade.linkedin import LinkedIn

app = Flask(__name__)
linkedin_handler = LinkedIn()
gpt_handler = ChatGPT()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/login")
def login():
    linkedin_handler.get_auth_code()

@app.route("/linkedin/callback")
def linkedin_callback():
    authorization_code = request.args.get("code")
    if authorization_code:
        linkedin_handler.get_access_token(authorization_code)
        return "Extracted authorization code"
    else:
        return "Authorization code not found in the request."
    
@app.route("/makePostContent", methods=['POST'])
def make_post_content():
    description = request.json['description']
    skills = request.json['skills']
    answer = gpt_handler.ask_question(description, skills)

    return answer

@app.route("/postPost", methods=['POST'])
def post_post():
    post_content = request.json["text"]
    response = linkedin_handler.post(post_content)

    return response