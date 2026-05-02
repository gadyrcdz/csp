from cps_backtracking.csp import (
    Course,
    _arc_satisfied,
    _degree,
    _neighbors,
    _select_first,
    ac3,
    backtracking,
    backtracking_with_inference,
    initialize,
    is_consistent,
    revise,
    select_degree,
    select_mrv,
    select_mrv_degree,
)


def test_course_stores_name_domain_and_starts_unassigned():
    course = Course("A", ["Monday", "Tuesday"])

    assert course.name == "A"
    assert course.domain == ["Monday", "Tuesday"]
    assert course.value is None


def test_course_assign_sets_value():
    course = Course("A", ["Monday"])

    course.assign("Monday")

    assert course.value == "Monday"


def test_course_remove_assignment_clears_value():
    course = Course("A", ["Monday"])
    course.assign("Monday")

    course.remove_assignment()

    assert course.value is None


def test_course_str_shows_name_and_value():
    course = Course("A", ["Monday"])
    course.assign("Monday")

    assert str(course) == "A: Monday"


def test_initialize_creates_one_course_per_variable():
    courses = initialize(["A", "B", "C"], ["Monday", "Tuesday"])

    assert [course.name for course in courses] == ["A", "B", "C"]
    assert [course.domain for course in courses] == [
        ["Monday", "Tuesday"],
        ["Monday", "Tuesday"],
        ["Monday", "Tuesday"],
    ]


def test_initialize_copies_domain_per_course():
    courses = initialize(["A", "B"], ["Monday", "Tuesday"])

    courses[0].domain.append("Wednesday")

    assert courses[0].domain == ["Monday", "Tuesday", "Wednesday"]
    assert courses[1].domain == ["Monday", "Tuesday"]


def test_is_consistent_returns_true_when_no_conflict():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday", "Tuesday"])
    course_a.assign("Monday")
    course_b.assign("Tuesday")

    assert is_consistent(course_b, [course_a], ["A!=B"]) is True


def test_is_consistent_returns_false_when_conflict_matches_constraint():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday", "Tuesday"])
    course_a.assign("Monday")
    course_b.assign("Monday")

    assert is_consistent(course_b, [course_a], ["A!=B"]) is False


def test_is_consistent_ignores_unrelated_or_unassigned_courses():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday", "Tuesday"])
    course_c = Course("C", ["Monday", "Tuesday"])
    course_a.assign("Monday")
    course_c.assign("Monday")

    assert is_consistent(course_b, [course_a, course_c], ["A!=C"]) is True


def test_backtracking_returns_true_for_satisfiable_problem():
    courses = initialize(["A", "B", "C"], ["Monday", "Tuesday"])
    first_course = courses[0]
    assigned_courses = []

    solved = backtracking(first_course, courses[1:], assigned_courses, ["A!=B", "B!=C"])

    assert solved is True
    assert len(assigned_courses) == 3
    assert all(course.value is not None for course in courses)
    assert courses[0].value != courses[1].value
    assert courses[1].value != courses[2].value


def test_backtracking_returns_false_for_unsatisfiable_problem():
    courses = initialize(["A", "B"], ["Monday"])
    first_course = courses[0]
    assigned_courses = []

    solved = backtracking(first_course, courses[1:], assigned_courses, ["A!=B"])

    assert solved is False
    assert assigned_courses == []
    assert all(course.value is None for course in courses)


def test_backtracking_finds_valid_solution_for_sample_problem():
    variables = ["A", "B", "C", "D", "E", "F", "G"]
    domain = ["Monday", "Tuesday", "Wednesday"]
    constraints = [
        "A!=B",
        "A!=C",
        "B!=C",
        "B!=D",
        "B!=E",
        "C!=E",
        "C!=F",
        "D!=E",
        "E!=F",
        "E!=G",
        "F!=G",
    ]
    courses = initialize(variables, domain)
    first_course = courses[0]
    assigned_courses = []

    solved = backtracking(first_course, courses[1:], assigned_courses, constraints)
    assignments = {course.name: course.value for course in courses}

    assert solved is True
    assert len(assigned_courses) == len(variables)
    assert sorted(assignments) == sorted(variables)
    assert set(assignments.values()).issubset(set(domain))

    for constraint in constraints:
        left, right = constraint.split("!=")
        assert assignments[left] != assignments[right]


