from datetime import datetime, timedelta
from threading import Thread, Lock, Event
import time
import os

# Global variables for control
screen_lock = Lock()
stop_event = Event()
current_mode = None
alarm_time = None
use_24h_format = True

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def format_time(time_obj):
    if use_24h_format:
        return time_obj.strftime("%H:%M:%S")
    return time_obj.strftime("%I:%M:%S %p")

def display_screen(clock_time, alarm_status=""):
    menu_text = """
Menu Options:
1. Set custom time
2. Set alarm
3. Use current time
4. Switch clock format (12/24)
5. Exit clock
Your choice (1/2/3/4/5): """
    
    with screen_lock:
        clear_screen()
        print(f"Current Time: {clock_time}")
        if alarm_time:
            print(f"Alarm set for: {alarm_time}")
        if alarm_status:
            print(alarm_status)
        print("\n" + menu_text)

def check_alarm():
    while not stop_event.is_set():
        if alarm_time:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == alarm_time:
                with screen_lock:
                    print("\nALARM! ALARM! ALARM!")
                    time.sleep(2)
        time.sleep(1)

def display_time(custom_time=None):
    while not stop_event.is_set():
        if custom_time and current_mode == "custom":
            display_time = format_time(custom_time)
            custom_time += timedelta(seconds=1)
        else:
            display_time = datetime.now().strftime("%H:%M:%S")
        
        display_screen(display_time)
        time.sleep(1)

def get_user_choice():
    while not stop_event.is_set():
        try:
            choice = input().strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            else:
                print("Please enter '1', '2', '3', or '4'")
        except EOFError:
            continue

def set_alarm():
    while True:
        try:
            alarm_str = input('Enter alarm time (HH:MM:SS): ').strip()
            return datetime.strptime(alarm_str, "%H:%M:%S").strftime("%H:%M:%S")
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS")
def toggle_time_format():
    global use_24h_format
    use_24h_format = not use_24h_format
    return "Time format switched to " + ("24-hour" if use_24h_format else "12-hour")

def reset_state():
    global current_mode, alarm_time
    stop_event.set()
    time.sleep(1)  # Give threads time to stop
    stop_event.clear()
    current_mode = None
    alarm_time = None

def main():
    global current_mode, alarm_time
    
    try:
        # Start initial clock with current time
        current_mode = "current"
        clock_thread = Thread(target=display_time)
        alarm_thread = Thread(target=check_alarm)
        clock_thread.daemon = True
        alarm_thread.daemon = True
        clock_thread.start()
        alarm_thread.start()

        while True:
            choice = get_user_choice()
            
            if choice == '5':  # Exit
                break
            
            if choice == '4':  # Toggle time format
                message = toggle_time_format()
                print(message)
                continue
                
            reset_state()  # Stop current threads
            
            if choice == '1':  # Custom time
                while True:
                    try:
                        time_str = input("Enter time (HH:MM:SS): ").strip()
                        custom_time = datetime.strptime(time_str, "%H:%M:%S")
                        current_mode = "custom"
                        clock_thread = Thread(target=display_time, args=(custom_time,))
                        clock_thread.daemon = True
                        clock_thread.start()
                        break
                    except ValueError:
                        print("Invalid time format. Please use HH:MM:SS")
            
            elif choice == '2':  # Set alarm
                alarm_time = set_alarm()
                print(f'Alarm set for {alarm_time}')
                current_mode = "current"
                clock_thread = Thread(target=display_time)
                alarm_thread = Thread(target=check_alarm)
                clock_thread.daemon = True
                alarm_thread.daemon = True
                clock_thread.start()
                alarm_thread.start()
            
            elif choice == '3':  # Current time
                current_mode = "current"
                clock_thread = Thread(target=display_time)
                alarm_thread = Thread(target=check_alarm)
                clock_thread.daemon = True
                alarm_thread.daemon = True
                clock_thread.start()
                alarm_thread.start()

    except KeyboardInterrupt:
        print("\nExiting clock...")
    finally:
        stop_event.set()  # Ensure all threads stop
        print("\nThank you for using the clock!")

if __name__ == "__main__":
    main()