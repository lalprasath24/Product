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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Customer',7,'add_customer'),(26,'Can change Customer',7,'change_customer'),(27,'Can delete Customer',7,'delete_customer'),(28,'Can view Customer',7,'view_customer'),(29,'Can add Delivery Area',8,'add_deliveryarea'),(30,'Can change Delivery Area',8,'change_deliveryarea'),(31,'Can delete Delivery Area',8,'delete_deliveryarea'),(32,'Can view Delivery Area',8,'view_deliveryarea'),(33,'Can add Product',9,'add_product'),(34,'Can change Product',9,'change_product'),(35,'Can delete Product',9,'delete_product'),(36,'Can view Product',9,'view_product'),(37,'Can add Staff',10,'add_staff'),(38,'Can change Staff',10,'change_staff'),(39,'Can delete Staff',10,'delete_staff'),(40,'Can view Staff',10,'view_staff'),(41,'Can add Subscription Plan',11,'add_subscriptionplan'),(42,'Can change Subscription Plan',11,'change_subscriptionplan'),(43,'Can delete Subscription Plan',11,'delete_subscriptionplan'),(44,'Can view Subscription Plan',11,'view_subscriptionplan'),(45,'Can add Customer Subscription',12,'add_customersubscription'),(46,'Can change Customer Subscription',12,'change_customersubscription'),(47,'Can delete Customer Subscription',12,'delete_customersubscription'),(48,'Can view Customer Subscription',12,'view_customersubscription'),(49,'Can add Order',13,'add_order'),(50,'Can change Order',13,'change_order'),(51,'Can delete Order',13,'delete_order'),(52,'Can view Order',13,'view_order'),(53,'Can add Payment',14,'add_payment'),(54,'Can change Payment',14,'change_payment'),(55,'Can delete Payment',14,'delete_payment'),(56,'Can view Payment',14,'view_payment'),(57,'Can add Order Item',15,'add_orderitem'),(58,'Can change Order Item',15,'change_orderitem'),(59,'Can delete Order Item',15,'delete_orderitem'),(60,'Can view Order Item',15,'view_orderitem'),(61,'Can add Delivery',16,'add_delivery'),(62,'Can change Delivery',16,'change_delivery'),(63,'Can delete Delivery',16,'delete_delivery'),(64,'Can view Delivery',16,'view_delivery'),(65,'Can add otp',17,'add_otp'),(66,'Can change otp',17,'change_otp'),(67,'Can delete otp',17,'delete_otp'),(68,'Can view otp',17,'view_otp'),(69,'Can add user',18,'add_user'),(70,'Can change user',18,'change_user'),(71,'Can delete user',18,'delete_user'),(72,'Can view user',18,'view_user');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-24 18:24:20
