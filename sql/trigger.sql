DELIMITER |

CREATE OR REPLACE FUNCTION get_places_libres(idHe INT, dateDeb DATE, dateFin DATE) RETURNS INT
BEGIN
  DECLARE nbArtiste INT;
  DECLARE nbPl INT;
  SELECT COUNT(*) INTO nbArtiste FROM artiste WHERE idG in (SELECT idG FROM heberge WHERE idH = idH AND dateDebut BETWEEN dateDeb AND dateFin OR dateFin BETWEEN dateDeb AND dateFin);
  SELECT nbPlaces INTO nbPl FROM hebergement WHERE idH = idHe;
  RETURN nbPl-nbArtiste;
END|

-- Le nombre de place de l'hebergement doit être supérieur ou égale au nombre d'artiste du groupe

CREATE OR REPLACE TRIGGER hebergement_nbPlaces_artiste_ajout BEFORE INSERT ON heberge FOR EACH ROW
BEGIN
  DECLARE placesLibres INT;
  SELECT get_places_libres(new.idH, new.dateDebut, new.dateFin) INTO placesLibres;
  IF placesLibres < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le nombre de place de l''hebergement doit être supérieur ou égale au nombre d''artiste du groupe';
  END IF;
END|

CREATE OR REPLACE TRIGGER hebergement_nbPlaces_ajout_artiste_groupe BEFORE INSERT ON artiste FOR EACH ROW
BEGIN
  DECLARE idH INT;
  DECLARE nbPl INT;
  DECLARE dateDeb DATE;
  DECLARE dateFin DATE;
  DECLARE fini BOOLEAN DEFAULT FALSE;
  DECLARE lesReservations CURSOR FOR SELECT idH, nbPlaces, dateDebut, dateFin FROM heberge NATURAL JOIN hebergement WHERE idG = new.idG;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;
  OPEN lesReservations;
  WHILE NOT fini DO
    FETCH lesReservations INTO idH, nbPl, dateDeb, dateFin;
    IF NOT fini AND get_places_libres(idH, dateDeb, dateFin) < 1 THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le nombre de place de l''hebergement doit être supérieur ou égale au nombre d''artiste du groupe';
    END IF;
  END WHILE;
END|

-- Le nombre de place du lieu de l'evenement doit être supérieur ou égale au nombre de visiteur qui assiste à l'évenement

CREATE OR REPLACE TRIGGER lieu_nbPlaces_visiteur BEFORE INSERT ON evenement FOR EACH ROW
BEGIN
  DECLARE nbVisiteur INT;
  DECLARE nbPl INT;
  SELECT COUNT(*) INTO nbVisiteur FROM s_inscrit WHERE idEv = new.idEv;
  SELECT nbPlaces INTO nbPl FROM lieu WHERE idL = new.idL;
  IF nbPl < nbVisiteur THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le nombre de place du lieu de l''evenement doit être supérieur ou égale au nombre de visiteur qui assiste à l''évenement';
  END IF;
END|

CREATE OR REPLACE TRIGGER lieu_nbPlaces_visiteur_update BEFORE UPDATE ON evenement FOR EACH ROW
BEGIN
  DECLARE nbVisiteur INT;
  DECLARE nbPl INT;
  SELECT COUNT(*) INTO nbVisiteur FROM s_inscrit WHERE idEv = new.idEv;
  SELECT nbPlaces INTO nbPl FROM lieu WHERE idL = new.idL;
  IF nbPl < nbVisiteur THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le nombre de place du lieu de l''evenement doit être supérieur ou égale au nombre de visiteur qui assiste à l''évenement';
  END IF;
END|

CREATE OR REPLACE TRIGGER lieu_nbPlaces_ajout_visiteur_evenement BEFORE INSERT ON s_inscrit FOR EACH ROW
BEGIN
  DECLARE nbVisiteur INT;
  DECLARE nbPl INT;
  SELECT COUNT(*) INTO nbVisiteur FROM s_inscrit WHERE idEv = new.idEv;
  SELECT nbPlaces INTO nbPl FROM lieu WHERE idL = (SELECT idL FROM evenement WHERE idEv = new.idEv);
  IF nbPl < nbVisiteur THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le nombre de place du lieu de l''evenement doit être supérieur ou égale au nombre de visiteur qui assiste à l''évenement';
  END IF;
