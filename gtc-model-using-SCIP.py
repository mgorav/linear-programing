from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')

    infinity = solver.infinity()
    # wrenches
    wrenches = solver.IntVar(0.0, infinity, 'wrenches')
    # pliers
    pliers = solver.IntVar(0.0, infinity, 'pliers')


    print('Number of variables =', solver.NumVariables())

    # constraints
    # steel
    solver.Add(1.5 * wrenches + pliers <= 27000)
    # molding
    solver.Add(1.0 * wrenches + pliers <= 21000)
    # assembly
    solver.Add(0.3 * wrenches + 0.5 * pliers <= 9000)
    # demand1
    solver.Add(wrenches <= 15000)
    # demand2
    solver.Add(pliers <= 16000)

    print('Number of constraints =', solver.NumConstraints())

    # objective function
    solver.Maximize(0.13 * wrenches + 0.10 * pliers)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
            print('Solution:')
            print('Objective value =', solver.Objective().Value())
            print('Wrenches =', wrenches.solution_value())
            print('Pliers =', pliers.solution_value())
            print('Slack steel', (27000 - (1.5 * wrenches.solution_value() + pliers.solution_value())))
            print('Slack molding', (21000 - (1.0 * wrenches.solution_value() + pliers.solution_value())))
            print('Slack assembly',(9000 -(0.3 * wrenches.solution_value() + 0.5 * pliers.solution_value())))
            print('Slack demand1',(15000 - wrenches.solution_value()))
            print('Slack demand2',(16000 - pliers.solution_value()))
    else:
            print('The problem does not have an optimal solution.')


    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    main()