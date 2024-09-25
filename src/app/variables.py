from datetime import datetime, time
import pytz


# Set the timezone to "Paris" time
ist = pytz.timezone('Europe/Paris')
# Get the current time in IST
current_time_ist = datetime.now(ist)
ctif = current_time_ist.strftime("%y-%m-%d %H:%M:%S")
hours = [time(i).strftime("%H:%M") for i in range(24)]
# Encoding for csv file
encoding = 'utf-8'
# Apartments list
apartments = ["Studio", "Appartement avant", "Appartement arrière"]

# Define file paths for storing booking data
booking_data_file = "booking_data.csv"  # file downlaoded as csv
file_dbx = '/booking/booking_data.csv'  # path for dropbox could contain folder if we want to oragnize on dbx

# Define columns to create for DataFrame is file is not existing
columns = ["uuid", "start_datetime", "end_datetime", "apartment", "name", "email", "nb_people"]
# Define columns to diplay inside app
columns_to_display = ["start_datetime", "end_datetime", "apartment", "name", "nb_people"]
columns_to_display_cancel = ["start_datetime", "end_datetime", "apartment", "name", "nb_people", "email"]

# TEXT
# home
home_header = "Bienvenue au Capitole"
home_instructions = '''Veuillez utiliser la barre de navigation ci-dessus afin: 

- de réserver un apartement aux dates désirées
- d'annuler une réservation déjà passée
- de visualiser le planning des réservations


Si vous ne voyez pas l'intégralité de la barre de navigation sur un smartphone, passez en mode horizontal.


Lors de votre réservation, un email vous sera envoyé contenant un code unique de réservation.
Conservez bien cet email car en cas d'annulation ce code vous sera demandé.


Nous vous souhaitons un agréable séjour au Capitole
'''

# email
email_sender = "lecapitole44@gmail.com"
email_subject = "Réservation du Capitole"
email_cancel_subject = "Annulation du Capitole"
email_validation = "Un email a été envoyé contenant vos informations de réservation"
email_cancel = "Un email a été envoyé confirmant l'annulation de votre réservation"
email_issue = "Nous n'avons pas réussi à envoyer un email à l'adresse indiquée"

# Book page
booking_header = "Réservation du Capitole"
booking_form_subheader = "Entrer vos dates"
booking_form_text = "Merci de bien vouloir remplir les informations ci-dessous"
booking_text_start_date = "Date de début de séjour"
booking_text_start_time = "Heure d'arrivée"
booking_text_start_time_issue = "l'heure d'arrivée est déjà passée"
booking_text_end_time_issue = "l'heure de départ n'est pas valable"
booking_text_end_date = "Date de fin de séjour"
booking_text_end_time = "Heure de départ"
booking_warning_available_appartments = "Tous les appartements sont occupés à ces dates"
availabilities_subheader = "Disponibilités"
availabilities_show = "Afficher les appartements occupés pendant ces dates"
apartment_text_available = "Appartements disponibles à ces dates"
apartment_subheader = "Réservation: "
apartment_text_name = "Entrer votre prénom"
apartment_text_email = "Entrer votre email"
apartment_text_nb_people = "Entrer le nombre de personnes"
apartment_warning_email = "Entrer un email valide"
apartment_warning_nb_people = "Le nombre de personnes dépasse la capacité de l'appartement"
booking_submit = "Réserver"
booked_text_validation = " a bien été réservé aux dates indiquées. Voici votre numéro de réservation: "

# Cancel page
cancel_header = "Annuler une réservation"
cancel_booking_text = "Entrer votre numéro de réservation"
cancel_warning_booking_number = "Aucune réservation existe avec ce numéro"
cancel_booking_retrieved = "Réservation existante"
cancel_submit = "Annuler ma réservation"
cancel_validation = "Merci, votre réservation a bien été annulée"
cancel_email_text = "Merci de confirmer votre email"

# View page
view_header = "Vue des réservations"
view_warning_booking = "Aucune réservations à afficher"

# CALENDAR SETTINGS
# Calendar
calendar_options = {
    "slotMinTime": "00:00:00",
    "slotMaxTime": "23:59:59",
    "initialView": "dayGridMonth",
    "resources": [
        {"id": "Studio", "title": "Studio"},
        {"id": "App.Avant", "title": "App.Avant"},
        {"id": "App.Arrière", "title": "App.Arrière"}
    ],
}

custom_css = """
    .fc-dom-1 {
        height: 250px;
    }
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-size: 0rem;
        content: unset;
    }
    .fc-event-title {
        font-size: 0.6rem;
    }
    .fc-toolbar-title {
        font-size: 1.1rem;
    }
    .fc-col-header-cell-cushion {
        font-size: 0.8rem;
    }
    .fc-daygrid-day-number {
        font-size: 0.6rem;
    }
    .fc-title {
        font-size: 1.1rem;
    }
    .fc-today-button {
        font-size: 0.8rem;
    }
    .fc-prev-button {
        font-size: 0.8rem;
    }
    .fc-next-button {
        font-size: 0.8rem;
    }
"""

# NAVABAR SETTINGS
styles = {
    "nav": {
        "background-color": "royalblue",
        "text-align": "left",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "1px",
    },
    "span": {
        "color": "white",
        "font-size": "14px",
        "padding": "8px",
    },
    "active": {
        "background-color": "blue",
        "color": "white",
        "font-weight": "normal",
        "padding": "14px",
    }
}
