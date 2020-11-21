from smtplib import SMTP_SSL
from email.message import EmailMessage
import glob

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import password

cred = credentials.Certificate(glob.glob("./aeapolimiweb-firebase*.json")[0])
firebase_admin.initialize_app(cred)

db = firestore.client()


def main():
    users_ref = db.collection(u'utenti').where(u"newsletter", "==", True)
    docs = users_ref.stream()
    destinatari = [doc.to_dict()["email"] for doc in docs]
    
    s = SMTP_SSL(host='smtps.aruba.it', port=465)
    s.login(password.mail, password.password)
    msg = EmailMessage()
    msg.set_content("Ciao")
    msg['Subject'] = 'CIAONE'
    msg['From'] = password.mail
    msg['To'] = ", ".join(destinatari)
    s.send_message(msg)
    s.quit()


if __name__ == "__main__":
    main()