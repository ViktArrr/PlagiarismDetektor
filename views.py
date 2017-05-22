from flask import render_template, redirect, request, url_for, session
from app import app, db
from .forms import Login, Student_registration, Create, UploadForm, Student_modify, Teacher_modify, Group, Admin_create, Admin_add, Comm, Admin_modify
from app.models import User, Labs, Programs, Roles
from app.backend import tokenization, ngramm, metric, find
import os
from sqlalchemy import update

import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime

import plotly
plotly.tools.set_credentials_file(username='ViktorS', api_key='gk3itQcWHuFkAfuZleor')
import plotly.plotly as py
import plotly.graph_objs as go

# new!!!!!!
# from flask import make_response
# from functools import update_wrapper

# def nocache(f):
#     def new_func(*args, **kwards):
#         resp=make_response(f(*args, **kwards))
#         resp.cache_control.no_cache=True
#         resp.headers['Cache-Control']='no-cache'
#     return update_wrapper(new_func, f)

# логин(((((((((((((
# from flask_login import login_user, login_required, logout_user

# from flask_cachecontrol import FlaskCacheControl, dont_cache

array=['', '', '', '']

name_grafic=[15, 15, 15, 15]

# Возвращает базовый шаблон
@app.route('/')
def base():
    return render_template('base.html')

# Страница авторизации
@app.route('/login', methods=['GET','POST'])
def login():
    form_login=Login(request.form)
    if request.form and True:
        # Выбор авторизация или регистрация
        flag=True
        for i in request.form:
            if i=='reg':
                flag=False

        if flag:
            # Изъятие данных из форм
            email=form_login.email.data
            password=form_login.password.data
            nickname=form_login.email.data

            # Выборка пользователя из бд по почте
            select=User.query.filter_by(email=email).first()
            if select:
                # Проверка пароля
                if select.password==password:

                    '''
                    логин((((((((((((
                    # session['logged_in']=True
                    # user=User.query.filter_by(email=email).first()
                    # login_user(user)
                    '''

                    # Процесс авторизации
                    global array
                    array[0]=select.name
                    array[1]=select.second_name
                    array[2]=select.group
                    array[3]=select.id

                    # В зависимости от роли, подгрузка шаблона
                    if select.role=='student':
                        return redirect(url_for('profile_student'))
                    elif select.role=='teacher':    
                        return redirect(url_for('profile_teacher'))
                    elif select.role=='admin':
                        return redirect(url_for('profile_admin'))

                else:
                    return render_template('erorr_log.html',
                        text='Ошибка №1: Пользователя с такой почтой или псевдонимом не существует. Возможно, что пароль указан не верно.',
                        todo='Проверьте раскладку клавиатуры, клавишу Caps lock.',
                        path_to_back='http://localhost:5000/login')

            # Если пользователя нет в бд
            else:
                # Выбор пользователя из бд по псевдониму
                select=User.query.filter_by(nickname=nickname).first()
                if select:
                    # Проверка пароля
                    if select.password==password:

                        '''
                        логин((((((((((((
                        # session['logged_in']=True
                        # user=User.query.filter_by(email=email).first()
                        # login_user(user)
                        '''

                        # Процесс авторизации
                        global array
                        array[0]=select.name
                        array[1]=select.second_name
                        array[2]=select.group
                        array[3]=select.id

                        # В зависимости от роли, подгрузка шаблона
                        if select.role=='student':
                            return redirect(url_for('profile_student'))
                        elif select.role=='teacher':    
                            return redirect(url_for('profile_teacher'))
                        elif select.role=='admin':
                            return redirect(url_for('profile_admin'))

                    else:
                        return render_template('erorr_log.html',
                            text='Ошибка №1: Пользователя с такой почтой или псевдонимом не существует. Возможно, что пароль указан не верно.',
                            todo='Проверьте раскладку клавиатуры, клавишу Caps lock.',
                            path_to_back='http://localhost:5000/login')

                else:
                    return render_template('erorr_log.html',
                        text='Ошибка №1: Пользователя с такой почтой или псевдонимом не существует. Возможно, что пароль указан не верно.',
                        todo='Проверьте раскладку клавиатуры, клавишу Caps lock.',
                        path_to_back='http://localhost:5000/login')

        else:
            return redirect(url_for('registry_student'))

    return render_template('login.html',
        form=form_login,
        )

# Страница регистрации студента
@app.route('/registry_student', methods=['GET','POST'])
def registry_student():
    form_student=Student_registration(request.form)

    if request.form and True:
        # Изъятие данных из форм
        nickname=form_student.nickname.data
        password=form_student.password.data
        email=form_student.email.data
        name=form_student.name.data
        second_name=form_student.second_name.data
        thriiid_name=form_student.thriiid_name.data
        group=form_student.group.data

        # Поиск повторной почты в бд
        select=User.query.filter_by(email=email).first()

        # Проверка на заполнение полей
        if email=='' or password=='' or nickname=='' or name=='' or second_name=='' or thriiid_name=='' or group==None:
            return render_template('erorr_log.html',
                text='Ошибка №2: Не заполненно одно из полей.',
                todo='Заполните все поля, возможно вы что-то пропустили.',
                path_to_back='http://localhost:5000/registry_student')

        # Если почта уже существует в бд
        if select:
            return render_template('erorr_log.html',
                text='Ошибка №3: Этот пользователь уже существует.',
                todo='Возможно вы уже зарегистрированны, постарайтесь вспомнить свою прошлую учётную запись.',
                path_to_back='http://localhost:5000/registry_student')

        # Создание пользователя и возврат на страницу авторизации
        else:
            # Проверки на корректность данных почты
            count=0
            i=0
            flag=False
            while i<len(email):
                if email[i]==' ':
                    flag=True
                    break
                
                if email[i]=='@' and count==0:
                    count+=1
                
                if email[i]=='.' and count==1:
                    count+=1
                
                i+=1

            if count!=2:
                flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №4: Почта введена некорректно.',
                    todo='Проверьте расскладку клавиатуры, регистры букв и введите заного.',
                    path_to_back='http://localhost:5000/registry_student')

            # Проверка поля пароль на корректность
            if len(password)<=8:
                return render_template('erorr_log.html',
                    text='Ошибка №5: Пароль должен быть больше 8 символов.',
                    todo='Введите пароль состоящий из 8 и более символов.',
                    path_to_back='http://localhost:5000/registry_student')

            # Проверка логина на корректность
            flag=False
            for i in nickname:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №6: В псевдониме не должно быть пробелов.',
                    todo='Введите псевдоним состоящий из одного слова.',
                    path_to_back='http://localhost:5000/registry_student')

            # Проверка имени
            flag=False
            for i in name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №7: В имени не должно быть пробелов.',
                    todo='Если у вас состовное имя, введите его через дефиз.',
                    path_to_back='http://localhost:5000/registry_student')

            # Проверка фамилии
            flag=False
            for i in second_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №8: В фамилии не должно быть пробелов.',
                    todo='Если у вас составная фамилия, введите её через дефиз.',
                    path_to_back='http://localhost:5000/registry_student')

            # Проверка отчества
            flag=False
            for i in thriiid_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №9: В отчестве не должно быть пробелов.',
                    todo='Возможно вы случайно нажали пробел, попробуйте ввести заного.',
                    path_to_back='http://localhost:5000/registry_student')

            # Проверка группы
            if group==None or group=='None':
                return render_template('erorr_log.html',
                    text='Ошибка №10: Выберите группу.',
                    todo='Выберите пожалуйста вашу группу.',
                    path_to_back='http://localhost:5000/registry_student')

            # Проверка на существование такого же псевдонима
            select=User.query.filter_by(nickname=nickname).first()
            if select:
                return render_template('erorr_log.html',
                    text='Ошибка №11: Пользователь с таким псевдонимом уже существует.',
                    todo='Проверьте ввод псевдонима или постарайтесь вспомнить вашу прошлую учётную запись.',
                    path_to_back='http://localhost:5000/registry_student')

            # Создани пользователя в БД
            U=User(nickname=nickname, password=password, email=email, role='student', name=name, second_name=second_name, thriiid_name=thriiid_name, group=group, name_avatar='ava.png')
            db.session.add(U)
            db.session.commit()

            return render_template('happy_log.html',
                text='Поздравление №1: Вы успешно зарегистрированны.',
                path_to_back='http://localhost:5000/login')

    return render_template('registry_student.html',
        form=form_student
        )

# Для восстановления пароля
@app.route('/foggot_password', methods=['GET', 'POST'])
def foggot_password():

    return render_template('foggot_password.html')

'''
логин (((((((((((
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
'''

