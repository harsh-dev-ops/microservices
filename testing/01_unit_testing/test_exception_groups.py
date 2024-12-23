import pytest


def f():
    raise ExceptionGroup(
        'Group Message',
        [
            RuntimeError(),
        ]
    )


def test_exception_groups():
    with pytest.raises(ExceptionGroup):
        f()
