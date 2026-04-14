------------------Execute KPIs--------

DROP MATERIALIZED VIEW IF EXISTS gold.executive_kpis cascade;

CREATE MATERIALIZED VIEW gold.executive_kpis AS (

WITH total AS (
    SELECT
        date_trunc('month', o.order_date)::date AS for_sorting,
        to_char(o.order_date, 'FMMonth YYYY') AS year_month,
        sum(oi.total_sales_curr_order) AS total_revenue,
        count(DISTINCT o.order_id) AS total_orders,
        count(DISTINCT o.customer_id) AS total_customers,
        sum(o.net_amount) / count(DISTINCT o.order_id) AS AOV,
        (sum(oi.total_sales_curr_order) - sum(oi.qty * p.cost_price)) / NULLIF(sum(oi.total_sales_curr_order),0) AS profit_margin_pct_decimal,
        count(DISTINCT ar.return_id)*1.0 / NULLIF(count(DISTINCT o.order_id),0) AS return_rate_pct_decimal,
        COUNT(DISTINCT co.order_id) * 1.0 / NULLIF(COUNT(DISTINCT o.order_id), 0) AS cancelled_order_rate_decimal

        FROM silver.order_items oi
        JOIN silver.orders o ON o.order_id = oi.order_id
        JOIN silver.products p ON p.product_id = oi.product_id
        LEFT JOIN silver.all_returns ar ON ar.order_id = o.order_id
        LEFT JOIN (SELECT order_id FROM silver.orders WHERE order_status = 'Cancelled') co ON co.order_id = o.order_id
    GROUP BY 1,2
)

SELECT * FROM total
);

REFRESH MATERIALIZED VIEW gold.executive_kpis;

