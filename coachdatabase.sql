-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (arm64)
--
-- Host: localhost    Database: coachdatabase
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `competition`
--

DROP TABLE IF EXISTS `competition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competition` (
  `competition_id` int NOT NULL AUTO_INCREMENT,
  `competition_date` date NOT NULL,
  `competition_location` varchar(255) NOT NULL,
  PRIMARY KEY (`competition_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competition`
--

LOCK TABLES `competition` WRITE;
/*!40000 ALTER TABLE `competition` DISABLE KEYS */;
/*!40000 ALTER TABLE `competition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fitness_watch`
--

DROP TABLE IF EXISTS `fitness_watch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fitness_watch` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `activity_date` date DEFAULT NULL,
  `activity_minutes` int DEFAULT NULL,
  `sleep_hours` float DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fitness_watch_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fitness_watch`
--

LOCK TABLES `fitness_watch` WRITE;
/*!40000 ALTER TABLE `fitness_watch` DISABLE KEYS */;
INSERT INTO `fitness_watch` VALUES (1,2,'2024-12-01',45,6),(2,3,'2024-12-01',120,8),(3,4,'2024-12-01',90,7),(4,5,'2024-12-01',75,6.5),(5,1,'2024-12-02',90,7.8),(6,2,'2024-12-02',60,7),(7,3,'2024-12-02',100,8.5),(8,4,'2024-12-02',80,7.2),(9,5,'2024-12-02',70,6.8),(10,1,'2024-12-03',90,7.8),(11,1,'2024-12-04',90,7.8),(12,1,'2024-12-05',90,7.8),(13,1,'2024-12-06',90,7.8),(14,1,'2024-12-07',90,7.8),(15,5,'2024-12-08',235,6.1),(16,5,'2024-12-09',700,7.9),(17,5,'2024-12-10',75,7),(18,5,'2024-12-11',80,7.2),(19,5,'2024-12-12',85,7.3),(20,4,'2024-12-08',235,7.7),(21,4,'2024-12-09',700,7.9),(22,4,'2024-12-10',75,7),(23,4,'2024-12-11',80,7.2),(24,4,'2024-12-12',85,7.3);
/*!40000 ALTER TABLE `fitness_watch` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_fitness_log_insert` AFTER INSERT ON `fitness_watch` FOR EACH ROW BEGIN
    DECLARE week_start_date DATE;
    SET week_start_date = DATE_SUB(NEW.activity_date, INTERVAL WEEKDAY(NEW.activity_date) DAY);
    CALL update_weekly_leaderboard(week_start_date);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_fitness_log_update` AFTER UPDATE ON `fitness_watch` FOR EACH ROW BEGIN
    DECLARE week_start_date DATE;
    SET week_start_date = DATE_SUB(NEW.activity_date, INTERVAL WEEKDAY(NEW.activity_date) DAY);
    CALL update_weekly_leaderboard(week_start_date);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `rewards`
--

DROP TABLE IF EXISTS `rewards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rewards` (
  `reward_id` int NOT NULL AUTO_INCREMENT,
  `creator_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `reward_date` date DEFAULT NULL,
  `reward_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`reward_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `rewards_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rewards`
--

LOCK TABLES `rewards` WRITE;
/*!40000 ALTER TABLE `rewards` DISABLE KEYS */;
/*!40000 ALTER TABLE `rewards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_competition`
--

DROP TABLE IF EXISTS `user_competition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_competition` (
  `user_id` int NOT NULL,
  `competition_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`competition_id`),
  KEY `competition_id` (`competition_id`),
  CONSTRAINT `user_competition_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `user_competition_ibfk_2` FOREIGN KEY (`competition_id`) REFERENCES `competition` (`competition_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_competition`
--

LOCK TABLES `user_competition` WRITE;
/*!40000 ALTER TABLE `user_competition` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_competition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Alice',25,'Female','alice123'),(2,'Bob',30,'Male','bob456'),(3,'Charlie',35,'Male','charlie789'),(4,'David',28,'Male','david234'),(5,'Eva',32,'Female','eva567');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_user_delete` AFTER DELETE ON `users` FOR EACH ROW BEGIN
    DELETE FROM rewards WHERE user_id = OLD.user_id;
    DELETE FROM weekly_leaderboard WHERE user_id = OLD.user_id;
    DELETE FROM fitness_watch WHERE user_id = OLD.user_id;
    DELETE FROM user_competition WHERE user_id = OLD.user_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `weekly_leaderboard`
--

DROP TABLE IF EXISTS `weekly_leaderboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weekly_leaderboard` (
  `leaderboard_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `week_start_date` date DEFAULT NULL,
  `fitness_score` float DEFAULT NULL,
  `total_exercise_minutes` int DEFAULT NULL,
  `total_sleep_hours` float DEFAULT NULL,
  `ranking` int DEFAULT NULL,
  PRIMARY KEY (`leaderboard_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `weekly_leaderboard_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weekly_leaderboard`
--

LOCK TABLES `weekly_leaderboard` WRITE;
/*!40000 ALTER TABLE `weekly_leaderboard` DISABLE KEYS */;
INSERT INTO `weekly_leaderboard` VALUES (8,2,'2024-11-25',1,45,6,3),(9,3,'2024-11-25',2,120,8,1),(10,4,'2024-11-25',2,90,7,2),(11,5,'2024-11-25',1,75,6.5,4),(82,1,'2024-12-02',12,540,46.8,1),(83,2,'2024-12-02',2,60,7,3),(84,3,'2024-12-02',2,100,8.5,4),(85,4,'2024-12-02',4,315,14.9,2),(86,5,'2024-12-02',2,305,12.9,5),(98,4,'2024-12-09',8,940,29.4,1),(99,5,'2024-12-09',8,940,29.4,2),(101,1,'2024-12-01',12,540,46.8,1),(102,2,'2024-12-01',3,105,13,4),(103,3,'2024-12-01',4,220,16.5,2),(104,4,'2024-12-01',4,170,14.2,3),(105,5,'2024-12-01',2,145,13.3,5),(108,4,'2024-12-08',10,1175,37.1,1),(109,5,'2024-12-08',9,1175,35.5,2);
/*!40000 ALTER TABLE `weekly_leaderboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'coachdatabase'
--

--
-- Dumping routines for database 'coachdatabase'
--
/*!50003 DROP PROCEDURE IF EXISTS `assign_rewards` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `assign_rewards`(IN week_start DATE)
BEGIN
    INSERT INTO rewards (user_id, reward_date, reward_description)
    SELECT user_id, week_start, 'Reward for achieving a fitness score of 10+'
    FROM weekly_leaderboard
    WHERE week_start_date = week_start
    AND fitness_score >= 10
    AND user_id NOT IN (SELECT user_id FROM rewards WHERE reward_date = week_start);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `check_competition_eligibility` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `check_competition_eligibility`(IN competition_date DATE)
BEGIN
    -- Fetch users who received at least one reward in the 2 weeks before the competition date
    SELECT u.user_id, u.first_name
    FROM users u
    WHERE EXISTS (
        SELECT 1
        FROM rewards r
        WHERE r.user_id = u.user_id
        AND r.reward_date BETWEEN DATE_SUB(competition_date, INTERVAL 14 DAY) AND competition_date
    );
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `personal_report` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `personal_report`(IN week_start DATE)
BEGIN
    SELECT u.user_id, 
           u.first_name,
           ROUND(AVG(f.sleep_hours), 2) AS avg_sleep_hours,
           ROUND(SUM(f.activity_minutes), 2) AS total_activity_minutes
    FROM fitness_watch f
    JOIN users u ON f.user_id = u.user_id
    WHERE f.activity_date BETWEEN week_start AND DATE_ADD(week_start, INTERVAL 6 DAY)
    GROUP BY u.user_id, u.first_name;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `register_user_for_competition` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `register_user_for_competition`(IN p_user_id INT, IN p_competition_date DATE)
BEGIN
    -- Declare a variable to store the eligibility status
    DECLARE is_eligible INT DEFAULT 0;

    -- Check if the user has earned a reward in the last 14 days before the competition date
    SELECT COUNT(*)
    INTO is_eligible
    FROM rewards r
    WHERE r.user_id = p_user_id
    AND r.reward_date BETWEEN DATE_SUB(p_competition_date, INTERVAL 14 DAY) AND p_competition_date;

    -- If the user is eligible, register them for the competition
    IF is_eligible > 0 THEN
        -- Insert the user into the user_competition table
        INSERT INTO user_competition (user_id, competition_id)
        SELECT p_user_id, c.competition_id
        FROM competition c
        WHERE c.competition_date = p_competition_date
        AND NOT EXISTS (
            SELECT 1
            FROM user_competition uc
            WHERE uc.user_id = p_user_id AND uc.competition_id = c.competition_id
        );
    ELSE
        -- If the user is not eligible, raise an error or handle as needed
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User is not eligible for the competition';
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `update_weekly_leaderboard` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_weekly_leaderboard`(IN start_date DATE)
BEGIN
    DELETE FROM weekly_leaderboard WHERE week_start_date = start_date;

    INSERT INTO weekly_leaderboard (user_id, week_start_date, fitness_score, total_exercise_minutes, total_sleep_hours, ranking)
    SELECT
        f.user_id,
        start_date AS week_start_date,
        SUM((f.activity_minutes >= 30) + (f.sleep_hours >= 7)) AS fitness_score,
        SUM(f.activity_minutes) AS total_exercise_minutes,
        SUM(f.sleep_hours) AS total_sleep_hours,
        0 AS ranking
    FROM fitness_watch f
    WHERE f.activity_date BETWEEN start_date AND DATE_ADD(start_date, INTERVAL 6 DAY)
    GROUP BY f.user_id;

    SET @rank = 0;
    UPDATE weekly_leaderboard wl
    JOIN (
        SELECT leaderboard_id
        FROM weekly_leaderboard
        WHERE week_start_date = start_date
        ORDER BY fitness_score DESC
    ) AS sorted_wl
    SET wl.ranking = (@rank := @rank + 1)
    WHERE wl.leaderboard_id = sorted_wl.leaderboard_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-05 22:47:55
