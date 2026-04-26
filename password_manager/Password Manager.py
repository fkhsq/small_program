import math
import json
import os 

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

FIXED_SHIFT = 7

# Create folder
DATA_FOLDER = "password_manager_data"  # Folder name

# If the folder does not exist, create it
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# File paths
DATA_FILE = os.path.join(DATA_FOLDER, "passwords.json")
ACCOUNT_FILE = os.path.join(DATA_FOLDER, "admin.json")

passwords = []
current_admin = None

#Encrypted Caesar Cipher
def caesar_encrypt(text, shift):

     result = list(text)

     for i in range(len(text)):
         # check if character is in alphabet
        if text[i] not in ALPHABET:
            continue  # non-alphabet characters remain unchanged
        
        j=0
        while True: 
            if ALPHABET[j]==text[i]:
                break
            j=j+1
        k=j+shift  #Obtain the position of the new letter in variable a by adding the original letter's position in variable a to the length of the backward shift.
        
        # Handle index out of range for both encryption and decryption
        while k >= len(ALPHABET): # if position exceeds alphabet length, move backward
            k = k - len(ALPHABET)  # adjust overflow position
        
        result[i]=ALPHABET[k] #Change the old letters to new letters

     return "".join(result)


#Decrypting the Caesar Cipher
def caesar_decrypt(text, shift):

     result = list(text)

     for i in range(len(text)):
         # check if character is in alphabet
        if text[i] not in ALPHABET:
            continue  # non-alphabet characters remain unchanged
        
        j=0
        while True: 
            if ALPHABET[j]==text[i]:
                break
            j=j+1
        k=j-shift  #Obtain the position of the new letter in variable a by adding the original letter's position in variable a to the length of the backward shift.
        
        # Handle index out of range for both encryption and decryption
        while k <0: # if position exceeds alphabet length, move backward
            k = k + len(ALPHABET)  # adjust overflow position
        
        result[i]=ALPHABET[k] #Change the old letters to new letters
     return "".join(result)

#Load administrator account file
def load_admin_account():
    global current_admin
    
    if os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("username"), data.get("password")
    return None, None

