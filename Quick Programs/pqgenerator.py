import csv

# Generate P, Q combinations sequentially
combinations = []
for p in range(1, 9):
    for q in range(1, 9):
        if p * q <= 64:
            combinations.append({
                'P': p,
                'Q': q,
                'PxQ': p * q
            })

# Sort by P, then Q
combinations.sort(key=lambda x: (x['P'], x['Q']))

# Write to CSV with the fixed format
with open('hpl_pq_combinations.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Write rows with fixed values before p, q
    for comb in combinations:
        writer.writerow([65536, 256, comb['P'], comb['Q'], 1, 1])

# Print preview of the first few rows
print("P,Q,PxQ")
for comb in combinations[:20]:
    print(f"65536, 256, {comb['P']},{comb['Q']},1,1")
