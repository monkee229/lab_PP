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

def test_find_multiple_emails_in_text():
    text = "Contacts: admin@mail.com, support@company.org, user123@domain.io"
    result = find_emails_in_text(text)
    assert "admin@mail.com" in result
    assert "support@company.org" in result
    assert "user123@domain.io" in result
    assert len(result) == 3


def test_is_valid_email_edge_cases():
    # максимально допустимые символы
    assert is_valid_email("a!#$%&'*+-/=?^_`{|}~z@domain.com")
    # нельзя начинать домен с '-'
    assert not is_valid_email("user@-domain.com")
    # нельзя заканчивать домен на '-'
    assert not is_valid_email("user@domain-.com")


def test_find_emails_ignores_false_matches():
    text = "Not emails: test@mail, @domain.com, mail@com, abc@@domain.com"
    result = find_emails_in_text(text)

    assert len(result) == 0
