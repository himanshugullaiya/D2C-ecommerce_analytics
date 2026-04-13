--------------CREATE ALL VIEWS------

DROP VIEW gold.v_cohort_retention CASCADE;
DROP VIEW gold.v_rfm_segmentation CASCADE;
DROP VIEW gold.v_product_performance CASCADE;
DROP VIEW gold.v_revenue_monthly CASCADE;
DROP VIEW gold.v_returns_analysis CASCADE;
DROP VIEW gold.v_executive_kpis CASCADE;



CREATE VIEW gold.v_cohort_retention AS SELECT * FROM gold.cohort_retention;
CREATE VIEW gold.v_rfm_segmentation AS SELECT * FROM gold.rfm_segmentation;
CREATE VIEW gold.v_product_performance AS SELECT * FROM gold.product_performance;
CREATE VIEW gold.v_revenue_monthly AS SELECT * FROM gold.revenue_monthly;
CREATE VIEW gold.v_returns_analysis AS SELECT * FROM gold.returns_analysis;
CREATE VIEW gold.v_executive_kpis AS SELECT * FROM gold.executive_kpis;

---------------------------------------




