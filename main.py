import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
from plyer import notification
import json
import os
import sys
import random



if getattr(sys, "frozen", False):
    APP_FOLDER = os.path.dirname(sys.executable)
else:
    APP_FOLDER = os.path.dirname(os.path.abspath(__file__))



FOODS_FILE = os.path.join(APP_FOLDER, "foods.json")
MEDICINES_FILE = os.path.join(APP_FOLDER, "medicines.json")
KITCHEN_FILE = os.path.join(APP_FOLDER, "kitchen.json")



foods = []
medicines = []
kitchen_items = []

language = "en"

recipe_matches = []



ROOT_BG = "#EAF4EA"
HEADER_GREEN = "#2E6B4E"
PAGE_BG = "#F7FAF7"
TEXT_GREEN = "#2E6B4E"
DELETE_RED = "#B85450"
WARNING_YELLOW = "#D49A2A"
SECONDARY_GREEN = "#5C8D89"



recipes = {
    "Chicken Rice": [
        "chicken",
        "rice",
        "onion",
        "oil",
        "salt"
    ],

    "Pasta with Tomato Sauce": [
        "pasta",
        "tomato",
        "onion",
        "oil",
        "salt"
    ],

    "Egg Sandwich": [
        "egg",
        "bread",
        "cheese",
        "salt"
    ],

    "Chicken Pasta": [
        "chicken",
        "pasta",
        "onion",
        "oil",
        "salt"
    ],

    "Omelette": [
        "egg",
        "onion",
        "tomato",
        "salt",
        "oil"
    ],

    "Rice and Eggs": [
        "rice",
        "egg",
        "oil",
        "salt"
    ],

    "Tuna Sandwich": [
        "tuna",
        "bread",
        "cheese"
    ],

    "Tomato Pasta": [
        "pasta",
        "tomato",
        "oil",
        "salt"
    ]
}



def save_foods():
    with open(FOODS_FILE, "w", encoding="utf-8") as file:
        json.dump(foods, file, ensure_ascii=False, indent=4)


def load_foods():
    global foods

    if os.path.exists(FOODS_FILE):
        try:
            with open(FOODS_FILE, "r", encoding="utf-8") as file:
                foods = json.load(file)
        except:
            foods = []
    else:
        foods = []


def add_food():
    name = food_name_entry.get().strip()
    expiry = food_expiry_entry.get().strip()
    quantity = food_quantity_entry.get().strip()

    if not name or not expiry or not quantity:
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Error",
            "Expiry date must be in this format: YYYY-MM-DD"
        )
        return

    foods.append([
        name,
        expiry,
        quantity
    ])

    save_foods()
    refresh_food_list()

    food_name_entry.delete(0, tk.END)
    food_expiry_entry.delete(0, tk.END)
    food_quantity_entry.delete(0, tk.END)


def refresh_food_list():
    food_listbox.delete(0, tk.END)

    for food in foods:
        if len(food) >= 3:
            food_listbox.insert(
                tk.END,
                f"{food[0]} | Expiry: {food[1]} | Quantity: {food[2]}"
            )


def delete_selected_food():
    selected = food_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an item first."
        )
        return

    index = selected[0]

    del foods[index]

    save_foods()
    refresh_food_list()


def check_expiry():
    today = date.today()
    warnings = []

    for food in foods:
        if len(food) < 3:
            continue

        try:
            expiry_date = datetime.strptime(
                food[1],
                "%Y-%m-%d"
            ).date()

            days_left = (expiry_date - today).days

            if days_left < 0:
                warnings.append(
                    f"{food[0]} has expired."
                )

            elif days_left <= 3:
                warnings.append(
                    f"{food[0]} expires in {days_left} day(s)."
                )

        except:
            pass

    if warnings:
        messagebox.showwarning(
            "Food Expiry Warning",
            "\n".join(warnings)
        )
    else:
        messagebox.showinfo(
            "Food Expiry",
            "No food items are close to expiry."
        )


def suggest_recipes():
    if not foods:
        messagebox.showinfo(
            "Recipe Suggestion",
            "Add some foods first."
        )
        return

    available_foods = [food[0] for food in foods]

    messagebox.showinfo(
        "Recipe Suggestion",
        "Available foods:\n\n" +
        "\n".join(available_foods[:3])
    )



