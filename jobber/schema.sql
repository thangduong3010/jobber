drop table if exists job_entries;
create table job_entries (
	issue_number integer primary key,
    id number not null,
    title text not null,
    label text null
);