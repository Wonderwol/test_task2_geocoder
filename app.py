import os
import requests
from requests.exceptions import RequestException
from flask import Flask, render_template, request, \
     flash, session, url_for, redirect
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import re

from models import db, History

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geocoder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Вставьте свой секретный ключ
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

db.init_app(app)

# Вставьте свой Яндекс API
YANDEX_API_KEY = os.environ.get("YANDEX_API_KEY")

if not YANDEX_API_KEY:
    raise ValueError("YANDEX_API_KEY не найден. Установите его в .env")


with app.app_context():
    db.create_all()


def geocode_address(address):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": YANDEX_API_KEY,
        "geocode": address,
        "format": "json",
        "kind": "house"
    }
    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    data = r.json()
    feature = data.get("response", {}).get("GeoObjectCollection", {}).get(
        "featureMember", [])
    if not feature:
        return None
    geo_object = feature[0]["GeoObject"]
    found_address = geo_object.get("metaDataProperty", {}).get(
        "GeocoderMetaData", {}).get("text", "")
    pos = geo_object["Point"]["pos"]
    lon, lat = map(float, pos.split())
    return found_address, lat, lon


@app.route("/", methods=["GET", "POST"])
def index():
    # Берём координаты из сессии или ставим дефолтные
    coords = session.pop("coords", None)
    if coords is None:
        coords = (55.751244, 37.618423)  # Дефолтные координаты (Москва)

    address = ""
    edit_id = request.args.get("edit_id", type=int)

    # GET-запрос для редактирования
    if request.method == "GET" and edit_id:
        entry = History.query.get(edit_id)
        if entry:
            address = entry.address
            coords = (entry.latitude, entry.longitude)

    if request.method == "POST":
        address = request.form.get("address", "").strip()
        edit_id_post = request.form.get("edit_id", type=int)

        if not address:
            flash("Адрес не может быть пустым.", "warning")
            return redirect(url_for("index"))

        try:
            result = geocode_address(address)
            if not result:
                flash("Адрес не найден. Попробуйте другой.", "danger")
                return redirect(url_for("index"))

            found_address, lat, lon = result
            coords = (lat, lon)

            # Проверка номера дома
            user_number = re.findall(r'\d+', address)
            found_number = re.findall(r'\d+', found_address)
            if (user_number and found_number
               and user_number[0] != found_number[0]):
                flash(f'''Введённый номер дома {user_number[0]}
                       отличается от найденного {found_number[0]}.
                       Адрес найден приблизительно.''', "warning")
            else:
                flash(f"Адрес найден: {found_address}", "success")

            # Сохраняем в базу
            try:
                if edit_id_post:
                    entry = History.query.get(edit_id_post)
                    entry.address = found_address
                    entry.latitude = lat
                    entry.longitude = lon
                else:
                    entry = History(address=found_address,
                                    latitude=lat, longitude=lon)
                    db.session.add(entry)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                flash("Ошибка при сохранении в базе данных.", "danger")

            session["coords"] = coords

        except RequestException:
            flash("Ошибка подключения к геокодеру. Попробуйте позже.",
                  "danger")
        except ValueError:
            flash("Ошибка обработки ответа геокодера.", "danger")

        return redirect(url_for("index"))

    history = History.query.order_by(History.created_at.desc()).limit(10).all()
    return render_template("index.html", coords=coords, history=history,
                           address=address, edit_id=edit_id)
