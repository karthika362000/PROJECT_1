#PY_QN2_QUERIES

#QUES_1->List_all_venues_along_with_their_associated_complex_name:
SELECT v.venue_name, c.complex_name 
FROM Venues v 
JOIN Complexes c ON v.complex_id = c.complex_id;


#QUES_2->Count_the_number_of_venues_in_each_complex:
SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM Venues v 
JOIN Complexes c ON v.complex_id = c.complex_id
GROUP BY c.complex_name;


#QUES_3->Get_details_of_venues_in_a_specific_country(e.g., Chile):
SELECT * FROM Venues WHERE country_name = 'Chile';

#QUES_4->Identify_all_venues_and_their_timezones:
SELECT venue_name, timezone FROM Venues;


#QUES_5->Find_complexes_that_have_more_than_one_venue:
SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM Venues v 
JOIN Complexes c ON v.complex_id = c.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;


#QUES_6->List_venues_grouped_by_country:
SELECT country_name, COUNT(venue_id) AS venue_count
FROM Venues
GROUP BY country_name;


#QUES_7->Find_all_venues_for_a_specific_complex(e.g., Nacional):
SELECT * FROM Venues WHERE complex_id = 'nacional';  -- Change ID as needed
                      #OR#
SELECT v.* 
FROM Venues v
JOIN Complexes c ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Nacional';