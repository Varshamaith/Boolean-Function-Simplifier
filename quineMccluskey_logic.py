import pandas as pd

def get_minterms():
    variables = input("Enter the variables separated by space: ")
    my_variables = variables.split()
    number_minterms = int(input("Enter the number of minterms: "))
    max_integer = 0
    min_terms = []
    binary_dict = {}

    for i in range(number_minterms):
        a = int(input(f"Enter minterm {i + 1}: "))
        max_integer = max(max_integer, a)
        min_terms.append(a)

    max_bits = len(my_variables)

    for term in min_terms:
        binary = format(term, f'0{max_bits}b')
        binary_dict[term] = binary

    print("\nBinary representation of minterms:\n")
    for k, v in binary_dict.items():
        print(f'{k} | {v}')
        print('----------')
    print()

    return binary_dict, min_terms, my_variables

def reduction(min_dict):
    combined_terms = {}
    not_combined_terms = {u: v for u, v in min_dict.items()}
    steps = []

    for i, (u, v) in enumerate(min_dict.items()):
        for j, (u2, v2) in enumerate(list(min_dict.items())[i + 1:]):
            count = 0
            combined = ''
            for char1, char2 in zip(v, v2):
                if char1 != char2:
                    count += 1
                    combined += '_'
                else:
                    combined += char1
            if count == 1:
                combined_terms[(u, u2)] = combined
                if u in not_combined_terms:
                    del not_combined_terms[u]
                if u2 in not_combined_terms:
                    del not_combined_terms[u2]
                steps.append({'Pair': (u, u2), 'Combined': combined})
                
    df_reduction = pd.DataFrame(steps)
    return combined_terms, not_combined_terms, df_reduction

# Call the functions
binary_dict, minterms, my_variables = get_minterms()

# Determine the number of reductions needed
num_reductions = len(my_variables) - 1

# Perform the reductions dynamically
current_dict = {k: v for k, v in binary_dict.items()}
all_not_combined_terms = []

for reduction_step in range(num_reductions):
    print(f"After Reduction {reduction_step + 1}:")
    combined_terms, not_combined_terms, df_reduction = reduction(current_dict)
    print(df_reduction)
    print()
    print(f'Not combined terms in reduction {reduction_step + 1}:')
    for k, v in not_combined_terms.items():
        print(v, end=" ")
    print('\n____________________________________________')

    all_not_combined_terms.extend(not_combined_terms.values())
    current_dict = combined_terms

# Combine all prime implicants (not combined terms) from all reductions
all_prime_implicants = list(set(all_not_combined_terms))
print(f"All Prime Implicants: {all_prime_implicants}")
print("\n")

# Create a coverage table
coverage_table = {m: [] for m in minterms}
for implicant in all_prime_implicants:
    for m in minterms:
        m_binary = binary_dict[m]
        if all(c1 == c2 or c1 == '_' for c1, c2 in zip(implicant, m_binary)):
            coverage_table[m].append(implicant)

# Find essential prime implicants
essential_prime_implicants = []
for minterm, implicants in coverage_table.items():
    if len(implicants) == 1:
        essential_prime_implicants.append(implicants[0])

# Remove duplicates from essential prime implicants
essential_prime_implicants = list(set(essential_prime_implicants))

print("Essential Prime Implicants:", essential_prime_implicants)
print("\n")

# Getting the expression
# Creating separate list for storing the expression
my_expression = []

for term in essential_prime_implicants:
    expression = ""
    for bit, variable in zip(term, my_variables):
        if bit == '1':
            expression += variable
        elif bit == '0':
            expression += variable + "'"
        elif bit == '_':
            pass  # Skip the underscores which are not used in expressions
    my_expression.append(expression)
result = ' + '.join(my_expression)

print("Simplified Expression:")
print("----------------------")
print("F =", result)
