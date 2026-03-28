import csv
from rich.table import Table
from rich.console import Console
console = Console()
from utils import write_data, read_data, clean_name, prompt_non_empty, prompt_flight_id, prompt_int, prompt_float, init_file, confirm

FILE = "flights.csv"
HEADERS = ["flight_id", "source", "destination", "seats", "fare"]

init_file(FILE, HEADERS)


#Add Flight 
def add_flight():
    while True:
        data = read_data(FILE)

        fid = prompt_flight_id("Flight ID (or 0 to exit): ")

        if fid == "0":
            print("Returning to menu...")
            return

        if any(f["flight_id"] == fid for f in data):
            print("Flight ID already exists!")
            continue

        src = clean_name(prompt_non_empty("From: "))
        dst = clean_name(prompt_non_empty("Destination: "))
        seats = prompt_int("Seats: ", min_val=45)
        fare = prompt_float("Fare: ", min_val=2000)

        data.append({
            "flight_id": fid,
            "source": src,
            "destination": dst,
            "seats": str(seats),
            "fare": str(fare)
        })

        write_data(FILE, data, HEADERS)
        print("Flight added successfully!")

        if not confirm("Add another flight? (y/n): "): 
            break

# View Flights


def view_flights():
    data = read_data(FILE)

    if not data:
        console.print("[red]No flights available.[/red]")
        return

    table = Table(title="Flights Details", show_lines=True)

    table.add_column("Flight ID", style="cyan")
    table.add_column("From", style="green")
    table.add_column("To", style="green")
    table.add_column("Seats", justify="right")
    table.add_column("Fare", justify="right")

    for f in data:
        table.add_row(
            f["flight_id"],
            f["source"],
            f["destination"],
            str(f["seats"]),
            f"{float(f['fare']):.2f}"
        )

    console.print(table)

def update_flight():
    
    while True:
        fid = prompt_flight_id("\nEnter Flight ID to update (or 0 to exit): ")

        if fid == "0":
            print("Returning to menu...")
            return

        data = read_data(FILE)
        found = False

        for f in data:
            if f["flight_id"] == fid:
                print("\nCurrent Data:")
                print(f"ID: {f['flight_id']} | From {f['source']} --> To {f['destination']} | Seats: {f['seats']} | Fare: {f['fare']}")

                updated = False 

                while True:
                    print("\nWhat do you want to update?")
                    print("1. Source")
                    print("2. Destination")
                    print("3. Seats")
                    print("4. Fare")
                    print("5. Exit")

                    choice = input("Choice: ").strip()

                    if choice == "1":
                        f["source"] = clean_name(prompt_non_empty("New Source: "))
                        updated = True
                        print("Source updated!")

                    elif choice == "2":
                        f["destination"] = clean_name(prompt_non_empty("New Destination: "))
                        updated = True
                        print("Destination updated!")

                    elif choice == "3":
                        f["seats"] = prompt_int("New Seats: ")
                        updated = True
                        print("Seats updated!")

                    elif choice == "4":
                        f["fare"] = prompt_float("New Fare: ")
                        updated = True
                        print("Fare updated!")

                    elif choice == "5":
                        break

                    else:
                        print("Invalid choice!")

                if updated:
                    if confirm("Save changes? (y/n): "):
                        write_data(FILE, data, HEADERS)
                        print("Flight updated successfully!")
                    else:
                        print("Update cancelled")

                found = True
                break

        if not found:
            print("Flight not found")

def search_flight():
    while True:
        fid = prompt_flight_id("\nEnter Flight ID (or 0 to exit): ")

        if fid == "0":
            print("Returning to menu...")
            break

        data = read_data(FILE)

        for f in data:
            if f["flight_id"] == fid:
                print("\nFlight Found:")
                print(f"{f['flight_id']} | From {f['source']} --> To {f['destination']} | Seats: {f['seats']} | Fare: {f['fare']}")
                break
        else:
            print("Flight not found")

# Delete Flight 
def delete_flight():
    while True:
        fid = prompt_flight_id("\nEnter Flight ID to delete (or 0 to exit): ")

        if fid == "0":
            print("Returning to menu...")
            break

        data = read_data(FILE)

        # Find flight first
        flight = next((f for f in data if f["flight_id"] == fid), None)

        if not flight:
            print("Flight not found")
            continue

        # Show details before deleting
        print("\nFlight Details:")
        print(f"ID: {flight['flight_id']} | From {flight['source']} --> To {flight['destination']} | Seats: {flight['seats']} | Fare: {flight['fare']}")

        # Confirm
        if not confirm("Are you sure you want to delete this flight? (y/n): "):
            print("Deletion cancelled")
            continue

        # Delete
        new_data = [f for f in data if f["flight_id"] != fid]
        write_data(FILE, new_data, HEADERS)

        print("Flight deleted successfully!")

# Sort Flights
def sort_flights():
    while True:
        data = read_data(FILE)

        if not data:
            print("No flights available.")
            return

        print("\n--- Sort Flights ---")
        print("1. Flight ID")
        print("2. Source")
        print("3. Destination")
        print("4. Seats")
        print("5. Fare")
        print("6. Back")

        choice = input("Enter choice: ").strip()

        if choice == "6":
            break

        mapping = {
            "1": "flight_id",
            "2": "source",
            "3": "destination",
            "4": "seats",
            "5": "fare"
        }

        if choice not in mapping:
            print("Invalid choice!")
            continue

        key = mapping[choice]

        order = input("Ascending or Descending? (a/d): ").strip().lower()
        reverse = (order == "d")

        if key == "seats":
            sorted_data = sorted(data, key=lambda x: int(x[key]), reverse=reverse)

        elif key == "fare":
            sorted_data = sorted(data, key=lambda x: float(x[key]), reverse=reverse)

        else:
            sorted_data = sorted(data, key=lambda x: x[key].lower(), reverse=reverse)

        print("\n--- Sorted Flights ---")
        for f in sorted_data:
            print(f"ID: {f['flight_id']} | From {f['source']} --> To {f['destination']} | Seats: {f['seats']} | Fare: {f['fare']}")