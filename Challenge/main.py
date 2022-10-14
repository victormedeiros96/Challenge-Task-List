from functions import *
from task_manager import Task_Manager

def main():
    print("""
Task list
    """)
    t = Task_Manager()
    choices = {
        'exit':exit_func,
        'help':help_func,
        'save':save_func,
        'list':list_func,
        'add':add_func,
        'delete':delete_func,
        'next':next_func,
        'complete':complete_func
        }
    while True:
        try:
            command = input_func()['task command']
        except KeyboardInterrupt:
            exit()
        choices[command](t)
if __name__ == "__main__":
    main()