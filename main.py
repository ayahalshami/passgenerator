import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from password_functions import make_password, get_strength, make_hash, check_hash


def start_app():
    window = tk.Tk()
    window.title("Password Generator and Hashing")
    window.geometry("730x600")
    window.minsize(650, 540)

    password = tk.StringVar()
    length = tk.StringVar(value="16")
    use_random_length = tk.BooleanVar()
    lower = tk.BooleanVar(value=True)
    upper = tk.BooleanVar(value=True)
    numbers = tk.BooleanVar(value=True)
    symbols = tk.BooleanVar(value=True)
    sample = tk.StringVar()
    hash_input = tk.StringVar()
    verify_input = tk.StringVar()
    salt_output = tk.StringVar()
    saved_hash = tk.StringVar()
    show_passwords = tk.BooleanVar(value=True)

    tabs = ttk.Notebook(window)
    tabs.pack(fill="both", expand=True, padx=15, pady=15)
    generator_tab = ttk.Frame(tabs, padding=18)
    hashing_tab = ttk.Frame(tabs, padding=12)
    tabs.add(generator_tab, text="Generate Password")
    tabs.add(hashing_tab, text="Hash Password")

    ttk.Label(generator_tab, text="Password Generator", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 12))

    length_row = ttk.Frame(generator_tab)
    length_row.pack(fill="x", pady=5)
    ttk.Label(length_row, text="Password length (8 to 64):").pack(side="left")
    length_entry = ttk.Entry(length_row, textvariable=length, width=6)
    length_entry.pack(side="left", padx=10)

    def change_length_option():
        if use_random_length.get():
            length_entry.config(state="disabled")
        else:
            length_entry.config(state="normal")

    ttk.Checkbutton(generator_tab, text="Use a random length", variable=use_random_length,
                    command=change_length_option).pack(anchor="w", pady=7)

    options = ttk.LabelFrame(generator_tab, text="Include", padding=10)
    options.pack(fill="x", pady=8)
    ttk.Checkbutton(options, text="Lowercase", variable=lower).pack(side="left", padx=6)
    ttk.Checkbutton(options, text="Uppercase", variable=upper).pack(side="left", padx=6)
    ttk.Checkbutton(options, text="Numbers", variable=numbers).pack(side="left", padx=6)
    ttk.Checkbutton(options, text="Symbols", variable=symbols).pack(side="left", padx=6)

    def update_strength(text):
        rating, details = get_strength(text)
        strength_label.config(text="Strength: " + rating)
        strength_details.config(text=details)

    def generate():
        try:
            size = None if use_random_length.get() else int(length.get())
            new_password = make_password(size, lower.get(), upper.get(), numbers.get(), symbols.get())
            password.set(new_password)
            update_strength(new_password)
        except ValueError as error:
            messagebox.showerror("Password", str(error))

    ttk.Button(generator_tab, text="Generate", command=generate).pack(anchor="w", pady=8)
    ttk.Label(generator_tab, text="Generated password:").pack(anchor="w", pady=(8, 3))
    ttk.Entry(generator_tab, textvariable=password, state="readonly", width=70).pack(fill="x")

    buttons = ttk.Frame(generator_tab)
    buttons.pack(anchor="w", pady=8)

    def copy_password():
        if password.get():
            window.clipboard_clear()
            window.clipboard_append(password.get())
            window.update()

    def use_in_hash():
        if password.get():
            hash_input.set(password.get())
            tabs.select(hashing_tab)

    ttk.Button(buttons, text="Copy Password", command=copy_password).pack(side="left", padx=(0, 8))
    ttk.Button(buttons, text="Send to Hashing", command=use_in_hash).pack(side="left")

    strength_box = ttk.LabelFrame(generator_tab, text="Password Strength", padding=10)
    strength_box.pack(fill="x", pady=7)
    strength_label = ttk.Label(strength_box, text="Strength: Not checked")
    strength_label.pack(anchor="w")
    strength_details = ttk.Label(strength_box, text="Generate or check a password.", wraplength=600)
    strength_details.pack(anchor="w", pady=5)
    sample_row = ttk.Frame(strength_box)
    sample_row.pack(fill="x", pady=2)
    ttk.Entry(sample_row, textvariable=sample).pack(side="left", fill="x", expand=True)
    ttk.Button(sample_row, text="Check Strength", command=lambda: update_strength(sample.get())).pack(side="left", padx=8)

    ttk.Label(hashing_tab, text="Password Hashing", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 8))
    ttk.Label(hashing_tab, text="Enter a password:").pack(anchor="w")
    hash_entry = ttk.Entry(hashing_tab, textvariable=hash_input)
    hash_entry.pack(fill="x", pady=4)

    def hash_it():
        try:
            old = saved_hash.get()
            new = make_hash(hash_input.get())
            saved_hash.set(new)
            salt_output.set(new.split("$")[2])
            hash_text.config(state="normal")
            hash_text.delete("1.0", "end")
            hash_text.insert("1.0", new)
            hash_text.config(state="disabled")
            verify_result.config(text="")
            if old and old != new:
                salt_note.config(text="New salt and hash generated. Try hashing the same password again.")
            else:
                salt_note.config(text="Hash again to see a different salt and hash.")
        except ValueError as error:
            messagebox.showerror("Hashing", str(error))

    ttk.Button(hashing_tab, text="Hash Password / Hash Again", command=hash_it).pack(anchor="w", pady=6)
    ttk.Label(hashing_tab, text="Salt:").pack(anchor="w", pady=(5, 2))
    ttk.Entry(hashing_tab, textvariable=salt_output, state="readonly").pack(fill="x")
    ttk.Label(hashing_tab, text="Saved hash (includes the salt):").pack(anchor="w", pady=(6, 2))
    hash_text = ScrolledText(hashing_tab, height=3, wrap="char", font=("Consolas", 10))
    hash_text.pack(fill="x")
    hash_text.config(state="disabled")
    salt_note = ttk.Label(hashing_tab, text="Hash twice to see a different salt.", wraplength=600)
    salt_note.pack(anchor="w", pady=4)

    verify_box = ttk.LabelFrame(hashing_tab, text="Check Password", padding=8)
    verify_box.pack(fill="x", pady=6)
    ttk.Label(verify_box, text="Type the password again:").pack(anchor="w")
    verify_entry = ttk.Entry(verify_box, textvariable=verify_input)
    verify_entry.pack(fill="x", pady=4)

    def show_or_hide():
        character = "" if show_passwords.get() else "*"
        hash_entry.config(show=character)
        verify_entry.config(show=character)

    ttk.Checkbutton(verify_box, text="Show entered passwords", variable=show_passwords,
                    command=show_or_hide).pack(anchor="w", pady=2)

    def verify():
        if not saved_hash.get():
            messagebox.showinfo("Hashing", "Hash a password first.")
        elif check_hash(verify_input.get(), saved_hash.get()):
            verify_result.config(text="Password matches")
        else:
            verify_result.config(text="Password does not match")

    ttk.Button(verify_box, text="Verify", command=verify).pack(anchor="w", pady=3)
    verify_result = ttk.Label(verify_box, text="")
    verify_result.pack(anchor="w", pady=3)

    window.mainloop()


if __name__ == "__main__":
    start_app()
