class TestClassDemo:
    x = 0

    def test_one(self):
        self.x = 1
        assert self.x == 1

    def test_two(self):
        assert self.x != 1
