USE incidents;
CREATE TABLE IF NOT EXISTS `incidents`.`blog_user` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `user_username` VARCHAR(45) NULL,
  `user_password` VARCHAR(45) NULL,
  PRIMARY KEY (`user_id`));

DROP procedure IF EXISTS `sp_validateLogin`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(45)
)
BEGIN
	select * from blog_user where user_username = p_username;
END$$

DELIMITER ;