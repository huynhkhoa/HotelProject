-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: hoteldb
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `roomdetail_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `roomdetail_id` (`roomdetail_id`),
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`roomdetail_id`) REFERENCES `roomdetail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(50) NOT NULL,
  `coefficient` float NOT NULL,
  `note` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Khách nội địa',3,'không có ghi chú'),(2,'Khách nước ngoài',3,'không có ghi chú');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` int NOT NULL,
  `price` float DEFAULT NULL,
  `value` int NOT NULL,
  `order_id` int NOT NULL,
  `user_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `invoice_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `identity_card` int NOT NULL,
  `address` varchar(50) NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `customer_id` int NOT NULL,
  `roomdetail_id` int NOT NULL,
  `surcharge_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `roomdetail_id` (`roomdetail_id`),
  KEY `surcharge_id` (`surcharge_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`roomdetail_id`) REFERENCES `roomdetail` (`id`),
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`surcharge_id`) REFERENCES `surcharge` (`id`),
  CONSTRAINT `order_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roomdetail`
--

DROP TABLE IF EXISTS `roomdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roomdetail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `price` float DEFAULT NULL,
  `guess` int DEFAULT NULL,
  `status` enum('HaveRoom','NoRoom') DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `roomdetail_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roomdetail`
--

LOCK TABLES `roomdetail` WRITE;
/*!40000 ALTER TABLE `roomdetail` DISABLE KEYS */;
INSERT INTO `roomdetail` VALUES (1,'PANORAMA SUITE',150,3,'HaveRoom','images/book1.jpg','Located on 25-29 floors, our Executive rooms bring a unique and memorable experience with access to Executive Lounge (on 30th floor) offering complimentary breakfast, exclusive...',1),(2,'EXCUTIVE SKYROOM',150,3,'HaveRoom','images/book2.jpg','Our Executive suites with private living rooms are all located on the executive floors. You can enjoy 46 inch LED IPTV, Espresso coffee machine and in-room fitness at this...',1),(3,'PRESIDENTIAL SUITE',150,3,'HaveRoom','images/book3.jpg','35m2-large contemporary style room provides a great comfort with modern facilities. 154 Superior rooms feature free Wi-Fi, 40 inch...',1),(4,'Deluxe Twin Room',170,3,'HaveRoom','images/about1.jpg','Twin Room from 6 to 9 floor: 40 square meters',2),(5,'Deluxe Room',170,3,'HaveRoom','images/about2.jpg','Deluxe rooms featuring cutting-edge designer bathtub, a separate rain-shower, Espresso coffee machine, IPTV and free Wi-Fi.',2),(6,'Residential Room',170,3,'HaveRoom','images/about3.jpg','Our 5-star luxury Deluxe and Premier Rooms are designed with both business and leisure travelers in mind.',2),(7,'Deluxe King Suite',200,3,'HaveRoom','images/about6.jpg','The limited edition Suite offers the perfect venue to celebrate for romantic honeymooners, anniversaries or an excuse to indulge in some romance.',3),(8,'Grand Deluxe Family Suite',200,3,'HaveRoom','images/about5.jpg','Our 5-star luxury Deluxe and Premier Rooms are designed with both business and leisure travelers in mind. Wonderfully soft beds and comfortable furnishings make every stay a pleasure, every room offers a marble bathroom or shower, writing desk and complimentary Wi-Fi to keep you in touch with friends, family and colleagues.',3),(9,'Deluxe Twin Sea View',200,3,'HaveRoom','images/about4.jpg','The limited edition Pullman Suite offers the perfect venue to celebrate for romantic honeymooners, anniversaries or an excuse to indulge in some romance. Featuring a contemporary designed one-bedroom studio and private bathtub for a deep soak.',3);
/*!40000 ALTER TABLE `roomdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surcharge`
--

DROP TABLE IF EXISTS `surcharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surcharge` (
  `id` int NOT NULL AUTO_INCREMENT,
  `surcharge` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surcharge`
--

LOCK TABLES `surcharge` WRITE;
/*!40000 ALTER TABLE `surcharge` DISABLE KEYS */;
INSERT INTO `surcharge` VALUES (1,25,3);
/*!40000 ALTER TABLE `surcharge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type`
--

DROP TABLE IF EXISTS `type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `price` float DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type`
--

LOCK TABLES `type` WRITE;
/*!40000 ALTER TABLE `type` DISABLE KEYS */;
INSERT INTO `type` VALUES (1,'Signature Suite',150,NULL),(2,'Deluxe Room',170,NULL),(3,'Economy Room',200,NULL);
/*!40000 ALTER TABLE `type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` int NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `user_role` enum('USER','ADMIN') DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','1754050037khoa@ou.edu.vn',706241646,1,'admin','827ccb0eea8a706c4c34a16891f84e7b',NULL,'ADMIN');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'hoteldb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-15  0:27:20
