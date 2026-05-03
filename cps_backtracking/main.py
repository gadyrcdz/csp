from cps_backtracking.csp import backtracking, initialize

variables = ["A", "B", "C", "D", "E", "F", "G"]
domain = ["Monday", "Tuesday", "Wednesday"]
constraints = [
    "A!=B", "A!=C", "B!=C", "B!=D", "B!=E",
    "C!=E", "C!=F", "D!=E", "E!=F", "E!=G", "F!=G",
]

def main():
    courses = initialize(variables, domain)
    first_course = courses[0]
    remaining_courses = courses[1:]
    assigned_courses = []

    if backtracking(first_course, remaining_courses, assigned_courses, constraints):
        for course in courses:
            print(f"{course.name}: {course.value}")
    else:
        print("No solution found")

if __name__ == "__main__":
    main()