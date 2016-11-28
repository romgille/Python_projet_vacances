from flask import render_template
from flask_mail import Message
from app import mail, models


class Mail:
    # send_mail
    # procedure to send mail
    #
    # @param subject string 
    # @param sender sender
    # @param recipients [string] array of recipients
    # @param text_body string 
    #  @param html_body string
    @staticmethod
    def send_mail(subject, recipients, text_body, html_body):
        message = Message(subject, recipients=recipients)
        message.body = text_body
        message.html = html_body

        mail.send(message)

    @staticmethod
    def add_vacation_notification(user, dates):
        responsable = models.User.query.get(user.resp_id)
        user.send_mail("Prise de congée de " + user.nom + " " + user.prenom,
                       [responsable.email],
                       render_template("app/templates/mail/addVacation.txt", user=user, responsable=responsable,
                                       dates=dates),
                       "")  # render_template ("app/templates/mail/addVacation.html", user=user,
        # responsable=responsable, dates=dates))
