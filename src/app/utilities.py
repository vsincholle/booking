import uuid
import pandas as pd
import data
import variables
import datetime


def is_apartment_available(start_date, start_time, end_date, end_time):
    df = data.load_csv()

    start_datetime = datetime.datetime.combine(start_date, start_time)
    end_datetime = datetime.datetime.combine(end_date, end_time)

    df['start_datetime'] = pd.to_datetime(df['start_datetime'], format="ISO8601")
    df['end_datetime'] = pd.to_datetime(df['end_datetime'], format="ISO8601")
    mask = ((df['start_datetime'] < start_datetime) & (df['end_datetime'] > end_datetime)) \
            | ((df['start_datetime'] < start_datetime) & (df['end_datetime'] > start_datetime)) \
            | ((df['start_datetime'] >= start_datetime) & (df['end_datetime'] <= end_datetime)) \
            | ((df['start_datetime'] < end_datetime) & (df['end_datetime'] >= end_datetime))
    intersection = df.loc[mask][['start_datetime', 'end_datetime', 'apartment', 'name', 'nb_people']]
    occupied = df.loc[mask].apartment.to_list()

    available_apartments = []
    for a in variables.apartments:
        if not (a in occupied):
            available_apartments.append(a)

    return intersection, available_apartments


def add_booking(start_date, start_time, end_date, end_time, apartment, name, email, nb_people):
    df = data.load_csv()

    start_datetime = datetime.datetime.combine(start_date, start_time)
    end_datetime = datetime.datetime.combine(end_date, end_time)

    booking_number = str(uuid.uuid4())

    df.loc[-1] = [booking_number, start_datetime, end_datetime, apartment, name, email, nb_people]

    df.to_csv(variables.booking_data_file, index=False)

    return booking_number


def retrieve_all():
    df = data.load_dbx(variables.file_dbx)
    df['start_datetime'] = pd.to_datetime(df['start_datetime'], format="ISO8601")
    df['end_datetime'] = pd.to_datetime(df['end_datetime'], format="ISO8601")  # Keep to build calendar later
    return df[variables.columns_to_display]


def retrieve_booking(booking_number):
    df = data.load_dbx(variables.file_dbx)
    return df[df['uuid'] == booking_number][variables.columns_to_display_cancel]


def cancel_booking(booking_number):
    df = data.load_dbx(variables.file_dbx)
    df = df.drop(df[df.uuid == booking_number].index)
    df.to_csv(variables.booking_data_file, index=False)
    data.upload_dbx(variables.booking_data_file)
    return True


def build_calendar_events(booked_apartments):
    calendar_events = []
    # print(booked_apartments.dtypes)
    booked_apartments['start_datetime'] = booked_apartments['start_datetime'].astype(str)
    booked_apartments['end_datetime'] = booked_apartments['end_datetime'].astype(str)
    records = booked_apartments.to_dict('records')
    # print('records: ',records)
    for record in records:
        event = {}
        # print('record: ',record)
        event['title'] = record['apartment'] + ' - ' + record['name'] + ' - ' + str(record['nb_people']) + ' pers.'
        event['start'] = record['start_datetime']
        event['end'] = record['end_datetime']
        event['resourceId'] = record['apartment']
        calendar_events.append(event)
    # print('calendar: ',calendar_events)
    return calendar_events
