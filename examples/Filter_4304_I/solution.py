def echo(input_string, flag=None):
    """
    Prints the input_string. If flag is '-n', it suppresses the trailing newline.
    """
    if flag == '-n':
        print(input_string, end='')
    else:
        print(input_string)