# Отображение профиля студента
# @dont_cache()
@app.route('/profile_student', methods=['GET','POST'])
def profile_student():
    global array

    # Выбор данных для статистики
    select=Programs.query.filter_by(who_upload=array[3]).all()
    
    if select:
        count_prog=0
        percent_all=0
        percent_last=''
        id_max=0
        for i in select:
            count_prog+=1
            percent_all+=float(i.percent[:-1])

            if i.id>id_max:
                id_max=i.id

        percent_all/=count_prog
        select=Programs.query.filter_by(id=id_max).first()
        percent_last=select.percent

    else:
        count_prog=0
        percent_all='-'
        percent_last='-'

    # Данные для графика
    percent=[]
    name_file=[]
    select=Programs.query.filter_by(who_upload=array[3]).all()
    
    for j in select:
        percent.append(j.percent)
        name_file.append(j.name_file)

    # График
    trace=go.Bar(x=name_file, y=percent)
    data=[trace]
    layout=go.Layout(title='Процент плагиата моих программ', width=1000, height=600)
    fig=go.Figure(data=data, layout=layout)

    global name_grafic
    name_grafic[0]+=1
    temp='app/static/grafics/grf_prof_stud_'+str(name_grafic[0])+'.png'
    py.image.save_as(fig, filename=temp)
    # py.image.save_as(fig, filename='app/static/grafics/grf_prof_stud_1.png')

    # Выбор данных для отображения в профиле
    select=User.query.filter_by(id=array[3]).first()
    
    # Костыль для графиеков
    template='''
    {% extends "base.html" %}
    {% block content %}


    <a href='http://localhost:5000/login'>
    '''+'''<img src="{{url_for('static', filename='Close-button1.png')}}" height='40px' width='40px' align='right'><br>'''+''''
    </a>
    <table width='70%' align='center'>
        <tr>
            <td valign='top' rowspan='3'>
                <div class='showchange' align='center'>
                '''+'''<img class='img-circle' src="{{url_for('static', filename='Ava.png')}}">'''+'''
                </div>
            </td>
            <td valign='top' colspan='2'>
                <div id='text3'>
                    <h3>
                    '''+'''{{second_name}}
                    {{name}}
                    {{thriiid_name}}<br>'''+'''
                    </h3>
                </div>
            </td>
        </tr>
        <tr>
            <td valign='top'>
                <div id='text4' style='font-size: 20px;'>
                    Information:
                </div>
                <div id='text5' style='font-size: 20px;'>
                    '''+'''{{group}}'''+'''
                </div>
            </td>
        </tr>
        <tr>
            <td valign='top'>
                <table>
                    <tr>
                        <td>
                            <a href='http://localhost:5000/razdel'>
                                <button class="btn btn-green" type="button" value='Submit' style='float: left;'>Upload programm</button>
                            </a>
                        </td>
                        <td>
                            <a href='http://localhost:5000/modify_student'>
                                <button class="btn-orange" type="button" value='Submit' style='float: left;'>Change profile</button>
                            </a>
                        </td>
                        <td>
                            <a href='http://localhost:5000/student_uploads'>
                                <button class="btn-blue" type="button" value='Submit' style='float: left;'>My uploads</button>           
                            </a>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td colspan='2'>
                <div id='text3'>
                    <br>
                    Count uploads programm:
                    '''+'''{{ count_prog }}'''+'''
                </div>
            </td>
        </tr>
        <tr>
            <td colspan='2'>
                <div id='text3'>
                    Total percentage of plagiarism:
                    '''+'''{{ percent_all }}'''+'''
                </div>
            </td>
        </tr>
        <tr>
            <td colspan='2'>
                <div id='text3'>
                    Last programm:
                    '''+'''{{ percent_last }}'''+'''
                </div>
            </td>
        </tr>
        <tr>
            <td colspan='3'>
                <br>
                <div align='center'>
                '''+'''<img src={{url_for('static', filename='grafics/grf_prof_stud_'''+str(name_grafic[0])+'''.png')}}>'''+'''
                </div>
            </td>
        </tr>
    </table>

    {% endblock %}
    '''

    f=open('app/templates/profile_student_'+str(name_grafic[0])+'.html', 'w')
    f.write(template)
    f.close()

    return render_template('profile_student_'+str(name_grafic[0])+'.html',
        name=select.name,
        second_name=select.second_name,
        thriiid_name=select.thriiid_name,
        group=select.group,
        count_prog=count_prog,
        percent_all=percent_all,
        percent_last=percent_last
        )

# Отображение профиля преподавателя
@app.route('/profile_teacher', methods=['GET','POST'])
def profile_teacher():
    # Данные для графика
    select=Programs.query.filter_by().all()
    date=[]
    for i in select:
        temp=''
        j=0

        while i.date[j]!=' ':
            temp+=i.date[j]
            j+=1
        date.append(temp)

    datete=['2017-01-01', '2017-01-02', '2017-01-03', '2017-01-04', '2017-01-05', '2017-01-06', '2017-01-07', '2017-01-08', '2017-01-09', '2017-01-10', '2017-01-11', 
    '2017-01-12', '2017-01-13', '2017-01-14', '2017-01-15', '2017-01-16', '2017-01-17', '2017-01-18', '2017-01-19', '2017-01-20', '2017-01-21', '2017-01-22', '2017-01-23', 
    '2017-01-24', '2017-01-25', '2017-01-26', '2017-01-27', '2017-01-28', '2017-01-29', '2017-01-30', '2017-01-31',
    '2017-02-01', '2017-02-02', '2017-02-03', '2017-02-04', '2017-02-05', '2017-02-06', '2017-02-07', '2017-02-08', '2017-02-09', '2017-02-10', '2017-02-11', 
    '2017-02-12', '2017-02-13', '2017-02-14', '2017-02-15', '2017-02-16', '2017-02-17', '2017-02-18', '2017-02-19', '2017-02-20', '2017-02-21', '2017-02-22', '2017-02-23', 
    '2017-02-24', '2017-02-25', '2017-02-26', '2017-02-27', '2017-02-28', '2017-02-29', '2017-02-30', '2017-02-31', 
    '2017-03-01', '2017-03-02', '2017-03-03', '2017-03-04', '2017-03-05', '2017-03-06', '2017-03-07', '2017-03-08', '2017-03-09', '2017-03-10', '2017-03-11', 
    '2017-03-12', '2017-03-13', '2017-03-14', '2017-03-15', '2017-03-16', '2017-03-17', '2017-03-18', '2017-03-19', '2017-03-20', '2017-03-21', '2017-03-22', '2017-03-23', 
    '2017-03-24', '2017-03-25', '2017-03-26', '2017-03-27', '2017-03-28', '2017-03-29', '2017-03-30', '2017-03-31', 
    '2017-04-01', '2017-04-02', '2017-04-03', '2017-04-04', '2017-04-05', '2017-04-06', '2017-04-07', '2017-04-08', '2017-04-09', '2017-04-10', '2017-04-11', 
    '2017-04-12', '2017-04-13', '2017-04-14', '2017-04-15', '2017-04-16', '2017-04-17', '2017-04-18', '2017-04-19', '2017-04-20', '2017-04-21', '2017-04-22', '2017-04-23', 
    '2017-04-24', '2017-04-25', '2017-04-26', '2017-04-27', '2017-04-28', '2017-04-29', '2017-04-30', '2017-04-31', 
    '2017-05-01', '2017-05-02', '2017-05-03', '2017-05-04', '2017-05-05', '2017-05-06', '2017-05-07', '2017-05-08', '2017-05-09', '2017-05-10', '2017-05-11', 
    '2017-05-12', '2017-05-13', '2017-05-14', '2017-05-15', '2017-05-16', '2017-05-17', '2017-05-18', '2017-05-19', '2017-05-20', '2017-05-21', '2017-05-22', '2017-05-23', 
    '2017-05-24', '2017-05-25', '2017-05-26', '2017-05-27', '2017-05-28', '2017-05-29', '2017-05-30', '2017-05-31', 
    '2017-06-01', '2017-06-02', '2017-06-03', '2017-06-04', '2017-06-05', '2017-06-06', '2017-06-07', '2017-06-08', '2017-06-09', '2017-06-10', '2017-06-11', 
    '2017-06-12', '2017-06-13', '2017-06-14', '2017-06-15', '2017-06-16', '2017-06-17', '2017-06-18', '2017-06-19', '2017-06-20', '2017-06-21', '2017-06-22', '2017-06-23', 
    '2017-06-24', '2017-06-25', '2017-06-26', '2017-06-27', '2017-06-28', '2017-06-29', '2017-06-30', '2017-06-31',
    '2017-07-01', '2017-07-02', '2017-07-03', '2017-07-04', '2017-07-05', '2017-07-06', '2017-07-07', '2017-07-08', '2017-07-09', '2017-07-10', '2017-07-11', 
    '2017-07-12', '2017-07-13', '2017-07-14', '2017-07-15', '2017-07-16', '2017-07-17', '2017-07-18', '2017-07-19', '2017-07-20', '2017-07-21', '2017-07-22', '2017-07-23', 
    '2017-07-24', '2017-07-25', '2017-07-26', '2017-07-27', '2017-07-28', '2017-07-29', '2017-07-30', '2017-07-31', 
    '2017-08-01', '2017-08-02', '2017-08-03', '2017-08-04', '2017-08-05', '2017-08-06', '2017-08-07', '2017-08-08', '2017-08-09', '2017-08-10', '2017-08-11', 
    '2017-08-12', '2017-08-13', '2017-08-14', '2017-08-15', '2017-08-16', '2017-08-17', '2017-08-18', '2017-08-19', '2017-08-20', '2017-08-21', '2017-08-22', '2017-08-23', 
    '2017-08-24', '2017-08-25', '2017-08-26', '2017-08-27', '2017-08-28', '2017-08-29', '2017-08-30', '2017-08-31', 
    '2017-09-01', '2017-09-02', '2017-09-03', '2017-09-04', '2017-09-05', '2017-09-06', '2017-09-07', '2017-09-08', '2017-09-09', '2017-09-10', '2017-09-11', 
    '2017-09-12', '2017-09-13', '2017-09-14', '2017-09-15', '2017-09-16', '2017-09-17', '2017-09-18', '2017-09-19', '2017-09-20', '2017-09-21', '2017-09-22', '2017-09-23', 
    '2017-09-24', '2017-09-25', '2017-09-26', '2017-09-27', '2017-09-28', '2017-09-29', '2017-09-30', '2017-09-31', 
    '2017-10-01', '2017-10-02', '2017-10-03', '2017-10-04', '2017-10-05', '2017-10-06', '2017-10-07', '2017-10-08', '2017-10-09', '2017-10-10', '2017-10-11', 
    '2017-10-12', '2017-10-13', '2017-10-14', '2017-10-15', '2017-10-16', '2017-10-17', '2017-10-18', '2017-10-19', '2017-10-20', '2017-10-21', '2017-10-22', '2017-10-23', 
    '2017-10-24', '2017-10-25', '2017-10-26', '2017-10-27', '2017-10-28', '2017-10-29', '2017-10-30', '2017-10-31', 
    '2017-11-01', '2017-11-02', '2017-11-03', '2017-11-04', '2017-11-05', '2017-11-06', '2017-11-07', '2017-11-08', '2017-11-09', '2017-11-10', '2017-11-11', 
    '2017-11-12', '2017-11-13', '2017-11-14', '2017-11-15', '2017-11-16', '2017-11-17', '2017-11-18', '2017-11-19', '2017-11-20', '2017-11-21', '2017-11-22', '2017-11-23', 
    '2017-11-24', '2017-11-25', '2017-11-26', '2017-11-27', '2017-11-28', '2017-11-29', '2017-11-30', '2017-11-31', 
    '2017-12-01', '2017-12-02', '2017-12-03', '2017-12-04', '2017-12-05', '2017-12-06', '2017-12-07', '2017-12-08', '2017-12-09', '2017-12-10', '2017-12-11', 
    '2017-12-12', '2017-12-13', '2017-12-14', '2017-12-15', '2017-12-16', '2017-12-17', '2017-12-18', '2017-12-19', '2017-12-20', '2017-12-21', '2017-12-22', '2017-12-23', 
    '2017-12-24', '2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28', '2017-12-29', '2017-12-30', '2017-12-31']

    soso=[]
    for i in datete:
        count=0
        for j in date:
            if i==j:
                count+=1
        soso.append(count)

    # График
    trace=go.Scatter(x=datete, y=soso)
    data=[trace]
    layout=go.Layout(title='Количество загруженных программ', width=1000, height=600)
    fig=go.Figure(data=data, layout=layout)

    global name_grafic
    name_grafic[1]+=1
    temp='app/static/grafics/grf_prof_teach_'+str(name_grafic[1])+'.png'
    py.image.save_as(fig, filename=temp)

    select=User.query.filter_by(id=array[3]).first()

    # Костыль для графиеков
    template='''
    {% extends "base.html" %}
    {% block content %}

    <a href='http://localhost:5000/login'>
        '''+'''<img src="{{url_for('static', filename='Close-button1.png')}}" height='40px' width='40px' align='right'><br>'''+'''
    </a>

    <table width='70%' align='center'>
        <tr>
            <td valign='top' rowspan='3'>
                <div class='showchange' align='center'>
                    '''+'''<img class='img-circle' src="{{url_for('static', filename='Ava.png')}}">'''+'''
                </div>
            </td>
            <td valign='top' colspan='2'>
                <div id='text3'>
                    <h3>
                    '''+'''
                        {{second_name}}
                        {{name}}
                        {{thriiid_name}}<br>'''+'''
                    </h3>
                </div>
            </td>
        </tr>
        <tr>
            <td valign='top'>
                <div id='text4' style='font-size: 20px;'>
                    Information
                </div>
                <div id='text5' style='font-size: 17px;'>
                '''+'''
                    {{group}}<br>
                    {{predmet}}<br>'''+'''
                </div>
            </td>
        <tr>
            <td>
                <table>
                    <tr>
                        <td>
                            <a href='http://localhost:5000/create_razdel'>
                                <button class="btn btn-green" type="button" value='Submit' style='float: left;'>Create lab</button>
                            </a>
                        </td>
                        <td>
                            <a href='http://localhost:5000/modify_teacher'>
                                <button class="btn" type="button" value='Submit' style='float: left;'>Change profile</button>
                            </a>
                        </td>
                        <td>
                            <a href='http://localhost:5000/groups'>
                                <button class="btn-orange" type="button" value='Submit' style='float: left;'>Predmets info</button>
                            </a>
                        </td>
                        <td>
                            <a href='http://localhost:5000/Comment'>
                                <button class="btn-blue" type="button" value='Submit' style='float: left;'>Student info</button>
                            </a>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td colspan='3'>
                <br>
                <div align='center'>
                '''+'''
                    <img src={{url_for('static', filename='grafics/grf_prof_teach_'''+str(name_grafic[1])+'''.png')}}>'''+'''
                </div>
            </td>
        </tr>
    </table>
    </div>

    {% endblock %}
    '''

    f=open('app/templates/profile_teacher_'+str(name_grafic[1])+'.html', 'w')
    f.write(template)
    f.close()

    return render_template('profile_teacher_'+str(name_grafic[1])+'.html',
        name=select.name,
        second_name=select.second_name,
        thriiid_name=select.thriiid_name,
        group=select.group,
        predmet=select.predmet
        )

