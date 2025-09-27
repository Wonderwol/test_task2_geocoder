#  Геокодер

## Описание проекта
Геокодер, который позволяет преобразовывать адреса в точку на карте.

Особенности:
- История введённых адресов с возможностью редактирования.
- Флэш-сообщения для уведомлений пользователя.
- Карта с маркерами, встроенная через API.

## Технологии:
- **Backend:** Flask, SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript
- **API:** Yandex Geocoder

## GIF-демонстрация
![Демонстрация работы геокодера](gif/geocoder.gif)  

## Установка и запуск

## 1. Клонируйте репозиторий:
git clone https://github.com/Wonderwol/test_task2_geocoder.git
cd test_task2_geocoder

## 2. Создайте и активируйте виртуальное окружение:
python -m venv venv

### Windows
venv\Scripts\activate

### macOS/Linux
source venv/bin/activate

## 3. Установите зависимости:
pip install -r requirements.txt

## 4. Вставте ключ и YANDEX API
Получите API-ключ Yandex Geocoder на https://developer.tech.yandex.ru

Создайте файл конфигурации .env и добавьте в него следующие переменные:
YANDEX_API_KEY = "ваш API-ключ"
SECRET_KEY = "ваш секретный ключ для Flask" (напишите любое слово)

## 5. Запуск
flask run
И откройте http://127.0.0.1:5000 в браузере.