def save_medicines():
    with open(MEDICINES_FILE, "w", encoding="utf-8") as file:
        json.dump(
            medicines,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_medicines():
    global medicines

    if os.path.exists(MEDICINES_FILE):
        try:
            with open(MEDICINES_FILE, "r", encoding="utf-8") as file:
                medicines = json.load(file)
        except:
            medicines = []
    else:
        medicines = []


def add_medicine():
    name = medicine_name_entry.get().strip()
    quantity = medicine_quantity_entry.get().strip()
    minimum = medicine_minimum_entry.get().strip()
    dose = medicine_dose_entry.get().strip()
    time = medicine_time_entry.get().strip()
    expiry = medicine_expiry_entry.get().strip()

    if not name or not quantity or not minimum or not dose or not time or not expiry:
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        quantity = int(quantity)
        minimum = int(minimum)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Quantity and minimum quantity must be numbers."
        )
        return

    try:
        datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Error",
            "Expiry date must be in this format: YYYY-MM-DD"
        )
        return

    medicines.append([
        name,
        quantity,
        minimum,
        dose,
        time,
        expiry
    ])

    save_medicines()
    refresh_medicine_list()

    medicine_name_entry.delete(0, tk.END)
    medicine_quantity_entry.delete(0, tk.END)
    medicine_minimum_entry.delete(0, tk.END)
    medicine_dose_entry.delete(0, tk.END)
    medicine_time_entry.delete(0, tk.END)
    medicine_expiry_entry.delete(0, tk.END)


def refresh_medicine_list():
    medicine_listbox.delete(0, tk.END)

    for medicine in medicines:
        if len(medicine) >= 6:
            medicine_listbox.insert(
                tk.END,
                f"{medicine[0]} | Qty: {medicine[1]} | "
                f"Min: {medicine[2]} | Dose: {medicine[3]} | "
                f"Time: {medicine[4]} | Expiry: {medicine[5]}"
            )


def delete_selected_medicine():
    selected = medicine_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a medicine first."
        )
        return

    index = selected[0]

    del medicines[index]

    save_medicines()
    refresh_medicine_list()


def check_medicine_expiry():
    today = date.today()
    warnings = []

    for medicine in medicines:
        if len(medicine) < 6:
            continue

        try:
            expiry_date = datetime.strptime(
                medicine[5],
                "%Y-%m-%d"
            ).date()

            days_left = (expiry_date - today).days

            if days_left < 0:
                warnings.append(
                    f"{medicine[0]} has expired."
                )

            elif days_left <= 7:
                warnings.append(
                    f"{medicine[0]} expires in {days_left} day(s)."
                )

        except:
            pass

    if warnings:
        messagebox.showwarning(
            "Medicine Expiry Warning",
            "\n".join(warnings)
        )
    else:
        messagebox.showinfo(
            "Medicine Expiry",
            "No medicines are close to expiry."
        )


def check_low_medicine_quantity():
    warnings = []

    for medicine in medicines:
        if len(medicine) < 6:
            continue

        try:
            quantity = int(medicine[1])
            minimum = int(medicine[2])

            if quantity <= minimum:
                warnings.append(
                    f"{medicine[0]} quantity is low."
                )

        except:
            pass

    if warnings:
        messagebox.showwarning(
            "Low Medicine Quantity",
            "\n".join(warnings)
        )
    else:
        messagebox.showinfo(
            "Medicine Quantity",
            "All medicine quantities are sufficient."
        )


def check_medicine_time():
    current_time = datetime.now().strftime("%H:%M")

    for medicine in medicines:
        if len(medicine) < 6:
            continue

        if medicine[4] == current_time:
            notification.notify(
                title="Home Manager",
                message=f"Time to take {medicine[0]}",
                timeout=10
            )

    root.after(60000, check_medicine_time)




