# Importing the time module for handling time-related operations
import time
# Importing the requests module for making HTTP requests
import requests
# Importing the selectorlib module for data extraction from HTML
import selectorlib
# Importing the smtplib module for sending email
import smtplib
# Importing the ssl module for SSL/TLS support
import ssl

# URL to scrape
URL = 'https://programmer100.pythonanywhere.com/tours/'

# Function to scrape the HTML content from the specified URL
def scrape(url):
    # Sending a GET request to the URL
    response = requests.get(url)
    # Extracting the HTML content from the response
    source = response.text
    # Returning the HTML source
    return source

# Function to extract data using a YAML selector file
def extract(source):
    # Loading the selector file
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    # Extracting data using the selector
    value = extractor.extract(source)['tours']
    # Returning the extracted data
    return value

# Function to send an email notification
def send_email(message):
    # SMTP server host
    host = "smtp.gmail.com"
    # SMTP port for SSL connection
    port = 465

    # Email address used for sending the email
    username = "chadoneal3@gmail.com"
    # Password for the email account
    password = os.getenv("TOUR_PASSWORD")

    # Email address of the recipient
    receiver = "chadoneal3@gmail.com"
    # Creating an SSL context for secure connection
    context = ssl.create_default_context()

    # Establishing a connection to the SMTP server
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        # Logging in to the email account
        server.login(username, password)
        # Sending the email
        server.sendmail(username, receiver, message)
    # Printing a confirmation message after sending the email
    print('Email sent!')

# Function to store extracted data in a file
def store(extracted):
    # Opening the file in append mode
    with open('data.txt', 'a') as file:
        # Writing the extracted data to the file
        file.write(extracted + '\n')

# Function to read data from a file
def read():
    # Opening the file in read mode
    with open('data.txt', 'r') as file:
        # Returning the content of the file
        return file.read()


if __name__ == '__main__':
    # Main program logic
    while True:  # Running an infinite loop
        # Scraping the specified URL
        scraped = scrape(URL)
        # Extracting data from the scraped HTML
        extracted = extract(scraped)
        # Printing the extracted data
        print(extracted)
        # Reading existing data from the file
        content = read()
        # Checking if there are upcoming tours
        if extracted != 'No upcoming tours':
            # Checking if the extracted data is not already in the file
            if extracted not in content:
                # Storing the extracted data in the file
                store(extracted)
                # Sending an email notification
                send_email(message='Tours scraped!')
        # Waiting for 3 minutes before scraping again
        time.sleep(180)


