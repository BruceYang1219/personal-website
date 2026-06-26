from flask import Flask
from flask import render_template
from flask import request
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    with open("messages.txt", "a", encoding="utf-8") as f:
        f.write(f"{name},{email},{message}\n")

    # Send email notification
    msg = EmailMessage()
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")
    msg['Subject'] = "New Message from Contact Form"
    msg['From'] = os.getenv("EMAIL_ADDRESS")
    msg['To'] = os.getenv("EMAIL_ADDRESS")

    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)

    return render_template("message_sent.html")


if __name__ == "__main__":
    app.run(debug=True)