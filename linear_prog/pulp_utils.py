import sys
import os
import pulp
import time
from pulp import solvers

sys.path.append(os.getcwd()+'/../../')

#from common.parc import *
from common import charts

import common.charts
class Params:
    def __init__(self):
            #parametres du solveur
            self.solveur="coin"
            self.logSolveur="on"
            self.solveurToleranceRelative=0.01
            self.solveurMaxTime=30.0
            self.pathCplex="/logiciels/cplex/linux/x86/cplex-126/cplex/bin/x86-64_linux/cplex"

class Model():
    def __init__(self, lp, prod_vars,volume_res=None):
        #Pulp problem
        self.lp=lp
        #variables
        self.prod_vars=prod_vars
        self.volume_res=volume_res
        self.indicators={}

class Results(): 
    def __init__(self,pb):
        self.prod_vars_solution={}
        self.volume_res_solution={}
        self.marginal_costs=[]
        for usine in pb.hydro_plants+ pb.thermal_plants:
                self.prod_vars_solution[usine.name]=[ 0 for t in pb.time_steps]
        

def getResultsModel(pb,model,name):
    results=Results(pb)
          
    for thermal_plant in pb.thermal_plants :
        results.prod_vars_solution[thermal_plant.name]=[]
        for t in pb.time_steps:
            results.prod_vars_solution[thermal_plant.name].append(model.prod_vars[t][thermal_plant].varValue)
    try:
        for usine in pb.hydro_plants:
            results.prod_vars_solution[usine.name]=[]
            for t in pb.time_steps:
               results.prod_vars_solution[usine.name].append(model.prod_vars[t][usine].varValue)
    except:
        pass
    
    #sum of hydroplants
    if (len(pb.hydro_plants)):
        results.prod_vars_solution["totalHydro"]=[]
        for t in pb.time_steps:
            results.prod_vars_solution["totalHydro"].append(sum ([model.prod_vars[t][usine].varValue for usine in pb.hydro_plants]))
        
    results.prod_vars_solution["totalThm"]=[]
    for t in pb.time_steps:
        results.prod_vars_solution["totalThm"].append(sum ([model.prod_vars[t][usine].varValue for usine in pb.thermal_plants]))
    

        
    results.volume_res_solution={}

    for reservoir in pb.reservoirs:
        if(len(str(reservoir.id)))==1:
            res_name="res_0"+str(reservoir.id)
        else:
            res_name="res_"+str(reservoir.id)
        results.volume_res_solution[res_name]=[]
        for t in pb.time_steps:
            results.volume_res_solution[res_name].append(model.volume_res[t][reservoir].varValue)

    getAllVariables(model,name)
    getAllConstraints(model,name)    
    

    return results
     
    
def updateResultsWithSubPbm(sous_pb,pb,model,results):

    for thermal_plant in sous_pb.thermal_plants :
        results.prod_vars_solution[thermal_plant.name]=[]
        for t in pb.time_steps:
            results.prod_vars_solution[thermal_plant.name].append(model.prod_vars[t][thermal_plant].varValue)
    
    for usine in sous_pb.hydro_plants:
            results.prod_vars_solution[usine.name]=[]
            for t in pb.time_steps:
               results.prod_vars_solution[usine.name].append(model.prod_vars[t][usine].varValue)
    
    #sum of hydroplants
    results.prod_vars_solution["totalHydro"]=[]
    for t in pb.time_steps:
        results.prod_vars_solution["totalHydro"].append(sum ([results.prod_vars_solution[usine.name][t] for usine in pb.hydro_plants]))
        
    results.prod_vars_solution["totalThm"]=[]
    for t in pb.time_steps:
        results.prod_vars_solution["totalThm"].append(sum ([results.prod_vars_solution[usine.name][t] for usine in pb.thermal_plants]))
    

        
    results.volume_res_solution={}

    for reservoir in sous_pb.reservoirs:
        if(len(str(reservoir.id)))==1:
            res_name="res_0"+str(reservoir.id)
        else:
            res_name="res_"+str(reservoir.id)
        results.volume_res_solution[res_name]=[]
        for t in pb.time_steps:
            results.volume_res_solution[res_name].append(model.volume_res[t][reservoir].varValue)
    

