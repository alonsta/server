import os
import server_procs


def log_requests(info):
    log_file_path = "Server_Logs.txt"

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as logs:
            file_text = logs.read()

        try:
            index = file_text.index(info.split(" ")[0]) + 9
            print("Index found:", index)
            before = file_text[:index]
            after = file_text[index:]
            middle = "\n\t " + info
            file_text = before + middle + after

            with open(log_file_path, "w") as logs:
                logs.writelines(file_text)

        except ValueError:
            print("New user")
            print(info.split(":")[0])
            new_entry = "started serving " + info.split(" ")[0] + "\n\t" + info + "\n"
            with open(log_file_path, "a") as logs:
                logs.write(new_entry)

    else:
        new_entry = "started serving " + info.split(" ")[0] + "\n\t" + info + "\n"
        with open(log_file_path, "a") as logs:
            logs.write("This is a log file for server.py\nWritten by: Alon Stavitsky\n\n")
            logs.write(new_entry)
            print("Opened a new log file")


def log_format(data, user="server_com", msg="none"):
    time = server_procs.r_time()
    return user + " requested: " + data + " // server replied: " + msg + "\t" + time


def format_z(info):
    length2 = str(len(info))
    length1 = str(len(length2)).zfill(4)
    return length1 + length2 + info