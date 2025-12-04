import json
import re, sys

#création class contact pour créer et gérer une liste de contact
class Contact:
    def __init__(self, nom, telephone, email):
        self.nom = nom
        self.telephone = telephone
        self.email = email


    def __str__(self):
        return f"{self.nom} | {self.telephone} | {self.email}"


class CarnetAdresse():
    def __init__(self, fichier = "CarnetAdresse.json"):
        self.fichier = fichier
        self.contacts = []
        self.charger_contact(fichier)


    def mail_valide(self, mail):
        #regex pour vérifier la forme générale du mail
        form_mail = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(form_mail, mail) is not None


    def ajouter_contact(self, contact):
        if not CarnetAdresse.mail_valide(self, contact.email):

        #vérifie doublons
            for c in self.contacts:
                print(contact.email)
                if c.email.lower() == contact.email.lower():
                    print(f"L'adresse mail {contact.email} existe déjà")
                    return
        self.contacts.append(contact)
        carnet.validation_changement()
        print(f"Contact {contact.nom} ajouté avec succès")
        menuCarnetAdresse.menuUtilisateur()


    def modifier_contact(self, mail, newName = None, newMail = None, newPhone = None):
        contact = self.recherche_contact(mail)
        if contact:
            print("le contact existe")
            if newName:
                contact.nom = newName
            if newMail:
                contact.email = newMail
            if newPhone:
                contact.telephone = newPhone
            print("Le contact a bien été modifié.\n")
            newcontact = carnet.recherche_contact(mail)
            print(f"Contact modifié : \n {newcontact}")
            saveContact = input("Voulez vous sauvegarder les changement dans le fichier ? \n 1-oui 2-non")
            if saveContact == str(1):
                carnet.sauvegarder_contacts()
            menuCarnetAdresse.menuUtilisateur()
        else:
            print("Le contact qe vous voulez modifier n'existe pas.")
            menuCarnetAdresse.menuUtilisateur()


    def supprimer_contact(self, mail):
        contactname = self.recherche_contact(mail)
        if contactname:
            try:
                self.contacts.remove(contactname)
                print("Le contact a été supprimé avec succès")
                carnet.validation_changement()
            except:
                print("L'adresse mail n'existe pas dans le carnet d'adresse")
                menuCarnetAdresse.menuUtilisateur()
        else:
            print("L'adresse mail n'a pas été trouvée. Aucune suppression de contacts.")
        menuCarnetAdresse.menuUtilisateur()


    def validation_changement(self):
        reponse = input("Enregistrer les modifications du carnet d'adresses ? \n 1- oui\n 2- non\n")
        if reponse == str(1):
            carnet.sauvegarder_contacts()
        menuCarnetAdresse.menuUtilisateur()


    def recherche_contact(self, mail):
        #recherche par mail
        for contactname in self.contacts:
            if contactname.email.lower() ==mail.lower():
                #print("Contact que vous recherchez : \n")
                return contactname
        return(f"Le mail {mail} ne fait pas partie de votre carnet d'adresse")
    

    def sauvegarder_contacts(self, fichier="CarnetAdresse.json"):
        #transforme chaque objet Contact en dictionnaire
        #créé une liste de dictionnaire pour tous les contacts
        data = [c.__dict__ for c in self.contacts]

        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("L'enregistrement du carnet d'adresse a été effecué avec succès.")
        menuCarnetAdresse.menuUtilisateur()


    def charger_contact(self, fichier="CarnetAdresse.json"):
        try:
            with open(fichier, "r", encoding="utf-8")as f:
                data = json.load(f)
                #prend chaque paire clé/valeur du dictionnaire et on a passe comme arguments
                self.contacts = [Contact(**c) for c in data]
        except FileNotFoundError:
            self.contacts = []


    def lire_carnet(self):
        lignes = [
                f"{'N°':<4}|{'Nom':<20}|{'Téléphone':<15}|{'Mail':<25}"
            ]
        if not self.contacts:
            print("Le carnet d'adresse est vide")
        else:
            #en-tete
            print(f"{'N°':<4}|{'Nom':<20}|{'Téléphone':<15}|{'Mail':<25}")
            print("-"*90)
            #contenu
            print("Carnet d'adresse :")
            for i, contact in enumerate(self.contacts, start=1):
                print(f"{i:<4}|{contact.nom:<20}|{contact.telephone:<15}|{contact.email:<25}")
                lignes.append(f"{i:<4}|{contact.nom:<20}|{contact.telephone:<15}|{contact.email:<25}")
        
        #carnet exporté pour markdown
        with open("carnet.md", "w", encoding="utf-8") as f:
            f.write("\n.".join(lignes))
            print("Carnet exporte dans le fichier carnet.md")
        menuCarnetAdresse.menuUtilisateur()


#creation du carnet d'adresse
carnet = CarnetAdresse()


#création de la classe Menu utilisateur
class menuCarnetAdresse():
    def __init__ (self) :
        pass        

    def menuUtilisateur():
        choix = input("Que voulez vous faire ? \n 1-Ajout un contact \n 2-Modifier un contact\n 3-Rechercher un contact\n 4-Supprimer un contact \n 5-lire le carnet d'adresse\n 6-Sauvegarder le carnet d'adresse\n 7-Quitter\n")
        if choix == str(1):
            nom_contact = input("Quel est le nom ?\n")
            tel_contact = input("Quel est le numéro de téléphone ?\n")
            mail_contact = input(f"Quel est l'adresse mail de {str(nom_contact)} ?\n")
            carnet.ajouter_contact(Contact(str(nom_contact), str(tel_contact),  str(mail_contact)))
        if choix == str(2):
            mail_contact = input("Quel est l'adresse mail du contact à modifier ?\n")
            newName = input("Quel est son nouveau nom ? (vide si identique)\n")
            newMail = input("Quel est sa nouvelle adresse mail ? (vide si identique)\n")
            newTel = input("Quelle est son nouveau numéro de téléphone ? (vide si identique)\n")
            carnet.modifier_contact(str(mail_contact), str(newName), str(newMail), str(newTel))
            pass
        if choix == str(3):
            nom_contact = input("Indiquez l'adresse mail de la personne recherchée :\n")
            print(carnet.recherche_contact(str(nom_contact)))
        if choix ==str(4):
            nom_contact = input("Quel contact voulez-vous enlever du carnet d'adresse ?\n")
            carnet.supprimer_contact(str(nom_contact))
        if choix ==str(6):
            carnet.sauvegarder_contacts()
        if choix == str(5):
            carnet.lire_carnet()
        if choix == str(7):
            sys.exit(0)
        else:
            menuCarnetAdresse()


#démarre l'application
menuCarnetAdresse.menuUtilisateur()