from {{cookiecutter.project_slug}}.main import inc


def test_inc():
    """
    A simple dummy test
    """
    # Setup
    origin = 3
    expected = 4

    # Execute
    actual = inc(origin)

    # Verify
    assert actual == expected
