#from bokeh.charts import  Step, show, output_file, defaults
from bokeh.layouts import row,widgetbox, column
from bokeh.plotting import figure, ColumnDataSource
from os.path import join,dirname
from bokeh.models import CustomJS
from bokeh.models.widgets import DataTable,  TableColumn, Button
from bokeh.io import save
from bokeh.io import output_file, show,output_notebook, push_notebook
import bokeh.palettes
from bokeh.palettes import brewer
from bokeh.models import HoverTool, Legend
import os, math
from bokeh.embed import file_html


def isnotebook():
    try:
        ipy_str = str(type(get_ipython()))
        if 'zmqshell' in ipy_str:
            return 'jupyter'
        if 'terminal' in ipy_str:
            return 'ipython'
    except:
        return 'terminal'

def save_plot(plot, plot_title = "", html_filename="plot"):
    output_file(html_filename+".html",  mode="inline", title=plot_title)
    save(plot)
    path = os.path.join( os.getcwd(), html_filename+".html")
    print("Plot file "+path+" saved.")
    
    



def plot_programs(programs, pb, plot_title = "Programs"):
    defaults.height=400
    defaults.width = 800


    p = plot_lines(programs, pb.time_step_to_string)
    p.title.text = plot_title
    return p


def plot_stock_management(pb, program, bellman_values, plot_title="Dynamic Programming"):
    defaults.height=400
    defaults.width = 800
    programs = {"stock": program[:pb.number_of_days]}
    progs = plot_lines(programs, lambda i : str(i), ylabel = "production days left")
    prices = plot_lines ( { "base prices" : pb.base_prices[:pb.number_of_days]},  #, "peak" : pb.peak_prices[:pb.number_of_days]},
                         lambda i : str(i),
                         ylabel="euros/MWh")
    prices.title.text = "Prices"


    states = sorted(bellman_values.keys())

    bellman_data = {str(t) : [ bellman_values[state][t] for state in states] for t in range(pb.number_of_days)}
    bellman_data["row_headers"] = [str(state) for state in states ]



    bellman_source =   ColumnDataSource(bellman_data)
    bellman_columns = [ TableColumn(field = "row_headers", title="States")]
    bellman_columns += [
                TableColumn(field =str(t), title= str(t)) for t in range(pb.number_of_days)
            ]



    bellman_table = DataTable(source = bellman_source, columns = bellman_columns,
                              row_headers = False,
                              fit_columns = True,
                              height = defaults.height,
                              width =defaults.width)

    indicators = ["number_of_days", "initial_stock","power", "peak_duration", "base_duration", "stock_consumption"]

    data = dict(
       indicator=[indicator for indicator in indicators],
       value=[pb.__dict__[indicator] for indicator in indicators ]
    )


    source = ColumnDataSource(data)

    columns = [
       TableColumn(field="indicator", title="indicator"),
       TableColumn(field="value", title="value"),
    ]
    area3 = DataTable(source=source, columns=columns, width=400, height=280)

    return row(column(progs, prices, bellman_table), area3)

def plot_dynamic_programming(thermal_plant, program, bellman_values, pb, plot_title="Dynamic Programming"):
    defaults.height=200
    defaults.width = 800
    programs = {thermal_plant.name : program}
    progs = plot_programs(programs, pb)
    prices = plot_lines ( { "prices" : pb.electricity_prices},
                         pb.time_step_to_string,
                         ylabel="euros/MWh")
    prices.title.text = "Electricity prices"

    #bellman_vals = plot_lines(bellman_values, pb.time_step_to_string, ylabel="euros")
    #bellman_vals.title.text = "Bellman Values"

    states = sorted(bellman_values.keys())

    bellman_data = {pb.time_step_to_string(t) : [ bellman_values[state][t] for state in states] for t in pb.time_steps}
    bellman_data["row_headers"] = [str(state) for state in states ]



    bellman_source =   ColumnDataSource(bellman_data)
    bellman_columns = [ TableColumn(field = "row_headers", title="States")]
    bellman_columns += [
                TableColumn(field =pb.time_step_to_string(t), title= pb.time_step_to_string(t)) for t in pb.time_steps
            ]



    bellman_table = DataTable(source = bellman_source, columns = bellman_columns,
                              row_headers = False,
                              fit_columns = True,
                              height = defaults.height,
                              width =defaults.width)

    indicators = ["production_levels", "proportionnal_cost", "startup_cost", "quadratic_cost"
                  , "maximum_increase_rate", "maximum_decrease_rate", "minimum_online_duration", "maximum_number_of_startups"]

    data = dict(
        indicator=[indicator for indicator in indicators],
        value=[str(thermal_plant.__dict__[indicator]) for indicator in indicators ]
    )


    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="indicator", title="indicator"),
        TableColumn(field="value", title="value"),
    ]
    area3 = DataTable(source=source, columns=columns, width=400, height=280)

    return row(column(progs, prices, bellman_table), area3)

