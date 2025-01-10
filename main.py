from datetime import datetime, timedelta
from threading import Thread
import time
import os

def refresh_screen():
    os.system("cls" if os.name == "nt" else "clear")

def check_alarm(alarm_time):
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time <= alarm_time:
            print("\nALARM!")
            break
        time.sleep(1)

def display_time():
    while True: 
        current_time = datetime.now().strftime("%H:%M:%S")
        refresh_screen()
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
        user_choice = input("Choose an option:\n1. Set custom time\n2. Set alarm\n3. Use current time\nYour choice (1/2/3): ")
        if user_choice in ['1', '2', '3']:
            return user_choice
        print("Please enter '1', '2', or '3'")

def set_alarm():
    while True:
        try:
            alarm_str = input('Enter alarm time (HH:MM:SS): ').strip()
            alarm_time = datetime.strptime(alarm_str, "%H:%M:%S").strftime("%H:%M:%S")
            print(f'Alarm set for {alarm_time}')
            return alarm_time
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS")

def main():
    try:
        choice = get_user_choice()
        
        if choice == '1':
            while True:
                time_str = input("Please enter the time in the format HH:MM:SS: ").strip()
                try:
                    custom_time = datetime.strptime(time_str, "%H:%M:%S")
                    display_custom_time(custom_time)
                    break
                except ValueError:
                    print("Invalid time format. Please use HH:MM:SS")
        
        elif choice == '2':
            alarm_time = set_alarm()
            # Create two threads - one for the clock and one for the alarm
            clock_thread = Thread(target=display_time)
            alarm_thread = Thread(target=check_alarm, args=(alarm_time,))
            
            clock_thread.daemon = True
            alarm_thread.daemon = True
            
            clock_thread.start()
            alarm_thread.start()
            
            # Keep the main thread running
            alarm_thread.join()
            
        else:
            display_time()
            
    except KeyboardInterrupt:
        print("\nExiting clock...")

if __name__ == "__main__":
    main()