from email_validator import (
    clean_email, is_valid_email, find_emails_in_text
)

def test_clean_email():
    assert clean_email("   test@example.com   ") == "test@example.com"
    assert clean_email("\nuser@mail.ru\n") == "user@mail.ru"

def test_is_valid_email_valid_cases():
    assert is_valid_email("test@example.com")
    assert is_valid_email("user.name+tag@gmail.com")
    assert is_valid_email("my-mail_123@domain.co.uk")

def test_is_valid_email_invalid_cases():
    assert not is_valid_email("invalid@@mail.com")
    assert not is_valid_email("user@.com")
    assert not is_valid_email("usermail.com")
    assert not is_valid_email("user@domain")

def test_find_emails_in_text():
    text = "Here are emails: test@mail.com, wrong@, hello@world.org"
    result = find_emails_in_text(text)
    assert "test@mail.com" in result
    assert "hello@world.org" in result
