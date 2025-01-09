from datetime import datetime, timedelta
from threading import Thread
import time
import os



def refresh_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_time():
    while True: 
        current_time = datetime.now().strftime("%H:%M:%S")
       # refresh_screen()
        print(current_time)
        time.sleep(1)

def display_custom_time(custom_time):
    while True:
        refresh_screen()
        print(custom_time.strftime("%H:%M:%S"))
        time.sleep(1)
        custom_time += timedelta(seconds=1)


def get_user_choice():
    while True:
        user_choice = input("Would you like to set a new time on the clock ? (y/n): ").lower()
        if user_choice in ['y', 'n']:
            return user_choice == 'y'
        print("Please enter 'y' or 'n'")

def clock_menu():
    alarm_str = input('HH:MM:SS').strip()
    alarm = datetime.strptime(alarm_str, "%H:%M:%S")
    print(f'alarm set to {alarm.strftime('%H:%M:%S')}')

    if alarm <= datetime.now:
        print('driiing')
    

def main():
    try:
        if get_user_choice():
            while True:
                time_str = input("Please enter the time in the format HH:MM:SS: ").strip()
                try:
                    custom_time = datetime.strptime(time_str, "%H:%M:%S")
                    display_custom_time(custom_time)
                    break
                except ValueError:
                    print("Invalid time format. Please use HH:MM:SS")
        else:
            display_time()
    except KeyboardInterrupt:
        print("\nExiting clock...")

main()