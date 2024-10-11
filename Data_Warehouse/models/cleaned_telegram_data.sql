with raw_data as (
    select * from {{ ref('doctorset') }}
    union all
    select * from {{ ref('lobelia4cosmetics') }}
    union all
    select * from {{ ref('yetenaweg') }}
    union all
    select * from {{ ref('eahci') }}
    union all
    select * from {{ ref('chemed') }}
),
deduplicated as (
    select distinct *
    from raw_data
),
final as (
    select
        "Channel Title",
        "Channel Username",
        "ID",
        case 
            when "Message" is null or trim("Message") = '' then 'No message available'
            else lower(trim(regexp_replace(regexp_replace("Message", 'https?://[^\s]+', '', 'g'), '[^\x20-\x7E]', '', 'g')))
        end as "Message",
        "Date",
        "Media Path",
        case 
            when "views" < 1 then 0
            else "views"
        end as "views",
        "message_link"
    from deduplicated
    where "views" > 1 and "Date" is not null
)

select * from final;