def save_kitchen_items():
    with open(KITCHEN_FILE, "w", encoding="utf-8") as file:
        json.dump(
            kitchen_items,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_kitchen_items():
    global kitchen_items

    if os.path.exists(KITCHEN_FILE):
        try:
            with open(KITCHEN_FILE, "r", encoding="utf-8") as file:
                kitchen_items = json.load(file)
        except:
            kitchen_items = []
    else:
        kitchen_items = []


def add_kitchen_item():
    name = kitchen_name_entry.get().strip()
    category = kitchen_category_entry.get().strip()
    quantity = kitchen_quantity_entry.get().strip()

    if not name or not category or not quantity:
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    kitchen_items.append([
        name,
        category,
        quantity
    ])

    save_kitchen_items()
    refresh_kitchen_list()

    kitchen_name_entry.delete(0, tk.END)
    kitchen_category_entry.delete(0, tk.END)
    kitchen_quantity_entry.delete(0, tk.END)


def refresh_kitchen_list():
    kitchen_listbox.delete(0, tk.END)

    for item in kitchen_items:
        if len(item) >= 3:
            kitchen_listbox.insert(
                tk.END,
                f"{item[0]} | Category: {item[1]} | Quantity: {item[2]}"
            )


def delete_selected_kitchen_item():
    selected = kitchen_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an item first."
        )
        return

    index = selected[0]

    del kitchen_items[index]

    save_kitchen_items()
    refresh_kitchen_list()




def get_available_ingredients():
    available = []

    for food in foods:
        if len(food) >= 1:
            available.append(
                food[0].strip().lower()
            )

    for item in kitchen_items:
        if len(item) >= 1:
            available.append(
                item[0].strip().lower()
            )

    return available


def calculate_recipe_matches():
    available = get_available_ingredients()

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

        total = len(ingredients)

        if total > 0:
            percentage = round(
                (len(available_ingredients) / total) * 100
            )
        else:
            percentage = 0

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

    return results


def find_recipe_matches():
    global recipe_matches

    available = get_available_ingredients()

    if not available:
        messagebox.showwarning(
            "No Ingredients",
            "Please add some foods or kitchen resources first."
        )
        return

    recipe_matches = calculate_recipe_matches()

    recipe_results_listbox.delete(
        0,
        tk.END
    )

    for result in recipe_matches:

        if result["percentage"] == 100:

            text = (
                f"✓ {result['name']} "
                f"- {result['percentage']}% Match "
                f"- You can make this!"
            )

        else:

            text = (
                f"• {result['name']} "
                f"- {result['percentage']}% Match "
                f"- Missing: "
                f"{', '.join(result['missing'])}"
            )

        recipe_results_listbox.insert(
            tk.END,
            text
        )


def show_recipe_details():
    selected = recipe_results_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a recipe first."
        )
        return

    index = selected[0]

    if index >= len(recipe_matches):
        return

    result = recipe_matches[index]

    recipe_name = result["name"]

    ingredients = recipes[recipe_name]

    details = (
        f"Recipe: {recipe_name}\n\n"
        f"Match: {result['percentage']}%\n\n"
    )

    details += "Ingredients:\n"

    for ingredient in ingredients:

        if ingredient in result["available"]:
            details += f"✓ {ingredient}\n"
        else:
            details += f"✗ {ingredient}\n"

    if result["missing"]:

        details += "\nMissing ingredients:\n"

        for ingredient in result["missing"]:
            details += f"• {ingredient}\n"

    else:

        details += (
            "\nYou have all the ingredients!\n"
            "You can make this recipe."
        )

    messagebox.showinfo(
        recipe_name,
        details
    )


def surprise_me():
    global recipe_matches

    available = get_available_ingredients()

    if not available:
        messagebox.showwarning(
            "Surprise Me",
            "Please add some foods or kitchen resources first."
        )
        return

    recipe_matches = calculate_recipe_matches()

    suitable_recipes = [
        recipe
        for recipe in recipe_matches
        if recipe["percentage"] >= 50
    ]

    if not suitable_recipes:
        messagebox.showinfo(
            "Surprise Me",
            "You don't have enough ingredients "
            "for the available recipes yet."
        )
        return

    selected_recipe = random.choice(
        suitable_recipes
    )

    recipe_results_listbox.delete(
        0,
        tk.END
    )

    selected_index = recipe_matches.index(
        selected_recipe
    )

    for result in recipe_matches:

        if result["percentage"] == 100:

            text = (
                f"✓ {result['name']} "
                f"- {result['percentage']}% Match "
                f"- You can make this!"
            )

        else:

            text = (
                f"• {result['name']} "
                f"- {result['percentage']}% Match "
                f"- Missing: "
                f"{', '.join(result['missing'])}"
            )

        recipe_results_listbox.insert(
            tk.END,
            text
        )

    recipe_results_listbox.selection_set(
        selected_index
    )

    recipe_results_listbox.see(
        selected_index
    )

    messagebox.showinfo(
        "Surprise Me!",
        f"How about:\n\n"
        f"{selected_recipe['name']}\n\n"
        f"Match: {selected_recipe['percentage']}%"
    )



