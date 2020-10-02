from {{cookiecutter.project_slug}}.misc import append_phrase


def test_append_phrase():
    """
    A simple dummy test
    """
    # Setup
    origin = 'Hello World'
    expected = 'Hello World...with fries?'

    # Execute
    actual = append_phrase(origin)

    # Verify
    assert actual == expected
