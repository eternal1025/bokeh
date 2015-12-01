from bokeh.io import vform
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import Figure, output_file, show

output_file("callback.html")

x = [x*0.005 for x in range(0, 200)]
y = x

source = ColumnDataSource(data=dict(x=x, y=y))

plot = Figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

def callback(source=source):
    data = source.get('data')
    f = cb_obj.get('value')
    x, y = data['x'], data['y']
    for i in range(len(x)):
        y[i] = Math.pow(x[i], f)
    source.trigger('change');

slider = Slider(start=0.1, end=4, value=1, step=.1, title="power", 
                callback=CustomJS.from_py_func(callback))

layout = vform(slider, plot)

show(layout)