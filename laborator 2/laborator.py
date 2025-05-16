import hashlib
import itertools

TARGET_HASH = "0e000d61c1735636f56154f30046be93b3d71f1abbac3cd9e3f80093fdb357ad"

def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
special_chars = "!@#$"
lowercase_letters = "abcdefghijklmnopqrstuvwxyz"

recursive_calls = 0
found = False


def backtrack(password, count_upper, count_digit, count_special, count_lower):
    global recursive_calls, found
    if found:
        return
    recursive_calls += 1

    if len(password) == 6:
        if count_upper == 1 and count_digit == 1 and count_special == 1 and count_lower == 3:
            current_hash = get_hash(password)
            print(f"Testăm parola: {password} -> Hash: {current_hash}")
            if current_hash == TARGET_HASH:
                print(f"Parola găsită: {password}")
                print(f"Număr apeluri recursive: {recursive_calls}")
                found = True
        return

    for char in itertools.chain(uppercase_letters, digits, special_chars, lowercase_letters):
        new_count_upper = count_upper + (char in uppercase_letters)
        new_count_digit = count_digit + (char in digits)
        new_count_special = count_special + (char in special_chars)
        new_count_lower = count_lower + (char in lowercase_letters)

        if new_count_upper <= 1 and new_count_digit <= 1 and new_count_special <= 1 and new_count_lower <= 3:
            backtrack(password + char, new_count_upper, new_count_digit, new_count_special, new_count_lower)

backtrack("", 0, 0, 0, 0)

if not found:
    print("Parola nu a fost găsită. Verifică dacă hash-ul este corect.")