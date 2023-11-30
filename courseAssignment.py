import pandas as pd
from sympy import Matrix, Eq, linsolve
import numpy as np
import itertools
import copy
import time
import os
from elec_Algorithm import *
from hd_CDC_algo import *
from hd_Elec_algo import *
dirname = os.path.dirname(__file__)
print(dirname)
dirname="/".join(dirname.split(sep='/')[:-1])
input_file = os.path.join(dirname, 'input.csv')
#Explain Potential Modifications
mode = 0 #Mode of Operation
#0 For Half Assignment Mode
#1 For Complete Assignment Mode
print("Programme started")

class Faculty:
    def __init__(self, name, id, maxload, prefl,ele_pref,hd_cdc_pref,hd_elec_pref):
        self.name = name
        self.id = id
        self.maxload = maxload
        self.pref = []
        self.ele_pref = []
        self.hd_cdc_pref = []
        self.hd_elec_pref = []
        for i in prefl:
            self.pref.append([int(i), 0])
        for i in ele_pref:    
            self.ele_pref.append([int(i),0])
        for i in hd_cdc_pref:    
            self.hd_cdc_pref.append([int(i),0])
        for i in hd_elec_pref:
            self.hd_elec_pref.append([int(i),0])
class Course:
    def __init__(self, name, id):
        self.name = name
        self.id = id
course_order = []
count_3load = 0
# Read the CSV data into a DataFrame
data = pd.read_csv(input_file)
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
        elec_pref = row["Elec_Pref"]
        hdcdc_pref = row["Hd_CDC_Pref"]
        hdelec_pref = row["Hd_Elec_Pref"]
        # Convert the course preference string into a list
        course_pref_list = course_pref.strip()[1:-1].split(" ")
        elec_pref_list = elec_pref.strip()[1:-1].split(" ")
        hdcdc_pref_list = hdcdc_pref.strip()[1:-1].split(" ")
        hdelec_pref_list = hdelec_pref.strip()[1:-1].split(" ")
        # Check for empty strings and skip them when converting to integers
        try:
            course_pref_list = [int(course) for course in course_pref_list]
            elec_pref_list = [int(course) for course in elec_pref_list]
            hdcdc_pref_list = [int(course) for course in hdcdc_pref_list]
            hdelec_pref_list = [int(course) for course in hdelec_pref_list]
        except ValueError:
            pass  # Skip empty strings
        # Add the faculty data to the dictionary
        f = Faculty(faculty_name, faculty_num, max_load, course_pref_list,elec_pref_list,hdcdc_pref_list,hdelec_pref_list)
        faculty.append(f)
    return faculty

def get_index_of_first_occurrence_of_all_unique_elements(list1,null_space_list):
  unique_elements = set(list1)
  index_of_first_occurrence = []
  for element in unique_elements:
    index = list1.index(element)
    for j in null_space_list:
            nl = list(reversed(j))
            if(nl[index+1]==1):
                index_of_first_occurrence.append(index)
                break
  return index_of_first_occurrence
def all_positive(list1,pref_3):
    count = 0
    for num in list1[0:len(list1) - 1]:
        if(int(num)<0):
            return False
        elif(count in pref_3):
            if(int(num)>3):
                return False
        elif(int(num)>2):
            return False
        count=count+1
    return True

print("Creating Null Space.......")
def find_all_possible_vectors(null_space,fac3load):
    generated_vector_rs_3 = []
    if(len(null_space)>1):
        # Create an empty list to store the generated vectors
        # Iterate through all possible combinations of coefficients
        print("Iterating through all possible combinations.......")
        t =  0
        for coefficients in itertools.product([2,1,0] if mode else [1,2,0], repeat=min(len(null_space), 10,len(course_order))):
            # Generate a linear combination using the current coefficients
            t = t +1
            if(t==pow(3,9)):
                print("33% Iterations Done...............")
            elif(t==2*pow(3,9)):
                print("66% Iterations Done.................")
            elif(t == pow(3,10)):
                print("Iterations Completed.........")
            generated_vector_r_3 = np.zeros_like(null_space[0])
            count = 0
            for i, coefficient in enumerate(coefficients):
                count = count + 1
                if i != len(coefficients) - 1 or len(coefficients)<len(null_space[0]):
                    generated_vector_r_3 += coefficient * null_space[(-course_order[i]-2)] 
            if(len(course_order)>10):
                for i in range(10,len(course_order)):
                    generated_vector_r_3 += 2 * null_space[(-course_order[i]-2)] 
            generated_vector_r_3 -= null_space[-1]
            # Check if the generated vector is already in the list
            if generated_vector_r_3.tolist() not in generated_vector_rs_3:
                if all_positive(generated_vector_r_3.tolist(),fac3load):
                    generated_vector_rs_3.append(generated_vector_r_3.tolist())

    return  generated_vector_rs_3


def create_matrix(faculties):
    # faculties is a list of faculties
    # counting
    count_3load = 0
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
                course_order.append(faculties[j].pref[i][0])
                index -= 1
    for i in range(n):
        matrix[i].append(faculties[i].maxload)
        if(int(faculties[i].maxload)==3):
            count_3load=count_3load+1
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

    return matrix,count_3load,maxCourses
matrix3 = create_dict()
matrix3Copy = copy.deepcopy(matrix3)
temp2,count_3load,cdc_count = create_matrix(matrix3)
dummy3load = []
for i in range(count_3load):
    dummy3load.append(len(matrix3)-i-1)
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
null_space = np.array(null_list_final)
print("Dimension of Null Space of Solution Set "+str(len(null_space)))
course_order = sorted(get_index_of_first_occurrence_of_all_unique_elements(course_order,null_list_final))

