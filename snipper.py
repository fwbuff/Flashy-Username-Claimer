import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import threading

# Set up the main Tkinter window
root = tk.Tk()
root.title("InstaSniper by Buff")
root.geometry("600x450")
root.configure(bg="#1e1e1e")

# Fonts and colors
FONT = ("Consolas", 11)
FG = "#ffffff"
BG = "#1e1e1e"
BTN = "#3a3a3a"

# Add Logo to window
logo = Image.open("assets/logo.png")  # Your logo path
logo = logo.resize((150, 150))  # Resize logo to fit
logo = ImageTk.PhotoImage(logo)

logo_label = tk.Label(root, image=logo, bg=BG)
logo_label.pack(pady=10)

# Title Label
title = tk.Label(root, text="InstaSniper 🌌 - Username Monitor", font=("Consolas", 14, "bold"), fg="#00ffcc", bg=BG)
title.pack(pady=10)

# Instagram Login Frame
login_frame = tk.Frame(root, bg=BG)
login_frame.pack(pady=20)

# Instagram Login Fields
insta_user_label = tk.Label(login_frame, text="Instagram Username:", font=FONT, fg=FG, bg=BG)
insta_user_label.grid(row=0, column=0, padx=5, pady=5)

insta_pass_label = tk.Label(login_frame, text="Instagram Password:", font=FONT, fg=FG, bg=BG)
insta_pass_label.grid(row=1, column=0, padx=5, pady=5)

insta_user_var = tk.StringVar()
insta_pass_var = tk.StringVar()

insta_user_entry = tk.Entry(login_frame, textvariable=insta_user_var, font=FONT, width=30, bg="#2e2e2e", fg=FG, insertbackground=FG)
insta_user_entry.grid(row=0, column=1, padx=5, pady=5)

insta_pass_entry = tk.Entry(login_frame, textvariable=insta_pass_var, font=FONT, width=30, show="*", bg="#2e2e2e", fg=FG, insertbackground=FG)
insta_pass_entry.grid(row=1, column=1, padx=5, pady=5)

# Function to handle Instagram login
def login_instagram():
    username = insta_user_var.get().strip()
    password = insta_pass_var.get().strip()
    
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password!")
        return
    
    # Check Instagram login (this is a mock function, replace with actual login logic)
    messagebox.showinfo("Login", "Instagram login successful!")

# Instagram login button
login_btn = tk.Button(login_frame, text="Login to Instagram", font=FONT, command=login_instagram, bg=BTN, fg=FG)
login_btn.grid(row=2, column=0, columnspan=2, pady=10)

# Entry Frame to input usernames
entry_frame = tk.Frame(root, bg=BG)
entry_frame.pack()

username_var = tk.StringVar()
username_entry = tk.Entry(entry_frame, textvariable=username_var, font=FONT, width=30, bg="#2e2e2e", fg=FG, insertbackground=FG)
username_entry.pack(side=tk.LEFT, padx=5)

# Function to add username to the listbox
def add_username():
    username = username_var.get().strip()
    if username:
        username_listbox.insert(tk.END, username + " - [checking]")
        username_var.set("")  # Clear the entry box
    else:
        messagebox.showwarning("Warning", "Enter a username first!")

add_btn = tk.Button(entry_frame, text="Add Username", font=FONT, command=add_username, bg=BTN, fg=FG)
add_btn.pack(side=tk.LEFT)

# Listbox to display usernames and their status
username_listbox = tk.Listbox(root, font=FONT, bg="#2e2e2e", fg=FG, height=10, width=50, selectbackground="#00ffcc")
username_listbox.pack(pady=20)

# Status Bar at the bottom
status_bar = tk.Label(root, text="Ready to start monitoring...", bg=BG, fg=FG, font=("Consolas", 10))
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Function to check availability (mock function for now)
def check_availability(username):
    url = f"https://www.instagram.com/{username}/"
    try:
        response = requests.get(url)
        if response.status_code == 404:  # Username is available
            return "✅ AVAILABLE"
        else:
            return "❌ TAKEN"
    except Exception as e:
        return "Error checking availability"

# Function to monitor usernames (checking availability in the background)
def monitor_usernames():
    while True:
        for i in range(username_listbox.size()):
            entry = username_listbox.get(i)
            username = entry.split(" - ")[0]
            status = check_availability(username)
            username_listbox.delete(i)
            username_listbox.insert(i, f"{username} - {status}")
        time.sleep(15)  # Wait 15 seconds before checking again

def start_monitoring():
    status_bar.config(text="Monitoring in progress...")
    threading.Thread(target=monitor_usernames, daemon=True).start()
    messagebox.showinfo("Sniping Started", "Monitoring usernames every 15s!")

# Start Monitoring button
start_btn = tk.Button(root, text="Start Monitoring", font=FONT, bg="#008080", fg=FG, width=20, command=start_monitoring)
start_btn.pack(pady=10)

# Start Tkinter event loop
root.mainloop()
