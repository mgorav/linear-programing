from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')

    infinity = solver.infinity()
    # Medium-haul (Boeing 787-10)
    x = solver.IntVar(0.0, infinity, 'x')
    # Luxury (Airbus A380)
    y = solver.IntVar(0.0, infinity, 'y')

    print('Number of variables =', solver.NumVariables())

    # constraints
    # Fuel required/day
    solver.Add(168300 * x + 258000 * y  <= 7800000 )
    # Crew hours Required/day
    solver.Add(51 * x + 68 * y <= 2200)
    # Pilot Hours required/day
    solver.Add(20 * x + 22 * y <= 865)
    # In-hangar storage capacity (demand)
    solver.Add(x <= 24)
    solver.Add(y <= 20)

    print('Number of constraints =', solver.NumConstraints())

    # objective function
    solver.Maximize(5050 * x + 7650 * y)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
            print('Solution:')
            print('Objective value =', solver.Objective().Value())
            print('x (Medium-haul (Boeing 787-10)) =', x.solution_value())
            print('y Luxury (Airbus A380)) =', y.solution_value())

            print('Slack Fuel required/day = ', (7800000 - (168300 * x.solution_value() + 258000 * y.solution_value()) ))
            print('Slack Crew hours Required/day = ', (2200 - (51 * x.solution_value() + 68 * y.solution_value())))
            print('Slack Pilot Hours required/day',865 - (20 * x.solution_value() + 22 * y.solution_value()))

    else:
            print('The problem does not have an optimal solution.')


    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    main()