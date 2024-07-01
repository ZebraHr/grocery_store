def num_sequence(n):
    result = []
    num = 1

    while len(result) < n:
        result.extend([num] * num)
        num += 1

    result = result[:n]

    return result


n = int(input("Введите число элементов последовательности n: "))
print(num_sequence(n))
