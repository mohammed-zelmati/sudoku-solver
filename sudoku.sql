CREATE TABLE `grilles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `grid` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `grilles` WRITE;
INSERT INTO `grilles` VALUES 
(1,'_729___3_\n__1__6_8_\n____4__6_\n96___41_8\n_487_5_96\n__56_8__3\n___4_2_1_\n85__6_327\n1__85____'),
(2,'7__92_4__\n______7__\n__4__8312\n4____25__\n2___1___3\n__85____4\n8432__6__\n__5______\n__2_64__5'),
(3,'__9_85_63\n_7_96____\n5_1__4___\n__67_3__4\n_4_21_39_\n8___9__57\n9845__6__\n__7649_3_\n61__2__4_'),
(4,'3______8_\n1__6_3__2\n56_______\n_8_1__97_\n___5_____\n2_9__4___\n__1___62_\n_______43\n_7__5_1__'),
(5,'__9_6____\n___3___1_\n_45_1___6\n_____82__\n_61_3___5\n7________\n9___4____\n_742__5__\n3_______7');
/*!40000 ALTER TABLE `grilles` ENABLE KEYS */;
UNLOCK TABLES;

