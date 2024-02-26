import base64
import json
import http.client
import secrets
import string
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField,EmailField,PasswordField)
from wtforms.validators import InputRequired, Length,Email,Regexp,EqualTo
# from form.forms import RegistrationForm
# from urllib.request import urlopen
from app.forms.forms import RegistrationForm
# from flask_wtf import FlaskForm
from flask import (jsonify, render_template,request, url_for, flash, redirect,Flask)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user,current_user, LoginManager
import random
import psycopg2
from app import app
from app import oauth
from app import db
# from sqlalchemy.sql import text
from app.models.accounts import Account
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

READY = False

def read_file(filename, mode="rt"):
    with open(filename, mode, encoding='utf-8') as fin:
        return fin.read()

def write_file(filename, contents, mode="wt"):
    with open(filename, mode, encoding="utf-8") as fout:
        fout.write(contents)
@app.route('/process', methods=['POST']) 
def process():
    data = request.form.get('data')
    return

# @app.route('/')
# def home():
#     return app.send_static_file('login.html')


#     #         db.session.commit()
#     return app.send_static_file('login.html')


@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/camera")
def camera_access():
    return render_template("camera.html")


# @app.route("/api")
# def call_api():
#     if READY:
#       with open('static/img/photo1.jpg', 'rb') as file:
#           images = [base64.b64encode(file.read()).decode('ascii')]

#       type_iden = ["health_assessment","identification"]

#       url_iden = "https://plant.id/api/v3/" + type_iden[1]
#       DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
#       q_iden = "?details=" + DETAILS +"&language=en"
#       url_iden += q_iden

#       payload = json.dumps({
#         "images": ["data:image/jpg;base64," + images[0]],
#         "similar_images": "true"
#       })
#       headers = {
#         'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
#         'Content-Type': 'application/json'
#       }

#       response = requests.request("POST", url_iden, headers=headers, data=payload)

#   # list_data = get_data(response)

#       raw_data = read_file("app/sandbox/Tle_sandbox/fake_data.txt")
#       fake_data = list(map(lambda x : get_data(eval(x)), raw_data))
#   # list_data = 
#   # db_plant = 
#   # print(fake_data)


#   return render_template("temp.html", data=fake_data)

@app.route("/user")
def user():
    db_users = Account.query.all()
    user = list(map(lambda x: x.to_dict(), db_users))
    return jsonify(user)

@app.route("/user/validate", methods=["GET", "POST"])
def validate_user():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get("id", "")
        validated = True
        validated_dict = {}
        valid_keys = ["firstname", "lastname"]



@app.route("/login",methods=('GET','POST'))
def login():
    logout_user()
    if request.method == 'POST':

        email = request.form.get('email').lower()
        password = request.form.get('password')
        user = Account.query.filter_by(email=email).first()
        print("login",email,password)
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('landing'))

    return render_template('login.html')

@app.route("/faqs")
def feqs():
    return render_template("faqs.html")

# Written by Wachirapong
# To call API
@app.route("/api")
def call_api():
    # if READY:
    #     with open('static/img/photo1.jpg', 'rb') as file:
    #         images = [base64.b64encode(file.read()).decode('ascii')]

    #     type_iden = ["health_assessment","identification"]

    #     url_iden = "https://plant.id/api/v3/" + type_iden[1]
    #     DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
    #     q_iden = "?details=" + DETAILS +"&language=en"
    #     url_iden += q_iden

    #     payload = json.dumps({
    #         "images": ["data:image/jpg;base64," + images[0]],
    #         "similar_images": "true"
    #     })
    #     headers = {
    #         'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
    #         'Content-Type': 'application/json'
    #     }

    #     response = requests.request("POST", url_iden, headers=headers, data=payload)

  # list_data = get_data(response)

    raw_data = read_file("app/sandbox/Tle_sandbox/fake_data.txt")
    data_list = eval(raw_data)
    
    fake_data = list(map(lambda x : get_data(x), data_list))
    # list_data = 
    # db_plant = 
    # print(fake_data)


    return render_template("plant_data.html", data=fake_data)


# Written by Wachirapong
# To get data from API that we need to list
def get_data(res):
    is_plant = res["result"]["is_plant"]["probability"]
    name = res["result"]["classification"]["suggestions"]
    dict_val = {}

    list_data = []
    for val in name:
        dict_val["id"] = val["id"]
        dict_val["name"] = val["name"]
        dict_val["probability"] = val["probability"]
        dict_val["similar_img"] = val["similar_images"]
        dict_val["common_name"] = val["details"]["common_names"]
        dict_val["taxonomy"] = val["details"]["taxonomy"]
        dict_val["url"] = val["details"]["url"]
        dict_val["description"] = val["details"]["description"]["value"]
        dict_val["synonyms"] = val["details"]["synonyms"]
        dict_val["img"] = val["details"]["image"]["value"]
        dict_val["watering"] = val["details"]["watering"]
        dict_val["propagation_methods"] = val["details"]["propagation_methods"]
        list_data.append(dict_val)
    return list_data


@app.route("/search")
def search():
   return render_template("search.html")
def validate_email_domain(form, field):
    email = field.data
    allowed_domains = ['gmail.com', 'hotmail.com','cmu.ac.th']
    domain = email.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f'Invalid email domain. Allowed domains are: {", ".join(allowed_domains)}')
