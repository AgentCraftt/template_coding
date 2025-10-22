import numpy as np


def create_symmetric_matrix(vector):
    """
    Creates a symmetric dense matrix from a given one-dimensional vector.

    The length of the vector should be n*(n+1)/2 for some positive integer n,
    indicating the number of unique elements in an n x n symmetric matrix.

    Parameters:
        vector (list or numpy array): The input vector containing the elements.

    Returns:
        numpy array: The resulting symmetric matrix.

    Raises:
        ValueError: If the length of vector does not form a valid symmetric matrix.
    """
    # Calculate the size of the symmetric matrix
    n_elements = len(vector)
    n = int((np.sqrt(1 + 8 * n_elements) - 1) / 2)

    if n * (n + 1) // 2 != n_elements:
        raise ValueError(
            "The length of the vector does not form a valid symmetric matrix."
        )

    # Initialize an empty matrix
    matrix = np.zeros((n, n))

    # Fill the upper triangular part of the matrix
    k = 0
    for i in range(n):
        for j in range(i, n):
            matrix[i, j] = vector[k]
            matrix[j, i] = vector[k]
            k += 1

    return matrix
