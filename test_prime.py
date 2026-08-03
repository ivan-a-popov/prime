from prime import check, find


def reference_is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))


def test_edge_cases():
    assert check(1) is False
    assert check(2) is True
    assert check(3) is True


def test_non_positive_numbers_are_not_prime():
    for n in (0, -1, -2, -7, -100):
        assert check(n) is False


def test_even_numbers():
    assert check(4) is False
    assert check(100) is False


def test_known_primes_and_composites():
    assert check(7919) is True  # 1000th prime
    assert check(7920) is False
    assert check(9) is False  # odd composite square
    assert check(25) is False


def test_matches_reference_implementation():
    for n in range(0, 2000):
        assert check(n) == reference_is_prime(n)


def test_find_excludes_bounds():
    assert find(1, 10) == [2, 3, 5, 7]
    assert find(2, 7) == [3, 5]  # 2 and 7 are prime but excluded as bounds


def test_find_empty_range():
    assert find(1, 2) == []
    assert find(14, 16) == []  # 15 is composite


def test_find_known_interval():
    assert find(10, 20) == [11, 13, 17, 19]
