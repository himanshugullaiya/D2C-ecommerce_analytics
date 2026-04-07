
DROP MATERIALIZED VIEW IF EXISTS gold.returns_analysis;

CREATE MATERIALIZED VIEW gold.returns_analysis AS (

WITH base_metrics AS (
    SELECT
        date_trunc('month', o.order_date) AS for_sorting,
        
        to_char(o.order_date, 'FMMonth YYYY') AS month_year,
        
        p.category, p.subcategory, p.brand, p.product_name,
        
        ar.return_reason,
        
        COUNT(DISTINCT ar.return_id) AS total_returns,
        
        SUM(ar.return_amount) AS total_return_value,
        
        AVG(ar.return_amount) AS avg_return_value
        
        --COUNT(DISTINCT o.order_id) AS total_orders,
        
        --COUNT(DISTINCT ar.return_id) * 1.0 / NULLIF(COUNT(DISTINCT o.order_id), 0) AS return_rate_pct_decimal
        
    FROM silver.orders o
    LEFT JOIN silver.all_returns ar ON o.order_id = ar.order_id
    LEFT JOIN silver.order_items oi ON oi.order_id = o.order_id
    LEFT JOIN silver.products p ON p.product_id = oi.product_id
    WHERE o.order_status = 'Returned'
    GROUP BY 1,2,3,4,5,6,7
),

with_window_funcs AS (
    SELECT *,
        LAG(total_returns) OVER (PARTITION BY product_name ORDER BY for_sorting) AS prevm_total_returns
       -- AVG(return_rate_pct_decimal) OVER (PARTITION BY category) AS category_avg_return_rate
    FROM base_metrics
),

with_flags AS (
    SELECT *,
        (total_returns - prevm_total_returns) * 1.00 / NULLIF(prevm_total_returns, 0) AS mom_return_change
    FROM with_window_funcs
)

SELECT *,

/*
    CASE 
	    WHEN return_rate_pct_decimal > category_avg_return_rate * 1.1 THEN 'High Risk' 
	    ELSE 'Normal'
    END AS return_risk_flag,
*/
    CASE 
	    WHEN mom_return_change > 0 THEN 'Worsening' 
	    ELSE 'Stable' 
    END AS worsening_flag


FROM with_flags
);

REFRESH MATERIALIZED VIEW gold.returns_analysis;

SELECT * FROM gold.returns_analysis;



