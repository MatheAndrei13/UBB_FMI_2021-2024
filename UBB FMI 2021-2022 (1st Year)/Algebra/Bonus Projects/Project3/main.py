"""
Bonus Project: Project 3
Author: Máthé Andrei
Group: 914 IE


Problem:
Write a program that reads a non-zero natural number n as input from a file and write in an output file:
1. the number of bases of the vector space Z^n_2 over Z_2
2. the vectors of each such basis (for n ≤ 4)


Solution:
For the first requirement, in order to get the number of bases I compute the following formula:
(q^n − 1)(q^n − q)(q^n − q^2)...(q^n − q^(k−1))
For the second requirement, I generate all possible arrangements of `n` vectors taken from the vector space
(where n is the dimension of the vector space), using Backtracking, and extract only the ones which have
linearly independent vectors.
"""

import copy


# ################################### NON-UI ################################### #
def matrix_det_z2(matrix):
    """
    The function returns the determinant of a square matrix with elements in Z_2.

    :param matrix: a square matrix with elements in Z_2
    :return: determinant of the square matrix
    """
    # the number of rows and column are equal
    num_rows = len(matrix)
    num_columns = len(matrix)

    determinant_value = 1

    # iterating through the elements on the diagonal
    for row_index in range(num_rows - 1):
        # index will contain the index of the row on which the current pivot is found
        index = row_index
        while index < num_rows and matrix[index][row_index] == 0:
            index += 1

        # check if whole column is 0 => det = 0
        if index == num_rows:
            return 0

        # swap rows if necessary
        if index != row_index:
            determinant_value *= -1
            matrix[row_index], matrix[index] = matrix[index], matrix[row_index]

        # making all the elements below the pivot 0
        for r in range(row_index + 1, num_rows):
            if matrix[r][row_index] != 0:
                for c in range(row_index, num_columns):
                    matrix[r][c] ^= 1

    # the determinant will be the product of the element on the diagonal
    for r in range(num_rows):
        determinant_value *= matrix[r][r]

    return determinant_value


def generate_bases(n, basis, dimension, k):
    """
    The function generates all the bases using a Backtracking algorithm and prints them.

    :param n: the number of components of each vector (integer)
    :param basis: a list of vectors (empty at the beginning)
    :param dimension: the dimension of the vector space (integer)
    :param k: current index of the basis (integer)
    :return:
    """
    # termination condition - all the basis is full
    if k == dimension:
        # check if the vector are linearly independent
        if matrix_det_z2(copy.deepcopy(basis)) != 0:
            print_basis(basis)
        return
    # append and pop all the possible vectors of the vector space to the basis
    for i in range(2**n):
        # create a vector (a list) using the bits of a number between 0 and 2^n - 1 (all the possible vectors)
        temp_vector = [int(bit) for bit in f"{i:0{n}b}"]

        basis.append(temp_vector)
        generate_bases(n, basis, dimension, k + 1)
        basis.pop()


def get_num_of_bases(n):
    """
    The function returns the number of bases of the vector space by computing the following formula:
    (q^n − 1)(q^n − q)(q^n − q^2)...(q^n − q^(k−1))
    q = 2 (comes from Z_2)
    n = the number of components of each vector in the vector space
    k = n

    q_n - the number of vectors in the vector space
    q_i - the number of vectors that can't be chosen for the current vector in the basis

    :param n: the number of components of each vector
    :return: the number of bases of the vector space
    """
    num_of_bases = 1
    q_n = 2 ** n
    q_i = 1
    k = n
    for i in range(0, k):
        num_of_bases *= q_n - q_i
        q_i *= 2
    return num_of_bases


# ##################################### UI ##################################### #
def print_basis(basis):
    """
    The function writes a basis of the vector space in the output file.

    :param basis: a basis (a list of vectors)
    :return:
    """
    basis_vectors_str = ['(' + ', '.join([str(elem) for elem in vector]) + ')' for vector in basis]
    file_out.write('(' + ', '.join(basis_vectors_str) + ')\n')


def print_num_of_bases(n):
    """
    The function writes the number of bases of the vector space in the output file.

    :param n: the number of components of each vector of the vector space
    :return:
    """
    file_out.write(f"The number of bases of the vector space is {get_num_of_bases(n)}\n")


def main():
    n = file_in.read()
    if not n.isnumeric() or int(n) == 0:
        file_out.write('Invalid input! The input should be a non-zero natural number!')
        exit()

    n = int(n)
    dimension = n
    basis = []

    print_num_of_bases(n)
    if n <= 4:
        file_out.write('\nThe vectors of each such basis are:\n')
        generate_bases(n, basis, dimension, 0)


file_in = open('input.txt', 'r')
file_out = open('output.txt', 'w')

if __name__ == '__main__':
    main()

    file_in.close()
    file_out.close()
