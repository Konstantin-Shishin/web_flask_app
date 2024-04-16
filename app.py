from flask import Flask
from flask import request, render_template

# Создаем экземпляр Flask с названием приложения
app = Flask(__name__)

# Словарь с информацией о пользователях
UID = {
    '1': {
        'name': 'Евгений',
        'city': 'Красноярск',
        'age': 14
    },
    '2': {
        'name': 'Иван',
        'city': 'Находка',
        'age': 16
    },
    '3': {
        'name': 'Софья',
        'city': 'Калининград',
        'age': 15
    }
}

# Определение маршрута для главной страницы
@app.route('/')
def index():
    return render_template('users.html', users=UID)

# Определение маршрута для отображения информации о конкретном пользователе
@app.route('/user/<id>')
def user(id):
    if id in UID:
        return f"Здравствуйте, Ваше имя: {UID[id]['name']}, Ваш город: {UID[id]['city']}, Ваш возраст: {UID[id]['age']}"
    else:
        return 'Такого пользователя не существует'


# Определение маршрута для добавления нового пользователя
@app.route('/add_user')
def add_user():
    # Получение данных о новом пользователе из запроса
    name = request.args.get('name')
    city = request.args.get('city')
    age = request.args.get('age')
    
    # Генерация уникального ID для нового пользователя
    new_id = str(int(max(UID)) + 1)
    
    # Добавление нового пользователя в словарь UID
    UID[new_id] = {
        'name': name,
        'city': city,
        'age': age
    }
    
    # Возвращение информации о добавленном пользователе в виде строки
    return f"Имя = {name}; Город = {city}; Возраст = {age}"

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
