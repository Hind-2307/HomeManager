from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import date, datetime

app = Flask(__name__)

FOODS_FILE = "foods.json"
MEDICINES_FILE = "medicines.json"
KITCHEN_FILE = "kitchen.json"


# =========================
# DATA FUNCTIONS
# =========================

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except Exception:
            pass

    return []


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# =========================
# DATA CONVERSION
# =========================

def normalize_food(food):
    if isinstance(food, dict):
        return {
            "name": food.get("name", ""),
            "expiry": food.get("expiry", ""),
            "quantity": food.get("quantity", "")
        }

    if isinstance(food, list):
        return {
            "name": food[0] if len(food) > 0 else "",
            "expiry": food[1] if len(food) > 1 else "",
            "quantity": food[2] if len(food) > 2 else ""
        }

    return {
        "name": "",
        "expiry": "",
        "quantity": ""
    }


def normalize_kitchen(item):
    if isinstance(item, dict):
        return {
            "name": item.get("name", ""),
            "category": item.get("category", ""),
            "quantity": item.get("quantity", "")
        }

    if isinstance(item, list):
        return {
            "name": item[0] if len(item) > 0 else "",
            "category": item[1] if len(item) > 1 else "",
            "quantity": item[2] if len(item) > 2 else ""
        }

    return {
        "name": "",
        "category": "",
        "quantity": ""
    }


def normalize_medicine(medicine):
    if isinstance(medicine, dict):
        return {
            "name": medicine.get("name", ""),
            "quantity": medicine.get("quantity", ""),
            "minimum": medicine.get("minimum", ""),
            "dose": medicine.get("dose", ""),
            "time": medicine.get("time", ""),
            "expiry": medicine.get("expiry", "")
        }

    if isinstance(medicine, list):
        return {
            "name": medicine[0] if len(medicine) > 0 else "",
            "quantity": medicine[1] if len(medicine) > 1 else "",
            "minimum": medicine[2] if len(medicine) > 2 else "",
            "dose": medicine[3] if len(medicine) > 3 else "",
            "time": medicine[4] if len(medicine) > 4 else "",
            "expiry": medicine[5] if len(medicine) > 5 else ""
        }

    return {
        "name": "",
        "quantity": "",
        "minimum": "",
        "dose": "",
        "time": "",
        "expiry": ""
    }


# =========================
# STATUS FUNCTIONS
# =========================

def expiry_status(expiry):
    if not expiry:
        return "normal"

    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        today = date.today()

        days_left = (expiry_date - today).days

        if days_left < 0:
            return "expired"

        if days_left <= 3:
            return "soon"

        return "normal"

    except Exception:
        return "normal"


def medicine_quantity_status(quantity, minimum):
    try:
        current = float(quantity)
        minimum_value = float(minimum)

        if current <= minimum_value:
            return "low"

    except Exception:
        pass

    return "normal"


# =========================
# RECIPES
# =========================

recipes = {
    "Chicken Rice": ["chicken", "rice", "onion", "oil", "salt"],
    "Pasta with Tomato Sauce": ["pasta", "tomato", "onion", "oil", "salt"],
    "Egg Sandwich": ["egg", "bread", "cheese", "salt"],
    "Chicken Pasta": ["chicken", "pasta", "onion", "oil", "salt"],
    "Omelette": ["egg", "onion", "tomato", "salt", "oil"],
    "Rice and Eggs": ["rice", "egg", "oil", "salt"],
    "Tuna Sandwich": ["tuna", "bread", "cheese"],
    "Tomato Pasta": ["pasta", "tomato", "oil", "salt"]
}


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# FOODS
# =========================

@app.route("/foods")
def foods():

    raw_foods = load_data(FOODS_FILE)

    foods_list = []

    for food in raw_foods:

        item = normalize_food(food)

        item["status"] = expiry_status(item["expiry"])

        foods_list.append(item)

    return render_template(
        "foods.html",
        foods=foods_list
    )


@app.route("/add_food", methods=["POST"])
def add_food():

    name = request.form.get("name")
    expiry = request.form.get("expiry")
    quantity = request.form.get("quantity")

    if name and expiry and quantity:

        foods_list = load_data(FOODS_FILE)

        foods_list.append({
            "name": name,
            "expiry": expiry,
            "quantity": quantity
        })

        save_data(
            FOODS_FILE,
            foods_list
        )

    return redirect(url_for("foods"))


