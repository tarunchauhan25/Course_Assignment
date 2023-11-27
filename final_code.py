import pandas as pd
from sympy import Matrix, Eq, linsolve 
import numpy as np
import itertools
import copy
class Faculty:
    def __init__(self,name,id,maxload,prefl):
        self.name = name
        self.id = id
        self.maxload = maxload
        self.pref = []
        for i in prefl:
            self.pref.append([int(i),0])
class Course:
    def __init__(self,name,id):
        self.name = name
        self.id = id   
# Read the CSV data into a DataFrame
data = pd.read_csv('input.csv')
# Create a dictionary to store the faculty data
def create_dict():
    faculty = []
    # Iterate through each row in the DataFrame
    for index, row in data.iterrows():
        faculty_name = row['Faculty_Name']
        faculty_num = row['Faculty_Num']
        max_load = row['Max_Load']
        course_pref = row['Course_Pref']
        # Convert the course preference string into a list
        course_pref_list = course_pref.strip()[1:-1].split(' ')
        # Check for empty strings and skip them when converting to integers
        try:
            course_pref_list = [int(course) for course in course_pref_list]
        except ValueError:
            pass  # Skip empty strings
        # Add the faculty data to the dictionary
        f = Faculty(faculty_name,faculty_num,max_load, course_pref_list)
        faculty.append(f)
    return faculty

def all_positive(list1):
  for num in list1[0:len(list1)-2]:
    if (int(num) < 0 or int(num) > 2):
      return False
  return True
def find_all_possible_vectors(null_space):
    # Create an empty list to store the generated vectors
    generated_vectors = []
    generated_vector_rs = []
    final_ans = []
    # Iterate through all possible combinations of coefficients
    for coefficients in itertools.product([1,2,0], repeat=min(len(null_space),10)):
        # Generate a linear combination using the current coefficients
        generated_vector = np.zeros_like(null_space[0])
        generated_vector_r = np.zeros_like(null_space[0])
        for i, coefficient in enumerate(coefficients):
            if i != len(coefficients) - 1:
                generated_vector += coefficient * null_space[-i-2]
                generated_vector_r += coefficient * null_space[i]
        generated_vector -= null_space[-1]
        generated_vector_r -= null_space[-1]
        # Check if the generated vector is already in the list
        if generated_vector.tolist() not in generated_vectors:
          if(all_positive(generated_vector.tolist())):
              generated_vectors.append(generated_vector.tolist())
        if generated_vector_r.tolist() not in generated_vector_rs:
          if(all_positive(generated_vector_r.tolist())):
              generated_vector_rs.append(generated_vector_r.tolist())
    return generated_vectors,generated_vector_rs
def find_all_possible_vectors_r(null_space):
    # Create an empty list to store the generated vectors
    generated_vectors = []
    # Iterate through all possible combinations of coefficients
    for coefficients in itertools.product([1,2,0], repeat=min(len(null_space),10)):
        # Generate a linear combination using the current coefficients
        generated_vector = np.zeros_like(null_space[0])
        for i, coefficient in enumerate(coefficients):
            if i != len(coefficients) - 1:
                generated_vector += coefficient * null_space[i]
        generated_vector -= null_space[-1]
        # Check if the generated vector is already in the list
        if generated_vector.tolist() not in generated_vectors:
          if(all_positive(generated_vector.tolist())):
              generated_vectors.append(generated_vector.tolist())
    return generated_vectors
# Example usage


def convert(matrix):
    n = len(matrix)
    totalCourses = 0
    columns = 0
    for i in range(1, n+1):
        totalCourses = max(totalCourses, max(matrix[i][1]))
        columns += len(matrix[i][1])
    eq_matrix = [[0 for i in range(columns + 1)] for j in range(n + totalCourses)]
    weight = 0
    for i in range(1, n+1):
        for j in range(len(matrix[i][1])):
            eq_matrix[i-1][weight] = 1
            eq_matrix[n + matrix[i][1][j] - 1][weight] = 1
            weight += 1
        eq_matrix[i-1][-1] = matrix[i][0]

    for i in range(n, len(eq_matrix)):
        eq_matrix[i][-1] = 2 
    # extending the matrix
    for i in range(n):
        for j in range(n + totalCourses):
            matrix[i][j].insert(0, 0)
    # putting right values
    extra_index = n-1
    for i in range(n):
        matrix[i][extra_index] = 1
        extra_index -= 1

    # print("matrix")
    # print(eq_matrix)
    # print("end")
    return eq_matrix

# convert({1:(3, [2,3]), 2:(3, [1,4]), 3: (2, [2,4])})
# temp = create_dict()
# temp2, const = convert(temp)
# M = Matrix(temp2)
# C = Matrix()
# print(M.nullspace())

# system = Eq(temp2 * temp2.nullspace()[0], const)
# sol = linsolve(system)
# print(sol)  

