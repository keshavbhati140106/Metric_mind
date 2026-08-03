WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_fact_transactions') }}
)
SELECT
    transaction_id,
    customer_id,
    product_id,
    CAST(transaction_date AS DATE) AS transaction_date,
    CAST(amount AS FLOAT) AS amount,
    currency,
    status
FROM source