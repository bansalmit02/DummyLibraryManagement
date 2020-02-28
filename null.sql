select count(distinct title)
from library_collection
where title is not null;

select count(distinct bibnum) as bibNumber_count
from library_collection
where bibnum is not null;

select count(title)
from library_collection
where isbn is not null and publicationYear is not null and 
publisher is not null and subject is not null and itemType is not null
and itemCollection is not null and title is not null and bibnum is not null
and floatingItem is not null and itemLocation is not null
and reportDate is not null
and itemcount is not null;

select count(distinct id) as id
from library_collection;

-- delete from library_collection_inventory
-- 	where
-- isbn is  null or publicationYear is  null or 
-- publisher is  null or subject is  null or itemType is  null
-- or itemCollection is  null or title is  null or bibnum is  null
-- or floatingItem is  null or itemLocation is  null
-- or reportDate is  null
-- or itecCount is  null;