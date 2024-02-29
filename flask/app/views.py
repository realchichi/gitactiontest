import base64
import json
import http.client
import requests
import os
import hashlib
import random
from flask import (jsonify, render_template,request, url_for, flash, redirect,Flask)
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user,current_user, LoginManager
from app.forms.forms import RegistrationForm
from app import app
from app import oauth
from sqlalchemy import desc
from app import db
from app.models.accounts import Account
from app.models.history import History
from app.models.plantinfo import PlantInfo
from app.models.community import Community
from app.models.community import Comment
# from app.models.community import Community
# from app.models.community import Comment
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))



def read_file(filename, mode="rt"):
    with open(filename, mode, encoding='utf-8') as fin:
        return fin.read()


def write_file(filename, contents, mode="wt"):
    with open(filename, mode, encoding="utf-8") as fout:
        fout.write(contents)



@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/landing")
def landing():
    return render_template("landing.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/user")
def user():
    db_users = Account.query.all()
    user = list(map(lambda x: x.to_dict(), db_users))
    return jsonify(user)


#bas
@app.route("/user/validate", methods=["GET", "POST"])
def validate_user():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get("id", "")
        validated = True
        validated_dict = {}
        valid_keys = ["firstname", "lastname"]


#bas
@app.route("/login",methods=('GET','POST'))
def login():
    logout_user()
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        user = Account.query.filter_by(email=email).first()
        remember = bool(request.form.get('is_active'))
        print("login",email,password)
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('landing'))
    return render_template('login.html')


#chi
@app.route("/faqs")
def feqs():
    return render_template("faqs.html")


@app.route("/community")
def community():
    return render_template("community.html")

# Written by Wachirapong
# To call validate form and store to database
@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    if request.method == "POST":
        result = request.form.to_dict()
        # print(result)
        valid_keys = ["name", "email", "message"]
        validated_dict = {}
        validated = True

        for key in result:
            if key not in valid_keys:
                continue

            if not result[key] or result[key] == "undefined":
                validated = False
                break

            validated_dict[key] = result[key].strip()
        # if validated:
        #     contact = Contact(**validated_dict)
        #     db.session.add(contact)

        # db.session.commit()
    return render_template("contact_us.html")


# Written by Wachirapong
# To call API
@app.route("/api")
@login_required
def call_api(img):
    # with open('app/static/img/longan1.jpg', 'rb') as file:
    #     images = [base64.b64encode(file.read()).decode('ascii')]

    url = "https://plant.id/api/v3/identification"
    DETAILS = "common_names,url,description,taxonomy,rank,gbif_id,inaturalist_id,image,synonyms,edible_parts,watering,propagation_methods"
    query = "?details=" + DETAILS +"&language=th"
    url += query

    payload = json.dumps({
        "images": ["data:image/jpg;base64," + img],
        "similar_images": True
    })
    headers = {
        'Api-Key': 'XbcsHOYrpQJBei7BNsrP7TeXUyerkYd1SpqRVAfSgq2T9lIZbu',
        'Content-Type': 'application/json'
    }

    # if u need to call API use these 2 lines
    response = requests.request("POST", url, headers=headers, data=payload)
    list_data = get_data(json.loads(response.text))
    # these 2 lines for temp data
    # raw_data = read_file("app/sandbox/data.txt")
    # list_data = eval(raw_data)

    return list_data

    
# Written by Wachirapong
# To get data from API that we need to put into list
def get_data(data):
    name = data["result"]["classification"]["suggestions"]
    list_data = []
    count = 0
    for val in name:
        dict_val = {}
        if count == 5:
            break
        dict_val["name"] = val.get("name", "N/A")
        dict_val["url_image"] = val["details"]["image"].get("value", "N/A")
        # print(val["details"]["description"])
        if val["details"]["description"]:
            dict_val["description"] = val["details"]["description"]["value"]
        else:
            dict_val["description"] = "N/A"
        dict_val["wiki_url"] = val["details"].get("url", "N/A")
        dict_val["taxonomy"] = str(val["details"].get("taxonomy", "N/A")).replace(":", ",")
        dict_val["common_name"] = val["details"].get("common_names", "N/A")
        dict_val["similar_images"] = []
        count_img = 0
        for simi_img in val["similar_images"]:
            if count_img == 3:
                break
            dict_val["similar_images"].append(simi_img["url"])
            count_img += 1
        dict_val["probability"] = val.get("probability", "N/A")
        count += 1
        list_data.append(dict_val)
    return list_data