END|

CREATE OR REPLACE TRIGGER lieu_nbPlaces_update_visiteur_evenement BEFORE UPDATE ON s_inscrit FOR EACH ROW
BEGIN
  DECLARE nbVisiteur INT;
  DECLARE nbPl INT;
  SELECT COUNT(*) INTO nbVisiteur FROM s_inscrit WHERE idEv = new.idEv;
  SELECT nbPlaces INTO nbPl FROM lieu WHERE idL = (SELECT idL FROM evenement WHERE idEv = new.idEv);
  IF nbPl < nbVisiteur THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Le nombre de place du lieu de l''evenement doit être supérieur ou égale au nombre de visiteur qui assiste à l''évenement';
  END IF;
END|

-- Un groupe ne peux pas faire deux évenements au même dates 

CREATE OR REPLACE TRIGGER evenement_date_groupe BEFORE INSERT ON evenement FOR EACH ROW
BEGIN
  DECLARE nbEv INT;
  SELECT COUNT(*) INTO nbEv FROM evenement WHERE idG = new.idG AND (new.dateDebut BETWEEN dateDebut AND dateFin OR new.dateFin BETWEEN dateDebut AND dateFin);
  IF nbEv > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un groupe ne peux pas faire deux évenements au même dates';
  END IF;
END|

CREATE OR REPLACE TRIGGER evenement_date_update_groupe BEFORE UPDATE ON evenement FOR EACH ROW
BEGIN
  DECLARE nbEv INT;
  SELECT COUNT(*) INTO nbEv FROM evenement WHERE idG = new.idG AND (new.dateDebut BETWEEN dateDebut AND dateFin OR new.dateFin BETWEEN dateDebut AND dateFin);
  IF nbEv > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un groupe ne peux pas faire deux évenements au même dates';
  END IF;
END|

-- 2 évenements ne doivent pas se chevaucher s'ils ont le même lieu.

CREATE OR REPLACE TRIGGER evenement_date_lieu BEFORE INSERT ON evenement FOR EACH ROW
BEGIN
  DECLARE nbEv INT;
  SELECT COUNT(*) INTO nbEv FROM evenement WHERE idL = new.idL AND (new.dateDebut BETWEEN dateDebut AND dateFin OR new.dateFin BETWEEN dateDebut AND dateFin);
  IF nbEv > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '2 évenements ne doivent pas se chevaucher s''ils ont le même lieu.';
  END IF;
END|

CREATE OR REPLACE TRIGGER evenement_date_update_lieu BEFORE UPDATE ON evenement FOR EACH ROW
BEGIN
  DECLARE nbEv INT;
  SELECT COUNT(*) INTO nbEv FROM evenement WHERE idL = new.idL AND (new.dateDebut BETWEEN dateDebut AND dateFin OR new.dateFin BETWEEN dateDebut AND dateFin);
  IF nbEv > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '2 évenements ne doivent pas se chevaucher s''ils ont le même lieu.';
  END IF;
END|

-- Si l'evenement est payant, le visiteur doit avoir un billet valide le jour de l'evenement

CREATE OR REPLACE TRIGGER evenement_billet_ajout_visiteur BEFORE INSERT ON s_inscrit FOR EACH ROW
BEGIN
  DECLARE nbBillet INT;
  DECLARE dateDeb DATE;
  DECLARE gratuit BOOLEAN;
  SELECT dateDebut INTO dateDeb FROM evenement WHERE idEv = new.idEv;
  SELECT gratuit INTO gratuit FROM evenement WHERE idEv = new.idEv;
  IF NOT gratuit THEN
    SELECT COUNT(*) INTO nbBillet FROM billet WHERE idV = new.idV AND dateDebutValidite <= dateDeb AND DATE_ADD(dateDebutValidite, INTERVAL duree DAY) >= dateDeb;
    iF nbBillet < 1 THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Si l''evenement est payant, le visiteur doit avoir un billet valide le jour de l''evenement';
    END IF;
  END IF;
END|

DELIMITER ;