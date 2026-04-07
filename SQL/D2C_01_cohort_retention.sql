----------Cohort Analysis----------------------------------------####
DROP MATERIALIZED VIEW IF EXISTS gold.cohort_retention;

CREATE MATERIALIZED VIEW gold.cohort_retention AS (

WITH foc AS (          --first order month  customer-wise
	SELECT customer_id, 
	date_trunc('month', min(order_date))::date AS cohort_month
	FROM silver.orders
	GROUP BY 1
),

customer_cohort AS (   --join cohort month to the orders table on customer_id and find the month difference from cohort
	SELECT cohort_month, foc.customer_id ,
	extract(YEAR FROM age(order_date, cohort_month))*12 + extract(MONTH FROM age(order_date, cohort_month)) AS total_months_from_cohort
	FROM silver.orders JOIN foc ON silver.orders.customer_id = foc.customer_id
),

cohort_size AS (   --- Size of M0
	SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_size
	FROM customer_cohort
	WHERE total_months_from_cohort = 0
	GROUP BY 1
),

cohort_monthly_retention AS (  
	SELECT cc.cohort_month, total_months_from_cohort, COUNT(DISTINCT customer_id) AS block_count, cs.cohort_size
	FROM customer_cohort cc JOIN cohort_size cs ON cc.cohort_month = cs.cohort_month
	GROUP BY 1, 2,4
	ORDER BY 1, 2,4
	)

SELECT *, block_count*1.0/cohort_size AS retention_pct_decimal
FROM cohort_monthly_retention

);

REFRESH MATERIALIZED VIEW gold.cohort_retention;

SELECT * FROM gold.cohort_retention;

---------------------------------------------------------------#


