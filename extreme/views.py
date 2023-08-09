import sqlite3
from django import forms
from django.urls import path,include
# pour la date
from datetime import*
# pour les mails
from django.core.mail import send_mass_mail
from django.contrib import messages
# pour les requêtes AJAX
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
path_database = "/home/Extreme1/extreme1.eu.pythonanywhere.com/bdd.db"
# path_database = "/Users/albancadic/Documents/mon_site/siteweb/bdd.db"
from siteweb.settings import *

global time30
time30 = True

# Fonction qui gère les e-mails

import email.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, message, to_email):
    # try:
    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    message = Mail(from_email=DEFAULT_FROM_EMAIL, to_emails=to_email, subject=subject, html_content=message)
    response = sg.send(message)
    return True
    # except Exception as e:
    #     print(str(e))
    #     return False

# Create your views here.
def home(request):
    global time30
    time30 = True

    return render(request,'home.html')

def reservation1(request):
    return render(request,'reservation1.html')

def reservation2_thalasso(request):
    global form_temps
    global massage

    form_temps = 30
    massage = 'thalasso'

    return render(request,'reservation2_thalasso.html')

def thalasso_mesure(request):
    return render(request,'thalasso_mesure.html')

def reservation2_sur_mesure(request):
    global massage
    global option
    global form_temps

    class massage_mesure(forms.Form):
        type_massage = forms.CharField(label='type_massage', max_length=100)
        type_option = forms.CharField(label='type_option', max_length=100)
        temps = forms.CharField(label='form_temps', max_length=100)

    if request.method == 'POST':
        list_massage = request.POST.getlist("type_massage")
        setm1 = set(list_massage)
        setm2 = {'épaules, nuque', 'pieds, jambes(huiles gratuites)', 'dos', 'bras, mains', 'tout le corps', 'tête', 'sur place'}
        intersectionM = list(setm1 & setm2)

        list_option = request.POST.getlist("type_option")
        seto1 = set(list_option)
        seto2 = {'une 2ème paire de mains', 'le coussin massant', 'le rouleau', 'insecte masseur', 'le masse tête', 'aucune option', ''}
        intersectionO = list(seto1 & seto2)

        temps = request.POST["form_temps"]
        time_list_verification = ['5', '10', '15']
        
        if not(intersectionM) or not(intersectionO):
            error_message = "Une erreur inattendue est apparu, désolé. Vous pouvez essayer de recharger la page."
            return render(request, 'reservation2_sur_mesure.html', {'error_message': error_message})

        else :
            if temps in time_list_verification :
                massage = ','.join(list_massage)
                option = ','.join(list_option)
                form_temps = int(temps)

                return render(request, 'reservation_date.html')

    return render(request, 'reservation2_sur_mesure.html')

def reservation2_pret(request):
    global massage
    global time30
    
    class type(forms.Form):
        type_massage = forms.CharField(label='type_massage', max_length=100)
    
    if request.method == 'POST':
        
        formulaire = type(request.POST)
        
        if formulaire.is_valid():
            
            massage = request.POST["type_massage"]
            time30 = False
            
            return render(request,'reservation_temps.html')
        
    return render(request,'reservation2_pret.html')

def reservation_temps(request):
    global form_temps
    global time30
    global massage
    
    class timming(forms.Form):
        temps = forms.CharField(label='temps', max_length=100)
    
    if request.method == 'POST':
        
        formulaire = timming(request.POST)
        
        if formulaire.is_valid():
            
            form_temps = request.POST["temps"]
            form_temps = int(form_temps)
            if form_temps == 30:
                massage = 'thalasso'
            
            return render(request,'reservation_date.html')
    
    return render(request,'reservation_temps.html', {'time30': time30})

