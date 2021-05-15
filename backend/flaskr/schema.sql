use tps;
SET FOREIGN_KEY_CHECKS = 0

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `product_id` INTEGER NOT NULL auto_increment COMMENT '상품아이디',
  `product_name` varchar(30) NOT NULL COMMENT '이름',
  `product_price` INTEGER NOT NULL DEFAULT 0 COMMENT '상품가격',
  `product_sales` INTEGER NOT NULL DEFAULT 0 COMMENT '상품판매가',
  `product_num` INTEGER NOT NULL DEFAULT 0 COMMENT '상품수량',
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `order_type` boolean NOT NULL COMMENT '요청구분',
  `order_time` TIMESTAMP NOT NULL COMMENT '주문시간',
  `product_name` varchar(30) NOT NULL COMMENT '상품명',
  `order_num` INTEGER NOT NULL DEFAULT 0 COMMENT '주문수량',
  PRIMARY KEY (`product_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for temp
-- ----------------------------
DROP TABLE IF EXISTS `temp`;
CREATE TABLE `temp` (
  `upper` FLOAT NOT NULL COMMENT '상한온도',
  `lower` FLOAT NOT NULL COMMENT '하한온도',
  PRIMARY KEY (`upper`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS=1;

show tables;