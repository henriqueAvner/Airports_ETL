-- aeroportos por estado
select  
	state as estado, 
	count(airport_name) as quantidade_aeroportos 
from airports
group by airports.state
order by quantidade_aeroportos desc;

-- altitude média dos aeroportos por estado
select  
	state as estado, 
	count(airport_name) as quantidade_aeroportos,
	avg(altitude) as altitude_media
from airports
group by airports.state
order by quantidade_aeroportos desc;


-- estados com varios aeroportos -> having filtra de acordo com o grupo quantidade_aeroportos
select state as estado,
count(airport_name) as quantidade_aeroportos
from airports
group by airports.state
having(count(airport_name)) > 25;


-- classificando aeroportos por altitude
select 
	airport_name, 
	altitude,
	case
		when altitude >= 200 then 'alto'
		when altitude >= 100 and altitude <= 200 then 'medio'
		else 'baixo'
	end as classificacao
from airports;


--areoportos acima da altitude media nacional
select
	airport_name,
	city,
	state,
	altitude
from airports 
where altitude > (
select 
	avg(altitude)
from airports)

--aeorporto ou aeroportos de maior altitude
select 
	airport_name,
	altitude,
	city,
	state
from airports
where altitude = (select MAX(altitude) from airports)
group by airport_name, altitude, city, state;



--Estados com quantidade de aeroportos acima da média

with quantidadeAeroportos as (
select 
state, count(airport_name) as quantidade
from airports
group by state
order by quantidade desc
) 
select
	state,
	quantidade
from quantidadeAeroportos 
where quantidade > 
(select
	 avg(quantidade)
from quantidadeAeroportos);