#Save administrator account to file
def save_admin_account(username, password):
    data = {
        "username": username,
        "password": password
    }
    with open(ACCOUNT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

#Create a new administrator account
def create_admin_account():
    print(f"\n{'='*50}")
    print(f"First time use, please create an admin account")
    print(f"{'='*50}")
    
    while True:
        username = input(f"Please enter the administrator username: ").strip()
        if username == "":
            print(f"Username cannot be empty, please re-enter")
            continue
        break
    
    while True:
        password = input(f"Please enter the administrator password: ").strip()
        if password == "":
            print(f"Password cannot be empty, please re-enter")
            continue
        confirm = input(f"Please enter the password again: ").strip()
        if password != confirm:
            print(f"The passwords entered twice do not match, please re-enter.")
            continue
        break

    # Save the administrator account (password is stored using Caesar cipher encryption)
    encrypted_pwd = caesar_encrypt(password, 17)  # Use shift 17
    save_admin_account(username, encrypted_pwd)
    
    print(f"Administrator account created successfully!")
    print(f"  Username: {username}")
    return username

# Admin login
def login():
    global current_admin
    
    print(f"\n{'='*50}")
    print(f"Password Manager - Account Login")
    print(f"{'='*50}")
    
    # Check if an account already exists
    saved_username, saved_encrypted_pwd = load_admin_account()
    
    # If no account exists, go directly to registration process
    if saved_username is None:
        print(f"\nFirst-time use detected. Please register an admin account first.")
        current_admin = create_admin_account()
        return True
    
    # Account exists, enter login loop
    while True:
        print(f"\nPlease select an option:")
        print(f"  1. Login to existing account")
        print(f"  2. Register a new account")
        print(f"  3. Exit program")
        
        choice = input(f"\nEnter your choice (1/2/3): ").strip()
        
        if choice == "1":
            # Login to existing account
            username = input(f"\nEnter admin username: ").strip()
            password = input(f"Enter admin password: ").strip()
            
            # Verify username
            if username != saved_username:
                print(f"Username is incorrect!")
                # Ask whether to retry login or register
                retry = input(f"\nDo you want to retry login? (y/n): ").lower()
                if retry == 'y':
                    continue
                else:
                    return False
            
            # Verify password (compare after decryption)
            decrypted_pwd = caesar_decrypt(saved_encrypted_pwd, 17)
            if password != decrypted_pwd:
                print(f"Password is incorrect!")
                retry = input(f"\nDo you want to retry login? (y/n): ").lower()
                if retry == 'y':
                    continue
                else:
                    return False
            
            # Login successful
            current_admin = username
            print(f"\nLogin successful! Welcome back, {username}")
            return True
        
        elif choice == "2":
            # Register a new account
            print(f"\n⚠ Note: Registering a new account will overwrite existing account data")
            confirm = input(f"Confirm you want to register a new account? (y/n): ").lower()
            if confirm == 'y':
                # Delete old account file
                if os.path.exists(ACCOUNT_FILE):
                    os.remove(ACCOUNT_FILE)
                    print(f"Old account data has been deleted")
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                # Create a new account
                current_admin = create_admin_account()
                return True
            else:
                print(f"Registration cancelled")
                continue
        
        elif choice == "3":
            print(f"\nProgram exited")
            return False
        
        else:
            print(f"\nInvalid choice. Please enter 1, 2, or 3")

# Load password data from file
def load_passwords():
    global passwords
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            passwords = json.load(f)
        print(f"Loaded {len(passwords)} password record(s)")
    else:
        passwords = []
        print(f"Data file not found. A new file will be created.")

# Save password data to file
def save_passwords():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(passwords, f, indent=4, ensure_ascii=False)

# Add a new password record (password will be automatically encrypted for storage)
def add_password():
    print(f"\n{'='*50}")
    print(f"Add New Password")
    print(f"{'='*50}")
    print(f"Note: Password will be encrypted using Caesar cipher")
    
    username = input(f"Enter username: ").strip()
    if username == "":
        print(f"Username cannot be empty!")
        return
    
    password = input(f"Enter password: ").strip()
    if password == "":
        print(f"Password cannot be empty!")
        return
    
    # Check if username already exists
    for item in passwords:
        if item["username"] == username:
            print(f"Username '{username}' already exists!")
            overwrite = input(f"Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                return
            passwords.remove(item)
            break
    
    # Encrypt password using fixed shift of 7
    encrypted_password = caesar_encrypt(password, FIXED_SHIFT)
    
    # Store record
    record = {
        "username": username,
        "password": encrypted_password,
        "shift": FIXED_SHIFT
    }
    passwords.append(record)
    save_passwords()
    
    print(f"Password record successfully added!")
    print(f"  Username: {username}")


# Use linear search to find a record by username
def linear_search_by_username(target_username):
    comparisons = 0
    found_record = None
    
    print(f"\n--- Searching for username '{target_username}' ---")
    
    for i in range(len(passwords)):
        if passwords[i]["username"] == target_username:
            found_record = passwords[i]
            break
    
    if found_record is None:
        print(f"Record with username '{target_username}' not found")
        return None
    else:
        print(f"Record found!")
        return found_record

# Search by username
def search_by_username():
    if len(passwords) == 0:
        print(f"\nNo password records yet. Please add a record first.")
        return
    
    target = input(f"\nEnter the username to search for: ").strip()
    if target == "":
        print(f"Username cannot be empty!")
        return
    
    found = linear_search_by_username(target)
    
    if found:
        print(f"\nRecord found:")
        print(f"  Username: {found['username']}")

        # Ask whether to view the decrypted password
        show = input(f"\nDo you want to view the decrypted password? (y/n): ").lower()
        if show == 'y':
            pwd_input = input(f"\nPlease enter admin password to view decrypted password: ").strip()
            
            # 验证管理员密码
            saved_username, saved_encrypted_pwd = load_admin_account()
            decrypted_admin_pwd = caesar_decrypt(saved_encrypted_pwd, 17)
            
            if pwd_input != decrypted_admin_pwd:
                print(f"\n❌ Incorrect admin password! Cannot show decrypted password.")
                print(f"  Encrypted password: {found['password']}")
            else:
                decrypted = caesar_decrypt(found["password"], found["shift"])
                print(f"\n✓ Password correct!")
            print(f"  Decrypted password: {decrypted}")
        else:
            print(f"  Encrypted password: {found['password']}")

# Sort by username using selection sort
def selection_sort_by_username():
    if len(passwords) == 0:
        return []
    
    L = passwords.copy()
    n = len(L)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if L[j]["username"] < L[min_idx]["username"]:
                min_idx = j
        
        if min_idx != i:
            L[i], L[min_idx] = L[min_idx], L[i]
    return L


# Display all saved password records
def display_all_passwords():
    if len(passwords) == 0:
        print(f"\nNo password records yet. Please add a record first.")
        return
    
    print(f"\n{'='*60}")
    print(f"All Saved Password Records")
    print(f"{'='*60}")
    
    # Sort by username using selection sort
    sorted_list = selection_sort_by_username()
    
    # Choose display method
    print(f"\nPlease choose a display method:")
    print(f"  1. Enter password to view decrypted passwords")
    print(f"  2. View encrypted passwords directly (no password required)")
    
    choice = input(f"\nEnter your choice (1/2): ").strip()
    
    if choice == "1":
        # Need to enter admin password
        pwd_input = input(f"\nEnter admin password: ").strip()
        
        # Verify admin password
        saved_username, saved_encrypted_pwd = load_admin_account()
        decrypted_admin_pwd = caesar_decrypt(saved_encrypted_pwd, 17)
        
        if pwd_input != decrypted_admin_pwd:
            print(f"\nIncorrect password! You can only view encrypted passwords.")
            show_encrypted = True
        else:
            print(f"\nPassword correct! Displaying decrypted passwords.")
            show_encrypted = False
    else:
        print(f"\nYou chose to view encrypted passwords directly.")
        show_encrypted = True
    
    print(f"\n{'Username':<20} {'Password':<30}")
    print(f"{'-'*60}")
    
    for record in sorted_list:
        if show_encrypted:
            print(f"{record['username']:<20} {record['password']:<30}")
        else:
            decrypted_pwd = caesar_decrypt(record["password"], record["shift"])
            print(f"{record['username']:<20} {decrypted_pwd:<30} ")
    
    print(f"{'='*60}")
    print(f"Total {len(passwords)} record(s)")


# Delete a password record
def delete_password():
    if len(passwords) == 0:
        print(f"\nNo password records yet. Please add a record first.")
        return
    
    print(f"\n{'='*50}")
    print(f"Delete Password Record")
    print(f"{'='*50}")
    
    username = input(f"Enter the username to delete: ").strip()
    
    for i in range(len(passwords)):
        if passwords[i]["username"] == username:
            passwords.pop(i)
            save_passwords()
            print(f"✓ Successfully deleted record for username '{username}'")
            return
    
    print(f"Record with username '{username}' not found")

# Display the main menu
def show_menu():
    print(f"\n{'='*50}")
    print(f"        Password Manager")
    print(f"        Current Admin: {current_admin}")
    print(f"{'='*50}")
    print(f"1. Add new password record (password automatically encrypted, fixed shift of {FIXED_SHIFT})")
    print(f"2. Search by username (linear search)")
    print(f"3. View all password records (automatically sorted by username)")
    print(f"4. Delete a password record")
    print(f"0. Exit and save")
    print(f"{'='*50}")

# Main program
def main():
    print(f"\n{'='*50}")
    print(f"Welcome to Password Manager!")
    print(f"Your passwords will be encrypted and stored using Caesar cipher")
    print(f"{'='*50}")
    
    # Admin login
    if not login():
        print(f"\nProgram exited")
        return
    
    # Load existing password data
    load_passwords()
    
    while True:
        show_menu()
        choice = input(f"Please select an option (0-4): ")
        
        if choice == "1":
            add_password()
        
        elif choice == "2":
            search_by_username()
        
        elif choice == "3":
            display_all_passwords()
        
        elif choice == "4":
            delete_password()
        
        elif choice == "0":
            save_passwords()
            print(f"\nData has been saved!")
            print(f"Thank you for using Password Manager! Goodbye!")
            break
        
        else:
            print(f"Error! Please enter a number between 0 and 4")
        
        print(f"\n{'='*50}")
        print(f"Press Enter to continue...")
        input()


if __name__ == "__main__":
    main()

