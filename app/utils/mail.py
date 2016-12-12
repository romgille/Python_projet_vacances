from flask import render_template
from flask_mail import Message
from app import mail, models
from enum import Enum


class Mail :

    # send_mail
    # procedure to send mail
    #
    # @param subject string : mail subject
    # @param recipients [string] : array of recipients
    # @param text_body string : mail text content
    # @param html_body string : mail html content
    @staticmethod
    def send_mail (subject, recipients, text_body ) : #, html_body) :
        message = Message (subject, recipients = recipients)
        message.body = text_body
        #message.html = html_body

        mail.send(message)


    # ENUM TYPE notification_type
    class notification_type (Enum) :
        add_vacation        = 1,
        remove_vacation     = 2


    # vacation_notification
    # procedure to send a mail notification 
    #
    # @param user Model.User : user 
    # @param dates_start datetime.date : date of start
    # @param dates_end datetime.date : date of end
    # @param notificationType notification_type : type of mail to send
    @staticmethod
    def vacation_notification (user, dates, notificationType) :
        responsable = models.User.query.get(user.resp_id)
        mail_object = "[AUTO] [app/vacances]"
        template_base_name = "mails/"
        
        if notificationType == Mail.notification_type.add_vacation :
            mail_object = mail_object + "Prise de congés de " + user.nom + " " + user.prenom
            template_base_name = template_base_name + "add_vacation"
        elif notificationType == Mail.notification_type.remove_vacation :
            mail_object = mail_object + "Retrait de congés de " + user.nom + " " + user.prenom
            template_base_name = template_base_name + "remove_vacation"
            
        Mail.send_mail (
            mail_object,
            [responsable.email],
            render_template (
                template_base_name + ".txt",
                user = user,
                responsable = responsable,
                dates = {'debut': dates[0], 'fin': dates[1]})  )#,
            #render_template (
            #    template_base_name + ".html",
            #    user = user,
            #    responsable = responsable, 
            #    dates = {'}debut': dates[0], 'fin': dates[1]}))
                
                
                
                
                
