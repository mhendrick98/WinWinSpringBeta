from flask import Flask, request, render_template
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



'''TODO: Need to import and setup MongoDB for database stuff,
Each mako page needs to be designed in a way that more closely represents our mockups
'''


app = Flask(__name__)

csrf = CsrfProtect()

csrf.init_app(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'testWinWin',
    'host': 'mongodb://localhost:27017/testWinWinBeta'
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = '_no_one_cared_til_i_put_on_the_mask_'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

class User(UserMixin, db.Document):
    meta = {'collection': 'accounts'}
    name = db.StringField()
    email = db.StringField(max_length=30)
    all_classes = db.StringField() # Ex: CS112,CS131, etc.
    is_matched = db.StringField() # Ex: 1,0,1,0 etc.
    member_groups = db.StringField() # Ex: 2342,12321,43435, etc.

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class RegForm(FlaskForm):
    name = StringField('name',  validators=[InputRequired(), Length(max=30)])
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])

class LogInForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Length(max=30)])

class classesForm(FlaskForm):
    classes = StringField('classes', validators=[InputRequired()])


@app.route("/", methods=['GET', 'POST'])
def home():
    form = LogInForm()
    if request.method == 'GET':
        if current_user.is_authenticated == True:
            return render_template('dashboard.html',user=current_user)
        return render_template('home.html', form=form)
    else:
        check_user = User.objects(username=form.username.data).first()
        if check_user:
            login_user(check_user)
            return render_template('dashboard.html', user=current_user)
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
                newUser = User(name=form.name.data, email=form.email.data, all_classes="",is_matched="", member_groups="").save()
                login_user(newUser)
                return render_template('courseSelect.html', form=classesForm())
        return render_template('signup.html', form=form) #We should return a pop up error msg as well bad input

@login_required
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route("/faq")
def faq():
    return render_template('faq.html')

@login_required
@app.route("/courseSelect", methods=['GET', 'POST'])
def courseSelect():
    form = classesForm()
    if request.method == 'GET':
        toPassIn = ""
        for x in current_user.all_classes.split(","):
            toPassIn += "<p>"+ x +"</p>"
        return render_template('courseSelect.html', form=form, curr_classes=toPassIn)
    else:
        #Formatting hell but trust it works
        temp = form.classes.data
        temp = temp.replace("<p>", ",")
        temp = temp.replace("</p>", ",")
        temp = temp.replace(",,", ",")
        temp = temp[1:]
        temp = temp[:-1]
        temp = temp.strip()
        temp = temp.split(",")
        temp = list(set(temp))
        temp = ",".join(temp)
        current_user.all_classes=temp
        current_user.save()
        return render_template('courseSelect.html', form=form, user=current_user)


@app.route("/feedback")
def feedback():
    return render_template('feedback.html')

@app.route("/jquery-1.11.2.min.js")
def jQueryFix():
    return render_template('jquery-1.11.2.min.js')

@app.route("/picker.js")
def pickerFix():
    return render_template('picker.js')

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    form = RegForm()
    return render_template('home.html', form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
