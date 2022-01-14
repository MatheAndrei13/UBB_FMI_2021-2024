"""
Bonus Project: Project 1
Author: Máthé Andrei
Group: 914 IE


Problem:
Write a program that reads a non-zero natural number n as input from a file and write in an output file:
1. the number of partitions on a set A of n elements
2. the partitions on a set A of n elements and their corresponding equivalence relations (for n ≤ 8)


Solution:
For the first requirement, in order to get the number of partitions I compute the bell number of a set
of n elements as a sum of Stirling numbers of the second kind. For the second requirement, I generate
all possible partition representations (restricted growth strings) and create all the partitions
using the representations. The equivalence relations are generated by creating all possible groups of
two elements belonging to the same class.
"""

import math


# ################################### NON-UI ################################### #
def stirling_partition_number(n, k):
    """
    The function return the number of ways to partition a set of n element into k groups. For that it uses
    Stirling numbers of the second kind.

    :param n: the number of elements in a set
    :param k: the number of groups
    :return: number of partitions with k classes of a set of n elements
    """
    if n == k:
        return 1
    if n == 0 or k == 0:
        return 0

    sigma_sum = 0
    for i in range(k + 1):
        sigma_sum += (1 - 2 * (i % 2)) * math.comb(k, i) * (k - i) ** n
    return int((1.0 / math.factorial(k)) * sigma_sum)


def bell_number(n):
    """
    The function returns the number of partitions on a set A of n elements using the Bell number.

    :param n: the number of elements in a set
    :return: total number of partitions
    """
    number_of_partitions = 0
    for k in range(n + 1):
        number_of_partitions += stirling_partition_number(n, k)
    return number_of_partitions


def create_partition(partition_rep, n):
    """
    The function creates a partition using the a partition representation and returns it.

    :param partition_rep: partition representation (a list)
    :param n: the number of elements in a set
    :return: partition
    """
    partition = []
    for element in range(n):
        class_index = partition_rep[element]
        if len(partition) - 1 < class_index:
            partition.append(list())
        partition[class_index].append(element)
    return partition


def add_partition(partitions, partition):
    """
    The function appends a partitions to the list of partitions.

    :param partitions: list of partitions
    :param partition: a partition of a set
    :return:
    """
    partitions.append(partition)


def generate_partition_representations(partitions, partition_rep, n, k, max_class_index):
    """
    The function generates all the possible partition representations using a backtracking algorithm and
    adds the corresponding partitions to the list of partitions.

    :param partitions: list of partitions
    :param partition_rep: partition representation (list)
    :param n: the number of elements in the set
    :param k: current element
    :param max_class_index: maximum element from the partition representation
    :return:
    """
    if k == n:
        partition = create_partition(partition_rep, n)
        add_partition(partitions, partition)
        return
    for i in range(max_class_index + 2):
        partition_rep[k] = i
        generate_partition_representations(partitions, partition_rep, n, k + 1, max(i, max_class_index))


def generate_partitions(partitions, n):
    """
    The function generates all the partitions of a set of n elements.

    :param partitions: list of partitions
    :param n: the number of element in the set
    :return:
    """
    partition_rep = [None] * n
    k = 0
    max_class_index = -1
    generate_partition_representations(partitions, partition_rep, n, k, max_class_index)


# ##################################### UI ##################################### #
def get_digit_subscript(digit):
    """
    The function returns the digit as a subscript.

    :param digit: digit (integer)
    :return: a unicode character representing the subscript digit
    """
    return chr(int('208' + str(digit), base=16))


def print_number_of_partitions(fout, n):
    """
    The function writes to the output file the number of partitions of a a set of n elements.

    :param fout: object of the output file
    :param n: number of elements in the set
    :return:
    """
    fout.write('The number of partitions on a set A of ' + str(n) + ' elements is ' + str(bell_number(n)) + '\n')


def class_to_str(class_partition):
    """
    The function converts a partition's class to a string and returns it.

    :param class_partition: a class of a partition
    :return: string representing a class of a partition
    """
    class_partition_str = ['a' + get_digit_subscript(element + 1) for element in class_partition]
    return '{' + ', '.join(class_partition_str) + '}'


def partition_to_str(partition):
    """
    The function converts a partition to a string and returns it.

    :param partition: a partition of a set
    :return: string representing a partition of a set
    """
    partition_str = [class_to_str(class_partition) for class_partition in partition]
    return '{' + ', '.join(partition_str) + '}'


def equivalence_relations_to_str(partition):
    """
    The function returns a string representing the equivalence relations of a partition of a set.

    :param partition: a partition of a set
    :return: string representing the equivalence relations of a partition of a set
    """
    equivalence_relations_str = []
    for class_partition in partition:
        for i in class_partition:
            for j in class_partition[class_partition.index(i) + 1:]:
                equivalence_relations_str.append('(a' + get_digit_subscript(i + 1) + ', a' + get_digit_subscript(j + 1) + ')')
                equivalence_relations_str.append('(a' + get_digit_subscript(j + 1) + ', a' + get_digit_subscript(i + 1) + ')')
    return '{' + ', '.join(equivalence_relations_str) + '}'


def print_partitions_relations(fout, partitions, n):
    """
    The function writes to the output file all the partitions of a set of n elements and their
    corresponding equivalence relations.

    :param fout: object of the output file
    :param partitions: list of partitions
    :param n: the number of elements in a set
    :return:
    """
    fout.write('Using the notation ∆A = {')
    for i in range(n - 1):
        fout.write('(a' + get_digit_subscript(i + 1) + ', a' + get_digit_subscript(i + 1) + '),')
    fout.write('(a' + get_digit_subscript(n) + ', a' + get_digit_subscript(n) + ')')
    fout.write('}, the partitions on a set A = {')
    for i in range(n - 1):
        fout.write('a' + get_digit_subscript(i + 1) + ', ')
    fout.write('a' + get_digit_subscript(n))
    fout.write('} and their corresponding equivalence relations are:\n')

    for partition in partitions:
        fout.write(partition_to_str(partition))
        if len(partition) == 1:
            fout.write(' ⇝ A × A\n')
        elif len(partition) == n:
            fout.write(' ⇝ ∆A\n')
        else:
            fout.write(' ⇝ ∆A∪' + equivalence_relations_to_str(partition) + '\n')


# #################################### MAIN #################################### #
def main():
    fin = open('input.txt', 'r')
    fout = open('output.txt', 'w')

    n = fin.read()
    if not n.isnumeric() or int(n) == 0:
        fout.write('Invalid input!')
        exit()

    partitions = []
    n = int(n)

    print_number_of_partitions(fout, n)

    if n <= 8:
        fout.write('\n')
        generate_partitions(partitions, n)
        print_partitions_relations(fout, partitions, n)


if __name__ == '__main__':
    main()