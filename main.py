# Importing necessary modules
import time  # Handling time-related operations
import requests  # Making HTTP requests
import selectorlib  # Data extraction from HTML
import smtplib  # Sending email
import ssl  # SSL/TLS support
import sqlite3  # Database operations
import os  # Operating System operations

# URL to scrape
URL = 'https://programmer100.pythonanywhere.com/tours/'

# Establishing a connection to the SQLite database
connection = sqlite3.connect('data.db')  # Connecting to the SQLite database file named 'data.db'
cursor = connection.cursor()  # Creating a cursor object to execute SQL queries


# Function to scrape HTML content from the specified URL
def scrape(url):
    try:
        response = requests.get(url,
                                timeout=10)  # Sending a GET request to the specified URL with a timeout of 10 seconds
        response.raise_for_status()  # Raise an HTTPError for bad response status
        source = response.text  # Extracting the HTML content from the response
        return source  # Returning the HTML source
    except requests.exceptions.RequestException as e:
        print(f"Failed to scrape URL: {e}")
        return None  # Return None if scraping fails


# Function to extract data using a YAML selector file
def extract(source):
    try:
        extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')  # Loading the selector file for extraction
        value = extractor.extract(source)['tours']  # Extracting data using the selector
        return value.strip() if value else None  # Returning the extracted data, stripped of leading and trailing whitespaces
    except selectorlib.ExtractorError as e:
        print(f"Failed to extract data: {e}")
        return None  # Return None if extraction fails


# Function to send an email notification
def send_email(message):
    try:
        host = "smtp.gmail.com"  # SMTP server host
        port = 465  # SMTP port for SSL connection

        username = "chadoneal3@gmail.com"  # Email address used for sending the email
        password = os.getenv(
            "TOUR_PASSWORD")  # Retrieving the email account password securely from environment variables

        receiver = "chadoneal3@gmail.com"  # Email address of the recipient
        context = ssl.create_default_context()  # Creating an SSL context for secure connection

        with smtplib.SMTP_SSL(host, port, context=context) as server:  # Establishing a connection to the SMTP server
            server.login(username, password)  # Logging in to the email account
            server.sendmail(username, receiver, message)  # Sending the email
        print('Email sent!')  # Printing a confirmation message after sending the email
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


# Function to store extracted data in the database
def store(extracted):
    try:
        row = extracted.split(',')  # Splitting the extracted data into individual elements
        print("Extracted row:", row)  # Debugging statement
        if len(row) == 3:  # Checking if there are three elements
            cursor.execute("INSERT INTO events (band, city, date) VALUES (?,?,?)",
                           row)  # Inserting data into the database
            connection.commit()  # Committing the transaction
        else:
            print("Invalid data format. Unable to store in the database.")
    except sqlite3.Error as e:
        print(f"Failed to store data in database: {e}")


# Function to read data from the database
def read(extracted):
    try:
        row = extracted.split(',')  # Splitting the extracted data into individual elements
        print("Extracted row:", row)  # Debugging statement
        if len(row) == 3:  # Checking if there are three elements
            band, city, date = row[0], row[1], row[2]  # Unpacking the row into band, city, and date variables
            cursor.execute("SELECT band, city, date FROM events WHERE band=? AND city=? AND date=?",
                           (band.strip(), city.strip(), date.strip()))  # Retrieving data from the database
            rows = cursor.fetchall()  # Fetching all matching rows
            return rows  # Returning the fetched rows
        else:
            print("Invalid data format. Unable to read from the database.")
            return []
    except sqlite3.Error as e:
        print(f"Failed to read data from database: {e}")
        return []


# Main program logic
if __name__ == '__main__':
    while True:  # Running an infinite loop
        scraped = scrape(URL)  # Scraping HTML content from the specified URL
        if scraped:  # Check if scraping is successful
            extracted = extract(scraped)  # Extracting data from the scraped HTML
            if extracted:  # Check if extraction is successful
                print("Extracted data:", extracted)  # Debugging statement
                rows = read(extracted)  # Reading data from the database
                if extracted != 'No upcoming tours':  # Checking if there are upcoming tours
                    if not rows:  # Checking if the extracted data is not already in the database
                        store(extracted)  # Storing the extracted data in the database
                        send_email(message='Tours scraped!')  # Sending an email notification
        time.sleep(45)  # Waiting for 45 seconds before scraping again