# Written by Wachirapong
# To store plant data table that user who identified plant
# and store it to history table
@app.route("/identification", methods=["POST", "GET"])
@login_required
def identification():
    if request.method == "POST":
        img = request.form.to_dict().get("image", "")
        if img:
            img_data = base64.b64decode(img.split(',')[1])
            hash_img = hashlib.sha256(img.encode('UTF-8')).hexdigest()[:16]
            filename = os.path.join(app.config['UPLOAD_FOLDER'], hash_img + ".jpg")
            with open(filename, "wb") as image_file:
                image_file.write(img_data)

            account_id = current_user.id
            identified_img = filename
            entry = History(account_id, identified_img)
            db.session.add(entry)
            iden_plant = History.query.filter_by(identified_img=identified_img).all()
            list_iden_plant = list(map(lambda x: x.identified_img, iden_plant))
            history = History.query.filter_by(identified_img=identified_img).first()
            if identified_img in list_iden_plant:
                history = History.query.order_by(desc(History.identified_date)).first()
            plant_data = call_api(img.split(',')[1])
            for i in range(len(plant_data)):
                temp = plant_data[i]
                temp["history_id"] = history.id
                plant_info = PlantInfo(**temp)
                db.session.add(plant_info)

            db.session.commit()
            return jsonify({"identified_plant" : hash_img})
    return render_template("identification.html")


# Written by Wachirapong
# To show data form API call
@app.route("/result")
@login_required
def result():
    plant = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('plant_data') + ".jpg")
    history = History.query.filter_by(identified_img=plant, removed_by=None).first()
    iden_plant = History.query.filter_by(identified_img=plant).all()
    list_iden_plant = list(map(lambda x: x.identified_img, iden_plant))
    history = History.query.filter_by(identified_img=plant).first()
    if plant in list_iden_plant:
        history = History.query.order_by(desc(History.identified_date)).first()
    id = history.id
    plant_info = PlantInfo.query.filter_by(history_id=id).all()
    list_plant = list(map(lambda x: convert_to_list(x.to_dict()), plant_info))
    return render_template("result.html", plant_data=list_plant, identified_img=plant[4:])


# Written by Wachirapong
# some value in dict there is {} in it
# To strip {} and convert it to list
def convert_to_list(dict_):
    for key in dict_:
        if key == "taxonomy":
            temp = dict_[key].split(",")
            list_temp = list(map(lambda x: x.strip(''' { } " ' '''), temp))
            dict_[key] = list_temp
            continue
        if isinstance(dict_[key], str):
            if "{" in dict_[key]:
                temp = dict_[key].strip("{}")
                list_temp = temp.split(",")
                result = []
                for item in list_temp:
                    result.append(item)
                dict_[key] = result
    return dict_

#bas
def validate_email_domain(form, field):
    email = field.data
    allowed_domains = ['gmail.com', 'hotmail.com','cmu.ac.th']
    domain = email.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f'Invalid email domain. Allowed domains are: {", ".join(allowed_domains)}')

#ohm
@app.route("/communtity", methods=("POST","GET"))
def storedata_commu():
    validated = True
    if request.method == 'POST' :
        result = request.form.to_dict()
        validated_dict = dict()
        valid_keys = ['plant_name', 'message','img_plant']
        account_id = current_user.id

        for key in result:
            app.logger.debug(f"{key}: {result[key]}")

            if key not in valid_keys:
                continue

            value = result[key].strip()

            if not value or value == 'undefined':
                validated = False
                break

            validated_dict[key] = value
        print(validated_dict,"66666666666666666666666")
        if validated:
            validated_dict['account_id']=account_id
            plant_share = Community(**validated_dict)
            db.session.add(plant_share) 
            db.session.commit()
    # print(validated_dict)
    return render_template('community.html')




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
            new_user = Account(email=email, name=name, password=generate_password_hash(password, method='sha256'),avatar_url="static/img/avatar/"+str(random.randint(1, 16))+".png",login_with="server")
            db.session.add(new_user)

            db.session.commit()

        return redirect(url_for('login')) 
        
    return render_template("signup.html")


#bas
@app.route("/signup/data")
def si():
    db_accounts = Account.query.all()
    accounts = list(map(lambda x: x.to_dict(), db_accounts))
    return jsonify(accounts)


#bas
@app.route("/update",methods=('POST','GET'))
@login_required
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


#bas
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


#bas
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))


def is_valid_email_domain(email):
    domain = email.split('@')[-1]
    return domain in ['gmail.com', 'hotmail.com', 'cmu.ac.th']


def is_valid_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/~' for c in password)


#bas
@app.route('/google/')
def google():
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope' : 'openid email profile',
        }
    )
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)




