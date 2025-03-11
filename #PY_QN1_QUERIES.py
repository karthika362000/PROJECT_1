#PY_QN1_QUERIES:

#QUES_1->List_all_competitions_along_with_their_category_name:
SELECT c.competition_name, cat.category_name 
FROM Competitions c 
JOIN Categories cat ON c.category_id = cat.category_id;


#QUES_2->Count_the_number_of_competitions_in_each_category:
SELECT cat.category_name, COUNT(c.competition_id) AS competition_count
FROM Competitions c 
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name;


#QUES_3->Find_all_competitions_of_type_doubles:
SELECT * FROM Competitions WHERE type = 'doubles';


#QUES_4->Get_competitions_that_belong_to_a_specific_category (e.g., ITF Men):
SELECT * FROM Competitions WHERE category_id = 'itf-men';  -- Change ID as needed
                      #OR#
SELECT c.competition_name, cat.category_name
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';



#QUES_5->Identify_parent_competitions_and_their_sub-competitions:
SELECT parent.competition_name AS parent_competition, child.competition_name AS sub_competition
FROM Competitions child
JOIN Competitions parent ON child.parent_id = parent.competition_id;


#QUES_6->Analyze_the_distribution_of_competition_types_by_category:
SELECT cat.category_name, c.type, COUNT(*) AS count_per_type
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type;


#QUES_7->List_all_competitions_with_no_parent(top-level_competitions):
SELECT * FROM Competitions WHERE parent_id IS NULL;