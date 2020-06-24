import sys
from searchGeneric import AStarSearcher
from cspProblem import CSP, Constraint
from cspConsistency import Search_with_AC_from_CSP

###############################
# BEFORE START OUR ASSIGNMENT #
###############################
"""
Change class display in python file display.py:
change 'max_display_level = 1 to 'max_display_level = 0'
this is because we do not need to print the expanded path

Change class Arc in searchProblem.py:
change def __init__(self, from_node, to_node, cost=1, action=None):
to  def __init__(self, from_node, to_node, cost=0, action=None):
it is because in our assignment problem, no arc cost from one node to next node

Change AstarSearcher
value = path.cost + self.problem.heuristic(path.end())
to greedy search algorithm
value = self.problem.heuristic(path.end())
in order to handle with our own cost
"""

"""
A CSP problem for this assignment need:
1. domains ==> {
                't1': {(start, end), (start, end)...}, 
                't2': {(start, end), (start, end)...}
                }
2. (hard) contraints ==> [
                Constraint(('t2',), func_),
                Constraint(('t1', 't2'), func_relation),
                Constraint(('t1', 't2'), func_relation),
                ] 
3. soft constrains ==> {t1: end-by-time, t2: end-by-time}
4. soft cost ==>  {t1: 10, t2: 10}
"""


################################
###### START TO IMPLEMENT ######
################################

# extend newCSP inherited from CSP
# we add attributes soft_constraints and soft_costs
class My_CSP(CSP):
    def __init__(self, domains, constraints, soft_constraints, soft_costs):
        super().__init__(domains, constraints)
        self.soft_constraints = soft_constraints
        self.soft_costs = soft_costs


class Search_with_AC_from_Cost_CSP(Search_with_AC_from_CSP):
    def __init__(self, csp):
        super().__init__(csp)
        self.soft_constrains = csp.soft_constraints
        self.soft_costs = csp.soft_costs


# define hard binary constraints
def bc_before(t1, t2):
    # 't1': {(start, end), (start, end)...},
    # 't2': {(start, end), (start, end)...}
    return t1[1] <= t2[0]  # t1.end_time <= t2.start_time


def bc_after(t1, t2):
    return t1[0] >= t2[1]  # t1.start_time >= t2.end_time


def bc_same_day(t1, t2):
    return t1[0] // 10 == t2[0] // 10  # t1.start_time.day >= t2.start_time.day


def bc_starts_at(t1, t2):
    return t1[0] == t2[1]  # t1.start_time.day >= t2.start_time.day


# define hard unary constraints
def uc_starts_before_day_and_time(t1):
    pass


