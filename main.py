# imports for grabber
from selenium import webdriver
from bs4 import BeautifulSoup

# imports for sending email
from email.mime.text import MIMEText
import smtplib, ssl

def get_source():
    url = 'https://mhnow.cc/'
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source # get html source
    driver.quit()
    return html

def send_email(subject, body, sender, recipients, password):
    context = ssl.create_default_context()
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def main():
    soup = BeautifulSoup(get_source(), "html.parser")
    count = 0
    body = ""
    for monster in soup.find_all(string="黑角龍"): # find first matching monster
        stars = monster.find_parent('div').find_previous_sibling('div')
        starCount = len(list(stars.children))
        if starCount == 1 or starCount == 5: # find 1 or 6 or 10 stars (i think)
            count += 1
            data = monster.find_parent('div').find_parent('div').find_parent('div').find_next_sibling('div').find('span').string
            body += data + '\n'
    body += str(count) + ' monsters are found'
    print(body)

    ## in case you want to send email as an output
    ## uncomment the following lines and fill in the information
    ## note: if you want to send with your gmail account, you will need an App Password
    ## see App Passwords - https://support.google.com/mail/answer/185833?hl=en

    # subject = "Black Diablos Appearance Report"
    # sender = "sender@gmail.com"
    # recipients = ["receiver@gmail.com"]
    # password = "password"
    # send_email(subject, body, sender, recipients, password)

if __name__ == "__main__":
    main()