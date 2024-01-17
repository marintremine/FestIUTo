INSERT INTO groupe (idG, nomG, descriptionG) VALUES
  (1, 'Nirvana', 'Grunge Rock américain'),
  (2, 'Pink Floyd', 'Rock psychédélique du Royaume-Uni'),
  (3, 'The Beatles', 'Rock britannique'),
  (4, 'The Rolling Stones', 'Rock britannique'),
  (5, 'The Who', 'Rock britannique'),
  (6, 'The Doors', 'Rock américain'),
  (7, 'The Weekend', 'Artiste canadien pop / new wave');

INSERT INTO style (idS_1,idS_2, nomS) VALUES
  (1, NULL, 'Rock'),
  (2, 1 ,'Rock psychédélique'),
  (3, 1,'Rock progressif'),
  (4, 1,'Rock alternatif'),
  (5, 1,'Grunge'),
  (6, NULL,'Pop'),
  (7, 6,'New wave');


INSERT INTO posseder (idG, idS) VALUES
  (1, 1),
  (1, 5),
  (2, 1),
  (2, 2),
  (2, 3),
  (3, 1),
  (3, 3),
  (4, 1),
  (4, 3),
  (5, 1),
  (5, 3),
  (6, 1),
  (6, 3),
  (7, 6),
  (7, 7);

INSERT INTO artiste (ida, noma, prenoma, dateNaissA, idG) VALUES
  (1, 'Cobain', 'Kurt', '1967-02-20', 1),
  (2, 'Grohl', 'Dave', '1969-01-14', 1),
  (3, 'Novoselic', 'Krist', '1965-05-16', 1),
  (4, 'Waters', 'Roger', '1943-09-06', 2),
  (5, 'Gilmour', 'David', '1946-03-06', 2),
  (6, 'Mason', 'Nick', '1944-01-27', 2),
  (7, 'Wright', 'Richard', '1943-07-28', 2),
  (8, 'Lennon', 'John', '1940-10-09', 3),
  (9, 'McCartney', 'Paul', '1942-06-18', 3),
  (10, 'Harrison', 'George', '1943-02-25', 3),
  (11, 'Starr', 'Ringo', '1940-07-07', 3),
  (12, 'Jagger', 'Mick', '1943-07-26', 4),
  (13, 'Richards', 'Keith', '1943-12-18', 4),
  (14, 'Wood', 'Ronnie', '1947-06-01', 4),
  (15, 'Jones', 'Brian', '1942-02-28', 4),
  (16, 'Townshend', 'Pete', '1945-05-19', 5),
  (17, 'Daltrey', 'Roger', '1944-03-01', 5),
  (18, 'Entwistle', 'John', '1944-10-09', 5),
  (19, 'Moon', 'Keith', '1946-08-23', 5),
  (20, 'Morrison', 'Jim', '1943-12-08', 6),
  (21, 'Manzarek', 'Ray', '1939-02-12', 6),
  (22, 'Krieger', 'Robby', '1946-01-08', 6),
  (23, 'Densmore', 'John', '1944-12-01', 6),
  (24, 'Tesfaye', 'Abel', '1990-02-16', 7);

INSERT INTO instrument (idI, nomI) VALUES
  (1, 'Guitare'),
  (2, 'Basse'),
  (3, 'Batterie'),
  (4, 'Chant'),
  (5, 'Clavier'),
  (6, 'Piano'),
  (7, 'Synthétiseur'),
  (8, 'Saxophone'),
  (9, 'Trompette'),
  (10, 'Violon'),
  (11, 'Violoncelle'),
  (12, 'Flute'),
  (13, 'Harpe'),
  (14, 'Trombone'),
  (15, 'Tuba'),
  (16, 'Accordéon'),
  (17, 'Banjo'),
  (18, 'Harmonica'),
  (19, 'Orgue'),
  (20, 'Percussions'),
  (21, 'Sitar'),
  (22, 'Ukulélé'),
  (23, 'Xylophone');

