use CAP;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `product_name` varchar(30) NOT NULL COMMENT '이름',
  `product_price` INTEGER NOT NULL DEFAULT 0 COMMENT '상품가격',
  `product_num` INTEGER NOT NULL DEFAULT 0 COMMENT '상품수량',
  PRIMARY KEY (`product_name`)
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

SET FOREIGN_KEY_CHECKS=1;

show tables;