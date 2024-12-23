import pytest


def f():
    raise SystemExit(1)


def test_sysexit():
    with pytest.raises(SystemExit):
        f()
