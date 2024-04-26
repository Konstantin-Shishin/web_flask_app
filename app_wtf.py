# Импорт необходимых модулей из библиотек Flask и Flask-WTF
from flask import Flask, render_template
from flask_wtf import FlaskForm

# Импорт классов полей из модуля wtforms
from wtforms import StringField, IntegerField, SubmitField, TelField, RadioField

# Импорт валидаторов из модуля wtforms.validators
from wtforms.validators import InputRequired

# Импорт модуля SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр Flask с названием приложения
app = Flask(__name__)

# Установка URI для подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Создаем объект базы данных
db = SQLAlchemy(app)

# Класс Пользователя для базы данных
class User(db.Model):
    #Указываем им таблицы
    __tablename__ = 'users'

    # Заводим поля
    UID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    age = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)
    email = db.Column(db.String(120))
    pol = db.Column(db.String(20))
    phone = db.Column(db.Integer)

    # Инициализатор для создания объектов класса
    def __init__(self, name, city, age, is_active, email, pol, phone):
        self.name = name
        self.city = city
        self.age = age
        self.is_active = is_active
        self.email = email
        self.pol = pol
        self.phone = phone

    # Метод для текстового представления объекта Пользователя
    def __str__(self):
        return f'<Пользователь {self.name}, {self.city}, {self.age}>'

# Определение класса формы регистрации
class RegistrationForm(FlaskForm):  
    # Заводим поля
    email = StringField(validators=[InputRequired()])
    phone = TelField(validators=[InputRequired()])
    name = StringField(validators=[InputRequired()])
    age = IntegerField()
    address = StringField()
    pol = RadioField(label='Пол', choices=[(0 ,'Мужской' ), (1, 'Женский')]) 
    # Поле кнопки отправки формы
    submit = SubmitField(label=('Submit'))


# Обработчик маршрута для главной страницы
@app.route('/')
def index():
    return render_template('main.html')

# Обработчик маршрута для страницы пользователей с таблицей
@app.route('/users')
def users():
    #SELECT запрос на получение всей таблицы (список записей)
    people = User.query.all() 
    # Вывод полученных Пользователей в консоль
    for user in users:
        print(user)
    # Возвращаем html c таблицей
    return render_template('users.html', users = people)

# Обработчик маршрута для страницы регистрации
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # Создаем экземпляр формы для регистрации
    form = RegistrationForm()

    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        # Если форма прошла валидацию, получаем данные из полей формы
        email, phone, name, address, pol, age = form.email.data, form.phone.data, form.name.data, form.address.data, form.pol.data, form.age.data        
        # Выводим данные формы в консоль для отладки
        print(email, phone, name, address, pol, age)
        # Создаем новый объект Пользователя
        new_user = User(name=name, city=address, age=age, email=email,pol='Мужской' if pol == 0 else 'Женский', phone=phone, is_active=True)
        db.session.add(new_user)  # Добавляем Пользователя в базу данных
        db.session.commit()  # Фиксация изменений в базе данных
        # Возвращаем приветственное сообщение (html) с использованием имени пользователя
        return render_template('success_reg.html', name=name)
    
    # Если форма не была отправлена или не прошла валидацию,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных пользователем данных
    return render_template('reg_form_wtf.html', form=form)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False  # Отключаем проверку CSRF для WTForms
    app.run(debug=True)  # Запускаем приложение в режиме отладки