INSERT INTO jouer (idI, ida) VALUES
  (1, 1),
  (2, 1),
  (3, 1),
  (4, 1),
  (1, 2),
  (3, 2),
  (4, 2),
  (1, 3),
  (2, 3),
  (3, 3),
  (4, 3),
  (1, 4),
  (4, 4),
  (1, 5),
  (2, 5),
  (3, 5),
  (4, 5),
  (1, 6),
  (2, 6),
  (3, 6),
  (4, 6),
  (1, 7),
  (2, 7),
  (3, 7),
  (4, 7),
  (1, 8),
  (4, 8),
  (1, 9),
  (4, 9),
  (1, 10),
  (4, 10),
  (1, 11),
  (4, 11),
  (1, 12),
  (4, 12),
  (1, 13),
  (4, 13),
  (1, 14),
  (4, 14),
  (1, 15),
  (4, 15),
  (1, 16),
  (4, 16),
  (1, 17),
  (4, 17),
  (1, 18),
  (4, 18),
  (1, 19),
  (4, 19),
  (1, 20),
  (4, 20),
  (1, 21),
  (4, 21),
  (1, 22),
  (4, 22),
  (1, 23),
  (4, 23),
  (1, 24),
  (4, 24);

INSERT INTO reseau_social (idRs, nomReseau, urlLogoReseau) VALUES
  (1, 'Facebook', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Facebook_Logo_%282019%29.png/1200px-Facebook_Logo_%282019%29.png'),
  (2, 'X', 'https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg'),
  (3, 'Instagram', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/1200px-Instagram_logo_2016.svg.png'),
  (4, 'Youtube', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/1200px-YouTube_social_white_squircle_%282017%29.svg.png');

INSERT INTO lien_rs (idG, idRs, pos, pseudo, urlReseau) VALUES
  (1, 1, 1, 'Nirvana', 'https://www.facebook.com/Nirvana/'),
  (1, 4, 2, 'Nirvana', 'https://www.youtube.com/Nirvana/'),
  (2, 1, 1, 'Pink Floyd', 'https://www.facebook.com/PinkFloyd/'),
  (2, 2, 2, 'Pink Floyd', 'https://www.x.com/PinkFloyd/'),
  (2, 3, 3, 'Pink Floyd', 'https://www.instagram.com/PinkFloyd/'),
  (2, 4, 4, 'Pink Floyd', 'https://www.youtube.com/PinkFloyd/'),
  (3, 1, 1, 'The Beatles', 'https://www.facebook.com/TheBeatles/'),
  (3, 2, 2, 'The Beatles', 'https://www.x.com/TheBeatles/'),
  (3, 3, 3, 'The Beatles', 'https://www.instagram.com/TheBeatles/'),
  (3, 4, 4, 'The Beatles', 'https://www.youtube.com/TheBeatles/'),
  (4, 1, 1, 'The Rolling Stones', 'https://www.facebook.com/TheRollingStones/'),
  (4, 2, 2, 'The Rolling Stones', 'https://www.x.com/TheRollingStones/'),
  (4, 3, 3, 'The Rolling Stones', 'https://www.instagram.com/TheRollingStones/'),
  (4, 4, 4, 'The Rolling Stones', 'https://www.youtube.com/TheRollingStones/'),
  (5, 1, 1, 'The Who', 'https://www.facebook.com/TheWho/'),
  (6, 1, 1, 'The Doors', 'https://www.facebook.com/TheDoors/'),
  (6, 2, 2, 'The Doors', 'https://www.x.com/TheDoors/'),
  (6, 3, 3, 'The Doors', 'https://www.instagram.com/TheDoors/'),
  (6, 4, 4, 'The Doors', 'https://www.youtube.com/TheDoors/'),
  (7, 4, 1, 'The Weekend', 'https://www.youtube.com/channel/UC0WP5P-ufpRfjbNrmOWwLBQ');

INSERT INTO hebergement (idH, nomHebergement, addresse, nbPlaces) VALUES
  (1, 'Hotel des Lilas', '13 rue des Lilas', 23),
  (2, 'Hotel du Centre', '25 rue du Centre', 30),
  (3, 'Hotel de la Plage', '10 avenue de la Plage', 50),
  (4, 'Hotel des Alpes', '5 rue des Alpes', 40),
  (5, 'Hotel du Parc', '15 avenue du Parc', 20);

INSERT INTO heberge (idG, idH, dateDebut, dateFin) VALUES
  (1, 1, '2023-12-11', '2023-12-13'),
  (2, 2, '2023-12-11', '2023-12-13'),
  (3, 3, '2023-12-11', '2023-12-13'),
  (4, 4, '2023-12-11', '2023-12-13'),
  (5, 5, '2023-12-11', '2023-12-13'),
  (6, 1, '2023-12-11', '2023-12-13'),
  (7, 4, '2023-12-11', '2023-12-13');

INSERT INTO video (idVideo, urlVideo, idG, pos) VALUES
  (1, 'https://www.youtube.com/watch?v=R3XIGon2RjY', 1, 1),
  (2, 'https://www.youtube.com/watch?v=84Tq-eAJIk4', 2, 1),
  (3, 'https://www.youtube.com/watch?v=CTsB-llTzyc', 3, 1),
  (4, 'https://www.youtube.com/watch?v=nVrdXUHvsF0', 4, 1),
  (5, 'https://www.youtube.com/watch?v=8c1hYO_BYHY', 5, 1),
  (6, 'https://www.youtube.com/watch?v=aKd6yarfkxA', 6, 1),
  (7, 'https://www.youtube.com/watch?v=s37x2VSZrLw', 7, 1);


INSERT INTO photo (idPh, urlPh, pos, idG) VALUES(1, 'https://static.printler.com/cache/f/4/8/e/f/2/f48ef2e0a66f418305234b1ed4b8310529d72bae.jpg', 1, '1');
INSERT INTO photo (idPh, urlPh, pos, idG) VALUES(2, 'https://img.nrj.fr/-I_CLcqGR7_zjWmLMbjRKI0ZKqY=/http%3A%2F%2Fmedia.nostalgie.fr%2F1900x1200%2F2017%2F02%2Fpinkfloyd-jpg-3153981.jpg', 1, '2');
INSERT INTO photo (idPh, urlPh, pos, idG) VALUES(3, 'https://pbs.twimg.com/media/F-sMa1La0AA-pBK.jpg', 1, '3');
INSERT INTO photo (idPh, urlPh, pos, idG) VALUES(4, 'https://upload.wikimedia.org/wikipedia/commons/5/5e/Rolling_Stones_onstage_at_Summerfest_2015.jpg', 1, '4');
INSERT INTO photo (idPh, urlPh, pos, idG) VALUES(5, 'https://cdns-images.dzcdn.net/images/artist/079cce2a1a5ae11bda17f026b4e74334/500x500.jpg', 1, '5');
INSERT INTO photo (idPh, urlPh, pos, idG) VALUES(6, 'https://upload.wikimedia.org/wikipedia/commons/6/60/Doors_electra_publicity_photo.JPG', 1, '6');
INSERT INTO photo (idPh, urlPh, pos, idG) VALUES(7, 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/The_Weeknd_Portrait_by_Brian_Ziff.jpg/1200px-The_Weeknd_Portrait_by_Brian_Ziff.jpg', 1, '7');

INSERT INTO visiteur (idV, nomV, prenomV, dateNaissV, numtel, email, motdepasse, admin) VALUES
  (1, 'Rosse', 'Julien', '2004-02-06', '0606060606', 'contact@julienrosse.fr', '$argon2id$v=19$m=65536,t=3,p=4$/9b7IKIFHeJNPNDyVQmUOg$NY9EaMDqPhT319WoU+HJvsBzjRVCcg2B2uPltRT8KBU', 1),
  (2, 'Tremine', 'Marin', '2004-03-18', '0642789024', 'marin@marin.tech', '$argon2id$v=19$m=65536,t=3,p=4$pYvKZCaWHRwnXIRAAtCR3Q$VnCno4KsFOwpuDCbF01gsBYk62bhJ65CK3Hj4l+C2hQ', 1),
  (3, 'Bouvet', 'Alexandre', '2004-04-10', '0634567890', 'balex@gmail.test', '$argon2id$v=19$m=65536,t=3,p=4$0Z3Z3Z3Z3Z', 0),
  (4, 'Girard', 'Mathis', '2004-05-25', '0600000000', 'hfeuioshiu@fei.copm', '$argon2id$v=19$m=65536,t=3,p=4$0Z3Z3Z3Z3Z', 0),
  (5, 'Le Roux', 'Louis', '2004-06-12', '03438973489', 'fheiushfies@fehsku.ej', '$argon2id$v=19$m=65536,t=3,p=4$0Z3Z3Z3Z3Z', 0);

INSERT INTO visiteur (idV, nomV, prenomV, dateNaissV, numtel, email, motdepasse, admin) VALUES(6, 'Admin', 'Admin', '2000-01-01', '0000000000', 'admin@festiuto.fr', '$argon2id$v=19$m=65536,t=3,p=4$ZH5xMnyCRPxUa6p4AfukBg$R/3k+d593IAtRG64d+z55t489Zw858RHzUHAO1ZK860', 1);
INSERT INTO visiteur (idV, nomV, prenomV, dateNaissV, numtel, email, motdepasse, admin) VALUES(8, 'TREMINE', 'Marin', '2004-09-16', '0781371307', 'extrayer.dev@gmail.com', '$argon2id$v=19$m=65536,t=3,p=4$3ak+VL4JkZuoJ0I2T0DTGA$pao096F5vePluJVcyYK95plf+KhjqAOKeW8hEB0/zBk', NULL);

INSERT INTO favoris (idG, idV) VALUES
  (1, 1),
  (2, 1),
  (3, 1),
  (7, 1),
  (1, 2),
  (2, 2),
  (7, 2),
  (1, 3),
  (2, 3),
  (3, 3),
  (4, 3),
  (5, 3),
  (6, 3),
  (3, 4),
  (4, 4),
  (5, 4),
  (6, 4),
  (7, 4),
  (1, 5),
  (2, 5),
  (5, 5),
  (6, 5),
  (7, 5);

INSERT INTO lieu (idL, nomLieu, nbPlaces) VALUES
  (1, 'Scene Alpha', 3789),
  (2, 'Scene Beta', 1234),
  (3, 'Scene Gamma', 2232),
  (4, 'Scene Delta', 133),
  (5, 'Scene Epsilon', 998);

INSERT INTO evenement (idEv, typeEv, descrEv, tempsMontage, tempsDemontage, gratuit, dateDebut, dateFin, idG, idL) VALUES
  (1, 'Concert', 'Concert de Nirvana', '01:00:00', '00:30:00', 0, '2023-12-12 08:00:00', '2023-12-12 12:00:00', 1, 1),
  (2, 'Concert', 'Concert de Pink Floyd', '01:00:00', '00:30:00', 0, '2023-12-12 10:00:00', '2023-12-12 22:00:00', 2, 2),
  (3, 'Concert', 'Concert de The Beatles', '01:00:00', '00:30:00', 0, '2023-12-12 20:00:00', '2023-12-12 22:00:00', 3, 3),
  (4, 'Concert', 'Concert de The Rolling Stones', '01:00:00', '00:30:00', 1, '2023-12-12 20:00:00', '2023-12-12 22:00:00', 4, 4),
  (5, 'Concert', 'Concert de The Who', '01:00:00', '00:30:00', 0, '2023-12-12 20:00:00', '2023-12-12 22:00:00', 5, 5),
  (6, 'Concert', 'Concert de The Doors', '01:00:00', '00:30:00', 0, '2023-12-13 20:00:00', '2023-12-13 22:00:00', 6, 1),
  (7, 'Concert', 'Concert de The Weekend', '01:00:00', '00:30:00', 0, '2023-12-13 20:00:00', '2023-12-13 22:00:00', 7, 2);

INSERT INTO type_billet (idTb, nomB, prix, duree) VALUES
  (1, 'Billet 1 jour', 10, 1),
  (2, 'Billet 2 jours', 15, 2),
  (3, 'Billet 3 jours', 20, 3),
  (4, 'Billet saisonnier', 50, NULL);

INSERT INTO billet (idB, dateDebutValidite, idTb, idV) VALUES
  (1, '2023-12-12', 4, 1),
  (2, '2023-12-12', 4, 2),
  (3, '2023-12-13', 1, 3);

INSERT INTO s_inscrit (idEv, idV) VALUES
  (1, 1),
  (2, 1),
  (3, 1),
  (4, 1),
  (5, 1),
  (3, 2),
  (4, 2),
  (5, 2),
  (3, 3),
  (4, 3),
  (5, 3),
  (6, 3),
  (3, 4),
  (4, 4),
  (5, 4),
  (6, 4),
  (7, 4),
  (1, 5),
  (2, 5),
  (3, 5),
  (4, 5),
  (7, 5);

 

INSERT INTO visiteur (nomV,prenomV,dateNaissV,numtel,email,motdepasse,admin) VALUES
	 ('Admin','Admin','2000-01-01','00000000000','admin@festiuto.fr','$argon2id$v=19$m=65536,t=3,p=4$ZH5xMnyCRPxUa6p4AfukBg$R/3k+d593IAtRG64d+z55t489Zw858RHzUHAO1ZK860',NULL);
