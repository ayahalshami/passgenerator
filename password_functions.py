import hashlib
import hmac
import secrets
import string


def random_length():
    number = secrets.randbelow(20)
    if number <= 8:
        return secrets.choice(range(8, 16))
    if number <= 12:
        return secrets.choice(range(16, 25))
    if number <= 16:
        return secrets.choice(range(25, 40))
    return secrets.choice(range(40, 65))


def make_password(length, lower=True, upper=True, numbers=True, symbols=True):
    if length is None:
        length = random_length()
    if not isinstance(length, int) or isinstance(length, bool) or length < 8 or length > 64:
        raise ValueError("Password length must be between 8 and 64.")

    choices = []
    all_choices = []

    if lower:
        choices.append(string.ascii_lowercase)
        all_choices += [string.ascii_lowercase] * 9
    if upper:
        choices.append(string.ascii_uppercase)
        all_choices += [string.ascii_uppercase] * 4
    if numbers:
        choices.append(string.digits)
        all_choices += [string.digits] * 4
    if symbols:
        choices.append(string.punctuation)
        all_choices += [string.punctuation] * 3

    if not choices:
        raise ValueError("Choose at least one character type.")

    password = []
    for group in choices:
        password.append(secrets.choice(group))

    while len(password) < length:
        group = secrets.choice(all_choices)
        password.append(secrets.choice(group))

    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def get_strength(password):
    if not password:
        return "Not checked", "Enter a password first."

    has_lower = any(letter.islower() for letter in password)
    has_upper = any(letter.isupper() for letter in password)
    has_number = any(letter.isdigit() for letter in password)
    has_symbol = any(letter in string.punctuation for letter in password)
    types = sum([has_lower, has_upper, has_number, has_symbol])

    for word in ["password", "1234", "qwerty", "admin", "letmein"]:
        if word in password.lower():
            return "Weak", "This password contains a common pattern."

    if len(password) >= 16 and types >= 3:
        if not has_symbol:
            return "Strong", "Good length and variety. You could also add a special character."
        return "Strong", "Good length and a mix of characters. Keep it unique."

    if len(password) >= 12 and types >= 2:
        rating = "Moderate"
    else:
        rating = "Weak"

    tips = []
    if len(password) < 12:
        tips.append("at least 12 characters")
    elif len(password) < 16:
        tips.append("a longer password (16+ characters)")
    if not has_lower:
        tips.append("lowercase letters")
    if not has_upper:
        tips.append("uppercase letters")
    if not has_number:
        tips.append("numbers")
    if not has_symbol:
        tips.append("a special character")

    if tips:
        return rating, "To improve it, try " + ", ".join(tips) + "."
    return rating, "Try a longer, more varied password."


def make_hash(password):
    if not password:
        raise ValueError("Enter a password first.")

    salt = secrets.token_bytes(16)
    result = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600000)
    return "pbkdf2_sha256$600000$" + salt.hex() + "$" + result.hex()


def check_hash(password, saved_hash):
    try:
        method, count, salt_text, hash_text = saved_hash.split("$")
        count = int(count)
        salt = bytes.fromhex(salt_text)
        expected = bytes.fromhex(hash_text)

        if method != "pbkdf2_sha256" or count < 1 or count > 2000000:
            return False
        if len(salt) != 16 or len(expected) != 32:
            return False

        result = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, count)
        return hmac.compare_digest(result, expected)
    except (ValueError, TypeError, AttributeError):
        return False
