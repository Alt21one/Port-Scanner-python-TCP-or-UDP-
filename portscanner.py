import socket
import threading
import tkinter as tk
from tkinter import scrolledtext




# -------- Scan Function --------

def start_scan():

    protocol = entry_protocol.get()
    protocol = protocol.upper()


    target = entry_target.get()

    try:
        target_ip = socket.gethostbyname(target)
    except:
        result_box.insert(tk.END, "Invalid target\n")
        return

    if protocol == "TCP":
        result_box.insert(tk.END, f"Scanning {target_ip}...\n")
        for port in range(1, 65535):
            threading.Thread(target=scan_tcp,args=(target_ip, port),daemon=True).start()


    elif protocol == "UDP":
        result_box.insert(tk.END, f"Scanning {target_ip}...\n")
        for port in range(1, 65535):
            threading.Thread(target=scan_udp,args=(target_ip, port),daemon=True).start()


    elif protocol == "BOTH":
        result_box.insert(tk.END, f"Scanning {target_ip}...\n")
        for port in range(1, 65535):
            threading.Thread(target=scan_tcp,args=(target_ip, port),daemon=True).start()
            threading.Thread(target=scan_udp,args=(target_ip, port),daemon=True).start()
    else:
        result_box.insert(tk.END, "Invalid protocol\n")
        return

    open_ports.clear()
    
    
   
def scan_tcp(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)

    if sock.connect_ex((target_ip, port)) == 0:
        result_box.insert(tk.END, f"TCP Port {port} OPEN\n")

    sock.close()

def scan_udp(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.3)
    try:
        sock.sendto(b"test", (target_ip, port))
        data, addr = sock.recvfrom(1024)
        result_box.insert(tk.END, f"UDP Port {port} OPEN\n")
    except:
        pass

    sock.close()


# -------- GUI --------

open_ports = []

window = tk.Tk()
window.title("Simple Port Scanner")
window.geometry("500x400")

Protocol = tk.Label(window, text="Enter Protocol (TCP or UDP or Both):")
Protocol.pack()

entry_protocol = tk.Entry(window, width=30)
entry_protocol.pack()


label = tk.Label(window, text="Enter Target:")
label.pack()

entry_target = tk.Entry(window, width=30)
entry_target.pack()



scan_button = tk.Button(window, text="Scan", command=start_scan)
scan_button.pack(pady=5)


result_box = scrolledtext.ScrolledText(window, width=60, height=20)
result_box.pack()


window.mainloop()