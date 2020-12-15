from ortools.linear_solver import pywraplp


def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')

    infinity = solver.infinity()
    # Short-haul (Bombardier CRJ-900)
    x = solver.IntVar(0.0, infinity, 'x')
    # Long-haul (Airbus A350)
    y = solver.IntVar(0.0, infinity, 'y')

    print('Number of variables =', solver.NumVariables())

    # constraints
    # Fuel required/day
    solver.Add(110000 * x + 220000 * y <= 7800000)
    # Crew hours Required/day
    solver.Add(24 * x + 80 * y <= 2200)
    # Pilot Hours required/day
    solver.Add(8 * x + 35 * y <= 865)
    # In-hangar storage capacity (demand)
    solver.Add(x <= 32)
    solver.Add(y <= 20)

    print('Number of constraints =', solver.NumConstraints())

    # objective function
    solver.Maximize(4400 * x + 5100 * y)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        objective_value = solver.Objective().Value()
        print('Objective value =', objective_value)
        print('x (Short-haul (Bombardier CRJ-900)) =', x.solution_value())
        print('y (Long-haul (Airbus A350)) =', y.solution_value())
        slack_fuel = (7800000 - (110000 * x.solution_value() + 220000 * y.solution_value()))
        print('Slack Fuel required/day = ', slack_fuel)
        print('Slack Crew hours Required/day = ', (2200 - (24 * x.solution_value() + 80 * y.solution_value())))
        print('Slack Pilot Hours required/day', (865 - (8 * x.solution_value() + 35 * y.solution_value())))

        print("Given cost of fuel 0.25 and ability to sell back.Adjusted profit....")

        print("New objective value " + str(objective_value + (0.25 * slack_fuel)))

    else:
        print('The problem does not have an optimal solution.')

    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    main()
