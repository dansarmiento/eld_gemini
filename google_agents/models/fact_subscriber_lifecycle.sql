{{ config(materialized='table') }}

with subscriber_events as (
    -- Simulating lifecycle states for the streaming MVP
    select 
        uuid() as subscriber_id,
        case 
            when random() > 0.5 then 'Premium' 
            else 'Basic' 
        end as subscription_tier,
        case 
            when random() > 0.8 then 'Churned' 
            else 'Active' 
        end as lifecycle_status,
        current_date as last_updated
    from generate_series(1, 50)
)

select
    subscriber_id,
    subscription_tier,
    lifecycle_status,
    last_updated
from subscriber_events