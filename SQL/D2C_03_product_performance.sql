-----------PRODUCT  PERFORMANCE------------##

DROP MATERIALIZED VIEW IF EXISTS gold.product_performance ;

CREATE MATERIALIZED VIEW gold.product_performance AS (

WITH base_metrics AS (
	SELECT 
		p.category, p.subcategory, p.product_name, p.brand, 
		
		sum(oi.total_sales_curr_order) AS total_revenue,
		
		count(DISTINCT o.order_id) AS total_orders,
		
		sum(oi.qty) AS total_qty,
		
		sum(oi.qty * p.cost_price) AS total_cost,
		
		sum(oi.qty * (p.unit_price - p.cost_price)) AS total_profit,
		
		(sum(oi.total_sales_curr_order) - sum(oi.qty * p.cost_price))*1.0/ NULLIF(sum(oi.total_sales_curr_order), 0)  AS profit_margin_pct_decimal,-- total_sales - total_cost / total_sales
		 
		count(DISTINCT ar.return_id) * 1.0/ NULLIF(count(DISTINCT o.order_id),0) AS return_rate_pct_decimal,
		
		rank() OVER (PARTITION BY p.category ORDER BY sum(oi.total_sales_curr_order)) AS revenue_rank_in_category
	
	
	FROM silver.order_items oi 
	JOIN silver.orders o   ON oi.order_id = o.order_id
	RIGHT JOIN silver.products p ON p.product_id= oi.product_id
	LEFT  JOIN silver.all_returns ar ON ar.order_id = o.order_id
	GROUP BY 1,2,3,4
	)

SELECT *,
AVG(return_rate_pct_decimal) OVER (PARTITION BY category) AS category_avg_return_rate,
CASE 
    WHEN return_rate_pct_decimal > AVG(return_rate_pct_decimal) OVER (PARTITION BY category) * 1.1
    THEN 'High Risk'
    ELSE 'Normal'
END AS return_risk_flag
FROM base_metrics
);

REFRESH MATERIALIZED VIEW gold.product_performance;

SELECT * FROM gold.product_performance;