if __name__ == '__main__':
    # transform "mon, tue, wed, thu, fri" to numbers
    # transform "9am, 10am, 11am, 12pm, 1pm, 2pm, 3pm, 4pm, 5pm" to numbers
    # days = {'mon', 'tue', 'wed', 'thu', 'fri'}
    # time = {'9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'}
    day2num = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5}
    time2num = {'9am': 1, '10am': 2, '11am': 3, '12pm': 4, '1pm': 5, '2pm': 6, '3pm': 7, '4pm': 8, '5pm': 9}
    domains = {}
    constraints = []
    soft_constraints = {}
    soft_cost = {}
    with open('input1.txt', 'r') as input_file:
        variables = []  # (task, duration)
        file_content = input_file.readlines()
        my_content = []
        for line in file_content:
            if '#' in line:
                continue
            my_content.append(line)

        # when read tasks
        for line in my_content:
            if "task" in line:
                data = line.strip().split(' ')
                variables.append((data[1], int(data[2])))

        # when read binary constraints
        for line in my_content:
            if "constraint" in line:
                data = line.strip().split(' ')
                scope = (data[1], data[3])
                if data[2] == "before":
                    condition = lambda x, y: x.end_time <= y.start_time
                    constraints.append(Constraint(scope, condition))
                if data[2] == "after":
                    condition = lambda x, y: y.end_time <= x.start_time
                    constraints.append(Constraint(scope, condition))
                if data[2] == "same-day":
                    condition = lambda x, y: x.start_time.day == y.start_time.day
                    constraints.append(Constraint(scope, condition))
                if data[2] == "starts-at":
                    condition = lambda x, y: x.start_time == y.end_time
                    constraints.append(Constraint(scope, condition))

        # when read soft constraints and unary constraints
        for line in my_content:
            if "domain" in line:
                data = line.strip().split(' ')
                if data[2] == "ends-by":  # read soft constraints
                    task = data[1]
                    day = day2num[data[3]]
                    time = time2num[data[4]]
                    soft_cost[task] = data[-1]
                    soft_constraints[task] = 10 * day + time
                else:  # read unary constraints
                    if data[2] in day2num.keys():  # case: domain, <t>, <day>
                        scope = (data[1],)
                        condition = lambda x: x.start_time.day == day2num[data[2]]
                        constraints.append(Constraint(scope, condition))
                    if data[2] in time2num.keys():  # case: domain, <t>, <time>
                        scope = (data[1],)
                        condition = lambda x: x.start_time.time == time2num[data[2]]
                        constraints.append(Constraint(scope, condition))
                    if data[2] == "starts-before":
                        if data[3] in time2num.keys():  # case: domain, <t>, starts-before <time>
                            scope = (data[1],)
                            condition = lambda x: x.start_time.time <= time2num[data[3]]
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, starts-before <day> <time>
                            scope = (data[1],)
                            condition = lambda x: x.start_time <= day2num[data[3]] + time2num[data[4]]
                            # condition = lambda x: x.start_time.day <= day2num[data[3]] and x.start_time.time <= time2num[data[4]]
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "starts-after":
                        if data[3] in time2num.keys():  # case: domain, <t>, starts-after <time>
                            scope = (data[1],)
                            condition = lambda x: x.start_time.time >= time2num[data[3]]
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, starts-after <day> <time>
                            scope = (data[1],)
                            condition = lambda x: x.start_time >= day2num[data[3]] + time2num[data[4]]
                            # condition = lambda x: x.start_time.day >= day2num[data[3]] and x.start_time.time >= time2num[data[4]]
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "ends-before":
                        if data[3] in time2num.keys():  # case: domain, <t>, ends-before <time>
                            scope = (data[1],)
                            condition = lambda x: x.end_time.time <= time2num[data[3]]
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, ends-before <day> <time>
                            scope = (data[1],)
                            condition = lambda x: x.end_time <= day2num[data[3]] + time2num[data[4]]
                            # condition = lambda x: x.end_time.day <= day2num[data[3]] and x.end_time.time <= time2num[data[4]]
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "ends-after":
                        if data[3] in time2num.keys():  # case: domain, <t>, ends-after <time>
                            scope = (data[1],)
                            condition = lambda x: x.end_time.time >= time2num[data[3]]
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, ends-after <day> <time>
                            scope = (data[1],)
                            condition = lambda x: x.end_time >= day2num[data[3]] + time2num[data[4]]
                            # condition = lambda x: x.end_time.day >= day2num[data[3]] and x.end_time.time >= time2num[data[4]]
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "starts-in":
                        start_day = data[3]
                        start_time = data[4].split('-')[0]
                        end_day = data[4].split('-')[1]
                        end_time = data[5]
                        scope = (data[1],)
                        condition = lambda x: day2num[start_day] + time2num[start_time] <= x.start_time <= day2num[end_day] + time2num[end_time]
                        constraints.append(Constraint(scope, condition))
                    if data[2] == "ends-in":
                        start_day = data[3]
                        start_time = data[4].split('-')[0]
                        end_day = data[4].split('-')[1]
                        end_time = data[5]
                        scope = (data[1],)
                        condition = lambda x: day2num[start_day] + time2num[start_time] <= x.end_time <= day2num[end_day] + time2num[end_time]
                        constraints.append(Constraint(scope, condition))

        # get domains for each task
        for var in variables:
            task = var[0]
            duration = var[1]
            domains[task] = sorted({(i * 10 + j, i * 10 + j + duration) for i in range(1, 6) for j in range(1, 10 - duration)})

    print("variables = ", variables)
    print("domains = ", domains)
    print("constraints", constraints)
    print("soft_constraints", soft_constraints)
    print("soft_cost", soft_cost)

    # create my own constraints:
    # which adds soft_constraints and soft_cost compared with origin
    my_csp = My_CSP(domains, constraints, soft_constraints, soft_cost)

    searcher = AStarSearcher(Search_with_AC_from_Cost_CSP(my_csp))
