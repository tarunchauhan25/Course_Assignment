# Course Assignment
## Our Team
1. Tanish Desai (2022A7PS0053G)
2. Aditya Bagla (2022A7PS0497G)
3. Tarun Chauhan (2022A7PS0025G)
 
This project contains algorithm to solve the Faculty Course Assignment problem. Given the prefrence list of faculties, we have to assign them courses within their prefrence list.  

## Note:  
Due to Github restriction (of 25 mb) we could not upload the video and executable file here. Please access them through [this google drive link](https://drive.google.com/drive/folders/13WKMec3Ds-A400uwICikQeUK2Obra-s-?usp=sharing).  
If the system does not have the given library then use the `Executable` folder for procedure to run the code. The folder contains a setup video and a zip for both MacOS and Windows.

## Algorithms used:
We have introduced a variable `mode`.   
If `mode` = 0, most of the faculties are assigned half courses.  
If `mode` = 1, most of the faculties are assigned complete courses.  

We have used two techniques to solve the given Course Assignment problem: Linear Programming and Transportation method  

Our main algorithm is Linear Programming which is implemented in [`courseAssignment.py`](courseAssignment.py) (details of implementation in latex file and video). Files [`elec_Algorithm.py`](elec_Algorithm.py), [`hd_CDC_algo.py`](hd_CDC_algo.py) and [`hd_Elec_algo.py`](hd_Elec_algo.py) contain Transportation algorithm.  

It can be thought of a transportation problem where the main matrix will contain a constant value (-1 in this case) for the courses in prefrence list, infnity elsewhere. The demands of course will be 1 and supply by the faculties will be their maximum loads.

## Libraries used:    
- `numpy`  
- `pandas`  
- `sympy`  
- `itertools`  
- `copy`
- `time`
- `os`

## Files created:  
- [`Documentation.pdf`](Documentation.pdf) : pdf form of `doc.tex`
- [`courseAssignment.py`](courseAssignment.py) : main file
- [`courseAssignment.spec`](courseAssignment.spec) : used for making executable code (.exe)
- [`crash_test.pdf`](crash_test.pdf) : crash test report
- [`doc.tex`](doc.tex) : latex documentation
- [`elec_Algorithm.py`](elec_Algorithm.py), [`hd_CDC_algo.py`](hd_CDC_algo.py) and [`hd_Elec_algo.py`](hd_Elec_algo.py) : respective algorithms for electives and CDCs
- [`input_1.csv`](input_1.csv) and [`input_2.csv`](input_2.csv) : contains the input in csv format
- [`output1.txt`](output_1.txt) and [`output2.txt`](output_2.txt) : stores the output in text format
- [`random_testcase_generator.py`](random_testcase_generator.py) : generates random testcases based on the given number of faculty and courses
-  [`testcase.pdf`](testcase.pdf) : contains description of testcases and their outputs

## Functions created:  

> ### courseAssignment.py:  
- `create_dict()` :  takes data from `input.csv` and creates seperate list (array) of `Faculty` objects for fd/hd courses and electives
- `get_index_of_first_occurrence_of_all_unique_elements(list1,null_space_list)` :  
             - Input: Flatten from of faculty prefernce list and null_space_vectors in a list   
             - Purpose: This function iterates over all the prefernces of faculties and returns the index of first occurence of courses to assign those as free variables on whom we will iterate.

- `all_positive(list1)` :  
            - Input: a list containing values of Xi  
            - Purpose: this checks if the values in the list is >= 0 and <= 2 (since Xi should belong to the set {0, 1, 2})

  
- `find_all_possible_vectors(null_space)` :  
            - Input: a list containing null space vectors  
            - Purpose: it creates an empty list to store generated vectors and iterated over all possible combinations of coefficients

  
- `create_matrix(faculties)` :  
            - Input: a list containing `Faculty` objects  
            - Purpose: creates the equation matrix

- `makeStringForLoad(num)` :  
            - Input: a number  
            - Purpose: returns the equivalent english word for the number  



> ### elec_Algorithm.py, hd_CDC_algo.py and fd_Elec_algo.py:
  - `findTotalCourses(self)` : finds the maximum course id given in the prefrence list of faculties
  - `generateMatrix(self)` : creates a matrix for solving the transportation problem
  - `createDemand(self)`, `createSupply(self)` : calculates the demand and supply matrix respectively
  - `balance(self)` : if the total demand is not equal to the total supply, we need to make them equal by introducing dummy course or faculty
  - `penalties(self)` : calculates the penalties and stores them in a list. It also appends the answer in `self.allAns` when the assignment is done
  - `operation(self)` : updates `self.matrix` after performaing calculations used for solving transportation problem
  - `final(self)` : returns one possible assignment

## Input File: input.csv

The `input.csv` file contains information about faculty members and their preferences for courses. Here's a breakdown of the columns:

- **Faculty_Name:** The name of the faculty member.
- **Faculty_Num:** The unique identifier for each faculty member.
- **Max_Load:** The maximum number of courses a faculty member can be assigned.
- **Course_Pref:** A list of course preferences, represented as an array of course numbers.

## Output File: output.txt

The `output.txt` file presents several possible solutions for assigning courses to faculty members. Each solution is labeled as "Possible Solution Number X," where X is the solution number. The assignments are then listed for each faculty member, indicating the fraction of the course assigned and the course number.

### Sample Output:

```plaintext
------------------Start-Case------------------
Possible Solution Number: 1
FD CDC Assignment
Professor_1 is assigned full fd cdc course 10 
Professor_2 is assigned full fd cdc course 7 
Professor_3 is assigned full fd cdc course 2 and half fd cdc course 3 
Professor_4 is assigned full fd cdc course 11 
Professor_5 is assigned full fd cdc course 4 
Professor_6 is assigned full fd cdc course 5 
Professor_7 is assigned full fd cdc course 1 
Professor_9 is assigned full fd cdc course 6 
Professor_21 is assigned full fd cdc course 8 
Professor_17 is assigned full fd cdc course 9 
Professor_25 is assigned half fd cdc course 3 

FD Elective Assignment
Professor_1 is assigned half fd elective course 1
Professor_2 is assigned half fd elective course 2
Professor_4 is assigned half fd elective course 2
Professor_5 is assigned half fd elective course 1
Professor_6 is assigned half fd elective course 6
Professor_7 is assigned half fd elective course 4
Professor_8 is assigned full fd elective course 3
Professor_8 is assigned half fd elective course 7
Professor_9 is assigned half fd elective course 5
Professor_10 is assigned half fd elective course 4
Professor_10 is assigned half fd elective course 5
Professor_11 is assigned half fd elective course 6
Professor_11 is assigned half fd elective course 7
Professor_12 is assigned full fd elective course 8

HD CDC Assignment
Professor_13 is assigned full hd cdc course 3
Professor_14 is assigned full hd cdc course 1
Professor_15 is assigned full hd cdc course 2
Professor_18 is assigned full hd cdc course 4
Professor_20 is assigned full hd cdc course 5

HD Elective Assignment
Professor_16 is assigned full hd elective course 1
Professor_19 is assigned full hd elective course 4
Professor_22 is assigned full hd elective course 2
Professor_24 is assigned full hd elective course 5
------------------End-Case------------------

```
## Conclusion:

The output.txt file provides multiple possible solutions to the assignment problem, each adhering to the faculty members' preferences and load constraints. Analyzing these solutions can help in selecting the most suitable assignment strategy for the given scenario.
