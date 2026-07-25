{{ config(materialized='table') }}

with raw_telemetry as (
    -- Simulating raw event ingestion for the streaming MVP
    select 
        uuid() as event_id,
        uuid() as session_id,
        round(random() * 30 + 5, 2) as playback_duration_seconds,
        current_timestamp as event_timestamp
    from generate_series(1, 100)
)

select
    event_id,
    session_id,
    playback_duration_seconds,
    event_timestamp
from raw_telemetry