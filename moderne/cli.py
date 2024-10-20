import argparse
import os
import shutil
import subprocess
import socket
import importlib.resources as pkg_resources
import webbrowser
import moderne.templates

def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(('localhost', port)) == 0

def find_next_available_port(starting_port=8000):
    """Find the next available port starting from the specified port."""
    port = starting_port
    while is_port_in_use(port):
        port += 1
    return port

def run_uvicorn(port=8000):
    """Run Uvicorn server with a specific port and hot-reload enabled."""
    try:
        if is_port_in_use(port):
            print(f"Port {port} is already in use.")
            response = input(f"Do you want to use the next available port (starting from {port + 1})? (y/n): ").strip().lower()
            if response == 'y':
                port = find_next_available_port(port + 1)
                print(f"Using port {port} instead.")

        subprocess.Popen(["uvicorn", "app:app", "--reload", "--port", str(port)])
        
        url = f"http://localhost:{port}"
        print(f"Opening {url} in your default browser")
        webbrowser.open(url)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Uvicorn: {e}")


def create_app_directory(name):
    directory_path = os.path.join(os.getcwd(), name)

    try:
        os.makedirs(directory_path, exist_ok=True)

        # Use pkg_resources to copy files from the 'templates' package
        with pkg_resources.path(moderne.templates, 'settings.py') as master_settings:
            new_settings_path = os.path.join(directory_path, 'settings.py')
            shutil.copyfile(master_settings, new_settings_path)

        with open(new_settings_path, 'a') as f:
            f.write(f"\n# App-specific settings\nAPP_NAME = '{name}'\n")

        with pkg_resources.path(moderne.templates, 'main.py') as master_main:
            new_main_path = os.path.join(directory_path, 'main.py')
            shutil.copyfile(master_main, new_main_path)

        with pkg_resources.path(moderne.templates, 'app.py') as master_app:
            new_app_path = os.path.join(directory_path, 'app.py')
            shutil.copyfile(master_app, new_app_path)

        app_dir = os.path.join(directory_path, 'app')
        os.makedirs(app_dir, exist_ok=True)

        routes_dir = os.path.join(app_dir, 'routes')
        os.makedirs(routes_dir, exist_ok=True)

        static_dir = os.path.join(app_dir, 'static')
        os.makedirs(static_dir, exist_ok=True)

        with pkg_resources.path(moderne.templates, 'index.py') as master_index:
            new_index_path = os.path.join(routes_dir, 'index.py')
            shutil.copyfile(master_index, new_index_path)

        with pkg_resources.path(moderne.templates, 'index.html') as master_index_html:
            new_index_html_path = os.path.join(static_dir, 'index.html')
            shutil.copyfile(master_index_html, new_index_html_path)

        with pkg_resources.path(moderne.templates, 'moderne.png') as master_logo:
            new_logo_path = os.path.join(static_dir, 'moderne.png')
            shutil.copyfile(master_logo, new_logo_path)

        print(f"Created a new Moderne app at {directory_path}")
    except Exception as e:
        print(f"An error occurred while creating the directory: {e}")

def main():
    """CLI entry point."""
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Moderne App Generator and Runner")
    
    # Add 'new' and 'run' commands
    parser.add_argument("command", help="The command to run (e.g., new or run)")
    parser.add_argument("name", nargs='?', help="The name of the app directory to be created (for 'new' command)")
    parser.add_argument("--port", type=int, help="The port to run the development server on (for 'run' command)", default=8000)

    # Parse the arguments
    args = parser.parse_args()

    # Check which command is provided
    if args.command == "new":
        if args.name:
            create_app_directory(args.name)
        else:
            print("Please provide a name for the new app. Usage: 'moderne new <name>'")
    elif args.command == "run":
        run_uvicorn(port=args.port)
    else:
        print("Invalid command. Use 'moderne new <name>' to create a new app or 'moderne run' to run the development server.")

if __name__ == "__main__":
    main()
