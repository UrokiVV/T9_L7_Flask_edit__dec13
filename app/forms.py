from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        print(f'validate_username {username}')
        if user:
            print('*** ERROR: Такое имя уже существует !')
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        print(f'validate_email {email}')
        email = User.query.filter_by(email=email.data).first()
        if email:
            print('*** ERROR: Такая почта уже существует !')
            raise ValidationError('Такая почта уже используется')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')


class TestForm(FlaskForm):
    pole01 = StringField('Pole 01', validators=[DataRequired()])
    pole02 = StringField('Pole 02', validators=[DataRequired()])
    submit = SubmitField('Simple Test')

class TestDbForm(FlaskForm):
    submit = SubmitField('DB users')


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    # email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    email = StringField('Электронная почта', validators=[DataRequired() ])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        print(f'EditProfileForm init: username={original_username}, email={original_email} ')
