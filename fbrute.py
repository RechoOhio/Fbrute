import requests
import time
from urllib.parse import urlparse, parse_qs
import sys

def get_fb_credentials_from_url(url):
    """Extract email/username from Facebook URL if present"""
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if 'email' in query:
            return query['email'][0]
        elif 'username' in query:
            return query['username'][0]
        elif 'id' in query:
            return query['id'][0]
    except:
        pass
    return None

def load_wordlist(wordlist_path):
    """Load passwords from a wordlist file"""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Error: Wordlist file not found at {wordlist_path}")
        return None

def generate_bruteforce_pattern(length, charset):
    """Generate passwords for brute-force attack"""
    from itertools import product
    for candidate in product(charset, repeat=length):
        yield ''.join(candidate)

def attempt_login(email, password, session):
    """login attempt (./.)"""
    print(f"Trying: {password}")
    time.sleep(0.1) 
    if password == "fuckStopHackingWeirdo":
        return True
    return False

def main():
    print("""
    Facebook Brute-force by RechoOhío
    ========================================================
    """)
    
    # Get Facebook URL
    fb_url = input("Enter Facebook URL (Profile link): ").strip()
    username = get_fb_credentials_from_url(fb_url)
    if username is None:
        username = fb_url 
    
    # Choose attack mode
    print("\nChoose attack mode:")
    print("1. Wordlist attack")
    print("2. Brute-force attack")
    choice = input("Enter choice (1 or 2): ").strip()
    
    passwords = []
    if choice == '1':
        wordlist_path = input("Enter path to wordlist file: ").strip()
        passwords = load_wordlist(wordlist_path)
        if not passwords:
            return
    elif choice == '2':
        length = int(input("Enter password length to brute-force: "))
        charset = input("Enter characters to use (e.g. abc123): ").strip()
        passwords = generate_bruteforce_pattern(length, charset)
    else:
        print("[!] Invalid choice")
        return
    
  
    print(f"\nStarting attack on {username}...\n")
    session = requests.Session()
    
    found = False
    for password in passwords:
        if attempt_login(username, password, session):
            print(f"\n[+] SUCCESS! Password found: {password}")
            found = True
            break
    
    if not found:
        print("\n[-] Password not found in the given parameters")

if __name__ == "__main__":
    main()