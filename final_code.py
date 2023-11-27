import pandas as pd
from sympy import Matrix, Eq, linsolve
import numpy as np
import itertools
import copy

print("Programme started")
# print("Programme is running...............")
class Faculty:
    def __init__(self, name, id, maxload, prefl):
        self.name = name
        self.id = id
        self.maxload = maxload
        self.pref = []
        for i in prefl:
            self.pref.append([int(i), 0])


class Course:
    def __init__(self, name, id):
        self.name = name
        self.id = id


# Read the CSV data into a DataFrame
data = pd.read_csv("input.csv")


# Create a dictionary to store the faculty data
def create_dict():
    faculty = []
    # Iterate through each row in the DataFrame
    print("Taking input from input.csv file.......")
    print("Creating Matrix.......")
    print("Finding all possible vectors......")
    for index, row in data.iterrows():
        faculty_name = row["Faculty_Name"]
        faculty_num = row["Faculty_Num"]
        max_load = row["Max_Load"]
        course_pref = row["Course_Pref"]
        # Convert the course preference string into a list
        course_pref_list = course_pref.strip()[1:-1].split(" ")
        # Check for empty strings and skip them when converting to integers
        try:
            course_pref_list = [int(course) for course in course_pref_list]
        except ValueError:
            pass  # Skip empty strings
        # Add the faculty data to the dictionary
        f = Faculty(faculty_name, faculty_num, max_load, course_pref_list)
        faculty.append(f)
    return faculty


def all_positive(list1):
    for num in list1[0 : len(list1) - 2]:
        if int(num) < 0 or int(num) > 2:
            return False
    return True

print("Creating Null Space.......")
def find_all_possible_vectors(null_space):
    # Create an empty list to store the generated vectors
    generated_vectors = []
    generated_vector_rs = []
    final_ans = []
    # Iterate through all possible combinations of coefficients
    print("Iterating through all possible combinations.......")
    t =  0
    for coefficients in itertools.product([1, 2 , 0], repeat=min(len(null_space), 10)):
        # Generate a linear combination using the current coefficients
        t = t +1
        if(t==pow(3,9)):
            print("33% Iterations Done...............")
        elif(t==2*pow(3,9)):
            print("66% Iterations Done.................")
        elif(t == pow(3,10)):
            print("Iterations Completed.........")
        generated_vector = np.zeros_like(null_space[0])
        generated_vector_r = np.zeros_like(null_space[0])
        for i, coefficient in enumerate(coefficients):
            if i != len(coefficients) - 1:
                generated_vector += coefficient * null_space[-i - 2]
                generated_vector_r += (
                    coefficient * null_space[(i + 10) % len(null_space)]
                )
        generated_vector -= null_space[-1]
        generated_vector_r -= null_space[-1]
        # Check if the generated vector is already in the list
        if generated_vector.tolist() not in generated_vectors:
            if all_positive(generated_vector.tolist()):
                generated_vectors.append(generated_vector.tolist())
        if generated_vector_r.tolist() not in generated_vector_rs:
            if all_positive(generated_vector_r.tolist()):
                generated_vector_rs.append(generated_vector_r.tolist())
    return generated_vectors, generated_vector_rs
def convert(matrix):
    n = len(matrix)
    totalCourses = 0
    columns = 0
    for i in range(1, n + 1):
        totalCourses = max(totalCourses, max(matrix[i][1]))
        columns += len(matrix[i][1])
    eq_matrix = [[0 for i in range(columns + 1)] for j in range(n + totalCourses)]
    weight = 0
    for i in range(1, n + 1):
        for j in range(len(matrix[i][1])):
            eq_matrix[i - 1][weight] = 1
            eq_matrix[n + matrix[i][1][j] - 1][weight] = 1
            weight += 1
        eq_matrix[i - 1][-1] = matrix[i][0]

    for i in range(n, len(eq_matrix)):
        eq_matrix[i][-1] = 2
    # extending the matrix
    for i in range(n):
        for j in range(n + totalCourses):
            matrix[i][j].insert(0, 0)
    # putting right values
    extra_index = n - 1
    for i in range(n):
        matrix[i][extra_index] = 1
        extra_index -= 1

    return eq_matrix

