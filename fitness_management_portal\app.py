"""
Fitness Management Portal

Console-based Python application for managing customer packages, class bookings,
trainer schedules, class planning, and business statistics.
"""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "fitness_data.json"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

CLASS_TYPES = ["Pilates", "Yoga", "MMA", "Boxing", "KPop Fitness"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
STUDIOS = {
    "Studio 1": {"capacity": 20, "cost": 20},
    "Studio 2": {"capacity": 20, "cost": 20},
    "Studio 3": {"capacity": 10, "cost": 12},
    "Studio 4": {"capacity": 10, "cost": 12},
}
PACKAGES = [
    {"id": 1, "class_type": "Pilates", "lessons": 10, "price": 300, "per_class": 30},
    {"id": 2, "class_type": "Pilates", "lessons": 30, "price": 660, "per_class": 22},
    {"id": 3, "class_type": "Yoga", "lessons": 10, "price": 300, "per_class": 30},
    {"id": 4, "class_type": "Yoga", "lessons": 30, "price": 660, "per_class": 22},
    {"id": 5, "class_type": "MMA", "lessons": 10, "price": 450, "per_class": 45},
    {"id": 6, "class_type": "MMA", "lessons": 30, "price": 1050, "per_class": 35},
    {"id": 7, "class_type": "Boxing", "lessons": 10, "price": 450, "per_class": 45},
    {"id": 8, "class_type": "Boxing", "lessons": 30, "price": 1050, "per_class": 35},
    {"id": 9, "class_type": "KPop Fitness", "lessons": 10, "price": 250, "per_class": 25},
    {"id": 10, "class_type": "KPop Fitness", "lessons": 30, "price": 600, "per_class": 20},
]
PROFIT_RATE = {"Pilates": 22, "Yoga": 22, "MMA": 35, "Boxing": 35, "KPop Fitness": 20}


def parse_date(value: str) -> date:
    return datetime.strptime(value, DATE_FORMAT).date()


def parse_time(value: str) -> time:
    return datetime.strptime(value, TIME_FORMAT).time()


def format_date(value: date) -> str:
    return value.strftime(DATE_FORMAT)


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def input_int(prompt: str, minimum: int | None = None, maximum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Please enter at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Please enter not more than {maximum}.")
            continue
        return value


def next_id(items: list[dict]) -> int:
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def default_trainers() -> list[dict]:
    return [
        make_trainer(1, "John Wick", ["MMA", "Boxing"], 120, ["Mon", "Tue", "Wed", "Thu"], ["08:00", "09:00", "15:00", "19:00"]),
        make_trainer(2, "Rocky Tan", ["MMA", "Boxing"], 100, ["Mon", "Wed", "Fri", "Sun"], ["08:00", "17:00", "19:30"]),
        make_trainer(3, "Linda Lee", ["Pilates", "Yoga"], 85, ["Mon", "Tue", "Thu", "Sat"], ["09:00", "11:00", "18:00"]),
        make_trainer(4, "Indira Raj", ["Yoga"], 90, ["Mon", "Tue", "Wed", "Fri"], ["08:00", "09:00", "15:00"]),
        make_trainer(5, "Vincent Koh", ["KPop Fitness"], 100, ["Tue", "Thu", "Sat", "Sun"], ["17:00", "18:00", "19:00"]),
        make_trainer(6, "Ray Vargas", ["Pilates", "KPop Fitness"], 90, ["Mon", "Wed", "Fri", "Sun"], ["10:00", "18:00", "19:00"]),
        make_trainer(7, "Dean Richards", ["MMA"], 110, ["Mon", "Tue", "Thu", "Sat"], ["15:00", "19:00"]),
        make_trainer(8, "Alice Booker", ["Yoga", "Pilates"], 88, ["Wed", "Thu", "Fri", "Sun"], ["09:00", "11:00", "16:00"]),
        make_trainer(9, "Janice Chew", ["KPop Fitness"], 95, ["Mon", "Wed", "Fri", "Sat"], ["17:00", "18:00"]),
    ]


def make_trainer(trainer_id: int, name: str, skills: list[str], hourly_rate: int, days: list[str], slots: list[str]) -> dict:
    availability = {day: slots[:] if day in days else [] for day in DAYS}
    return {
        "id": trainer_id,
        "name": name,
        "skills": skills,
        "hourly_rate": hourly_rate,
        "availability": availability,
    }


def create_empty_data() -> dict:
    return {
        "admins": [{"username": "admin", "password": "admin123"}],
        "customers": [],
        "trainers": default_trainers(),
        "classes": [],
        "bookings": [],
        "package_purchases": [],
    }


def load_data() -> dict:
    if not DATA_FILE.exists():
        DATA_DIR.mkdir(exist_ok=True)
        data = create_sample_data()
        save_data(data)
        return data
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data: dict) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def create_sample_data() -> dict:
    data = create_empty_data()
    random.seed(2026)
    create_sample_customers(data)
    create_sample_classes(data)
    create_sample_packages_and_bookings(data)
    return data


def create_sample_customers(data: dict) -> None:
    genders = ["Male", "Female"]
    for number in range(1, 321):
        data["customers"].append(
            {
                "id": number,
                "username": f"customer{number:03d}",
                "password": "pass123",
                "email": f"customer{number:03d}@example.com",
                "age": random.randint(18, 62),
                "gender": random.choice(genders),
                "packages": [],
            }
        )


def create_sample_classes(data: dict) -> None:
    start_day = date.today() - timedelta(days=180)
    start_day -= timedelta(days=start_day.weekday())
    trainer_by_skill = defaultdict(list)
    for trainer in data["trainers"]:
        for skill in trainer["skills"]:
            trainer_by_skill[skill].append(trainer)

    class_id = 1
    common_times = ["08:00", "09:00", "11:00", "15:00", "17:00", "18:00", "19:00", "19:30"]
    for offset in range(210):
        current_day = start_day + timedelta(days=offset)
        weekday = DAYS[current_day.weekday()]
        used_studio_times = set()
        daily_count = random.randint(7, 10)
        attempts = 0
        while daily_count > 0 and attempts < 80:
            attempts += 1
            class_type = random.choice(CLASS_TYPES)
            possible_trainers = [
                trainer for trainer in trainer_by_skill[class_type]
                if common_trainer_slots(trainer, weekday)
            ]
            if not possible_trainers:
                continue
            trainer = random.choice(possible_trainers)
            available_times = common_trainer_slots(trainer, weekday)
            start = random.choice(available_times)
            studio = random.choice(list(STUDIOS))
            if (studio, start) in used_studio_times:
                continue
            used_studio_times.add((studio, start))
            data["classes"].append(
                {
                    "id": class_id,
                    "date": format_date(current_day),
                    "class_type": class_type,
                    "start_time": start,
                    "end_time": add_one_hour(start),
                    "studio": studio,
                    "trainer_id": trainer["id"],
                }
            )
            class_id += 1
            daily_count -= 1


def common_trainer_slots(trainer: dict, weekday: str) -> list[str]:
    return [slot for slot in trainer["availability"].get(weekday, []) if "08:00" <= slot <= "20:00"]


def create_sample_packages_and_bookings(data: dict) -> None:
    purchase_id = 1
    booking_id = 1
    classes_by_type = defaultdict(list)
    for class_item in data["classes"]:
        classes_by_type[class_item["class_type"]].append(class_item)

    for customer in data["customers"]:
        bought_types = random.sample(CLASS_TYPES, random.randint(1, 3))
        for class_type in bought_types:
            package = random.choice([pkg for pkg in PACKAGES if pkg["class_type"] == class_type])
            remaining = package["lessons"]
            purchase_date = date.today() - timedelta(days=random.randint(1, 170))
            purchase = {
                "id": purchase_id,
                "customer_id": customer["id"],
                "package_id": package["id"],
                "class_type": package["class_type"],
                "lessons": package["lessons"],
                "remaining": remaining,
                "price": package["price"],
                "purchase_date": format_date(purchase_date),
            }
            data["package_purchases"].append(purchase)
            customer["packages"].append(purchase.copy())
            purchase_id += 1

            possible_classes = classes_by_type[class_type][:]
            random.shuffle(possible_classes)
            booking_target = random.randint(2, min(10, package["lessons"]))
            for class_item in possible_classes[:booking_target]:
                if class_slots_left(data, class_item["id"]) <= 0:
                    continue
                data["bookings"].append(
                    {
                        "id": booking_id,
                        "customer_id": customer["id"],
                        "class_id": class_item["id"],
                        "booking_date": format_date(parse_date(class_item["date"]) - timedelta(days=random.randint(0, 21))),
                    }
                )
                booking_id += 1
                purchase["remaining"] -= 1
                customer_package = customer["packages"][-1]
                customer_package["remaining"] -= 1


def add_one_hour(start_value: str) -> str:
    start_dt = datetime.combine(date.today(), parse_time(start_value))
    return (start_dt + timedelta(hours=1)).strftime(TIME_FORMAT)


def class_slots_left(data: dict, class_id: int) -> int:
    class_item = find_by_id(data["classes"], class_id)
    if not class_item:
        return 0
    capacity = STUDIOS[class_item["studio"]]["capacity"]
    booked = sum(1 for booking in data["bookings"] if booking["class_id"] == class_id)
    return capacity - booked


def find_by_id(items: list[dict], item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def main() -> None:
    data = load_data()
    while True:
        print("\n@@@@ Fitness Management Portal @@@@")
        print("1. Customer registration/Login")
        print("2. Admin Login")
        print("0. Exit")
        option = input("Enter option: ").strip()
        if option == "1":
            customer_entry(data)
        elif option == "2":
            admin_login(data)
        elif option == "0":
            save_data(data)
            print("Thank you for using Fitness Management Portal.")
            break
        else:
            print("Invalid option.")


def customer_entry(data: dict) -> None:
    while True:
        print("\n@@@@ Customer System @@@@")
        print("1. Login")
        print("2. Register")
        print("0. Back")
        option = input("Enter option: ").strip()
        if option == "1":
            customer = customer_login(data)
            if customer:
                customer_menu(data, customer)
        elif option == "2":
            register_customer(data)
        elif option == "0":
            return
        else:
            print("Invalid option.")


def register_customer(data: dict) -> None:
    print("\nCustomer Registration")
    while True:
        username = input_non_empty("Username: ")
        if any(customer["username"].lower() == username.lower() for customer in data["customers"]):
            print("Username already exists. Please choose another.")
        else:
            break
    password = input_non_empty("Password: ")
    email = input_non_empty("Email address: ")
    age = input_int("Age: ", 1, 120)
    gender = input_non_empty("Gender: ")
    customer = {
        "id": next_id(data["customers"]),
        "username": username,
        "password": password,
        "email": email,
        "age": age,
        "gender": gender,
        "packages": [],
    }
    data["customers"].append(customer)
    save_data(data)
    print("Registration successful. You may now login.")


def customer_login(data: dict) -> dict | None:
    print("\nCustomer Login")
    username = input_non_empty("Username: ")
    password = input_non_empty("Password: ")
    for customer in data["customers"]:
        if customer["username"] == username and customer["password"] == password:
            print(f"Welcome, {customer['username']}!")
            return customer
    print("Invalid username or password.")
    return None


def customer_menu(data: dict, customer: dict) -> None:
    while True:
        print("\n@@@@ Members Main Menu @@@@")
        print("1. Buy package")
        print("2. View packages")
        print("3. Register for class")
        print("4. Logout")
        option = input("Enter option: ").strip()
        if option == "1":
            buy_package(data, customer)
        elif option == "2":
            view_customer_packages(customer)
        elif option == "3":
            register_for_class(data, customer)
        elif option == "4":
            save_data(data)
            return
        else:
            print("Invalid option.")


def buy_package(data: dict, customer: dict) -> None:
    print("\nAvailable Packages")
    for package in PACKAGES:
        print(
            f"{package['id']}. {package['class_type']} x {package['lessons']} "
            f"(${package['price']}, ${package['per_class']}/class)"
        )
    choice = input_int("Select package number, or 0 to cancel: ", 0, len(PACKAGES))
    if choice == 0:
        return
    package = PACKAGES[choice - 1]
    purchase = {
        "id": next_id(data["package_purchases"]),
        "customer_id": customer["id"],
        "package_id": package["id"],
        "class_type": package["class_type"],
        "lessons": package["lessons"],
        "remaining": package["lessons"],
        "price": package["price"],
        "purchase_date": format_date(date.today()),
    }
    data["package_purchases"].append(purchase)
    customer["packages"].append(purchase.copy())
    save_data(data)
    print(f"{package['class_type']} x {package['lessons']} package added.")


def view_customer_packages(customer: dict) -> None:
    print("\nYour Packages")
    active_packages = [pkg for pkg in customer["packages"] if pkg["remaining"] > 0]
    if not active_packages:
        print("No active packages.")
        return
    for package in active_packages:
        print(
            f"{package['class_type']} package: {package['remaining']} "
            f"of {package['lessons']} lessons left"
        )


def register_for_class(data: dict, customer: dict) -> None:
    week_start = date.today() - timedelta(days=date.today().weekday())
    max_week_start = week_start + timedelta(weeks=4)
    while True:
        visible_classes = display_week_classes(data, week_start)
        print("\nChoose class number to register, N for next week, P for previous week, or 0 to go back.")
        choice = input("Enter choice: ").strip().upper()
        if choice == "0":
            return
        if choice == "N":
            if week_start >= max_week_start:
                print("You can only book up to 4 weeks in advance.")
            else:
                week_start += timedelta(weeks=1)
            continue
        if choice == "P":
            current_week = date.today() - timedelta(days=date.today().weekday())
            if week_start <= current_week:
                print("Cannot go before the current week.")
            else:
                week_start -= timedelta(weeks=1)
            continue
        if not choice.isdigit():
            print("Invalid option.")
            continue
        index = int(choice)
        if index not in visible_classes:
            print("Class number not found.")
            continue
        book_class(data, customer, visible_classes[index])


def display_week_classes(data: dict, week_start: date) -> dict[int, dict]:
    print(f"\nClasses for week starting {week_start.strftime('%d-%b-%Y')}")
    visible = {}
    running_number = 1
    for day_offset in range(7):
        current_day = week_start + timedelta(days=day_offset)
        print(f"\n{DAYS[current_day.weekday()]} ({current_day.strftime('%d-%b')})")
        day_classes = sorted(
            [class_item for class_item in data["classes"] if class_item["date"] == format_date(current_day)],
            key=lambda item: item["start_time"],
        )
        if not day_classes:
            print("  No classes scheduled.")
        for class_item in day_classes:
            trainer = find_by_id(data["trainers"], class_item["trainer_id"])
            slots = class_slots_left(data, class_item["id"])
            print(
                f"{running_number}. {class_item['class_type']}, {class_item['start_time']} - "
                f"{class_item['end_time']}, {trainer['name'] if trainer else 'Unknown'}, "
                f"{class_item['studio']}, {slots} slots left"
            )
            visible[running_number] = class_item
            running_number += 1
    return visible


def book_class(data: dict, customer: dict, class_item: dict) -> None:
    class_date = parse_date(class_item["date"])
    class_start = datetime.combine(class_date, parse_time(class_item["start_time"]))
    if class_start < datetime.now():
        print("This class has already passed.")
        return
    if class_date > date.today() + timedelta(weeks=4):
        print("Bookings are only allowed up to 4 weeks in advance.")
        return
    if class_slots_left(data, class_item["id"]) <= 0:
        print("This class is full.")
        return
    already_booked = any(
        booking["customer_id"] == customer["id"] and booking["class_id"] == class_item["id"]
        for booking in data["bookings"]
    )
    if already_booked:
        print("You have already registered for this class.")
        return

    package = first_available_package(customer, class_item["class_type"])
    if not package:
        print(f"You do not have an active {class_item['class_type']} package.")
        return

    confirm = input(
        f"Confirm booking {class_item['date']} {class_item['class_type']} "
        f"{class_item['start_time']} - {class_item['end_time']}? (y/n): "
    ).strip().lower()
    if confirm != "y":
        print("Booking cancelled.")
        return

    booking = {
        "id": next_id(data["bookings"]),
        "customer_id": customer["id"],
        "class_id": class_item["id"],
        "booking_date": format_date(date.today()),
    }
    data["bookings"].append(booking)
    package["remaining"] -= 1
    update_matching_purchase(data, customer, package)
    customer["packages"] = [pkg for pkg in customer["packages"] if pkg["remaining"] > 0]
    save_data(data)
    print("Booking confirmed. Your package has been deducted.")


def first_available_package(customer: dict, class_type: str) -> dict | None:
    for package in customer["packages"]:
        if package["class_type"] == class_type and package["remaining"] > 0:
            return package
    return None


def update_matching_purchase(data: dict, customer: dict, package: dict) -> None:
    for purchase in data["package_purchases"]:
        if purchase["id"] == package["id"] and purchase["customer_id"] == customer["id"]:
            purchase["remaining"] = package["remaining"]
            break


def admin_login(data: dict) -> None:
    print("\nAdmin Login")
    username = input_non_empty("Username: ")
    password = input_non_empty("Password: ")
    for admin in data["admins"]:
        if admin["username"] == username and admin["password"] == password:
            print("Admin login successful.")
            admin_menu(data)
            return
    print("Invalid admin login.")


def admin_menu(data: dict) -> None:
    while True:
        print("\n@@@ Admin System @@@")
        print("1. Class planner")
        print("2. View/Add trainer")
        print("3. View statistics")
        print("4. Logout")
        option = input("Enter option: ").strip()
        if option == "1":
            class_planner(data)
        elif option == "2":
            trainer_menu(data)
        elif option == "3":
            statistics_menu(data)
        elif option == "4":
            save_data(data)
            return
        else:
            print("Invalid option.")


def class_planner(data: dict) -> None:
    selected_date = read_date("Enter date to view (YYYY-MM-DD): ")
    while True:
        print(f"\nClass Planner for {selected_date}")
        day_classes = display_day_classes(data, selected_date)
        print("\n1. Add class")
        print("2. Delete class")
        print("0. Back")
        option = input("Enter option: ").strip()
        if option == "1":
            add_class(data, selected_date)
        elif option == "2":
            if day_classes:
                delete_class(data, day_classes)
            else:
                print("No classes to delete.")
        elif option == "0":
            return
        else:
            print("Invalid option.")


def read_date(prompt: str) -> date:
    while True:
        value = input(prompt).strip()
        try:
            return parse_date(value)
        except ValueError:
            print("Please enter date in YYYY-MM-DD format.")


def display_day_classes(data: dict, selected_date: date) -> dict[int, dict]:
    day_classes = sorted(
        [class_item for class_item in data["classes"] if class_item["date"] == format_date(selected_date)],
        key=lambda item: item["start_time"],
    )
    if not day_classes:
        print("No classes scheduled.")
        return {}
    numbered = {}
    for index, class_item in enumerate(day_classes, start=1):
        trainer = find_by_id(data["trainers"], class_item["trainer_id"])
        registered = sum(1 for booking in data["bookings"] if booking["class_id"] == class_item["id"])
        print(
            f"{index}. {class_item['class_type']}, {class_item['start_time']} - {class_item['end_time']}, "
            f"{trainer['name'] if trainer else 'Unknown'}, {class_item['studio']}, "
            f"{registered} registered"
        )
        numbered[index] = class_item
    return numbered


def add_class(data: dict, selected_date: date) -> None:
    print("\nAdd Class")
    class_type = choose_from_list("Class type", CLASS_TYPES)
    start_time = read_start_time()
    studio = choose_from_list("Studio", list(STUDIOS))
    available_trainers = eligible_trainers(data, class_type, selected_date, start_time)
    if not available_trainers:
        print("No trainer is skilled and available for that class/time.")
        return
    print("\nAvailable trainers")
    for index, trainer in enumerate(available_trainers, start=1):
        print(f"{index}. {trainer['name']} (${trainer['hourly_rate']}/hr)")
    trainer_choice = input_int("Select trainer: ", 1, len(available_trainers))
    trainer = available_trainers[trainer_choice - 1]

    new_class = {
        "id": next_id(data["classes"]),
        "date": format_date(selected_date),
        "class_type": class_type,
        "start_time": start_time,
        "end_time": add_one_hour(start_time),
        "studio": studio,
        "trainer_id": trainer["id"],
    }
    error = validate_new_class(data, new_class)
    if error:
        print(error)
        return
    data["classes"].append(new_class)
    save_data(data)
    print("Class added successfully.")


def choose_from_list(label: str, options: list[str]) -> str:
    print(f"\n{label}")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    choice = input_int("Select option: ", 1, len(options))
    return options[choice - 1]


def read_start_time() -> str:
    while True:
        value = input("Start time (HH:MM, earliest 08:00, latest 20:00): ").strip()
        try:
            parsed = parse_time(value)
        except ValueError:
            print("Please enter time in HH:MM format.")
            continue
        if parsed < time(8, 0) or parsed > time(20, 0):
            print("Start time must be between 08:00 and 20:00.")
            continue
        return value


def eligible_trainers(data: dict, class_type: str, selected_date: date, start_time: str) -> list[dict]:
    weekday = DAYS[selected_date.weekday()]
    return [
        trainer for trainer in data["trainers"]
        if class_type in trainer["skills"] and start_time in trainer["availability"].get(weekday, [])
    ]


def validate_new_class(data: dict, new_class: dict) -> str | None:
    if new_class["class_type"] not in CLASS_TYPES:
        return "Invalid class type."
    start = parse_time(new_class["start_time"])
    if start < time(8, 0) or start > time(20, 0):
        return "Start time must be between 08:00 and 20:00."
    for class_item in data["classes"]:
        if class_item["date"] != new_class["date"]:
            continue
        if class_item["studio"] == new_class["studio"] and times_overlap(new_class, class_item):
            return "The studio already has a class at an overlapping time."
        if class_item["trainer_id"] == new_class["trainer_id"] and times_overlap(new_class, class_item):
            return "The trainer already has a class at an overlapping time."
    return None


def times_overlap(first: dict, second: dict) -> bool:
    first_start = parse_time(first["start_time"])
    first_end = parse_time(first["end_time"])
    second_start = parse_time(second["start_time"])
    second_end = parse_time(second["end_time"])
    return first_start < second_end and second_start < first_end


def delete_class(data: dict, day_classes: dict[int, dict]) -> None:
    choice = input_int("Enter class number to delete, or 0 to cancel: ", 0, len(day_classes))
    if choice == 0:
        return
    class_item = day_classes.get(choice)
    registered = sum(1 for booking in data["bookings"] if booking["class_id"] == class_item["id"])
    if registered > 0:
        print("Cannot delete class because students are already registered.")
        return
    data["classes"] = [item for item in data["classes"] if item["id"] != class_item["id"]]
    save_data(data)
    print("Class deleted.")


def trainer_menu(data: dict) -> None:
    while True:
        print("\nTrainer list")
        for index, trainer in enumerate(data["trainers"], start=1):
            skills = ", ".join(trainer["skills"])
            print(f"{index}. {trainer['name']} ({skills}) ${trainer['hourly_rate']}/hr")
        print("A. Add new trainer")
        print("0. Back")
        choice = input("Enter trainer number to view schedule, A to add, or 0 to go back: ").strip().upper()
        if choice == "0":
            return
        if choice == "A":
            add_trainer(data)
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(data["trainers"]):
            show_trainer_schedule(data["trainers"][int(choice) - 1])
        else:
            print("Invalid option.")


def show_trainer_schedule(trainer: dict) -> None:
    print(f"\nSchedule for {trainer['name']}")
    for day in DAYS:
        slots = trainer["availability"].get(day, [])
        print(f"{day}: {', '.join(slots) if slots else 'Not available'}")


def add_trainer(data: dict) -> None:
    print("\nAdd Trainer")
    name = input_non_empty("Trainer name: ")
    print("Enter skill numbers separated by comma.")
    for index, class_type in enumerate(CLASS_TYPES, start=1):
        print(f"{index}. {class_type}")
    skills = []
    while not skills:
        choices = input("Skills: ").replace(" ", "").split(",")
        for choice in choices:
            if choice.isdigit() and 1 <= int(choice) <= len(CLASS_TYPES):
                skills.append(CLASS_TYPES[int(choice) - 1])
        skills = sorted(set(skills), key=CLASS_TYPES.index)
        if not skills:
            print("Please select at least one valid skill.")
    hourly_rate = input_int("Hourly rate: ", 1)
    availability = {}
    print("Enter weekly available times for each day, separated by comma. Example: 08:00,09:00,17:00")
    for day in DAYS:
        raw = input(f"{day}: ").strip()
        slots = [slot.strip() for slot in raw.split(",") if slot.strip()]
        availability[day] = [slot for slot in slots if valid_time_text(slot)]
    trainer = {
        "id": next_id(data["trainers"]),
        "name": name,
        "skills": skills,
        "hourly_rate": hourly_rate,
        "availability": availability,
    }
    data["trainers"].append(trainer)
    save_data(data)
    print("Trainer added.")


def valid_time_text(value: str) -> bool:
    try:
        parse_time(value)
        return True
    except ValueError:
        return False


def statistics_menu(data: dict) -> None:
    while True:
        print("\nStatistics Period")
        print("1. Last 4 weeks")
        print("2. Last 3 months")
        print("3. Last 12 months")
        print("0. Back")
        option = input("Enter option: ").strip()
        if option == "0":
            return
        if option not in {"1", "2", "3"}:
            print("Invalid option.")
            continue
        days = {"1": 28, "2": 90, "3": 365}[option]
        display_statistics(data, date.today() - timedelta(days=days), date.today())


def display_statistics(data: dict, start_date: date, end_date: date) -> None:
    period_classes = {
        class_item["id"]: class_item
        for class_item in data["classes"]
        if start_date <= parse_date(class_item["date"]) <= end_date
    }
    period_bookings = [
        booking for booking in data["bookings"]
        if booking["class_id"] in period_classes
    ]
    period_purchases = [
        purchase for purchase in data["package_purchases"]
        if start_date <= parse_date(purchase["purchase_date"]) <= end_date
    ]

    print(f"\nStatistics from {start_date} to {end_date}")
    print("\n1) Class registrations by class type")
    registration_counts = Counter(period_classes[booking["class_id"]]["class_type"] for booking in period_bookings)
    print_counter_bar(registration_counts)

    print("\n2) Packages bought by class type")
    package_counts = Counter(purchase["class_type"] for purchase in period_purchases)
    print_counter_bar(package_counts)

    print("\n3) Top 5 trainers")
    trainer_counts = Counter(period_classes[booking["class_id"]]["trainer_id"] for booking in period_bookings)
    for trainer_id, count in trainer_counts.most_common(5):
        trainer = find_by_id(data["trainers"], trainer_id)
        print(f"{trainer['name'] if trainer else 'Unknown'}: {count} registrations")

    print("\n4) Estimated profit")
    profit = calculate_profit(data, period_classes, period_bookings, start_date, end_date)
    print(f"Revenue: ${profit['revenue']:.2f}")
    print(f"Trainer cost: ${profit['trainer_cost']:.2f}")
    print(f"Studio operating cost: ${profit['studio_cost']:.2f}")
    print(f"Rental cost: ${profit['rental_cost']:.2f}")
    print(f"Estimated profit: ${profit['profit']:.2f}")

    print("\nAdditional statistic: Studio utilisation")
    utilisation = Counter(period_classes[booking["class_id"]]["studio"] for booking in period_bookings)
    print_counter_bar(utilisation)


def print_counter_bar(counter: Counter) -> None:
    if not counter:
        print("No data in this period.")
        return
    max_value = max(counter.values())
    for key, value in counter.most_common():
        bar_length = max(1, int((value / max_value) * 30))
        print(f"{key:15} {value:5} {'#' * bar_length}")


def calculate_profit(data: dict, period_classes: dict[int, dict], bookings: list[dict], start_date: date, end_date: date) -> dict:
    revenue = 0
    for booking in bookings:
        class_item = period_classes[booking["class_id"]]
        revenue += PROFIT_RATE[class_item["class_type"]]

    trainer_cost = 0
    studio_cost = 0
    for class_item in period_classes.values():
        trainer = find_by_id(data["trainers"], class_item["trainer_id"])
        trainer_cost += trainer["hourly_rate"] if trainer else 0
        studio_cost += STUDIOS[class_item["studio"]]["cost"]

    months = max(1, round((end_date - start_date).days / 30))
    rental_cost = months * 17000
    total_cost = trainer_cost + studio_cost + rental_cost
    return {
        "revenue": revenue,
        "trainer_cost": trainer_cost,
        "studio_cost": studio_cost,
        "rental_cost": rental_cost,
        "profit": revenue - total_cost,
    }


if __name__ == "__main__":
    main()
