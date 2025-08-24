import psycopg2

# Test direct connection
direct_url = "postgresql://postgres:Akogo66022.@db.zbeyhbmuqgdqdsccimtt.supabase.co:5432/postgres"

# Test pooled connection (get this from Transaction pooler tab)
# pooled_url = "postgresql://postgres.zbeyhbmuqgdqdsccimtt:Akogo66022.@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

print("Testing direct connection...")
try:
    conn = psycopg2.connect(direct_url)
    print("✅ Direct connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Direct connection failed: {e}")

# Uncomment and test pooled connection if direct failsimport psycopg2

# Test direct connection
direct_url = "postgresql://postgres:Akogo66022.@db.zbeyhbmuqgdqdsccimtt.supabase.co:5432/postgres"

# Test pooled connection (get this from Transaction pooler tab)
# pooled_url = "postgresql://postgres.zbeyhbmuqgdqdsccimtt:Akogo66022.@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

print("Testing direct connection...")
try:
    conn = psycopg2.connect(direct_url)
    print("✅ Direct connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Direct connection failed: {e}")

# Uncomment and test pooled connection if direct fails