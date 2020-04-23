# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 01:06:03 2020

@author: C33354
"""

import sys
import os
import pulp
import bokeh
#import bkcharts
print (bokeh.__version__)



import common.parc as parc
from linear_prog.pulp_utils import *

def create_thermal_plant_lp( pb,name):



    lp = pulp.LpProblem(name+".lp", pulp.LpMinimize)
    lp.setSolver()
    prod_vars = {}
    status_vars = {}
    switch_vars = {}

    for t in pb.time_steps:
        prod_vars[t] = {}
        status_vars[t] = {}
        switch_vars[t] = {}
        
        for thermal_plant in pb.thermal_plants :
            
            #Vars
            
            var_name_prod = "prod_"+str(t)+"_"+str(thermal_plant.name)
            prod_vars[t][thermal_plant] = pulp.LpVariable(var_name_prod, 0, thermal_plant.pmax(t))
            
            var_name_status = "status_"+str(t)+"_"+str(thermal_plant.name) # centrale allumee ou eteinte
            status_vars[t][thermal_plant] = pulp.LpVariable(var_name_status, cat="Binary")
            
            var_name_switch = "switch_"+str(t)+"_"+str(thermal_plant.name) # changement d'état de la centrale
            switch_vars[t][thermal_plant] = pulp.LpVariable(var_name_switch, cat="Binary")
        
            
            #Constraints
            
            
            # productions min et max si la centrale est allumee (status == 1)
            constraint_name_min = "minimimum_production"+ str(t)+"_"+thermal_plant.name
            lp+=prod_vars[t][thermal_plant] >= thermal_plant.pmin(t)*status_vars[t][thermal_plant],constraint_name_min
            
            constraint_name_max = "maximum_production"+ str(t)+"_"+thermal_plant.name
            lp+=prod_vars[t][thermal_plant] <= thermal_plant.pmax(t)*status_vars[t][thermal_plant],constraint_name_max
            
            
            # arrets prevus
            for m in thermal_plant.mandatory_shutdowns:
                if m.start_date<=t*pb.time_step_duration<m.end_date:
                    constraint_name_shut = "shutdown_t_"+str(t)+"_"+thermal_plant.name
                    lp+=status_vars[t][thermal_plant]==0,constraint_name_shut
            
            
            # detection du demarrage avec les variables switch
            if t == pb.time_steps[0]:
                #centrale eteinte avant t==0
                lp += switch_vars[t][thermal_plant] == status_vars[t][thermal_plant],"and_1_"+str(t)+"_"+thermal_plant.name
            else:
                lp += switch_vars[t][thermal_plant] >= status_vars[t][thermal_plant] - status_vars[t-1][thermal_plant],"and_2_"+str(t)+"_"+thermal_plant.name
                lp += switch_vars[t][thermal_plant] <= 1 - status_vars[t-1][thermal_plant],"and_3_"+str(t)+"_"+thermal_plant.name
                lp += switch_vars[t][thermal_plant] <= status_vars[t][thermal_plant],"and_4_"+str(t)+"_"+thermal_plant.name
                
            
        # equilibre a tout t
        constraint_name_eq="equilibre_"+str(t)
        lp+=pulp.lpSum([prod_vars[t][thermal_plant] for thermal_plant in pb.thermal_plants ])==pb.demand[t],constraint_name_eq
    
    
    
    # duree minimum de fonctionnement
    for t in pb.time_steps:
        for thermal_plant in pb.thermal_plants :            
            for tp in range(t,t+int(thermal_plant.minimum_online_duration/pb.time_step_duration)):
                if tp<pb.number_of_time_steps:
                    constraint_name_dur = "dur_"+ str(t)+"_"+str(tp)+"_"+thermal_plant.name
                    lp+=switch_vars[t][thermal_plant]<=status_vars[tp][thermal_plant],constraint_name_dur
            
    
    
    
    
    
    #Objective
    
    lp.setObjective( pulp.lpSum([
    2*thermal_plant.proportionnal_cost* prod_vars[t][thermal_plant] 
    + switch_vars[t][thermal_plant]*thermal_plant.startup_cost
    for thermal_plant in pb.thermal_plants for t in pb.time_steps]))

    model=Model(lp,prod_vars)

    return model





def run():
    pb_name = "data/question1"
    pb = parc.build_from_data(pb_name+".json")
    

    print ("Creating Model " + pb_name)
    model = create_thermal_plant_lp(pb, pb_name)
  
    print ("Solving Model")
    solve(model, pb_name)
   
    print ("Post Treatment")
    

    results=getResultsModel(pb,model,pb_name)
    printResults(pb, model, pb_name,[],results)

    print("execution terminee")
    return
    
   
run()
