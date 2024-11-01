create_script = '''revoke usage on schema yandex_eats_ph from public;
grant usage on schema yandex_eats_ph to public;
grant create on schema yandex_eats_ph to public;
DROP SCHEMA yandex_eats_ph CASCADE;
CREATE SCHEMA yandex_eats_ph;

DROP TYPE IF EXISTS vehicle cascade;
DROP TYPE IF EXISTS cfp cascade;
DROP domain IF EXISTS rating cascade;

CREATE TYPE yandex_eats_ph.vehicle as enum ('onfoot', 'bicycle', 'car');
CREATE type yandex_eats_ph.cfp as (carbs real, fats real, proteins real);
CREATE domain yandex_eats_ph.rating as real check(0 <= value and value <= 5);

create table if not exists yandex_eats_ph.person(           -----
	person_id serial not null primary key,
	phone_number text,
	login text,
	full_name text
);
create table if not exists yandex_eats_ph.courier(
	courier_id serial not null primary key,
	name text,
	rating real,
	transport yandex_eats_ph.vehicle,
	is_busy boolean
);
create table if not exists yandex_eats_ph.address(
	address_id serial not null primary key,
	city text,
	street text,
	house text,
	entrance int
);
create table if not exists yandex_eats_ph.prov_address(
	prov_address_id serial not null primary key,
	city text,
	street text,
	is_available boolean
);
create table if not exists yandex_eats_ph.provider(           -----
	provider_id serial not null primary key,
	name text,
	price_range int,
	rating yandex_eats_ph.rating,
	contacts int
);

create table if not exists yandex_eats_ph.provider_prov_address(
	provider_id int not null references yandex_eats_ph.provider (provider_id),
	prov_address_id int not null references yandex_eats_ph.prov_address (prov_address_id),
	primary key (provider_id, prov_address_id)
);

create table if not exists yandex_eats_ph."order"(           -----
	order_id serial not null primary key,
	person_id int not null references yandex_eats_ph.person (person_id),
	provider_id int not null references yandex_eats_ph.provider (provider_id),
	courier_id int not null references yandex_eats_ph.courier (courier_id),
	data text,
	eta time,
	price money,
	status boolean
);
create table if not exists yandex_eats_ph.dishes(           -----
	dish_id serial not null primary key,
	provider_id int not null references yandex_eats_ph.provider (provider_id),
	nutrients yandex_eats_ph.cfp,
	portion_size int,
	contains text,
	is_vegan boolean
);
create table if not exists yandex_eats_ph.change_address(
	person_id int not null references yandex_eats_ph.person (person_id),
	address_id int not null references yandex_eats_ph.address (address_id),
	primary key (person_id, address_id)
);
create table if not exists yandex_eats_ph.order_dishes(
	order_id int not null references yandex_eats_ph."order" (order_id),
	dish_id int not null references yandex_eats_ph.dishes (dish_id),
	primary key (order_id, dish_id)
);


create table if not exists yandex_eats_ph.account(           -----
	person_id int not null references yandex_eats_ph.person(person_id),
	points int,
	promos text,
	money_sum money,
	payment_id serial,
	primary key(payment_id)
);

create table if not exists yandex_eats_ph.payment_info(
	payment_id int not null references yandex_eats_ph.account(payment_id),
	card_number int not null,
	cvc int not null,
	exp_date date not null,
	owner text,
	bank text
);'''