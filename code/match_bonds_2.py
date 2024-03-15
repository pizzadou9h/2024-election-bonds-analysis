import pandas as pd
from datetime import datetime, timedelta

# Read the CSV files
df_company = pd.read_csv('e-bonds_company.csv')
df_party = pd.read_csv('e-bonds_party.csv')

# Convert the 'Date' column to datetime type
df_company['Date'] = pd.to_datetime(df_company['Date'], format='%d/%b/%Y')
df_party['Date'] = pd.to_datetime(df_party['Date'], format='%d/%b/%Y')

# Initialize an empty list to store the matched data
matched_data = []

# Iterate over each row in the party DataFrame
for _, row_party in df_party.iterrows():
    redemption_date = row_party['Date']
    political_party = row_party['Name of the Political Party']
    redemption_amount = row_party['Denomination']
    
    # Find the matching purchases within 14 days
    mask = (df_company['Date'] >= redemption_date - timedelta(days=14)) & (df_company['Date'] <= redemption_date)
    matching_purchases = df_company.loc[mask]
    
    # Iterate over each matching purchase
    for _, row_company in matching_purchases.iterrows():
        purchase_date = row_company['Date']
        purchaser_name = row_company['Purchaser Name']
        purchase_amount = row_company['Denomination']
        
        # Check if the redemption amount matches the purchase amount
        if redemption_amount == purchase_amount:
            matched_data.append([purchase_date, purchaser_name, political_party, purchase_amount, redemption_date])
            df_company.drop(row_company.name, inplace=True)  # Remove the matched purchase from df_company
            break  # Stop searching for more matches

# Create a DataFrame from the matched data
df_matched = pd.DataFrame(matched_data, columns=['Purchase Date', 'Purchaser Name', 'Political Party', 'Amount', 'Redemption Date'])

# Print the matched data
print("Matched Data:")
print(df_matched)

# Save the matched data to a new CSV file
df_matched.to_csv('matched_transactions_rev.csv', index=False)

# Print the unmatched purchases
unmatched_purchases = df_company[~df_company['Denomination'].isin(df_matched['Amount'])]
print("\nUnmatched Purchases:")
print(unmatched_purchases)

# Print the unmatched redemptions
unmatched_redemptions = df_party[~df_party['Denomination'].isin(df_matched['Amount'])]
print("\nUnmatched Redemptions:")
print(unmatched_redemptions)
