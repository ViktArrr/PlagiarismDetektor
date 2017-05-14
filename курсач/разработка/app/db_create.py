from app import db
from app.models import User, Roles

db.create_all()

U=User(nickname='admin', password='321519', email='admin@example.com', role='admin', name='Виктор', second_name='Сергеев', thriiid_name='Сергеевич', name_avatar='ava.png')
db.session.add(U)

R=Roles(description='Создаёт/удаляет преподавателей, предметы, группы')
db.session.add(R)
R=Roles(description='Создаёт разделы для загрузки программ и анализирует статистику полученную в ходе работы детектора плагиата')
db.session.add(R)
R=Roles(description='Загружает программы и надеется на лучшее')
db.session.add(R)

db.session.commit()