def printResults(pb, model, name,electricity_prices,results,printIndicators=True):
    programs={"totalThm":results.prod_vars_solution["totalThm"]}  
    
    if(len(pb.hydro_plants)>0):
        programs["totalHydro"]=results.prod_vars_solution["totalHydro"]
    charts.display_EOD(programs, pb, model.indicators, name, pb.demand,electricity_prices,printIndicators)
    

    charts.display_programms(results.prod_vars_solution, pb)
    
    
    stock_min={}
    stock_max={}
    for reservoir in pb.reservoirs:
        for t in pb.time_steps:
          if len(str(reservoir.id))==1:
            res_name="res_0"+str(reservoir.id)
          else:
            res_name="res_"+str(reservoir.id) 
            
        stock_min[res_name]=[]
        stock_max[res_name]=[]    
        for t in pb.time_steps:       
            stock_min[res_name].append(reservoir.minimum_volume)
            stock_max[res_name].append(reservoir.maximum_volume)
    
    if(len(pb.reservoirs)>0):
        charts.display_programms_with_bounds(results.volume_res_solution,stock_min,stock_max, pb,"m3")

def solve(model, name,params=Params()):
    path = model.lp.solver.path
    
    if (params.solveur=="coin"):
        if (params.logSolveur=="on"):
          
            model.lp.setSolver(solvers.PULP_CBC_CMD(msg=0,fracGap=params.solveurToleranceRelative,maxSeconds=params.solveurMaxTime,keepFiles=1))
            
        else:
            model.lp.setSolver(solvers.PULP_CBC_CMD(msg=0,fracGap=params.solveurToleranceRelative,maxSeconds=params.solveurMaxTime,keepFiles=1))
    else:
        path=params.pathCplex 
        options=[" set mip tol mipgap  "+str(params.solveurToleranceRelative)]
        options+=[" set timelimit "+str(params.solveurMaxTime)+"\n"]
        if (params.logSolveur=="on"):
            model.lp.setSolver(solvers.CPLEX_CMD(path,msg=1,keepFiles=1,options=options))
        else:
            model.lp.setSolver(solvers.CPLEX_CMD(path,msg=0,keepFiles=1,options=options))
    solutionTime =- time.time()
    model.lp.solve()
    solutionTime+=time.time()
    
    model.lp.writeLP(name+".lp")
    model.indicators["solutionTime"]=solutionTime
    getIndicators(model)

def getIndicators(model):

    model.indicators["lpStatus"]=pulp.LpStatus[model.lp.status]
    model.indicators["objective function"]=pulp.value(model.lp.objective) 
    print (model.indicators)


def getAllVariables(model,name):
     sortedKeys=["variable name","variable value","lower bound","upper bound"]
     resultsVariable={}
     for key in sortedKeys:
         resultsVariable[key]=[]
     file=open("variable_results.csv","w")
     for v in model.lp.variables():
         resultsVariable["variable value"].append(v.value())
         resultsVariable["variable name"].append(v.name)
         resultsVariable["lower bound"].append(v.lowBound)
         resultsVariable["upper bound"].append(v.upBound)
         file.write(v.name+"\t"+str(v.value())+"\t"+str(v.lowBound)+"\t"+str(v.upBound)+"\n")  
     file.close()
        
     name_table="variables"
     charts.displayResultTable(sortedKeys,resultsVariable,name_table)



def getAllConstraints(model,name):
     sortedKeys=["constraint name","slack","pi","rhs"]
     resultsConstraints={}
     for key in sortedKeys:
         resultsConstraints[key]=[]
     fic=open("contraints_results.csv","w")
     for k,c in model.lp.constraints.items():
         resultsConstraints["constraint name"].append(c.name)
         resultsConstraints["slack"].append(c.slack)
         resultsConstraints["pi"].append(c.pi)
         resultsConstraints["rhs"].append(-c.constant)
         fic.write(c.name+"\t"+str(c.value())+"\t"+str(c.slack)+"\t"+str(-c.constant)+"\n")
     fic.close()
     name_table="constraints"
     charts.displayResultTable(sortedKeys,resultsConstraints,name_table)

def getAllDualVariables(model):
    dual_variables={}
    for k,c in model.lp.constraints.items():
        dual_variables[c.name]=c.pi
    return dual_variables
    
