with raw_data as (
    select * from {{ source('public', 'doctorset') }}
    union all
    select * from {{ source('public', 'lobelia4cosmetics') }}
    union all
    select * from {{ source('public', 'yetenaweg') }}
    union all
    select * from {{ source('public', 'eahci') }}
    union all
    select * from {{ source('public', 'chemed') }}
),
deduplicated as (
    select 
        *,
        row_number() over (partition by channel_title order by date) as rn_channel,
        row_number() over (partition by message_id order by date) as rn_message
    from raw_data
)
select
    "channel_title",
    "channel_username",
    "message_id",
    case 
        when "message" is null or trim("message") = '' then 'No message available'
        else lower(trim(regexp_replace(regexp_replace("message", 'https?://[^\s]+', '', 'g'), '[^\x20-\x7E]', '', 'g')))
    end as "message",
    "date",
    "media_path",
    case 
        when "views" < 1 then 0
        else "views"
    end as "views",
    "message_link"
from deduplicated
where rn_channel = 1 and rn_message = 1  
  and "views" > 1 
  and "date" is not null