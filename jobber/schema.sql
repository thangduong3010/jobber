drop table if exists job_entries;
create table job_entries (
	issue_number integer primary key,
    id integer not null,
    title text not null,
    url text not null,
    label text null
);