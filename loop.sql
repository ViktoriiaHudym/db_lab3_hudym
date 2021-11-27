DO $$
DECLARE
    difficulty CHAR(50);
BEGIN
    difficulty := 'type';
    FOR counter IN 5..9
        LOOP
		   INSERT INTO difficultytype(type_id, type_name) 
		   VALUES (counter, difficulty || counter);
        END LOOP;
END;
$$

-- select * from difficultytype;