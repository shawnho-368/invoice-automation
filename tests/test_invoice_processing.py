import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from process_invoices import proj_code, invoice_amt, vendor_name, text_date, number_date, date_cleaner, description

class InvoiceTestProcesssing(unittest.TestCase):

    def test_proj_code_standard(self):
        testcase = 'PROJ-001'
        result = proj_code(testcase)
        self.assertEqual(result, 'PRO-001')
    
    def test_proj_code_lowercase(self):
        testcase = 'proj-001'
        result = proj_code(testcase)
        self.assertEqual(result, 'PRO-001')
    
    def test_proj_code_shortened(self):
        testcase = 'p-001'
        result = proj_code(testcase)
        self.assertEqual(result, 'PRO-001')
    
    def test_proj_code_full(self):
        testcase = 'project-001'
        result = proj_code(testcase)
        self.assertEqual(result, 'PRO-001')
    
    def test_vendor_name_standard(self):
        testcase = 'John Smith Consulting'
        result = vendor_name(testcase)
        self.assertEqual(result, 'John Smith Consulting')
    
    def test_vendor_name_none(self):
        testcase = 'John smith consulting'
        result = vendor_name(testcase)
        self.assertEqual(result, None)
    
    def test_vendor_name_apostrophe(self):
        testcase = "John O'Brien Consulting"
        result = vendor_name(testcase)
        self.assertEqual(result, "John O'Brien Consulting")
    
    def test_vendor_name_period(self):
        testcase = 'John Smith Co.'
        result = vendor_name(testcase)
        self.assertEqual(result, 'John Smith Co.')
    
    def test_vendor_name_caps(self):
        testcase = 'John Smith LLC'
        result = vendor_name(testcase)
        self.assertEqual(result, 'John Smith LLC')
    
    def test_text_date_fullmonth(self):
        testcase = 'March 13, 2025'
        result = text_date(testcase)
        self.assertEqual(result, 'March 13, 2025')
    
    def test_text_date_ordinal(self):
        testcase = 'March 13th, 2025'
        result = text_date(testcase)
        self.assertEqual(result, 'March 13, 2025')
    
    def test_text_date_ordinal_two(self):
        testcase = 'March 21st, 2025'
        result = text_date(testcase)
        self.assertEqual(result, 'March 21, 2025')
    
    def test_text_date_ordinal_three(self):
        testcase = 'March 22nd, 2025'
        result = text_date(testcase)
        self.assertEqual(result, 'March 22, 2025')
    
    def test_text_date_ordinal_four(self):
        testcase = 'March 20th, 2025'
        result = text_date(testcase)
        self.assertEqual(result, 'March 20, 2025')
    
    def test_text_date_none(self):
        testcase = '3/20/25'
        result = text_date(testcase)
        self.assertEqual(result, None)

    def test_number_date_standard(self):
        testcase = '03-20-2025'
        result = number_date(testcase)
        self.assertEqual(result, 'March 20, 2025')
    
    def test_number_date_shortyear(self):
        testcase = '03-20-25'
        result = number_date(testcase)
        self.assertEqual(result, None)
    
    def test_number_date_shortmonth(self):
        testcase = '3-20-25'
        result = number_date(testcase)
        self.assertEqual(result, None)

    def test_number_date_mdy(self):
        testcase1 = '03/20/2025'
        result1 = number_date(testcase1)
        testcase2 = '03-20-2025'
        result2 = number_date(testcase2)
        self.assertEqual(result1, 'March 20, 2025')
        self.assertEqual(result2, 'March 20, 2025')
    
    def test_number_date_ymd(self):
        testcase1 = '2025/03/20'
        result1 = number_date(testcase1)
        testcase2 = '2025-03-20'
        result2 = number_date(testcase2)
        self.assertEqual(result1, 'March 20, 2025')
        self.assertEqual(result2, 'March 20, 2025')
    
    def test_number_date_dmy(self):
        testcase1 = '20/03/2025'
        result1 = number_date(testcase1)
        testcase2 = '20-03-2025'
        result2 = number_date(testcase2)
        self.assertEqual(result1, 'March 20, 2025')
        self.assertEqual(result2, 'March 20, 2025')

    def test_date_cleaner_standard_(self):
        testcase = 'March 1st, 2025'
        result = date_cleaner(testcase)
        self.assertEqual(result, 'March 1, 2025')
    
    def test_date_cleaner_singledigit(self):
        testcase = '03/01/2025'
        result = date_cleaner(testcase)
        self.assertEqual(result, 'March 1, 2025')
    
    def test_date_cleaner_doubledigit(self):
        testcase = '03/31/2025'
        result = date_cleaner(testcase)
        self.assertEqual(result, 'March 31, 2025')

    def test_description_standard(self):
        testcase = 'Doing stuff'
        result = description(testcase)
        self.assertEqual(result, 'Doing stuff')

    def test_description_standard_slash(self):
        testcase = 'UI/UX work'
        result = description(testcase)
        self.assertEqual(result, 'UI/UX work')

    def test_description_caps(self):
        testcase = 'John Smith Consulting'
        result = description(testcase)
        self.assertEqual(result, None)

if __name__ == "__main__":
    unittest.main()