#temp = create_dict()
#temp2 = convert(temp)
def create_matrix(faculties):
    # faculties is a list of faculties
    #counting
    n = len(faculties)
    columns = 0
    maxCourses = 0
    for i in range(n):
        columns += len(faculties[i].pref)
        max_Cid = 0
        for j in range(len(faculties[i].pref)):
            max_Cid = max(max_Cid, faculties[i].pref[j][0])
        maxCourses = max(maxCourses, max_Cid)
    # print(columns)
    # print(maxCourses)
    # initializing the matrix
    matrix = [[0 for i in range(columns)] for j in range(n + maxCourses)]

    # filling the matrix
    index = columns - 1
    for i in range(maxCourses):
        for j in range(n):
            if i < len(faculties[j].pref):
                matrix[j][index] = 1
                matrix[n + faculties[j].pref[i][0] - 1][index] = 1
                index -= 1
    for i in range(n):
        matrix[i].append(faculties[i].maxload)
    for i in range(n, n + maxCourses):
        matrix[i].append(2)

    # print("original")
    # for i in matrix:
    #     print(i)
    # print("new")
    
    # extending the matrix
    for i in range(n):
        for j in range(n + maxCourses):
            matrix[j].insert(0, 0)
    
    # putting right values
    extra_index = n-1
    for i in range(n):
        matrix[i][extra_index] = 1
        extra_index -= 1

    # print("matrix")
    # for i in range(len(matrix)):
    #     print(matrix[i])
    # print(len(matrix[0]))
    # print("end")

    return matrix 


# matrix2 = [Faculty(3,[[2, 0], [3, 0], [4, 0]]), 
#           Faculty(3, [[1, 0], [2, 0], [4, 0]]),
#           Faculty(2, [[2, 0], [3, 0],[4,0]]),
#           ]
# matrix = [Faculty(3, [[1, 0], [2, 0], [3, 0], [4, 0]]), 
#           Faculty(3, [[3, 0], [4, 0], [5, 0], [6, 0]]),
#           Faculty(3, [[5, 0], [6, 0], [7, 0], [8, 0]]),
#           Faculty(3, [[7, 0], [8, 0], [9, 0], [1, 0]]),
#           Faculty(3, [[9, 0], [1, 0], [2, 0], [3, 0]]),
#           Faculty(3, [[2, 0], [3, 0], [4, 0], [5, 0]]),
#           ]
matrix3 = create_dict()
# for i in matrix3:
#     print(i.name)
temp2 = create_matrix(matrix3)
# for i in range(len(temp2)):
#     print(temp2[i])
# print(temp2)
M = Matrix(temp2)
null = M.nullspace()
null_list = []
for i in range(len(null)):
    null_list.append(null[i].tolist())
null_list_final = []

temppp = []
for i in range(len(null_list)):
    for j in range(len(null_list[0])):
        temppp.append(null_list[i][j][0])
    null_list_final.append(temppp)
    temppp = []
# print(null_list_final)
    
num_vars = len(null_list)
final_ans = []
temp_ans = []
coeff = [2 for i in range(num_vars)]
for i in range(min(1000000, pow(3, num_vars))):
    for j in range(len(null_list[0])):
        tempSum = 0
        for k in range(num_vars-1):
            tempSum += null_list[k][j][0]
        tempSum -= null_list[-1][j][0]
        if tempSum < 0:
            temp_ans = []
            break 
        temp_ans.append(tempSum)
    final_ans.append(temp_ans)
    coeff[-2] -= 1
    if coeff[-2] == -1:
        coeff[-2] = 2
        coeff[-3] -= 1
        if coeff[-3] == -1:
            break
#     print(coeff)
# print(null_list)
# print(num_vars)
# print(final_ans)

null_space = np.array(null_list_final)
generated_vectors,generated_vector_rs = find_all_possible_vectors(null_space)
# print(len(null_space))
print("ans")
count=0
# print(len(generated_vectors[0]))
# print(len(generated_vectors[1]))
final_sol = []
for sol in generated_vectors:
    f_a = []
    ca = 0
    print("Possible Solution Number "+str(count+1))
    for i,s in enumerate(reversed(sol)):
        if(i!=0 and i<=len(matrix3)*len(matrix3[0].pref) and s!=0):
            print(str(matrix3[(i-1)%(len(matrix3))].name + " is assigned "+str(float(s/2))+" course "+str(matrix3[(i-1)%(len(matrix3))].pref[(i-1)//len(matrix3)][0])))  
    print("--------------------End-Case----------------------")
    final_sol.append(f_a)
    count = count + 1
    if(count>10):
        break
for sol in generated_vector_rs:
    f_a = []
    ca = 0
    print("Possible Solution Number "+str(count+1))
    for i,s in enumerate(reversed(sol)):
        if(i!=0 and i<=len(matrix3)*len(matrix3[0].pref) and s!=0):
            print(str(matrix3[(i-1)%(len(matrix3))].name + " is assigned "+str(float(s/2))+" course "+str(matrix3[(i-1)%(len(matrix3))].pref[(i-1)//len(matrix3)][0])))  
    print("--------------------End-Case----------------------")
    final_sol.append(f_a)
    count = count + 1
    if(count>10):
        break
# if final_sol:
#     for j in final_sol:
#         for f in j:
#             print(f.pref)
#         print()