def create_matrix(faculties):
    # faculties is a list of faculties
    # counting
    n = len(faculties)
    columns = 0
    maxCourses = 0
    for i in range(n):
        columns += len(faculties[i].pref)
        max_Cid = 0
        for j in range(len(faculties[i].pref)):
            max_Cid = max(max_Cid, faculties[i].pref[j][0])
        maxCourses = max(maxCourses, max_Cid)

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

    for i in range(n):
        for j in range(n + maxCourses):
            matrix[j].insert(0, 0)

    # putting right values
    extra_index = n - 1
    for i in range(n):
        matrix[i][extra_index] = 1
        extra_index -= 1

    return matrix

matrix3 = create_dict()
temp2 = create_matrix(matrix3)
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

num_vars = len(null_list)
final_ans = []
temp_ans = []
coeff = [2 for i in range(num_vars)]
for i in range(min(1000000, pow(3, num_vars))):
    for j in range(len(null_list[0])):
        tempSum = 0
        for k in range(num_vars - 1):
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

null_space = np.array(null_list_final)
generated_vectors, generated_vector_rs = find_all_possible_vectors(null_space)
# print("ans")
count = 0
print("Copying the solutions to output.txt file")
# print(len(generated_vectors))
# print(len(generated_vector_rs))
final_sol = []
file = open("output.txt", "w")
final_assignment = {}
all_final_assignment = {}
for sol in generated_vectors:
    f_a = []
    fac_assignment = {}
    ca = 0
    for i, s in enumerate(reversed(sol)):
        if i != 0 and i <= len(matrix3) * len(matrix3[0].pref) and s != 0:
            if matrix3[(i - 1) % (len(matrix3))].name in final_assignment:
                final_assignment[matrix3[(i - 1) % (len(matrix3))].name].append(
                    [
                        matrix3[(i - 1) % (len(matrix3))].pref[(i - 1) // len(matrix3)][
                            0
                        ],
                        s / 2,
                    ]
                )
            else:
                final_assignment[matrix3[(i - 1) % (len(matrix3))].name] = [
                    [
                        matrix3[(i - 1) % (len(matrix3))].pref[(i - 1) // len(matrix3)][
                            0
                        ],
                        s / 2,
                    ]
                ]
    all_final_assignment[count + 1] = final_assignment
    final_assignment = {}
    final_sol.append(f_a)
    count = count + 1
    if count > 10:
        break
for sol in generated_vector_rs:
    f_a = []
    ca = 0
    for i, s in enumerate(reversed(sol)):
        if i != 0 and i <= len(matrix3) * len(matrix3[0].pref) and s != 0:
            if matrix3[(i - 1) % (len(matrix3))].name in final_assignment:
                final_assignment[matrix3[(i - 1) % (len(matrix3))].name].append(
                    [
                        matrix3[(i - 1) % (len(matrix3))].pref[(i - 1) // len(matrix3)][
                            0
                        ],
                        s / 2,
                    ]
                )
            else:
                final_assignment[matrix3[(i - 1) % (len(matrix3))].name] = [
                    [
                        matrix3[(i - 1) % (len(matrix3))].pref[(i - 1) // len(matrix3)][
                            0
                        ],
                        s / 2,
                    ]
                ]
    final_assignment = {}
    final_sol.append(f_a)
    count = count + 1
    if count > 10:
        break

def makeStringForLoad(num):
    if num == 0.5:
        return "half"
    elif num == 1:
        return "full"


for case in all_final_assignment.keys():
    # print("Possible Solution Number: ", case)
    file.write("Possible Solution Number: " + str(case))
    file.write("\n")
    for faculty in all_final_assignment[case]:
        # print(str(faculty) + " is assigned ", end="")
        file.write(str(str(faculty) + " is assigned "))
        for courses in range(len(all_final_assignment[case][faculty])):
            if courses != 0:
                # print("and ", end="")
                file.write("and ")
            # print(
            #     makeStringForLoad(all_final_assignment[case][faculty][courses][1])
            #     + " course "
            #     + str(all_final_assignment[case][faculty][courses][0])
            #     + " ",
            #     end="",
            # )
            file.write(
                str(
                    makeStringForLoad(all_final_assignment[case][faculty][courses][1])
                    + " course "
                    + str(all_final_assignment[case][faculty][courses][0])
                    + " "
                )
            )
        # print(".")
        file.write("\n")
    # print("------------------End-Case------------------")
    file.write("------------------End-Case------------------")
    file.write("\n")
print("Completed, check output.txt")
file.close()
