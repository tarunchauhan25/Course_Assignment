# Assignment README

This README serves as the documentation of the code.  

## Note:
We have introduced a variable `mode`.   
In mode = 1 most of the faculties are assigned complete courses.  
In mode = 2 most of the faculties are assigned half courses.  
- Details about the algorithm is provided in the video and the latex file

## Libraries used:    
- `numpy`  
- `pandas`  
- `sympy`  
- `itertools`  
- `copy`  

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
Faculty1	 is assigned full course 1 
Faculty2	 is assigned full course 3 
Faculty4	 is assigned full course 5 
Faculty5	 is assigned half course 4 
Faculty6	 is assigned full course 6 
Faculty12	 is assigned half course 2 
Faculty18	 is assigned half course 2 
Faculty11	 is assigned half course 4 
------------------End-Case------------------
```

## Interpretation:

Faculty member 'a' is assigned 0.5 of course 8 and 1.0 of course 6.
Similar assignments are made for other faculty members according to their preferences and the maximum load constraints.

## Functions created:

- `create_dict()` :

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

## Conclusion:

The output.txt file provides multiple possible solutions to the assignment problem, each adhering to the faculty members' preferences and load constraints. Analyzing these solutions can help in selecting the most suitable assignment strategy for the given scenario.