def show_page(page):
    home_page.pack_forget()
    food_page.pack_forget()
    medicine_page.pack_forget()
    kitchen_page.pack_forget()
    recipe_page.pack_forget()

    page.pack(
        fill="both",
        expand=True
    )


def show_home():
    show_page(home_page)


def show_foods():
    show_page(food_page)


def show_medicines():
    show_page(medicine_page)


def show_kitchen():
    show_page(kitchen_page)


def show_recipes():
    show_page(recipe_page)




def change_language():
    global language

    if language == "en":
        language = "ar"
    else:
        language = "en"

    update_language()


def update_language():

    if language == "en":


        title_label.config(text="Home Manager")
        subtitle_label.config(
            text="Organize your home resources easily"
        )
        question_label.config(
            text="What would you like to manage today?"
        )

        foods_button.config(text="Foods")
        kitchen_button.config(text="Kitchen Cabinet")
        medicines_button.config(text="Medicines")
        recipes_button.config(text="What Should I Cook?")

        language_button.config(text="AR 🌐")


        food_title.config(text="Foods")
        food_name_label.config(text="Food Name")
        food_expiry_label.config(text="Expiry Date")
        food_quantity_label.config(text="Quantity")

        food_add_button.config(text="Add Food")
        food_delete_button.config(text="Delete Selected")
        food_expiry_button.config(text="Check Expiry")
        food_recipe_button.config(text="Suggest Recipes")
        food_home_button.config(text="Home")


        medicine_title.config(text="Medicines")
        medicine_name_label.config(text="Medicine Name")
        medicine_quantity_label.config(text="Quantity")
        medicine_minimum_label.config(text="Minimum Quantity")
        medicine_dose_label.config(text="Dose")
        medicine_time_label.config(text="Time")
        medicine_expiry_label.config(text="Expiry Date")

        medicine_add_button.config(text="Add Medicine")
        medicine_delete_button.config(text="Delete Selected")
        medicine_expiry_button.config(text="Check Expiry")
        medicine_quantity_button.config(
            text="Check Low Quantity"
        )
        medicine_home_button.config(text="Home")


        kitchen_title.config(text="Kitchen Cabinet")
        kitchen_name_label.config(text="Resource Name")
        kitchen_category_label.config(text="Category")
        kitchen_quantity_label.config(text="Quantity")
        kitchen_add_button.config(text="Add Resource")
        kitchen_delete_button.config(text="Delete Selected")
        kitchen_home_button.config(text="Home")


        recipe_title.config(text="What Should I Cook?")
        recipe_description.config(
            text="Find the ingredients you have and the ones you need."
        )
        recipe_search_button.config(
            text="Find Recipes"
        )
        recipe_surprise_button.config(
            text="Surprise Me!"
        )
        recipe_details_button.config(
            text="View Recipe Details"
        )
        recipe_home_button.config(
            text="Home"
        )

    else:


        title_label.config(text="مدير المنزل")
        subtitle_label.config(
            text="نظّم موارد منزلك بسهولة"
        )
        question_label.config(
            text="ماذا تريدين أن تديري اليوم؟"
        )

        foods_button.config(text="الأطعمة")
        kitchen_button.config(text="خزانة المطبخ")
        medicines_button.config(text="الأدوية")
        recipes_button.config(text="ماذا أطبخ؟")

        language_button.config(text="EN 🌐")


        food_title.config(text="الأطعمة")
        food_name_label.config(text="اسم الطعام")
        food_expiry_label.config(text="تاريخ الانتهاء")
        food_quantity_label.config(text="الكمية")

        food_add_button.config(text="إضافة طعام")
        food_delete_button.config(text="حذف المحدد")
        food_expiry_button.config(text="فحص الانتهاء")
        food_recipe_button.config(text="اقتراح وصفات")
        food_home_button.config(text="الرئيسية")


        medicine_title.config(text="الأدوية")
        medicine_name_label.config(text="اسم الدواء")
        medicine_quantity_label.config(text="الكمية")
        medicine_minimum_label.config(
            text="الحد الأدنى للكمية"
        )
        medicine_dose_label.config(text="الجرعة")
        medicine_time_label.config(text="الوقت")
        medicine_expiry_label.config(
            text="تاريخ الانتهاء"
        )

        medicine_add_button.config(
            text="إضافة دواء"
        )
        medicine_delete_button.config(
            text="حذف المحدد"
        )
        medicine_expiry_button.config(
            text="فحص الانتهاء"
        )
        medicine_quantity_button.config(
            text="فحص الكمية المنخفضة"
        )

        medicine_home_button.config(
            text="الرئيسية"
        )


        kitchen_title.config(
            text="خزانة المطبخ"
        )
        kitchen_name_label.config(
            text="اسم المورد"
        )
        kitchen_category_label.config(
            text="التصنيف"
        )
        kitchen_quantity_label.config(
            text="الكمية"
        )
        kitchen_add_button.config(
            text="إضافة مورد"
        )
        kitchen_delete_button.config(
            text="حذف المحدد"
        )

        kitchen_home_button.config(
            text="الرئيسية"
        )



        recipe_title.config(
            text="ماذا أطبخ؟"
        )
        recipe_description.config(
            text="اعرفي المكونات الموجودة والمكونات التي تحتاجينها."
        )
        recipe_search_button.config(
            text="البحث عن وصفات"
        )
        recipe_surprise_button.config(
            text="فاجئيني!"
        )
        recipe_details_button.config(
            text="عرض تفاصيل الوصفة"
        )
        recipe_home_button.config(
            text="الرئيسية"
        )



