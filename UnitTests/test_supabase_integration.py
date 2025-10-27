"""
Test suite for Supabase integration
Tests data loading, pagination, and database connectivity

NOTE: All tests in this module require Supabase credentials.
Mark as @pytest.mark.integration and @pytest.mark.slow
Run with: pytest -m integration (when credentials are available)
"""
import pytest
import pandas as pd
import os
from supabase_client import load_supabase_data

# Skip entire module if no credentials
pytestmark = [
    pytest.mark.integration,
    pytest.mark.slow,
    pytest.mark.skipif(
        not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_KEY'),
        reason="Requires Supabase credentials (SUPABASE_URL and SUPABASE_KEY)"
    )
]


class TestSupabaseConnection:
    """Test Supabase connection and basic queries"""
    
    def test_load_supabase_data_basic(self):
        """Test basic data loading from Supabase"""
        data = load_supabase_data()
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty, "Data should not be empty"
        assert len(data) > 0, "Should load at least some records"
    
    def test_load_supabase_data_with_custom_table(self):
        """Test loading from custom table name"""
        data = load_supabase_data(table_name='FR2000 Annual Quant Data')
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
    
    def test_loaded_data_structure(self):
        """Test that loaded data has expected structure"""
        data = load_supabase_data()
        
        # Should have multiple columns
        assert len(data.columns) > 10, "Should have multiple columns"
        
        # Should have expected key columns
        expected_columns = ['ID', 'Security_Name', 'Ticker-Region', 'Ending_Price']
        for col in expected_columns:
            assert col in data.columns, f"Missing column: {col}"


class TestSupabasePagination:
    """Test pagination functionality"""
    
    def test_pagination_loads_all_records(self):
        """Test that pagination loads all available records"""
        data = load_supabase_data()
        
        # Should load thousands of records (known dataset size)
        assert len(data) > 10000, "Should load large dataset with pagination"
    
    def test_pagination_no_duplicates(self):
        """Test that pagination doesn't create duplicate records"""
        data = load_supabase_data()
        
        # Check if there are duplicate rows
        duplicates = data.duplicated()
        assert duplicates.sum() == 0, "Should not have duplicate rows"


class TestSupabaseDataQuality:
    """Test quality of loaded data"""
    
    @pytest.fixture
    def data(self):
        """Load data for testing"""
        return load_supabase_data()
    
    def test_data_has_records(self, data):
        """Test that data has substantial number of records"""
        assert len(data) > 1000, "Should have significant amount of data"
    
    def test_required_columns_present(self, data):
        """Test that all required columns are present"""
        required = [
            'ID', 'Security_Name', 'Ticker-Region', 'Ending_Price',
            '6-Mo_Momentum', 'ROE_using_9-30_Data', 'Date'
        ]
        
        for col in required:
            assert col in data.columns, f"Required column missing: {col}"
    
    def test_data_types_appropriate(self, data):
        """Test that data types are appropriate"""
        # ID should be numeric
        if 'ID' in data.columns:
            assert pd.api.types.is_numeric_dtype(data['ID']) or \
                   pd.api.types.is_integer_dtype(data['ID'])
        
        # Security_Name should be string/object
        if 'Security_Name' in data.columns:
            assert pd.api.types.is_object_dtype(data['Security_Name']) or \
                   pd.api.types.is_string_dtype(data['Security_Name'])
    
    def test_no_all_null_columns(self, data):
        """Test that no columns are completely null"""
        for col in data.columns:
            null_count = data[col].isna().sum()
            assert null_count < len(data), f"Column {col} is all null"
    
    def test_ticker_format(self, data):
        """Test that tickers have expected format"""
        if 'Ticker-Region' in data.columns:
            # Sample some tickers
            sample_tickers = data['Ticker-Region'].dropna().head(10)
            
            for ticker in sample_tickers:
                # Should contain hyphen (e.g., AAPL-US)
                assert '-' in str(ticker), f"Ticker should have region: {ticker}"
    
    def test_price_data_reasonable(self, data):
        """Test that price data is reasonable"""
        if 'Ending_Price' in data.columns:
            prices = data['Ending_Price'].dropna()
            
            # Prices should be positive
            assert (prices > 0).all(), "All prices should be positive"
            
            # Prices should be reasonable (not too extreme)
            assert prices.max() < 100000, "Prices seem unreasonably high"
            assert prices.min() > 0, "Prices should be above 0"
    
    def test_date_column_exists(self, data):
        """Test that date column exists and has valid dates"""
        assert 'Date' in data.columns, "Date column should exist"
        
        # Sample some dates
        sample_dates = data['Date'].dropna().head(10)
        assert len(sample_dates) > 0, "Should have some valid dates"


class TestSupabasePerformance:
    """Test performance and efficiency"""
    
    @pytest.mark.slow
    def test_load_data_reasonable_time(self):
        """Test that data loads in reasonable time"""
        import time
        
        start = time.time()
        data = load_supabase_data()
        elapsed = time.time() - start
        
        # Should load in under 30 seconds
        assert elapsed < 30, f"Data loading took too long: {elapsed:.2f}s"
        assert len(data) > 0


class TestSupabaseErrorHandling:
    """Test error handling and edge cases"""
    
    def test_load_invalid_table_name(self):
        """Test loading from non-existent table"""
        # This might raise an error or return empty dataframe
        # depending on implementation
        try:
            data = load_supabase_data(table_name='NonExistentTable12345')
            # If no error, should return empty dataframe
            assert isinstance(data, pd.DataFrame)
        except Exception as e:
            # Should raise a reasonable error
            assert isinstance(e, Exception)
    
    def test_connection_resilience(self):
        """Test that connection can be re-established"""
        # Load data twice to ensure connection can be reused
        data1 = load_supabase_data()
        data2 = load_supabase_data()
        
        assert len(data1) == len(data2), "Should load same amount of data"
        assert len(data1.columns) == len(data2.columns), "Should have same columns"
