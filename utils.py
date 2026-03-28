from __future__ import annotations
import csv

#Initialize file with headers
def init_file(filename, headers):
    try:
        with open(filename, "r"):
            pass
    except FileNotFoundError:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)


#Read CSV data
def read_data(file):
    try:
        with open(file, mode='r', newline='') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


#Write CSV data
def write_data(file, data, headers):
    with open(file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


# Non-empty string input
def prompt_non_empty(prompt: str) -> str:
    """Prompt until user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


# Clean name (Title Case)
def clean_name(name: str) -> str:
    """Format name properly."""
    return name.strip().title()


# Integer input with range validation
def prompt_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """Prompt for integer with optional min/max validation."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Enter a valid integer.")
            continue

        if min_val is not None and value < min_val:
            print(f"Must be >= {min_val}")
            continue
        if max_val is not None and value > max_val:
            print(f"Must be <= {max_val}")
            continue

        return value


# Float input with range validation
def prompt_float(prompt: str, min_val: float | None = None, max_val: float | None = None) -> float:
    """Prompt for float with optional min/max validation."""
    while True:
        try:
            value = float(input(prompt).strip())
        except ValueError:
            print("Enter a valid number.")
            continue

        if min_val is not None and value < min_val:
            print(f"Must be >= {min_val}")
            continue
        if max_val is not None and value > max_val:
            print(f"Must be <= {max_val}")
            continue

        return value


# Confirm (used before delete/update)
def confirm(prompt: str = "Are you sure? (y/n): ") -> bool:
    """Return True if user confirms."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        elif ans in ("n", "no"):
            return False
        print("Enter 'y' or 'n'.")

def prompt_flight_id(prompt: str = "Flight ID: ") -> str:
    while True:
        val = input(prompt).strip().lower()

        #HANDLE EXIT FIRST
        if val == "0":
            return "0"

        if not val:
            print("ID cannot be empty.")

        elif " " in val:
            print("ID cannot contain spaces.")

        elif not val.startswith("f"):
            print("Flight ID must start with 'f'.")

        elif not val[1:].isdigit():
            print("After 'f', only numbers allowed.")

        elif int(val[1:]) == 0:
            print("ID number must be greater than 0.")

        else:
            return val
        
def prompt_passenger_id(prompt: str = "Passenger ID: ") -> str:
    while True:
        val = input(prompt).strip().lower()

        # allow exit
        if val == "0":
            return "0"

        if not val:
            print("ID cannot be empty.")

        elif " " in val:
            print("ID cannot contain spaces.")

        elif not val.startswith("p"):
            print("Passenger ID must start with 'p'")

        elif not val[1:].isdigit():
            print("After 'p', only numbers allowed ")

        elif int(val[1:]) == 0:
            print("ID number must be greater than 0 ")

        else:
            return val
        
def prompt_booking_id(prompt: str = "Booking ID: ") -> str:
    while True:
        val = input(prompt).strip().lower()


        if val == "0":
            return "0"

        if not val:
            print("ID cannot be empty.")

        elif " " in val:
            print("ID cannot contain spaces.")

        elif not val.startswith("b"):
            print("Booking ID must start with 'b' (e.g., b1).")

        elif not val[1:].isdigit():
            print("After 'b', only numbers allowed (e.g., b12).")

        elif int(val[1:]) == 0:
            print("ID number must be greater than 0 (e.g., b1).")

        else:
            return val
        

def prompt_gender() -> str:
    while True:
        print("\nSelect Gender:")
        print("1. Male")
        print("2. Female")
        print("3. Other")

        choice = input("Choice: ").strip()

        mapping = {
            "1": "Male",
            "2": "Female",
            "3": "Other"
        }

        if choice in mapping:
            return mapping[choice]

        print("Invalid choice. Try again.")

def prompt_age(prompt: str = "Age: ") -> int:
    while True:
        try:
            age = int(input(prompt).strip())
            if age <= 0 or age > 120:
                print("Age must be between 1 and 120.")
                continue
            return age
        except ValueError:
            print("Enter a valid age (number).")
        
def prompt_name(prompt: str = "Name: ") -> str:
    while True:
        name = input(prompt).strip()
        if not name:
            print("Name cannot be empty.")
        elif not name.replace(" ", "").isalpha():
            print("Name must contain only letters.")
        else:
            return name.title()
        
def prompt_nationality(prompt: str = "Nationality: ") -> str:
    while True:
        nat = input(prompt).strip()
        if not nat:
            print("Nationality cannot be empty.")
        elif not nat.replace(" ", "").isalpha():
            print("Only letters allowed.")
        else:
            return nat.title()
        