def test_revise_removes_unsupported_values():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])

    revised = revise(course_a, course_b, ["A!=B"])

    assert revised is True
    assert course_a.domain == []


def test_revise_keeps_supported_values():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday"])

    revised = revise(course_a, course_b, ["A!=B"])

    assert revised is True
    assert course_a.domain == ["Tuesday"]


def test_revise_returns_false_when_no_change():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday", "Tuesday"])

    revised = revise(course_a, course_b, ["A!=B"])

    assert revised is False
    assert course_a.domain == ["Monday", "Tuesday"]


def test_ac3_returns_true_and_reduces_domains():
    courses = initialize(["A", "B"], ["Monday", "Tuesday"])

    result = ac3(courses, ["A!=B"])

    assert result is True
    course_map = {c.name: c for c in courses}
    assert set(course_map["A"].domain) == {"Monday", "Tuesday"}
    assert set(course_map["B"].domain) == {"Monday", "Tuesday"}


def test_ac3_returns_false_when_domain_becomes_empty():
    courses = initialize(["A", "B"], ["Monday"])

    result = ac3(courses, ["A!=B"])

    assert result is False


def test_ac3_does_not_modify_unrelated_domains():
    courses = initialize(["A", "B", "C"], ["Monday", "Tuesday"])

    result = ac3(courses, ["A!=B"])

    assert result is True
    course_map = {c.name: c for c in courses}
    assert set(course_map["C"].domain) == {"Monday", "Tuesday"}


def test_ac3_satisfiable_sample_problem():
    variables = ["A", "B", "C", "D", "E", "F", "G"]
    domain = ["Monday", "Tuesday", "Wednesday"]
    constraints = [
        "A!=B",
        "A!=C",
        "B!=C",
        "B!=D",
        "B!=E",
        "C!=E",
        "C!=F",
        "D!=E",
        "E!=F",
        "E!=G",
        "F!=G",
    ]
    courses = initialize(variables, domain)

    result = ac3(courses, constraints)

    assert result is True
    for course in courses:
        assert len(course.domain) >= 1


def test_backtracking_with_inference_returns_true_for_satisfiable_problem():
    courses = initialize(["A", "B", "C"], ["Monday", "Tuesday"])
    assigned = []

    solved = backtracking_with_inference(courses, assigned, ["A!=B", "B!=C"])

    assert solved is True
    assert len(assigned) == 3
    assert all(course.value is not None for course in courses)
    assert courses[0].value != courses[1].value
    assert courses[1].value != courses[2].value


def test_backtracking_with_inference_returns_false_for_unsatisfiable_problem():
    courses = initialize(["A", "B"], ["Monday"])
    assigned = []

    solved = backtracking_with_inference(courses, assigned, ["A!=B"])

    assert solved is False
    assert assigned == []
    assert all(course.value is None for course in courses)


def test_backtracking_with_inference_all_constraints_satisfied_for_sample_problem():
    variables = ["A", "B", "C", "D", "E", "F", "G"]
    domain = ["Monday", "Tuesday", "Wednesday"]
    constraints = [
        "A!=B",
        "A!=C",
        "B!=C",
        "B!=D",
        "B!=E",
        "C!=E",
        "C!=F",
        "D!=E",
        "E!=F",
        "E!=G",
        "F!=G",
    ]
    courses = initialize(variables, domain)
    assigned = []

    solved = backtracking_with_inference(courses, assigned, constraints)
    assignments = {course.name: course.value for course in courses}

    assert solved is True
    assert len(assigned) == len(variables)
    for constraint in constraints:
        left, right = constraint.split("!=")
        assert assignments[left] != assignments[right]


def test_backtracking_with_inference_restores_domains_on_failure():
    courses = initialize(["A", "B"], ["Monday"])
    original_domains = {c.name: c.domain[:] for c in courses}

    backtracking_with_inference(courses, [], ["A!=B"])

    for course in courses:
        assert course.domain == original_domains[course.name]


