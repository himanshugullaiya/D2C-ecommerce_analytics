----------------RFM Query--------------------------------------#
DROP MATERIALIZED VIEW IF EXISTS gold.rfm_segmentation;

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
	
	SELECT 
		sg.customer_id,
		concat(c.first_name, ' ', c.last_name) AS customer_name,
		sg.recency,
		sg.frequency,
		sg.monetary_value,
		sg.r_rating,
		sg.f_rating,
		sg.m_rating,
		sg.segments,
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
	FROM segments sg JOIN silver.customers c ON sg.customer_id = c.customer_id
);

REFRESH MATERIALIZED VIEW gold.rfm_segmentation;

SELECT * FROM gold.rfm_segmentation;
