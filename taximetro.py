import time
from datetime import datetime
import os

# Precios por segundo
PRICE_STOPPED = 0.02
PRICE_MOVING = 0.05

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_fare(seconds_stopped, seconds_moving):
    fare = seconds_stopped * PRICE_STOPPED + seconds_moving * PRICE_MOVING
    return fare

def taxi_menu(available_options):
    options_dict = {
        "1": "1. To start Taximeter",
        "2": "2. To stop Taxi",
        "3": "3. Move Taxi",
        "4": "4. End trayectory",
        "5": "5. Exit"
    }

    print("\nPlease select an option:")
    for key in available_options:
        if key in options_dict:
            print(options_dict[key])

def taximeter(test_mode=False):
    clear_screen()
    print("  🙋‍♂️    Welcome to Taxi Meter   ")

    trip_active = False
    start_time = 0
    stop_time = 0
    moving_time = 0
    state = None
    state_start_time = 0

    while True:
        # Mostrar menú dinámico según estado
        if not trip_active:
            taxi_menu(["1", "5"])
        elif state == "stopped":
            taxi_menu(["3", "4", "5"])
        elif state == "moving":
            taxi_menu(["2", "4", "5"])
        else:
            taxi_menu(["2", "3", "4", "5"])

        command = input(" > ").strip()

        if command == "1":
            if trip_active:
                print(" ⚠️  You already started your journey.")
                continue
            trip_active = True
            start_time = time.time()
            stop_time = 0
            moving_time = 0
            state = "stopped"
            state_start_time = time.time()
            print(f" 🚕  Journey started at {datetime.now().strftime('%H:%M:%S')}")

        elif command in ("2", "3"):
            if not trip_active:
                print(" ⚠️  You haven't started the journey yet.")
                continue

            duration = time.time() - state_start_time
            if state == "stopped":
                stop_time += duration
            elif state == "moving":
                moving_time += duration

            if command == "2":
                state = "stopped"
                print("Taxi is now stopped. 🚦 🚕   ")
            else:
                state = "moving"
                print("Taxi is now moving. 🚕 🚕  🚕💨")

            state_start_time = time.time()

        elif command == "4":
            if not trip_active:
                print("  🤷   You haven't started the journey.  🤦‍♂️  ")
                continue

            duration = time.time() - state_start_time
            if state == "stopped":
                stop_time += duration
            elif state == "moving":
                moving_time += duration

            fare = calculate_fare(stop_time, moving_time)

            stop_minutes, stop_seconds = divmod(stop_time, 60)
            move_minutes, move_seconds = divmod(moving_time, 60)

            print(f"\n Journey ended.   🚕💨➡️🏁   ")
            print(f"Total stopped time: {int(stop_minutes)} min {int(stop_seconds)} sec")
            print(f"Total moving time: {int(move_minutes)} min {int(move_seconds)} sec")
            print(f" 💰  Total fare:   {fare:.2f} €")
            print(" ✅ Thank you for using Taxi Meter.\n ")

            # Reiniciar variables
            trip_active = False
            state = None

            if test_mode:
                break  # salir del bucle solo en modo test

            

        elif command == "5":
            print("👋 Exiting Taxi Meter. Have a nice day! 😁")
            break

        else:
            print("  🫣 Invalid option. 👉 Please try again. 🫡  ")

if __name__ == "__main__":
    taximeter()