def plot_programs_and_prices(programs, pb, plot_title=""):
  #  defaults.height=400
  #  defaults.width = 800
    progs = plot_programs(programs, pb)
    prices = plot_lines ( { "prices" : pb.electricity_prices},
                         pb.time_step_to_string,
                         ylabel="euros/MWh")
    return column(progs, prices)

def display_EOD(programs, pb, indicators, name, demand,electricity_prices=[],printIndicators=True):

   # defaults.height=400
   # defaults.width = 400
    demand = pb.demand
    print(isnotebook())
    
    areas=[]
    
    def time_step_hour (i) :
        return pb.time_step_to_string(i)

    
    area1 = plot_lines(programs,  time_step_hour)
    area1.title.text = "Production plans"
    areas.append(area1)

    area2 = stack_lines(programs,  time_step_hour)
    area2.title.text = "Cumulative production"
    
    area2.line([i+1.5 for i in range(len(demand))],demand,line_width=2,line_color="black",legend_label="Demand")
    areas.append(area2)
    
    if printIndicators==True:
        data = dict(
                    indicator=[indicator for indicator in indicators],
                    value=[indicators[indicator] for indicator in indicators ]
                    )
        source = ColumnDataSource(data)

        columns = [
                   TableColumn(field="indicator", title="indicator"),
                   TableColumn(field="value", title="value"),
                   ]
        area3 = DataTable(source=source, columns=columns, width=400, height=280)
        areas.append(area3)
    
    if(len(electricity_prices)>0):
        area4 = plot_lines({"price":electricity_prices},  time_step_hour,ylabel="euros/MWh")
        area4.title.text = "Electricity_price"
        areas.append(area4)

    output_file("global_programs.html", title=name, mode="inline")
    

    handle=show(row(areas))
    push_notebook(handle=handle)
#    save(row(areas))
    
def display_programms(programs, pb):

#    defaults.height=400
 #   defaults.width = 400
   
    
    def time_step_hour (i) :
        return pb.time_step_to_string(i)
    
    areas=[]
    for program in sorted(programs.keys()):
        dico_program={program:programs[program]}
        area=plot_lines(dico_program,  time_step_hour)
        area.title.text = program
        areas.append(area)
    
    #areas=plot_lines(programs,  time_step_hour)
    
    output_file("detailed_programs.html", title="detailed programs", mode="inline")
    save(column(areas))
 
def display_programms_with_bounds(programs,programs_min,programs_max, pb,unite=""):

#    defaults.height=400
 #   defaults.width = 400
   
    
    def time_step_hour (i) :
        return pb.time_step_to_string(i)
    
    areas=[]
    for program in sorted(programs.keys()):
        dico_program={program:programs[program],"minimum":programs_min[program],"maximum":programs_max[program]}
        area=plot_lines(dico_program,  time_step_hour,ylabel=unite)
        area.title.text = program
        areas.append(area)
    
    #areas=plot_lines(programs,  time_step_hour)
    
    output_file("reservoir_results.html", title="reservoir_results", mode="inline")
    
    save(column(areas))      

