# Store Analytics Dashboard (RetailIQ)

RetailIQ is a high-performance Streamlit intelligence dashboard built for multi-page retail store analytics, handling 740,000+ transaction rows effortlessly.

---

## 1. Quick Start

### Prerequisites
- Python 3.10+
- Pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/soulanalytic101/Analytics.git
   cd Analytics
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App Locally
1. Configure your `.env` file (see [Environment Variables](#environment-variables) below).
2. Run the Streamlit server:
   ```bash
   streamlit run dashboard.py
   ```

---

## 2. Environment Variables

Create a `.env` file in the root directory:
```env
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-supabase-service-role-key"
```

> [!IMPORTANT]
> The project uses **Row-Level Security (RLS)** in Supabase. You must use the **Service Role Key** (starts with `eyJ...`) in your deployed secrets and local `.env` to bypass RLS and allow uploads to succeed.

---

## 3. Database Optimizations & View Setup

For sub-second performance across 740k+ records, we utilize **PostgreSQL Materialized Views** and brand-level indexes. Run the following SQL queries in your Supabase SQL Editor:

```sql
-- 1. Create the base table (if not exists)
CREATE TABLE IF NOT EXISTS sales_data (
    id BIGSERIAL PRIMARY KEY,
    new_date DATE,
    month TEXT,
    bill_no TEXT,
    store_name_report TEXT,
    name TEXT,
    store_code TEXT,
    brand TEXT,
    report_status TEXT,
    store_status TEXT,
    type TEXT,
    zone TEXT,
    city TEXT,
    state TEXT,
    distributor_name TEXT,
    asm_rsm TEXT,
    new_ean_code TEXT,
    main_category TEXT,
    item_name TEXT,
    category TEXT,
    shade TEXT,
    size TEXT,
    season TEXT,
    mrp NUMERIC,
    fit TEXT,
    print_type TEXT,
    clsng_qty INTEGER,
    clsng_value NUMERIC,
    qty_sale INTEGER,
    net_sale_value NUMERIC,
    discount_value NUMERIC,
    mrp_sale_value NUMERIC,
    f_year TEXT,

    UNIQUE (brand, bill_no, new_ean_code)
);

-- 2. Create Materialized View for Monthly Sales
CREATE MATERIALIZED VIEW v_monthly_sales AS
SELECT 
    brand, f_year, month, 
    (f_year || ' ' || month) AS f_year_month,
    zone, state, city, main_category,
    SUM(qty_sale)       AS total_qty,
    SUM(net_sale_value) AS total_net_sales,
    SUM(mrp_sale_value) AS total_mrp_sales,
    SUM(discount_value) AS total_discount
FROM sales_data
GROUP BY brand, f_year, month, zone, state, city, main_category;

-- 3. Create Materialized View for Store Performance
CREATE MATERIALIZED VIEW v_store_performance AS
SELECT 
    brand, store_code, name, city, state, zone,
    SUM(qty_sale)       AS total_qty,
    SUM(net_sale_value) AS total_net_sales,
    SUM(discount_value) AS total_discount
FROM sales_data
GROUP BY brand, store_code, name, city, state, zone;

-- 4. Create Indexes on the Materialized Views for instant brand filters
CREATE INDEX idx_mv_monthly_brand ON v_monthly_sales(brand);
CREATE INDEX idx_mv_store_brand ON v_store_performance(brand);

-- 5. Create Helper function to refresh views after new uploads
CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW v_monthly_sales;
    REFRESH MATERIALIZED VIEW v_store_performance;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## 4. Key Performance Optimizations Built

1. **Materialized View Aggregation**: Computations (`SUM`, `GROUP BY`) are calculated database-side in PostgreSQL and stored on-disk. The dashboard reads the pre-cached results instantly instead of downloading raw logs.
2. **Selective Column Ingestion (Granular Fetching)**: Subpages (Product, Size, and Color Intelligence) query `sales_data` but only select the specific columns required for their charts. This leverages PostgreSQL indexing and reduces network overhead by 80%.
3. **Optimized Upload Pipeline**: Upload chunks are batched into packages of `1,000` to fit under Supabase's statement execution limit. Columns are cast to Pandas `Int64` nullable integer format to match the database constraints and prevent casting conflicts.
4. **Interactive Ingestion Indicator**: Shows live upload speed (`rows/sec`) and percentage completion in real-time.