# Отображение профиля админинстратора
@app.route('/profile_admin', methods=['GET', 'POST'])
def profile_admin():
    # Выбор уже сушествующих преподавателей для дальнейшего отображения
    select=User.query.filter_by(role='teacher').all()

    # Поиск всех созданных преподавателей
    fio=[]
    groups=[]
    predmets=[]
    idd=[]
    for i in select:
        idd.append(i.id)
        temp=''
        temp+=i.second_name
        temp+=' '
        temp+=i.name
        temp+=' '
        temp+=i.thriiid_name
        fio.append(temp)
        groups.append(i.group)
        predmets.append(i.predmet)
    count=len(select)

    # Объявление форм
    form_admin_add=Admin_add(request.form)
    form_admin_create=Admin_create(request.form)

    if request.form and True:
        # Действие на удаление преподавателя
        for i in request.form:
            if i[0]=='D' and i[1]=='E' and i[2]=='L':
                idd=''
                for j in range(4, len(i)):
                    if i[j]!=' ':
                        idd+=i[j]
                    else:
                        break

                # Выбор имени и фамилии для пути
                temp=''
                for j in range(4, len(i)):
                    temp+=i[j]
                path='app/upload_file/'+temp

                select=User.query.filter_by(id=idd).first()

                # пишет что нет прав-----------------------------------------------------------------------------------------------------
                # os.remove(path)
                db.session.delete(select)
                db.session.commit()

                return render_template('happy_log.html',
                    text='Поздравление №2: Преподаватель успешно удалён.',
                    path_to_back='http://localhost:5000/profile_admin')

        # Обработка действий над предметом
        if 'predmets' in request.form:
            # Выбор действие удаления или же добавление
            flag=True
            for i in request.form:
                if i[0]=='d' and i[1]=='e' and i[2]=='l' and i[3]=='e' and i[4]=='t' and i[5]=='e' and i[6]==' ':
                    flag=False

            # Добавление предмета
            if flag:
                predmets=form_admin_add.predmets.data
                
                # Проверка на существование предмета
                if predmets=='':
                    return render_template('erorr_log.html',
                        text='Ошибка №12: Имя предмета не указано.',
                        todo='Введите название предмета.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка корректности названия предмета
                flag=False
                for i in predmets:
                    if i==' ':
                        flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №13: Имя предмета указанно не корректно.',
                        todo='Введите название предмета без проблеов, можете использовать символ "_".',
                        path_to_back='http://localhost:5000/profile_admin')

                # Выбор имени преподавателя
                for i in request.form:
                    if i!='predmets':
                        temp=i
                idd=''
                for i in range(len(temp)):
                    if temp[i]!=' ':
                        idd+=temp[i]
                    else:
                        break

                # Проверка, добавлен ли уже этот предмет
                flag=False
                select=User.query.filter_by(id=idd).first()
                predmetsss=[]
                temp=''

                if select.predmet!=None:
                    for i in select.predmet:
                        if i==' ':
                            predmetsss.append(temp)
                            temp=''
                        else:
                            temp+=i
                    predmetsss.append(temp)
                else:
                    predmetsss.append('')

                if predmets in predmetsss:
                    flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №14: Предмет уже создан.',
                        todo='Введите новый предмет.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Выбора преподавателя из бд
                select=User.query.filter_by(id=idd).first()
                bucket=select.predmet
                if bucket!=None:
                    bucket+=' '
                    bucket+=predmets
                else:
                    bucket=predmets
                
                select=User.query.filter_by(id=idd).first()
                temp=''
                temp+=select.second_name+' '+select.name+' '+select.thriiid_name

                # Добавление предмета в бд и создание папки
                path='app/upload_file/'+temp+'/'+predmets
                db.session.query(User).filter_by(id=idd).update({'predmet':bucket})
                db.session.commit()
                os.mkdir(path)

                return render_template('happy_log.html',
                    text='Поздравление №3: Предмет успешно добавлен.',
                    path_to_back='http://localhost:5000/profile_admin')

            # Удаление предмета
            else:
                predmets=form_admin_add.predmets.data

                if predmets=='':
                    return render_template('erorr_log.html',
                        text='Ошибка №15: Имя предмета не указано.',
                        todo='Введите имя предмета которое надо удалить.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Выбор фамилии преподавателя
                for i in request.form:
                    if i!='predmets':
                        temp=i
                idd=''
                for i in range(7, len(temp)):
                    if temp[i]!=' ':
                        idd+=temp[i]
                    else:
                        break

                # Выбор предмета из бд
                select=User.query.filter_by(id=idd).first()
                bucket=[]
                list=select.predmet
                predmet_name=''
                for i in range(len(list)):
                    if list[i]==' ':
                        bucket.append(predmet_name)
                        predmet_name=''
                        continue
                    else:
                        predmet_name+=list[i]
                bucket.append(predmet_name)

                list=''
                count=1
                if bucket[0]!=predmets:
                    list+=bucket[0]
                else:
                    count=2
                    list+=bucket[1]
                for i in range(count, len(bucket)):
                    if bucket[i]==predmets:
                        continue
                    else:
                        list+=' '
                        list+=bucket[i]

                db.session.query(User).filter_by(id=idd).update({'predmet':list})
                db.session.commit()
                path='app/upload_file/'+select.second_name+' '+select.name+' '+select.thriiid_name+'/'+predmets
                # отказ в доступе--------------------------------------------------------------------------------------------------------------
                # os.remove(path)

                return render_template('happy_log.html',
                    text='Поздравление №4: Предмет успешно удалён.',
                    path_to_back='http://localhost:5000/profile_admin')

        # Обработка действий над группой
        elif 'group' in request.form:
            # Выбор удаление или же добавление
            flag=True
            for i in request.form:
                if i[0]=='d' and i[1]=='e' and i[2]=='l' and i[3]=='e' and i[4]=='t' and i[5]=='e' and i[6]==' ':
                    flag=False

            # Добавление
            if flag:
                group=form_admin_add.group.data

                # Проверка на ввод группы
                if group=='':
                    return render_template('erorr_log.html',
                        text='Ошибка №16: Группа не указана.',
                        todo='Введите группу которую надо добавить.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка на корректность ввода группы
                flag=False
                if group not in ['Y2231', 'Y2232', 'Y2233', 'Y2234', 'Y2235', 'Y2236',
                                'Y2331', 'Y2332', 'Y2333', 'Y2334', 'Y2335', 'Y2336',
                                'Y2431', 'Y2432', 'Y2433', 'Y2434', 'Y2435', 'Y2436']:
                    flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №17: Группа указана не верно.',
                        todo='Значение регистров имеет значение, введите используя клавишу Caps lock.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Имя преподавателя
                for i in request.form:
                    if i!='group':
                        temp=i
                idd=''
                for i in range(len(temp)):
                    if temp[i]!=' ':
                        idd+=temp[i]
                    else:
                        break

                # Проверка на существование данной группы
                flag=False
                select=User.query.filter_by(id=idd).first()
                groups=[]
                temp=''

                if select.group!=None:
                    for i in select.group:
                        if i==' ':
                            groups.append(temp)
                            temp=''
                        else:
                            temp+=i
                    groups.append(temp)
                else:
                    groups.append('')

                if group in groups:
                    flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №18: Группа уже прикрепленна.',
                        todo='Введите новую группу для добавления или выберите другой предмет.',
                        path_to_back='http://localhost:5000/profile_admin')

                # добавление группы
                select=User.query.filter_by(id=idd).first()
                bucket=select.group
                if bucket!=None:
                    bucket+=' '
                    bucket+=group
                else:
                    bucket=group

                db.session.query(User).filter_by(id=idd).update({'group':bucket})
                db.session.commit()

                return render_template('happy_log.html',
                    text='Поздравление №5: Группа успешно прикрепленна.',
                    path_to_back='http://localhost:5000/profile_admin')

            # Удаление группы
            else:
                group=form_admin_add.group.data

                if group=='':
                    return render_template('erorr_log.html',
                        text='Ошибка №19: Имя группы не указано.',
                        todo='Введите название группы которую надо удалить.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Выбор айди преподавателя
                for i in request.form:
                    if i!='group':
                        temp=i
                idd=''
                for i in range(7, len(temp)):
                    if temp[i]!=' ':
                        idd+=temp[i]
                    else:
                        break

                select=User.query.filter_by(id=idd).first()
                bucket=[]
                list=select.group
                group_name=''
                for i in range(len(list)):
                    if list[i]==' ':
                        bucket.append(group_name)
                        group_name=''
                        continue
                    else:
                        group_name+=list[i]
                bucket.append(group_name)

                list=''
                count=1
                if bucket[0]==group:
                    list=''
                else:
                    if bucket[0]!=group:
                        list+=bucket[0]
                    else:
                        count=2
                        list+=bucket[1]
                    for i in range(count, len(bucket)):
                        if bucket[i]==group:
                            continue
                        else:
                            list+=' '
                            list+=bucket[i]

                db.session.query(User).filter_by(id=idd).update({'group':list})
                db.session.commit()
                
                return render_template('happy_log.html',
                    text='Поздравление №6: Группа успешно удаленна.',
                    path_to_back='http://localhost:5000/profile_admin')

        # Обработка действий над добавлением преподавателя
        else:
            email=form_admin_create.email.data
            password=form_admin_create.password.data
            nickname=form_admin_create.nickname.data
            name=form_admin_create.name.data
            second_name=form_admin_create.second_name.data
            thriiid_name=form_admin_create.thriiid_name.data
            
            if email=='' or password=='' or name=='' or second_name=='' or thriiid_name=='' or nickname=='':
                return render_template('erorr_log.html',
                    text='Ошибка №2: Не заполненно одно из полей.',
                    todo='Возможно вы пропустили одно из полей, повторите ввод.',
                    path_to_back='http://localhost:5000/profile_admin')

            select=User.query.filter_by(email=email).first()
            if select:
                return render_template('erorr_log.html',
                    text='Ошибка №3: Этот пользователь уже существует.',
                    todo='Вспомнить свой прошлый профиль или же повторите ввод.',
                    path_to_back='http://localhost:5000/profile_admin')
            
            else:
                # Проверки на корректность данных почты
                count=0
                i=0
                flag=False
                while i<len(email):
                    if email[i]==' ':
                        flag=True
                        break
                    
                    if email[i]=='@' and count==0:
                        count+=1
                    
                    if email[i]=='.' and count==1:
                        count+=1
                    
                    i+=1

                if count!=2:
                    flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №4: Почта введена некорректно.',
                        todo='Проверьте раскладку клавиатуры и регистры и повторите ввод.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка поля пароль на корректность
                if len(password)<=8:
                    return render_template('erorr_log.html',
                        text='Ошибка №5: Пароль должен быть больше 8 символов.',
                        todo='Введите 8 или более символов.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка логина на корректность
                flag=False
                for i in nickname:
                    if i==' ':
                        flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №6: В псевдониме не должно быть пробелов.',
                        todo='Введите псевдоним состоящий из одного слова.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка имени
                flag=False
                for i in name:
                    if i==' ':
                        flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №7: В имени не должно быть пробелов.',
                        todo='Если у вас состовное имя, то используйте дефиз.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка фамилии
                flag=False
                for i in second_name:
                    if i==' ':
                        flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №8: В фамилии не должно быть пробелов.',
                        todo='Если у вас оставная фамилия то используйте дефиз.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка отчества
                flag=False
                for i in thriiid_name:
                    if i==' ':
                        flag=True

                if flag:
                    return render_template('erorr_log.html',
                        text='Ошибка №9: В отчестве не должно быть пробелов.',
                        todo='Возможно вы случайно нажали пробле, повторите ввод.',
                        path_to_back='http://localhost:5000/profile_admin')

                # Проверка на существование такого же псевдонима
                select=User.query.filter_by(nickname=nickname).first()
                if select:
                    return render_template('erorr_log.html',
                        text='Ошибка №11: Пользователь с таким псевдонимом уже существует.',
                        todo='Постарайтесь вспомнить свою прошлую учётную запись.',
                        path_to_back='http://localhost:5000/profile_admin')

                U=User(nickname=nickname, password=password, email=email, role='teacher', name=name, second_name=second_name, thriiid_name=thriiid_name, name_avatar='ava.png')
                db.session.add(U)
                db.session.commit()

                # Создание папки этого преподавателя для создания в ней разделов
                path='app/upload_file/'+second_name+' '+name+' '+thriiid_name
                os.mkdir(path)

                return render_template('happy_log.html',
                    text='Поздравление №7: Преподаватель успешно создан.',
                    path_to_back='http://localhost:5000/profile_admin')

    select1=Roles.query.filter_by(id=1).first()
    select2=Roles.query.filter_by(id=2).first()
    select3=Roles.query.filter_by(id=3).first()

    # Выбор данных для профиля администратора
    select=User.query.filter_by(id=array[3]).first()

    return render_template('profile_admin.html',
        name=select.name,
        second_name=select.second_name,
        thriiid_name=select.thriiid_name,
        fios=fio,
        predmets=predmets,
        groups=groups,
        len=count,
        form_add=form_admin_add,
        form_create=form_admin_create,
        select1=select1.description,
        select2=select2.description,
        select3=select3.description,
        idd=idd
        )

# Редактирование данных студента
@app.route('/modify_student', methods=['GET', 'POST'])
def modify_student():
    global array

    # Достаём старые данные студента
    select=User.query.filter_by(id=array[3]).first()
    nickname=select.nickname
    password=select.password
    name=select.name
    second_name=select.second_name
    group=select.group
    thriiid_name=select.thriiid_name
    email=select.email

    # Объявление формы
    form_mod_stud=Student_modify(request.form)

    if request.form and True:
        # Получаем новые данные
        nickname=form_mod_stud.nickname.data
        password=form_mod_stud.password.data
        name=form_mod_stud.name.data
        second_name=form_mod_stud.second_name.data
        group=form_mod_stud.group.data
        thriiid_name=form_mod_stud.thriiid_name.data
        email=form_mod_stud.email.data

        # Проверка на пустые данные
        if len(nickname)==0 and len(password)==0 and len(name)==0 and len(second_name)==0 and len(group)==0 and len(thriiid_name)==0 and len(email)==0:
            return render_template('erorr_log.html',
                text='Ошибка №20: Данных нет.',
                todo='Вы пытаетесь изменить данные не изменяя данные, введите новые данные.',
                path_to_back='http://localhost:5000/modify_student')     

        if nickname!='':
            # Проверка логина на корректность
            flag=False
            for i in nickname:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №6: В псевдониме не должно быть пробелов.',
                    todo='Введите псевдоним состоящий из одного слова.',
                    path_to_back='http://localhost:5000/modify_student')

            # Проверка на существование такого же псевдонима
            select=User.query.filter_by(nickname=nickname).first()
            if select:
                return render_template('erorr_log.html',
                    text='Ошибка №11: Пользователь с таким псевдонимом уже существует.',
                    todo='Введите другой псевдоним.',
                    path_to_back='http://localhost:5000/modify_student')   

            db.session.query(User).filter_by(id=array[3]).update({'nickname':nickname})
            db.session.commit()

        if password!='':
            # Проверка поля пароль на корректность
            if len(password)<=8:
                return render_template('erorr_log.html',
                    text='Ошибка №5: Пароль должен быть больше 8 символов.',
                    todo='Введите 8 или более символов.',
                    path_to_back='http://localhost:5000/modify_student')

            db.session.query(User).filter_by(id=array[3]).update({'password':password})
            db.session.commit()

        if name!='':
            # Проверка имени
            flag=False
            for i in name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №7: В имени не должно быть пробелов.',
                    todo='Если у вас составное имя, то используйте дефиз.',
                    path_to_back='http://localhost:5000/modify_student')

            db.session.query(User).filter_by(id=array[3]).update({'name':name})
            db.session.commit()

        if second_name!='':
            # Проверка фамилии
            flag=False
            for i in second_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №8: В фамилии не должно быть пробелов.',
                    todo='Если у вас составная фамилия, используйте дефиз.',
                    path_to_back='http://localhost:5000/modify_student')

            db.session.query(User).filter_by(id=array[3]).update({'second_name':second_name})
            db.session.commit()

        if group!='':
            # Проверка группы
            if group==None or group=='None':
                return render_template('erorr_log.html',
                    text='Ошибка №10: Выберите группу.',
                    todo='Введите группу.',
                    path_to_back='http://localhost:5000/modify_student')

            db.session.query(User).filter_by(id=array[3]).update({'group':group})
            db.session.commit()

        if thriiid_name!='':
            # Проверка отчества
            flag=False
            for i in thriiid_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №9: В отчестве не должно быть пробелов.',
                    todo='Возможно вы случайно нажали пробел, повторите ввод.',
                    path_to_back='http://localhost:5000/modify_student')

            db.session.query(User).filter_by(id=array[3]).update({'thriiid_name':thriiid_name})
            db.session.commit()

        if email!='':
            # Проверки на корректность данных почты
            count=0
            i=0
            flag=False
            while i<len(email):
                if email[i]==' ':
                    flag=True
                    break
                  
                if email[i]=='@' and count==0:
                    count+=1
                  
                if email[i]=='.' and count==1:
                    count+=1
                    
                i+=1

            if count!=2:
                flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №4: Почта введена некорректно.',
                    todo='Проверьте раскладку и повторите ввод.',
                    path_to_back='http://localhost:5000/modify_student')

            db.session.query(User).filter_by(id=array[3]).update({'email':email})
            db.session.commit() 

        return render_template('erorr_log.html',
                text='Поздравление №8: Данные обновились.',
                path_to_back='http://localhost:5000/profile_student')

    return render_template('modify_student.html',
        nickname=nickname,
        password=password,
        name=name,
        second_name=second_name,
        group=group,
        thriiid_name=thriiid_name,
        email=email,
        form=form_mod_stud
        )

