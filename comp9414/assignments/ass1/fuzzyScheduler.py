import sys
from searchGeneric import AStarSearcher
from cspProblem import CSP, Constraint
from cspConsistency import Search_with_AC_from_CSP

###############################
# BEFORE START OUR ASSIGNMENT #
###############################

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

"""
Change class display in python file display.py:
change 'max_display_level = 1 to 'max_display_level = 0'
this is because we do not need to print the expanded path

Change class Arc in searchProblem.py:
change def __init__(self, from_node, to_node, cost=1, action=None):
to  def __init__(self, from_node, to_node, cost=0, action=None):
it is because in our assignment problem, no arc cost from one node to next node

Change AstarSearcher in searchGeneric.py:
value = path.cost + self.problem.heuristic(path.end())
to greedy search algorithm
value = self.problem.heuristic(path.end())
in order to handle with our own cost
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

        # soft_constrains ==> {t1: end-by-time, t2: end -by-time}
        # soft_cost ==> {t1: 10, t2: 10}
        self.soft_constrains = csp.soft_constraints
        self.soft_costs = csp.soft_costs

    def heuristic(self, end_node):
        # the content of end_node is below:
        # {'t1': [(11, 14), (12, 15), ...,],
        #  't2': [(11, 15), (12, 16), ...,]}
        cost_record = []  # use to record all cost for all tasks
        # iterate for every task in node
        for task in end_node:
            if task in self.soft_constrains:
                temp_cost = []
                end_by_day_time = soft_constraints[task]  # soft con rules end-by-time
                for value in end_node[task]:
                    task_actual_end_time = value[1]  # (11, 14) --> 14
                    if task_actual_end_time > end_by_day_time:
                        # calculate delay for every value in one task
                        delay = (task_actual_end_time // 10 - end_by_day_time // 10) * 24 \
                                + (task_actual_end_time % 10 - end_by_day_time % 10)
                        cost_delay = delay * self.soft_costs[task]
                        temp_cost.append(cost_delay)
                    else:
                        temp_cost.append(0)
                if len(temp_cost) > 0:
                    cost_record.append(min(temp_cost))
        total_cost = sum(cost_record)
        return total_cost


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
def uc_day(day):
    return lambda x: x[0] // 10 == day


def uc_time(time):
    return lambda x: x[0] % 10 == time


def uc_starts_before_day_and_time(day, time):
    return lambda x: x[0] <= day * 10 + time


def uc_starts_before_time(time):
    return lambda x: x[0] % 10 <= time


def uc_starts_after_day_and_time(day, time):
    return lambda x: x[0] >= day * 10 + time


def uc_starts_after_time(time):
    return lambda x: x[0] % 10 >= time


def uc_ends_before_day_and_time(day, time):
    return lambda x: x[1] <= day * 10 + time


def uc_ends_before_time(time):
    return lambda x: x[1] % 10 <= time


def uc_ends_after_day_and_time(day, time):
    return lambda x: x[1] >= day * 10 + time


def uc_ends_after_time(time):
    return lambda x: x[1] % 10 >= time


def uc_starts_in_period(day1, time1, day2, time2):
    return lambda x: day1 * 10 + time1 <= x[0] <= day2 * 10 + time2


def uc_ends_in_period(day1, time1, day2, time2):
    return lambda x: day1 * 10 + time1 <= x[1] <= day2 * 10 + time2


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

    file_name = sys.argv[1]  # read command argv[1]
    with open(file_name, 'r') as input_file:
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
                    condition = bc_before
                    constraints.append(Constraint(scope, bc_before))
                if data[2] == "after":
                    condition = bc_after
                    constraints.append(Constraint(scope, condition))
                if data[2] == "same-day":
                    condition = bc_same_day
                    constraints.append(Constraint(scope, condition))
                if data[2] == "starts-at":
                    condition = bc_starts_at
                    constraints.append(Constraint(scope, condition))

        # when read soft constraints and unary constraints
        for line in my_content:
            if "domain" in line:
                data = line.strip().split(' ')
                if data[2] == "ends-by":  # read soft constraints
                    task = data[1]
                    day = day2num[data[3]]
                    time = time2num[data[4]]
                    soft_cost[task] = int(data[-1])
                    soft_constraints[task] = 10 * day + time
                else:  # read unary constraints
                    if data[2] in day2num.keys():  # case: domain, <t>, <day>
                        scope = (data[1],)
                        day = day2num[data[2]]
                        condition = uc_day(day)
                        constraints.append(Constraint(scope, condition))
                    if data[2] in time2num.keys():  # case: domain, <t>, <time>
                        scope = (data[1],)
                        time = time2num[data[2]]
                        condition = uc_time(time)
                        constraints.append(Constraint(scope, condition))
                    if data[2] == "starts-before":
                        if data[3] in time2num.keys():  # case: domain, <t>, starts-before <time>
                            scope = (data[1],)
                            time = time2num[data[3]]
                            condition = uc_starts_before_time(time)
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, starts-before <day> <time>
                            scope = (data[1],)
                            day = day2num[data[3]]
                            time = time2num[data[4]]
                            condition = uc_starts_before_day_and_time(day, time)
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "starts-after":
                        if data[3] in time2num.keys():  # case: domain, <t>, starts-after <time>
                            scope = (data[1],)
                            time = time2num[data[3]]
                            condition = uc_starts_after_time(time)
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, starts-after <day> <time>
                            scope = (data[1],)
                            day = day2num[data[3]]
                            time = time2num[data[4]]
                            condition = uc_starts_after_day_and_time(day, time)
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "ends-before":
                        if data[3] in time2num.keys():  # case: domain, <t>, ends-before <time>
                            scope = (data[1],)
                            time = time2num[data[3]]
                            condition = uc_ends_before_time(time)
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, ends-before <day> <time>
                            scope = (data[1],)
                            day = day2num[data[3]]
                            time = time2num[data[4]]
                            condition = uc_ends_before_day_and_time(day, time)
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "ends-after":
                        if data[3] in time2num.keys():  # case: domain, <t>, ends-after <time>
                            scope = (data[1],)
                            time = time2num[data[3]]
                            condition = uc_ends_after_time(time)
                            constraints.append(Constraint(scope, condition))
                        elif data[3] in day2num.keys():  # case: domain, <t>, ends-after <day> <time>
                            scope = (data[1],)
                            day = day2num[data[3]]
                            time = time2num[data[4]]
                            condition = uc_ends_after_day_and_time(day, time)
                            constraints.append(Constraint(scope, condition))
                    if data[2] == "starts-in":
                        start_day = day2num[data[3]]
                        start_time = time2num[data[4].split('-')[0]]
                        end_day = day2num[data[4].split('-')[1]]
                        end_time = time2num[data[5]]
                        scope = (data[1],)
                        condition = uc_starts_in_period(start_day, start_time, end_day, end_time)
                        constraints.append(Constraint(scope, condition))
                    if data[2] == "ends-in":
                        start_day = day2num[data[3]]
                        start_time = time2num[data[4].split('-')[0]]
                        end_day = day2num[data[4].split('-')[1]]
                        end_time = time2num[data[5]]
                        scope = (data[1],)
                        condition = uc_ends_in_period(start_day, start_time, end_day, end_time)
                        constraints.append(Constraint(scope, condition))

        # get domains for each task
        for var in variables:
            task = var[0]
            duration = var[1]
            domains[task] = sorted({(i * 10 + j, i * 10 + j + duration) for i in range(1, 6) for j in range(1, 10 - duration)})

    # print("variables = ", variables)
    # print("domains = ", domains)
    # print("constraints", constraints)
    # print("soft_constraints", soft_constraints)
    # print("soft_cost", soft_cost)

    # which adds soft_constraints and soft_cost compared with origin
    my_csp = My_CSP(domains, constraints, soft_constraints, soft_cost)
    my_problem = Search_with_AC_from_Cost_CSP(my_csp)
    my_searcher = AStarSearcher(my_problem)

    my_solution = my_searcher.search()
    # print(my_solution)
    if my_solution is not None:  # there is a solution if finding a path
        final_schedule = my_solution.end()  # find the end node(result) in our solution path
        if final_schedule is not None:
            my_cost = my_problem.heuristic(final_schedule)
            for task in final_schedule:
                start_time = list(final_schedule[task])[0][0]
                day = start_time // 10
                time = start_time % 10
                output_day = ""
                output_time = ""
                for key in day2num:
                    if day2num[key] == day:
                        output_day = key
                for key in time2num:
                    if time2num[key] == time:
                        output_time = key
                print(f'{task}:{output_day} {output_time}')
            print(f'cost:{my_cost}')
    else:
        print('No solution!')
