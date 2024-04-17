# Импорт необходимых модулей из библиотек Flask и Flask-WTF
from flask import Flask, render_template
from flask_wtf import FlaskForm

# Импорт классов полей из модуля wtforms
from wtforms import StringField, IntegerField, SubmitField, TelField

# Импорт валидаторов из модуля wtforms.validators
from wtforms.validators import InputRequired, Email

# Создаем экземпляр Flask с названием приложения
app = Flask(__name__)

# Определение класса формы регистрации
class RegistrationForm(FlaskForm):
    # Поле для ввода email с валидацией наличия ввода и соответствия формату email
    email = StringField(validators=[InputRequired(), Email()])
    
    # Поле для ввода телефона с валидацией наличия ввода
    phone = TelField(validators=[InputRequired()])
    
    # Поле для ввода имени с валидацией наличия ввода
    name = StringField(validators=[InputRequired()])
    
    # Поле для ввода адреса без валидации
    address = StringField()
    
    # Поле для ввода индекса без валидации
    index = IntegerField()
    
    # Поле для ввода комментария без валидации
    comment = StringField()
    
    # Кнопка отправки формы
    submit = SubmitField(label=('Submit'))


# Обработчик маршрута для главной страницы
@app.route('/')
def index():
    return 'Главная страница'

# Обработчик маршрута для страницы регистрации
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # Создаем экземпляр формы для регистрации
    form = RegistrationForm()

    # Проверяем, была ли форма отправлена и прошла ли валидацию
    if form.validate_on_submit():
        # Если форма прошла валидацию, получаем данные из полей формы
        email, phone, name, address = form.email.data, form.phone.data, form.name.data, form.address.data
        
        # Выводим данные формы в консоль для отладки
        print(email, phone, name, address)

        # Возвращаем приветственное сообщение с использованием имени пользователя
        return f'Hello {name} welcome to our site!'
    
    # Если форма не была отправлена или не прошла валидацию,
    # отображаем HTML-шаблон с формой регистрации,
    # передавая объект формы для отображения введенных пользователем данных
    return render_template('reg_form_wtf.html', form=form)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False  # Отключаем проверку CSRF для WTForms
    app.run(debug=True)  # Запускаем приложение в режиме отладки
