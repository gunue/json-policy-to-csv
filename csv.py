import pandas as pd
import json

# Load JSON data from policy.json
with open("policy.json", "r") as file:
    data = json.load(file)

# Extract policies data
policies = data["policies"]

# Create a DataFrame
df = pd.DataFrame(policies)

# Mapping 'disabled' to 'Status' and renaming columns as per requirement
df['Status'] = df['disabled'].apply(lambda x: 'Enabled' if not x else 'Disabled')
df['Stage'] = df['lifecycleStages'].apply(lambda x: ", ".join(x))
df['Severity'] = df['severity']
df['Id'] = df['id']
df['Policy Name'] = df['name']
df['Description'] = df['description']
df['Remediation'] = df['remediation']
df['Rationale'] = df['rationale']

# Selecting the required columns
df = df[['Id', 'Severity', 'Stage', 'Policy Name', 'Status', 'Description', 'Remediation', 'Rationale']]

# Define custom sorting order for lifecycle stages
stage_order = {'RUNTIME': 0, 'DEPLOY': 1, 'BUILD, DEPLOY': 2, 'BUILD': 3}

# Sort lifecycle stages and then the entire DataFrame
df['Stage'] = df['Stage'].apply(lambda x: ", ".join(sorted(x.split(", "), key=lambda s: stage_order.get(s, 4))))
df = df.sort_values(by='Stage')

# Save to CSV
df.to_csv("policies.csv", index=False)

print("CSV file 'policies.csv' has been created.")
