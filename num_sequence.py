def num_sequence(n):
    """Выводит n первых элементов последовательности."""
    result = []
    num = 1
    while len(result) < n:
        result.extend([num] * num)
        num += 1
    return result[:n]


n = int(input("Введите число элементов последовательности n: "))
print(num_sequence(n))
