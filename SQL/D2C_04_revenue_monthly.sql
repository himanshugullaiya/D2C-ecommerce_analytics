
DROP MATERIALIZED VIEW IF EXISTS gold.revenue_monthly cascade;

CREATE MATERIALIZED VIEW gold.revenue_monthly AS (
	WITH base_metrics AS (
		SELECT 
		to_char(o.order_date, 'FMMonth YYYY') AS month_year,
		sum(oi.total_sales_curr_order) AS total_revenue,
		sum(oi.qty * (p.unit_price - p.cost_price)) AS total_profit,
		date_trunc('month', o.order_date) AS for_sorting,
		count(DISTINCT o.order_id) AS total_orders,
		count(DISTINCT o.customer_id) AS total_customers
		FROM silver.order_items oi 
		JOIN silver.orders o ON oi.order_id = o.order_id
		JOIN silver.products p ON oi.product_id = p.product_id
		GROUP BY date_trunc('month', o.order_date),1
		ORDER BY date_trunc('month', o.order_date)
	),
	
	comparison_parts AS (
		SELECT *,
		lag(total_revenue,1)  OVER (ORDER BY for_sorting) AS prevm_revenue,
		lag(total_orders, 1)  OVER (ORDER BY for_sorting) AS prevm_orders	
		FROM base_metrics
	
	)
	
	SELECT month_year,
		total_revenue,
		total_orders,
		total_customers,
		for_sorting,
		(total_revenue - prevm_revenue)*1.0 / NULLIF(prevm_revenue,0) AS mom_revenue_change_pct_decimal,
		(total_orders - prevm_orders)*1.0 / NULLIF(prevm_orders,0) AS mom_orders_change_pct_decimal
	FROM comparison_parts
);

REFRESH MATERIALIZED VIEW gold.revenue_monthly;

SELECT * FROM gold.revenue_monthly;

	
