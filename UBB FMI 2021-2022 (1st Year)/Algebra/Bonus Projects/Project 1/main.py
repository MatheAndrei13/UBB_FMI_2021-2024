import math


# ################################### NON-UI ################################### #
def stirling_partition_number(n, k):
    if n == k:
        return 1
    if n == 0 or k == 0:
        return 0

    sigma_sum = 0
    for i in range(k + 1):
        sigma_sum += (1 - 2 * (i % 2)) * math.comb(k, i) * (k - i) ** n
    return int((1.0 / math.factorial(k)) * sigma_sum)


def bell_number(n):
    number_of_partitions = 0
    for k in range(n + 1):
        number_of_partitions += stirling_partition_number(n, k)
    return number_of_partitions


def create_partition(partition_rep):
    n = len(partition_rep)
    partition = []
    for i in range(n):
        if len(partition) < partition_rep[i]:
            partition.append(list())
        partition[partition_rep[i]].append(i)
    return partition


def add_partition(partitions, partition):
    partitions.appent(partition)


def generate_partition_representations(partitions, partition_rep, n, k, max_class_number):
    if k == n:
        partition = create_partition(partition_rep)
        add_partition(partitions, partition)
        return
    for i in range(max_class_number + 2):
        partition_rep[k] = i
        generate_partition_representations(partitions, partition_rep, n, k + 1, i)


def generate_partitions(partitions, n):
    partition_rep = [] * n
    k = 0
    max_class_number = -1
    generate_partition_representations(partitions, partition_rep, n, k, max_class_number)


# ##################################### UI ##################################### #
def get_digit_subscript(digit):
    return chr(int('208' + str(digit), base=16))


def print_number_of_partitions(n):
    print('The number of partitions: ' + str(bell_number(n)))


def main():
    print('Enter a non-zero natural number n.')
    while True:
        n = input('n = ')
        if n.isnumeric() and int(n) != 0:
            break
        else:
            print('Invalid number! Try again!')

    n = int(n)
    partitions = []

    print_number_of_partitions(n)
    generate_partitions(partitions, n)


if __name__ == '__main__':
    main()
