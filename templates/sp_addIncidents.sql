CREATE TABLE IF NOT EXISTS `tbl_blog` (
  `blog_user_id` varchar(45) NOT NULL,
  `blog_title` varchar(45) DEFAULT NULL,
  `blog_date` varchar(45) DEFAULT NULL,
  `blog_location` varchar(45) DEFAULT NULL,
  `blog_vehicle` varchar(45) DEFAULT NULL,
  `blog_incident` varchar(1000) DEFAULT NULL,
  `blog_suspect` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`blog_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;


DROP procedure IF EXISTS `sp_addIncidents`;
USE incidents;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addIncidents`(
    IN p_user varchar(45),
    IN p_title varchar(45),
    IN p_date varchar(45),
    IN p_location varchar(45),
    IN p_vehicle varchar(45),
    IN p_incident VARCHAR(1000),
    IN p_suspect VARCHAR(1000)
)
BEGIN
    insert into tbl_blog(
        blog_user_id,
        blog_title,
        blog_date,
        blog_location,
        blog_vehicle,
        blog_incident,
        blog_suspect
    )
    values
    (
        p_user,
        p_title,
        p_date,
        p_location,
        p_vehicle,
        p_incident,
        p_suspect
    );
END$$
 
DELIMITER ;