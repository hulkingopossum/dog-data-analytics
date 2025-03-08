-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 06, 2025 at 11:09 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dog-data`
--

-- --------------------------------------------------------

--
-- Table structure for table `breed`
--

DROP TABLE IF EXISTS `breed`;
CREATE TABLE IF NOT EXISTS `breed` (
  `id` int NOT NULL AUTO_INCREMENT,
  `breed_name` varchar(255) DEFAULT NULL,
  `breed_age` int DEFAULT NULL,
  `breed_group` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `dogs`
--

DROP TABLE IF EXISTS `dogs`;
CREATE TABLE IF NOT EXISTS `dogs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `breed_id` int DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `owner_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  KEY `breed_id` (`breed_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lifespan`
--

DROP TABLE IF EXISTS `lifespan`;
CREATE TABLE IF NOT EXISTS `lifespan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `breed_id` int DEFAULT NULL,
  `min_lifespan` int DEFAULT NULL,
  `max_lifespan` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `breed_id` (`breed_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `owners`
--

DROP TABLE IF EXISTS `owners`;
CREATE TABLE IF NOT EXISTS `owners` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
