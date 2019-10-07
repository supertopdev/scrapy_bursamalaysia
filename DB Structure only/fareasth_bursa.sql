-- phpMyAdmin SQL Dump
-- version 4.0.10.14
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Sep 15, 2019 at 04:13 PM
-- Server version: 5.5.52-cll
-- PHP Version: 5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `fareasth_bursa`
--

-- --------------------------------------------------------

--
-- Table structure for table `alerts`
--

CREATE TABLE IF NOT EXISTS `alerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(200) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=164 ;

-- --------------------------------------------------------

--
-- Table structure for table `annc`
--

CREATE TABLE IF NOT EXISTS `annc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) NOT NULL,
  `category` varchar(100) NOT NULL,
  `date_of_publishing` varchar(20) NOT NULL,
  `direct_linktoarticle_iframe` varchar(500) NOT NULL,
  `linktoarticle_on_indexpage` varchar(500) NOT NULL,
  `short_description` varchar(1000) NOT NULL,
  `html` text NOT NULL,
  `attachment_location_ondisk` varchar(1000) NOT NULL,
  `reference_no` varchar(100) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  `active` int(11) NOT NULL DEFAULT '1' COMMENT '1->Active,0->inactive',
  `crawled` tinyint(1) DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=482133 ;

-- --------------------------------------------------------

--
-- Table structure for table `announcements`
--

CREATE TABLE IF NOT EXISTS `announcements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(1000) DEFAULT NULL,
  `category` varchar(100) NOT NULL,
  `date_of_publishing` varchar(20) NOT NULL,
  `direct_linktoarticle_iframe` varchar(500) NOT NULL,
  `linktoarticle_on_indexpage` varchar(500) NOT NULL,
  `short_description` varchar(1000) NOT NULL,
  `html` longtext,
  `attachment_location_ondisk` varchar(1000) NOT NULL,
  `reference_no` varchar(100) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '1',
  `active` int(11) NOT NULL DEFAULT '1' COMMENT '1->Active,0->inactive',
  `crawled` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4443 ;

-- --------------------------------------------------------

--
-- Table structure for table `annualreports`
--

CREATE TABLE IF NOT EXISTS `annualreports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(4) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date` varchar(45) NOT NULL,
  `short_description` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `image_file_name` varchar(255) DEFAULT NULL,
  `image_file_size` int(11) DEFAULT NULL,
  `image_content_type` varchar(255) DEFAULT NULL,
  `image_updated_at` timestamp NULL DEFAULT NULL,
  `pdf_file_name` varchar(255) DEFAULT NULL,
  `pdf_file_size` int(11) DEFAULT NULL,
  `pdf_content_type` varchar(255) DEFAULT NULL,
  `pdf_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE IF NOT EXISTS `applications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vaccancyid` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `dob` varchar(45) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `education` varchar(500) NOT NULL,
  `contactno` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `resume_file_name` varchar(255) DEFAULT NULL,
  `resume_file_size` int(11) DEFAULT NULL,
  `resume_content_type` varchar(255) DEFAULT NULL,
  `resume_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `banners`
--

CREATE TABLE IF NOT EXISTS `banners` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `display_order` int(11) NOT NULL,
  `banner_text1` varchar(200) NOT NULL,
  `banner_text2` varchar(200) NOT NULL,
  `active` tinyint(4) NOT NULL DEFAULT '1',
  `bannerimage_file_name` varchar(255) DEFAULT NULL,
  `bannerimage_file_size` int(11) DEFAULT NULL,
  `bannerimage_content_type` varchar(255) DEFAULT NULL,
  `bannerimage_updated_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `brandslistings`
--

CREATE TABLE IF NOT EXISTS `brandslistings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `short_description` varchar(200) NOT NULL,
  `url` varchar(100) DEFAULT NULL,
  `display_order` tinyint(4) DEFAULT '1',
  `active` tinyint(4) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `bannerimage_file_name` varchar(255) DEFAULT NULL,
  `bannerimage_file_size` int(11) DEFAULT NULL,
  `bannerimage_content_type` varchar(255) DEFAULT NULL,
  `bannerimage_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `corebusinesses`
--

CREATE TABLE IF NOT EXISTS `corebusinesses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `short_description` varchar(200) NOT NULL,
  `url` varchar(100) NOT NULL,
  `display_order` tinyint(4) NOT NULL DEFAULT '1',
  `active` tinyint(4) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `corebusinessimage_file_name` varchar(255) DEFAULT NULL,
  `corebusinessimage_file_size` int(11) DEFAULT NULL,
  `corebusinessimage_content_type` varchar(255) DEFAULT NULL,
  `corebusinessimage_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `corporate_stockinfo`
--

