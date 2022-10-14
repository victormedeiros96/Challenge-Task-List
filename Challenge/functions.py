from PyInquirer import prompt,Separator
import sys
def save_func(*args,**kwargs):
    # args[0] = task_manager
    args[0].save_data()

def complete_func(*args,**kwargs):
    # args[0] = task_manager
    id = input('? id: ').strip()
    if id.isnumeric():
        task = [row for row in args[0].table if row[0]==id]
        if len(task):
            args[0].complete_task(task[0][0])
            print(f'Task {id} completed.')
            return
        print('Error: Task id not found.')
        return
    print('Error: Id has to be an integer value.')
    
def add_func(*args,**kwargs):
    # args[0] = task_manager
    print('Enter the task detail and "-p <priority>" if the priority should not be "low"\nExample 1: make some stuffs\nExample 2: make other stuffs -p high')
    command = input('? ').strip().split('-p')
    if len(command)>1:
        priority = command[-1].strip()
        args[0].add_task(command[0].strip(),priority)
        return
    args[0].add_task(command[0])

def delete_func(*args,**kwargs):
    id = input('? id: ').strip()
    if id.isnumeric():
        row = [row for row in args[0].table if row[0]==id]
        if len(row):
            args[0].table.remove(row[0])
            print(f'Task {id} removed.')
            return
        print('Error: Task id not found.')
        return
    print('Error: Id has to be an integer value.')
def list_func(*args,**kwargs):
    # args[0] = task_manager
    list_details = prompt({
        'type': 'list',
        'message': ' list option ',
        'name': 'list_option',
        'choices': ['pending tasks','concluded','all']
        })['list_option']
    _ = {
        'all':str(args[0]),
        'concluded':args[0].list_concluded(),
        'pending tasks':args[0].list_pending()
        }[list_details]
    print(_)

def next_func(*args,**kwargs):
    # args[0] = task_manager
    tasks = args[0].list_pending(True)
    priorities = set([_[3] for _ in tasks])
    list_priorities = prompt({
        'type': 'list',
        'message': ' list option ',
        'name': 'list_option',
        'choices': ['all']+list(priorities)
        })['list_option']
    if list_priorities=='all':
        for priority in priorities:
            print(args[0].list( [task for task in tasks if task[3]==priority ] ))
        return
    print(args[0].list( [task for task in tasks if task[3]==list_priorities ] ))

def help_func(*args,**kwargs):
    print('''
 task $ <command> # Accepts add, complete, delete, list, next, save and exit as commands
 task $ add <description> [-p <priority>] # Adds a pending task. Can set the task's priority to low, normal or high with the -p (or --priority) option
 task $ complete <id> # Marks a task as done
 task $ delete <id> # Deletes a task
 task $ list # Shows pending tasks. The "all" option shows all tasks
 task $ next # Shows the next task of each priority
    ''')
def exit_func(*args,**kwargs):
    print("\nBye bye")
    sys.exit()

def input_func():
    _ = {
        'type': 'list',
        'message': ' Select task ',
        'name': 'task command',
        'choices': [
            {
                'name': 'Help',
                'value': 'help'
            },
            {
                'name': 'Add',
                'value': 'add'
            },
            {
                'name': 'Complete',
                'value': 'complete'
            },
            {
                'name': 'Delete',
                'value': 'delete'
            },
            {
                'name': 'List',
                'value': 'list'
            },
            {
                'name': 'Next',
                'value': 'next'
            },
            Separator(),
            {
                'name': 'Save',
                'value': 'save'
            },
            {
                'name': 'Exit',
                'value': 'exit'
            }
        ]
    }
    return prompt(_)