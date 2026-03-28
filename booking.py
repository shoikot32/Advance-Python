import csv
from rich.table import Table
from rich.console import Console
console = Console()
from utils import read_data, write_data, prompt_flight_id, prompt_passenger_id, prompt_booking_id, init_file, confirm

FILE = "bookings.csv"
HEADERS = ["booking_id", "flight_id", "passenger_id"]


init_file(FILE, HEADERS)


def add_booking():
    while True:
        bookings = read_data(FILE)
        passengers = read_data("passengers.csv")
        flights = read_data("flights.csv")

        bid = prompt_booking_id("Booking ID (or 0 to exit): ")

        if bid == "0":
            print("Returning to menu...")
            break

        if any(b["booking_id"] == bid for b in bookings):
            print("Booking ID already exists!")
            continue

        while True:
            fid = prompt_flight_id("Flight ID (or 0 to exit): ")

            if fid == "0":
                break

            flight = next((f for f in flights if f["flight_id"] == fid), None)

            if not flight:
                print("Flight not found")
                print("Try another Flight ID or press 0 to exit")
                continue

            print(f"\n Flight Found: {fid} | {flight['source']} --> {flight['destination']} | Seats: {flight['seats']} | Fare: {flight['fare']}")
            break

        if fid == "0":
            continue

        while True:
            pid = prompt_passenger_id("Passenger ID (or 0 to exit): ")

            if pid == "0":
                break

            passenger = next((p for p in passengers if p["id"] == pid), None)

            if not passenger:
                print("Passenger not found")
                continue

            # Duplicate check
            if any(b["flight_id"] == fid and b["passenger_id"] == pid for b in bookings):
                print("This passenger already booked this flight")
                print(" Try another Passenger ID or press 0 to exit")
                continue

            print("\nPassenger Found:")
            print(f"{passenger['id']} | {passenger['name']} | {passenger['passport']} | {passenger['age']} | {passenger['nationality']} | {passenger['gender']}")
            break

        if pid == "0":
            continue

        #SEAT CHECK
        if int(flight["seats"]) <= 0:
            print("No seats available")
            continue

        #REDUCE SEAT
        flight["seats"] = str(int(flight["seats"]) - 1)
        write_data("flights.csv", flights, ["flight_id", "source", "destination", "seats", "fare"])

        #ADD BOOKING
        bookings.append({
            "booking_id": bid,
            "flight_id": fid,
            "passenger_id": pid
        })

        write_data(FILE, bookings, HEADERS)

        # FINAL OUTPUT
        print("\nBooking Confirmed:")
        print(f"{bid} | {passenger['name']} | {flight['source']} --> {flight['destination']} | Flight: {fid}")

        # CONTINUE?
        if not confirm("Add another booking? (y/n): "):
            break
        
# VIEW BOOKINGS
def view_bookings():
    bookings = read_data(FILE)
    passengers = read_data("passengers.csv")
    flights = read_data("flights.csv")

    if not bookings:
        print("No bookings found.")
        return

    print("\n--- Bookings ---")

    for b in bookings:
        p = next((x for x in passengers if x["id"] == b["passenger_id"]), None)
        f = next((x for x in flights if x["flight_id"] == b["flight_id"]), None)

        name = p["name"] if p else "Unknown"
        route = f"{f['source']} --> {f['destination']}" if f else "Unknown"

        print(f"{b['booking_id']} | {name} | {route} | Flight: {b['flight_id']}")


# DELETE BOOKING
def delete_booking():
    while True:
        bid = prompt_booking_id("\nEnter Booking ID to delete (or 0 to exit): ")

        if bid == "0":
            break

        bookings = read_data(FILE)
        flights = read_data("flights.csv")

        booking = next((b for b in bookings if b["booking_id"] == bid), None)

        if not booking:
            print("Booking not found")
            continue

        # Confirm
        if not confirm("Delete this booking? (y/n): "):
            print("Cancelled")
            continue

        # Restore seat
        for f in flights:
            if f["flight_id"] == booking["flight_id"]:
                f["seats"] = str(int(f["seats"]) + 1)

        # Delete
        bookings = [b for b in bookings if b["booking_id"] != bid]

        write_data(FILE, bookings, HEADERS)
        write_data("flights.csv", flights, ["flight_id","source","destination","seats","fare"])

        print("Booking deleted & seat restored")


