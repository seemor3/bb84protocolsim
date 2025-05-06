import subprocess
import os
import platform

# Get the absolute path of the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))

def open_terminal_mac(script_name):
    full_path = os.path.join(base_dir, script_name)
    command = f"cd '{base_dir}'; python3 '{full_path}'"
    subprocess.Popen([
        "osascript", "-e",
        f'tell application "Terminal" to do script "{command}"'
    ])

def open_terminal(script_name):
    system = platform.system()
    if system == "Darwin":  # macOS
        open_terminal_mac(script_name)
    elif system == "Linux":
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"python3 '{os.path.join(base_dir, script_name)}'; exec bash"])
    elif system == "Windows":
        subprocess.Popen(["cmd", "/c", f"start cmd /k python {os.path.join(base_dir, script_name)}"])
    else:
        print("Unsupported OS for terminal launching.")

# Run the three scripts
open_terminal("server.py")
open_terminal("alice.py")
open_terminal("bob.py")