def plot_lines(datas_, index_to_string, ylabel = "MW"):
    datas = { str(key).replace(" ", "_") : value for  key, value in  datas_.items()}
    keys = sorted(datas.keys())
    nb_max_values = max([ len(datas[key]) for key in  keys])
    indices = range(nb_max_values)

    palette = bokeh.palettes.viridis(len(keys))
    colors = {key : palette[i] for i,key in enumerate(keys)}

    xrange = [index_to_string(i) for i in range(nb_max_values+1)]


    columns = {}
    for key in keys :
        columns[key]  = [ datas[key][i] for i in indices ]




    lines = {}
    lines["time"] = []
    for i in indices:
        lines["time"]+= [index_to_string(i), index_to_string(i+1)]
    for key in keys:
        lines[key] = []
        for i in indices :
            v = datas[key][i]
            lines[key] += [v, v]

    ds = ColumnDataSource(lines)

    #print(xrange)

    p=figure(x_range = xrange
                 , height = 400,
                 width = 400
             )


    legend_items={}
    lines = []
    for key in keys:
        line = p.line( "time", key,
                color = colors[key],
                source = ds,
                line_width = 4,
                alpha = 0.7
                )
        legend_items[key] = [line]
        lines += [line]


    legend = Legend(
            items=[ (key, legend_items[key])
                    for key in sorted(legend_items.keys()) ]
            , location=(0, 0)
            , orientation="horizontal"
            )
    p.add_layout(legend, "below")

    p.yaxis.axis_label = ylabel

    #if there is two many lines, we do not put the hover tool
    if len(keys) > 20:
        return p


    columns = {}
    for key in keys :
        columns[key]  = [ datas[key][i] for i in indices ]


    hover_ds = ColumnDataSource(columns)
    hover_ds.add([index_to_string(i) for i in range(nb_max_values)], "time")
    hover_ds.add([index_to_string(i) for i in range(nb_max_values)], "left")
    hover_ds.add([index_to_string(i+1) for i in range(nb_max_values)], "right")

    max_val = -math.inf
    min_val = math.inf
    for key in keys :
        for i in indices :
            v = datas[key][i]
            if math.isfinite(v):
                max_val = max(max_val, v)
                min_val = min(min_val, v)

    hover_ds.add([max_val for i in range(nb_max_values)], "top")
    hover_ds.add([min_val for i in range(nb_max_values)], "bottom")



    hover_glyphs = []
    #for key in keys:
    glyph = p.quad(top="top", bottom="bottom",
                   left="left", right="right",
                   alpha = 0,
                   source = hover_ds,
                   color = "white",
                   hover_alpha=0.1,
                   hover_color = "black")
    hover_glyphs += [glyph]

    hover = HoverTool(
            tooltips = [("time", "@time")]
                          + [ (key, "@"+key + " " + ylabel ) for key in keys ]
           , attachment="horizontal"
           #, mode = "vline"
           , renderers = hover_glyphs
    )
    p.add_tools(hover)





    return p

def stack_lines(datas,  index_to_string, ylabel = "MW"):
    keys = sorted(datas.keys())
    nb_max_values = max([ len(datas[key]) for key in keys])
    indices = range(nb_max_values)
    #palette= brewer["Spectral"][nb_max_values]
    palette = bokeh.palettes.viridis(len(keys))
    colors = {key : palette[i] for i,key in enumerate(keys)}

    xrange = [index_to_string(i) for i in range(nb_max_values+1)]
    lines = {}

    columns = {}
    for key in keys :
        columns[key]  = [ datas[key][i] for i in indices ]

    ds = ColumnDataSource(columns)
    ds.add([index_to_string(i) for i in range(nb_max_values)], "left")
    ds.add([index_to_string(i+1) for i in range(nb_max_values)], "right")




    p=figure(x_range = xrange,
                 height = 400,
                 width = 400
             )


    #print(ds.data)
    partial_sum = [ 0. for i in range(nb_max_values)]
    legend_items={}
    for key in keys:
        ds.add( partial_sum , "bottom"+str(key))
        ds.add([ partial_sum[i] + datas[key][i] for i in range(nb_max_values)], "top"+str(key))


        quad = p.quad(
                top = "top"+str(key) ,
                bottom = "bottom"+str(key),
                left = "left",
                right = "right",
                color = colors[key],
                source = ds,
                fill_alpha = 0.7,
                hover_fill_alpha = 0.99,
                hover_fill_color=colors[key],
                hover_line_color=colors[key],
                )
        legend_items[key] = [quad]
        partial_sum = ds.data["top"+str(key)]


    legend = Legend(items=[
            (key, legend_items[key])
            for key in legend_items.keys()
], location=(0, 0), orientation="horizontal")
    p.add_layout(legend, "below")

    p.yaxis.axis_label = ylabel

    #if there is two many lines, we do not put the hover tool
    if len(keys) > 10:
        return p

    hover = HoverTool(
        tooltips=
       [("time", "@left")]
        + [ (key, "@"+key+ " "+ylabel) for key in keys]
        , attachment="horizontal"
        , show_arrow=True


    )
    p.add_tools(hover)



    return p



def displayResultTable(sortedKeys, dictionnary, name):
    
    #display a table in
    source = ColumnDataSource(dictionnary)

    columns = [
        TableColumn(field=key, title=key)
        for key in sortedKeys
    ]

    area = DataTable(source=source, columns=columns, width=600, height=800)
    button = Button(label="Download", button_type="success")
   # button.callback = CustomJS(args=dict(source=source),
    #                       code=open(join(dirname(__file__), "download.js")).read())

    controls=widgetbox(button)

    output_file(name+".html", title=name)

    save(row(area,controls))




