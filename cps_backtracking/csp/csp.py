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

# function is consistent(course, assigned courses, constraints)
#     assigned by name <- dictionary of assigned courses using the name as key

#     for each constraint in constraints
#         left, right <- split the constraint by "!="

#         if the course is not left and is not right
#             continue with the next constraint

#         other name <- right if the course is left, otherwise left
#         other course <- assigned course with that name

#         if other course does not exist or has no assigned value
#             continue with the next constraint

#         if the current course value is equal to the other course value
#             return false

#     return true

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
                

# function backtracking(course, remaining courses, assigned courses, constraints)
#     for each day in the domain of the course
#         assign that day to the course

#         if the assignment is not consistent
#             remove the assignment from the course
#             continue with the next day

#         add the course to assigned courses

#         if there are no remaining courses
#             return true

#         next course <- first course in remaining courses
#         next remaining courses <- all remaining courses except the first one

#         if backtracking(next course, next remaining courses, assigned courses, constraints)
#             return true

#         remove the last assigned course
#         remove the assignment from the current course

#     return false
