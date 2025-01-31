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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

def send_reset_password_email(email_to: str, code: str, first_name: str = ''):
    try:
        # Valider l'email de l'utilisateur
        validate_email(email_to)

        # Création du message
        msg = MIMEMultipart()
        msg['From'] = 'laurentalphonsewilfried@gmail.com'
        msg['To'] = email_to
        msg['Subject'] = 'Réinitialisation de mot de passe'

        body = f"""
        Bonjour {first_name},

        Vous avez demandé à réinitialiser votre mot de passe. Veuillez utiliser le code suivant pour réinitialiser votre mot de passe :

        Code de réinitialisation : {code}

        Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer ce message.

        """
        msg.attach(MIMEText(body, 'plain'))

        # Connexion au serveur SMTP
        with smtplib.SMTP(Config.MAILTRAP_HOST, Config.MAILTRAP_PORT) as server:
            server.starttls()  # Sécuriser la connexion
            server.login(Config.MAILTRAP_USERNAME, Config.MAILTRAP_PASSWORD)  # Utiliser les credentials de Mailtrap
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print(f"Email envoyé à {email_to} avec le code de réinitialisation.")

    except EmailNotValidError as e:
        print(f"Email invalide: {e}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")