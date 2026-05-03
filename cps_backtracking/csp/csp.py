from collections import deque
import copy


class Course:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.value = None  # Inicializado a None en lugar de vacío

    def assign(self, value):
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def remove_assignment(self):
        self.value = None  # Cambiado a None para ser consistente

    def initialize(self, variables, domain):
        courses = []
        for each in variables:
            course = Course(each, copy.deepcopy(domain))
            courses.append(course)
        return courses


def initialize(variables, domain) -> list[Course]:
    courses = []
    for each in variables:
        course = Course(each, copy.deepcopy(domain))
        courses.append(course)
    return courses


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
        if backtracking(next_course, next_remaining_courses, assigned_courses, constraints):
            return True
        assigned_courses.pop()
        course.remove_assignment()
    return False


def _neighbors(name: str, constraints: list[str]):
    result = []
    for e in constraints:
        left, right = e.split("!=")
        if name == left:
            result.append(right)
        elif name == right:
            result.append(left)
    return result


def _arc_satisfied(x: str, y: str, X: Course, Y: Course, constraints: list[str]):
    for e in constraints:
        left, right = e.split("!=")
        if (X.name == left and Y.name == right) or (X.name == right and Y.name == left):
            if x == y:
                return False
    return True


def revise(X: Course, Y: Course, constraints: list[str]):
    revised = False
    for x in X.domain[:]:
        if not any(_arc_satisfied(x, y, X, Y, constraints) for y in Y.domain):
            X.domain.remove(x)
            revised = True
    return revised


def ac3(courses: list[Course], constraints: list[str]):
    assigned_by_name = {c.name: c for c in courses}
    queue = deque()
    for e in constraints:
        left, right = e.split("!=")
        queue.append((left, right))
        queue.append((right, left))
    while queue:
        x_name, y_name = queue.popleft()  # popleft para FIFO (más eficiente)
        X = assigned_by_name.get(x_name)
        Y = assigned_by_name.get(y_name)
        if revise(X, Y, constraints):
            if len(X.domain) == 0:
                return False
            for z_name in _neighbors(x_name, constraints):
                if z_name != y_name:
                    queue.append((z_name, x_name))
    return True


# ─── Funciones faltantes ────────────────────────────────────────────────────

def select_mrv(unassigned: list[Course], constraints: list[str]) -> Course:
    """Mínimos Valores Restantes: elige el curso con el dominio más pequeño."""
    return min(unassigned, key=lambda c: len(c.domain))


def _degree(course: Course, unassigned_names: set, constraints: list[str]) -> int:
    """Cuenta cuántas restricciones tiene course con otras variables no asignadas."""
    count = 0
    for constraint in constraints:
        left, right = constraint.split("!=")
        if course.name == left and right in unassigned_names:
            count += 1
        elif course.name == right and left in unassigned_names:
            count += 1
    return count


def select_degree(unassigned: list[Course], constraints: list[str]) -> Course:
    """Heurística de grado: elige el curso con más restricciones sobre no asignados."""
    unassigned_names = {c.name for c in unassigned}
    return max(unassigned, key=lambda c: _degree(c, unassigned_names, constraints))


def select_mrv_degree(unassigned: list[Course], constraints: list[str]) -> Course:
    """MRV con desempate por grado."""
    min_size = min(len(c.domain) for c in unassigned)
    candidates = [c for c in unassigned if len(c.domain) == min_size]
    if len(candidates) == 1:
        return candidates[0]
    unassigned_names = {c.name for c in unassigned}
    return max(candidates, key=lambda c: _degree(c, unassigned_names, constraints))


def _select_first(unassigned: list[Course], constraints: list[str]) -> Course:
    """Selección simple: devuelve el primer curso de la lista."""
    return unassigned[0]


def backtracking_with_inference(
    unassigned: list[Course],
    assigned: list[Course],
    constraints: list[str],
    select=_select_first,
) -> bool:
    """Backtracking con inferencia AC-3 después de cada asignación."""
    if not unassigned:
        return True

    course = select(unassigned, constraints)
    remaining = [c for c in unassigned if c is not course]

    for day in course.domain[:]:  # copia del dominio para iterar con seguridad
        course.assign(day)

        if not is_consistent(course, assigned, constraints):
            course.remove_assignment()
            continue

        assigned.append(course)
        all_courses = assigned + remaining

        # Guardar dominios antes de la inferencia
        saved_domains = {c.name: c.domain[:] for c in all_courses}

        # Restringir el dominio del curso actual al valor asignado
        course.domain = [day]

        if ac3(all_courses, constraints):
            if backtracking_with_inference(remaining, assigned, constraints, select):
                return True

        # Restaurar dominios
        for c in all_courses:
            c.domain = saved_domains[c.name]

        assigned.pop()
        course.remove_assignment()

    return False