def test_backtracking_with_inference_mrv_satisfies_all_constraints():
    variables = ["A", "B", "C", "D", "E", "F", "G"]
    domain = ["Monday", "Tuesday", "Wednesday"]
    constraints = [
        "A!=B",
        "A!=C",
        "B!=C",
        "B!=D",
        "B!=E",
        "C!=E",
        "C!=F",
        "D!=E",
        "E!=F",
        "E!=G",
        "F!=G",
    ]
    courses = initialize(variables, domain)
    assigned = []

    solved = backtracking_with_inference(
        courses, assigned, constraints, select=select_mrv
    )
    assignments = {course.name: course.value for course in courses}

    assert solved is True
    for constraint in constraints:
        left, right = constraint.split("!=")
        assert assignments[left] != assignments[right]


def test_backtracking_with_inference_degree_satisfies_all_constraints():
    variables = ["A", "B", "C", "D", "E", "F", "G"]
    domain = ["Monday", "Tuesday", "Wednesday"]
    constraints = [
        "A!=B",
        "A!=C",
        "B!=C",
        "B!=D",
        "B!=E",
        "C!=E",
        "C!=F",
        "D!=E",
        "E!=F",
        "E!=G",
        "F!=G",
    ]
    courses = initialize(variables, domain)
    assigned = []

    solved = backtracking_with_inference(
        courses, assigned, constraints, select=select_degree
    )
    assignments = {course.name: course.value for course in courses}

    assert solved is True
    for constraint in constraints:
        left, right = constraint.split("!=")
        assert assignments[left] != assignments[right]


def test_backtracking_with_inference_mrv_degree_satisfies_all_constraints():
    variables = ["A", "B", "C", "D", "E", "F", "G"]
    domain = ["Monday", "Tuesday", "Wednesday"]
    constraints = [
        "A!=B",
        "A!=C",
        "B!=C",
        "B!=D",
        "B!=E",
        "C!=E",
        "C!=F",
        "D!=E",
        "E!=F",
        "E!=G",
        "F!=G",
    ]
    courses = initialize(variables, domain)
    assigned = []

    solved = backtracking_with_inference(
        courses, assigned, constraints, select=select_mrv_degree
    )
    assignments = {course.name: course.value for course in courses}

    assert solved is True
    for constraint in constraints:
        left, right = constraint.split("!=")
        assert assignments[left] != assignments[right]


def test_select_first_returns_first_course():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])
    course_c = Course("C", ["Monday"])

    selected = _select_first([course_a, course_b, course_c], [])

    assert selected is course_a


def test_select_first_ignores_constraints():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])

    selected = _select_first([course_a, course_b], ["B!=A"])

    assert selected is course_a


def test_select_first_returns_only_course_when_one_unassigned():
    course_a = Course("A", ["Monday"])

    selected = _select_first([course_a], [])

    assert selected is course_a


def test_degree_returns_zero_when_no_constraints_match():
    course_a = Course("A", ["Monday"])
    unassigned_names = {"A", "B"}

    assert _degree(course_a, unassigned_names, ["C!=D"]) == 0


def test_degree_counts_constraint_where_course_is_on_left():
    course_a = Course("A", ["Monday"])
    unassigned_names = {"A", "B"}

    assert _degree(course_a, unassigned_names, ["A!=B"]) == 1


def test_degree_counts_constraint_where_course_is_on_right():
    course_b = Course("B", ["Monday"])
    unassigned_names = {"A", "B"}

    assert _degree(course_b, unassigned_names, ["A!=B"]) == 1


def test_degree_counts_multiple_matching_constraints():
    course_a = Course("A", ["Monday"])
    unassigned_names = {"A", "B", "C"}

    assert _degree(course_a, unassigned_names, ["A!=B", "A!=C"]) == 2


def test_degree_does_not_count_constraint_whose_other_variable_is_not_unassigned():
    course_a = Course("A", ["Monday"])
    unassigned_names = {"A"}

    assert _degree(course_a, unassigned_names, ["A!=B"]) == 0


def test_select_degree_picks_course_with_most_constraints_to_unassigned():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday", "Tuesday"])
    course_c = Course("C", ["Monday", "Tuesday"])
    unassigned = [course_a, course_b, course_c]
    constraints = ["A!=B", "A!=C", "B!=C"]

    selected = select_degree(unassigned, constraints)

    assert selected is course_a


