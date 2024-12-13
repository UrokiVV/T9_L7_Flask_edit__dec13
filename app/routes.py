from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, EditProfileForm, TestForm, TestDbForm


@app.route('/')
@app.route('/home')
def home():
    print('home()')
    if current_user.is_authenticated:
        print(f'home(user=home, id={current_user.id}, email={current_user.email}  )')
        message = f"Рады вас видеть, {current_user.username} !"
    else:
        message = f"Добро пожаловать, уважаемый гость!"
    return render_template('home.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    print('register()')
    print('Request method:', request.method)
    print('Request form data:', request.form)

    form = RegistrationForm()
    if request.method == 'POST':
        print('register() in POST')
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!', 'success')
            print('Вы успешно зарегистрировались!')
            return redirect(url_for('login'))
        print('register(): ERROR - form not validated!')
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login()')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('login(): OK')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные.')
            print('login(): Введены неверные данные. Попробуйте ещё раз.')
    else:
        if request.method == 'POST':
            print('login(): ERROR: Введе ны ошибочные анные')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    print('logout_user')
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    print('account()')
    return render_template('account.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    print('Request method:', request.method)

    form = TestForm()
    print('test(): OK ')
    if current_user.is_authenticated:
        print(f'test(user={current_user.username}, id={current_user.id}, email={current_user.email}  )')

    print(f'test(): pole01 = {form.pole01.data}')
    print(f'test(): pole02 = {form.pole02.data}')
    print('Request method:', request.method)
    print('Request form data:', request.form)
    if request.method == 'POST':
        print('test(): method = POST ')
        if form.validate_on_submit():
            print('test(): OK ')
            print(f'test(): pole01 = {form.pole01.data}')
            print(f'test(): pole02 = {form.pole02.data}')
            message = "Данные успешно введены"
            #   return redirect(url_for('home'))
        else:
            print('*** ERROR test Not validated')
            print(form.errors)           #  вывод ошибок формы
            message = "*** ERROR: все поля должны быть заполнены"
    else:
        print('test(): method = GET ')
        message = "Введите данные"

    return render_template('test.html', form=form, message=message)


@app.route('/test_db', methods=['GET', 'POST'])
def test_db():
    print('test_db(): ')
    print('Request method:', request.method)
    print('Request form data:', request.form)
    message = ""

    form = TestDbForm()
    print('test_db(): begin ')
    if current_user.is_authenticated:
        print(f'test_db(user={current_user.username}, id={current_user.id}, email={current_user.email}  )')

    if request.method == 'POST':
        print('test_db(): method = POST ')
        message = "Первые 10 пользователей:"
        users = db.session.query(User).limit(10).all()
        for utst in users:
            s_utst=f" (id: {utst.id} , name:{utst.username},  email: {utst.email} ) "
            print(s_utst)
            message = message +s_utst
    else:
        message = "GET"
    return render_template('test_db.html', form=form, message=message)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = current_user.id
    print(f'edit_profile(): user_id={user_id} ')
    m_error = []
    message_err01 = ""
    message_err02 = ""

    user = User.query.get(user_id)
    if user is None:
        return redirect(url_for('home.html'))

    print(f'edit_profile()-2: user_id={user.id}. username={user.username}, user.email={user.email}')
    form = EditProfileForm(original_username=user.username, original_email=user.email)
    if request.method == 'POST':
        print('edit_profile(): method = POST ')
        username_new = form.username.data
        useremail_new = form.email.data
        password_new=form.password.data
        fl_new_name = False
        fl_new_email = False
        fl_err_user_new = False
        fl_err_email_new = False
        fl_err_except = False
        message = "begin-0"
        mess_bad_user = ""
        mess_bad_email = ""
        try:
            user_new = User.query.filter_by(username=username_new).first()

            # имя существует у другого пользователя
            if user_new != None and user_new != user:
                fl_err_user_new = True
                mess_bad_user = "Пользователь с таким именем уже есть в системе: "+username_new
                m_error.append(mess_bad_user)
            else:
                fl_new_name = True

            user_email_new = db.session.query(User).filter_by(email=useremail_new).first()
            # email существует у другого пользователя
            if user_email_new  != None and user_email_new  != user:
                fl_err_email_new = True
                mess_bad_email = "Пользователь с таким email уже есть в системе: " +useremail_new
                m_error.append(mess_bad_email)
            else:
                fl_new_email = True

        except:
            fl_err_except = True
            s_err = "except: *** Error ошибочные данные"
            m_error.append(s_err)
            print('4) edit_profile() ' +s_err)
            print(f"4A) except:  username_new = {username_new}" )
            print(f"4B) except:  useremail_new = {useremail_new}")

        if fl_err_user_new or fl_err_email_new or fl_err_except:
            n_err = 0
            for s_err in m_error:
                if n_err == 0:
                    message_err01 = s_err
                else:
                    message_err02 = s_err
                n_err += 1

            message = mess_bad_user +"; " +mess_bad_email
            print("==> edit_error.html: " +message)
            return render_template('edit_error.html',
                                   message_err01=message_err01, message_err02=message_err02)
        else:
            if form.validate_on_submit():
                print("validated OK")
                user_id = current_user.id
                user = User.query.get(user_id)
                user.username = form.username.data
                user.email = form.email.data
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password

                db.session.commit()

                print('All OK: edit_profile(): Ваши изменения сохранены.')
                message = "Ваши изменения сохранены"
                if fl_new_name:
                    message = message + " Имя =" +username_new
                if fl_new_email:
                    message = message + " email =" +useremail_new
                message = message +" (запомните новый пароль!) "

                form.username.data = user.username
                form.email.data = user.email
                form.password = hashed_password

                print(f'OK edit_profile(): {message}')
                return render_template('edit_ok.html', form=form, message=message)
            else:
                print('*** ERROR edit_profile() Not validated')
                message = "*** ERROR: ошибки в данных"
                # return render_template('home.html', message=message)
                return render_template('edit_error.html',
                                       message_err01=message, message_err02="")

    else:
        print('edit_profile(): method = GET ')
        message = "Введите данные для изменений. Все поля должны быть запонены!"

    print(message)
    print(f'edit_profile() ==> edit_profile.html : user_id={user_id}, username={user.username}, user.email={user.email}')
    return render_template('edit_profile.html', form=form)

