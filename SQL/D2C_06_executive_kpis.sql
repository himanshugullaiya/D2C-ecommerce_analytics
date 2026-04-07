SELECT * FROM silver.orders LIMIT 5;
SELECT * FROM silver.order_items LIMIT 5;
SELECT * FROM silver.products LIMIT 5;
SELECT * FROM silver.orders LIMIT 5;


SELECT 
	sum(o.net_amount) AS total_revenue,
	count(DISTINCT o.order_id) AS total_orders,
	count(DISTINCT o.customer_id) AS total_customers,
	sum(o.net_amount) / count(DISTINCT o.order_id) AS AOV,
	sum(o.net_amount) - sum(oi.qty)


	
SELECT * FROM silver.order_items oi LEFT JOIN orders o ON oi.order_id = o.order_id;