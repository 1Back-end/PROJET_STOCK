import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr
from fastapi import HTTPException
from typing import List
from app.main.core.config import Config
# Configurations de Mailtrap (ajuste avec tes informations)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

def send_email(to_email: str, subject: str, body: str):
    try:
        # Création de l'email
        message = MIMEMultipart()
        message["From"] = Config.MAILTRAP_USERNAME  # Email de l'expéditeur
        message["To"] = to_email
        message["Subject"] = subject

        # Contenu de l'email
        message.attach(MIMEText(body, "plain"))

        # Connexion au serveur SMTP (Mailtrap)
        with smtplib.SMTP(Config.MAILTRAP_HOST, Config.MAILTRAP_PORT) as server:
            server.starttls()  # Activer TLS pour sécuriser la connexion
            server.login(Config.MAILTRAP_USERNAME, Config.MAILTRAP_PASSWORD)  # Authentification Mailtrap
            server.sendmail(Config.MAILTRAP_USERNAME, to_email, message.as_string())  # Envoi de l'email

        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False