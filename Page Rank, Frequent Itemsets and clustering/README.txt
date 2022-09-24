Student Id: A1790186
Email Id: niketaneshwar.moon@student.adelaide.edu.au

Mining Big Data Assignment 3

The Assignment3 folder contains vpgrank folder which is the virtual environment that I used.
In the readme I have given how to create a new virtual environment. 
So vpgrank is actually not needed for implementing on other laptop.

Exercise 1
Solution: Solution given in the pdf by name "MBD Assignment 3 E1 E3.1.pdf"

Exercise 2
All the code for Question 1 and Question 2 is given in the Exercise 2 folder

Go into the Assignment 3 folder
Create a virtual environment. I used virtualenv.
Command: virtualenv env_name

Activate the environment
Command: source env_name/bin/activate

Install the requirements
pip install -r requirements.txt

Change directory to Assignment3/Exercise 2
Question 1
Report of the whole code is given in "Report Exercise 2.pdf"
Run  the code using Command
python pagerank.py

Question 2
Report of the whole code is given in "Report Exercise 2.pdf"
Run the code using Command
python pagerank_google.py web-Google.txt

The file containing all the nodes and its pagerank is given in output_file.txt
The file containing list of top 10 nodes having the largest pagerank and then node and its pagerank value is given in top_10_output_file.txt
Eg.
[nodeid1, nodeid2, nodeid3, nodeid4, nodeid5, nodeid6, nodeid7, nodeid8, nodeid9, nodeid10]
Nodeid pagerank_value

The time required for execution is given in the pdf report for question 2


Exercise 3:
Question 1:
Solution is given in the pdf by name "MBD Assignment 3 E1 E3.1.pdf"

Question 2:
All the code is given in the Exercise 3 Q 2 folder filename "kmeans_iris_dataset.py"
Solution of the implementation is given in the pdf file "Kmeans and iris dataset.pdf"
Report of the code description is given in "Report Exercise 3 Q2.pdf"

Change directory to Assignment3/Exercise 3 Q 2
Make sure that the virtual environment is active. This virtual environment is the same one that we created in Exercise 2

Run the code using the below Command
python kmeans_iris_dataset.py
