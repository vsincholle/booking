import pandas as pd
import streamlit as st
import variables
import dropbox
from io import BytesIO
import os
from dotenv import load_dotenv
import requests
import json


# Loading the Access Token as an environmental variable
load_dotenv()
if os.getenv("app_key"):
    app_key = os.getenv("app_key")
    app_secret = os.getenv("app_secret")
    refresh_token = os.getenv("rtoken")
else:
    app_key = st.secrets["app_key"]
    app_secret = st.secrets["app_secret"]
    refresh_token = st.secrets["rtoken"]


# Retrieving an access token for the current session
def retrieve_DBtoken(key, secret, refresh_token):
    """
    Use Dropbox App key/secret and a refresh token to authenticate
    via Dropbox API v2.
    return:  a freshly generated access token
    """
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': key,
        'client_secret': secret,
    }
    response = requests.post('https://api.dropbox.com/oauth2/token',
                             data=data)
    response_data = json.loads(response.text)
    access_token = response_data["access_token"]
    return access_token


def load_dbx(file):
    """
    Download a CSV file from Dropbox
    return: file as a dataframe
    """
    atoken = retrieve_DBtoken(app_key, app_secret, refresh_token)
    # Loading a Dropbox client
    dbx = dropbox.Dropbox(atoken)
    # Downloading Dropbox files
    _, res = dbx.files_download(file)
    data = res.content
    # Reading data from files
    try:
        with BytesIO(data) as dfile:
            df = pd.read_csv(dfile, encoding='utf-8')
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=variables.columns)


def upload_dbx(file):
    """
    Upload a CSV local file to Dropbox
    If file already exist it will be overwrited
    """
    atoken = retrieve_DBtoken(app_key, app_secret, refresh_token)
    # Loading a Dropbox client
    dbx = dropbox.Dropbox(atoken)
    # Reading data from files
    try:
        with open(file, 'rb') as f:
            dbx.files_upload(f.read(),
                             variables.file_dbx,
                             mode=dropbox.files.WriteMode.overwrite)
    except Exception as e:
        st.warning('File not uploaded on Dropbox: ' + str(e))
