# Website to scrape from: http://programmer100.pythonanywhere.com/tours/

import requests, selectorlib, smtplib, ssl, os

filepath = "data.txt"
source_file = "extract.yml"
url = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """Scrapes the page source from URL"""
    request = requests.get(url, headers=HEADERS)
    text = request.text
    return text

def extract(source, source_file=source_file):
    """Extracts data from source page"""
    extractor = selectorlib.Extractor.from_yaml_file(source_file)
    value = extractor.extract(source)["tours"]
    return value

def store(extracted, filepath=filepath):
    """Writes to text file the extracted data"""
    with open(filepath, "a") as file:
        file.write(extracted + "\n")

def read(extracted, filepath=filepath):
    with open(filepath, "r") as file:
        return file.read()

def send_email(message):
    """Sends message to the target email address"""
    host = "smtp.gmail.com"
    port = 465

    username = "khui3850@gmail.com"

    password = os.getenv("PASSWORD")        

    target = "khui3850@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, target, message)

if __name__ == "__main__":
    scraped = scrape(url)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message="New Event Found")