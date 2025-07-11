from collections import Counter
import subprocess
import statistics
import sys
import re

#if len(sys.argv) != 3:
#    print("Usage: per-image_stats.py strong.refl dials.ssx_index.log")
#    sys.exit(1)

# Get file names from command-line arguments
#refl_file = sys.argv[1]
#index_file = sys.argv[2]
refl_file = 'strong.refl'
index_file = 'dials.ssx_index.log'

print(f"Producing reflection_table.txt...")
# Run the command and capture output
result = subprocess.run(['dials.show', 'show_all_reflection_data=true', refl_file], capture_output=True, text=True)


# Split output into lines
lines = result.stdout.splitlines()

# Find the index of the line containing " id "
start_index = 0
for i, line in enumerate(lines):
    if "(N pix)" in line:
        start_index = i + 1  # Skip this line and everything before it
        break

# Get the filtered lines
filtered_lines = lines[start_index:]

# Write to output file
with open('reflection_table.txt', 'w') as f:
    f.write('\n'.join(filtered_lines))



# Input and output file names
input_file = 'reflection_table.txt'
spots_file = 'spots.txt'

# Read the input file and extract the first column values
with open(input_file, 'r') as file:
    lines = file.readlines()
    values = [int(line.split()[0]) for line in lines if line.strip()]

# Count the occurrences of each integer
value_counts = Counter(values)

# Determine the full range of integers from min to max
min_val = min(values)
max_val = max(values)

# Write the output file with all integers in the range and their counts
with open(spots_file, 'w') as outfile:
    for i in range(min_val, max_val + 1):
        count = value_counts.get(i, 0)
        outfile.write(f"{i} {count}\n")

print(f"Output written to {spots_file}")

#index_file = 'dials.ssx_index.log'
existing_file = 'spots.txt'
output_file = 'image_stats.txt'

# Step 1: Extract values from lines containing "nxs-"
results = []
pattern = re.compile(r'nxs-(\d+).*?(\d+)/')

with open(index_file, "r") as infile:
    for line in infile:
        match = pattern.search(line)
        if match:
            first_col = match.group(1).strip()
            second_col = match.group(2).strip()
            results.append((first_col, second_col))

# Convert results to a dictionary for quick lookup
results_dict = {key: value for key, value in results}

# Step 2: Read existing file and append third and fourth columns with headers
with open(existing_file, "r") as infile, open(output_file, "w") as outfile:
    # Write headers
    outfile.write("image spots indexed prop_indexed\n")
    
    for line in infile:
        parts = line.strip().split()
        #print(parts)
        if len(parts) >= 2:
            key = parts[0].strip()
            spots = parts[1].strip()
            indexed = results_dict.get(key, "0")
            
            try:
                prop_indexed = float(indexed) / float(spots) if float(spots) != 0 else 0
            except ValueError:
                prop_indexed = 0
            outfile.write(f"{parts[0]} {spots} {indexed} {prop_indexed:.3f}\n")
        else:
            key = parts[0].strip() if parts else "UNKNOWN"
            indexed = results_dict.get(key, "0")
            outfile.write(f"{key} 0 {indexed} 0\n")


import statistics

# Initialize lists to store values from each column
spots = []
indexed = []
prop_indexed = []

# Read the output file and skip the header
with open(output_file, "r") as f:
    lines = f.readlines()[1:]  # skip header

for line in lines:
    parts = line.strip().split()
    if len(parts) >= 4:
        try:
            spot_val = float(parts[1])
            indexed_val = float(parts[2])
            prop_val = float(parts[3])

            spots.append(spot_val)
            indexed.append(indexed_val)
            prop_indexed.append(prop_val)
        except ValueError:
            continue  # skip lines with invalid data

# Calculate mean and standard deviation of column 2 (spots)
mean_spots = statistics.mean(spots)
std_spots = statistics.stdev(spots) if len(spots) > 1 else 0
hits = [val for val in spots if val >= 20]

# Calculate hit rate: non-zero entries in column 3 / total rows
non_zero_indexed = sum(1 for val in indexed if val != 0)
hit_rate = non_zero_indexed / len(indexed) if indexed else 0

# Calculate mean of non-zero values in column 4 (prop. indexed)
non_zero_prop = [val for val in prop_indexed if val != 0]
mean_non_zero_prop = statistics.mean(non_zero_prop) if non_zero_prop else 0

# Print the results
print(hits)
print(f"Mean of column 2 (spots): {mean_spots:.3f}")
print(f"Standard deviation of column 2 (spots): {std_spots:.3f}")
print(f"Index rate (non-zero indexed / total rows): {hit_rate:.3f}")
print(f"Mean of non-zero values in column 4 (prop. indexed): {mean_non_zero_prop:.3f}")





# Function to compute mean and standard deviation
#def compute_stats(values):
#    if values:
#        mean_val = statistics.mean(values)
#        std_dev = statistics.stdev(values) if len(values) > 1 else 0
#        return mean_val, std_dev
#    else:
#        return 0, 0

# Compute and print statistics
#for name, col in zip(["spots", "indexed", "prop_indexed"], [spots_vals, indexed_vals, proportion_vals]):
#    mean_val, std_dev = compute_stats(col)
#    print(f"{name.title()}: Mean = {mean_val:.2f}, Standard Deviation = {std_dev:.2f}")

# Print additional metrics
#print(f"Hits (spots ≥ 20): {hits_count}")
#print(f"Total Indexed (non-zero indexed entries): {total_indexed_count}")

0