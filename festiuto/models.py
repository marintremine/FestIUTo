
from base64 import b64encode
from .app import db,login_manager
import argon2

ph = argon2.PasswordHasher()

class Artiste(db.Model):
    idA = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomA = db.Column(db.String(50))
    prenomA = db.Column(db.String(50))
    dateNaissA = db.Column(db.Date)
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), nullable=False)
    
    groupe = db.relationship('Groupe', backref='artistes')

    def __repr__(self):
        return f"<Artisteimport argon2 ida={self.idA} noma={self.nomA} prenoma={self.prenomA} dateNaissA={self.dateNaissA} idG={self.idG}>"

class TypeBillet(db.Model):
    idTb = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomB = db.Column(db.String(50))
    prix = db.Column(db.DECIMAL(5, 2))
    duree = db.Column(db.Integer)
    

    def __repr__(self):
        return f"<TypeBillet idTb={self.idTb} nomB={self.nomB} prix={self.prix} duree={self.duree}>"

class Billet(db.Model):
    idB = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateDebutValidite = db.Column(db.Date)
    idV = db.Column(db.Integer, db.ForeignKey('visiteur.idV'), nullable=False)
    idTb = db.Column(db.Integer, db.ForeignKey('type_billet.idTb'), nullable=False)

    typeBillet = db.relationship('TypeBillet', backref='billets')
    visiteur = db.relationship('Visiteur', backref='billets')

    def __repr__(self):
        return f"<Billet idB={self.idB} dateDebutValidite={self.dateDebutValidite} idTb={self.idTb} idV={self.idV}>"
    


class Favoris(db.Model):
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), primary_key=True, nullable=False)
    idV = db.Column(db.Integer, db.ForeignKey('visiteur.idV'), primary_key=True, nullable=False)

    groupe = db.relationship('Groupe', backref='favoris')
    visiteur = db.relationship('Visiteur', backref='favoris')


class Groupe(db.Model):
    idG = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomG = db.Column(db.String(42))
    descriptionG = db.Column(db.String(42)) 
    def __repr__(self):
        return f"<Groupe idG={self.idG} nomG={self.nomG} descriptionG={self.descriptionG}>"


class Hebergement(db.Model):
    idH = db.Column(db.Integer, primary_key=True)
    nomHebergement = db.Column(db.String(50))
    addresse = db.Column(db.String(200))
    nbPlaces = db.Column(db.Integer)

    def __repr__(self):
        return f"<Hebergement idH={self.idH} nomHebergement={self.nomH} addresse={self.addresse} nbPlaces={self.nbPlaces}>"


class Heberge(db.Model):
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), primary_key=True, nullable=False)
    idH = db.Column(db.Integer, db.ForeignKey('hebergement.idH'), primary_key=True, nullable=False)
    dateDebut = db.Column(db.Date)
    dateFin = db.Column(db.Date)

    groupe = db.relationship('Groupe', backref='heberge')
    hebergement = db.relationship('Hebergement', backref='heberge')

    def __repr__(self):
        return f"<Heberge idG={self.idG} idH={self.idH} dateDebut={self.dateDebut} dateFin={self.dateFin}>"


class Instrument(db.Model):
    idI = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomI = db.Column(db.String(80))

    def __repr__(self):
        return f"<Instrument idI={self.idI} nomI={self.nomI}>"


class LienRS(db.Model):
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), primary_key=True, nullable=False)
    idRs = db.Column(db.Integer, db.ForeignKey('reseau_social.idRs'), nullable=False, primary_key=True)
    pos = db.Column(db.Integer)
    pseudo = db.Column(db.String(80))
    urlReseau = db.Column(db.String(200))
    
    

    groupe = db.relationship('Groupe', backref='lienrs')
    reseau = db.relationship('ReseauSocial', backref='lienrs')

    def __repr__(self):
        return f"<LienRS idG={self.idG} idRs={self.idRs} pos={self.pos} pseudo={self.pseudo} urlReseau={self.urlReseau}>"


class Lieu(db.Model):
    idL = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomLieu = db.Column(db.String(80))
    nbPlaces = db.Column(db.Integer)

    def __repr__(self):
        return f"<Lieu idL={self.idL} nomLieu={self.nomLieu} nbPlaces={self.nbPlaces}>"


class Photo(db.Model):
    idPh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    urlPh = db.Column(db.String(200))
    pos = db.Column(db.Integer)
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), nullable=False)

    groupe = db.relationship('Groupe', backref='photo')

    def __repr__(self):
        return f"<Photo idPh={self.idPh} urlPh={self.urlPh} idG={self.idG} pos={self.pos}>"


class ReseauSocial(db.Model):
    idRs = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomReseau = db.Column(db.String(50))
    urlLogoReseau = db.Column(db.String(200))

    def __repr__(self):
        return f"<ReseauSocial idRs={self.idRs} nomReseau={self.nomReseau} urlLogoReseau={self.urlLogoReseau}>"
    
