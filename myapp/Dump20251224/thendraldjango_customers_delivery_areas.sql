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
-- Table structure for table `customers_delivery_areas`
--

DROP TABLE IF EXISTS `customers_delivery_areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers_delivery_areas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `deliveryarea_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customers_delivery_areas_customer_id_deliveryarea_aeed48f6_uniq` (`customer_id`,`deliveryarea_id`),
  KEY `customers_delivery_a_deliveryarea_id_ecaf2c08_fk_delivery_` (`deliveryarea_id`),
  CONSTRAINT `customers_delivery_a_customer_id_b074e2e6_fk_customers` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `customers_delivery_a_deliveryarea_id_ecaf2c08_fk_delivery_` FOREIGN KEY (`deliveryarea_id`) REFERENCES `delivery_areas` (`area_id`)
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers_delivery_areas`
--

LOCK TABLES `customers_delivery_areas` WRITE;
/*!40000 ALTER TABLE `customers_delivery_areas` DISABLE KEYS */;
INSERT INTO `customers_delivery_areas` VALUES (5,1,1),(7,4,4),(49,6,6),(50,7,1),(51,8,2),(52,9,3),(53,10,4),(54,11,5),(55,12,6),(56,13,1),(57,14,2),(58,15,3),(59,16,4),(60,17,5),(61,18,6),(62,19,1),(63,20,2),(64,21,3),(65,22,4),(66,23,5),(67,24,6),(68,25,1),(69,26,2),(70,27,3),(71,28,4),(72,29,5),(73,30,6),(74,31,1),(75,32,2),(76,33,3),(77,34,4),(78,35,5),(79,36,6),(80,37,1),(81,38,2),(82,39,3),(83,40,4),(84,41,5),(85,42,6),(86,43,1),(87,44,2),(88,45,3),(89,46,4),(90,47,5),(91,48,6),(92,49,1),(93,50,2),(94,51,3),(95,52,4),(96,53,5),(97,54,6),(98,55,1),(99,56,2),(100,57,3),(101,58,4),(102,59,5),(103,60,6),(104,61,1),(105,62,2),(106,63,3),(107,64,4),(108,65,5),(109,66,6),(110,67,1),(111,68,2),(112,69,3),(113,70,4),(114,71,5),(115,72,6),(116,73,1),(117,74,2),(118,75,3),(119,76,4),(120,77,5),(121,78,6),(122,79,1),(123,80,2),(124,81,3),(125,82,4),(126,83,5),(127,84,6),(128,85,1),(129,86,2),(130,87,3),(131,88,4),(132,89,5),(133,90,6),(134,91,1),(135,92,2),(8,114,6),(30,115,1),(16,120,6),(17,121,1),(9,122,2),(18,123,3),(10,124,4),(24,125,5),(44,126,6),(19,131,5),(31,132,6),(25,133,1),(11,134,2),(20,135,3),(26,136,4),(27,137,5),(45,138,6),(21,139,1),(32,140,2),(12,141,3),(33,142,4),(34,143,5),(22,144,6),(35,145,1),(36,146,2),(37,147,3),(23,148,4),(46,149,5),(38,150,6),(39,151,1),(40,152,2),(41,153,3),(13,154,4),(42,155,5),(47,156,6),(28,157,1),(14,158,2),(15,159,3),(29,160,4),(43,161,5),(48,162,6),(6,163,1),(260,164,1),(261,165,1),(262,166,1),(263,167,1),(264,168,1);
/*!40000 ALTER TABLE `customers_delivery_areas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-24 18:24:24