def reservation_date(request):
    global form_date
    global form_hour
    global form_temps
    global time_list
    
    class dating(forms.Form):
        date = forms.CharField(label='date', max_length=100)
        hour = forms.CharField(label='hour', max_length=100)
    
    if request.method == 'POST':
        
        try:
            json_data = json.loads(request.body)  # Convertir la charge utile JSON en un objet Python
            selected_date = json_data.get('selectedDate')  # Récupérer la date sélectionnée

            # Traiter la date sélectionnée
            conn = sqlite3.connect(path_database)
            cur = conn.cursor()
            sql = "SELECT time_list FROM reservation WHERE date = ?"
            cur.execute(sql, (selected_date,))
            results = cur.fetchall()
            cur.close()
            conn.close()

            time_list_final = [time_str.strip() for result in results for time_str in result[0].split(',')]

            iteration = len(results)
            iteration2 = int(form_temps/5)
            for i in range(iteration):
                list = results[i]
                string1 = list[0]
                date_string = datetime.strptime(string1[0:7], '%H : %M')
                for j in range(iteration2):
                    final_string = date_string-timedelta(minutes = (j+1)*5)
                    final_date = final_string.time().strftime('%H : %M')
                    time_list_final.append(final_date)
                    print(time_list_final)


            # Retourner une réponse JSON
            response_json = {
                'time_list': time_list_final
            }
            return JsonResponse(response_json)
        
        except json.JSONDecodeError:

            form = dating(request.POST)
            
            if form.is_valid():
                
                form_date = request.POST["date"]
                form_hour = request.POST["hour"]
                form_hour = datetime.strptime(form_hour, '%H : %M')

                iteration_number = int((form_temps/5)+1)
                time_list = []
                for i in range(iteration_number):
                    number = (i)*5
                    add_number = form_hour + timedelta(minutes = number)
                    add_number = add_number.time()
                    add_number = add_number.strftime('%H : %M')
                    time_list.append(add_number)
                    
                time_list = ', '.join(time_list)
                
                return render(request, 'reservation4.html')

    return render(request,'reservation_date.html')

def confirmation(request):
    return render(request,'confirmation.html')

