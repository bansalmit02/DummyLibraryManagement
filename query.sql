-- library_collection_inventory
-- checkouts_by_title_data_lens
-- integrated_library_system_ils_data_dictionary

select * from library_collection_inventory limit 5;
select * from checkouts_by_title_data_lens limit 10;
select * from integrated_library_system_ils_data_dictionary limit 10;

select userid, count(userid) from checkouts_data 
group by userid;

update userdetails, (select userid, count(userid) from checkouts_data 
group by userid) as data set book_issued = data.count 
	where userdetails.userid = data.userid;


UPDATE userdetails
SET    books_issued = data.count
      
FROM   (select userid, count(userid) from checkouts_data 
group by userid) as data
WHERE  data.userid = userdetails.id;


SELECT floor(random()*(50-0)+0);

update userdetails set fine= floor(random()*(50-0)+0);

update checkouts_data 
set due_date= (due_date + interval '7 day')::date
from
(select acc_type, id from userdetails) as acc
where acc.acc_type ='3' and acc.id = checkouts_data.userid;


DATE_PART('day', '{} 00:00:00'::timestamp - '{} 00:00:00'::timestamp);"

