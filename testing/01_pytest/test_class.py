class TestClass:
    def test_one(self):
        x = "one"
        assert 'o' in x

    def test_two(self):
        x = "hello"
        assert not 'world' in x
        assert hasattr(self, "test_two")
