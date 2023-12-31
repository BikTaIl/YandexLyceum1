class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


def check_password(password):
    bad = 'йцукенгшщзхъ фывапролджэё ячсмитьбю qwertyuiop asdfghjkl zxcvbnm'
    if len(password) <= 8:
        raise LengthError
    elif password.lower() == password or password.upper() == password:
        raise LetterError
    elif len(list(filter(lambda x: x.isdigit(), list(password)))) == 0:
        raise DigitError
    for i in range(len(password) - 2):
        if password[i:i + 3].lower() in bad:
            raise SequenceError
    return 'ok'