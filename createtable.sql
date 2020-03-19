-- drop table userDetails;
create table userDetails(
	Id text not null primary key,
	name text not null, 
	password text not null,
	contact text not null,
	acc_type text not null,
	books_issued integer default 0,
	fine integer default 0
);

-- drop table admindetails;
create table admindetails(
	username text,
	name text,
	email text,
	password text,
	contact text
);

-- drop table library_collection;
create table library_collection(
	id integer not null,
	bibnum integer not null,
	title text not null,
	author text not null,
	isbn text not null,
	publicationYear text not null,
	publisher text not null,
	subject text not null,
	itemType text not null, 
	itemCollection text not null,
	floatingItem text not null,
	itemLocation text not null,
	reportDate date not null,
	itemcount integer not null check (itemcount >= 0),
	constraint unique_id primary key (id)
);
-- drop table checkouts_data;
create table checkouts_data(
	userid text not null,
	bookid integer not null,
	issue_date date,
	admin_issued text,
	due_date date,
	constraint due_date_check check (issue_date < due_date)
);
create table pending(
	Id text not null primary key,
	name text not null, 
	password text not null,
	contact text not null,
	acc_type text not null,
	books_issued integer default 0,
	fine integer default 0
);
-- drop table chcekin_data;
create table checkin_data(
	userid text not null,
	bookid integer not null,
	issue_date date not null,
	admin_issued text not null,
	due_date date not null,
	return_date date not null,
	admin_returned text not null
);
create table returnbookDetails(
	userid text not null,
	bookid integer,
	returndate date,
	duedate date,
	chekinby text
);
insert into admindetails values('2017TT10922', 'Asif Anwar', 'asifanwar@gmail.com', 'qwerty', '7260948737');
insert into admindetails values('2017TT10925', 'Zia Kamran', 'ziakamran@gmail.com', 'qwerty', '7260948737');
insert into admindetails values('2017TT10926', 'Lakshya Narayan', 'lakshyanarayn@gmail.com', 'qwerty', '7260948737');
insert into admindetails values('2017CS10354', 'Minhaj Shakeel', 'minhajshakeel@gmail.com', 'qwerty', '7260948737');

--Open psql inside col362 folder
\copy userDetails from 'data/user.csv' delimiter ',' csv header;
\copy library_collection from 'data/library_collection.csv' delimiter ',' csv header;
\copy checkouts_data from 'data/newcheckout.csv' delimiter ',' csv header;
\copy checkin_data from 'data/newhistory.csv' delimiter ',' csv header;
