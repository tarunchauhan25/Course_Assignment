import pandas as pd
from sympy import Matrix, Eq, linsolve 
import numpy as np
import itertools
import copy
def find_all_possible_vectors(null_space):
    # Create an empty list to store the generated vectors
    generated_vectors = []
    # Iterate through all possible combinations of coefficients
    for coefficients in itertools.product([1,2,0], repeat=min(len(null_space),2)):
        # Generate a linear combination using the current coefficients
        generated_vector = np.zeros_like(null_space[0])
        for i, coefficient in enumerate(coefficients):
            if i != len(coefficients) - 1:
                generated_vector += coefficient * null_space[-i-2]
        generated_vector -= null_space[-1]
        # Check if the generated vector is already in the list
        # if generated_vector.tolist() not in generated_vectors:
        #   if(all_positive(generated_vector.tolist())):
        #       generated_vectors.append(generated_vector.tolist())
    return generated_vectors
find_all_possible_vectors([
    [1,0,0],[0,1,0],[1,0,0],[0,0,-1]])
itertools.product([1,2,0], repeat=2)