root = tk.Tk()

root.title("Home Manager")
root.geometry("900x750")
root.minsize(800, 650)
root.configure(bg=ROOT_BG)




header = tk.Frame(
    root,
    bg=HEADER_GREEN,
    height=120
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title_label = tk.Label(
    header,
    text="Home Manager",
    font=("Arial", 28, "bold"),
    bg=HEADER_GREEN,
    fg="white"
)

title_label.pack(
    pady=(20, 0)
)


subtitle_label = tk.Label(
    header,
    text="Organize your home resources easily",
    font=("Arial", 12),
    bg=HEADER_GREEN,
    fg="white"
)

subtitle_label.pack()


language_button = tk.Button(
    header,
    text="AR 🌐",
    command=change_language,
    font=("Arial", 10, "bold"),
    bg="white",
    fg=HEADER_GREEN,
    relief="flat",
    padx=10
)

language_button.place(
    relx=0.95,
    rely=0.5,
    anchor="e"
)



home_page = tk.Frame(
    root,
    bg=PAGE_BG
)

question_label = tk.Label(
    home_page,
    text="What would you like to manage today?",
    font=("Arial", 20, "bold"),
    bg=PAGE_BG,
    fg=TEXT_GREEN
)

question_label.pack(
    pady=(40, 30)
)


cards_frame = tk.Frame(
    home_page,
    bg=PAGE_BG
)

cards_frame.pack()


foods_button = tk.Button(
    cards_frame,
    text="Foods",
    command=show_foods,
    font=("Arial", 16, "bold"),
    bg="white",
    fg=TEXT_GREEN,
    width=25,
    height=3,
    relief="flat"
)

foods_button.grid(
    row=0,
    column=0,
    padx=15,
    pady=15
)


kitchen_button = tk.Button(
    cards_frame,
    text="Kitchen Cabinet",
    command=show_kitchen,
    font=("Arial", 16, "bold"),
    bg="white",
    fg=TEXT_GREEN,
    width=25,
    height=3,
    relief="flat"
)

kitchen_button.grid(
    row=0,
    column=1,
    padx=15,
    pady=15
)


medicines_button = tk.Button(
    cards_frame,
    text="Medicines",
    command=show_medicines,
    font=("Arial", 16, "bold"),
    bg="white",
    fg=TEXT_GREEN,
    width=25,
    height=3,
    relief="flat"
)

medicines_button.grid(
    row=1,
    column=0,
    padx=15,
    pady=15
)


recipes_button = tk.Button(
    cards_frame,
    text="What Should I Cook?",
    command=show_recipes,
    font=("Arial", 16, "bold"),
    bg="white",
    fg=SECONDARY_GREEN,
    width=25,
    height=3,
    relief="flat"
)

recipes_button.grid(
    row=1,
    column=1,
    padx=15,
    pady=15
)



food_page = tk.Frame(
    root,
    bg=PAGE_BG
)


food_home_button = tk.Button(
    food_page,
    text="Home",
    command=show_home,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5
)

food_home_button.pack(
    anchor="ne",
    padx=25,
    pady=(15, 0)
)

food_title = tk.Label(
    food_page,
    text="Foods",
    font=("Arial", 24, "bold"),
    bg=PAGE_BG,
    fg=TEXT_GREEN
)

food_title.pack(pady=(5, 20))



food_form = tk.Frame(
    food_page,
    bg="white",
    padx=20,
    pady=15
)

food_form.pack(
    padx=30,
    pady=5
)



food_name_label = tk.Label(
    food_form,
    text="Food Name",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

food_name_label.grid(
    row=0,
    column=0,
    padx=8,
    pady=(0, 5)
)

food_name_entry = tk.Entry(
    food_form,
    width=22
)

food_name_entry.grid(
    row=1,
    column=0,
    padx=8
)



food_expiry_label = tk.Label(
    food_form,
    text="Expiry Date",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

food_expiry_label.grid(
    row=0,
    column=1,
    padx=8,
    pady=(0, 5)
)

food_expiry_entry = tk.Entry(
    food_form,
    width=22
)

food_expiry_entry.grid(
    row=1,
    column=1,
    padx=8
)



food_quantity_label = tk.Label(
    food_form,
    text="Quantity",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

food_quantity_label.grid(
    row=0,
    column=2,
    padx=8,
    pady=(0, 5)
)

food_quantity_entry = tk.Entry(
    food_form,
    width=22
)

food_quantity_entry.grid(
    row=1,
    column=2,
    padx=8
)



food_add_button = tk.Button(
    food_page,
    text="Add Food",
    command=add_food,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

food_add_button.pack(pady=12)



food_listbox = tk.Listbox(
    food_page,
    width=90,
    height=9,
    font=("Arial", 10)
)

food_listbox.pack(
    padx=30,
    pady=5
)



food_actions = tk.Frame(
    food_page,
    bg=PAGE_BG
)

food_actions.pack(pady=10)


food_delete_button = tk.Button(
    food_actions,
    text="Delete Selected",
    command=delete_selected_food,
    bg=DELETE_RED,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

food_delete_button.grid(
    row=0,
    column=0,
    padx=5
)


food_expiry_button = tk.Button(
    food_actions,
    text="Check Expiry",
    command=check_expiry,
    bg=WARNING_YELLOW,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

food_expiry_button.grid(
    row=0,
    column=1,
    padx=5
)


food_recipe_button = tk.Button(
    food_actions,
    text="Suggest Recipes",
    command=suggest_recipes,
    bg=SECONDARY_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

food_recipe_button.grid(
    row=0,
    column=2,
    padx=5
)



medicine_page = tk.Frame(
    root,
    bg=PAGE_BG
)


medicine_home_button = tk.Button(
    medicine_page,
    text="Home",
    command=show_home,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5
)

medicine_home_button.pack(
    anchor="ne",
    padx=25,
    pady=(15, 0)
)


medicine_title = tk.Label(
    medicine_page,
    text="Medicines",
    font=("Arial", 24, "bold"),
    bg=PAGE_BG,
    fg=TEXT_GREEN
)

medicine_title.pack(pady=(5, 15))



medicine_form = tk.Frame(
    medicine_page,
    bg="white",
    padx=20,
    pady=15
)

medicine_form.pack(
    padx=25,
    pady=5
)




medicine_name_label = tk.Label(
    medicine_form,
    text="Medicine Name",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

medicine_name_label.grid(
    row=0,
    column=0,
    padx=7,
    pady=(0, 5)
)

medicine_name_entry = tk.Entry(
    medicine_form,
    width=20
)

medicine_name_entry.grid(
    row=1,
    column=0,
    padx=7
)


medicine_quantity_label = tk.Label(
    medicine_form,
    text="Quantity",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

medicine_quantity_label.grid(
    row=0,
    column=1,
    padx=7,
    pady=(0, 5)
)

medicine_quantity_entry = tk.Entry(
    medicine_form,
    width=15
)

medicine_quantity_entry.grid(
    row=1,
    column=1,
    padx=7
)


medicine_minimum_label = tk.Label(
    medicine_form,
    text="Minimum Quantity",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

medicine_minimum_label.grid(
    row=0,
    column=2,
    padx=7,
    pady=(0, 5)
)

medicine_minimum_entry = tk.Entry(
    medicine_form,
    width=18
)

medicine_minimum_entry.grid(
    row=1,
    column=2,
    padx=7
)




medicine_dose_label = tk.Label(
    medicine_form,
    text="Dose",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

medicine_dose_label.grid(
    row=2,
    column=0,
    padx=7,
    pady=(15, 5)
)

medicine_dose_entry = tk.Entry(
    medicine_form,
    width=20
)

medicine_dose_entry.grid(
    row=3,
    column=0,
    padx=7
)


medicine_time_label = tk.Label(
    medicine_form,
    text="Time",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

medicine_time_label.grid(
    row=2,
    column=1,
    padx=7,
    pady=(15, 5)
)

medicine_time_entry = tk.Entry(
    medicine_form,
    width=15
)

medicine_time_entry.grid(
    row=3,
    column=1,
    padx=7
)


medicine_expiry_label = tk.Label(
    medicine_form,
    text="Expiry Date",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

medicine_expiry_label.grid(
    row=2,
    column=2,
    padx=7,
    pady=(15, 5)
)

medicine_expiry_entry = tk.Entry(
    medicine_form,
    width=18
)

medicine_expiry_entry.grid(
    row=3,
    column=2,
    padx=7
)



medicine_add_button = tk.Button(
    medicine_page,
    text="Add Medicine",
    command=add_medicine,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=20,
    relief="flat"
)

medicine_add_button.pack(pady=12)



medicine_listbox = tk.Listbox(
    medicine_page,
    width=105,
    height=7,
    font=("Arial", 10)
)

medicine_listbox.pack(
    padx=20,
    pady=5
)



medicine_actions = tk.Frame(
    medicine_page,
    bg=PAGE_BG
)

medicine_actions.pack(pady=10)


medicine_delete_button = tk.Button(
    medicine_actions,
    text="Delete Selected",
    command=delete_selected_medicine,
    bg=DELETE_RED,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

medicine_delete_button.grid(
    row=0,
    column=0,
    padx=5
)


medicine_expiry_button = tk.Button(
    medicine_actions,
    text="Check Expiry",
    command=check_medicine_expiry,
    bg=WARNING_YELLOW,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

medicine_expiry_button.grid(
    row=0,
    column=1,
    padx=5
)


medicine_quantity_button = tk.Button(
    medicine_actions,
    text="Check Low Quantity",
    command=check_low_medicine_quantity,
    bg=SECONDARY_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=20,
    relief="flat"
)

medicine_quantity_button.grid(
    row=0,
    column=2,
    padx=5
)


kitchen_page = tk.Frame(
    root,
    bg=PAGE_BG
)


kitchen_home_button = tk.Button(
    kitchen_page,
    text="Home",
    command=show_home,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5
)

kitchen_home_button.pack(
    anchor="ne",
    padx=25,
    pady=(15, 0)
)


kitchen_title = tk.Label(
    kitchen_page,
    text="Kitchen Cabinet",
    font=("Arial", 24, "bold"),
    bg=PAGE_BG,
    fg=TEXT_GREEN
)

kitchen_title.pack(pady=(5, 20))



kitchen_form = tk.Frame(
    kitchen_page,
    bg="white",
    padx=20,
    pady=15
)

kitchen_form.pack(
    padx=30,
    pady=5
)



kitchen_name_label = tk.Label(
    kitchen_form,
    text="Resource Name",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

kitchen_name_label.grid(
    row=0,
    column=0,
    padx=8,
    pady=(0, 5)
)

kitchen_name_entry = tk.Entry(
    kitchen_form,
    width=22
)

kitchen_name_entry.grid(
    row=1,
    column=0,
    padx=8
)



kitchen_category_label = tk.Label(
    kitchen_form,
    text="Category",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

kitchen_category_label.grid(
    row=0,
    column=1,
    padx=8,
    pady=(0, 5)
)

kitchen_category_entry = tk.Entry(
    kitchen_form,
    width=22
)

kitchen_category_entry.grid(
    row=1,
    column=1,
    padx=8
)



kitchen_quantity_label = tk.Label(
    kitchen_form,
    text="Quantity",
    font=("Arial", 10, "bold"),
    bg="white",
    fg=TEXT_GREEN
)

kitchen_quantity_label.grid(
    row=0,
    column=2,
    padx=8,
    pady=(0, 5)
)

kitchen_quantity_entry = tk.Entry(
    kitchen_form,
    width=22
)

kitchen_quantity_entry.grid(
    row=1,
    column=2,
    padx=8
)



kitchen_add_button = tk.Button(
    kitchen_page,
    text="Add Resource",
    command=add_kitchen_item,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=20,
    relief="flat"
)

kitchen_add_button.pack(pady=12)



kitchen_listbox = tk.Listbox(
    kitchen_page,
    width=90,
    height=10,
    font=("Arial", 10)
)

kitchen_listbox.pack(
    padx=30,
    pady=5
)



kitchen_actions = tk.Frame(
    kitchen_page,
    bg=PAGE_BG
)

kitchen_actions.pack(pady=10)


kitchen_delete_button = tk.Button(
    kitchen_actions,
    text="Delete Selected",
    command=delete_selected_kitchen_item,
    bg=DELETE_RED,
    fg="white",
    font=("Arial", 10, "bold"),
    width=20,
    relief="flat"
)

kitchen_delete_button.grid(
    row=0,
    column=0,
    padx=5
)


recipe_page = tk.Frame(
    root,
    bg=PAGE_BG
)


recipe_home_button = tk.Button(
    recipe_page,
    text="Home",
    command=show_home,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5
)

recipe_home_button.pack(
    anchor="ne",
    padx=25,
    pady=(15, 0)
)


recipe_title = tk.Label(
    recipe_page,
    text="What Should I Cook?",
    font=("Arial", 24, "bold"),
    bg=PAGE_BG,
    fg=TEXT_GREEN
)

recipe_title.pack(pady=(5, 10))


recipe_description = tk.Label(
    recipe_page,
    text="Find recipes based on the ingredients you already have.",
    font=("Arial", 11),
    bg=PAGE_BG,
    fg="#555555"
)

recipe_description.pack(pady=(0, 20))



recipe_actions = tk.Frame(
    recipe_page,
    bg=PAGE_BG
)

recipe_actions.pack(pady=5)


recipe_search_button = tk.Button(
    recipe_actions,
    text="Find Recipes",
    command=find_recipe_matches,
    bg=HEADER_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

recipe_search_button.grid(
    row=0,
    column=0,
    padx=5
)


recipe_surprise_button = tk.Button(
    recipe_actions,
    text="Surprise Me",
    command=surprise_me,
    bg=SECONDARY_GREEN,
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    relief="flat"
)

recipe_surprise_button.grid(
    row=0,
    column=1,
    padx=5
)



recipe_results_listbox = tk.Listbox(
    recipe_page,
    width=90,
    height=12,
    font=("Arial", 10)
)

recipe_results_listbox.pack(
    padx=30,
    pady=15
)



recipe_details_button = tk.Button(
    recipe_page,
    text="View Recipe Details",
    command=show_recipe_details,
    bg=WARNING_YELLOW,
    fg="white",
    font=("Arial", 10, "bold"),
    width=22,
    relief="flat"
)

recipe_details_button.pack(
    pady=5
)


load_foods()
refresh_food_list()

load_medicines()
refresh_medicine_list()

load_kitchen_items()
refresh_kitchen_list()

show_home()

check_medicine_time()

root.mainloop()