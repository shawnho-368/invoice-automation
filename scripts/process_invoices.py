import csv
import os
import re
from datetime import datetime

def proj_code(line): 
    """
    Standardizes project codes to PRO-XXX format from various input patterns.
    Handles: PROJ-001, proj-002, P-001, project_004, PROJECT-002, etc.
    """
    if isinstance(line, str):
        line = [line]
    for text in line:
        # Match project codes: [P/p] + letters + [-/_] + 3 digits
        match = re.search(r'[Pp][a-zA-Z]*[-_](\d{3})', text)
        if match:
            return("PRO-{}".format(match[1]))
    
def invoice_amt(line): 
    """
    Extracts and formats currency amounts, handling split values across CSV columns.
    Combines fragments like "$1" + "450.00" into "$1,450.00"
    """
    if isinstance(line, str):
        line = [line]

    matches = []
    for i, text in enumerate(line):
        # Skip date-like patterns that contain dashes or slashes
        if '-' in line[i] or '/' in text:
            continue
        else:
            # Remove dollar signs and commas for processing
            clean = re.sub(r'[?,]', '', text)
            # Extract numeric amounts (with or without decimals)
            match = re.search(r'\d+\.\d{2}|\d+', clean)
            if match:
                matches.append(match.group(0))
    # Combine all numeric parts and format as currency
    final = ''.join(matches)
    return f'${float(final):,.2f}'

def vendor_name(line):
    """
    Extracts vendor names that follow business naming conventions.
    Expects capitalized words like "John Smith Consulting" or "Mike's Dev Shop"
    """
    if isinstance(line, str):
        line = [line]

    for text in line:
        # Match business names: Capital letter + words with apostrophes/periods
        match = re.search(r"[A-Z][a-z']+ ([A-Z][A-Za-z'.]+ ?)+", text)
        if match:
            return match.group(0)
        
def text_date(line):
    """
    Parses text-based dates like "March 15, 2024" or "Mar 15th, 2024"
    Returns standardized format: "March 15, 2024"
    """
    if isinstance(line, str):
        line = [line]

    for text in line:
        # Match month names + day + year patterns
        match = re.search(r'[A-Z][a-z]+ \d+([a-z]*)?, \d{4}', text)
        text_formats = ["%B %d, %Y", "%b %d, %Y"]  # Full and abbreviated month names
        if match:
            # Remove ordinal suffixes (st, nd, rd, th) from day numbers
            text_date_cleaned = re.sub(r'(\d+)(st|th|nd|rd)', r'\1', match.group(0))
            for fmt in text_formats:
                try:
                    date_obj = datetime.strptime(text_date_cleaned, fmt)
                    day = date_obj.day  # This gives you 1, not 01
                    month = date_obj.strftime("%B")
                    year = date_obj.year
                    return f"{month} {day}, {year}"
                except ValueError:
                    continue
            return None

def number_date(line):
    """
    Parses numeric dates in various formats: MM/DD/YYYY, YYYY-MM-DD, etc.
    Assumes US date format (MM/DD) when ambiguous
    """
    if isinstance(line, str):
        line = [line]

    for text in line:
        # Match various numeric date patterns
        match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{2,4})|(\d{2,4}[/-]\d{2}[/-]\d{2})', text)
        # Try multiple format interpretations, prioritizing US format
        num_formats = ['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%d-%m-%Y']
        if match:
            for fmt in num_formats:
                try:
                    date_obj = datetime.strptime(match.group(0), fmt)
                    day = date_obj.day
                    month = date_obj.strftime("%B")
                    year = date_obj.year  
                    return f"{month} {day}, {year}"
                except ValueError:
                    continue
            return None
    
def date_cleaner(line):
    """
    Attempts to parse dates using both text and numeric date functions.
    Returns the first successful match or None if no valid date found.
    """
    if isinstance(line, str):
        line = [line]

    for text in line:
        # Try text date parsing first (March 15, 2024)
        result = text_date(text)
        if result:
            return result
        # Fall back to numeric date parsing (03/15/2024)
        result = number_date(text)
        if result:
            return result
    return None

