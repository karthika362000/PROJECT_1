#PY_QN3_QUERIES:

#QUES_1->Get_all_competitors_with_their_rank_and_points:
SELECT c.name, r.player_rank, r.points 
FROM Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.player_rank ASC;


#QUES_2->Find_competitors_ranked_in_the_top_5:
SELECT c.name, r.player_rank, r.points 
FROM Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
WHERE r.player_rank <= 5
ORDER BY r.player_rank ASC;


#QUES_3->List_competitors_with_no_rank_movement_(stable rank):
SELECT c.name, r.player_rank, r.points 
FROM Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
WHERE r.movement = 0;


#QUES_4->Get_the_total_points_of_competitors_from_a_specific_country(e.g., Croatia):
SELECT c.country, SUM(r.points) AS total_points
FROM Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;


#QUES_5->Count_the_number_of_competitors_per_country:
SELECT c.country, COUNT(c.competitor_id) AS competitor_count
FROM Competitors c
GROUP BY c.country;


#QUES_6Find_competitors_with_the_highest_points_in_the_current_week:
SELECT c.name, r.points 
FROM Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.points DESC
LIMIT 1;