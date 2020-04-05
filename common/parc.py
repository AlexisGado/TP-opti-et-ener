from common import commentjson
from pprint import pprint



class TimeStep:
    def __init__(self, id, start_date, end_date):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date

class ProductionLevel:
    def __init__(self, power):
        self.power = power
    def __repr__(self):
        return str(self.power) + "MW"
    def __lt__(self, other):
        return self.power < other.power

class MandatoryShutdown:
    def __init__(self,  data):
        self.start_date = data["start_date"] #mn
        self.end_date = data["end_date"] #mn
        
class Valley:
    def __init__(self,id,data,hydro_plants,reservoirs,steps):
        self.id=id
        self.reservoirs=[]
        self.steps=[]
        self.hydro_plants=[]
        for usine_id in data["hydroplants_ids"]:
            self.hydro_plants.append(hydro_plants[usine_id])
        
        for reservoir_id in data["reservoirs_ids"]:
            self.reservoirs.append(reservoirs[reservoir_id])
            
        for step in steps:
            if step.id_turb in data["hydroplants_ids"] and step.id_pump in data["hydroplants_ids"]:
                self.steps.append(step)
            elif step.id_turb not in data["hydroplants_ids"] and step.id_pump not in data["hydroplants_ids"]:
                pass
            else:
                print( "error with valley "+str(id)+" and turbine "+str(step.id_turb)+" and pump "+str(step.id_pump))

class ThermalPlant:
    def __init__(self, id, data,time_step_duration):
        self.id = id
        self.name = data["name"]
        self.offline_production_level = ProductionLevel( 0)
        self.production_levels = [ ProductionLevel(power)  for power in data["production_levels"] ]
        self.proportionnal_cost = data["proportionnal_cost"]#euro/MWh
        self.quadratic_cost = data.get( "quadratic_cost", 0)#euro/MWh/MWh
        self.startup_cost = data.get("startup_cost", 0)#euro
        self.gradient = data.get("gradient",1000)
        self.initP = data.get("initP",0)
        self.maximum_increase_rate = data.get("maximum_increase_rate", None)#MW/mn
        self.maximum_decrease_rate = data.get("maximum_decrease_rate", None)#MW/mn
        self.minimum_online_duration = data.get("minimum_online_duration", 0)#mn
        self.maximum_number_of_startups = data.get("maximum_number_of_startups", None)#0,1,2...

        self.mandatory_shutdowns = [ MandatoryShutdown( d)
                                for d in data.get("mandatory_shutdowns", [] ) ]
        
        self.time_step_duration=time_step_duration



    def pmax(self, time_step):
        date=self.time_step_duration*time_step
        for shutdown in self.mandatory_shutdowns :
            if (shutdown.start_date <= date
                and date < shutdown.end_date) :
                return 0

        return max( [ prod_level.power for prod_level in self.production_levels] )

    def pmin(self, time_step):
        return min( [ prod_level.power for prod_level in self.production_levels] )


class Reservoir:
    def __init__(self, id, data) :
        self.id = id
        self.initial_volume = data["initial_volume"] #m3
        self.inflows = data["inflows"]#m3/s
        self.maximum_volume = data["maximum_volume"]#m3
        self.minimum_volume = data["minimum_volume"]#m3
        self.water_value = data.get("water_value", None)#euros/m3
        self.downstream_hydro_plants_ids=data["downstream_hydroplants_ids"]#0,1,2...
        self.upstream_hydro_plants_ids=data["upstream_hydroplants_ids"]#0,1,2...
        

class HydroOperatingLevel:
    def __init__(self, id, data):
        self.id = id
        self.power = data["power"]#MW
        self.flow = data["flow"]#m3/s

class HydroPlant:
    def __init__(self, id, data):
        self.id = id
        if(len(str(id))==1):
            self.name="hyd_0"+str(id)
        else:
            self.name="hyd_"+str(id)
        self.downstream_delay =  data.get( "downstream_delay", None)
        self.maximum_increase_rate = data["maximum_increase_rate"]#m3/s/mn
        self.maximum_decrease_rate = data["maximum_decrease_rate"]#m3/s/mn
        self.operating_levels = [ HydroOperatingLevel(i, d) for i,d in enumerate(data["operating_levels"])]



class Step:
    def __init__(self, id, data):
        self.id = id
        self.id_turb = data.get("id_turb")
        self.id_pump =data.get("id_pump")


class UnitCommitmentProblem:
    def __init__(self, data):

        self.number_of_time_steps= data["number_of_time_steps"]#0,1,2...
        self.time_step_duration= data["time_step_duration"]#mn
        self.time_steps = range(self.number_of_time_steps)

        self.thermal_plants = [ThermalPlant(i, d,data["time_step_duration"]) for i, d in enumerate(data.get("thermal_plants", [] ))]
        self.reservoirs = [Reservoir(i, d) for i,d in enumerate(data.get("reservoirs", []))]
        self.hydro_plants= [HydroPlant(i, d) for i,d in enumerate(data.get("hydro_powerplants", []))]
        self.steps=[Step(i, d) for i,d in enumerate(data.get("steps", []))]
        self.valleys=[Valley(i,d,self.hydro_plants,self.reservoirs,self.steps) for i,d in enumerate(data.get("valleys", []))]

        self.demand = data.get("demand", [ 0. for t in self.time_steps]) #MW
        self.wind = data.get("wind", [ 0. for t in self.time_steps]) #MW

        self.maximum_over_production = data.get("maximum_over_production", None)#MW
        self.maximum_under_production = data.get( "maximum_under_production", None)#MW
        self.over_production_penalty = data.get( "over_production_penalty", None)#euros/MWh
        self.under_production_penalty = data.get( "under_production_penalty", None)#euros/MWh
        
        self.electricity_prices = data.get("electricity_prices",  [0. for t in self.time_steps])#euros/MWh

        
        if len(self.demand) < self.number_of_time_steps :
            print("Demand vector is shorter than the number of time steps : ",
                                                                           len(self.demand)," values for ",
                                                                              self.number_of_time_steps, " time steps.")
            last_val = self.demand[-1]
            print("Missing time steps filled with the last provided value of ", last_val, " MW.")
            self.demand += [ last_val for t in range( self.number_of_time_steps - len(self.demand))]


        if len(self.electricity_prices) < self.number_of_time_steps :
            print("Electricity prices vector is shorter than the number of time steps : ",
                                                                           len(self.electricity_prices)," values for ",
                                                                              self.number_of_time_steps, " time steps.")
            last_val = self.electricity_prices[-1]
            print("Missing time steps filled the last provided value of ", last_val, " euros")
            self.electricity_prices+= [ last_val for t in range( self.number_of_time_steps - len(self.electricity_prices))]

    def start_date(self, time_step) :
        return time_step * self.time_step_duration

    def end_date(self, time_step) :
        return (time_step + 1) * self.time_step_duration

    def time_step_to_string(self, time_step):
        start_date = self.start_date(time_step)
        hours = int( start_date/60)
        minutes = int( start_date % 60)
        if(hours <=24):
            return str(hours) + "h" + str("{:02}").format(minutes)
        days = int(hours/24)
        hours_in_last_day = int( hours % 24)
        return ( str(days) + "d" + str("{:02}h").format(hours_in_last_day)
                        + str("{:02}").format(minutes) )

def test():
    with open('data.json') as data_file:
        data = commentjson.load(data_file)

    pb = UnitCommitmentProblem(data)

    return pb

def build_from_data(name="data"):
    print( "Reading data from file : ", name)
    with open(name) as data_file:
        data = commentjson.load(data_file)
    pb = UnitCommitmentProblem(data)
    return pb
