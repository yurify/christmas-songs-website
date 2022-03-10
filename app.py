from threading import current_thread
from flask import Flask, render_template, redirect, url_for, flash
from flask.helpers import get_flashed_messages
from flask_login.utils import logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_manager, UserMixin, login_user, login_required, current_user
from forms import SignupForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_users.db'
app.config['SECRET_KEY'] = '************'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

playlist = db.Table('playlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE")),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id', ondelete="CASCADE")),
    db.PrimaryKeyConstraint('user_id', 'song_id')
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    songs = db.relationship('Song', secondary=playlist, backref=db.backref('subscribers', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String, unique=False, index=True)
    song_lyrics = db.Column(db.String, unique=False, index=True)
    song_url = db.Column(db.String, unique=False, index=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #subscribers

    def __repr__(self):
        return '<Song %r>' % self.song_title




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if logged in, then redirect to the account
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter(User.username == form.username.data).first() : # checking if this username already exists
            flash("Sorry, this username is already taken.")
            return redirect(url_for('signup'))
        elif User.query.filter(User.email == form.email.data).first() :
            flash("Sorry, this email is already used by another user.")
            return redirect(url_for('signup'))
        else:
            user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash("You have created an account successfully. You can now log in.")
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    # if logged in, then redirect to the account
    if current_user.is_authenticated:
        return redirect(url_for('account'))    

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('account'))
            else:
                flash("Incorrect password!")
            return redirect(url_for('login'))
        flash("No account with the username " + str(form.username.data))
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/song/<int:id>')
@login_required
def songer(id):
    song_to_show = Song.query.get_or_404(id)
    return render_template('song_page.html', song=song_to_show)

@app.route('/account/all_songs')
@login_required
def all_songs():
    songs_to_show = Song.query.all()
    return render_template('all_songs.html', songs=songs_to_show)


@app.route('/account/add_song/<int:id>')
@login_required
def add_song(id):
    sng = Song.query.get_or_404(id)
    sng.subscribers.append(current_user)
    db.session.commit()
    return redirect(url_for('all_songs'))


@app.route('/account/remove_song/<int:id>')
@login_required
def remove_song(id):
    sng= Song.query.get(id)
    current_user.songs.remove(sng)
    db.session.commit()
    return redirect(url_for('all_songs'))


@login_manager.unauthorized_handler
def unauthorized():
    return "You must log in to view this page."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# for testing purposes
# if __name__ == '__main__':
#     app.run(debug=True)


# Notes for the database management:
#
# >>> song1 = Song.query.get(1)
# >>> song1
# <User 'jingle bells'>
# >>> song2 = Song.query.get(2)
# >>> song2
# <User 'I wanna wish you a Merry Christmas'>
# >>> song3 = Song.query.get(3)
# >>> song3
# <User 'Silent night'>
# >>> user1 = User.query.get(1)
# >>> user1
# <User 'c'>
# >>> user2 = User.query.get(2)
# >>> user2
# <User 'b'>
# >>> song1.subscribers.append(user1)
# >>> song1.subscribers.append(user2) 
# >>> song2.subscribers.append(user1)
# >>> song3.subscribers.append(user1)
# >>> song1.subscribers.all()
# [<User 'c'>, <User 'b'>]
# >>> user1.songs
# [<User 'Silent night'>, <User 'jingle bells'>, <User 'I wanna wish you a Merry Christmas'>]
# db.session.commit()


