import argparse
import os
import shutil

def create_app_directory(name):
    # Define the directory path in the current directory
    directory_path = os.path.join(os.getcwd(), name)
    
    try:
        # Create a new directory with the provided name
        os.makedirs(directory_path, exist_ok=True)

        master_settings_path = os.path.join(os.path.dirname(__file__), 'settings.py')
        new_settings_path = os.path.join(directory_path, 'settings.py')
        shutil.copyfile(master_settings_path, new_settings_path)

        main_file_path = os.path.join(directory_path, 'main.py')
        with open(main_file_path, 'w') as f:
            f.write("import psx_syntax\n")

        app_dir = os.path.join(directory_path, 'app')
        os.makedirs(app_dir, exist_ok=True)

        routes_dir = os.path.join(app_dir, 'routes')
        os.makedirs(routes_dir, exist_ok=True)

        master_index_path = os.path.join(os.path.dirname(__file__), 'index.py')
        new_index_path = os.path.join(routes_dir, 'index.py')
        shutil.copyfile(master_index_path, new_index_path)
        
        print(f"Created a new Moderne app at {directory_path}")
    except Exception as e:
        print(f"An error occurred while creating the directory: {e}")

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Moderne App Generator")
    
    # Add 'new' command and a positional argument 'name'
    parser.add_argument("command", help="The command to run (e.g., new)")
    parser.add_argument("name", help="The name of the app directory to be created")

    # Parse the arguments
    args = parser.parse_args()

    # Check if the 'new' command is provided
    if args.command == "new":
        create_app_directory(args.name)
    else:
        print("Invalid command. Use 'moderne new <name>' to create a new app.")

if __name__ == "__main__":
    main()