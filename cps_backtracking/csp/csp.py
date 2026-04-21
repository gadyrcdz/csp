import copy


class Course:
#     function __init__(name, domain)
#         name <- name
#         domain <- domain
#         value <- empty
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.value;

#     function assign(value)
#         value of the course <- value
    def assign(self,value):
        self.value = value
#     function remove assignment
#         value of the course <- empty
    def remove_assignment(self):
        self.value = 0

# function initialize(variables, domain)
#     courses <- empty list
#     for each variable in variables
#         course <- new course with that variable and a copy of the domain
#         add course to courses
#     return courses
    def initialize(self, variables, domain):
        courses = []
        for each in variables:
            course = Course(each, copy.deepcopy(domain))
            courses.append(course)
        return courses

def initialize(variables, domain) -> list[Course]:
    courses = []

    for variable in variables:
        course = Course(name=variable, domain=domain.copy())
        courses.append(course)

    return courses

    def is_consistent(self, course, assignedCourses, constraints):
        assigned_by_name = assignedCourses.get("name", 0)

        for each in constraints:
            left, right = each.split("!=")

            if(course is not left and course is not right):
                continue
            
            if(course == left):
                other_name = right
            else:
                other_name = left

            other_course = assignedCourses.get(other_name, 0)
            if(other_course == 0):
                continue
            if(course.value == other_course):
                return False
            
        return True
                

def is_consistent(course: Course, assigned_courses: list[Course], constraints) -> bool:
    assigned_by_name = {
        assigned_course.name: assigned_course for assigned_course in assigned_courses
    }

    for constraint in constraints:
        left, right = constraint.split("!=")

        if course.name != left and course.name != right:
            continue

        other_name = right if course.name == left else left
        other_course = assigned_by_name.get(other_name)

        if other_course is None or other_course.value is None:
            continue

        if course.value == other_course.value:
            return False

    return True


def backtracking(
    course: Course,
    remaining_courses: list[Course],
    assigned_courses: list[Course],
    constraints: list[str],
) -> bool:
    for day in course.domain:
        course.assign(day)

        if not is_consistent(course, assigned_courses, constraints):
            course.remove_assignment()

            continue

        assigned_courses.append(course)

        if not remaining_courses:
            return True

        next_course = remaining_courses[0]
        next_remaining_courses = remaining_courses[1:]

        if backtracking(
            next_course, next_remaining_courses, assigned_courses, constraints
        ):
            return True

        assigned_courses.pop()
        course.remove_assignment()

    return False


def _neighbors(name: str, constraints: list[str]):
    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         if name is equal to left
    #             add right to result
    #         else if name is equal to right
    #             add left to result

    #     return result
    result = []
    for e in constraints:
        left, right = e.split("!=")
        if(name == left):
            result.append(right)
        elif(name ==right):
            result.append(left)
    return result


            

    # raise Exception("Not implemented")


def _arc_satisfied(x: str, y: str, X: Course, Y: Course, constraints: list[str]):

    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         if (X is left and Y is right) or (X is right and Y is left)
    #             if x val is equal to y val
    #                 return false

    #     return true
    # raise Exception("Not implemented")
    for e in constraints:
        left, right = e.split("!=")
        if((X == left) and (X == right) or (X == right) and (Y == left)):
            if(x == y):
                return False
    return True


def revise(X: Course, Y: Course, constraints: list[str]):

    #     revised <- false

    #     for each x in a copy of X domain
    #         if no value y in Y domain satisfies arc satisfied(x, y, X, Y, constraints)
    #             remove x from X domain
    #             revised <- true

    #     return revised
    raise Exception("Not implemented")


def ac3(courses: list[Course], constraints: list[str]):
    #     course map <- dictionary of courses using the name as key
    #     queue <- empty deque

    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         add (left, right) to queue
    #         add (right, left) to queue

    #     while queue is not empty
    #         x name, y name <- take the first element from queue
    #         X <- course with x name from course map
    #         Y <- course with y name from course map

    #         if revise(X, Y, constraints)
    #             if X domain is empty
    #                 return false
    #             for each z name in neighbors(x name, constraints)
    #                 if z name is not equal to y name
    #                     add (z name, x name) to queue

    #     return true
    raise Exception("Not implemented")


def select_mrv(unassigned: list[Course], constraints: list[str]):
    #     return the course in unassigned with the smallest domain
    raise Exception("Not implemented")


def _degree(course: Course, unassigned_names, constraints: list[str]):
    #     count <- 0

    #     for each constraint in constraints
    #         left, right <- split the constraint by "!="

    #         if course name is equal to left and right is in unassigned names
    #             increment count by 1

    #         else if course name is equal to right and left is in unassigned names
    #             increment count by 1

    #     return count
    raise Exception("Not implemented")


def select_degree(unassigned: list[Course], constraints: list[str]):

    #     unassigned names <- set of names of unassigned courses

    #     for each course compute degree as the number of constraints
    #         involving that course where the other variable is also unassigned

    #     return the course with the highest degree
    raise Exception("Not implemented")


def select_mrv_degree(unassigned: list[Course], constraints: list[str]):
    #     min size <- smallest domain size among unassigned courses
    #     candidates <- all unassigned courses whose domain size equals min size

    #     if there is only one candidate
    #         return that candidate

    #     unassigned names <- set of names of unassigned courses

    #     for each candidate compute degree as the number of constraints
    #         involving that candidate where the other variable is also unassigned

    #     return the candidate with the highest degree
    raise Exception("Not implemented")


def _select_first(unassigned: list[Course], constraints: list[str]):
    #     return the first course in unassigned
    raise Exception("Not implemented")


def backtracking_with_inference(
    unassigned: list[Course],
    assigned: list[Course],
    constraints: list[str],
    select=_select_first,
):
    #     if unassigned is empty
    #         return true

    #     course <- select var(unassigned, constraints)
    #     remaining <- all courses in unassigned except course

    #     for each day in a copy of course domain
    #         assign that day to the course

    #         if the assignment is not consistent
    #             remove the assignment from the course
    #             continue with the next day

    #         add course to assigned
    #         all courses <- assigned combined with remaining
    #         saved domains <- save a copy of the domain of every course in all courses
    #         set course domain to contain only that day
    #         inference ok <- ac3(all courses, constraints)

    #         if inference ok
    #             if backtracking with inference(remaining, assigned, constraints, select var)
    #                 return true

    #         restore the domain of every course from saved domains
    #         remove course from assigned
    #         remove the assignment from the course
    #     return false
    raise Exception("Not implemented")
