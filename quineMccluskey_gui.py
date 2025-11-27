import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd

def get_minterms():
    variables = var_entry.get()
    my_variables = variables.split()
    number_minterms = int(minterm_count_entry.get())
    min_terms = list(map(int, minterms_entry.get().split()))
    max_bits = len(my_variables)
    binary_dict = {term: format(term, f'0{max_bits}b') for term in min_terms}
    return binary_dict, min_terms, my_variables

def reduction(min_dict, step_log):
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
                steps.append(f"Pair ({u}, {u2}) → {combined}")
    
    step_log.append("\n".join(steps))
    return combined_terms, not_combined_terms

def compute():
    binary_dict, minterms, my_variables = get_minterms()
    num_reductions = len(my_variables) - 1
    current_dict = binary_dict
    all_not_combined_terms = []
    step_log = []
    
    # Binary Representation
    step_log.append("Binary Representation:\n" + "\n".join(f"{k}: {v}" for k, v in binary_dict.items()))
    
    # Reduction Steps
    for step in range(num_reductions):
        step_log.append(f"\nAfter Reduction {step + 1}:")
        combined_terms, not_combined_terms = reduction(current_dict, step_log)
        all_not_combined_terms.extend(not_combined_terms.values())
        current_dict = combined_terms
    
    # Prime Implicants
    all_prime_implicants = list(set(all_not_combined_terms))
    step_log.append("\nPrime Implicants: " + str(all_prime_implicants))
    
    # Coverage Table
    coverage_table = {m: [] for m in minterms}
    for implicant in all_prime_implicants:
        for m in minterms:
            if all(c1 == c2 or c1 == '_' for c1, c2 in zip(implicant, binary_dict[m])):
                coverage_table[m].append(implicant)
    
    step_log.append("\nCoverage Table:")
    for k, v in coverage_table.items():
        step_log.append(f"{k}: {v}")
    
    # Essential Prime Implicants
    essential_prime_implicants = list(set(implicant[0] for implicant in coverage_table.values() if len(implicant) == 1))
    step_log.append("\nEssential Prime Implicants: " + str(essential_prime_implicants))
    
    # Generating Boolean Expression
    my_expression = [
        "".join(variable if bit == '1' else variable + "'" if bit == '0' else "" for bit, variable in zip(term, my_variables))
        for term in essential_prime_implicants
    ]
    result_label.config(text=f"Simplified Expression: F = {' + '.join(my_expression)}")
    
    # Display Steps in Text Area
    step_text.config(state=tk.NORMAL)
    step_text.delete(1.0, tk.END)
    step_text.insert(tk.END, "\n".join(step_log))
    step_text.config(state=tk.DISABLED)

# GUI Setup
app = tk.Tk()
app.title("Quine-McCluskey Simplifier")
app.configure(bg="#1e1e2e")

tk.Label(app, text="Enter Variables (space separated):", fg="white", bg="#1e1e2e").pack()
var_entry = tk.Entry(app, bg="#282a36", fg="white")
var_entry.pack()

tk.Label(app, text="Enter Number of Minterms:", fg="white", bg="#1e1e2e").pack()
minterm_count_entry = tk.Entry(app, bg="#282a36", fg="white")
minterm_count_entry.pack()

tk.Label(app, text="Enter Minterms (space separated):", fg="white", bg="#1e1e2e").pack()
minterms_entry = tk.Entry(app, bg="#282a36", fg="white")
minterms_entry.pack()

tk.Button(app, text="Compute", command=compute, bg="#ff79c6", fg="black").pack()
result_label = tk.Label(app, text="", fg="white", bg="#1e1e2e")
result_label.pack()

step_text = scrolledtext.ScrolledText(app, width=60, height=20, bg="#282a36", fg="white", state=tk.DISABLED)
step_text.pack()

app.mainloop()
