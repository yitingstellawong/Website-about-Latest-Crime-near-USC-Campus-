USE incidents;
DROP procedure IF EXISTS `sp_GetIncidentsByUser`;
 
DELIMITER $$
CREATE PROCEDURE `sp_GetIncidentsByUser` (
IN p_user VARCHAR(45)
)
BEGIN
    select * from tbl_blog where blog_user_id = p_user;
END$$
 
DELIMITER ;