# Обновление данных преподавателя
@app.route('/modify_teacher', methods=['GET', 'POST'])
def modify_teacher():
    global array

    # Получение старых данных
    select=User.query.filter_by(id=array[3]).first()
    nickname=select.nickname
    password=select.password
    name=select.name
    second_name=select.second_name
    thriiid_name=select.thriiid_name
    email=select.email

    # Объявление формы
    form_mod_teach=Teacher_modify(request.form)

    if request.form and True:
        # Получаем новые данные
        nickname=form_mod_teach.nickname.data
        password=form_mod_teach.password.data
        name=form_mod_teach.name.data
        second_name=form_mod_teach.second_name.data
        thriiid_name=form_mod_teach.thriiid_name.data
        email=form_mod_teach.email

        # Проверка на пустые данные
        if len(nickname)==0 and len(password)==0 and len(name)==0 and len(second_name)==0 and len(thriiid_name)==0 and len(email)==0:
            return render_template('erorr_log.html',
                text='Ошибка №20: Данных нет.',
                todo='Введите новые данные.',
                path_to_back='http://localhost:5000/modify_teacher')

        if nickname!='':
            # Проверка логина на корректность
            flag=False
            for i in nickname:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №6: В псевдониме не должно быть пробелов.',
                    todo='Введите псевдоним из одного слова.',
                    path_to_back='http://localhost:5000/modify_teacher')

            # Проверка на существование такого же псевдонима
            select=User.query.filter_by(nickname=nickname).first()
            if select:
                return render_template('erorr_log.html',
                    text='Ошибка №11: Пользователь с таким псевдонимом уже существует.',
                    todo='Если у вас составное имя, то используйте дефиз.',
                    path_to_back='http://localhost:5000/modify_teacher')   

            db.session.query(User).filter_by(id=array[3]).update({'nickname':nickname})
            db.session.commit()

        if password!='':
            # Проверка поля пароль на корректность
            if len(password)<=8:
                return render_template('erorr_log.html',
                    text='Ошибка №5: Пароль должен быть больше 8 символов.',
                    todo='Введите 8 или более символов.',
                    path_to_back='http://localhost:5000/modify_teacher')

            db.session.query(User).filter_by(id=array[3]).update({'password':password})
            db.session.commit()

        if name!='':
            # Проверка имени
            flag=False
            for i in name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №7: В имени не должно быть пробелов.',
                    todo='Если у вас составное имя, то используйте дефиз.',
                    path_to_back='http://localhost:5000/modify_teacher')

            db.session.query(User).filter_by(id=array[3]).update({'name':name})
            db.session.commit()

        if second_name!='':
            # Проверка фамилии
            flag=False
            for i in second_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №8: В фамилии не должно быть пробелов.',
                    todo='Если у вас составная фамилия, то используйте дефиз.',
                    path_to_back='http://localhost:5000/modify_teacher')

            db.session.query(User).filter_by(id=array[3]).update({'second_name':second_name})
            db.session.commit()

        if thriiid_name!='':
            # Проверка отчества
            flag=False
            for i in thriiid_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №9: В отчестве не должно быть пробелов.',
                    todo='Возможно вы случайно нажали пробел, повторите ввод.',
                    path_to_back='http://localhost:5000/modify_teacher')

            db.session.query(User).filter_by(id=array[3]).update({'thriiid_name':thriiid_name})
            db.session.commit()

        if email!='':
            # Проверки на корректность данных почты
            count=0
            i=0
            flag=False
            while i<len(email):
                if email[i]==' ':
                    flag=True
                    break
                  
                if email[i]=='@' and count==0:
                    count+=1
                  
                if email[i]=='.' and count==1:
                    count+=1
                    
                i+=1

            if count!=2:
                flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №4: Почта введена некорректно.',
                    todo='Проверьте раскладку и повторите ввод.',
                    path_to_back='http://localhost:5000/modify_teacher')

            db.session.query(User).filter_by(id=array[3]).update({'email':email})
            db.session.commit() 

        return render_template('erorr_log.html',
                text='Поздравление №9: Данные обновились.',
                path_to_back='http://localhost:5000/profile_teacher')

    return render_template('modify_teacher.html',
        nickname=nickname,
        password=password,
        name=name,
        second_name=second_name,
        thriiid_name=thriiid_name,
        email=email,
        form=form_mod_teach
        )

