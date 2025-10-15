"""
Diagnostic script to check Supabase connection and available tables.
"""
import os
from supabase import create_client

# Set your credentials
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ozusfgnnzanaxpcfidbm.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'sb_publishable_PyVKM3BdygFWVdeZrirAVA_AxZFyNAA')

print("=" * 60)
print("SUPABASE DIAGNOSTIC TOOL")
print("=" * 60)

try:
    # Connect to Supabase
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Successfully connected to Supabase")
    print(f"  URL: {SUPABASE_URL}")
    print()
    
    # Try different possible table names
    possible_table_names = [
        'FR2000 Annual Quant Data',
        'All',
        'market_data',
        'fr2000_annual_quant_data',  # snake_case version
        'all',  # lowercase
    ]
    
    print("Testing possible table names:")
    print("-" * 60)
    
    for table_name in possible_table_names:
        try:
            print(f"\nTrying table: '{table_name}'")
            response = client.table(table_name).select("*").limit(1).execute()
            
            if response.data:
                print(f"  ✓ SUCCESS! Found data in '{table_name}'")
                print(f"  Columns: {list(response.data[0].keys())}")
                print(f"  Sample row count: {len(response.data)}")
                
                # Get total count
                count_response = client.table(table_name).select("*", count='exact').limit(0).execute()
                print(f"  Total rows: {count_response.count}")
            else:
                print(f"  ⚠ Table exists but is EMPTY")
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("RECOMMENDATION:")
    print("Use the table name that showed '✓ SUCCESS!' above")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ Failed to connect to Supabase: {e}")
    print("\nPlease check:")
    print("1. SUPABASE_URL is correct")
    print("2. SUPABASE_KEY is correct")
    print("3. Your internet connection")
