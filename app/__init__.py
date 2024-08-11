from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import EditProfileForm

app = Flask(__name__)  # Исправлено на __name__
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    return redirect(url_for('edit_profile'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Обработка данных формы
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Здесь можно обновить пользователя в базе данных (например, обновление username и email)

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html', form=form)

@app.route('/add_user')
def add_user():
    new_user = User(username='new_username')
    db.session.add(new_user)
    db.session.commit()
    return 'User added'

@app.route('/users')
def get_users():
    users = User.query.all()
    return str(users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)