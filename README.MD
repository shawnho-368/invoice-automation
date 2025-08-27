# Invoice Processing Automation

Automates processing of freelancer invoices from CSV and TXT formats into standardized output for business accounting workflows.

## Business Problem

TechStart Solutions receives freelancer invoices in multiple formats via email attachments. The accounting team was spending 4-5 hours weekly manually processing these invoices to extract vendor information, standardize amounts, and generate reports. This automation reduces processing time to under 30 minutes while eliminating manual data entry errors.

## Features

- Cleans and standardizes invoice data from messy input formats
- Handles multiple date formats (text dates, numeric dates, ordinals)
- Processes both CSV and TXT input files
- Standardizes project codes and currency formatting
- Generates formatted reports with consistent structure
- Handles missing data with appropriate placeholders

## Project Structure

```
invoice-automation/
├── input/              # Sample input files
├── output/             # Generated reports (created automatically)
├── scripts/            # Main processing script
├── tests/              # Unit tests
└── README.md
```

## Requirements

- Python 3.x (no external dependencies required)

## Usage

1. Clone the repository
2. Ensure Python 3.x is installed
3. Run from the project root directory:

```bash
python scripts/process_invoices.py
```

The script will process all input files and generate a timestamped report in the `output/` directory.

## Input vs Output Example

**Input (messy data):**
```
"Jennifer Wu LLC",$1,450.00,"Mar 22, 2024","P-001","Content writing services"
```

**Output (standardized):**
```
Vendor: Jennifer Wu LLC
Amount: $1,450.00
Date Processed: August 25, 2025
Project Code: PRO-001
Original Date: March 22, 2024
Description: Content writing services
Status: Processed
```

## Testing

Run the unit test suite:

```bash
python tests/test_invoice_processing.py
```
Tests cover individual data cleaning functions including project code standardization, amount formatting, and date parsing.

## Data Processing

The automation handles common data quality issues:
- Split currency amounts (e.g., "$1" and "450.00" in separate columns)
- Inconsistent date formats across multiple standards
- Mixed case and formatting in project codes
- Missing or malformed data fields

Generated reports include processing timestamps and data quality indicators for audit purposes.# invoice-automation
