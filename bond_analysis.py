import PyPDF2
import pandas as pd
import io

def extract_data_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        data = []

        for page in reader.pages:
            text = page.extract_text()
            lines = text.split('\n')

            for line in lines:
                if line.startswith('Date of Purchase'):
                    continue
                values = line.split()
                if len(values) == 4:
                    date, purchaser_name, _, denomination = values
                    data.append([date, purchaser_name, float(denomination.replace(',', ''))])

    return data

def validate_data(data):
    df = pd.DataFrame(data, columns=['Date', 'Purchaser Name', 'Denomination'])
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        print("Missing values found:")
        print(missing_values)
    else:
        print("No missing values found.")
    
    # Check for duplicate entries
    duplicates = df.duplicated()
    if duplicates.any():
        print("Duplicate entries found:")
        print(df[duplicates])
    else:
        print("No duplicate entries found.")
    
    # Check for invalid denominations
    invalid_denominations = df[df['Denomination'] <= 0]
    if not invalid_denominations.empty:
        print("Invalid denominations found:")
        print(invalid_denominations)
    else:
        print("No invalid denominations found.")

# Usage
pdf_path = 'e-bonds_company.pdf'
data = extract_data_from_pdf(pdf_path)
validate_data(data)