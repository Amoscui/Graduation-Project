CREATE TABLE `Admin` (
  `name` varchar(15) CHARACTER SET utf8 NOT NULL,
  `password` varchar(45) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `judgeOperate` (
  `isCorrect` varchar(10) CHARACTER SET utf8 NOT NULL,
  `TestNum_3` int(11) NOT NULL,
  `titleNo_3` int(11) NOT NULL,
  `drawnum` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`drawnum`),
  KEY `TestNum_3` (`TestNum_3`),
  KEY `titleNo_3` (`titleNo_3`),
  CONSTRAINT `TestNum_3` FOREIGN KEY (`TestNum_3`) REFERENCES `TestRecord` (`TestNum`),
  CONSTRAINT `titleNo_3` FOREIGN KEY (`titleNo_3`) REFERENCES `true-falseItem` (`titleNo`)
) ENGINE=InnoDB AUTO_INCREMENT=162 DEFAULT CHARSET=latin1;

CREATE TABLE `ManyChooseItem` (
  `content` varchar(100) CHARACTER SET utf8 NOT NULL,
  `chooseA` varchar(100) CHARACTER SET utf8 NOT NULL,
  `answer` varchar(45) CHARACTER SET utf8 NOT NULL,
  `titleNo` int(11) NOT NULL,
  `chooseB` varchar(100) CHARACTER SET utf8 NOT NULL,
  `chooseC` varchar(100) CHARACTER SET utf8 NOT NULL,
  `chooseD` varchar(100) CHARACTER SET utf8 NOT NULL,
  `category` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`titleNo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `many-chooseOperate` (
  `titleNo_2` int(11) NOT NULL,
  `isCorrect` varchar(10) CHARACTER SET utf8 NOT NULL,
  `TestNum_2` int(11) NOT NULL,
  `drawnum` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`drawnum`),
  KEY `titleNo_2` (`TestNum_2`),
  KEY `titleNo_idx` (`titleNo_2`),
  CONSTRAINT `TestNum_2` FOREIGN KEY (`TestNum_2`) REFERENCES `TestRecord` (`TestNum`),
  CONSTRAINT `titleNo_2` FOREIGN KEY (`titleNo_2`) REFERENCES `ManyChooseItem` (`titleNo`)
) ENGINE=InnoDB AUTO_INCREMENT=341 DEFAULT CHARSET=latin1;

CREATE TABLE `OneChooseItem` (
  `content` varchar(300) NOT NULL,
  `chooseA` varchar(300) NOT NULL,
  `answer` char(2) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `titleNo` int(11) NOT NULL,
  `chooseB` varchar(45) NOT NULL,
  `chooseC` varchar(45) NOT NULL,
  `chooseD` varchar(45) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`titleNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `one-chooseOperate` (
  `titleNo_1` int(11) NOT NULL,
  `isCorrect` varchar(10) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `TestNum_1` int(11) NOT NULL,
  `drawnum` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`drawnum`),
  KEY `titleNo` (`titleNo_1`),
  KEY `TestNum_1` (`TestNum_1`),
  CONSTRAINT `TestNum_1` FOREIGN KEY (`TestNum_1`) REFERENCES `TestRecord` (`TestNum`),
  CONSTRAINT `titleNo_1` FOREIGN KEY (`titleNo_1`) REFERENCES `OneChooseItem` (`titleNo`)
) ENGINE=InnoDB AUTO_INCREMENT=401 DEFAULT CHARSET=latin1;

CREATE TABLE `Search` (
  `id` varchar(15) NOT NULL,
  `TestNum` int(11) NOT NULL,
  `num` int(11) NOT NULL AUTO_INCREMENT,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`num`),
  KEY `id` (`id`),
  KEY `TestNum_idx` (`TestNum`),
  CONSTRAINT `TestNum` FOREIGN KEY (`TestNum`) REFERENCES `TestRecord` (`TestNum`),
  CONSTRAINT `id` FOREIGN KEY (`id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

CREATE TABLE `TestRecord` (
  `TestNum` int(11) NOT NULL AUTO_INCREMENT,
  `achieveMent` varchar(1000) DEFAULT NULL,
  `startTime` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `endTime` timestamp(6) NULL DEFAULT NULL,
  PRIMARY KEY (`TestNum`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=latin1;

CREATE TABLE `true-falseItem` (
  `titleNo` int(11) NOT NULL,
  `content` varchar(150) CHARACTER SET utf8 NOT NULL,
  `answer` varchar(45) CHARACTER SET utf8 NOT NULL,
  `category` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`titleNo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `User` (
  `name` varchar(15) NOT NULL,
  `password` varchar(45) NOT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `sex` char(1) NOT NULL DEFAULT '0',
  `tel` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