@app.route('/modify_admin', methods=['GET', 'POST'])
def modify_admin():

    select=User.query.filter_by(id=array[3]).first()
    email=select.email
    nickname=select.nickname
    password=select.password
    name=select.name
    second_name=select.second_name
    thriiid_name=select.thriiid_name

    # Объявление формы
    form_mod_admin=Admin_modify(request.form)

    if request.form and True:
        # Получаем новые данные
        email=form_mod_admin.email.data
        nickname=form_mod_admin.nickname.data
        password=form_mod_admin.password.data
        name=form_mod_admin.name.data
        second_name=form_mod_admin.second_name.data
        thriiid_name=form_mod_admin.thriiid_name.data

        # Проверка на пустые данные
        if len(nickname)==0 and len(password)==0 and len(name)==0 and len(second_name)==0 and len(thriiid_name)==0 and len(email)==0:
            return render_template('erorr_log.html',
                text='Ошибка №20: Данных нет.',
                todo='Введите данные для изменения.',
                path_to_back='http://localhost:5000/modify_admin')

        if nickname!='':
            # Проверка логина на корректность
            flag=False
            for i in nickname:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №6: В псевдониме не должно быть пробелов.',
                    todo='Введите псевдоним состоящий из одного слова.',
                    path_to_back='http://localhost:5000/modify_admin')

            # Проверка на существование такого же псевдонима
            select=User.query.filter_by(nickname=nickname).first()
            if select:
                return render_template('erorr_log.html',
                    text='Ошибка №11: Пользователь с таким псевдонимом уже существует.',
                    todo='Введите другой псевдоним.',
                    path_to_back='http://localhost:5000/modify_admin')

            db.session.query(User).filter_by(id=array[3]).update({'nickname':nickname})
            db.session.commit()

        if password!='':
            # Проверка поля пароль на корректность
            if len(password)<=8:
                return render_template('erorr_log.html',
                    text='Ошибка №5: Пароль должен быть больше 8 символов.',
                    todo='Введите 8 или более символов.',
                    path_to_back='http://localhost:5000/modify_admin')

            db.session.query(User).filter_by(id=array[3]).update({'password':password})
            db.session.commit()

        if name!='':
            # Проверка имени
            flag=False
            for i in name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №6: В имени не должно быть пробелов.',
                    todo='Если у вас составное имя, то используйте дефиз.',
                    path_to_back='http://localhost:5000/modify_admin')

            db.session.query(User).filter_by(id=array[3]).update({'name':name})
            db.session.commit()

        if second_name!='':
            # Проверка фамилии
            flag=False
            for i in second_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №7: В фамилии не должно быть пробелов.',
                    todo='Если у вас составная фамилия, то используйте дефиз.',
                    path_to_back='http://localhost:5000/modify_admin')

            db.session.query(User).filter_by(id=array[3]).update({'second_name':second_name})
            db.session.commit()

        if thriiid_name!='':
            # Проверка отчества
            flag=False
            for i in thriiid_name:
                if i==' ':
                    flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №8: В отчестве не должно быть пробелов.',
                    todo='Возможно вы случайно нажали пробел, повторите ввод.',
                    path_to_back='http://localhost:5000/modify_admin')

            db.session.query(User).filter_by(id=array[3]).update({'thriiid_name':thriiid_name})
            db.session.commit()

        if email!='':
            # Проверки на корректность данных почты
            count=0
            i=0
            flag=False
            while i<len(email):
                if email[i]==' ':
                    flag=True
                    break
                  
                if email[i]=='@' and count==0:
                    count+=1
                  
                if email[i]=='.' and count==1:
                    count+=1
                    
                i+=1

            if count!=2:
                flag=True

            if flag:
                return render_template('erorr_log.html',
                    text='Ошибка №4: Почта введена некорректно.',
                    todo='Проверьте раскладку и повторите ввод.',
                    path_to_back='http://localhost:5000/modify_admin')

            db.session.query(User).filter_by(id=array[3]).update({'email':email})
            db.session.commit()            

        return render_template('erorr_log.html',
                text='Поздравление №10: Данные обновились.',
                path_to_back='http://localhost:5000/modify_admin')

    return render_template('modify_admin.html',
        nickname=nickname,
        email=email,
        password=password,
        name=name,
        second_name=second_name,
        thriiid_name=thriiid_name,
        form=form_mod_admin
        )

