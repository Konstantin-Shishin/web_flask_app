# Импорт необходимых модулей из библиотек Flask и Flask-WTF
from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm

# Импорт классов полей из модуля wtforms
from wtforms import StringField, IntegerField, SubmitField, TelField, RadioField, FileField

# Импорт валидаторов из модуля wtforms.validators
from wtforms.validators import InputRequired

from flask_wtf.file import FileField, FileRequired

from werkzeug.utils import secure_filename

import os

# Создаем экземпляр Flask с названием приложения
app = Flask(__name__)

# Словарь пользователей
UID = {
        '1':
    {
    'name': 'Евгений',
    'city': 'Красноярск',
    'age': 14,
    'is_active': True,
    'email': 'yuyuy@mail.ru',
    'pol': 'Мужской',
    'phone': 789653223
    },
        '2': 
    {
    'name': 'Иван',
    'city': 'Находка',
    'age': 16,
    'is_active': True,
    'email': 'yuyuy@mail.ru',
    'pol': 'Мужской',
    'phone': 789653224
    },
       '3': {
    'name': 'Софья',
    'city': 'Калининград',
    'age': 15,
    'is_active': False,
    'email': 'yuyuy@mail.ru',
    'pol': 'Женский',
    'phone': 789653225
    }
    }

# Определение класса формы регистрации
class RegistrationForm(FlaskForm):
    # Поле для ввода email с валидацией наличия ввода
    email = StringField(validators=[InputRequired()])
    
    # Поле для ввода телефона с валидацией наличия ввода
    phone = TelField(validators=[InputRequired()])
    
    # Поле для ввода имени с валидацией наличия ввода
    name = StringField(validators=[InputRequired()])

    # Поле для ввода возраста
    age = IntegerField()
    
    # Поле для ввода адреса без валидации
    address = StringField()

    #Поле радио-кнопки для выбора пола
    pol = RadioField(label='Пол', choices=[(0 ,'Мужской' ), (1, 'Женский')])
    
    # Поле для ввода индекса без валидации
    index = IntegerField()
    
    # Поле для ввода комментария без валидации
    comment = StringField()

    file = FileField(validators=[FileRequired()])
    
    # Кнопка отправки формы
    submit = SubmitField(label=('Submit'))

# Обработчик маршрута для главной страницы
@app.route('/')
def index():
    return 'Главная страница'

@app.route('/users')
def userss():
    return render_template('users.html', users = UID)

# Обработчик маршрута для страницы регистрации
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # Создаем экземпляр формы для регистрации
    form = RegistrationForm()

    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        # Если форма прошла валидацию, получаем данные из полей формы
        email, phone, name, address, pol, age, file = form.email.data, form.phone.data, form.name.data, form.address.data, form.pol.data, form.age.data, form.file.data
        
        # Выводим данные формы в консоль для отладки
        print(email, phone, name, address, pol, age)

        
        filename = secure_filename(file.filename)
        file.save(os.path.join(
                app.static_folder, 'photos', filename
        ))

        # Добавление пользователя в словарь
        UID[str(int(max(UID))+1)]= {
        'name': name,
        'city': address,
        'age': age,
        'email': email,
        'pol': pol,
        'phone': phone,
        'filename': filename
        } 

        # Возвращаем приветственное сообщение с использованием имени пользователя
        # return f'Hello {name} welcome to our site! {filename}'
        return render_template('welcome.html', fname = filename)
    
    # Если форма не была отправлена или не прошла валидацию,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных пользователем данных
    return render_template('reg_form_wtf.html', form=form)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False  # Отключаем проверку CSRF для WTForms
    app.run(debug=True)  # Запускаем приложение в режиме отладки