@app.route("/delete_food/<int:index>")
def delete_food(index):

    foods_list = load_data(FOODS_FILE)

    if 0 <= index < len(foods_list):

        foods_list.pop(index)

        save_data(
            FOODS_FILE,
            foods_list
        )

    return redirect(url_for("foods"))


# =========================
# KITCHEN
# =========================

@app.route("/kitchen")
def kitchen():

    raw_kitchen = load_data(KITCHEN_FILE)

    kitchen_list = [
        normalize_kitchen(item)
        for item in raw_kitchen
    ]

    return render_template(
        "kitchen.html",
        kitchen=kitchen_list
    )


@app.route("/add_kitchen", methods=["POST"])
def add_kitchen():

    name = request.form.get("name")
    category = request.form.get("category")
    quantity = request.form.get("quantity")

    if name and category and quantity:

        kitchen_list = load_data(KITCHEN_FILE)

        kitchen_list.append({
            "name": name,
            "category": category,
            "quantity": quantity
        })

        save_data(
            KITCHEN_FILE,
            kitchen_list
        )

    return redirect(url_for("kitchen"))


@app.route("/delete_kitchen/<int:index>")
def delete_kitchen(index):

    kitchen_list = load_data(KITCHEN_FILE)

    if 0 <= index < len(kitchen_list):

        kitchen_list.pop(index)

        save_data(
            KITCHEN_FILE,
            kitchen_list
        )

    return redirect(url_for("kitchen"))


# =========================
# MEDICINES
# =========================

@app.route("/medicines")
def medicines():

    raw_medicines = load_data(MEDICINES_FILE)

    medicines_list = []

    for medicine in raw_medicines:

        item = normalize_medicine(medicine)

        item["expiry_status"] = expiry_status(
            item["expiry"]
        )

        item["quantity_status"] = medicine_quantity_status(
            item["quantity"],
            item["minimum"]
        )

        medicines_list.append(item)

    return render_template(
        "medicines.html",
        medicines=medicines_list
    )


@app.route("/add_medicine", methods=["POST"])
def add_medicine():

    name = request.form.get("name")
    quantity = request.form.get("quantity")
    minimum = request.form.get("minimum")
    dose = request.form.get("dose")
    time = request.form.get("time")
    expiry = request.form.get("expiry")

    if (
        name
        and quantity
        and minimum
        and dose
        and time
        and expiry
    ):

        medicines_list = load_data(
            MEDICINES_FILE
        )

        medicines_list.append({
            "name": name,
            "quantity": quantity,
            "minimum": minimum,
            "dose": dose,
            "time": time,
            "expiry": expiry
        })

        save_data(
            MEDICINES_FILE,
            medicines_list
        )

    return redirect(url_for("medicines"))


@app.route("/delete_medicine/<int:index>")
def delete_medicine(index):

    medicines_list = load_data(
        MEDICINES_FILE
    )

    if 0 <= index < len(medicines_list):

        medicines_list.pop(index)

        save_data(
            MEDICINES_FILE,
            medicines_list
        )

    return redirect(url_for("medicines"))


# =========================
# RECIPES
# =========================

@app.route("/recipes")
def recipes_page():

    return render_template(
        "recipes.html",
        results=None
    )


@app.route("/find_recipes", methods=["POST"])
def find_recipes():

    raw_foods = load_data(
        FOODS_FILE
    )

    raw_kitchen = load_data(
        KITCHEN_FILE
    )

    foods_list = [
        normalize_food(food)
        for food in raw_foods
    ]

    kitchen_list = [
        normalize_kitchen(item)
        for item in raw_kitchen
    ]

    available = set()

    for food in foods_list:

        name = food["name"].strip().lower()

        if name:
            available.add(name)

    for item in kitchen_list:

        name = item["name"].strip().lower()

        if name:
            available.add(name)

    results = []

    for recipe_name, ingredients in recipes.items():

        available_ingredients = []
        missing_ingredients = []

        for ingredient in ingredients:

            if ingredient.lower() in available:

                available_ingredients.append(
                    ingredient
                )

            else:

                missing_ingredients.append(
                    ingredient
                )

        percentage = int(
            len(available_ingredients)
            / len(ingredients)
            * 100
        )

        results.append({
            "name": recipe_name,
            "percentage": percentage,
            "available": available_ingredients,
            "missing": missing_ingredients
        })

    results.sort(
        key=lambda recipe: recipe["percentage"],
        reverse=True
    )

    return render_template(
        "recipes.html",
        results=results
    )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )