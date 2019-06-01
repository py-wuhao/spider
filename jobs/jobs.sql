/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 100121
Source Host           : localhost:3306
Source Database       : jobs

Target Server Type    : MYSQL
Target Server Version : 100121
File Encoding         : 65001

Date: 2019-06-01 21:37:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for job
-- ----------------------------
DROP TABLE IF EXISTS `job`;
CREATE TABLE `job` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hash_url` varchar(64) COLLATE utf8_german2_ci DEFAULT NULL,
  `job_url` varchar(255) COLLATE utf8_german2_ci DEFAULT NULL,
  `name` varchar(64) COLLATE utf8_german2_ci DEFAULT NULL,
  `max_salary` int(11) DEFAULT NULL,
  `min_salary` int(11) DEFAULT NULL,
  `settlement` varchar(16) COLLATE utf8_german2_ci DEFAULT NULL,
  `address` varchar(128) COLLATE utf8_german2_ci DEFAULT NULL,
  `company_name` varchar(128) COLLATE utf8_german2_ci DEFAULT NULL,
  `job_info` text COLLATE utf8_german2_ci,
  `work_year` varchar(64) COLLATE utf8_german2_ci DEFAULT NULL,
  `experience` varchar(16) COLLATE utf8_german2_ci DEFAULT NULL,
  `publish_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hash_url` (`hash_url`) USING HASH
) ENGINE=MyISAM AUTO_INCREMENT=13852 DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci;
