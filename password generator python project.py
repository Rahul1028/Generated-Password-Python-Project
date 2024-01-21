import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

def is_strong_password(password):
    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)
    
    return has_lowercase and has_uppercase and has_digit and has_special

def generate_password_strength(length, strength):
    if strength == "strong":
        return generate_strong_password(length)
    elif strength == "medium":
        return generate_medium_password(length)
    else:
        return generate_weak_password(length)

def generate_strong_password(length=12):
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digit_chars = string.digits
    special_chars = string.punctuation

    characters = lowercase_chars + uppercase_chars + digit_chars + special_chars

    password = secrets.choice(lowercase_chars)
    password += secrets.choice(uppercase_chars)
    password += secrets.choice(digit_chars)
    password += secrets.choice(special_chars)

    password += ''.join(secrets.choice(characters) for _ in range(length - 4))

    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)

    return password

def generate_medium_password(length=12):
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digit_chars = string.digits

    characters = lowercase_chars + uppercase_chars + digit_chars

    password = secrets.choice(lowercase_chars)
    password += secrets.choice(uppercase_chars)
    password += secrets.choice(digit_chars)

    password += ''.join(secrets.choice(characters) for _ in range(length - 3))

    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)

    return password

def generate_weak_password(length=12):
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase

    characters = lowercase_chars + uppercase_chars

    password = secrets.choice(lowercase_chars)
    password += secrets.choice(uppercase_chars)

    password += ''.join(secrets.choice(characters) for _ in range(length - 2))

    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)

    return password

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def reset_gui():
    username_var.set("")
    length_var.set("12")
    num_var.set("1")
    copy_to_clipboard_var.set(False)
    result_text.delete(1.0, tk.END)

def accept_password():
    selected_password = result_text.get("1.0", tk.END).strip()
    username = username_var.get()

    if not selected_password:
        messagebox.showerror("Error", "No password generated to accept.")
        return

    if not username:
        messagebox.showwarning("Warning", "Username is empty. It is recommended to associate a username with the generated password.")

    messagebox.showinfo("Password Accepted", f"Password for {username} accepted:\n\n{selected_password}")

def generate_passwords_wrapper():
    password_length = int(length_var.get())
    num_passwords = int(num_var.get())
    strength = strength_var.get()
    passwords = [generate_password_strength(password_length, strength) for _ in range(num_passwords)]

    result_text.delete(1.0, tk.END)
    for idx, password in enumerate(passwords, start=1):
        strength_indicator = "Strong" if is_strong_password(password) else "Weak"
        
        # Set color based on strength
        color = "green" if is_strong_password(password) else "red"
        
        # Display password with color and strength label
        result_text.insert(tk.END, f"{idx}. {password} ({strength_indicator})", color)
        result_text.insert(tk.END, "\n")

    if copy_to_clipboard_var.get():
        copy_to_clipboard(passwords[0])
        messagebox.showinfo("Password Copied", "The first password has been copied to the clipboard.")

# GUI setup
root = tk.Tk()
root.title("Password Generator")

# Set the background color to light blue
root.configure(bg='#add8e6')

# Create a custom style for frame, radiobutton, and checkbutton
style = ttk.Style(root)
style.configure("LightBlue.TFrame", background='#add8e6')
style.configure("LightBlue.TRadiobutton", background='#add8e6')
style.configure("LightBlue.TCheckbutton", background='#add8e6')

# Set the window size to medium
window_width = 800
window_height = 600
root.geometry(f"{window_width}x{window_height}")

# Input frame
input_frame = ttk.Frame(root, padding="20", style="LightBlue.TFrame")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(input_frame, text="Username:", background='#add8e6').grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
username_var = tk.StringVar()
username_entry = ttk.Entry(input_frame, textvariable=username_var, width=20)
username_entry.grid(row=0, column=1, sticky=tk.W, pady=10)

ttk.Label(input_frame, text="Password Length:", background='#add8e6').grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
length_var = tk.StringVar()
length_entry = ttk.Entry(input_frame, textvariable=length_var, width=5)
length_entry.grid(row=1, column=1, sticky=tk.W, pady=10)

ttk.Label(input_frame, text="Number of Passwords:", background='#add8e6').grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
num_var = tk.StringVar()
num_entry = ttk.Entry(input_frame, textvariable=num_var, width=5)
num_entry.grid(row=2, column=1, sticky=tk.W, pady=10)

# Use a Frame for the Checkbutton to set background color
checkbox_frame = ttk.Frame(input_frame, style="LightBlue.TFrame")
checkbox_frame.grid(row=3, columnspan=2, pady=10, sticky=tk.W)
copy_to_clipboard_var = tk.BooleanVar()
copy_checkbox = ttk.Checkbutton(checkbox_frame, text="Copy first password to clipboard", variable=copy_to_clipboard_var, style="LightBlue.TCheckbutton")
copy_checkbox.grid(row=0, column=0, sticky=tk.W, pady=10)

# Strength buttons
strength_var = tk.StringVar(value="strong")
strong_button = ttk.Radiobutton(input_frame, text="Strong", variable=strength_var, value="strong", style="LightBlue.TRadiobutton")
strong_button.grid(row=4, column=0, sticky=tk.W, pady=10)
medium_button = ttk.Radiobutton(input_frame, text="Medium", variable=strength_var, value="medium", style="LightBlue.TRadiobutton")
medium_button.grid(row=4, column=1, sticky=tk.W, pady=10)
weak_button = ttk.Radiobutton(input_frame, text="Weak", variable=strength_var, value="weak", style="LightBlue.TRadiobutton")
weak_button.grid(row=4, column=2, sticky=tk.W, pady=10)

generate_button = ttk.Button(input_frame, text="Generate Passwords", command=generate_passwords_wrapper)
generate_button.grid(row=5, column=0, columnspan=3, pady=10)

# Result frame
result_frame = ttk.Frame(root, padding="20", style="LightBlue.TFrame")
result_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20)

result_text = tk.Text(result_frame, height=15, width=30, background='#add8e6')
result_text.grid(row=0, column=0, sticky=tk.W)

# Add tags for different text colors
result_text.tag_configure("green", foreground="green")
result_text.tag_configure("red", foreground="red")

# Accept and Reset buttons
accept_button = ttk.Button(result_frame, text="Accept Password", command=accept_password)
accept_button.grid(row=1, column=0, pady=10)

reset_button = ttk.Button(result_frame, text="Reset", command=reset_gui)
reset_button.grid(row=2, column=0, pady=10)

# Run the GUI
root.mainloop()
