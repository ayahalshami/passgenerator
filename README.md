
This is a simple Python desktop program for CSI 3480. It uses Tkinter for the window and builds on the password generator and PBKDF2 hashing ideas from our group's earlier notebook.

## Run the program

1. Install Python 
2. Open this folder in File Explorer.
3. Type `cmd` in the address bar and press Enter.
4. Run `py main.py`. If that does not work, try `python main.py`.


## What it does

- Generates passwords with a selected length and character types.
- Gives basic password-strength feedback. 
- Hashes a password using PBKDF2-HMAC-SHA256.
- Creates a new 16-byte random salt every time a password is hashed.
- Checks whether a typed password matches the hash that was just made. The hashing and verification inputs are visible by default for demonstration, with a checkbox to hide them.



