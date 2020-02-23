-- create table library_collection_inventory(
-- 	bibnum integer,
-- 	title text,
-- 	author text,
-- 	isbn text,
-- 	publicationYear text,
-- 	publisher text,
-- 	subject text,
-- 	itemType text, 
-- 	itemCollection text,
-- 	floatingItem text,
-- 	itemLocation text,
-- 	reportDate date,
-- 	itecCount integer	
-- );

-- create table checkouts_by_title_data_lens(
-- 	bibnumber integer,
-- 	itemBarcode text,
-- 	itemtype text,
-- 	collection text,
-- 	callNumber text,
-- 	checkoutdatetime timestamp

-- );

-- create table integrated_library_system_ils_data_dictionary(
-- 	Code text,
-- 	Description text,
-- 	CodeType text,
-- 	FormatGroup text,
-- 	FormatSubgroup text,
-- 	CategoryGroup text,
-- 	CategorySubgroup text
-- );

create table userDetails(
	Id text,
	name text, 
	password text,
	contact text,
	acc_type text,
	books_issued integer,
	fine integer
);



-- \copy library_collection_inventory from 'data/Library_Collection_Inventory.csv' delimiter ',' csv header;
-- \copy checkouts_by_title_data_lens from 'data/Checkouts_By_Title_Data_Lens_2017.csv' delimiter ',' csv header;
-- \copy integrated_library_system_ils_data_dictionary from 'data/Integrated_Library_System__ILS__Data_Dictionary.csv' delimiter ',' csv header;
\copy userDetails from 'data/user.csv' delimiter ',' csv header;

-- -- drop table library_collection_inventory;
-- -- drop table checkouts_by_title_data_lens;
-- -- drop table integrated_library_system_ils_data_dictionary;