# Отображение разделов созданных преподавателем
@app.route('/razdel', methods=['GET','POST'])
def razdel():
    # Объявление переменных для отображения в разделе
    name_lab=False
    labs=[]
    teachers=[]
    predmets=[]
    name_teacher=''
    path=''

    # Возврат нужного шаблона страницы в зависимости от рольи
    select=User.query.filter_by(id=array[3]).first()
    if select.role=='teacher':
        path_to_back='http://localhost:5000/profile_teacher'
    else:
        path_to_back='http://localhost:5000/profile_student'

    name=select.name
    name+=' '
    second_name=select.second_name
    thriiid_name=select.thriiid_name
    
    # Создание массива с название лаб для их отображения преподавателя
    if select.role=='teacher':
        predmet=select.predmet
        temp=''
        for i in range(len(predmet)):
            if predmet[i]==' ':
                predmets.append(temp)
                temp=''
                continue
            else:
                temp+=predmet[i]
        predmets.append(temp)
        select=Labs.query.filter_by(id_user=select.id).all()
        for i in select:
            labs.append(i.name_lab)
        teachers.append(second_name+' '+name+thriiid_name)

    else:
        select=User.query.all()
        for i in select:
            if i.role=='teacher':
                teachers.append(i.second_name+' '+i.name+' '+i.thriiid_name)
                if i.group!=None:
                    arr=i.group.split(' ')
                for j in range(len(arr)):
                    temp=''
                    for k in range(len(i.predmet)):
                        if i.predmet[k]==' ':
                            if temp not in predmets:
                                predmets.append(temp)
                            temp=''
                            continue
                        else:
                            temp+=i.predmet[k]
                    if temp not in predmets:
                        predmets.append(temp)
                    
                    if arr[j]==array[2]:
                        select=Labs.query.filter_by(id_user=i.id).all()
                        for k in select:
                            labs.append(k.name_lab)

    form_upload=UploadForm(request.form)
    if request.form and True:
        # Изъятие данных из форм
        data=request.files[form_upload.image.name].read()
        predmetss=[]
        temp=''

        # Отлов сигнала с названием раздела лабы
        for i in request.form:
            select=User.query.filter_by(id=array[3]).first()

            # Раздел для преподавателя
            if select.role=='teacher':
                select=User.query.filter_by(name=i).first()
                if select:
                    name_teacher+=select.name
                    name_teacher+=' '
                    name_teacher+=select.second_name
                    temp+=select.predmet
                    word=''
                    
                    for j in range(len(temp)):
                        if temp[j]==' ':
                            predmetss.append(word)
                            word=''
                            continue
                        else:
                            word+=temp[j]
                    predmetss.append(word)

                if name_teacher=='':
                    return render_template('erorr_log.html',
                        text='Ошибка №21: Преподаватель не выбран.',
                        todo='Выберите преподавателя.',
                        path_to_back='http://localhost:5000/razdel')

                # Выбор имени преподавателя
                print(form.request)
                name=''
                i=0
                while name_teacher[i]!=' ':
                    name+=name_teacher[i]
                    i+=1

                # Отлов предмета
                for i in request.form:
                    if i!='name_file' and i!=name and i not in predmetss:
                        name_lab=i
                    elif i in predmetss:
                        predmet=i

                # Непонятно зачем
                if name_lab:
                    print(name)
                    select=User.query.filter_by(name=name).first()#вооооот здесь если будет второй дмитрий то грусть, позже исправь----------------------
                    select=Labs.query.filter_by(id_user=select.id).all()
                    for i in select:
                        count=0
                        temp=''
                        j=0
                        while count!=3:
                            if i.path[j]=='/':
                                count+=1
                            j+=1
                        for k in range(j, len(i.path)):
                            temp+=i.path[k]
                        if temp==name_lab:
                            path+=i.path
                            path+='/'
            
            # Раздел для студента
            else:
                select=User.query.filter_by(role='teacher').all()
                for l in request.form:
                    for j in select:
                        if l==j.second_name:
                            name_teacher=j.second_name
                            name_teacher+=' '
                            name_teacher+=j.name
                            name_teacher+=' '
                            name_teacher+=j.thriiid_name

                if name_teacher=='':
                    return render_template('erorr_log.html',
                        text='Ошибка №21: Преподаватель не выбран.',
                        todo='Выберите преподавателя.',
                        path_to_back='http://localhost:5000/razdel')

                # Выбор имени
                second_name=''
                i=0
                while name_teacher[i]!=' ':
                    second_name+=name_teacher[i]
                    i+=1

                predmetss=[]

                # Если здесь второй такой же то жопа------------------------------------------------------------------------
                # Выбор предметов
                select=User.query.filter_by(second_name=second_name).first()
                temp=''
                for i in range(len(select.predmet)):
                    if select.predmet[i]==' ':
                        predmetss.append(temp)
                        temp=''
                        continue
                    else:
                        temp+=select.predmet[i]
                predmetss.append(temp)

                # Создание предмета
                for i in request.form:
                    if i!='name_file' and i!=second_name and i not in predmetss:
                        name_lab=i
                    elif i in predmetss:
                        predmet=i

        # Забираем название файла
        name_file=form_upload.name_file.data
        if name_file=='':
            return render_template('erorr_log.html',
                text='Ошибка №22: Название файла не введено.',
                todo='Введите название файла.',
                path_to_back='http://localhost:5000/razdel')

        # Проверка на корректность имени файла
        flag=False
        flag_raschirenie=True
        for i in range(len(name_file)):
            if name_file[i]==' ':
                flag=True

            if name_file[i]=='.':
                if (i+3)<=len(name_file):
                    if name_file[i+1]=='c' and name_file[i+2]=='p' and name_file[i+3]=='p':
                        flag_raschirenie=False

        if flag:
            return render_template('erorr_log.html',
                text='Ошибка №24: Название файла введено не корректно.',
                todo='Возможно вы ввели пробел, попробуйте ещё раз.',
                path_to_back='http://localhost:5000/razdel')
        
        if flag_raschirenie:
            return render_template('erorr_log.html',
                text='Ошибка №25: Название файла не содержит расширение или оно не корректно.',
                todo='Пожалуйста, введите расширение файла вместе с названием файла.',
                path_to_back='http://localhost:5000/razdel')

        # Сам файл
        if not name_lab:
            return render_template('erorr_log.html',
                text='Ошибка №26: Файл не выбран.',
                todo='Выберите файл.',
                path_to_back='http://localhost:5000/razdel')

        # Загрузка в папку
        path='app/upload_file/'+name_teacher+'/'+predmet+'/'+name_lab+'/'
        f=open(path+name_file, 'wb')
        f.write(data)
        f.close()

        # Сохранение времени загрузки программы
        from datetime import datetime
        date=datetime.now()

        select=Labs.query.filter_by(name_lab=name_lab).first()
        idd=select.name_lab

        # Узнаём все программы загруженные для данной лабораторной
        paths=[]
        select=Programs.query.filter_by(name_lab=idd).all()
        for i in select:
            # нужен путь без названия файла
            temp=''
            count=0
            for j in i.path:
                if j=='/':
                    count+=1
                if count!=5:
                    temp+=j
            paths.append(temp)
            paths.append(i.name_file)

        # Создаём токены этой программы и всех программ для этой лабы
        tokens=[]
        token=tokenization.main(path, name_file)
        for i in range(0, len(paths), 2):
            bucket=tokenization.main(paths[i], paths[i+1])
            bucket=bucket[:(len(bucket)-2)]
            tokens.append(bucket)

        lines=token[len(token)-1]
        z=token[len(token)-2]
        token=token[:(len(token)-2)]

        ngrammSELF=ngramm.main(token)
        result_metric=[]
        
        # Проверяем нашу последовательность токенов со всеми метрикой схожести и выбираем самый большой процент схожести
        for i in range(len(tokens)):
            ngrammOTHER=ngramm.main(tokens[i])
            result_metric.append(metric.main(ngrammSELF, ngrammOTHER))

        # Когда программа загружается первой в раздел
        if result_metric==[]:
            # Сохрание информации о том кто залил, путь к лабе и раздел
            P=Programs(name_lab=idd, who_upload=array[3], path=(path+name_file), name_file=name_file, date=date, percent='0%')
            db.session.add(P)
            db.session.commit()

            return render_template('happy_log.html',
                    text='Подздравение №11: Программа загруженна.',
                    path_to_back='http://localhost:5000/razdel')

        # Если по метрике не выявленно сходство то тогда метод поиска наибольшей подстроки
        max_metric=max(result_metric)
        if max_metric<=1.10:
            result_find=[]
            for i in range(len(tokens)):
                midle=find.main(token, tokens[i], z, lines)
                result_find.append(midle[0])

            percent=str(max(result_find))+'%'
        else:
            percent=str(max_metric*100)+'%'

        # Сохрание информации о том кто залил, путь к лабе и раздел
        P=Programs(name_lab=idd, who_upload=array[3], path=(path+name_file), name_file=name_file, date=date, percent=percent, copycode=midle[1])
        db.session.add(P)
        db.session.commit()

        return render_template('happy_log.html',
                text='Подздравение №11: Программа загруженна.',
                path_to_back='http://localhost:5000/razdel')

    return render_template('razdel.html',
        labs=labs,
        teachers=teachers,
        predmets=predmets,
        form=form_upload,
        profile=path_to_back
        )