def reservation4(request):
    global form_date
    global form_temps
    global form_hour
    global massage
    global option
    global time_list
    
    
    class mail(forms.Form):
        email = forms.CharField(label='email', max_length=100)
        
    if request.method == 'POST':
        
        form_mail = mail(request.POST)
        
        if form_mail.is_valid():


            mail_to = request.POST["email"]
            heure_fin = form_hour + timedelta(minutes=form_temps)
            heure_fin = heure_fin.time()
            form_hour = form_hour.time()

            if 'option' in globals():
                
                conn = sqlite3.connect(path_database)
                cur = conn.cursor()
                sql = "INSERT INTO reservation (email,date,moment,fin,type_massage,\"option\",time_list) VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(mail_to, form_date, form_hour, heure_fin, massage, option, time_list)
                count = cur.execute(sql)
                conn.commit()
                cur.close()
                conn.close()

                # corps_message = ("Éxtrême", f"Bonjour, {mail_to} a réservé le massage {massage} avec l'option {option} pour {form_temps} min chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.", 
                #                 f"albancadic.bruz@orange.fr", ["massage.extreme@orange.fr", "bastiencadic@orange.fr"])
            
                # corps_message_client = ("Réservation chez l'Éxtrême", 
                #                         f"Bonjour, vous avez bien réservé le massage {massage} avec l'option {option} chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.\n\nNous vous attendons à l'horaire réservé pour vous fournir un moment de détente extrême de {form_temps}min.\n\n⚠ Si vous avez réservé entre le lundi, et le vendredi, votre réservation peut encore être refusé, surveillez vos mails.\nSi vous n'êtes pas à l'origine de cette demande, merci de répondre à ce message pour nous en informer.\nCordialement, l'équipe dirigeante de l'Éxtrême.", 
                #                         "massage.extreme@orange.fr", [f"{mail_to}"])

                corps_message = f"Bonjour, {mail_to} a réservé le massage {massage} avec l'option {option} pour {form_temps} min chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}."
            
                corps_message_client = f"Bonjour, vous avez bien réservé le massage {massage} avec l'option {option} chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.\n\nNous vous attendons à l'horaire réservé pour vous fournir un moment de détente extrême de {form_temps}min.\n\n⚠ Si vous avez réservé entre le lundi, et le vendredi, votre réservation peut encore être refusé, surveillez vos mails.\nSi vous n'êtes pas à l'origine de cette demande, merci de répondre à ce message pour nous en informer.\nCordialement, l'équipe dirigeante de l'Éxtrême.", 
            
            elif 'massage' in globals():
                
                conn = sqlite3.connect(path_database)
                cur = conn.cursor()
                sql = "INSERT INTO reservation (email,date,moment,fin,type_massage,time_list) VALUES ('%s','%s','%s','%s','%s','%s')" %(mail_to, form_date, form_hour, heure_fin, massage, time_list)
                count = cur.execute(sql)
                conn.commit()
                cur.close()
                conn.close()

                # corps_message = ("Éxtrême", f"Bonjour, {mail_to} a réservé le massage {massage} pour {form_temps} min chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.", 
                #                 f"albancadic.bruz@orange.fr", ["massage.extreme@orange.fr", "bastiencadic@orange.fr"])
            
                # corps_message_client = ("Réservation chez l'Éxtrême", 
                #                         f"Bonjour, vous avez bien réservé le massage {massage} chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.\n\nNous vous attendons à l'horaire réservé pour vous fournir un moment de détente extrême de {form_temps}min.\n\n⚠ Si vous avez réservé entre le lundi, et le vendredi, votre réservation peut encore être refusé, surveillez vos mails.\nSi vous n'êtes pas à l'origine de cette demande, merci de répondre à ce message pour nous en informer.\nCordialement, l'équipe dirigeante de l'Éxtrême.", 
                #                         "massage.extreme@orange.fr", [f"{mail_to}"])

                corps_message = f"Bonjour, {mail_to} a réservé le massage {massage} pour {form_temps} min chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}."
            
                corps_message_client = f"Bonjour, vous avez bien réservé le massage {massage} chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.\n\nNous vous attendons à l'horaire réservé pour vous fournir un moment de détente extrême de {form_temps}min.\n\n⚠ Si vous avez réservé entre le lundi, et le vendredi, votre réservation peut encore être refusé, surveillez vos mails.\nSi vous n'êtes pas à l'origine de cette demande, merci de répondre à ce message pour nous en informer.\nCordialement, l'équipe dirigeante de l'Éxtrême.", 
            
            else:
                
                conn = sqlite3.connect(path_database)
                cur = conn.cursor()
                sql = "INSERT INTO reservation (email,date,moment,fin,time_list) VALUES ('%s','%s','%s','%s','%s')" %(mail_to, form_date, form_hour, heure_fin, time_list)
                count = cur.execute(sql)
                conn.commit()
                cur.close()
                conn.close()
            
                # corps_message = ("Éxtrême", f"Bonjour, {mail_to} a réservé un massage de {form_temps} min chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.", 
                #                 f"albancadic.bruz@orange.fr", ["massage.extreme@orange.fr", "bastiencadic@orange.fr"])
            
                # corps_message_client = ("Réservation chez l'Éxtrême", 
                #                         f"Bonjour, vous avez bien réservé un massage chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.\n\nNous vous attendons à l'horaire réservé pour vous fournir un moment de détente extrême de {form_temps}min.\n\n⚠ Si vous avez réservé entre le lundi, et le vendredi, votre réservation peut encore être refusé, surveillez vos mails.\nSi vous n'êtes pas à l'origine de cette demande, merci de répondre à ce message pour nous en informer.\nCordialement, l'équipe dirigeante de l'Éxtrême.", 
                #                         "massage.extreme@orange.fr", [f"{mail_to}"])

                corps_message = f"Bonjour, {mail_to} a réservé un massage de {form_temps} min chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}."
            
                corps_message_client = f"Bonjour, vous avez bien réservé un massage chez l'Éxtrême le {form_date} de {form_hour} à {heure_fin}.\n\nNous vous attendons à l'horaire réservé pour vous fournir un moment de détente extrême de {form_temps}min.\n\n⚠ Si vous avez réservé entre le lundi, et le vendredi, votre réservation peut encore être refusé, surveillez vos mails.\nSi vous n'êtes pas à l'origine de cette demande, merci de répondre à ce message pour nous en informer.\nCordialement, l'équipe dirigeante de l'Éxtrême.",
            
            # print(EMAIL_HOST_USER)
            # print(EMAIL_HOST_PASSWORD)
            # send_mass_mail ((corps_message, corps_message_client), fail_silently=False)

            send_email("Réservation chez l'Extrême", corps_message_client, mail_to)
            send_email("Extrême", corps_message, "albancadic@gmail.com")
            send_email("Extrême", corps_message, "bastiencadic@orange.fr")


            return render(request,'confirmation.html')
            
    return render(request,'reservation4.html')


def nous(request):
    return render(request,'nous.html')

def contact(request):
    return render(request,'contact.html')