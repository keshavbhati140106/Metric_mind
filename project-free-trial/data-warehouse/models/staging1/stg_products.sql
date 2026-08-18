WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_dim_products') }}
)
SELECT
    product_id,
    product_name,
    CAST(monthly_price AS NUMBER) AS monthly_price,
    billing_cycle
FROM source