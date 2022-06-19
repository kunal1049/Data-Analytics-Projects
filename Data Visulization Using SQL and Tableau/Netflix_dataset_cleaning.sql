Use [Data Analytics Project];

/*     Titles Table     */
/* Displaying all the entries from the table*/
Select * from titles;

/* Deleting the row with null value in title column*/
Select * from titles where title IS NULL;
Delete from titles where title IS NULL;
Select count(id) as Count_of_Null from titles where title IS NULL;

/* Converting the null values to N/A and 0 */
Update titles Set age_certification='N/A' Where age_certification IS NULL;
Update titles Set seasons= 0 Where seasons IS NULL;
Update titles Set imdb_id='N/A' Where imdb_id IS NULL;
Update titles Set imdb_score = 0 Where imdb_score IS NULL;
Update titles Set imdb_votes = '0'  Where imdb_votes IS NULL;
Update titles Set tmdb_score = 0 Where tmdb_score IS NULL;
Select * from titles;

/* Converting the datatype of few columns */
ALTER TABLE titles ALTER COLUMN imdb_score float;
ALTER TABLE titles ALTER COLUMN tmdb_score float;

/*        Credits Table      */
/* Displaying all the entries from the table */
Select * from credits;

/* Finding ot the NULL Values and their relation */
Select * from credits where character IS NULL;
Select Count(*) as Count_of_Actors_with_Null  from credits where character IS NULL AND role LIKE 'ACTOR';
Select Count(*) as Count_of_Director_with_Null  from credits where character IS NULL AND role LIKE 'DIRECTOR';

/* Conerted the NULL values to specific value according to their relations */
Update credits Set character = 'N/A' Where character IS NULL AND role LIKE 'DIRECTOR';
Update credits Set character = 'Role not defined' Where character IS NULL AND role LIKE 'ACTOR';
