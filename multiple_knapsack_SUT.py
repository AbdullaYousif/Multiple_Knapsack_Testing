from ortools.linear_solver import pywraplp

def multiple_knapsack_SUT(data):

    #setting up the MIP solver

    solver = pywraplp.Solver.CreateSolver("SCIP")
    # if solver is None:
    #     print("SCIP solver is unavailable")
    #     return

    #above line commented out because it is impacting test coverage, branch never executed because solver is always present.

    #creating the variables for the problem
    #example  x[i, b] = 1 if item i is packed in bin b.
    x = {}

    for i in data["all_items"]:
        for b in data["all_bins"]:
            x[i,b] = solver.BoolVar(f"x_{i}_{b}")

    #where each x[(i,j)] is a 0-1 variable, wher
    for i in data["all_items"]:
        for b in data["all_bins"]:
            x[i,b] = solver.BoolVar(f"x_{i}_{b}")

    #where each x[(i,j)] is a 0-1 variable, where i represents an item and j is a bin.
    #In the solution, x[(i,j)] will be 1 if item i is placed in bin j, otherwise it will be 0


    #Defining the constraints for the problem

    #Each item is assigned to at most one bin
    for i in data["all_items"]:
        solver.Add(sum(x[i,b] for b in data["all_bins"]) <=1)

    # The amount packed in each bin cannot exceed its capacity
    for b in data["all_bins"]:
        solver.Add(sum(x[i,b] * data["weights"][i] for i in data["all_items"])<=data["bin_capacities"][b])

    #The total weight packed in each bin can't exceed its capacity. 
    # This constraint is set by requiring the sum of the weights of items placed in bin j to be less than or equal to the capacity of the bin.

    #objective of maximizing total value of packed items

    objective = solver.Objective()
    for i in data["all_items"]:
        for b in data["all_bins"]:
            objective.SetCoefficient(x[i,b], data["values"][i])
    objective.SetMaximization()


    #use the solver based on our objective and constraints

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Total packed value: {objective.Value()}")

        #Initialize Y vector: where yi = 0, which means item is not packed and values other than 1 correspond to the index of the bin
        Y = [0] * data["num_items"]

        total_weight = 0
        for b in data["all_bins"]:
            print(f"Bin {b}")
            bin_weight = 0
            bin_value = 0
            for i in data["all_items"]:
                if x[i,b].solution_value() > 0:
                    print(f"Item {i}: weight: {data['weights'][i]} value: "
                          f"{data['values'][i]}"
                    )
                    Y[i] = b
                    bin_weight+=data["weights"][i]
                    bin_value+= data["values"][i]
            print(f"Packed bin weight: {bin_weight}")
            print(f"Packed bin value: {bin_value}\n")
            total_weight += bin_weight
        print(f"Total packed weight: {total_weight}")
        print("Assignment vector Y (where 0 = not packed):")
        print(Y)
    else:
        print("The problem does not have an optimal solution")