WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_dim_customers') }}
)
SELECT
    customer_id,
    company_name,
    industry,
    region,
    tier,
    CAST(signup_date AS DATE) AS signup_date
FROM source