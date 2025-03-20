import csv
import zmq 
import json
import os
import platform
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout

def export(data):
    """Handles exporting a file to the downloads folder."""
    filename = "new_export.csv"

    if platform.system() == "Windows":
        downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        downloads_path = os.path.join(os.path.expanduser("~"), "downloads")
    else:
        raise OSError("Unsupported operating system")

    file_path = os.path.join(downloads_path, filename)
    print(file_path)

    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            reply = 'CSV file created successfully.'
            print(reply)
    except Exception as e:
        reply = f"An error occurred: {e}"
        print(reply)
    return reply

def import_data(data):
    """Handles importing a file."""
    # Expand user-specific paths (e.g., ~/)
    file_path = os.path.expanduser(data)
   
    # Normalize the path (e.g., convert / to \ on Windows)
    file_path = os.path.normpath(file_path)

    # Ensure the path is absolute
    if not os.path.isabs(file_path):
      file_path = os.path.abspath(file_path)

    # Grab data from csv file and format as JSON
    with open(file_path, 'r') as read_obj:
        csv_reader = csv.reader(read_obj) 
    
        # convert string to list 
        list_of_csv = list(csv_reader)
        list_of_csv.pop(0)
 
    return list_of_csv

def server_commands_interface():
    """Handles smooth shutdown of app."""
    global shutdown_flag
    global context

    commands = [
        "exit"
    ]

    completer = WordCompleter(commands)

    session = PromptSession(completer=completer)

    # Run until exit is entered or and error occurs
    while not shutdown_flag:
        with patch_stdout():
            try:
                action = session.prompt("Type exit to close 'Import/Export' app: ", wrap_lines=False)
                parts = action.split()
                cmd = parts[0].lower() if parts else ""

                if cmd == "exit":
                    shutdown_flag = True
                    context.destroy()
                else:
                    print("Invalid Command!!!")

            except Exception as e:
                print(f"Error in server command interface: {e}")
    
if __name__ == "__main__":
    
    global shutdown_flag
    shutdown_flag = False

    # Create the context for communication
    global context
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")

    # Start the thread for the UI
    command_thread = threading.Thread(target=server_commands_interface, daemon=True)
    command_thread.start()

    # Listen for incoming messages
    try:
        while True:
            message = json.loads(socket.recv())
            print(f"Received client request: {message}")
            if len(message) > 0:
                if "import" in message:
                    reply = import_data(message["import"])
                elif "export" in message:
                    reply = export(message["export"])
                socket.send_string(json.dumps(reply))
    finally:
        print("Program terminated.\n")