@app.route("/signup", methods=('GET', 'POST'))
def signup():
    
    if request.method == 'POST' :
        result = request.form.to_dict()
        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password']
        for key in result:
            if key not in valid_keys:
                continue
            value = result[key].strip()
            if not value or value == 'undefined':
                
                validated = False
                break
            validated_dict[key] = value
            validated_value = RegistrationForm()
            
        if   len(validated_dict["name"]) < 2 or len(validated_dict["name"])>20:
            flash('name must be between 2 and 20 characters long')
            return redirect(url_for('signup'))
        elif   not is_valid_email_domain(validated_dict["email"]) :
            flash('Email is required mush be *@gmail.com or *@hotmail.com or *@cmu.ac.th')
            return redirect(url_for('signup'))
        elif  not is_valid_password(validated_dict["password"]):
            flash('Password must contain at least 8 characters including at least one digit, one lowercase letter, one uppercase letter, and one special character')
            return redirect(url_for('signup'))
        elif validated:
            email = validated_dict['email'].lower()
            name = validated_dict['name']
            password = validated_dict['password']
            user = Account.query.filter_by(email=email).first()
            if user:
                flash('Email address already exists')
                return redirect(url_for('signup'))  
            print("signup",email,password)
            new_user = Account(email=email, name=name, password=generate_password_hash(password, method='sha256'),avatar_url="static/img/avatar/"+str(random.randint(1, 8))+".png",login_with="server")
            db.session.add(new_user)

            db.session.commit()

        return redirect(url_for('login')) 
        
    return render_template("signup.html")





@app.route("/signup/data")
def si():
    db_accounts = Account.query.all()
    accounts = list(map(lambda x: x.to_dict(), db_accounts))
    return jsonify(accounts)

@app.route("/update",methods=('POST','GET'))
def update():

    if request.method == 'POST':
        check = False
        result = request.form.to_dict()
        email = result.get('email','')
        name = result.get('name','')
        avatar = result.get('avatar_url','')
        password = result.get('password','')
        accounts = Account.query.get(current_user.id)
        if password == '':
            password = current_user.password
            check=True
        if   len(name) < 2 or len(name)>20:
            flash('name must be between 2 and 20 characters long')
            return "name"
        elif   not is_valid_email_domain(email) :
            flash('Email is required mush be *@gmail.com or *@hotmail.com or *@cmu.ac.th')
            return "email"
        elif  not is_valid_password(password):
            # flash('check')
            flash('Password must contain at least 8 characters including at least one digit, one lowercase letter, one uppercase letter, and one special character')
            return "password"
        if check:
            accounts.update(email=email,name=name, avatar_url=avatar,password=password)
        else:
            accounts.update(email=email,name=name, avatar_url=avatar,password=generate_password_hash(password, method='sha256'))
        db.session.commit()
    return redirect(url_for('landing'))

@app.route("/checkpassword",methods=('GET','POST'))
def hw10_update():
    ans={"ans":False}
    if request.method == "POST":
        result = request.form.to_dict()
        password = result.get('password','')
        contact = Account.query.get(current_user.id)
        print("update",password)
        if check_password_hash(contact.password,password):
            ans["ans"]=True
            return ans
        else :
            flash('password not correct')
    return ans

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

# @app.route('/validate_email', methods=['POST'])
# def validate_email():
#     ans={"ans":False}
#     form = RegistrationForm(request.form.to_dict().get('email',''))
#     if form.validate():
#         ans["ans":True]
#         return ans

#     return ans
def is_valid_email_domain(email):
    domain = email.split('@')[-1]
    return domain in ['gmail.com', 'hotmail.com', 'cmu.ac.th']

def is_valid_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/~' for c in password)

@app.route('/google/')
def google():


    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope' : 'openid email profile',
            # 'redirect_uri':  'postmessage'
        }
    )
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..",app.config['GOOGLE_CLIENT_ID'],app.config['GOOGLE_CLIENT_SECRET'],app.config['GOOGLE_DISCOVERY_URL'])
    # app.logger.debug("str(token)")
   # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)





@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    userinfo = token['userinfo']
    email = userinfo['email']
    user = Account.query.filter_by(email=email).first()
    # print(userinfo['password'])

    if not user:
        name = userinfo.get('given_name','') + " " + userinfo.get('family_name','')
        random_pass_len = 8
        # password = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(random_pass_len))
        password = "12345678"
        picture = "static/img/avatar/"+str(random.randint(1, 8))+".png"
        new_user = Account(email=email, name=name,password=generate_password_hash(password, method='sha256'),avatar_url=picture,login_with="google")
        db.session.add(new_user)
        db.session.commit()
        user = Account.query.filter_by(email=email).first()
        login_user(user)
        flash("your password is 12345678, you can change it in the profile.")
    return redirect('/landing')

@app.route('/facebook/')
def facebook():
   
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = app.config['FACEBOOK_CLIENT_ID']
    FACEBOOK_CLIENT_SECRET = app.config['FACEBOOK_CLIENT_SECRET']
    # print(",,,,,,,,,,,,,,",FACEBOOK_CLIENT_ID,FACEBOOK_CLIENT_SECRET)
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)
 
@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)
    email = profile['email']
    name = profile['name']
    random_pass_len = random_pass_len = 8
    # password = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(random_pass_len))
    password = "12345678"
    user = Account.query.filter_by(email=email).first()


    if not user:
        picture = "static/img/avatar/"+str(random.randint(1, 8))+".png"
        new_user = Account(email=email, name=name,password=generate_password_hash(password, method='sha256'),avatar_url=picture,login_with ="facebook")
        db.session.add(new_user)
        db.session.commit()
        user = Account.query.filter_by(email=email).first()
        login_user(user)
        flash("your password is 12345678, you can change it in the profile.")
    return redirect('/landing')