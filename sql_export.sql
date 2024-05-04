-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` text NOT NULL,
  `first_name` text NOT NULL,
  `last_name` text NOT NULL,
  `street_name` text NOT NULL,
  `street_number` int NOT NULL,
  `apartment_number` int DEFAULT NULL,
  `city` text NOT NULL,
  `state` text NOT NULL,
  `zip` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'maria@google.com','Maria','Sanchez','Main Street',123,201,'New York','New York',10101),(2,'john.doe@example.com','John','Doe','Main Street',123,NULL,'Springfield','IL',62701),(3,'jane.smith@example.com','Jane','Smith','Maple Avenue',456,101,'Greenville','SC',29601),(4,'michael.johnson@example.com','Michael','Johnson','Oak Street',789,NULL,'Portland','OR',97201),(5,'ndebroke0@smh.com.au','Cécilia','de Broke','Glendale',2,411,'Västerhaninge','Stockholm',59797),(6,'jghiotto2@upenn.edu','Véronique','Ghiotto','Eagan',792,341,'Viking','Alberta',25750),(7,'ksprowle3@spotify.com','Märta','Sprowle','Manley',2483,141,'Stuttgart','Baden-Württemberg',98158),(8,'cclemonts0@cornell.edu','Thérèsa','Clemonts','Fallview',28,78,'San Antonio','Texas',52953),(9,'gbradnocke1@dailymail.co.uk','Laurène','Bradnocke','Mcbride',899,37,'Mesa','Arizona',74888),(10,'mspybey2@com.com','Adèle','Spybey','Manley',10,217,'Lexington','Kentucky',52811),(11,'dnarracott3@icio.us','Léandre','Narracott','Mandrake',47,134,'San Antonio','Texas',39667),(12,'khanratty4@yahoo.co.jp','Hélèna','Hanratty','Pond',778,52,'Des Moines','Iowa',85708),(13,'eaucutt5@so-net.ne.jp','Léa','Aucutt','Monica',5,316,'New Orleans','Louisiana',13972),(14,'pgleadhell6@ning.com','Lauréna','Gleadhell','Fulton',71,178,'Seattle','Washington',63573),(15,'hdyter7@digg.com','Åke','Dyter','Ryan',21,100,'Pasadena','California',15092),(16,'aibeson8@deviantart.com','Loïc','Ibeson','Birchwood',7615,427,'Cincinnati','Ohio',78389),(17,'kroizin9@mozilla.org','Maïté','Roizin','Morning',213,56,'Columbia','South Carolina',35023),(18,'john@example.com','John','Doe','Main St',123,NULL,'Anytown','CA',12345),(22,'johndoe@gmail.com','John','Doe','Main',1234,NULL,'Kent','Ohio',44240),(23,'joe@gmail.com','Joe','Joe','Main',4319,NULL,'Kent','Ohio',44240),(24,'bob@gmail.com','Bob','Hank','Main',1234,NULL,'Kent','Ohio',44240),(25,'hank@gmail.com','Hank','Smith','Main',1237,2,'Kent','Ohio',44240),(26,'customer@example.com','Giovanni','Herrera','Main St',123,NULL,'Anytown','CA',12345);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_phone_numbers`
--

