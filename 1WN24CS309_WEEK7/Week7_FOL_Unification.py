import re


def parse_expression(s):
    s = s.replace(" ", "")
    if "(" not in s:
        return s

    idx = s.find("(")
    name = s[:idx]

    args = []
    current_arg = []
    bracket_count = 0

    for char in s[idx + 1 : -1]:
        if char == "(":
            bracket_count += 1
        elif char == ")":
            bracket_count -= 1

        if char == "," and bracket_count == 0:
            args.append(parse_expression("".join(current_arg)))
            current_arg = []
        else:
            current_arg.append(char)

    if current_arg:
        args.append(parse_expression("".join(current_arg)))

    return [name] + args


def expr_to_str(expr):
    if isinstance(expr, list):
        return f"{expr[0]}({', '.join(expr_to_str(e) for e in expr[1:])})"
    return str(expr)


def is_variable(term):
    return isinstance(term, str) and len(term) == 1 and term.islower()


def occurs_in(var, term):
    if var == term:
        return True
    if isinstance(term, list):
        return any(occurs_in(var, t) for t in term)
    return False


def apply_subst(term, subst):
    if is_variable(term):
        return subst.get(term, term)
    if isinstance(term, list):
        return [apply_subst(t, subst) for t in term]
    return term


def compose_subst(subst, new_s):
    updated = {}
    for var, val in subst.items():
        updated[var] = apply_subst(val, new_s)
    for var, val in new_s.items():
        if var not in updated:
            updated[var] = val
    return updated


def unify(psi1, psi2):
    if isinstance(psi1, str) or isinstance(psi2, str):
        if psi1 == psi2:
            return {}
        if is_variable(psi1):
            if occurs_in(psi1, psi2):
                return "FAILURE"
            return {psi1: psi2}
        if is_variable(psi2):
            if occurs_in(psi2, psi1):
                return "FAILURE"
            return {psi2: psi1}
        return "FAILURE"

    if psi1[0] != psi2[0]:
        return "FAILURE"

    if len(psi1) != len(psi2):
        return "FAILURE"

    subst = {}

    for i in range(1, len(psi1)):
        arg1 = apply_subst(psi1[i], subst)
        arg2 = apply_subst(psi2[i], subst)

        s = unify(arg1, arg2)
        if s == "FAILURE":
            return "FAILURE"

        if s != {}:
            subst = compose_subst(subst, s)

    return subst


if __name__ == "__main__":
    print("Rule: Single lowercase letters (x, y, z, w) are treated as variables.")
    print("Example format: P(x, f(g(x)), y)\n")

    input_1 = input("Enter Expression 1: ")
    input_2 = input("Enter Expression 2: ")

    try:
        expr1 = parse_expression(input_1)
        expr2 = parse_expression(input_2)

        result = unify(expr1, expr2)

        if result == "FAILURE":
            print("\nResult: Unification FAILED.")
        else:
            print("\nResult: Unification SUCCESSFUL!")
            if not result:
                print("Substitution Set: NIL (Expressions are already identical)")
            else:
                print("Substitution Set (MGU):")
                for var, val in result.items():
                    print(f"  {var} -> {expr_to_str(val)}")

                unified_expr = expr_to_str(apply_subst(expr1, result))
                print(f"\nUnified Output Form: {unified_expr}")

    except Exception as e:
        print(f"\nParsing Error: Please verify parenthesis layout syntax. Details: {e}")
