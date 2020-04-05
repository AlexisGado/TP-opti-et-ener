import sys
import os
import pulp

sys.path.append(os.getcwd()+'/../../')
from common import parc
from linear_prog.pulp_utils import *
import common.charts



def create_thermal_plant_lp( pb,name):

    lp = pulp.LpProblem(name+".lp", pulp.LpMinimize)
    lp.setSolver()
    prod_vars = {}
    volume_res ={}
    status_vars = {}

    for t in pb.time_steps:
        prod_vars[t] = {}
        volume_res[t] ={}
        status_vars[t] = {}
        
        for thermal_plant in pb.thermal_plants :
            
            
            #Vars
            
            var_name_prod = "prod_"+str(t)+"_"+str(thermal_plant.name)
            prod_vars[t][thermal_plant] = pulp.LpVariable(var_name_prod, 0, thermal_plant.pmax(t))
            
            var_name_status = "status_"+str(t)+"_"+str(thermal_plant.name) # centrale allumee ou eteinte
            status_vars[t][thermal_plant] = pulp.LpVariable(var_name_status, cat="Binary")
            
        
            
            #Constraints
            
            
            # productions min et max si la centrale est allumee (status == 1)
            constraint_name_min = "minimum_production"+ str(t)+"_"+thermal_plant.name
            lp+=prod_vars[t][thermal_plant] >= thermal_plant.pmin(t)*status_vars[t][thermal_plant],constraint_name_min
            
            constraint_name_max = "maximum_production"+ str(t)+"_"+thermal_plant.name
            lp+=prod_vars[t][thermal_plant] <= thermal_plant.pmax(t)*status_vars[t][thermal_plant],constraint_name_max
            
            
            # arrets prevus
            for m in thermal_plant.mandatory_shutdowns:
                if m.start_date<=t*pb.time_step_duration<m.end_date:
                    constraint_name_shut = "shutdown_t_"+str(t)+"_"+thermal_plant.name
                    lp+=status_vars[t][thermal_plant]==0,constraint_name_shut
            
            
        for reservoir in pb.reservoirs :
            var_name="reservoir_"+str(t)+"_"+str(reservoir.id)
            volume_res[t][reservoir]=pulp.LpVariable(var_name,None,None)
            
        for hydro_plant in pb.hydro_plants :
            var_name ="prod_"+str(t)+"_"+str(hydro_plant.name)
            prod_vars[t][hydro_plant]=pulp.LpVariable(var_name,0.0,hydro_plant.operating_levels[0].power)
        for reservoir in pb.reservoirs:
            hydro_plants_down=[pb.hydro_plants[id] for id in reservoir.downstream_hydro_plants_ids]
            const_name="maj_stock"+str(t)
            rendement=hydro_plant.operating_levels[0].flow/hydro_plant.operating_levels[0].power
            if t>0:
               lp+=volume_res[t][reservoir]==volume_res[t-1][reservoir]-rendement*pb.time_step_duration*60*pulp.lpSum(([prod_vars[t][hydro_plant] for hydro_plant in hydro_plants_down])),const_name
            else :
               lp+=volume_res[t][reservoir]==reservoir.initial_volume-rendement*pb.time_step_duration*60*pulp.lpSum(([prod_vars[t][hydro_plant] for hydro_plant in hydro_plants_down])),const_name
            
            #min/max reservoirs 
            constraint_name_min = "minimum_stock"+ str(t)+"_"+str(reservoir.id)
            lp+=volume_res[t][reservoir] >= reservoir.minimum_volume,constraint_name_min
            
            constraint_name_max = "maximum_stock"+ str(t)+"_"+str(reservoir.id)
            lp+=volume_res[t][reservoir] <= reservoir.maximum_volume,constraint_name_max

        constraint_name = "balance_"+ str(t)
        lp +=  pulp.lpSum([ prod_vars[t][plant] for plant in pb.hydro_plants+pb.thermal_plants ]) == pb.demand[t], constraint_name
        

    lp.setObjective(pulp.lpSum([ 2*plant.proportionnal_cost*prod_vars[t][plant] for plant in pb.thermal_plants for t in pb.time_steps ]))

    model=Model(lp,prod_vars,volume_res)

    return model



def run():
    pb_name = "data/question8"
    pb = parc.build_from_data(pb_name+".json")

    print ("Creating Model " + pb_name)
    model = create_thermal_plant_lp(pb, pb_name)
  
    print ("Solving Model")
    solve(model, pb_name)
   
    print ("Post Treatment")
    

    results=getResultsModel(pb,model,pb_name)
    printResults(pb, model, pb_name,[],results)

if __name__ == '__main__':
    run()