DROP TABLE IF EXISTS `customer_phone_numbers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_phone_numbers` (
  `phone_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `phone_number` varchar(15) NOT NULL,
  `phone_type` enum('HOME','MOBILE','WORK') NOT NULL,
  PRIMARY KEY (`phone_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `customer_phone_numbers_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_phone_numbers`
--

LOCK TABLES `customer_phone_numbers` WRITE;
/*!40000 ALTER TABLE `customer_phone_numbers` DISABLE KEYS */;
INSERT INTO `customer_phone_numbers` VALUES (1,1,'(888)-555-0001','WORK'),(2,2,'(888)-555-0201','MOBILE'),(3,3,'(888)-555-2222','HOME'),(4,4,'(888)-555-9222','HOME'),(5,1,'(661) 7620912','WORK'),(6,2,'(849) 5966039','HOME'),(7,3,'(423) 6351897','HOME'),(8,4,'(869) 6250181','HOME'),(9,5,'(956) 7868207','HOME'),(10,6,'(572) 1322559','WORK'),(11,7,'(348) 6070836','WORK'),(12,8,'(655) 7670956','MOBILE'),(13,9,'(401) 7226298','MOBILE'),(14,10,'(447) 1415352','HOME'),(15,11,'(556) 1834412','MOBILE'),(16,12,'(906) 6874338','HOME'),(17,13,'(763) 8050652','WORK'),(18,14,'(806) 2884948','WORK'),(19,15,'(921) 4546410','MOBILE'),(20,16,'(121) 8448540','MOBILE'),(21,17,'(646) 1322237','HOME'),(22,18,'123-456-7890','HOME'),(23,18,'456-789-0123','MOBILE'),(24,22,'123-456-7890','HOME'),(25,22,'908-765-4321','MOBILE'),(26,23,'123-456-7890','HOME'),(27,24,'546-743-9132','HOME'),(28,25,'927-138-1203','HOME'),(29,25,'190-129-1029','MOBILE');
/*!40000 ALTER TABLE `customer_phone_numbers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `vehicle_vin` varchar(17) DEFAULT NULL,
  `street_name` text NOT NULL,
  `street_number` int NOT NULL,
  `apartment_number` int DEFAULT NULL,
  `city` text NOT NULL,
  `state` text NOT NULL,
  `zip` int NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `vehicle_vin` (`vehicle_vin`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`vehicle_vin`) REFERENCES `vehicle` (`vin`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'ABC123','Cedar Bark Drive',675,1,'Aurora','Ohio',44202,'2024-04-19','19:18:48'),(2,1,'ABC123','Summit St.',111,3,'Kent','Ohio',44240,'2024-04-20','01:58:32'),(3,1,'ABC123','Summit St.',111,3,'Kent','Ohio',44240,'2024-04-20','02:05:09'),(4,1,'ABC123','Summit St.',111,3,'Kent','Ohio',44240,'2024-04-20','02:05:21'),(5,1,'ABC123','Main Street',123,1,'Anytown','Maryland',86753,'2024-04-20','18:18:30'),(6,1,'ABC123','Ur',1,1,'Mum','Lol',69696,'2024-04-20','19:10:53'),(7,1,'ABC123','qwe',123,1,'qwe','qwe',123123,'2024-04-21','04:44:29'),(8,1,'ABC123','qwe',123,1,'qwe','qwe',123123,'2024-04-21','05:00:09'),(9,1,'ABC123','qwe',123,1,'qwe','qwe',123123,'2024-04-21','05:00:22'),(10,1,'ABC123','qwe',123,1,'qwe','qwe',123123,'2024-04-21','05:01:01'),(11,1,'ABC123','asd',123,11,'qwe','qweasd',123123,'2024-04-21','05:12:39'),(12,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:30'),(13,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:32'),(14,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:33'),(15,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:34'),(16,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:35'),(17,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:41'),(18,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:41'),(19,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:41'),(20,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',41212,'2024-04-21','05:19:41'),(21,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',44460,'2024-04-21','05:20:03'),(22,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',44460,'2024-04-21','05:20:22'),(23,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',44460,'2024-04-21','05:20:23'),(24,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',44460,'2024-04-21','05:20:23'),(25,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',44460,'2024-04-21','05:20:25'),(26,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',44460,'2024-04-21','05:20:26'),(27,1,'1HGCR2F35FA016731','main',123,20,'kent','ohio',44460,'2024-04-21','05:20:42'),(28,1,'1HGCR2F35FA016731','main',123,20,'salme','ohio',44460,'2024-04-21','05:21:09'),(29,1,'ABC123','qewqwe',2323,3,'qweqwe','asdasd',123123,'2024-04-21','05:22:27'),(30,1,'1HGCR2F35FA016731','main',123,20,'salem','ohio',44460,'2024-04-21','05:22:38'),(31,1,'1HGCR2F35FA016731','main',123,20,'salem','ohio',44460,'2024-04-21','05:22:42'),(32,1,'1HGCR2F35FA016731','main',123,20,'salem','ohio',44460,'2024-04-21','05:22:43'),(33,1,'1HGCR2F35FA016731','main',123,20,'salem','ohio',44460,'2024-04-21','05:22:43'),(34,1,'ABC123','qewqwe.',2323,3,'qweqwe','asdasd',123123,'2024-04-21','05:23:30'),(35,1,'ABC123','Summit',111,1,'Kent','Ohio',44240,'2024-04-21','05:24:39'),(36,1,'ABC123','Summit St.',111,1,'Kent','Ohio',44240,'2024-04-21','05:24:52'),(37,1,'ABC123','Summit St.',111,55,'Kent','Ohio',44240,'2024-04-21','05:26:06');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ownership`
--

DROP TABLE IF EXISTS `ownership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ownership` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `vehicle_vin` varchar(17) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `vehicle_vin` (`vehicle_vin`),
  CONSTRAINT `fk_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `fk_vehicle_vin` FOREIGN KEY (`vehicle_vin`) REFERENCES `vehicle` (`vin`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ownership`
--

LOCK TABLES `ownership` WRITE;
/*!40000 ALTER TABLE `ownership` DISABLE KEYS */;
INSERT INTO `ownership` VALUES (1,1,'ABC123'),(2,26,'2B3CK3CV2AH757917');
/*!40000 ALTER TABLE `ownership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle` (
  `vin` varchar(17) NOT NULL,
  `year` int NOT NULL,
  `color` text NOT NULL,
  `mileage` int NOT NULL,
  `make` text NOT NULL,
  `model` text NOT NULL,
  `type` text NOT NULL,
  `mpg-city` int NOT NULL,
  `mpg-hwy` int NOT NULL,
  `msrp` int NOT NULL,
  PRIMARY KEY (`vin`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES ('1C6RR7LT4DS675829',2013,'Blue',44850,'Ram','1500','Truck',14,20,28995),('1FTFW1ET8BFC08090',2011,'Gray',71230,'Ford','F-150','Truck',16,21,31995),('1HGCR2F35FA016731',2015,'Silver',35890,'Honda','Accord','Sedan',27,36,23900),('2B3CK3CV2AH757917',1963,'Crimson',18378,'Austin','Mini','Coupe',19,45,56919),('2C3CDXCT7FH500278',2015,'White',29500,'Dodge','Charger','Sedan',19,31,31995),('ABC123',2022,'Blue',15000,'Toyota','Camry','Sedan',25,35,25000),('JHMZE2H31DS895929',2002,'Aquamarine',188820,'BMW','5 Series','Sedan',21,29,29329),('JTC8F4CL2Z2904612',2020,'grey',5500,'Ford','Fusion','Sedan',28,36,23170),('JTHKD5BH0A2177496',2010,'Black',55670,'Lexus','HS 250h','Sedan',35,34,34995),('SCBDC47L29C972763',1993,'Khaki',29114,'Chevrolet','Lumina','Sedan',21,29,38905),('WUADUAFG1CN342714',2002,'Grey',213762,'Audi','S6','Sedan',14,21,53958),('Y5HT3G9RK82CJVXW6',2018,'grey',3400,'Honda','Civic','Sedan',30,38,19740);
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_features`
--

DROP TABLE IF EXISTS `vehicle_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_features` (
  `feature_id` int NOT NULL AUTO_INCREMENT,
  `vehicle_vin` varchar(17) DEFAULT NULL,
  `feature` text NOT NULL,
  PRIMARY KEY (`feature_id`),
  KEY `vehicle_vin` (`vehicle_vin`),
  CONSTRAINT `vehicle_features_ibfk_1` FOREIGN KEY (`vehicle_vin`) REFERENCES `vehicle` (`vin`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_features`
--

LOCK TABLES `vehicle_features` WRITE;
/*!40000 ALTER TABLE `vehicle_features` DISABLE KEYS */;
INSERT INTO `vehicle_features` VALUES (1,'ABC123','Feature 1'),(2,'ABC123','Feature 2'),(3,'1HGCR2F35FA016731','navigation system'),(4,'1HGCR2F35FA016731','backup camera'),(5,'1C6RR7LT4DS675829','4-wheel drive'),(6,'1C6RR7LT4DS675829','towing package'),(7,'JTHKD5BH0A2177496','hybrid engine'),(8,'JTHKD5BH0A2177496','leather interior'),(9,'2C3CDXCT7FH500278','remote start'),(10,'2C3CDXCT7FH500278','sport suspension'),(11,'1FTFW1ET8BFC08090','extended cab'),(12,'1FTFW1ET8BFC08090','bed liner'),(13,'Y5HT3G9RK82CJVXW6','backup camera'),(14,'Y5HT3G9RK82CJVXW6','heated seats'),(15,'JTC8F4CL2Z2904612','remote start');
/*!40000 ALTER TABLE `vehicle_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_photos`
--

DROP TABLE IF EXISTS `vehicle_photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_photos` (
  `photo_id` int NOT NULL AUTO_INCREMENT,
  `vehicle_vin` varchar(17) DEFAULT NULL,
  `photo` text NOT NULL,
  PRIMARY KEY (`photo_id`),
  KEY `vehicle_vin` (`vehicle_vin`),
  CONSTRAINT `vehicle_photos_ibfk_1` FOREIGN KEY (`vehicle_vin`) REFERENCES `vehicle` (`vin`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 COMMENT='photo is saved as a link';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_photos`
--

LOCK TABLES `vehicle_photos` WRITE;
/*!40000 ALTER TABLE `vehicle_photos` DISABLE KEYS */;
INSERT INTO `vehicle_photos` VALUES (1,'ABC123','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQV_GyY9772XT1SBrRdVAvv4kz2pQbvXV3V6gix8dUh3g2QYQB'),(2,'ABC123','https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.edmunds.com%2Ftoyota%2Fcamry-hybrid%2F2022%2Freview%2F&psig=AOvVaw3TaDMlj2RB4j2YCxQ5f1L3&ust=1713636093822000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIiW24buzoUDFQAAAAAdAAAAABAH'),(3,'SCBDC47L29C972763','https://images.nettiauto.com/live/2023/05/30/2edaf4723b37f7aa-large.jpg'),(4,'JHMZE2H31DS895929','https://static.cargurus.com/images/site/2009/09/27/06/59/2002_bmw_530i-pic-5621-1600x1200.jpeg'),(5,'2B3CK3CV2AH757917','https://images.classic.com/vehicles/0f5b1aabad7a3205b249bc601ad85c1f5213ce1c.jpg?ar=16%3A9&fit=crop&w=600'),(6,'WUADUAFG1CN342714','https://media.carsandbids.com/cdn-cgi/image/width=2080,quality=70/d9b636c2ec84ddc3bc7f2eb32861b39bdd5f9683/photos/3zm2M7wB-rWXgTT4yfg-(edit).jpg?t=169075166472'),(7,'1HGCR2F35FA016731','https://cars.usnews.com/static/images/Auto/izmo/Colors/honda_15accordexlv69a_alabastersilvermetallic.jpg'),(8,'1C6RR7LT4DS675829','https://i.pinimg.com/originals/d5/92/16/d59216492cfeb17dea8d741737745874.jpg'),(9,'JTHKD5BH0A2177496','https://www.motortrend.com/uploads/sites/5/2009/11/2010-lexus-HS-250h-front-three-quarters-view-static.jpg'),(10,'2C3CDXCT7FH500278','https://www.carpro.com/hubfs/car-review-blog/review_70238_1.jpg#keepProtocol'),(11,'1FTFW1ET8BFC08090','https://www.cars.com/i/large/in/v2/stock_photos/6aa4b84e-63df-4b7a-b589-5234d8a7d059/654e06e3-2afd-4cf7-9ad7-72ba9e116f6c.png'),(12,'Y5HT3G9RK82CJVXW6','https://edgecast-img.yahoo.net/mysterio/api/E27CFF5C773BF85E91E9D1129AFCC164333EAB53BB111DEB833624F3CED39C35/autoblog/resizefill_w660_h372;quality_80;format_webp;cc_31536000;/https://s.aolcdn.com/commerce/autodata/images/CAC80HOC021B121001.jpg'),(13,'JTC8F4CL2Z2904612','https://edgecast-img.yahoo.net/mysterio/api/C4A5DCD0F6512F14C88B112733DC604FAB5E403244052959706EE5DAAC709737/autoblog/resizefill_w660_h372;quality_80;format_webp;cc_31536000;/https://s.aolcdn.com/commerce/autodata/images/USC90FOC201B021001.jpg');
/*!40000 ALTER TABLE `vehicle_photos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-29 22:59:18
