-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Sep 15, 2019 at 04:17 PM
-- Server version: 5.5.52-cll
-- PHP Version: 5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `fareasth_yahoo`
--

-- --------------------------------------------------------

--
-- Table structure for table `yahoo`
--

CREATE TABLE IF NOT EXISTS `yahoo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `volume` varchar(12) NOT NULL,
  `avg_volume` varchar(12) NOT NULL,
  `prev_close` varchar(10) NOT NULL,
  `open` varchar(10) NOT NULL,
  `bid` varchar(10) NOT NULL,
  `ask` varchar(10) NOT NULL,
  `1y_target_est` varchar(15) NOT NULL,
  `beta` varchar(15) NOT NULL,
  `next_earnings_date` varchar(15) NOT NULL,
  `days_range` varchar(15) NOT NULL,
  `52wk_range` varchar(15) NOT NULL,
  `market_cap` varchar(15) NOT NULL,
  `p_e` varchar(15) NOT NULL,
  `eps` varchar(15) NOT NULL,
  `div_yield` varchar(15) NOT NULL,
  `created_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=101340 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
