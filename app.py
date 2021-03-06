from flask import Flask, request, render_template, redirect, url_for
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from stableMatching import find_matches
import env
import smtplib




'''TODO: Need to import and setup MongoDB for database stuff,
Each mako page needs to be designed in a way that more closely represents our mockups
'''

app = Flask(__name__)

csrf = CsrfProtect()

csrf.init_app(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'testWinWin',
    'host': env.MONGO_URI
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = env.SECRET
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

# class RemoteUserMiddleware(object):
#     def __init__(self, app):
#         self.app = app
#     def __call__(self, environ, start_response):
#         user = environ.pop('HTTP_X_PROXY_REMOTE_USER', None)
#         environ['REMOTE_USER'] = user
#         return self.app(environ, start_response)
#
# app.wsgi_app = RemoteUserMiddleware(app.wsgi_app)


class User(UserMixin, db.Document):
    meta = {'collection': 'accounts'}
    name = db.StringField()
    email = db.StringField(max_length=30)
    password = db.StringField()
    all_classes = db.DictField()

class Groups(UserMixin, db.Document):
    meta = {'collection': 'groups'}
    group_id = db.IntField()
    members = db.ListField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class RegForm(FlaskForm):
    name = StringField('name',  validators=[InputRequired(), Length(max=30)])
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class LogInForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class DeleteForm(FlaskForm):
    toDelete = StringField('toDelete',  validators=[InputRequired(), Length(max=30)])

class classesForm(FlaskForm):
    classes = StringField('classes', validators=[InputRequired()])


def send_emails(to):
    try:
        gmail_user = env.GMAIL_USER
        gmail_password = env.GMAIL_PASS
        sent_from = gmail_user

        #email_text = "Did you get this??"
        email_text = 'Subject: {}\nTo: {}\n\n{}'.format("New Match with BU Study Group!", ", ".join(to), "Hey!\n\nHead over to www.bustudygroup.com to see a new match for one of your classes!\n\nHappy Finals!\n-BU Study Group Team")
        # email_text = """\
        # From: %s
        # To: %s     #
        # %s
        # """ % (sent_from, ", ".join(to), subject, body)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except Exception as e:
        print('Something went wrong...', e)

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LogInForm()
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return redirect(url_for('dashboard'))
        all_courses = []
        course_file = open("./static/data/courses.txt","r")
        contents = course_file.readlines()
        for line in contents:
            y = (" ".join(line.split(" ")[:2])).replace("\n", "")
            y = y[:6] + " " + y[6:9]
            all_courses.append(y)
        return render_template('home.html', form=form, classes=set(all_courses))
    else:
        check_user = User.objects(email=form.email.data).first()
        if check_user:
            if check_password_hash(check_user['password'], form.password.data):
                login_user(check_user)
                return redirect(url_for('dashboard'))
            return render_template('home.html', form=form, error="Incorrect password!")
        return render_template('home.html', form=form, error="Username doesn't exist!")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    else:
        if form.validate_on_submit():
            existing_email = User.objects(email=form.email.data).first()
            if existing_email is not None:
                return render_template('signup.html', form=form, error="Email taken")  # We should return a pop up error msg as well account taken
            else:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                newUser = User(name=form.name.data, email=form.email.data,password=hashpass, all_classes={}).save()
                login_user(newUser)
                return redirect(url_for('courseSelect'))
        return render_template('signup.html', form=form) #We should return a pop up error msg as well bad input

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = DeleteForm()
    if request.method == "GET":
        member_groups = list(current_user.all_classes.values())
        class_to_members = {}
        another_one = {}
        class_emails = {}
        for group in Groups.objects():
            if group.group_id in member_groups:
                class_to_members[group.group_id] = group.members
        classes = list(current_user.all_classes.keys())
        for c in classes:
            another_one[c] = class_to_members[current_user.all_classes[c]]
        return render_template('dashboard.html', user=current_user, classes = another_one.items(), form = form)
    else:
        remove = form.toDelete.data
        new_classes = current_user.all_classes
        id_of_group = current_user.all_classes[remove]
        curr_group = Groups.objects(group_id=id_of_group).first()
        curr_group.members.remove(current_user.email)
        Groups.objects(group_id=id_of_group).update_one(members=curr_group.members)
        del new_classes[remove]
        User.objects(email=current_user.email).update_one(all_classes=new_classes)
        return redirect(url_for('dashboard'))

@app.route("/faq")
def faq():
    return render_template('faq.html')

@app.route("/courseSelect", methods=['GET', 'POST'])
@login_required
def courseSelect():
    form = classesForm()
    toPassIn = ""
    for x in list(current_user.all_classes.keys()):
        toPassIn += "<p>"+ x +"</p>"
    if request.method == 'GET':
        return render_template('courseSelect.html', form=form, curr_classes=toPassIn)
    else:
        #Formatting hell but trust it works
        temp = form.classes.data.upper()
        if(" " not in temp):
            return render_template('courseSelect.html', form=form, curr_classes=toPassIn, error="Make sure the format is College *space* DeptCourseNumber")
        all_courses = []
        course_file = open("./static/data/courses.txt","r")
        contents = course_file.readlines()
        for line in contents:
            all_courses.append(" ".join(line.split(" ")[:2]))
        course_file.close()
        temp = temp.replace("<P>", ",")
        temp = temp.replace("</P>", ",")
        temp = temp.replace(",,", ",")
        temp = temp[1:]
        temp = temp[:-1]
        temp = temp.strip()
        temp = temp.split(",")
        temp = list(set(temp))
        for t in temp:
            if(t not in all_courses):
                return render_template('courseSelect.html', form=form, curr_classes=toPassIn, error="Course not found :( Check your formatting!")
        new_dict = current_user.all_classes
        for x in temp:
            if x not in new_dict:
                new_dict[x] = -1
        current_user.all_classes = new_dict
        current_user.save()
        all_students = []
        all_groups = {}
        get_users = User.objects()
        get_groups = Groups.objects()
        for g in get_users:
            all_students.append(g.to_mongo().to_dict())
        for d in get_groups:
            all_groups[d.group_id] = d.members
        s, g = find_matches(all_students, all_groups)
        for student in s:
            User.objects(email=student["email"]).update_one(all_classes=student["all_classes"])
        for group in g.keys():
            group_exists = Groups.objects(group_id=group).first()
            if group_exists:
                if group_exists.members != g[group] and len(g[group]) > 1:
                    send_emails(g[group])
                Groups.objects(group_id=group).update_one(members=g[group])
            else:
                Groups(group_id=group, members=g[group]).save()

        # for a in User.objects():
        #     print(a.name, a.email, a.all_classes)
        # for b in Groups.objects():
        #     print(b.group_id, b.members)
        return redirect(url_for('dashboard'))


@app.route("/feedback")
def feedback():
    return render_template('feedback.html')

@app.route("/debug")
def debug():
    return str(request.headers)

@app.route("/postAuth", methods=["POST"])
def postAuth():
    if request.methods == "POST":
        return "ayooooooo"


@app.route("/dlogin", methods=["POST"])
def dlogin():
    return str(request.environ)

# @app.route("/Shibboleth.sso/SAML2/POST", methods=['GET', 'POST'])
# def bad_code():
#     if request.method == "POST":
#         return str(request.environ)
#     else:
#         return "nope"

@app.route("/shibddebug")
def shibddebug():
    return str(request.headers)

@app.route("/jquery-1.11.2.min.js")
def jQueryFix():
    return render_template('jquery-1.11.2.min.js')

@app.route("/picker.js")
def pickerFix():
    return render_template('picker.js')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    form = RegForm()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
