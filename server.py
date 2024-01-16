from flask import Flask, request, render_template, flash
from promethee import Promethee

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]'

@app.route('/', methods=['GET'])
def welcome():
    alternatives = []
    criterions = []
    criterionWeight = []
    generateTable = False
    criterionImportance=[]
    values=[[]]
    finalValues = 0
    
    for arg in range (len(request.args.getlist("alternative"))):
        if (arg < len(alternatives)):
            alternatives[arg] = request.args.getlist("alternative")[arg]
        else:
            alternatives.append(request.args.getlist("alternative")[arg])
    
            
    for crweight in range (len(request.args.getlist("criterionWeight"))):
        if (crweight < len(criterionWeight)):
            criterionWeight[crweight] = float(request.args.getlist("criterionWeight")[crweight])
        else:
            criterionWeight.append(float(request.args.getlist("criterionWeight")[crweight]))
            
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
            
    values=[[0 for x in range(len(criterions))] for y in range(len(alternatives))] 
        
    if (sum(criterionWeight) < 1):
        flash("Criterions weight are to low")
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= values,
                               generateTable= False,
                               finalCalculation = finalValues)
    
    if (sum(criterionWeight) > 1):
        flash("Criterions weight are to high")
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= values,
                               generateTable= False,
                               finalCalculation = finalValues)

    if (request.args.get('generateTable') != None  and len(alternatives) > 0 and len(criterions) > 0):
        generateTable = True
        
    if ('row00' in str(request.args)):
        for alt in range(len(alternatives)):
            row=[0 for x in range(len(criterions))]
            for c in range (len(criterions)):
                whichRow='row'+str(alt)+str(c)
                try :
                    row[c] = int(request.args.get(whichRow))
                except :
                    row[c] = 0
            if (alt < len(values)):
                values[alt] = row
            else:
                values.append(row)
    
    if (request.args.get('startCalculation') != None and len(alternatives) > 0 and len(criterions) > 0):
        PrometheeCalc = Promethee(alternatives, criterionWeight, criterions, criterionImportance, values)
        finalValues = PrometheeCalc.recommendations

    if request.method == 'GET':
        return render_template('base.html', 
                               alternatives = alternatives, 
                               criterions = criterions, 
                               criterionWeight = criterionWeight, 
                               numberOfCriterions = len(criterions), 
                               numberOfAlternatives=len(alternatives), 
                               name=alternatives, 
                               values= values,
                               generateTable= generateTable,
                               finalCalculation = finalValues)


    

app.run(host='0.0.0.0',debug=True, port=1234, use_reloader=False)