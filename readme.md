to run source code install ortools library (pip install ortools)


COMBINATORIAL TESTING

In terms of input parameters, the key variables that influence the programs behavior are:

weights: A vector which contains the weights of the items
values: A vector which contains the values of the items
capacities (knapsacks): A vector containing the capacities of all the bins
number of items
number of knapsacks
capacity constraints
weight-value correlation



 py -3.11 -m venv .venv
 .\.venv\Scripts\activate
 python -m pip install --upgrade pip
 pip install -r requirements.txt



 coverage:

 coverage run --branch pairwise_generation.py
 coverage report -m
 coverage html
 start htmlcov/index.html

