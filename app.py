from flask import Flask,render_template,url_for,Response,redirect
import cv2
from authlib.integrations.flask_client import OAuth


app=Flask(__name__)
oauth=OAuth(app)
app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GOOGLE_CLIENT_ID']= "1067384783903-5vo89t4tevet3p64p84n5jip5gtj3fkb.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET']="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"

app.config['GITHUB_CLIENT_ID']="103a6457b4ffc37879bd"
app.config['GITHUB_CLIENT_SECRET']="4eaf1d49e735ec4959e5b6725a9f5cd01f22ba7b"
google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)
github = oauth.register (
  name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)

camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cv2.destroyAllWindows()

def generate_frames():
    while True:
        success,frame=camera.read()
        if not success:
            break
        else :
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")

# def index():
#     return render_template('index.html')   hello world
def index():
    return render_template('index1.html')

@app.route("/video")

def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login/google')
def google_login():
    google=oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    #return "You are successfully signed in  using Google"
    return render_template('index.html')

@app.route('/login/github')
def github_login():
    github=oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/login/github/authorize')
def github_authorize():
    github=oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print(f"\n{resp}\n")
    return render_template('index.html')
    


if __name__=="__main__":
     app.run(debug=True)