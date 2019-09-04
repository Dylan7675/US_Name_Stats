import re


def name_validation(val):
    if not re.match('^[a-zA-Z]+$', val):
        raise ValueError("Enter a Valid Name(Letters Only)")


if __name__ == "__main__":
    main()