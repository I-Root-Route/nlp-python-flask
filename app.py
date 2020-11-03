from flask import Flask, render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from flaskext.markdown import Markdown
from db_system import db, app
from db_system.models import User
from db_system.forms import LoginForm, RegistrationForm, UserForm, ResetPasswordForm
from werkzeug.security import generate_password_hash

from nlp_pyfiles.processing import NLProcessing

Markdown(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=["GET", "POST"])
@login_required
def result():
    if request.method == "POST":
        data = request.form['text']
        nl = NLProcessing(data)
        text = nl.get_entities()
        en_ja = nl.translate_most_freq_words(nb_top=40)
        sentiments = nl.analyze_sentiment(threshold=0.4)
        nb_words = nl.get_nb_words()
        current_user.total_volume += nb_words
        db.session.commit()
        return render_template('result.html', text=text, en_ja=en_ja, sentiments=sentiments, nb_words=nb_words)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Log in Successfully')
            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('index')

            return redirect(next)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Thanks for registeration")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You Logged Out")
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Successfully Updated')
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', form=form, total_volume=current_user.total_volume)


@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Successfully Resetted')
            return redirect(url_for('account'))
    return render_template('reset_password.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