def description(line):
    """
    Extracts service descriptions that start with capital letter.
    Matches patterns like "Web development work" or "UI/UX design work"
    """
    if isinstance(line, str):
        line = [line]

    for text in line:
        # Match description patterns: Capital + mixed case words
        match = re.search(r'[A-Z][a-zA-Z-/]*(?: [a-z]+)+', text)
        if match:
            return match.group(0)

# Set up file paths relative to script location
script_dir = os.path.dirname(__file__)
input_dir = os.path.join(script_dir, '..', 'input')
file_path = os.path.join(input_dir, 'freelancer_invoices_raw.csv')

# Process CSV freelancer invoices
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    csv_cleaned = []
    
    for line in reader:
        record = {}
        # Extract and clean each field, using "MISSING" for failed extractions
        record['Vendor'] = vendor_name(line) or "MISSING"
        record['Amount'] = invoice_amt(line) or "MISSING"
        record['Date Processed'] = datetime.now().strftime("%B %d, %Y")  # Current date always succeeds
        record['Project Code'] = proj_code(line) or "MISSING"
        record['Description'] = description(line) or "MISSING"
        record['Original Date'] = date_cleaner(line) or "MISSING"
        csv_cleaned.append(record)

# Process TXT contractor payments file
input_dir = os.path.join(script_dir, '..', 'input')
file_path = os.path.join(input_dir, 'contractor_payments.txt')

with open(file_path, 'r') as file:
    txt_matches = []
    record = {}

    for line in file:
        # Handle record separators - save completed record and start fresh
        if '---' in line:
            if record:  # Only save if we've accumulated fields
                record['Date Processed'] = datetime.now().strftime("%B %d, %Y")
                record['Generated On'] = datetime.now().strftime("%B %d, %Y")
                txt_matches.append(record)
                record = {}  # Reset for next record
            continue

        # Skip header lines, empty lines, and lines without field labels
        if not line or '=' in line or ':' not in line:
            continue
        else:
            line = line.strip()
            # Extract value after colon and label
            cleaned_line = line.split(':', 1)[1].strip()
            
            # Parse different field types based on line prefix
            if line.startswith('Vendor: '):
                record['Vendor'] = vendor_name(cleaned_line) or "MISSING"
            elif line.startswith('Amount: '):
                record['Amount'] = invoice_amt(cleaned_line) or "MISSING"
            elif line.startswith('Project: '):
                record['Project Code'] = proj_code(cleaned_line) or "MISSING"
            elif line.startswith('Date: '):
                record['Original Date'] = date_cleaner(cleaned_line) or "MISSING"
            elif line.startswith('Description: '):
                record['Description'] = description(cleaned_line) or "MISSING"

    # Handle final record if file doesn't end with separator
    if record:
        record['Date Processed'] = datetime.now().strftime("%B %d, %Y")
        record['Generated On'] = datetime.now().strftime("%B %d, %Y")
        txt_matches.append(record)

# Generate output report
output_dir = os.path.join(script_dir, '..', 'output')
filename = f'invoice {datetime.now().strftime("%m.%d.%y")}.txt'
file_path = os.path.join(output_dir, filename)

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

with open(file_path, 'w') as file:
    # Write report header
    file.write('TECHSTART SOLUTIONS - STANDARDIZED INVOICE RECORD\n')
    file.write('================================================\n')

    # Combine all processed records from both file types
    all_records = csv_cleaned + txt_matches

    # Write each invoice record in standardized format
    for record in all_records:
        file.write(f'Vendor: {record["Vendor"]}\n')
        file.write(f'Amount: {record["Amount"]}\n')
        file.write(f'Date Processed: {record["Date Processed"]}\n')
        file.write(f'Project Code: {record["Project Code"]}\n')
        file.write(f'Original Date: {record["Original Date"]}\n')
        file.write(f'Description: {record["Description"]}\n')
        file.write(f'Status: Processed\n')  # Mark all records as processed for accounting
        file.write('\n')
        file.write('---\n')  # Separator between records
    
    # Add report generation timestamp
    file.write(f'Generated On {datetime.now().strftime("%B %d, %Y")}\n')