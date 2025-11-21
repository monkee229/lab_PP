import re
import requests

# RFC5322 email simplified
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@'
    r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
    r'[a-zA-Z]{2,}$'
)


def clean_email(email):
    return email.strip()


def normalize_email(email):
    cleaned = clean_email(email)
    if '@' not in cleaned:
        return cleaned
    username, domain = cleaned.split('@', 1)
    return f"{username}@{domain.lower()}"


def extract_domain(email):
    cleaned = clean_email(email)
    if '@' not in cleaned:
        return None
    return cleaned.split('@')[1]


def extract_username(email):
    cleaned = clean_email(email)
    if '@' not in cleaned:
        return None
    return cleaned.split('@')[0]


def is_valid_email(email):
    cleaned = clean_email(email)
    return bool(EMAIL_REGEX.match(cleaned))


def find_emails_in_text(text):
    pattern = re.compile(
        r'[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@'
        r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
        r'[a-zA-Z]{2,}'
    )
    return re.findall(pattern, text)


def unique_emails(emails):
    seen = set()
    result = []
    for e in emails:
        if e not in seen:
            seen.add(e)
            result.append(e)
    return result


def count_emails_in_text(text):
    found = find_emails_in_text(text)
    valid = [e for e in found if is_valid_email(e)]
    return {
        "total_found": len(found),
        "valid": len(valid),
        "invalid": len(found) - len(valid)
    }


def main():
    mode = input("input/url/file: ").strip().lower()

    if mode == 'input':
        email = input("Enter email: ").strip()
        normalized = normalize_email(email)
        if is_valid_email(normalized):
            print(f"Valid email: {normalized}")
            print(f"Username: {extract_username(normalized)}")
            print(f"Domain: {extract_domain(normalized)}")
        else:
            print("Invalid email syntax.")

    elif mode == 'url':
        url = input("Enter URL: ").strip()
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            emails = find_emails_in_text(response.text)
            valid = [e for e in emails if is_valid_email(e)]
            unique = unique_emails(valid)

            stats = count_emails_in_text(response.text)

            print(f"Found valid unique emails: {unique}")
            print(f"Stats: {stats}")

        except requests.RequestException as e:
            print(f"Error fetching: {e}")

    elif mode == 'file':
        file_path = input("Enter file path: ").strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            emails = find_emails_in_text(content)
            valid = [e for e in emails if is_valid_email(e)]
            unique = unique_emails(valid)

            stats = count_emails_in_text(content)

            print(f"Found valid unique emails: {unique}")
            print(f"Stats: {stats}")

        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error reading file: {e}")

    else:
        print("Invalid mode.")


if __name__ == "__main__":
    main()