# Создание разделов
@app.route('/create_razdel', methods=['GET','POST'])
def create_razdel():
    form_create=Create(request.form)

    if request.form and True:
        # Изъятие данных из формы
        name_lab=form_create.name_lab.data
        description=form_create.description.data
        helpp=form_create.helpp.data

        # Проверка заполненности полей
        if name_lab=='':
            return render_template('erorr_log.html',
                text='Ошибка №27: Название лабораторной не введено.',
                todo='Введите название лабораторной.',
                path_to_back='http://localhost:5000/create_razdel')

        # Проверка на уже существование данного раздела
        select=Labs.query.filter_by(name_lab=name_lab).first()
        if select:
            return render_template('erorr_log.html',
                text='Ошибка №28: Такая лабораторная уже существует.',
                path_to_back='http://localhost:5000/create_razdel')

        # Проверка на пробелы
        flag=False
        for i in name_lab:
            if i==' ':
                flag=True

        if flag:
            return render_template('erorr_log.html',
                text='Ошибка №29: Имя лабораторной не должно содержать пробелы.',
                todo='Повторите ввод без пробелов, используя знак "_".',
                path_to_back='http://localhost:5000/create_razdel')

        # Создание раздела в папке с преподавателем
        else:
            for i in request.form:
                if i!='name_lab' and i!='helpp' and i!='description':
                    temp=i

            select=User.query.filter_by(id=array[3]).all()
            for i in select:
                name=i.name
                second_name=i.second_name
                thriiid_name=i.thriiid_name

            # Создание пути для раздела
            path='app/upload_file/'+second_name+' '+name+' '+thriiid_name+'/'+temp+'/'+name_lab

            L=Labs(name_lab=name_lab, id_user=array[3], path=path, description=description, predmet=temp)
            db.session.add(L)
            db.session.commit()
            
            # Сохранение айди созданной лабы
            select=User.query.filter_by(id=array[3]).first()
            temp=select.labs_id
            if temp!=None:
                temp+='|'
            select=Labs.query.filter_by(name_lab=form_create.name_lab.data).first()
            if temp!=None:
                temp+=str(select.id)
            else:
                temp=str(select.id)

            db.session.query(User).filter_by(id=array[3]).update({'labs_id':temp})
            db.session.commit()
            os.mkdir(path)

            return render_template('happy_log.html',
                text='Подздравление №12: Лабораторная создана.',
                path_to_back='http://localhost:5000/profile_teacher')

    # Выборка списка предметов для которых будет создаваться раздел
    select=User.query.filter_by(id=array[3]).first()
    predmet=select.predmet
    predmets=[]
    temp=''
    for i in range(len(predmet)):
        if predmet[i]==' ':
            predmets.append(temp)
            temp=''
            continue
        else:
            temp+=predmet[i]
    predmets.append(temp)
    
    return render_template('create_razdel.html',
        form=form_create,
        predmets=predmets
        )

# Для просмотра студентом своих загрузок
@app.route('/student_uploads', methods=['GET','POST'])
def student_uploads():
    global array
    files=[]
    labs=[]
    temp=[]
    select=Programs.query.filter_by(who_upload=array[3]).all()

    # Создание списков
    for i in select:
        files.append(i.name_lab)
        labs.append(i.path)
    
    upload_links=labs

    # Выделение названия лабы из пути
    for i in labs:
        bucket=''
        count=0
        j=0
        while count<3:
            if i[j]=='/':
                count+=1
            j+=1
        while i[j]!='/':
            bucket+=i[j]
            j+=1
        temp.append(bucket)
    labs=temp

    if request.form and True:
        # Выбор файла для удаления
        for i in request.form:
            file_for_delete=i
        
        # Удаление файла
        select=Programs.query.filter_by(name_lab=file_for_delete).first()
        os.remove(select.path)
        db.session.delete(select)
        db.session.commit()

        return render_template('erorr_log.html',
                text='Поздравление №13: Файл удалён.',
                path_to_back='http://localhost:5000/profile_student')

    return render_template('student_uploads.html',
        files=files
        )

