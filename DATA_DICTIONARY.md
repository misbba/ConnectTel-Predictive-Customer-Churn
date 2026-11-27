# Data dictionary
CSV headers and representative values are shown below. IDs are join keys, not predictive features. Numeric zeros are observed zero, not missing data. Dates are ISO format; currency is fictional USD. Multi-value fields use |.

## customers
- `customer_id`: e.g. `C001`
- `snapshot_date`: e.g. `2025-01-01`
- `tenure_months`: e.g. `48`
- `contract`: e.g. `two_year`
- `internet_service`: e.g. `none`
- `monthly_charges_usd`: e.g. `45`
- `total_charges_usd`: e.g. `2215.59`
- `security_service`: e.g. `1`
- `streaming_service`: e.g. `0`
- `failed_payments_90d`: e.g. `2`
- `churn_30d`: e.g. `0`
- `split`: e.g. `train`

See README for target, units, split and leakage rules.
