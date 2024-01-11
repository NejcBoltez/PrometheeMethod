from flask import Flask, request,render_template
from promethee import Promethee

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    print("TEST: " + str(request.args.get('alternatives')))
    alternatives = []
    criterions = []
    criterionWeight = []
    generateTable = False

    values=[[]]
    print("VALUES: " + str(values))
    print("VALUES: " + str(len(values)))
    
    for arg in range (len(request.args.getlist("alternative"))):
        if (arg < len(alternatives)):
            alternatives[arg] = request.args.getlist("alternative")[arg]
        else:
            alternatives.append(request.args.getlist("alternative")[arg])
    
            
    for crweight in range (len(request.args.getlist("criterionWeight"))):
        if (crweight < len(criterionWeight)):
            criterionWeight[crweight] = request.args.getlist("criterionWeight")[crweight]
        else:
            criterionWeight.append(request.args.getlist("criterionWeight")[crweight])
            
    for cr in range (len(request.args.getlist("criterion"))):
        if (cr < len(criterions)):
            criterions[cr] = request.args.getlist("criterion")[cr]
        else:
            criterions.append(request.args.getlist("criterion")[cr])
            
    values=[[0 for x in range(len(criterions))] for y in range(len(alternatives))] 
        
        
    if (request.args.get('generateTable') != None):
        generateTable = True
        
    if ('row00' in str(request.args)):
        for alt in range(len(alternatives)):
            row=[0 for x in range(len(criterions))]
            for c in range (len(criterions)):
                whichRow='row'+str(alt)+str(c)
                print('row'+str(alt)+str(c))
                try :
                    row[c] = int(request.args.get(whichRow))
                except :
                    row[c] = 0
            if (alt < len(values)):
                values[alt] = row
            else:
                values.append(row)
    finalValues = 0
    if (request.args.get('startCalculation') != None):
        PrometheeCalc = Promethee(alternatives, criterionWeight, criterions, ["Beneficial", "Non-Beneficial", "Beneficial"],values)
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