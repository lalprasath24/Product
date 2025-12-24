-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: thendraldjango
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `delivery_areas`
--

DROP TABLE IF EXISTS `delivery_areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_areas` (
  `area_id` int NOT NULL AUTO_INCREMENT,
  `area_name` varchar(100) NOT NULL,
  `pincode` varchar(20) NOT NULL,
  `is_serviced` tinyint(1) NOT NULL,
  `area_code` varchar(20) DEFAULT NULL,
  `live_location` varchar(2000) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`area_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_areas`
--

LOCK TABLES `delivery_areas` WRITE;
/*!40000 ALTER TABLE `delivery_areas` DISABLE KEYS */;
INSERT INTO `delivery_areas` VALUES (1,'kodambakkam','654456',1,'001','https://www.bing.com/search?pglt=41&q=kodambakkam+location+url&cvid=0ef926dec7c24a5e88b65a8af3c33122&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCTEwNjY4ajBqMagCALACAA&FORM=ANNTA1&PC=U531','lalptasathk187@gmail.com','7010044587'),(2,'Nungabakkam','654543',1,'002','https://www.bing.com/search?pglt=41&q=kodambakkam+location+url&cvid=0ef926dec7c24a5e88b65a8af3c33122&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCTEwNjY4ajBqMagCALACAA&FORM=ANNTA1&PC=U531',NULL,NULL),(3,'guindy','654123',1,'003','https://www.bing.com/search?pglt=41&q=kodambakkam+location+url&cvid=0ef926dec7c24a5e88b65a8af3c33122&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCTEwNjY4ajBqMagCALACAA&FORM=ANNTA1&PC=U531',NULL,NULL),(4,'chaidapet','654098',1,'004','https://www.bing.com/search?pglt=41&q=kodambakkam+location+url&cvid=0ef926dec7c24a5e88b65a8af3c33122&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCTEwNjY4ajBqMagCALACAA&FORM=ANNTA1&PC=U531',NULL,NULL),(5,'kodambakkam','654456',1,'001','https://www.bing.com/search?pglt=41&q=kodambakkam+location+url&cvid=0ef926dec7c24a5e88b65a8af3c33122&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCTEwNjY4ajBqMagCALACAA&FORM=ANNTA1&PC=U531',NULL,NULL),(6,'Anaicut','654456',0,'006','https://www.bing.com/search?pglt=41&q=kodambakkam+location+url&cvid=0ef926dec7c24a5e88b65a8af3c33122&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCTEwNjY4ajBqMagCALACAA&FORM=ANNTA1&PC=U531',NULL,NULL);
/*!40000 ALTER TABLE `delivery_areas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-24 18:24:23
