with clientes as (
select distinct 
		company_id
	   ,max(created_at::timestamp) max_created_at
from purchase
where lower(purchase_channel) = 'web'
and status in (2)
and  created_at::date >= cast (CURRENT_TIMESTAMP - INTERVAL '30 days' as date)
group by 1
)
select f.company_id 
	  ,f.empresa
	  ,f.ambiente
	  ,f.quantidade
	  ,f.data_ultima_transacao
	  ,f.hora_ultima_transacao
	  ,f.gap_time
	  ,f.status
 from (
select r.company_id 
	  ,upper(r.Empresa) empresa 
	  ,r.ambiente
	  ,r.quantidade
	  ,r.data_ultima_transacao
	  ,r.hora_ultima_transacao
	  ,r.gap_time::text
	  ,case when r.gap_time > '01:00:00'
	  		then 1
	  	else 0
	  end status
from (
select c.company_id
      , co.name as Empresa
     , case when (co.id in (25,28,49,50,22,23,26,21,24,101,102,103)) then 'V3 - Grupo A'
                        else 'V2 - Grupo A'
         end as Ambiente
        , count(p) Quantidade
        ,case when max(p.created_at) is null 
        		then c.max_created_at::date
        	else  max(p.created_at)::date
        end as Data_ultima_transacao
       ,case when max(p.created_at) is null 
        		then TO_CHAR(c.max_created_at, 'HH24:MI:SS')
        	else  TO_CHAR(max(p.created_at), 'HH24:MI:SS')
        end as Hora_ultima_transacao
        ,case when max(p.created_at) is null
        then DATE_TRUNC('SECOND',current_timestamp - interval '3 hours' - max(c.max_created_at))
         else DATE_TRUNC('SECOND', current_timestamp - interval '3 hours' - max(p.created_at) )
        end as Gap_time
from clientes c 
left join company co on co.id = c.company_id
left join purchase p on p.company_id = c.company_id
					and p.status in (2)
					and p.purchase_channel in ('WEB')
					and p.created_at::date >= cast (CURRENT_TIMESTAMP - INTERVAL '12 hours' as date)
where p.company_id in (17,18,15,21,23)
group by co.name, p.status, co.id, c.max_created_at, c.company_id
) r
union all 
select r.company_id
	  ,upper(r.Empresa) empresa 
	  ,r.ambiente
	  ,r.quantidade
	  ,r.data_ultima_transacao
	  ,r.hora_ultima_transacao
	  ,r.gap_time::text
	  ,case when r.gap_time > '02:00:00'
	  		then 1
	  	else 0
	  end status
from (
select c.company_id 
	 , co.name as Empresa
     , case when (co.id in (25,28,49,50,22,23,26,21,24,101,102,103)) then 'V3 - Grupo B'
                        else 'V2 - Grupo B'
         end as Ambiente
        , count(p) Quantidade
        ,case when max(p.created_at) is null 
        		then c.max_created_at::date
        	else  max(p.created_at)::date
        end as Data_ultima_transacao
       ,case when max(p.created_at) is null 
        		then TO_CHAR(c.max_created_at, 'HH24:MI:SS')
        	else  TO_CHAR(max(p.created_at), 'HH24:MI:SS')
        end as Hora_ultima_transacao
        ,case when max(p.created_at) is null
        then DATE_TRUNC('SECOND', current_timestamp - interval '3 hours' - max(c.max_created_at))
         else DATE_TRUNC('SECOND', current_timestamp - interval '3 hours' - max(p.created_at) )
        end as Gap_time
from clientes c 
left join company co on co.id = c.company_id
left join purchase p on p.company_id = c.company_id
					and p.status in (2)
					and p.purchase_channel in ('WEB')
					and p.created_at::date >= cast (CURRENT_TIMESTAMP - INTERVAL '12 hours' as date)
where p.company_id in (3,4,14,26,22)
group by co.name, p.status, co.id, c.max_created_at, c.company_id 
) r
union all 
select r.company_id
	  ,upper(r.Empresa) empresa 
	  ,r.ambiente
	  ,r.quantidade
	  ,r.data_ultima_transacao
	  ,r.hora_ultima_transacao
	  ,r.gap_time::text
	  ,case when r.gap_time > '23:59:59'
	  		then 1
	  	else 0
	  end status
from (
select c.company_id
	 , co.name as Empresa
     , case when (co.id in (25,28,49,50,22,23,26,21,24,101,102,103)) then 'V3'
                        else 'V2'
         end as Ambiente
        , count(p) Quantidade
        ,case when max(p.created_at) is null 
        		then c.max_created_at::date
        	else  max(p.created_at)::date
        end as Data_ultima_transacao
       ,case when max(p.created_at) is null 
        		then TO_CHAR(c.max_created_at, 'HH24:MI:SS')
        	else  TO_CHAR(max(p.created_at), 'HH24:MI:SS')
        end as Hora_ultima_transacao
        ,case when max(p.created_at) is null
        then DATE_TRUNC('SECOND', current_timestamp - interval '3 hours' - max(c.max_created_at))
         else DATE_TRUNC('SECOND', current_timestamp - interval '3 hours' - max(p.created_at) )
        end as Gap_time
from clientes c 
left join company co on co.id = c.company_id
left join purchase p on p.company_id = c.company_id
					and p.status in (2)
					and p.purchase_channel in ('WEB')
					and p.created_at::date >= cast (CURRENT_TIMESTAMP - INTERVAL '30 hours' as date)
where c.company_id not in (3,4,14,23,26,17,18,15,21,22) -- Grupos A e B
  and c.company_id not in ( 32,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48) -- Empresas BRK
group by co.name, p.status, co.id, c.max_created_at,c.company_id
) r 
	) f 
order by (f.data_ultima_transacao
	    ,f.hora_ultima_transacao::time) desc
