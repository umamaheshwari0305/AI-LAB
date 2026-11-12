
# First Order Logic - Forward Chaining

# Initial Knowledge Base (Facts)
facts = {
    ("American", "Robert"),
    ("Enemy", "A", "America"),
    ("Owns", "A", "T1"),
    ("Missile", "T1")
}

# Rules:
# 1. Enemy of America is Hostile
# 2. Missiles are Weapons
# 3. Missiles owned by a country are sold to it by Robert
# 4. An American selling weapons to a hostile nation is Criminal

print("Initial Knowledge Base:")
for fact in sorted(facts):
    print(fact)

print("\nApplying Forward Chaining Rules...\n")

# Rule 1: Enemy(x, America) -> Hostile(x)
for fact in list(facts):
    if fact[0] == "Enemy" and fact[2] == "America":
        new_fact = ("Hostile", fact[1])
        if new_fact not in facts:
            facts.add(new_fact)
            print("Rule 1 applied:", new_fact)

# Rule 2: Missile(x) -> Weapon(x)
for fact in list(facts):
    if fact[0] == "Missile":
        new_fact = ("Weapon", fact[1])
        if new_fact not in facts:
            facts.add(new_fact)
            print("Rule 2 applied:", new_fact)

# Rule 3: Missile(x) AND Owns(A, x)
#         -> Sells(Robert, x, A)
for missile in list(facts):
    if missile[0] == "Missile":
        x = missile[1]
        if ("Owns", "A", x) in facts:
            new_fact = ("Sells", "Robert", x, "A")
            if new_fact not in facts:
                facts.add(new_fact)
                print("Rule 3 applied:", new_fact)

# Rule 4: American(p) AND Weapon(q) AND
#         Sells(p, q, r) AND Hostile(r)
#         -> Criminal(p)

for person in list(facts):
    if person[0] == "American":
        p = person[1]

        for sale in list(facts):
            if sale[0] == "Sells" and sale[1] == p:
                q = sale[2]
                r = sale[3]

                if (("Weapon", q) in facts and
                    ("Hostile", r) in facts):

                    new_fact = ("Criminal", p)

                    if new_fact not in facts:
                        facts.add(new_fact)
                        print("Rule 4 applied:", new_fact)

# Check the goal
print("\nFinal Result:")

if ("Criminal", "Robert") in facts:
    print("Goal Proved: Robert is a Criminal.")
else:
    print("Goal Not Proved.")
