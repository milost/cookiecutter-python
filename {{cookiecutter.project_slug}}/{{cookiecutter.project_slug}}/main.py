def say_hello(name: str) -> str:
    """
    Returns a simple string file
    :param name: The name of the person that should be greeted.
    :type name: str
    :return: a simple string
    :rtype: str
    """
    return f'Hello from {name}'


def inc(x: int) -> int:
    return x + 1


def main():
    """
    The Main module which serves as a preliminary entrypoint
    """
    print(inc(3))
    print(say_hello('python cookiecutter template!'))


if __name__ == '__main__':
    main()
