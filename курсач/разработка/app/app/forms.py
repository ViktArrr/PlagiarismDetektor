from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, BooleanField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class Login(Form):
	email=StringField('E-mail', validators=[Email(), DataRequired()])
	password=PasswordField('Пароль', validators=[DataRequired()])

class Student_registration(Form):
	nickname=StringField('Псевдоним', validators=[DataRequired()])
	password=PasswordField('Пароль', validators=[DataRequired()])
	email=StringField('E-mail', validators=[Email(), DataRequired()])
	name=StringField('Имя пользователя', validators=[DataRequired()])
	second_name=StringField('Фамилия пользователя', validators=[DataRequired()])
	thriiid_name=StringField('Отчество пользователя', validators=[DataRequired()])
	group=RadioField(validators=[DataRequired()],
        choices=[('Y2231', 'Y2231'), ('Y2232', 'Y2232'), ('Y2233', 'Y2233'), ('Y2234', 'Y2234'), ('Y2235', 'Y2235'), ('Y2236', 'Y2236'),
        ('Y2331', 'Y2331'), ('Y2332', 'Y2332'), ('Y2333', 'Y2333'), ('Y2334', 'Y2334'), ('Y2335', 'Y2335'), ('Y2336', 'Y2336'),
        ('Y2431', 'Y2431'), ('Y2432', 'Y2432'), ('Y2433', 'Y2433'), ('Y2434', 'Y2434'), ('Y2435', 'Y2435'), ('Y2436', 'Y2436')])

class Create(Form):
	name_lab=StringField('Название лабараторной', validators=[DataRequired()])
	description=TextAreaField('Что делать', validators=[DataRequired()])
	helpp=TextAreaField('Помощь в выполнении', validators=[DataRequired()])

class UploadForm(Form):
    image=FileField(u'Text File', validators=[DataRequired()])
    name_file=StringField('Название файла', validators=[DataRequired()])

class Student_modify(Form):
	email=StringField('Почта', validators=[DataRequired()])
	nickname=StringField('Псевдоним', validators=[DataRequired()])
	password=PasswordField('Пароль', validators=[DataRequired()])
	name=StringField('Имя пользователя', validators=[DataRequired()])
	second_name=StringField('Фамилия пользователя', validators=[DataRequired()])
	group=StringField('Номер группы пользователя', validators=[DataRequired()])
	thriiid_name=StringField('Отчество пользователя', validators=[DataRequired()])

class Teacher_modify(Form):
	email=StringField('Почта', validators=[DataRequired()])
	nickname=StringField('Псевдоним', validators=[DataRequired()])
	password=PasswordField('Пароль', validators=[DataRequired()])
	name=StringField('Имя пользователя', validators=[DataRequired()])
	second_name=StringField('Фамилия пользователя', validators=[DataRequired()])
	thriiid_name=StringField('Отчество пользователя', validators=[DataRequired()])

class Group(Form):
	number=StringField('№', validators=[DataRequired()])

class Admin_create(Form):
	email=StringField('E-mail', validators=[Email(), DataRequired()])
	nickname=StringField('Псевдоним', validators=[DataRequired()])
	password=PasswordField('Пароль', validators=[DataRequired()])
	name=StringField('Имя пользователя', validators=[DataRequired()])
	second_name=StringField('Фамилия пользователя', validators=[DataRequired()])
	thriiid_name=StringField('Отчество пользователя', validators=[DataRequired()])

class Admin_add(Form):
	predmets=StringField('Предмет', validators=[DataRequired()])
	group=StringField('Группа', validators=[DataRequired()])

class Comm(Form):
	comm=StringField('Комментарий', validators=[DataRequired()])

class Admin_modify(Form):
	email=StringField('Почта', validators=[DataRequired()])
	nickname=StringField('Псевдоним', validators=[DataRequired()])
	password=PasswordField('Пароль', validators=[DataRequired()])
	name=StringField('Имя пользователя', validators=[DataRequired()])
	second_name=StringField('Фамилия пользователя', validators=[DataRequired()])
	thriiid_name=StringField('Отчество пользователя', validators=[DataRequired()])