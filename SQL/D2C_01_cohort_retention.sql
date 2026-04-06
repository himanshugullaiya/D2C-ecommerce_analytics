----------Cohort Analysis----------------------------------------####

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

SELECT *
FROM cohort_monthly_retention

);

REFRESH MATERIALIZED VIEW gold.cohort_retention;

SELECT * FROM gold.cohort_retention;

---------------------------------------------------------------#

----------------RFM Query--------------------------------------#

CREATE MATERIALIZED VIEW gold.rfm_segmentation AS (

WITH base_values AS (
	SELECT 
		customer_id,
		
		age((SELECT max(order_date) FROM silver.orders), max(order_date)) AS recency,    --This or current_date use anything
		count(order_id) AS frequency,
		sum(net_amount) AS monetary_value
	FROM silver.orders
	GROUP BY customer_id
),

ratings AS (
	SELECT *,
		NTILE(5) OVER (ORDER BY recency desc) AS r_rating,
		NTILE(5) OVER (ORDER BY frequency) AS f_rating,
		NTILE(5) OVER (ORDER BY monetary_value) AS m_rating
	FROM base_values
),

segments AS (
	SELECT *,
	CASE 
	    WHEN r_rating >= 4 AND f_rating >= 4 AND m_rating >= 4 THEN 'Champion'
	    WHEN r_rating >= 4 AND f_rating = 1                    THEN 'New Customer'
	    WHEN r_rating >= 3 AND f_rating >= 3                   THEN 'Loyal'
	    WHEN r_rating >= 3 AND f_rating < 3                    THEN 'Promising'
	    WHEN r_rating < 3  AND f_rating >= 3 AND m_rating >= 3 THEN 'At Risk'
	    WHEN r_rating < 3  AND f_rating >= 3 AND m_rating < 3  THEN 'Needs Attention'
	    WHEN r_rating < 3  AND f_rating < 3                    THEN 'Lost'
	    ELSE 'Uncategorized'	
	END AS segments
	FROM ratings
)

SELECT *,
CASE
	    WHEN segments = 'Champion'     THEN 'Reward & Retain — loyalty program, early access'
	    WHEN segments = 'Loyal'        THEN 'Upsell & Cross-sell — premium products, bundles'
	    WHEN segments = 'Promising'    THEN 'Nurture — onboarding emails, first repeat discount'
	    WHEN segments = 'New Customer' THEN 'Engage — welcome series, guide to products'
	    WHEN segments = 'At Risk'      THEN 'Win Back — urgent re-engagement campaign'
	    WHEN segments = 'Needs Attention' THEN 'Reactivate — targeted offer, feedback survey'
	    WHEN segments = 'Lost'         THEN 'Deprioritize — minimal spend, sunset campaign'
	    ELSE 'Review Manually'
END AS action_to_take
FROM segments
);

REFRESH MATERIALIZED VIEW rfm_segmentation;

SELECT * FROM rfm_segmentation WHERE segments = 'Champion';
