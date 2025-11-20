import re
import requests

# RFC5322 email simplified
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@'
    r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
)

def clean_email(email):
    return email.strip()

def is_valid_email(email):
    cleaned = clean_email(email)
    return bool(EMAIL_REGEX.match(cleaned))

def find_emails_in_text(text):
    pattern = r'[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def main():
    mode = input("input/url/file: ").strip().lower()

    if mode == 'input':
        email = input("Enter email: ").strip()
        if is_valid_email(email):
            print(f"Valid email: {email}")
        else:
            print("Invalid email syntax.")

    elif mode == 'url':
        url = input("Enter URL: ").strip()
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            emails = find_emails_in_text(response.text)
            valid = [e for e in emails if is_valid_email(e)]
            print(f"Found {len(valid)} valid emails: {valid}")
        except requests.RequestException as e:
            print(f"Error fetching: {e}")

    elif mode == 'file':
        file_path = input("Enter file path: ").strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            emails = find_emails_in_text(content)
            valid = [e for e in emails if is_valid_email(e)]
            print(f"Found {len(valid)} valid emails: {valid}")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error reading file: {e}")

    else:
        print("Invalid mode.")

if __name__ == "__main__":
    main()
