# Assignment README

This README provides an overview and guidance for the assignment process described in the provided `input.csv` file and the generated `output.txt` file.

## Input File: input.csv

The `input.csv` file contains information about faculty members and their preferences for courses. Here's a breakdown of the columns:

- **Faculty_Name:** The name of the faculty member.
- **Faculty_Num:** The unique identifier for each faculty member.
- **Max_Load:** The maximum number of courses a faculty member can be assigned.
- **Course_Pref:** A list of course preferences, represented as an array of course numbers.

## Output File: output.txt

The `output.txt` file presents several possible solutions for assigning courses to faculty members. Each solution is labeled as "Possible Solution Number X," where X is the solution number. The assignments are then listed for each faculty member, indicating the fraction of the course assigned and the course number.

### Example Solution:

```plaintext
Possible Solution Number 1
a is assigned 0.5 course 8
b is assigned 0.5 course 1
d is assigned 0.5 course 7
e is assigned 0.5 course 2
g is assigned 0.5 course 8
i is assigned 0.5 course 3
a is assigned 1.0 course 6
c is assigned 1.0 course 4
h is assigned 1.0 course 5
j is assigned 0.5 course 3
k is assigned 0.5 course 1
l is assigned 0.5 course 7
m is assigned 0.5 course 2
n is assigned 1.0 course 9
--------------------End-Case----------------------
```

## Interpretation:

Faculty member 'a' is assigned 0.5 of course 8 and 1.0 of course 6.
Similar assignments are made for other faculty members according to their preferences and the maximum load constraints.

## Conclusion:

The output.txt file provides multiple possible solutions to the assignment problem, each adhering to the faculty members' preferences and load constraints. Analyzing these solutions can help in selecting the most suitable assignment strategy for the given scenario.
