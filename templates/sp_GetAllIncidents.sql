USE incidents;
DROP procedure IF EXISTS `sp_GetAllIncidents`;
 
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetAllIncidents`()
BEGIN
    select blog_title,
        blog_date,
        blog_location,
        blog_vehicle,
        blog_incident,
        blog_suspect 
	from tbl_blog;
END$$
 
DELIMITER ;