
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for problem_sim
-- ----------------------------
CREATE TABLE `problem_sim` (
  `pid1` int(11) NOT NULL,
  `pid2` int(11) NOT NULL,
  `sim` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