CREATE TABLE IF NOT EXISTS `corporate_stockinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stock_name` varchar(500) NOT NULL,
  `stock_code` varchar(100) NOT NULL,
  `listing` varchar(500) NOT NULL,
  `sector` varchar(500) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=641 ;

-- --------------------------------------------------------

--
-- Table structure for table `crawledannounces`
--

CREATE TABLE IF NOT EXISTS `crawledannounces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `announcement_id` int(11) NOT NULL DEFAULT '0',
  `title` varchar(500) NOT NULL,
  `category` varchar(100) NOT NULL,
  `company_name` varchar(100) NOT NULL DEFAULT 'FAR EAST HOLDINGS BERHAD',
  `date_of_publishing` date NOT NULL,
  `html` text NOT NULL,
  `reference_no` varchar(100) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '1' COMMENT '1->Active,0->inactive',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17314 ;

-- --------------------------------------------------------

--
-- Table structure for table `eventcalendar`
--

CREATE TABLE IF NOT EXISTS `eventcalendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `title` varchar(200) NOT NULL,
  `date` varchar(200) NOT NULL,
  `time` varchar(100) NOT NULL,
  `venue` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=54 ;

-- --------------------------------------------------------

--
-- Table structure for table `feedbacks`
--

CREATE TABLE IF NOT EXISTS `feedbacks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `company_address` text NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `post_code` varchar(45) NOT NULL,
  `country` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contact_number` varchar(45) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `questions_comments` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `manufacturing_processeslistings`
--

CREATE TABLE IF NOT EXISTS `manufacturing_processeslistings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `short_description` varchar(200) NOT NULL,
  `display_order` int(11) NOT NULL,
  `active` tinyint(4) NOT NULL,
  `type` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `bannerimage_file_name` varchar(255) DEFAULT NULL,
  `bannerimage_file_size` int(11) DEFAULT NULL,
  `bannerimage_content_type` varchar(255) DEFAULT NULL,
  `bannerimage_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `manufacturing_slidingbanners`
--

CREATE TABLE IF NOT EXISTS `manufacturing_slidingbanners` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `display_order` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `type` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `bannerimage_file_name` varchar(255) DEFAULT NULL,
  `bannerimage_file_size` int(11) DEFAULT NULL,
  `bannerimage_content_type` varchar(255) DEFAULT NULL,
  `bannerimage_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `menus`
--

CREATE TABLE IF NOT EXISTS `menus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rootid` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `url` varchar(100) NOT NULL,
  `type` enum('link','section') NOT NULL,
  `active` enum('1','0') NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE IF NOT EXISTS `migrations` (
  `migration` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pages`
--

CREATE TABLE IF NOT EXISTS `pages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL,
  `published` tinyint(4) NOT NULL DEFAULT '1',
  `page_title` text NOT NULL,
  `left_block1_title` text NOT NULL,
  `left_block1_content` text NOT NULL,
  `left_block2_title` text NOT NULL,
  `left_block2_content` text NOT NULL,
  `left_block3_title` text NOT NULL,
  `left_block3_content` text NOT NULL,
  `right_block1_title` text NOT NULL,
  `right_block1_content` text NOT NULL,
  `right_block2_title` text NOT NULL,
  `right_block2_content` text NOT NULL,
  `right_block3_title` text NOT NULL,
  `right_block3_content` text NOT NULL,
  `left_inner_block` int(11) NOT NULL DEFAULT '0',
  `left_inner_block_title1` text NOT NULL,
  `left_inner_block_content1` text NOT NULL,
  `left_inner_block_title2` text NOT NULL,
  `left_inner_block_content2` text NOT NULL,
  `left_inner_block_title3` text NOT NULL,
  `left_inner_block_content3` text NOT NULL,
  `left_inner_block_title4` text NOT NULL,
  `left_inner_block_content4` text NOT NULL,
  `left_inner_block_title5` text NOT NULL,
  `left_inner_block_content5` text NOT NULL,
  `left_inner_block_title6` text NOT NULL,
  `left_inner_block_content6` text NOT NULL,
  `left_inner_block_title7` text NOT NULL,
  `left_inner_block_content7` text NOT NULL,
  `left_inner_block_title8` text NOT NULL,
  `left_inner_block_content8` text NOT NULL,
  `left_inner_block_title9` text NOT NULL,
  `left_inner_block_content9` text NOT NULL,
  `left_inner_block_title10` text NOT NULL,
  `left_inner_block_content10` text NOT NULL,
  `left_inner_block_title11` text NOT NULL,
  `left_inner_block_content11` text NOT NULL,
  `left_inner_block_title12` text NOT NULL,
  `left_inner_block_content12` text NOT NULL,
  `left_inner_block_title13` text NOT NULL,
  `left_inner_block_content13` text NOT NULL,
  `left_inner_block_title14` text NOT NULL,
  `left_inner_block_content14` text NOT NULL,
  `left_inner_block_title15` text NOT NULL,
  `left_inner_block_content15` text NOT NULL,
  `left_inner_block_title16` text NOT NULL,
  `left_inner_block_content16` text NOT NULL,
  `left_inner_block_title17` text NOT NULL,
  `left_inner_block_content17` text NOT NULL,
  `left_inner_block_title18` text NOT NULL,
  `left_inner_block_content18` text NOT NULL,
  `left_inner_block_title19` text NOT NULL,
  `left_inner_block_content19` text NOT NULL,
  `left_inner_block_title20` text NOT NULL,
  `left_inner_block_title21` text NOT NULL,
  `left_inner_block_content20` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1275 ;

-- --------------------------------------------------------

--
-- Table structure for table `password_reminders`
--

CREATE TABLE IF NOT EXISTS `password_reminders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(500) NOT NULL,
  `token` varchar(500) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `pdf`
