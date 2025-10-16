from solution import echo

def test_echo_with_newline(capsys):
    echo("Hello, World!")
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"

def test_echo_without_newline(capsys):
    echo("Hello, World!", "-n")
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!"

def test_echo_empty_string_with_newline(capsys):
    echo("")
    captured = capsys.readouterr()
    assert captured.out == "\n"

def test_echo_empty_string_without_newline(capsys):
    echo("", "-n")
    captured = capsys.readouterr()
    assert captured.out == ""

def test_echo_multiword_string_with_newline(capsys):
    echo("This is a test")
    captured = capsys.readouterr()
    assert captured.out == "This is a test\n"

def test_echo_multiword_string_without_newline(capsys):
    echo("This is a test", "-n")
    captured = capsys.readouterr()
    assert captured.out == "This is a test"