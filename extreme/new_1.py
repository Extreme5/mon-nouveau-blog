# Import Required Library
from tkinter import *
from tkcalendar import Calendar
 
# Create Object
root = Tk()
 
# Set geometry
root.geometry("400x400")
 
# Add Calendar
cal = Calendar(root, selectmode = 'day',
               year = 2020, month = 5,
               day = 22)
 
cal.pack(pady = 20)
 
def grad_date():
    date.config(text = "Selected Date is: " + cal.get_date())
 
# Add Button and Label
Button(root, text = "Get Date",
       command = grad_date).pack(pady = 20)
 
date = Label(root, text = "")
date.pack(pady = 20)
 
# Execute Tkinter
root.mainloop()

input:invalid+span:after {
	position: absolute;
	content: '✖ indisponible';
	padding-left: 5px;
	}
	
	input:valid+span:after {
	position: absolute;
	content: '✓ disponible';
	padding-left: 5px;
	}
	
	input.bouton{
	border-radius: 10px ;
	background-color: blue;
	font-size: 30px ;
	}
	.styled {
    border: 0;
    line-height: 2.5;
    padding: 0 20px;
    font-size: 1rem;
    text-align: center;
    color: #fff;
    text-shadow: 1px 1px 1px #000;
    border-radius: 10px;
    background-color: rgba(3, 164, 241, 1);
    background-image: linear-gradient(to top left,
                                      rgba(0, 0, 0, .2),
                                      rgba(0, 0, 0, .2) 30%,
                                      rgba(0, 0, 0, 0));
    box-shadow: inset 2px 2px 3px rgba(255, 255, 255, .6),
                inset -2px -2px 3px rgba(0, 0, 0, .6);
}
{% extends "bases.html"%}

{% block content %}

<center>
<h1 class = "mt-5">Votre massage a bien été réservé.</h1>
</center>

{% endblock %}

<a href="{% url 'reservation_temps'%}" class="btn btn-primary">réserver un créneau(à partir de 60c)</a>

import cgi
import cgitb

# à retirer
cgitb.enable()

form = cgi.fieldStorage()

if form.getvalue("mail") :
    mail = form.getvalue("mail")
    
    conn = sqlite3.connect('bdd')
    cur = conn.cursor()
    sql = "INSERT INTO reservation (email) VALUES ('mail')"
    count = cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


else:
    raise Exeption("adresse mail non transmise")


href="{% url 'reservation_date'%}" 
 href="{% url 'reservation_date'%}"
 href="{% url 'reservation_date'%}"
 href="{% url 'reservation_date'%}"


<!-- <div class="button-container"> -->
<!-- <center> -->
	<!-- <h3 class="mt-4 mb-5">Combien de temps de massage voulez-vous ?</h3> -->
	<!-- <a id="btn" onclick="clicked(5)" class="btn btn-primary mb-3">5min</a> -->
	<!-- <a id="btn" onclick="clicked(10)" class="btn btn-primary mb-3">10min</a> -->
	<!-- <a id="btn" onclick="clicked(15)" class="btn btn-primary mb-3" leftmargin="100">15min</a> -->
	<!-- <a id="btn" onclick="clicked(30)" class="btn btn-primary mb-3">30min (uniquement pour les thalassos)</a> -->

		<!-- <script> -->
			<!-- const btn = document.getElementById('btn') -->
			
			<!-- function temps(valeur){ -->
				<!-- document.getElementById("temps").value = valeur -->
				
				<!-- var req = new XMLHttpRequest(); -->
				<!-- req.onload = temps; -->
				<!-- req.open("GET", "views.py", true); -->
				<!-- req.send(valeur); -->
			<!-- } -->
		<!-- </script> -->
<!-- </center> -->
<!-- </div> -->

<!-- <script> -->
<!-- function envoyer(valeur){ -->
<!-- document.getElementById("date").value = valeur; -->
<!-- } -->
<!-- </script> -->
 
<!-- <button onclick="envoyer(9);">Matin</button><br><br> -->
<!-- <button onclick="envoyer(15);">Apres Midi</button><br><br> -->
  
<!-- <form action="ton_script.php" method="post">  -->
    <!-- <label> Date: </label> -->
    <!-- <input type="text" id="date" readonly></input><br><br> -->
    <!-- <input type="submit" value="Soumettre"> -->
<!-- </form> -->