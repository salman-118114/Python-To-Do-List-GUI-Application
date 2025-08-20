import os
import PySimpleGUI as sg

# Define the file name for the to-do list
FILENAME = "todolist.txt"

def add_task(task_description):
    """
    Adds a new task to the to-do list file.
    Each task is formatted with a completion status indicator "[ ]".
    """
    with open(FILENAME, "a") as file:
        file.write(f"[ ] {task_description}\n")

def view_tasks():
    """
    Reads all tasks from the to-do list file.
    Returns a list of tasks. Returns an empty list if the file is empty or doesn't exist.
    """
    if not os.path.exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        return []
    
    with open(FILENAME, "r") as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def update_tasks_file(updated_tasks):
    """
    A helper function to write the entire list of tasks back to the file.
    This is more efficient than reading and writing inside each function.
    """
    with open(FILENAME, "w") as file:
        file.writelines(f"{task}\n" for task in updated_tasks)

def mark_completed(task_index):
    """
    Marks a task as completed based on its index in the list.
    Returns True if the task was successfully marked, False otherwise.
    """
    tasks = view_tasks()
    if 0 <= task_index < len(tasks):
        current_task = tasks[task_index]
        if "[ ]" in current_task:
            tasks[task_index] = current_task.replace("[ ]", "[x]", 1)
            update_tasks_file(tasks)
            return True
    return False

def delete_task(task_index):
    """
    Deletes a task based on its index in the list.
    Returns True if the task was successfully deleted, False otherwise.
    """
    tasks = view_tasks()
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
        update_tasks_file(tasks)
        return True
    return False

def edit_task(task_index, new_description):
    """
    Edits a task's description based on its index in the list.
    Preserves the completion status ([ ] or [x]).
    Returns True if the task was successfully edited, False otherwise.
    """
    tasks = view_tasks()
    if 0 <= task_index < len(tasks):
        old_task = tasks[task_index]
        # Get the status part of the task (e.g., "[ ]" or "[x]")
        status = old_task.split(' ', 1)[0]
        tasks[task_index] = f"{status} {new_description}"
        update_tasks_file(tasks)
        return True
    return False

def main():
    """Main function to run the to-do list GUI application."""
    
    # Define the GUI layout
    layout = [
        [sg.Text('To-Do List', font=('Helvetica', 20), justification='center', expand_x=True)],
        [sg.Listbox(values=view_tasks(), size=(40, 10), key='-LIST-', enable_events=True, bind_return_key=True)],
        [sg.Input(key='-INPUT-', expand_x=True), sg.Button('Add Task', bind_return_key=True)],
        [sg.Button('Mark Completed'), sg.Button('Edit Task'), sg.Button('Delete Task'), sg.Button('Exit')]
    ]

    # Create the window
    window = sg.Window('My To-Do App', layout)

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        
        # If user closes window or clicks Exit button
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        # Get the index of the selected item in the listbox
        selected_indices = values['-LIST-']
        selected_index = selected_indices[0] if selected_indices else None

        if event == 'Add Task':
            task = values['-INPUT-']
            if task:
                add_task(task)
                # Refresh the Listbox and clear the input field
                window['-LIST-'].update(view_tasks())
                window['-INPUT-'].update('')
            else:
                sg.popup_ok("Please enter a task.")

        elif event == 'Mark Completed':
            if values['-LIST-']:
                # Get the full string of the selected task from the Listbox
                selected_task_full_string = values['-LIST-'][0]
                
                # Get the full list of tasks from the file
                tasks_list = view_tasks()
                
                try:
                    # Find the integer index of the selected task string
                    selected_index = tasks_list.index(selected_task_full_string)
                    
                    # Pass the correct integer index to the mark_completed function
                    if mark_completed(selected_index):
                        window['-LIST-'].update(view_tasks())
                    else:
                        sg.popup_ok("This task is already completed.")
                        
                except ValueError:
                    # This handles cases where the task might not be found
                    sg.popup_ok("Error: The selected task could not be found.")
                    
            else:
                sg.popup_ok("Please select a task to mark.")
        elif event == 'Edit Task':
            if values['-LIST-']:
                # Get the full string of the selected task
                selected_task_full_string = values['-LIST-'][0]
                # Get the task description part by slicing
                old_task_description = selected_task_full_string[4:].strip()
                
                # Get the new task description from the user
                new_task = sg.popup_get_text("Edit task:", default_text=old_task_description)
                
                if new_task:
                    # Find the original index of the task to edit
                    tasks = view_tasks()
                    try:
                        task_index_to_edit = tasks.index(selected_task_full_string)
                        edit_task(task_index_to_edit, new_task)
                        window['-LIST-'].update(view_tasks())
                    except ValueError:
                        sg.popup_ok("Error: Task not found in list.")
            else:
                sg.popup_ok("Please select a task to edit.")

        elif event == 'Delete Task':
            if values['-LIST-']:
                # Get the full string of the selected task from the Listbox
                selected_task_full_string = values['-LIST-'][0]
                
                # Get the full list of tasks from the file
                tasks_list = view_tasks()
                
                try:
                    # Find the integer index of the selected task string
                    selected_index = tasks_list.index(selected_task_full_string)
                    
                    if sg.popup_ok_cancel("Are you sure you want to delete this task?") == 'OK':
                        # Pass the correct integer index to the delete_task function
                        delete_task(selected_index)
                        window['-LIST-'].update(view_tasks())
                except ValueError:
                    # This handles cases where the task might not be found
                    sg.popup_ok("Error: The selected task could not be found.")
            else:
                sg.popup_ok("Please select a task to delete.")
    
    window.close()

if __name__ == "__main__":
    main()