#bas
@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    userinfo = token['userinfo']
    email = userinfo['email']
    user = Account.query.filter_by(email=email).first()
    # print(userinfo['password'])

    if not user:
        name = userinfo.get('given_name','') + " " + userinfo.get('family_name','')
        password = "12345678"
        picture = "static/img/avatar/"+str(random.randint(1, 16))+".png"
        new_user = Account(email=email, name=name,password=generate_password_hash(password, method='sha256'),avatar_url=picture,login_with="google")
        db.session.add(new_user)
        db.session.commit()
        user = Account.query.filter_by(email=email).first()
        login_user(user)
        flash("your password is 12345678, you can change it in the profile.")
    else:
        user = Account.query.filter_by(email=email).first()
        login_user(user)
    return redirect('/landing')
#bas
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
 
#bas
@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)
    email = profile['email']
    name = profile['name']
    # random_pass_len = random_pass_len = 8
    # password = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(random_pass_len))
    password = "12345678"
    user = Account.query.filter_by(email=email).first()
    if not user:

        picture = "static/img/avatar/"+str(random.randint(1, 16))+".png"
        new_user = Account(email=email, name=name,password=generate_password_hash(password, method='sha256'),avatar_url=picture,login_with ="facebook")
        db.session.add(new_user)
        db.session.commit()
        user = Account.query.filter_by(email=email).first()
        login_user(user)
    else:
        user = Account.query.filter_by(email=email).first()
        login_user(user)
    return redirect('/landing')



#bas
@app.route("/commu/data")
# @login_required
def commu_data():
    commu = Community.query.all()
    commu_data = list(map(lambda x: x.to_dict(), commu))
    # print(";;;;;;;;;;;;;",commu_data)
    for i in range(len(commu_data)):
        id_ = commu_data[i]["account_id"]
        x = Account.query.get(id_).to_dict()
        commu_data[i]["name_user"] = x["name"]
        commu_data[i]["avatar_url"] = x["avatar_url"]
    return jsonify(commu_data)

#bas
@app.route("/commu")
@login_required
def commu():
    return render_template("community.html")


#bas
@app.route("/<comment>",methods=('GET','POST'))
@login_required
def comment():
    if request.method == "POST":
        result = request.form.to_dict()
        commu_id = result.get('commu_id','')
        comment = Community.query.get(commu_id).to_dict()
        comment["img_user"] = current_user.avatar_url
        comment["user_name"] = current_user.name
    return render_template("comment.html",data = comment)

#bas
@app.route("/comment/data")
@login_required
def comment_data():
    comment = Comment.query.all()
    comment_data = list(map(lambda x: x.to_dict(), comment))
    # commu_id
    for i in range(len(comment_data)):
        # commu = Community.query.get(commu_id)
        accounts = Account.query.get(comment_data)
        comment_data[i]["user_img"] = accounts["avatar_url"]
        comment_data[i]["user_name"] = accounts["name"]
    return jsonify(comment_data)

#bas
@app.route("/delete/commu",methods=('GET','POST'))
@login_required
def delete_commu():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get('id', '')
        commu = History.query.get(id_)
        if history.account_id == current_user.id:
            commu = commu.share()
            db.session.commit()
        return commu_data()

#bas
@app.route("/edit/commu",methods=('GET','POST'))
@login_required
def edit_commu():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get('id', '')
        account_id = result.get('account_id', '')
        message = result.get('message', '')
        commu = Community.query.get(id_)
        if account_id == current_user.id:
            Community.edit(message)
            db.session.commit()
        return history_data()

#bas
@app.route("/history")
@login_required
def history():
    return render_template("history.html")

#bas
@app.route("/delete/history",methods=('GET','POST'))
@login_required
def delete_history():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get('id', '')
        account_id = result.get('account_id', '')
        history = History.query.get(id_)
        if history.account_id == current_user.id:
            history.remove_history(account_id)
            db.session.commit()
        return history_data()


#bas
@app.route("/history/data")
@login_required
def history_data():
    # history = History.query.get(current_user.id)
    # plant = PlantInfo.query.get(account_id)
    history = History.query.filter(History.account_id == current_user.id)
    history_data = list(map(lambda x: x.to_dict(), history))
    return jsonify(history_data)

#bas
@app.route("/comment/add")
@login_required
def comment_add():
    if request.method == "POST":
        result = request.form.to_dict()
        id_ = result.get('commu_id', '')
        message = result.get('message', '')
        # comment = Comment.query.get(id_)
        comment = Comment(commu_id=id_,message=message)
        db.session.add(comment)
        db.session.commit()
    return commu_data()