# Показывает списко групп и студентов которые там учатся
@app.route('/groups', methods=['GET','POST'])
def Groups():
    select=User.query.filter_by(id=array[3]).all()
    predmets=[]
    labs=[]
    graf=[]

    for i in select:
        predmet=i.predmet
        lab=i.labs_id
    
    temp=''
    for i in range(len(predmet)):
        if predmet[i]==' ':
            predmets.append(temp)
            temp=''
        else:
            temp+=predmet[i]
    predmets.append(temp)

    temp=''
    # Отлов ошибки при отсутствии данных
    # print(lab)
    if lab==None:
        return render_template('erorr_log.html',
                text='Ошибка №30: Студентов нет.',
                todo='Подождите регистрации студентов.',
                path_to_back='http://localhost:5000/profile_teacher')

    for i in range(len(lab)):
        if lab[i]=='|':
            select=Labs.query.filter_by(id=int(temp)).first()
            labs.append(select.name_lab)
            graf.append(select.name_lab)
            temp=''
        else:
            temp+=lab[i]
    select=Labs.query.filter_by(id=int(temp)).first()
    labs.append(select.name_lab)
    graf.append(select.name_lab)

    # Соаздание связи предмет-лаба
    enity=[]
    i=0
    j=0
    while i<len(predmets):
        bucket=[]
        bucket.append(predmets[i])

        while j<len(labs):
            select=Labs.query.filter_by(name_lab=labs[j]).first()
            if select.predmet==predmets[i]:
                bucket.append(labs[j])
            else:
                break
            j+=1
        enity.append(bucket)
        i+=1

    form_group=Group(request.form)

    if request.form and True:
        # отлов номера студента для предоставления информации по нему
        for i in request.form:
            name_lab=i

        if name_lab=='':
            return render_template('erorr_log.html',
                text='Ошибка №30: Укажите номер студента.',
                todo='Введите номер студента.',
                path_to_back='http://localhost:5000/groups')

        else:
            select=Programs.query.filter_by(name_lab=name_lab).all()
            number=[]
            for i in select:
                number.append(i)
            
            global number
            return redirect(url_for('Student'))

    percenttt=[]
    for i in graf:
        select=Programs.query.filter_by(name_lab=i).all()
        percent=0
        count=0
        for j in select:
            bucket=j.percent
            new=''
            k=0
            while bucket[k]!='%':
                new+=bucket[k]
                k+=1

            percent+=float(new)
            count+=1
        if count!=0:
            temp=percent/count
            percenttt.append(temp)

    # График
    trace=go.Bar(x=graf, y=percenttt)
    data=[trace]
    layout=go.Layout(title='Процент плагита в лабораторных задания в предмете', width=800, height=350)
    fig=go.Figure(data=data, layout=layout)

    global name_grafic
    name_grafic[2]+=1
    temp='app/static/grafics/grf_group_'+str(name_grafic[2])+'.png'
    py.image.save_as(fig, filename=temp)

    # Костыль для графиеков
    template='''
    {% extends "base.html" %}
    {% block content %}

    <a href='http://localhost:5000/profile_teacher'>
    '''+'''
        <img src="{{url_for('static', filename='Close-button1.png')}}" height='40px' width='40px' align='right'>'''+'''
    </a>

    <form method='post' name='reg'>
        <table width='80%' align='center' style='border-style: solid; border-width: 2px; border-radius: 20px; border-color: #c0c0c0; box-shadow: 0 0 50px rgba(0,0,0,0.5); padding-left: 30px; padding-top: 20px; padding-bottom: 20px; padding-right: 20px;'>
            '''+'''{% for predmet in data %}'''+'''
            <tr>
                <td valign='top'>
                    <div id='text3'>
                        Predmet - '''+'''{{predmet[0]}}'''+'''
                    </div>
                    '''+'''
                    {% for lab in predmet %}'''+'''
                        <div id='frame1' style='width: 600px;'>
                        '''+'''
                            <input type='radio' name='{{lab}}'>
                            {{lab}}'''+'''
                        </div>
                        '''+'''
                    {% endfor %}
                    '''+'''
                    <br>
                    <div style='padding-left: 120px;'>
                            <input class='btn-green' style='width: 100px;' type='submit' value='Next'>
                    </div>
                </td>
                <td>
                    <div align='center'>
                    '''+'''
                        <img src={{url_for('static', filename='grafics/grf_group_'''+str(name_grafic[2])+'''.png')}}>'''+'''
                    </div>
                </td>
            </tr>
            <tr>
                <td colspan='2'>
                    <hr size='2px' color='#a0a0a0'> 
                </td>
            </tr>
            '''+'''
            {% endfor %}'''+'''
        </table>
    </form> 

    {% endblock %}
    '''

    f=open('app/templates/groups_'+str(name_grafic[2])+'.html', 'w')
    f.write(template)
    f.close()

    return render_template('groups_'+str(name_grafic[2])+'.html',
        data=enity,
        form=form_group
        )

# Вывод информации по студенту
@app.route('/student', methods=['GET','POST'])
def Student():
    global array
    global number
    
    labs=[]
    description=[]
    fio=[]
    group=[]
    percent=[]
    date=[]
    copycode=[]

    for i in number:
        copycode.append(i.copycode)
        date.append(i.date)
        percent.append(i.percent)
        labs.append(i.name_lab)
        
        select=User.query.filter_by(id=i.who_upload).first()
        temp=select.second_name+' '+select.name+' '+select.thriiid_name
        fio.append(temp)
        group.append(select.group)

        select=Labs.query.filter_by(name_lab=i.name_lab).first()
        description.append(select.description)

    lenSELF=len(fio)
    
    if request.form and True:
        pass
    
    return render_template('student.html',
        labs=labs,
        description=description,
        fio=fio,
        group=group,
        percent=percent,
        date=date,
        copycode=copycode,
        lenSELF=lenSELF
        )

# Просмотр процента плагита студентов
@app.route('/Comment', methods=['GET','POST'])
def Comment():
    select=User.query.filter_by(role='student').all()
    enity=[]
    d=[]
    for i in select:
        enity.append(i.group)
        enity.append(i.second_name)
        enity.append(i.name)
        enity.append(i.thriiid_name)
        d.append(i.id)

    if len(enity)==4:
        lenSELF=1
    else:
        lenSELF=len(enity)//4

    if request.form and True:
        for i in request.form:
            second_name=i

        if second_name=='':
            return render_template('erorr_log.html',
                text='Ошибка №30: Укажите номер студента.',
                todo='Введите номер студента.',
                path_to_back='http://localhost:5000/groups')
        else:
            select=User.query.filter_by(second_name=second_name).first()
            aidi=select.id
            global aidi

            return redirect(url_for('info'))

    # Данные для графика
    # print(d)
    all_percent=[]
    all_name_file=[]

    for i in d:
        percent=[]
        name_file=[]
        select=Programs.query.filter_by(who_upload=i).all()
    
        for j in select:
            percent.append(j.percent)
            name_file.append(j.name_file)

        all_percent.append(percent)
        all_name_file.append(name_file)

    # print(all_percent)
    # print(all_name_file)

    # Отлов ошибки при отсутствии данных
    # print(len(all_name_file), len(all_percent))
    if len(all_name_file)!=0 and len(all_percent)!=0:
        # График
        trace=go.Bar(x=all_name_file[0], y=all_percent[0])
        data=[trace]
        layout=go.Layout(title='Плагиат студента', width=1000, height=400)
        fig=go.Figure(data=data, layout=layout)

        global name_grafic
        name_grafic[3]+=1
        temp='app/static/grafics/grf_stud_'+str(name_grafic[3])+'.png'
        py.image.save_as(fig, filename=temp)

    # Костыль для графиеков
    template='''
        {% extends "base.html" %}
        {% block content %}

        <a href='http://localhost:5000/profile_teacher'>'''+'''
            <img src="{{url_for('static', filename='Close-button1.png')}}" height='40px' width='40px' align='right'>'''+'''
        </a>

        <form method='post' name='reg'>
            <table id='comm'>
            '''+'''
                {% for i in range(0, lenSELF, 4) %}'''+'''
                    <tr>
                        <td valign='top'>
                        '''+'''
                            <input type='radio' name='{{enity[i+1]}}'>'''+'''
                            <div id='text3'>
                            '''+'''
                                {{ enity[i] }}
                                {{ enity[i+1] }}
                                {{ enity[i+2] }}
                                {{ enity[i+3] }}
                                '''+'''
                            </div>
                        </td>
                        <td>
                            <div align='center' style='padding-left: 40px'>'''+'''
                                <img src={{url_for('static', filename='grafics/grf_stud_'''+str(name_grafic[3])+'''.png')}}>'''+'''
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td colspan='2'>
                            <hr color='#a0a0a0' size='2px'>
                        </td>
                    </tr>
                {% endfor %}
            </table>
            <br>
            <br>
            <input class='btn-green' style='width: 100px;' type='submit' value='Next'>
        </form> 

        {% endblock %}
    '''

    f=open('app/templates/comment_'+str(name_grafic[3])+'.html', 'w')
    f.write(template)
    f.close()

    return render_template('comment_'+str(name_grafic[3])+'.html',
        lenSELF=lenSELF,
        enity=enity
        )

@app.route('/info', methods=['GET', 'POST'])
def info():
    global aidi
    select=User.query.filter_by(id=aidi).first()
    selectt=Programs.query.filter_by(who_upload=aidi).all()
    
    name_file=[]
    percent=[]
    date=[]
    copycode=[]
    comment=[]
    iddd=[]
    for i in selectt:
        name_file.append(i.name_file)
        percent.append(i.percent)
        date.append(i.date)
        copycode.append(i.copycode)
        comment.append(i.comment)
        iddd.append(i.id)

    lenSELF=len(name_file)

    if request.form and True:
        for i in request.form:
            comment=i

        if comment=='':
            return render_template('erorr_log.html',
                text='Ошибка №30: Укажите номер студента.',
                todo='Введите номер студента.',
                path_to_back='http://localhost:5000/groups')
        else:
            for i in request.form:
                nextt=i
            global nextt
            
    form_comm=Comm(request.form)
    return render_template('info.html',
        name=select.name,
        second_name=select.second_name,
        thriiid_name=select.thriiid_name,
        name_file=name_file,
        percent=percent,
        date=date,
        copycode=copycode,
        comment=comment,
        form=form_comm,
        lenSELF=lenSELF,
        iddd=iddd
        )