generated_vector_rs_3 = find_all_possible_vectors(null_space,dummy3load)
count = 0
print("Copying the solutions to output.txt file")
print(str(len(generated_vector_rs_3)) + " Different Solutions Found! ;)")
final_sol = []
output_file = os.path.join(dirname, 'output.txt')
file = open(output_file, "w")
final_assignment = {}
all_final_assignment = {}
#Extracting weights data from matrix and assign it to faculties
for sol in generated_vector_rs_3:
    f_a = []
    fac_assignment = {}
    ca = 0
    for i, s in enumerate(reversed(sol)):
        if i != 0 and i <= (len(matrix3) * len(matrix3[0].pref)) and s != 0:
            if matrix3[(i - 1) % (len(matrix3))].name in final_assignment:
                final_assignment[matrix3[(i - 1) % (len(matrix3))].name].append(
                    [matrix3[(i - 1) % (len(matrix3))].pref[(i - 1) // len(matrix3)][0], s/2,])
            else:
                final_assignment[matrix3[(i - 1) % (len(matrix3))].name] = [[matrix3[(i - 1) % (len(matrix3))].pref[(i - 1) // len(matrix3)][0], s/2,]]
    all_final_assignment[count + 1] = final_assignment
    final_assignment = {}
    final_sol.append(f_a)
    count = count + 1
    if count > 15:
        break

#making string of Loads
def makeStringForLoad(num):
    if num == 0.5:
        return "half"
    elif num == 1:
        return "full"

#Saving final Assignment to output file
max_id = 0
max_count_fdele = 0
max_count_hdcdc = 0
max_count_hdele = 0
if len(all_final_assignment) == 0:
    cdc_count = 0
for case in all_final_assignment.keys():
    matrix3 = copy.deepcopy(matrix3Copy)

    file.write("------------------Start-Case------------------")
    file.write("\n")
    file.write("Possible Solution Number: " + str(case))
    file.write("\n")
    file.write("FD CDC Assignment")
    file.write("\n")
    for faculty in all_final_assignment[case]:
        index = 0
        for i in range(len(matrix3)):
            if matrix3[i].name == faculty:
                index = i
        file.write(str(str(faculty) + " is assigned "))
        for courses in range(len(all_final_assignment[case][faculty])):
            if courses != 0:
                file.write("and ")
            matrix3[index].maxload -= 2*all_final_assignment[case][faculty][courses][1]
            file.write(str(makeStringForLoad(all_final_assignment[case][faculty][courses][1])+ " fd cdc course "+ str(all_final_assignment[case][faculty][courses][0])+ " "))
        file.write("\n")
    file.write("\n")
    t = Initial(matrix3)
    trasportation_abs = t.findTotalCourses()
    mat = trasportation_abs[0]
    dem = trasportation_abs[1]
    sup = trasportation_abs[2]
    t1 = Tricks(mat,dem,sup,float('inf'))
    final_ele,course_assigned = t1.balance()
    if course_assigned>max_count_fdele:
        max_count_fdele = course_assigned
        max_id=case
    file.write("FD Elective Assignment")
    file.write("\n")
    f = 0
    for i in final_ele:
        c = 0
        for j in i:
            c+=1
            if(j!=0):
                load = ""
                if j==1:
                    load = "half"
                elif j==2:
                    load = "full"
                file.write(str(matrix3[f].name) + " is assigned "+load+" fd elective course "+str(c))
                file.write("\n")
                matrix3[f].maxload -= j
        f+=1
    t = Initial_hdcdc(matrix3)
    trasportation_abs = t.findTotalCourses()
    mat = trasportation_abs[0]
    dem = trasportation_abs[1]
    sup = trasportation_abs[2]
    t1 = Tricks_hdcdc(mat,dem,sup,float('inf'))
    final_ele,course_assigned = t1.balance()
    if course_assigned>max_count_hdcdc:
        max_count_hdcdc = course_assigned
        max_id=case
    file.write("\n")
    file.write("HD CDC Assignment")
    file.write("\n")
    f = 0
    for i in final_ele:
        c = 0
        for j in i:
            c+=1
            if(j!=0):
                load = ""
                if j==1:
                    load = "half"
                elif j==2:
                    load = "full"
                file.write(str(matrix3[f].name) + " is assigned "+load+" hd cdc course "+str(c))
                file.write("\n")
                matrix3[f].maxload -= j
        f+=1
    
    t = Initial_hdelec(matrix3)
    trasportation_abs = t.findTotalCourses()
    mat = trasportation_abs[0]
    dem = trasportation_abs[1]
    sup = trasportation_abs[2]
    t1 = Tricks_hdelec(mat,dem,sup,float('inf'))
    final_ele,course_assigned = t1.balance()
    if course_assigned>max_count_hdele:
        max_count_hdele = course_assigned
        max_id=case
    file.write("\n")
    file.write("HD Elective Assignment")
    file.write("\n")
    f = 0
    for i in final_ele:
        c = 0
        for j in i:
            c+=1
            if(j!=0):
                load = ""
                if j==1:
                    load = "half"
                elif j==2:
                    load = "full"
                file.write(str(matrix3[f].name) + " is assigned "+load+" hd elective course "+str(c))
                file.write("\n")
                matrix3[f].maxload -= j
        f+=1

    file.write("------------------End-Case------------------")
    file.write("\n")
    file.write("\n")
    file.write("\n")
print("The maximum number of courses assigned are "+str(cdc_count+max_count_hdcdc+max_count_hdcdc+max_count_hdele)+" with "+str(cdc_count)+" FD CDCs assigned and "+str(max_count_fdele)+" FD Electives assigned and "+str(max_count_hdcdc)+" HD CDCs assigned"+"and "+str(max_count_hdele)+" HD Electives assigned"+" in Possible Solution Number: "+str(max_id))
file.close()
time.sleep(15)
