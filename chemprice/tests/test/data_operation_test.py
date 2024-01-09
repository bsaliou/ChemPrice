import unittest
import pandas as pd
import math
import os
import sys
import numpy as np
from .. import Utils

# Add path
sys.path.insert(0, os.path.abspath('..'))
from chemprice import utils




# Function to compare two floats with specified significant digits
def significant_digits(number, n):
    return round(number, n - int(math.floor(math.log10(abs(number)))) - 1)




class TestMergeDataframes(unittest.TestCase):




    def test_single_min_price(self):
        """
        Test if the price csv have only one price for each molecules
        """
        # Input csv from Chemspace and Molport
        df1 = Utils.load_data('chemspace_prices_test')
        df2 = Utils.load_data('molport_prices_test')
        
        # Expected result
        expected_result = Utils.load_data('merged_prices_test')
        expected_result = expected_result.astype(str)
        expected_result.replace("nan", np.nan, inplace=True)
        
        # Function application
        result = utils.merge_dataframes([df1, df2]) 
        result.replace("nan", np.nan, inplace=True) 
        
        # Check the result
        pd.testing.assert_frame_equal(expected_result, result)
        
        


class TestExtractUnitBulk(unittest.TestCase):




    def test_good_extraction_for_conventional_unit(self):
        """
        Test for conventional units to be ignored 
        """  
        unit_string = "kg"
    
        result_bulk, result_unit = utils.extract_unit_bulk(unit_string)
        
        # check the result
        self.assertEqual(result_bulk, None)
        self.assertEqual(result_unit, None)
        
        
        
        
    def test_good_extraction_unit(self):
        """
        Test the good extraction of unit with the format (int x int unit)
        """
        unit_string = "10x25mL"
    
        result_bulk, result_unit = utils.extract_unit_bulk(unit_string)
        
        # check the result
        self.assertEqual(result_bulk, 250)
        self.assertEqual(result_unit, "ml")




class TestAddStandardizedColumns(unittest.TestCase):
        
        
        
        
    def test_good_price_result(self):
        """
        Test if the calcul of price is good
        """
        # Create a test DataFrame with input data
        test_df = pd.DataFrame({'Input SMILES': ["test"], 'Measure': ["mg"], 'Amount': [30], 'Price_USD': [600]})
        
        # Function application
        result_data = utils.add_standardized_columns(test_df)  
        price_per_gram = result_data.at[0, 'USD/g']
        
        # Expected result
        expected_result = significant_digits(20000.0, 5)

        # Assertion to check if the result dataframes are good
        self.assertEqual(expected_result, significant_digits(price_per_gram,5))
        
    
    
    
    def test_good_price_result2(self):
        """
        Test if the calcul of price is good with a difficult unit
        """
        # Create a test DataFrame with input data
        test_df = pd.DataFrame({'Input SMILES': ["test"], 'Measure': ["30x15mL"], 'Amount': [30], 'Price_USD': [600]})
        
        # Function application
        result_data = utils.add_standardized_columns(test_df)  
        price_per_liter = result_data.at[0, 'USD/l']
        
        # Expected result
        expected_result = significant_digits(44.444444444, 5)

        # Assertion to check if the result dataframes are good
        self.assertEqual(expected_result, significant_digits(price_per_liter,5))




class TestFilterCsvByMinPrice(unittest.TestCase):

    


    def test_all_min_price(self):
        """
        Test if all the best prices are kept
        """
        # Function application
        df = Utils.load_data('test_data')        
        result = utils.filter_csv_by_min_price(df)  
        
        # Expected result
        expected_result = Utils.load_data('best_prices')
        
        # Reset DataFrame indexes before comparing
        result.reset_index(drop=True, inplace=True)
        
        # Check the result
        pd.testing.assert_frame_equal(expected_result, result)
        
    
    
    
    def test_single_min_price(self):
        """
        Test if the price csv have only one price for each molecules
        """
        # Function application
        df = Utils.load_data('best_prices')
        result = utils.filter_csv_by_min_price(df)  
        
        # Count the number of different SMILES with a given price
        n_min_price = result.loc[result['USD/g'].notnull(), 'Input SMILES'].nunique()

        # Check there is only one best price
        self.assertLessEqual(n_min_price, 1)
        
        
        

if __name__ == '__main__':
    unittest.main()
    
    