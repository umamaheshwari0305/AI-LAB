import re


def parse_symbols(kb_expr, query_expr):
    combined = f"{kb_expr} {query_expr}"
    symbols = set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", combined))
    symbols.discard("and")
    symbols.discard("or")
    symbols.discard("not")
    return sorted(list(symbols))


def evaluate(expr, model):
    safe_expr = (
        expr.replace("and", " and ").replace("or", " or ").replace("not", " not ")
    )
    tokens = safe_expr.split()
    processed_tokens = []

    for token in tokens:
        if token in model:
            processed_tokens.append(str(model[token]))
        else:
            processed_tokens.append(token)

    try:
        return bool(eval(" ".join(processed_tokens)))
    except:
        return False


def generate_models(symbols):
    if not symbols:
        return [{}]
    p = symbols[0]
    rest = symbols[1:]
    sub_models = generate_models(rest)
    models = []
    for sub in sub_models:
        m_true = sub.copy()
        m_true[p] = True
        m_false = sub.copy()
        m_false[p] = False
        models.extend([m_true, m_false])
    return models


def print_truth_table(kb_expr, query_expr, symbols):
    header = " | ".join(symbols) + " || KB    | Query | Match?"
    print("\nTRUTH TABLE:")
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    models = generate_models(symbols)
    # Sort models to display nicely (True/False sequences grouped)
    models.sort(key=lambda m: [m[sym] for sym in symbols], reverse=True)

    is_entailed = True

    for model in models:
        kb_val = evaluate(kb_expr, model)
        query_val = evaluate(query_expr, model)

        match_status = "OK"
        if kb_val and not query_val:
            match_status = "FAIL"
            is_entailed = False
        elif not kb_val:
            match_status = "-"

        row_vals = [
            "T" if model[sym] else "F" for sym in symbols
        ]
        row_str = " | ".join(row_vals)
        kb_str = "T" if kb_val else "F"
        q_str = "T" if query_val else "F"

        print(f"{row_str} || {kb_str:<5} | {q_str:<5} | {match_status}")

    print("-" * len(header))
    return is_entailed


if __name__ == "__main__":
    print("Enter logic using standard syntax: 'and', 'or', 'not'\n")

    print("Enter your 3 Knowledge Base sentences:")
    sent1 = input("Sentence 1: ")
    sent2 = input("Sentence 2: ")
    sent3 = input("Sentence 3: ")

    query = input("\nEnter the Query to check: ")

    full_kb = f"({sent1}) and ({sent2}) and ({sent3})"
    all_symbols = parse_symbols(full_kb, query)

    entails_query = print_truth_table(full_kb, query, all_symbols)

    if entails_query:
        print("\nSUCCESS: The Knowledge Base ENTAILS the query.")
    else:
        print(
            "\nFAILURE: The Knowledge Base DOES NOT entail the query.\n(See 'FAIL' rows where KB is True but Query is False)"
        )
