import os
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from database import db
from forms.register import UserForm
from forms.add_book import BookForm
from forms.login import Login
from models import User, Book

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'Khaled2351998'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)
Bootstrap(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/users', endpoint='users', methods=['GET', 'POST'])
def user():
    form = UserForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = 'photo.jpg'
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            image=filename
        )
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/add_book', endpoint='book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    form.user_id.choices = [(user.id, user.first_name) for user in User.query.all()]
    if form.validate_on_submit():
        image = form.image.data
        filename = '1.jpg'
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

        book = Book(
            name=form.name.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            appropriate=form.appropriate.data,
            image=filename,
            user_id=form.user_id.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_book.html', form=form)

@app.route('/user_detail/<int:id>', endpoint='user_detail')
def user_detail(id):
    my_user = User.query.get_or_404(id)
    return render_template('user_detail.html', my_user=my_user)

@app.route('/books/', endpoint='home')
def home():
    my_books = Book.query.all()
    return render_template('home.html', my_books=my_books)

@app.route('/books/<int:book_id>', endpoint='detail')
def detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('detail.html', book=book)

@app.route('/login', endpoint='login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)
@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'], endpoint='edit')
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)  # Fetch the book or return 404 if not found
    form = BookForm(obj=book)  # Pre-populate the form with the book's current data

    # Dynamically set the choices for the user_id field
    form.user_id.choices = [(user.id, user.first_name) for user in User.query.all()]

    if form.validate_on_submit():
        # Update the book's data from the form
        form.populate_obj(book)

        # Handle the image upload
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            book.image = filename  # Update the book's image filename

        db.session.commit()  # Save changes to the database
        flash('Book updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_book.html', form=form, book=book)

@app.route('/delete_book/<int:book_id>', methods=['GET','POST'], endpoint='delete_book')
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/logout', endpoint='logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)