import requests, selectorlib, smtplib, ssl, os, time, sqlite3

"INSERT INTO events VALUES('Tigers', 'Tiger City, '2088.10.14')"
"SELECT * FROM events WHERE data='2088.10.15'"

connection = sqlite3.connect("./app10/data.db")

filepath = "./app10/data.txt"
source_file = "./app10/extract.yml"
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

def store(extracted, filepath=filepath):
    """Writes data to database file"""
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted, filepath=filepath):
    """Opens file to be read"""
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == "__main__":
    while True:
        scraped = scrape(url)
        extracted = extract(scraped)
        print(extracted)
        
        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="New Event Found")

        time.sleep(2)