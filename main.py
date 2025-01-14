
from datetime import datetime, timedelta  # For date and time operations
from threading import Thread, Lock, Event  # For thread management and synchronization
import time  # For time-related operations
import os    # For system operations like clearing screen

# Global variables for thread synchronization and clock state
screen_lock = Lock()      # Lock for thread-safe screen updates
stop_event = Event()      # Event to signal program termination
pause_event = Event()     # Event to control clock pause/resume
current_mode = None       # Tracks current clock mode (custom/current time)
alarm_time = None        # Stores the alarm time
use_24h_format = True    # Toggle between 24h and 12h format

def clear_screen():
    #Clear the terminal screen based on operating system.
    os.system("cls" if os.name == "nt" else "clear")

def format_time(time_obj):
    #Format time based on 24h or 12h preference.
    if use_24h_format:
        return time_obj.strftime("%H:%M:%S")
    return time_obj.strftime("%I:%M:%S %p")

def display_screen(clock_time, alarm_status=""):
    #Display the clock interface with menu options.
    
    menu_text = """
Menu Options:
1. Set custom time
2. Set alarm
3. Use current time
4. Switch clock format (12/24)
5. Pause/Resume time
6. Exit clock
Your choice (1/2/3/4/5/6): """

    with screen_lock:  # thread-safe screen updates
        clear_screen()
        print(f"Current Time: {clock_time}")
        if alarm_time:
            print(f"Alarm set for: {alarm_time}")
        if alarm_status:
            print(alarm_status)
        if pause_event.is_set():
            print("Time is PAUSED")
        print("\n" + menu_text)

def check_alarm():
    #Monitor current time and trigger alarm when alarm_time is reached.
    while not stop_event.is_set():
        if alarm_time and not pause_event.is_set():
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == alarm_time:
                with screen_lock:
                    print("\nALARM! ALARM! ALARM!")
                    time.sleep(2)
        time.sleep(1)

def display_time(custom_time=None):
    #Main clock display function that handles both custom and current time.
    
    paused_time = None
    while not stop_event.is_set():
        if pause_event.is_set():
            # Handle paused state
            if paused_time is None:
                if custom_time and current_mode == "custom":
                    paused_time = custom_time
                else:
                    paused_time = datetime.now()
            display_time = format_time(paused_time)
        else:
            # Handle running state
            if custom_time and current_mode == "custom":
                if paused_time:
                    custom_time = paused_time + timedelta(seconds=1)
                    paused_time = None
                display_time = format_time(custom_time)
                custom_time += timedelta(seconds=1)
            else:
                display_time = format_time(datetime.now())
        
        display_screen(display_time)
        if not pause_event.is_set():
            time.sleep(1)
        else:
            time.sleep(0.1)

def get_user_choice():
    #Get and validate user menu choice.
    
   while not stop_event.is_set():
        try:
            choice = input().strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Please enter '1', '2', '3', '4', '5', or '6'")
        except EOFError:
            continue

def set_alarm():
    #Get and validate alarm time from user.
    
    while True:
        try:
            alarm_str = input('Enter alarm time (HH:MM:SS): ').strip()
            return datetime.strptime(alarm_str, "%H:%M:%S").strftime("%H:%M:%S")
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS")

def toggle_time_format():
    #Toggle between 12h and 24h time format.
    
    global use_24h_format
    use_24h_format = not use_24h_format
    return "Time format switched to " + ("24-hour" if use_24h_format else "12-hour")

def toggle_pause():
    #Toggle clock pause state.
    if pause_event.is_set():
        pause_event.clear()
        return "Time resumed"
    else:
        pause_event.set()
        return "Time paused"

def reset_state():
    #Reset all clock state variables and events.
    global current_mode, alarm_time
    stop_event.set()
    time.sleep(1)
    stop_event.clear()
    pause_event.clear()
    current_mode = None
    alarm_time = None

def main():
    #Main program loop handling menu choices and thread management.
    global current_mode, alarm_time
    
    try:
        # Initialize clock with current time
        current_mode = "current"
        clock_thread = Thread(target=display_time)
        alarm_thread = Thread(target=check_alarm)
        clock_thread.daemon = True
        alarm_thread.daemon = True
        clock_thread.start()
        alarm_thread.start()

        while True:
            choice = get_user_choice()
            
            if choice == '6':  # Exit
                break
            
            if choice == '4':  # Toggle time format
                message = toggle_time_format()
                print(message)
                continue

            if choice == '5':  # Toggle pause
                message = toggle_pause()
                print(message)
                continue
                
            reset_state()  # Reset state for mode changes
            
            if choice == '1':  # Set custom time
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
            
            elif choice == '3':  # Use current time
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
        stop_event.set()
        print("\nThank you for using the clock!")

if __name__ == "__main__":
    main()