class Jouer(db.Model):
    idI = db.Column(db.Integer, db.ForeignKey('instrument.idI'), primary_key=True, nullable=False)
    idA = db.Column(db.Integer, db.ForeignKey('artiste.idA'), primary_key=True, nullable=False)

    instrument = db.relationship('Instrument', backref='joueurs')
    artiste = db.relationship('Artiste', backref='instruments')


class Style(db.Model):
    idS_1 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idS_2 = db.Column(db.Integer, db.ForeignKey("style.idS_1", ondelete="CASCADE", onupdate="CASCADE"))
    nomS = db.Column(db.String(280))

    style = db.relationship("Style")

    def __repr__(self):
        return f"<Style idS={self.idS_1} nomS={self.nomS}>"

# class EtreSousStyle(db.Model):
#     idS_1 = db.Column(db.Integer, db.ForeignKey('style.idS'), primary_key=True, nullable=False)
#     idS_2 = db.Column(db.Integer, db.ForeignKey('style.idS'), primary_key=True, nullable=False)

#     s1 = db.relationship('Style', backref='sous_styles1')
#     s2 = db.relationship('Style', backref='sous_styles2')


    
class Posseder(db.Model):
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), primary_key=True, nullable=False)
    idS = db.Column(db.Integer, db.ForeignKey('style.idS_1'), primary_key=True, nullable=False)

    groupe = db.relationship('Groupe', backref='styles')
    style = db.relationship('Style', backref='groupes')


class Video(db.Model):
    idVideo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    urlVideo = db.Column(db.String(200))
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), nullable=False)
    pos = db.Column(db.Integer)

    groupe = db.relationship('Groupe', backref='video')

    def __repr__(self):
        return f"<Video idVideo={self.idVideo} urlVideo={self.urlVideo} idG={self.idG} pos={self.pos}>"
    ph = argon2.PasswordHasher()
class SInscrit(db.Model):
    idEv = db.Column(db.Integer, db.ForeignKey('evenement.idEv'), primary_key=True, nullable=False)
    idV = db.Column(db.Integer, db.ForeignKey('visiteur.idV'), primary_key=True, nullable=False)

    evenement = db.relationship('Evenement', backref='inscrits')
    visiteur = db.relationship('Visiteur', backref='inscriptions')


class Visiteur(db.Model):
    idV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomV = db.Column(db.String(50))
    prenomV = db.Column(db.String(50))
    dateNaissV = db.Column(db.Date)
    numtel = db.Column(db.String(12))
    email = db.Column(db.String(255), unique=True)
    motdepasse = db.Column(db.String(255))
    admin = db.Column(db.Boolean)

    
    def __repr__(self):
        return f"<Visiteur idV={self.idV} nomV={self.nomV} prenomV={self.prenomV} dateNaissV={self.dateNaissV} " \
               f"numtel={self.numtel} email={self.email} motdepasse={self.motdepasse} admin={self.admin}>"
    
    def is_authenticated(self):
        """
        Returns True if the user is authenticated.
        """
        return True
    def is_active(self):
        """
        Returns True if the user is active.
        """
        return True
    def is_anonymous(self):
        """
        Returns True if the user is anonymous.
        """
        return False
    
    def get_id(self):
        """
        Returns the user's id.
        """
        return str(self.idV)

    @staticmethod
    def generate_hash(password):
        """Generate a hash from a password"""
        return ph.hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a password against a hash"""
        try:
            return ph.verify(hashed_password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False
    
@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database.
    """
    return Visiteur.query.get(int(user_id))

class Evenement(db.Model):
    idEv = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typeEv = db.Column(db.String(80))
    descrEv = db.Column(db.String(200))
    tempsMontage = db.Column(db.Time)
    tempsDemontage = db.Column(db.Time)
    gratuit = db.Column(db.Boolean)
    dateDebut = db.Column(db.DateTime)
    dateFin = db.Column(db.DateTime)
    idG = db.Column(db.String(42), db.ForeignKey('groupe.idG'), nullable=False)
    idL = db.Column(db.Integer, db.ForeignKey('lieu.idL'), nullable=False)

    groupe = db.relationship('Groupe', backref='evenements')
    lieu = db.relationship('Lieu', backref='evenements')

    def __repr__(self):
        return f"<Evenement idEv={self.idEv} typeEv={self.typeEv} descrEv={self.descrEv} " \
               f"tempsMontage={self.tempsMontage} tempsDemontage={self.tempsDemontage} " \
               f"gratuit={self.gratuit} dateDebut={self.dateDebut} dateFin={self.dateFin} " \
               f"idG={self.idG} idL={self.idL}>"