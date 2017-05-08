#!/usr/bin/python

import cgi
import cgitb
import math

cgitb.enable()

print "Content-type: text/html\n\n"

form=cgi.FieldStorage()

try:
  unitCode = int(form["unitCode"].value)
except:
  print("Error: Unit's not selected - odd this shouldn't happen, try refreshing")
  quit()
  
try:
  currentlevel = int(form["sbr"].value)
except:
  print("Error: Please enter an SBR - number only")
  quit()

if unitCode == 0:
  currentlevel = currentlevel*0.058479 # convert to american units, micromol/L -> mg/dL

try:
  gestation = int(form["gestation"].value)
except:
  print("Error: Please select a gestation")
  quit()

try:
  photoStarted = int(form["photoStarted"].value)
except:
  print("Error: When was phototherapy started")
  quit()

try:
  hoursOld = int(form["hoursOld"].value)
except:
  print("Error: How old were they for the current SBR")
  quit()

if hoursOld < 0 or hoursOld > 168:
	print("Error: Please choose an age less than 7 days - this formula is not validated for anything beyond 7 days")
	exit()

try:
  riskFactors = int(form["risk"].value)
except:
  print("Error: Please select if risk factors are present")
  quit()

hours4 = math.pow(hoursOld,4)
hours3 = math.pow(hoursOld,3)
hours2 = math.pow(hoursOld,2)

if gestation > 37 and riskFactors == 0:
	risk = 1
	print("Low risk line <br />")

if (gestation > 37 and riskFactors == 1) or (gestation > 34 and gestation < 38 and riskFactors == 0):
	risk = 2
	print("Medium risk line <br />")
	
if gestation > 34 and gestation < 38 and riskFactors == 1:
	risk = 3
	print("High risk line <br />")

## Risk line according to 2004 AAP guidelines - derived manually from modelling the papers graphs

if risk == 1:
	threshold = 0.0000000025*hours4+0.0000001153*hours3-0.0008729413*hours2+0.2156253999*hoursOld+6.7802889577
elif risk == 2:
	threshold = 0.0000000001*hours4+0.0000016763*hours3-0.001125756*hours2+0.2174603609*hoursOld+5.1433264534
elif risk == 3:
	threshold = 0.0000000234*hours4-0.0000055621*hours3-0.0004163134*hours2+0.1830601843*hoursOld+3.7994


if unitCode == 0:
  print("Phototherapy threshold = " + str("{0:.0f}".format(threshold/0.058479))+", ")
  diff = currentlevel/0.058479 - threshold/0.058479
else:
  print("Phototherapy threshold = " + str("{0:.2f}".format(threshold))+", ")
  diff = currentlevel - threshold

if diff < 0:
	print("currently " + str("{0:.1f}".format(diff)) + " below the line.<br />")
else:
	print("currently " + str("{0:.1f}".format(diff)) + " above the line.<br />")

## Ceaseing threshold

if gestation < 38:
	gestScore = 15
else:
	gestScore = 0

score = gestScore - (7 * (photoStarted/24)) - (4 * (threshold - currentlevel)) + 50

print("Score " + str("{0:.0f}".format(score)))

if score < 9:
	print("<div class='alert alert-success' role='alert'>Risk of rebound <strong>0.3%</strong> - get 'em outta here!</div>")
elif score > 9 and score < 20:
	print("<div class='alert alert-info' role='alert'>Risk of rebound <strong>2-3%</strong> - we can probably stop</div>")
elif score > 19 and score < 30:
	print("<div class='alert alert-info' role='alert'>Risk of rebound <strong>4.5-6.1%</strong> - do you live close by?</div>")
elif score > 29 and score < 40:
	print("<div class='alert alert-warning' role='alert'>Risk of rebound <strong>17-19%</strong> - I don't like those odds</div>")
elif score > 39 and score < 50:
	print("<div class='alert alert-warning' role='alert'>Risk of rebound <strong>25-33%</strong> - I'd want my child under lights</div>")
elif score > 49:
	print("<div class='alert alert-danger' role='alert'>Risk of rebound <strong>40-50%</strong> - tell them they're dreaming...</div>")