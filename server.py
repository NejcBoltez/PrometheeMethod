from flask import Flask, request, render_template, flash
from promethee import Promethee
import copy

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]'

@app.route('/', methods=['GET'])
def welcome():
    alternatives = []
    criterions = []
    criterionWeight = []
    generateTable = False
    criterionImportance=[]
    userValues=[[]]
    finalValues = 0
    
    for arg in range (len(request.args.getlist("alternative"))):
        if (arg < len(alternatives)):
            alternatives[arg] = request.args.getlist("alternative")[arg]
        else:
            alternatives.append(request.args.getlist("alternative")[arg])
    
            
    for crweight in range (len(request.args.getlist("criterionWeight"))):
        try:
            if (crweight < len(criterionWeight)):
                criterionWeight[crweight] = float(request.args.getlist("criterionWeight")[crweight])
            else:
                criterionWeight.append(float(request.args.getlist("criterionWeight")[crweight]))
        except Exception as e:
            if (crweight < len(criterionWeight)):
                criterionWeight[crweight] = 0.0
            else:
                criterionWeight.append(0.0)
            
    for cr in range (len(request.args.getlist("criterion"))):
        if (cr < len(criterions)):
            criterions[cr] = request.args.getlist("criterion")[cr]
        else:
            criterions.append(request.args.getlist("criterion")[cr])

    for ci in range (len(request.args.getlist("importance"))):
        if (ci < len(criterionImportance)):
            criterionImportance[ci] = request.args.getlist("importance")[ci]
        else:
            criterionImportance.append(request.args.getlist("importance")[ci])
            
    
    if (len(criterions) <= 1):
        flash("Please add some criterions ")
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= userValues,
                               generateTable= False,
                               finalCalculation = finalValues)
    if (len(alternatives) <= 1):
        flash("Please add some more alternatives ")
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= userValues,
                               generateTable= False,
                               finalCalculation = finalValues)
    if (0<sum(criterionWeight) < 0.99):
        flash("Criterions weight are to low")
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= userValues,
                               generateTable= False,
                               finalCalculation = finalValues)
    print(sum(criterionWeight))
    if (sum(criterionWeight) > 1.1):
        flash("Criterions weight are to high")
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= userValues,
                               generateTable= False,
                               finalCalculation = finalValues)
    print(len(criterions))
    
    if (request.args.get('generateTable') != None  and len(alternatives) > 0 and len(criterions) > 0):
        generateTable = True
    userValues=[[0 for x in range(len(criterions))] for y in range(len(alternatives))] 
    if ('row00' in str(request.args)):
        for alt in range(len(alternatives)):
            row=[0 for x in range(len(criterions))]
            for c in range (len(criterions)):
                whichRow='row'+str(alt)+str(c)
                try :
                    row[c] = int(request.args.get(whichRow))
                except :
                    row[c] = 0
            if (alt < len(userValues)):
                userValues[alt] = row
            else:
                userValues.append(row)

    print(userValues)
    if (request.args.get('startCalculation') != None and len(alternatives) > 0 and len(criterions) > 0):
        PrometheeCalc = Promethee(alternatives, criterionWeight, criterions, criterionImportance, userValues)
        finalValues = PrometheeCalc.recommendations
    print(userValues)
    if request.method == 'GET':
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= userValues,
                               generateTable= generateTable,
                               finalCalculation = finalValues)


    

app.run(host='0.0.0.0',debug=True, port=1234, use_reloader=False)