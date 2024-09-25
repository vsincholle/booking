import smtplib
from email.mime.text import MIMEText
import variables


def mail_booking(start_date, start_time, end_date, end_time, apartment, name, email_receiver, nb_people, booking_number, app_pwd):
    try:
        body = f"""
        Bonjour {name} !

        Nous avons le plaisir de vous informer de votre réservation du Capitole. 
        Vous avez réservé le {apartment} pour {nb_people} personnes du {start_date} {start_time} au {end_date} {end_time}.
        Veuillez noter votre numéro de réservation: {booking_number}, celui-ci vous sera demandé en cas d'annulation.

        Merci de ne pas répondre au présent email.
        Bien cordialement
        """

        msg = MIMEText(body)
        msg['From'] = variables.email_sender
        msg['To'] = email_receiver
        msg['Subject'] = variables.email_subject
        recipients = [variables.email_sender, email_receiver]

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(variables.email_sender, app_pwd)
            smtp_server.sendmail(variables.email_sender,
                                 recipients,
                                 msg.as_string())
        return True
    except Exception as e:
        print((f"Erreur lors de l’envoi de l’e-mail : {e}"))
        return False


def mail_cancel(booking_number, name, apartment, email_receiver, app_pwd):
    try:
        body = f"""
        Bonjour {name} !

        Nous vous confirmons l'annulation de votre réservation {booking_number} de l'appartement {apartment} du Capitole.

        Merci de ne pas répondre au présent email.
        Bien cordialement
        """

        msg = MIMEText(body)
        msg['From'] = variables.email_sender
        msg['To'] = email_receiver
        msg['Subject'] = variables.email_cancel_subject
        recipients = [variables.email_sender, email_receiver]

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(variables.email_sender, app_pwd)
            smtp_server.sendmail(variables.email_sender,
                                 recipients,
                                 msg.as_string())
        return True
    except Exception as e:
        print((f"Erreur lors de l’envoi de l’e-mail : {e}"))
        return False