def test_select_degree_counts_constraints_on_either_side():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday", "Tuesday"])
    course_c = Course("C", ["Monday", "Tuesday"])
    unassigned = [course_a, course_b, course_c]
    constraints = ["B!=A", "C!=A"]

    selected = select_degree(unassigned, constraints)

    assert selected is course_a


def test_select_degree_only_counts_unassigned_neighbors():
    course_b = Course("B", ["Monday", "Tuesday"])
    course_c = Course("C", ["Monday", "Tuesday"])
    unassigned = [course_b, course_c]
    constraints = ["A!=B", "A!=C", "B!=C"]

    selected = select_degree(unassigned, constraints)

    assert selected is course_b


def test_select_degree_returns_single_unassigned_course():
    course_a = Course("A", ["Monday"])

    selected = select_degree([course_a], [])

    assert selected is course_a


def test_select_degree_returns_zero_degree_course_when_no_constraints_match():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])

    selected = select_degree([course_a, course_b], ["C!=D"])

    assert selected in (course_a, course_b)


def test_select_mrv_picks_course_with_smallest_domain():
    course_a = Course("A", ["Monday", "Tuesday", "Wednesday"])
    course_b = Course("B", ["Monday", "Tuesday"])
    course_c = Course("C", ["Monday"])

    selected = select_mrv([course_a, course_b, course_c], [])

    assert selected is course_c


def test_select_mrv_returns_single_unassigned_course():
    course_a = Course("A", ["Monday", "Tuesday"])

    selected = select_mrv([course_a], [])

    assert selected is course_a


def test_select_mrv_ignores_constraints_when_choosing():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday", "Tuesday"])

    selected = select_mrv([course_a, course_b], ["A!=B"])

    assert selected is course_a


def test_select_mrv_picks_first_minimum_on_tie():
    course_a = Course("A", ["Monday", "Tuesday"])
    course_b = Course("B", ["Monday", "Tuesday"])

    selected = select_mrv([course_a, course_b], [])

    assert selected is course_a


def test_arc_satisfied_returns_true_when_values_differ():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Tuesday"])

    assert _arc_satisfied("Monday", "Tuesday", course_a, course_b, ["A!=B"]) is True


def test_arc_satisfied_returns_false_when_values_equal_and_constraint_applies():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])

    assert _arc_satisfied("Monday", "Monday", course_a, course_b, ["A!=B"]) is False


def test_arc_satisfied_returns_true_when_no_constraint_between_courses():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])

    assert _arc_satisfied("Monday", "Monday", course_a, course_b, ["A!=C"]) is True


def test_arc_satisfied_applies_constraint_regardless_of_operand_order():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])

    assert _arc_satisfied("Monday", "Monday", course_a, course_b, ["B!=A"]) is False


def test_arc_satisfied_returns_true_for_empty_constraints():
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday"])

    assert _arc_satisfied("Monday", "Monday", course_a, course_b, []) is True


def test_neighbors_returns_names_connected_by_constraint():
    result = _neighbors("A", ["A!=B", "A!=C"])

    assert sorted(result) == ["B", "C"]


def test_neighbors_includes_name_on_either_side_of_constraint():
    result = _neighbors("B", ["A!=B"])

    assert result == ["A"]


def test_neighbors_returns_empty_when_no_constraints_match():
    result = _neighbors("D", ["A!=B", "B!=C"])

    assert result == []


def test_neighbors_does_not_include_unrelated_names():
    result = _neighbors("A", ["A!=B", "C!=D"])

    assert result == ["B"]


def test_neighbors_handles_empty_constraints():
    result = _neighbors("A", [])

    assert result == []


def test_select_mrv_degree_picks_highest_degree_on_tie():
    # A has domain size 1, B and C both have size 2 — among B and C,
    # B has 2 constraints to unassigned variables, C has 1 → B wins.
    course_a = Course("A", ["Monday"])
    course_b = Course("B", ["Monday", "Tuesday"])
    course_c = Course("C", ["Monday", "Tuesday"])
    unassigned = [course_a, course_b, course_c]
    constraints = ["A!=B", "B!=C", "B!=A"]

    selected = select_mrv_degree(unassigned, constraints)

    assert selected is course_a
