from utils import prompt_non_empty
import flight as fm
import passenger as pm
import booking as bm

# Initialize files
from utils import init_file

init_file("flights.csv", ["flight_id","source","destination","seats","fare"])
init_file("passengers.csv", ["id","name"])
init_file("bookings.csv", ["id","flight_id","passenger_id"])

def menu():
    while True:
        print("\n--- Airline System ---")
        print("1. Flights")
        print("2. Passengers")
        print("3. Bookings")
        print("4. Exit")

        choice = input("Choice: ")

        if choice == "1":
            flight_menu()
        elif choice == "2":
            passenger_menu()
        elif choice == "3":
            booking_menu()
        elif choice == "4":
            print("Goodbye....")
            break
        else:
            print("Invalid choice!")


def flight_menu():
    while True:
        print("\n--- Flights Info ---")
        print("1. Add")
        print("2. View")
        print("3. Update")
        print("4. Delete")
        print("5. Search")
        print("6. Sort")
        print("7. Back")

        c = input("Choice: ")

        if c == "1":
            fm.add_flight()
        elif c == "2":
            fm.view_flights()
        elif c == "3":
            fm.update_flight()
        elif c == "4":
            fm.delete_flight()
        elif c == "5":
            fm.search_flight()
        elif c == "6":
            fm.sort_flights()
        elif c == "7":
            break
        else:
            print("Invalid choice!")


def passenger_menu():
    while True:
        print("\n--- Passengers ---")
        print("1. Add")
        print("2. View")
        print("3. Update")
        print("4. Delete")
        print("5. Search")
        print("6. Sort")
        print("7. Back")

        c = input("Choice: ")

        if c == "1":
            pm.add_passenger()
        elif c == "2":
            pm.view_passengers()
        elif c == "3":
            pm.update_passenger()
        elif c == "4":
            pm.delete_passenger()
        elif c == "5":
            pm.search_passenger()
        elif c == "6":
            pm.sort_passengers()
        elif c == "7":
            break
        else:
            print("Invalid choice!")


def booking_menu():
    while True:
        print("\n--- Bookings ---")
        print("1. Add")
        print("2. View")
        print("3. Delete")
        print("4. Search")
        print("5. Update")
        print("6. Flight Booking Summary")
        print("7. Back")

        c = input("Choice: ")

        if c == "1":
            bm.add_booking()
        elif c == "2":
            bm.view_bookings()
        elif c == "3":
            bm.delete_booking()
        elif c == "4":
            bm.search_booking()
        elif c == "5":
            bm.update_booking()
        elif c == "6":
            bm.flight_booking_summary_()
        elif c == "7":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    menu()