--

CREATE TABLE IF NOT EXISTS `pdf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(4) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pdf_file_name` varchar(255) DEFAULT NULL,
  `pdf_file_size` int(11) DEFAULT NULL,
  `pdf_content_type` varchar(255) DEFAULT NULL,
  `pdf_updated_at` timestamp NULL DEFAULT NULL,
  `type` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=150 ;

-- --------------------------------------------------------

--
-- Table structure for table `pressreleases`
--

CREATE TABLE IF NOT EXISTS `pressreleases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(4) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date` varchar(45) NOT NULL,
  `citation` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `read_more` tinyint(4) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `image_file_name` varchar(255) DEFAULT NULL,
  `image_file_size` int(11) DEFAULT NULL,
  `image_content_type` varchar(255) DEFAULT NULL,
  `image_updated_at` timestamp NULL DEFAULT NULL,
  `pdf_file_name` varchar(255) DEFAULT NULL,
  `pdf_file_size` int(11) DEFAULT NULL,
  `pdf_content_type` varchar(255) DEFAULT NULL,
  `pdf_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `profiles`
--

CREATE TABLE IF NOT EXISTS `profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `name` varchar(100) NOT NULL,
  `date` varchar(200) NOT NULL,
  `content` text NOT NULL,
  `type` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=79 ;

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE IF NOT EXISTS `reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(4) NOT NULL,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `date` varchar(45) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `image_file_name` varchar(255) NOT NULL,
  `image_file_size` int(11) NOT NULL,
  `image_content_type` varchar(255) NOT NULL,
  `image_updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pdf_file_name` varchar(255) DEFAULT NULL,
  `pdf_file_size` int(11) DEFAULT NULL,
  `pdf_content_type` varchar(255) DEFAULT NULL,
  `pdf_updated_at` timestamp NULL DEFAULT NULL,
  `pdf2_file_name` varchar(100) NOT NULL,
  `pdf2_file_size` int(11) NOT NULL,
  `pdf2_content_type` varchar(255) NOT NULL,
  `pdf2_updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pdf3_file_name` varchar(255) NOT NULL,
  `pdf3_file_size` int(11) NOT NULL,
  `pdf3_content_type` varchar(255) NOT NULL,
  `pdf3_updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pdf4_file_name` varchar(255) NOT NULL,
  `pdf4_file_size` int(11) NOT NULL,
  `pdf4_content_type` varchar(255) NOT NULL,
  `pdf4_updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `type` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=132 ;

-- --------------------------------------------------------

--
-- Table structure for table `shares`
--

CREATE TABLE IF NOT EXISTS `shares` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `shareheld` varchar(100) NOT NULL,
  `shareheld2` varchar(110) NOT NULL,
  `date` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `company` varchar(500) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(500) NOT NULL,
  `password` varchar(200) NOT NULL,
  `role` int(11) NOT NULL,
  `accesslist` text NOT NULL,
  `active` enum('1','0') NOT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `avatar_file_name` varchar(255) DEFAULT NULL,
  `avatar_file_size` int(11) DEFAULT NULL,
  `avatar_content_type` varchar(255) DEFAULT NULL,
  `avatar_updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;

-- --------------------------------------------------------

--
-- Table structure for table `vaccancies`
--

CREATE TABLE IF NOT EXISTS `vaccancies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_title` varchar(100) NOT NULL,
  `company` varchar(200) NOT NULL,
  `job_location` varchar(200) NOT NULL,
  `post_date` varchar(100) NOT NULL,
  `responsibilities_content` text NOT NULL,
  `requirements_content` text NOT NULL,
  `footer_content` text NOT NULL,
  `active` tinyint(4) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
