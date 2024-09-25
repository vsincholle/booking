import streamlit as st
from streamlit_calendar import calendar
from streamlit_navigation_bar import st_navbar
import re
import mail
import variables
import utilities
import data
import hmac
import os
from dotenv import load_dotenv


load_dotenv()
if os.getenv("password"):
    password = os.getenv("password")
    app_pwd = os.getenv("app_pwd")
else:
    password = st.secrets["password"]
    app_pwd = st.secrets["app_pwd"]


@st.fragment
def book_apartment():
    booking_flag = False
    booked = False
    end_time_flag = False
    st.header(variables.booking_header)
    with st.container(border=True):
        st.subheader(variables.booking_form_subheader)

        start_date = st.date_input(variables.booking_text_start_date,
                                   min_value=variables.current_time_ist.date(),
                                   value=None)
        start_time = st.time_input(variables.booking_text_start_time,
                                   value=None,
                                   step=3600)
        end_date = st.date_input(variables.booking_text_end_date,
                                 min_value=start_date,
                                 value=None)
        end_time = st.time_input(variables.booking_text_end_time,
                                 value=None,
                                 step=3600)

        if start_time is not None:
            if (start_date == variables.current_time_ist.date()
                and start_time < variables.current_time_ist.time()):
                st.warning(variables.booking_text_start_time_issue)

            if end_time is not None:
                if (end_date == start_date and end_time < start_time):
                    st.warning(variables.booking_text_end_time_issue)
                else:
                    end_time_flag = True

        if end_time_flag and end_date is not None:
            intersection, available_apartments = utilities.is_apartment_available(start_date,
                                                                                  start_time,
                                                                                  end_date,
                                                                                  end_time)
            if available_apartments == []:
                st.warning(variables.booking_warning_available_appartments)
                if st.checkbox(variables.availabilities_show):
                    st.dataframe(intersection)
            else:
                st.subheader((variables.availabilities_subheader))
                if not intersection.empty:
                    if st.checkbox(variables.availabilities_show):
                        st.dataframe(intersection)
                apartment_choice = st.selectbox(variables.apartment_text_available, available_apartments, index=None)
                if apartment_choice:
                    st.subheader(str(variables.apartment_subheader+apartment_choice))
                    name = st.text_input(variables.apartment_text_name)
                    email = st.text_input(variables.apartment_text_email)
                    nb_people = st.text_input(variables.apartment_text_nb_people)
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        st.warning(variables.apartment_warning_email)
                    if not name:
                        st.warning("All details are mandatory.")
                    if name and email and nb_people:
                        booked = True

        submit_enabled = start_date and start_time and end_date and end_time and booked
        if st.button(variables.booking_submit, type="primary", disabled=not submit_enabled):
            booking_number = utilities.add_booking(start_date,
                                                   start_time,
                                                   end_date,
                                                   end_time,
                                                   apartment_choice,
                                                   name,
                                                   email,
                                                   nb_people)
            booking_flag = True
            email = mail.mail_booking(start_date,
                                      start_time,
                                      end_date,
                                      end_time,
                                      apartment_choice,
                                      name,
                                      email,
                                      nb_people,
                                      booking_number,
                                      app_pwd)
            if email:
                st.info(variables.email_validation)
            else:
                st.warning(variables.email_issue)

    if booking_flag:
        st.info(apartment_choice + '\n' + variables.booked_text_validation + booking_number)
        data.upload_dbx(variables.booking_data_file)


def cancel_room():
    st.header(variables.cancel_header)

    with st.container(border=True):
        booking_number = st.text_input(variables.cancel_booking_text)

        if booking_number:
            booking = utilities.retrieve_booking(booking_number)
            if booking.empty:
                st.warning(variables.cancel_warning_booking_number)
            else:
                st.markdown(variables.cancel_booking_retrieved)
                st.dataframe(booking, hide_index=True)

                if st.button(variables.cancel_submit, type="primary"):
                    cancel = utilities.cancel_booking(booking_number)
                    if cancel:
                        st.info(variables.cancel_validation)
                        send_cancel_email = mail.mail_cancel(booking_number,
                                                             booking['name'].values[0],
                                                             booking['apartment'].values[0],
                                                             booking['email'].values[0],
                                                             app_pwd)
                        if send_cancel_email:
                            st.info(variables.email_cancel)
                        else:
                            st.warning(variables.email_issue)


def view_reservations():
    st.header(variables.view_header)
    booked_apartments = utilities.retrieve_all()
    if booked_apartments.empty:
        st.warning(variables.view_warning_booking)
    else:
        calendar_events = utilities.build_calendar_events(booked_apartments)
        calen = calendar(events=calendar_events,
                         options=variables.calendar_options)
        calen
        # st.dataframe(booked_apartments, hide_index=True) # To see df all bookings


def home():
    st.header(variables.home_header)
    st.markdown(variables.home_instructions)


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
        if hmac.compare_digest(st.session_state["password"], password):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


# Main Streamlit app starts here
st.set_page_config(initial_sidebar_state="collapsed")
if not check_password():
    print('---> Do not pass password step')
    st.stop()  # Do not continue if check_password is not True.
page = st_navbar(["Home", "Réserver", "Annuler", "Planning"], styles=variables.styles)
if page == "Réserver":
    book_apartment()
elif page == "Annuler":
    cancel_room()
elif page == "Planning":
    view_reservations()
elif page == "Home":
    home()
else:
    check_password()
