from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from . import db
from .models import User, Photo, Story, StoryPhoto, Comment, Like, Tag, Category


UPLOAD_FOLDER = 'static/uploads'


def register_routes(app):
    upload_folder = os.path.join(app.root_path, UPLOAD_FOLDER)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    app.config['UPLOAD_FOLDER'] = upload_folder

    @app.route('/')
    def index():
        stories = Story.query.order_by(Story.created_at.desc()).all()
        return render_template('index.html', stories=stories)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('register'))
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('Registration successful')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Invalid credentials')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload_photo():
        if request.method == 'POST':
            file = request.files['photo']
            if file:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                photo = Photo(
                    user_id=current_user.id,
                    filename=filename,
                    description=request.form.get('description'),
                    camera_model=request.form.get('camera_model'),
                    exposure_time=request.form.get('exposure_time'),
                )
                db.session.add(photo)
                db.session.commit()
                flash('Photo uploaded')
                return redirect(url_for('upload_photo'))
        return render_template('upload.html')

    @app.route('/create_story', methods=['GET', 'POST'])
    @login_required
    def create_story():
        if request.method == 'POST':
            title = request.form['title']
            description = request.form.get('description')
            visibility = request.form.get('visibility', 'public')
            story = Story(user_id=current_user.id, title=title, description=description, visibility=visibility)
            db.session.add(story)
            db.session.flush()
            photo_ids = request.form.getlist('photos')
            for order, pid in enumerate(photo_ids):
                assoc = StoryPhoto(story_id=story.id, photo_id=int(pid), order=order)
                db.session.add(assoc)
            db.session.commit()
            flash('Story created')
            return redirect(url_for('story_detail', story_id=story.id))
        photos = current_user.photos
        return render_template('create_story.html', photos=photos)

    @app.route('/story/<int:story_id>')
    def story_detail(story_id):
        story = Story.query.get_or_404(story_id)
        return render_template('story.html', story=story)

    @app.route('/story/<int:story_id>/comment', methods=['POST'])
    @login_required
    def comment_story(story_id):
        text = request.form['text']
        comment = Comment(user_id=current_user.id, story_id=story_id, text=text)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added')
        return redirect(url_for('story_detail', story_id=story_id))

    @app.route('/story/<int:story_id>/like')
    @login_required
    def like_story(story_id):
        if Like.query.filter_by(user_id=current_user.id, story_id=story_id).first():
            flash('Already liked')
        else:
            like = Like(user_id=current_user.id, story_id=story_id)
            db.session.add(like)
            db.session.commit()
            flash('Story liked')
        return redirect(url_for('story_detail', story_id=story_id))