#SEARCH BOOKING
def search_booking():
    while True:
        bid = prompt_booking_id("\nEnter Booking ID (or 0 to exit): ")

        if bid == "0":
            break

        bookings = read_data(FILE)
        passengers = read_data("passengers.csv")
        flights = read_data("flights.csv")

        for b in bookings:
            if b["booking_id"] == bid:
                p = next((x for x in passengers if x["id"] == b["passenger_id"]), None)
                f = next((x for x in flights if x["flight_id"] == b["flight_id"]), None)

                name = p["name"] if p else "Unknown"
                route = f"{f['source']} --> {f['destination']}" if f else "Unknown"

                print("\nBooking Found:")
                print(f"{b['booking_id']} | {name} | {route} | Flight: {b['flight_id']}")
                break
        else:
            print(" Booking not found")


    
def update_booking():
    
    while True:
        bid = prompt_booking_id("\nEnter Booking ID to update (or 0 to exit): ")

        if bid == "0":
            print("Returning to menu...")
            return

        bookings = read_data(FILE)
        passengers = read_data("passengers.csv")
        flights = read_data("flights.csv")

        found = False

        for b in bookings:
            if b["booking_id"] == bid:
                print("\nCurrent Data:")
                print(f"{b['booking_id']} | Flight: {b['flight_id']} | Passenger: {b['passenger_id']}")

                updated = False

                while True:
                    print("\nWhat do you want to update?")
                    print("1. Flight ID")
                    print("2. Passenger ID")
                    print("3. Exit")

                    choice = input("Choice: ").strip()

                    if choice == "1":
                        while True:
                            fid = prompt_flight_id("New Flight ID (or 0 to cancel): ")

                            if fid == "0":
                                break

                            flight = next((f for f in flights if f["flight_id"] == fid), None)

                            if not flight:
                                print("Flight not found")
                                continue

                            b["flight_id"] = fid
                            updated = True
                            print("Flight updated!")
                            break

                    elif choice == "2":
                        while True:
                            pid = prompt_passenger_id("New Passenger ID (or 0 to cancel): ")

                            if pid == "0":
                                break

                            passenger = next((p for p in passengers if p["id"] == pid), None)

                            if not passenger:
                                print("Passenger not found")
                                continue

                            # Duplicate check
                            if any(x["flight_id"] == b["flight_id"] and x["passenger_id"] == pid for x in bookings):
                                print("This passenger already booked this flight")
                                continue

                            b["passenger_id"] = pid
                            updated = True
                            print("Passenger updated!")
                            break

                    elif choice == "3":
                        break

                    else:
                        print("Invalid choice!")

                if updated:
                    if confirm("Save changes? (y/n): "):
                        write_data(FILE, bookings, HEADERS)
                        print("Booking updated successfully!")
                    else:
                        print("Update cancelled")
                else:
                    print("No changes made")

                found = True
                break

        if not found:
            print("Booking not found")

        if not confirm("Update another booking? (y/n): "):
            break


def flight_booking_summary_():
    bookings = read_data("bookings.csv")
    flights = read_data("flights.csv")

    if not flights:
        console.print("[red]No flights available.[/red]")
        return

    table = Table(title="Flight Summary", show_lines=True)

    table.add_column("Flight ID", style="cyan")
    table.add_column("Route", style="magenta")
    table.add_column("Price", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Booked", justify="right")
    table.add_column("Left", justify="right")
    table.add_column("Revenue", justify="right")
    table.add_column("Occupancy %", justify="right")

    for f in flights:
        fid = f["flight_id"]

        booked = sum(1 for b in bookings if b["flight_id"] == fid)

        total_seats = int(f["seats"]) + booked
        seats_left = int(f["seats"])

        fare = float(f["fare"])
        revenue = booked * fare

        occupancy = (booked / total_seats * 100) if total_seats > 0 else 0

        route = f"{f['source']} → {f['destination']}"

        table.add_row(
            fid,
            route,
            f"{fare:.2f}",
            str(total_seats),
            str(booked),
            str(seats_left),
            f"{revenue:.2f}",
            f"{occupancy:.2f}%"
        )

    console.print(table)