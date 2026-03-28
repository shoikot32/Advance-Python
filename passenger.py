import csv
from utils import write_data, read_data, init_file, prompt_passenger_id, prompt_name, prompt_age, prompt_nationality, prompt_non_empty, confirm, prompt_gender,prompt_passport
from rich.console import Console
from rich.table import Table
console = Console()

FILE = "passengers.csv"
HEADERS = ["id", "name", "passport", "age", "nationality", "gender"]
init_file(FILE, HEADERS)

""" add """
def add_passenger():
    while True:
        data = read_data(FILE)

        pid = prompt_passenger_id("Passenger ID (or 0 to exit): ")

        if pid == "0":
            print("Returning to menu...")
            return

        if any(f["id"] == pid for f in data):
            print("Passenger ID already exists!")
            continue

        name = prompt_name()

        while True:
            passport = prompt_passport()

            if any(p["passport"] == passport for p in data):
                print("Passport already exists! Try another.")
                continue
            break

        age = prompt_age()
        nationality = prompt_nationality()

        data.append({
            "id": pid,
            "name": name,
            "passport": passport,
            "age": str(age),
            "nationality": nationality,
            "gender": prompt_gender()
        })

        write_data(FILE, data, HEADERS)
        print("Passenger added successfully!")

        if not confirm("Add another passenger? (y/n): "):
            break


""" VIEW """
def view_passengers():
    data = read_data(FILE)

    if not data:
        console.print("No passengers found.")
        return

    print("\n--- Passengers ---")

    table = Table(title="✈ Passenger list")

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Passport")
    table.add_column("Age")
    table.add_column("Nationality")
    table.add_column("Gender")

    for p in data:
        table.add_row(
            p["id"],
            p["name"],
            p["passport"],
            p["age"],
            p["nationality"],
            p["gender"]
        )
    console.print(table)
            
""" SEARCH """
def search_passenger():
    while True:
        pid = prompt_passenger_id("\nEnter Passenger ID (or 0 to exit): ")

        if pid == "0":
            print("Returning to menu...")
            break

        data = read_data()

        for p in data:
            if p["id"] == pid:
                print("\nPassenger Found:")
                print(f"{p['id']} | {p['name']} | {p['passport']} | {p['age']} | {p['nationality']} | {p['gender']}")
                break
        else:
            print("Passenger not found")

        # ADD THIS (so user knows it continues)
        print("Search again or press 0 to exit")

""" UPDATE """
def update_passenger():
    while True:
        pid = prompt_passenger_id("\nEnter Passenger ID to update (or 0 to exit): ")

        if pid == "0":
            print("Returning to menu...")
            break

        data = read_data(FILE)

        for p in data:
            if p["id"] == pid:
                print("\nCurrent Data:", p)

                updated = False   #NEW FLAG

                while True:
                    print("\n1.Name 2.Passport 3.Age 4.Nationality 5.Gender 6.Done")
                    c = input("Choice: ").strip()

                    if c == "1":
                        p["name"] = prompt_name()
                        updated = True

                    elif c == "2":
                        new_pass = prompt_passport("New Passport: ")

                        if any(x["passport"] == new_pass for x in data):
                            print("Passport already exists!")
                        else:
                            p["passport"] = new_pass
                            updated = True

                    elif c == "3":
                        p["age"] = str(prompt_age())
                        updated = True

                    elif c == "4":
                        p["nationality"] = prompt_nationality()
                        updated = True

                    elif c == "5":
                        p["gender"] = prompt_gender()
                        updated = True

                    elif c == "6":
                        break

                    else:
                        print("Invalid!")

                # ONLY SAVE IF UPDATED
                if updated:
                    if confirm("Save changes? (y/n): "):
                        write_data(FILE, data, HEADERS)
                        print("Passenger updated!")
                    else:
                        print("Update cancelled")
                else:
                    print("No changes made")

                break
        else:
            print("Passenger not found")

        # LOOP CONTINUES CLEANLY
        print("\n Update another or press 0 to exit")

""" DELETE """
def delete_passenger():
    while True:
        pid = prompt_passenger_id("\nEnter Passenger ID to delete (or 0 to exit): ")

        if pid == "0":
            break

        data = read_data()

        for p in data:
            if p["id"] == pid:
                if confirm(f"Delete passenger {pid}? (y/n): "):
                    new_data = [x for x in data if x["id"] != pid]
                    write_data(FILE, new_data, HEADERS)
                    print("Passenger deleted!")
                else:
                    print("Cancelled")
                break
        else:
            print("Passenger not found")


""" SORT """
def sort_passengers():
    while True:
        data = read_data(FILE)

        if not data:
            console.print("No passengers found.")
            return

        print("\n1.ID 2.Name 3.Age 4.Nationality 5.Gender 6.Back")
        c = input("Choice: ").strip()

        if c == "6":
            break

        mapping = {
            "1": "id",
            "2": "name",
            "3": "age",
            "4": "nationality",
            "5": "gender"
        }

        if c not in mapping:
            print("Invalid!")
            continue

        key = mapping[c]
        reverse = input("Descending? (y/n): ").lower() == "y"

        if key == "age":
            data = sorted(data, key=lambda x: int(x[key]), reverse=reverse)
        else:
            data = sorted(data, key=lambda x: x[key].lower(), reverse=reverse)

        #print("\n--- Sorted ---")
        #for p in data:
        #    print(f"{p['id']} | {p['name']} | {p['age']} | {p['nationality']} | {p['gender']}")
        #    continue
        table = Table(title="sorted table")

        table.add_column("ID")
        table.add_column("Name")
        table.add_column("age")
        table.add_column("Nationality")
        table.add_column("Gender")

        for p in data:
            table.add_row(
                p["id"],
                p["name"],
                p["age"],
                p["nationality"],
                p["gender"]
            )
        console.print(table)       
