
```python
#################################################################################################################################
################################################ MILESTONE PROJECT - PART 1 ######################################################

#1. Create Pandas dataframes
#2. Manipulate data (indexing, selection, variable dtypes)conca

#3. Plot data (Matplotlib, Bokeh)

```


```python
#Load all libraries that will be used in this project

%matplotlib inline
import matplotlib
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144
```


```python
import pandas as pd
import json
from io import StringIO
import io
import csv
import sys
import datetime
```


```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
```


```python
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Spectral6
from bokeh.resources import CDN
from bokeh.embed import file_html
from ipywidgets import *
```


```python
from matplotlib import cm
import holoviews as hv
hv.extension('bokeh', 'matplotlib')
```





<script src="https://code.jquery.com/ui/1.10.4/jquery-ui.min.js" type="text/javascript"></script>
<script type="text/javascript">function HoloViewsWidget(){
}

HoloViewsWidget.comms = {};
HoloViewsWidget.comm_state = {};

HoloViewsWidget.prototype.init_slider = function(init_val){
  if(this.load_json) {
    this.from_json()
  } else {
    this.update_cache();
  }
}

HoloViewsWidget.prototype.populate_cache = function(idx){
  this.cache[idx].html(this.frames[idx]);
  if (this.embed) {
    delete this.frames[idx];
  }
}

HoloViewsWidget.prototype.process_error = function(msg){

}

HoloViewsWidget.prototype.from_json = function() {
  var data_url = this.json_path + this.id + '.json';
  $.getJSON(data_url, $.proxy(function(json_data) {
    this.frames = json_data;
    this.update_cache();
    this.update(0);
  }, this));
}

HoloViewsWidget.prototype.dynamic_update = function(current){
  if (current === undefined) {
    return
  }
  if(this.dynamic) {
    current = JSON.stringify(current);
  }
  function callback(initialized, msg){
    /* This callback receives data from Python as a string
       in order to parse it correctly quotes are sliced off*/
    if (msg.content.ename != undefined) {
      this.process_error(msg);
    }
    if (msg.msg_type != "execute_result") {
      console.log("Warning: HoloViews callback returned unexpected data for key: (", current, ") with the following content:", msg.content)
    } else {
      if (msg.content.data['text/plain'].includes('Complete')) {
        if (this.queue.length > 0) {
          this.time = Date.now();
          this.dynamic_update(this.queue[this.queue.length-1]);
          this.queue = [];
        } else {
          this.wait = false;
        }
        return
      }
    }
  }
  this.current = current;
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null)) {
    var kernel = Jupyter.notebook.kernel;
    callbacks = {iopub: {output: $.proxy(callback, this, this.initialized)}};
    var cmd = "holoviews.plotting.widgets.NdWidget.widgets['" + this.id + "'].update(" + current + ")";
    kernel.execute("import holoviews;" + cmd, callbacks, {silent : false});
  }
}

HoloViewsWidget.prototype.update_cache = function(force){
  var frame_len = Object.keys(this.frames).length;
  for (var i=0; i<frame_len; i++) {
    if(!this.load_json || this.dynamic)  {
      frame = Object.keys(this.frames)[i];
    } else {
      frame = i;
    }
    if(!(frame in this.cache) || force) {
      if ((frame in this.cache) && force) { this.cache[frame].remove() }
      this.cache[frame] = $('<div />').appendTo("#"+"_anim_img"+this.id).hide();
      var cache_id = "_anim_img"+this.id+"_"+frame;
      this.cache[frame].attr("id", cache_id);
      this.populate_cache(frame);
    }
  }
}

HoloViewsWidget.prototype.update = function(current){
  if(current in this.cache) {
    $.each(this.cache, function(index, value) {
      value.hide();
    });
    this.cache[current].show();
    this.wait = false;
  }
}

HoloViewsWidget.prototype.init_comms = function() {
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel !== undefined)) {
    var widget = this;
    comm_manager = Jupyter.notebook.kernel.comm_manager;
    comm_manager.register_target(this.id, function (comm) {
      comm.on_msg(function (msg) { widget.process_msg(msg) });
    });
  }
}

HoloViewsWidget.prototype.process_msg = function(msg) {
}

function SelectionWidget(frames, id, slider_ids, keyMap, dim_vals, notFound, load_json, mode, cached, json_path, dynamic){
  this.frames = frames;
  this.id = id;
  this.slider_ids = slider_ids;
  this.keyMap = keyMap
  this.current_frame = 0;
  this.current_vals = dim_vals;
  this.load_json = load_json;
  this.mode = mode;
  this.notFound = notFound;
  this.cached = cached;
  this.dynamic = dynamic;
  this.cache = {};
  this.json_path = json_path;
  this.init_slider(this.current_vals[0]);
  this.queue = [];
  this.wait = false;
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

SelectionWidget.prototype = new HoloViewsWidget;


SelectionWidget.prototype.get_key = function(current_vals) {
  var key = "(";
  for (var i=0; i<this.slider_ids.length; i++)
  {
    val = this.current_vals[i];
    if (!(typeof val === 'string')) {
      if (val % 1 === 0) { val = val.toFixed(1); }
      else { val = val.toFixed(10); val = val.slice(0, val.length-1);}
    }
    key += "'" + val + "'";
    if(i != this.slider_ids.length-1) { key += ', ';}
    else if(this.slider_ids.length == 1) { key += ',';}
  }
  key += ")";
  return this.keyMap[key];
}

SelectionWidget.prototype.set_frame = function(dim_val, dim_idx){
  this.current_vals[dim_idx] = dim_val;
  var key = this.current_vals;
  if (!this.dynamic) {
    key = this.get_key(key)
  }
  if (this.dynamic || !this.cached) {
    if ((this.time !== undefined) && ((this.wait) && ((this.time + 10000) > Date.now()))) {
      this.queue.push(key);
      return
    }
    this.queue = [];
    this.time = Date.now();
    this.current_frame = key;
    this.wait = true;
    this.dynamic_update(key)
  } else if (key !== undefined) {
    this.update(key)
  }
}


/* Define the ScrubberWidget class */
function ScrubberWidget(frames, num_frames, id, interval, load_json, mode, cached, json_path, dynamic){
  this.slider_id = "_anim_slider" + id;
  this.loop_select_id = "_anim_loop_select" + id;
  this.id = id;
  this.interval = interval;
  this.current_frame = 0;
  this.direction = 0;
  this.dynamic = dynamic;
  this.timer = null;
  this.load_json = load_json;
  this.mode = mode;
  this.cached = cached;
  this.frames = frames;
  this.cache = {};
  this.length = num_frames;
  this.json_path = json_path;
  document.getElementById(this.slider_id).max = this.length - 1;
  this.init_slider(0);
  this.wait = false;
  this.queue = [];
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

ScrubberWidget.prototype = new HoloViewsWidget;

ScrubberWidget.prototype.set_frame = function(frame){
  this.current_frame = frame;
  widget = document.getElementById(this.slider_id);
  if (widget === null) {
    this.pause_animation();
    return
  }
  widget.value = this.current_frame;
  if(this.cached) {
    this.update(frame)
  } else {
    this.dynamic_update(frame)
  }
}


ScrubberWidget.prototype.get_loop_state = function(){
  var button_group = document[this.loop_select_id].state;
  for (var i = 0; i < button_group.length; i++) {
    var button = button_group[i];
    if (button.checked) {
      return button.value;
    }
  }
  return undefined;
}


ScrubberWidget.prototype.next_frame = function() {
  this.set_frame(Math.min(this.length - 1, this.current_frame + 1));
}

ScrubberWidget.prototype.previous_frame = function() {
  this.set_frame(Math.max(0, this.current_frame - 1));
}

ScrubberWidget.prototype.first_frame = function() {
  this.set_frame(0);
}

ScrubberWidget.prototype.last_frame = function() {
  this.set_frame(this.length - 1);
}

ScrubberWidget.prototype.slower = function() {
  this.interval /= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.faster = function() {
  this.interval *= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.anim_step_forward = function() {
  if(this.current_frame < this.length - 1){
    this.next_frame();
  }else{
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.first_frame();
    }else if(loop_state == "reflect"){
      this.last_frame();
      this.reverse_animation();
    }else{
      this.pause_animation();
      this.last_frame();
    }
  }
}

ScrubberWidget.prototype.anim_step_reverse = function() {
  if(this.current_frame > 0){
    this.previous_frame();
  } else {
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.last_frame();
    }else if(loop_state == "reflect"){
      this.first_frame();
      this.play_animation();
    }else{
      this.pause_animation();
      this.first_frame();
    }
  }
}

ScrubberWidget.prototype.pause_animation = function() {
  this.direction = 0;
  if (this.timer){
    clearInterval(this.timer);
    this.timer = null;
  }
}

ScrubberWidget.prototype.play_animation = function() {
  this.pause_animation();
  this.direction = 1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_forward();}, this.interval);
}

ScrubberWidget.prototype.reverse_animation = function() {
  this.pause_animation();
  this.direction = -1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_reverse();}, this.interval);
}

function extend(destination, source) {
  for (var k in source) {
    if (source.hasOwnProperty(k)) {
      destination[k] = source[k];
    }
  }
  return destination;
}

function update_widget(widget, values) {
  if (widget.hasClass("ui-slider")) {
    widget.slider('option', {
      min: 0,
      max: values.length-1,
      dim_vals: values,
      value: 0,
      dim_labels: values
	})
    widget.slider('option', 'slide').call(widget, event, {value: 0})
  } else {
    widget.empty();
    for (var i=0; i<values.length; i++){
      widget.append($("<option>", {
        value: i,
        text: values[i]
      }))
    };
    widget.data('values', values);
    widget.data('value', 0);
    widget.trigger("change");
  };
}

// Define MPL specific subclasses
function MPLSelectionWidget() {
    SelectionWidget.apply(this, arguments);
}

function MPLScrubberWidget() {
    ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
MPLSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
MPLScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var MPLMethods = {
    init_slider : function(init_val){
        if(this.load_json) {
            this.from_json()
        } else {
            this.update_cache();
        }
        this.update(0);
        if(this.mode == 'nbagg') {
            this.set_frame(init_val, 0);
        }
    },
    populate_cache : function(idx){
        var cache_id = "_anim_img"+this.id+"_"+idx;
        this.cache[idx].html(this.frames[idx]);
        if (this.embed) {
            delete this.frames[idx];
        }
    },
    process_msg : function(msg) {
        if (!(this.mode == 'nbagg')) {
            var data = msg.content.data;
            this.frames[this.current] = data;
            this.update_cache(true);
            this.update(this.current);
        }
    }
}
// Extend MPL widgets with backend specific methods
extend(MPLSelectionWidget.prototype, MPLMethods);
extend(MPLScrubberWidget.prototype, MPLMethods);

// Define Bokeh specific subclasses
function BokehSelectionWidget() {
	SelectionWidget.apply(this, arguments);
}

function BokehScrubberWidget() {
	ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
BokehSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
BokehScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var BokehMethods = {
	update_cache : function(){
		$.each(this.frames, $.proxy(function(index, frame) {
			this.frames[index] = JSON.parse(frame);
		}, this));
	},
	update : function(current){
		if (current === undefined) {
			var data = undefined;
		} else {
			var data = this.frames[current];
		}
		if (data !== undefined) {
			var doc = Bokeh.index[data.root].model.document;
			doc.apply_json_patch(data.content);
		}
	},
	init_comms : function() {
	}
}

// Extend Bokeh widgets with backend specific methods
extend(BokehSelectionWidget.prototype, BokehMethods);
extend(BokehScrubberWidget.prototype, BokehMethods);
</script>


<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<style>div.hololayout {
    display: flex;
    align-items: center;
    margin: 0;
}

div.holoframe {
	width: 75%;
}

div.holowell {
    display: flex;
    align-items: center;
    margin: 0;
}

form.holoform {
    background-color: #fafafa;
    border-radius: 5px;
    overflow: hidden;
	padding-left: 0.8em;
    padding-right: 0.8em;
    padding-top: 0.4em;
    padding-bottom: 0.4em;
}

div.holowidgets {
    padding-right: 0;
	width: 25%;
}

div.holoslider {
    min-height: 0 !important;
    height: 0.8em;
    width: 60%;
}

div.holoformgroup {
    padding-top: 0.5em;
    margin-bottom: 0.5em;
}

div.hologroup {
    padding-left: 0;
    padding-right: 0.8em;
    width: 50%;
}

.holoselect {
    width: 92%;
    margin-left: 0;
    margin-right: 0;
}

.holotext {
    width: 100%;
    padding-left:  0.5em;
    padding-right: 0;
}

.holowidgets .ui-resizable-se {
	visibility: hidden
}

.holoframe > .ui-resizable-se {
	visibility: hidden
}

.holowidgets .ui-resizable-s {
	visibility: hidden
}

div.bk-hbox {
    display: flex;
    justify-content: center;
}

div.bk-hbox div.bk-plot {
    padding: 8px;
}

div.bk-hbox div.bk-data-table {
    padding: 20px;
}
</style>


<div class="logo-block">
<img src='data:image/png;base64,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
roTBs2RqAAAAAElFTkSuQmCC'
     style='height:25px; border-radius:12px; display: inline-block; float: left; vertical-align: middle'></img>


  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



</div>




```python
#create a dataframe

df1 = pd.DataFrame({
    'id':[1,2,3,4,5,6,7,8,9,10,11],
    'number': ['16.30', '17.20', '17.70','16.30','17.90','15.90','16.00','18.12','16.40','17.00','16.32'],
    'response':[0,1,1,0,0,1,0,1,0,0,0]},
    index=[1,2,3,4,5,6,7,8,9,10,11])
```


```python
#Indexing dataframes by 'id'

df1.set_index(['id']).head(11)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>number</th>
      <th>response</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>16.30</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>17.20</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>17.70</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>16.30</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>17.90</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>15.90</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>16.00</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>18.12</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>16.40</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>17.00</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>16.32</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Let's create a new variable 'date' from current year and range from 2005 to 2015. Then I'll add this new column to each dataframe

year = datetime.datetime.today().year
date = range(2005,year-2)
date

#Also, can create a new variable date which years ranging between 2005 and 2015 as:
#date = pd.date_range('2005', '2016', freq='A')
```




    [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]




```python
#Convert list to an array with float format

date = np.array(date, dtype=np.float32)
date
```




    array([ 2005.,  2006.,  2007.,  2008.,  2009.,  2010.,  2011.,  2012.,
            2013.,  2014.,  2015.], dtype=float32)




```python
#Sort by reverse index
#df1.sort_index(ascending=False).head(11)
```


```python
#Define object length using the the variable 'number' as reference

sLength = len(df1['number'])

#Add the new variable 'date' to each dataframe

df1['date'] = date
```


```python
#Sort by'number' values

df1.sort_values('number').head(11)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>number</th>
      <th>response</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>15.90</td>
      <td>1</td>
      <td>2010.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>16.00</td>
      <td>0</td>
      <td>2011.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>16.30</td>
      <td>0</td>
      <td>2005.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>16.30</td>
      <td>0</td>
      <td>2008.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11</td>
      <td>16.32</td>
      <td>0</td>
      <td>2015.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>16.40</td>
      <td>0</td>
      <td>2013.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>17.00</td>
      <td>0</td>
      <td>2014.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>17.20</td>
      <td>1</td>
      <td>2006.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>17.70</td>
      <td>1</td>
      <td>2007.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>17.90</td>
      <td>0</td>
      <td>2009.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>18.12</td>
      <td>1</td>
      <td>2012.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#convert the variable 'number' to float64
df1[['number']] = df1[['number']].astype('float')

#convert the variable 'year' to int
df1[['date']] = df1[['date']].astype('int')
#output['date'] = pd.to_datetime(output['date'])
#output['date'] = output['date'].apply(lambda x: x.strftime('%Y'))

#Convert "response" variable to boolean
df1[['response']] = df1[['response']].astype('bool') #Also: #output['response'].astype(str).astype(int)
                                                                 #pd.factorize(output['response'])[0]
```


```python
#see dtype objects
df1.dtypes
```




    id            int64
    number      float64
    response       bool
    date          int64
    dtype: object




```python
df1
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>number</th>
      <th>response</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>16.30</td>
      <td>False</td>
      <td>2005</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>17.20</td>
      <td>True</td>
      <td>2006</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>17.70</td>
      <td>True</td>
      <td>2007</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>16.30</td>
      <td>False</td>
      <td>2008</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>17.90</td>
      <td>False</td>
      <td>2009</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>15.90</td>
      <td>True</td>
      <td>2010</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>16.00</td>
      <td>False</td>
      <td>2011</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>18.12</td>
      <td>True</td>
      <td>2012</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>16.40</td>
      <td>False</td>
      <td>2013</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>17.00</td>
      <td>False</td>
      <td>2014</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11</td>
      <td>16.32</td>
      <td>False</td>
      <td>2015</td>
    </tr>
  </tbody>
</table>
</div>




```python
df1.set_index(['date']).head(11)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>number</th>
      <th>response</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2005</th>
      <td>1</td>
      <td>16.30</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>2</td>
      <td>17.20</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>3</td>
      <td>17.70</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>4</td>
      <td>16.30</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>5</td>
      <td>17.90</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>6</td>
      <td>15.90</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>7</td>
      <td>16.00</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>8</td>
      <td>18.12</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>9</td>
      <td>16.40</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>10</td>
      <td>17.00</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>11</td>
      <td>16.32</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>




```python
from ipywidgets import interact
import numpy as np

from bokeh.io import push_notebook
from bokeh.plotting import figure, show, output_notebook
```


```python
x = df1['date']
y = df1['number']
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="a597a527-58d2-4ef9-8c5e-e4b9cd5d8655">Loading BokehJS ...</span>
    </div>





```python
#Plot number vs date using matplotlib

from matplotlib import pylab as plt
df1.sort_values(by='date').plot(x='date', y='number', label=id)
plt.ylabel("number")
plt.legend(loc='lower right')
```




    <matplotlib.legend.Legend at 0x7f8a3d908410>




![png](MILESTONE/images/output_19_1.png)



```python
#Use Bokeh to create an interactive plot of the temporal trend

output_notebook()
TOOLS = "pan, box_zoom, wheel_zoom, reset, save"

p = figure(tools=TOOLS,title="Temporal trend", plot_height=300, plot_width=600, y_range=(15,20),x_axis_label="date")
r = p.line(x, y, color="#2222aa", line_width=3)
show(p)
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="217cf081-ed03-4ccb-b9c6-be6fbf2faed4">Loading BokehJS ...</span>
    </div>






<div class="bk-root">
    <div class="bk-plotdiv" id="eb53c6dd-8b9f-4cca-bd03-76481c427b78"></div>
</div>





```python
#Create two additional dataframes

df2 = pd.DataFrame({
    'id':[12,13,14,15,16,17,18,19,20,21,22],
    'number': ['18.00', '18.20', '16.90','17.10','16.60','17.50','17.60','17.62','17.30','16.50','17.12'],
    'response':[1,1,0,0,1,0,0,1,1,0,1]},
    index=[11,12,13,14,15,16,17,18,19,20,21])

df3 = pd.DataFrame({
    'id':[23,24,25,26,27,28,29,30,31,32,33],
    'number': ['16.00', '15.88', '17.30','15.90','16.00','17.10','16.60','15.92','16.30','16.10','17.42'],
    'response':[1,0,0,1,1,0,1,0,1,1,0]},
    index=[22,23,24,25,26,27,28,29,30,31,32])
```


```python
#Indexing dataframes by 'id'

df2.set_index(['id']).head(11)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>number</th>
      <th>response</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>12</th>
      <td>18.00</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>18.20</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>16.90</td>
      <td>0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>17.10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>16.60</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>17.50</td>
      <td>0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>17.60</td>
      <td>0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>17.62</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20</th>
      <td>17.30</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>16.50</td>
      <td>0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>17.12</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
df3.set_index(['id']).head(11)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>number</th>
      <th>response</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>23</th>
      <td>16.00</td>
      <td>1</td>
    </tr>
    <tr>
      <th>24</th>
      <td>15.88</td>
      <td>0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>17.30</td>
      <td>0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>15.90</td>
      <td>1</td>
    </tr>
    <tr>
      <th>27</th>
      <td>16.00</td>
      <td>1</td>
    </tr>
    <tr>
      <th>28</th>
      <td>17.10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>16.60</td>
      <td>1</td>
    </tr>
    <tr>
      <th>30</th>
      <td>15.92</td>
      <td>0</td>
    </tr>
    <tr>
      <th>31</th>
      <td>16.30</td>
      <td>1</td>
    </tr>
    <tr>
      <th>32</th>
      <td>16.10</td>
      <td>1</td>
    </tr>
    <tr>
      <th>33</th>
      <td>17.42</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Define object length using the the variable 'number' as reference

sLength = len(df1['number'])

#Add the new variable 'date' to each dataframe

df2['date'] = date
df3['date'] = date
```


```python
#Concatenate the three dataframes

dfs = [df1, df2, df3]
output = pd.concat(dfs)

#Also, can use merge to combine the three dataframes
#output_join= output.merge(output, on='date', how='left')
#output_join.head(33)
```


```python
#convert the variable 'number' to float64
output[['number']] = output[['number']].astype('float')

#convert the variable 'year' to int
output[['date']] = output[['date']].astype('int')

#Convert "response" variable to boolean True/False
output[['response']] = output[['response']].astype('bool')
```


```python
#Indexing by date

output.set_index(['date']).head(33)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>number</th>
      <th>response</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2005</th>
      <td>1</td>
      <td>16.30</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>2</td>
      <td>17.20</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>3</td>
      <td>17.70</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>4</td>
      <td>16.30</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>5</td>
      <td>17.90</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>6</td>
      <td>15.90</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>7</td>
      <td>16.00</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>8</td>
      <td>18.12</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>9</td>
      <td>16.40</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>10</td>
      <td>17.00</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>11</td>
      <td>16.32</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>12</td>
      <td>18.00</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>13</td>
      <td>18.20</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>14</td>
      <td>16.90</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>15</td>
      <td>17.10</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>16</td>
      <td>16.60</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>17</td>
      <td>17.50</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>18</td>
      <td>17.60</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>19</td>
      <td>17.62</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>20</td>
      <td>17.30</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>21</td>
      <td>16.50</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>22</td>
      <td>17.12</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>23</td>
      <td>16.00</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>24</td>
      <td>15.88</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>25</td>
      <td>17.30</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>26</td>
      <td>15.90</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>27</td>
      <td>16.00</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>28</td>
      <td>17.10</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>29</td>
      <td>16.60</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>30</td>
      <td>15.92</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>31</td>
      <td>16.30</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>32</td>
      <td>16.10</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>33</td>
      <td>17.42</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>




```python
#A short description of the variable "number" in the combined dataframes

print "Numbers between 2005 and 2015"
output['number'].describe()
```

    Numbers between 2005 and 2015





    count    33.000000
    mean     16.851515
    std       0.733468
    min      15.880000
    25%      16.300000
    50%      16.900000
    75%      17.420000
    max      18.200000
    Name: number, dtype: float64




```python
#select column 'number' and sum all its values

sum_numb= output['number'].sum()
sum_numb
```




    556.09999999999991




```python
#How many unique values are there in the dataframe?

output['number'].unique()[:11]
```




    array([ 16.3 ,  17.2 ,  17.7 ,  17.9 ,  15.9 ,  16.  ,  18.12,  16.4 ,
            17.  ,  16.32,  18.  ])




```python
#How many cases of each value are there?
output['number'].value_counts().head(33)
```




    16.00    3
    16.30    3
    17.30    2
    17.10    2
    15.90    2
    16.60    2
    17.42    1
    15.92    1
    17.00    1
    18.00    1
    18.12    1
    17.50    1
    18.20    1
    16.50    1
    17.60    1
    17.62    1
    17.70    1
    17.90    1
    15.88    1
    16.90    1
    16.10    1
    17.12    1
    16.32    1
    17.20    1
    16.40    1
    Name: number, dtype: int64




```python
output.plot(x="date", y=["number", "response"],  figsize=(12, 8), kind="bar")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f8a3a050310>




![png](MILESTONE/images/output_32_1.png)



```python
#Assign axis names to each dataframe
output = pd.concat(dfs, keys=['x', 'y', 'z'])
output
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>id</th>
      <th>number</th>
      <th>response</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="11" valign="top">x</th>
      <th>1</th>
      <td>1</td>
      <td>16.3</td>
      <td>0</td>
      <td>2005.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>17.2</td>
      <td>1</td>
      <td>2006.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>17.7</td>
      <td>1</td>
      <td>2007.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>16.3</td>
      <td>0</td>
      <td>2008.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>17.9</td>
      <td>0</td>
      <td>2009.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>15.9</td>
      <td>1</td>
      <td>2010.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>16</td>
      <td>0</td>
      <td>2011.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>18.12</td>
      <td>1</td>
      <td>2012.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>16.4</td>
      <td>0</td>
      <td>2013.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>10</td>
      <td>17</td>
      <td>0</td>
      <td>2014.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>11</td>
      <td>16.32</td>
      <td>0</td>
      <td>2015.0</td>
    </tr>
    <tr>
      <th rowspan="11" valign="top">y</th>
      <th>11</th>
      <td>12</td>
      <td>18.00</td>
      <td>1</td>
      <td>2005.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>13</td>
      <td>18.20</td>
      <td>1</td>
      <td>2006.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>14</td>
      <td>16.90</td>
      <td>0</td>
      <td>2007.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>15</td>
      <td>17.10</td>
      <td>0</td>
      <td>2008.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>16</td>
      <td>16.60</td>
      <td>1</td>
      <td>2009.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>17</td>
      <td>17.50</td>
      <td>0</td>
      <td>2010.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18</td>
      <td>17.60</td>
      <td>0</td>
      <td>2011.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>19</td>
      <td>17.62</td>
      <td>1</td>
      <td>2012.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>20</td>
      <td>17.30</td>
      <td>1</td>
      <td>2013.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>21</td>
      <td>16.50</td>
      <td>0</td>
      <td>2014.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>22</td>
      <td>17.12</td>
      <td>1</td>
      <td>2015.0</td>
    </tr>
    <tr>
      <th rowspan="11" valign="top">z</th>
      <th>22</th>
      <td>23</td>
      <td>16.00</td>
      <td>1</td>
      <td>2005.0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>24</td>
      <td>15.88</td>
      <td>0</td>
      <td>2006.0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>25</td>
      <td>17.30</td>
      <td>0</td>
      <td>2007.0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>26</td>
      <td>15.90</td>
      <td>1</td>
      <td>2008.0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>27</td>
      <td>16.00</td>
      <td>1</td>
      <td>2009.0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>28</td>
      <td>17.10</td>
      <td>0</td>
      <td>2010.0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>29</td>
      <td>16.60</td>
      <td>1</td>
      <td>2011.0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>30</td>
      <td>15.92</td>
      <td>0</td>
      <td>2012.0</td>
    </tr>
    <tr>
      <th>30</th>
      <td>31</td>
      <td>16.30</td>
      <td>1</td>
      <td>2013.0</td>
    </tr>
    <tr>
      <th>31</th>
      <td>32</td>
      <td>16.10</td>
      <td>1</td>
      <td>2014.0</td>
    </tr>
    <tr>
      <th>32</th>
      <td>33</td>
      <td>17.42</td>
      <td>0</td>
      <td>2015.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#################################################################################################################################
################################################ MILESTONE PROJECT - PART 2 ######################################################

#1. Request data from public API using request and simplejson libraries
#2. Convert jSon data to Pandas dataframe
#3. Create table and plotting data (Bokeh, Holoviews)

```


```python
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144
```


```python
import pandas as pd
import json
from io import StringIO
import io
import csv
import sys
import datetime
import numpy as np
import re

```


```python
import simplejson as json
import urllib2
import requests
import ujson as json
```


```python
import holoviews as hv
hv.extension('bokeh', 'matplotlib')
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Spectral6
from ipywidgets import *
```





<script src="https://code.jquery.com/ui/1.10.4/jquery-ui.min.js" type="text/javascript"></script>
<script type="text/javascript">function HoloViewsWidget(){
}

HoloViewsWidget.comms = {};
HoloViewsWidget.comm_state = {};

HoloViewsWidget.prototype.init_slider = function(init_val){
  if(this.load_json) {
    this.from_json()
  } else {
    this.update_cache();
  }
}

HoloViewsWidget.prototype.populate_cache = function(idx){
  this.cache[idx].html(this.frames[idx]);
  if (this.embed) {
    delete this.frames[idx];
  }
}

HoloViewsWidget.prototype.process_error = function(msg){

}

HoloViewsWidget.prototype.from_json = function() {
  var data_url = this.json_path + this.id + '.json';
  $.getJSON(data_url, $.proxy(function(json_data) {
    this.frames = json_data;
    this.update_cache();
    this.update(0);
  }, this));
}

HoloViewsWidget.prototype.dynamic_update = function(current){
  if (current === undefined) {
    return
  }
  if(this.dynamic) {
    current = JSON.stringify(current);
  }
  function callback(initialized, msg){
    /* This callback receives data from Python as a string
       in order to parse it correctly quotes are sliced off*/
    if (msg.content.ename != undefined) {
      this.process_error(msg);
    }
    if (msg.msg_type != "execute_result") {
      console.log("Warning: HoloViews callback returned unexpected data for key: (", current, ") with the following content:", msg.content)
    } else {
      if (msg.content.data['text/plain'].includes('Complete')) {
        if (this.queue.length > 0) {
          this.time = Date.now();
          this.dynamic_update(this.queue[this.queue.length-1]);
          this.queue = [];
        } else {
          this.wait = false;
        }
        return
      }
    }
  }
  this.current = current;
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null)) {
    var kernel = Jupyter.notebook.kernel;
    callbacks = {iopub: {output: $.proxy(callback, this, this.initialized)}};
    var cmd = "holoviews.plotting.widgets.NdWidget.widgets['" + this.id + "'].update(" + current + ")";
    kernel.execute("import holoviews;" + cmd, callbacks, {silent : false});
  }
}

HoloViewsWidget.prototype.update_cache = function(force){
  var frame_len = Object.keys(this.frames).length;
  for (var i=0; i<frame_len; i++) {
    if(!this.load_json || this.dynamic)  {
      frame = Object.keys(this.frames)[i];
    } else {
      frame = i;
    }
    if(!(frame in this.cache) || force) {
      if ((frame in this.cache) && force) { this.cache[frame].remove() }
      this.cache[frame] = $('<div />').appendTo("#"+"_anim_img"+this.id).hide();
      var cache_id = "_anim_img"+this.id+"_"+frame;
      this.cache[frame].attr("id", cache_id);
      this.populate_cache(frame);
    }
  }
}

HoloViewsWidget.prototype.update = function(current){
  if(current in this.cache) {
    $.each(this.cache, function(index, value) {
      value.hide();
    });
    this.cache[current].show();
    this.wait = false;
  }
}

HoloViewsWidget.prototype.init_comms = function() {
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel !== undefined)) {
    var widget = this;
    comm_manager = Jupyter.notebook.kernel.comm_manager;
    comm_manager.register_target(this.id, function (comm) {
      comm.on_msg(function (msg) { widget.process_msg(msg) });
    });
  }
}

HoloViewsWidget.prototype.process_msg = function(msg) {
}

function SelectionWidget(frames, id, slider_ids, keyMap, dim_vals, notFound, load_json, mode, cached, json_path, dynamic){
  this.frames = frames;
  this.id = id;
  this.slider_ids = slider_ids;
  this.keyMap = keyMap
  this.current_frame = 0;
  this.current_vals = dim_vals;
  this.load_json = load_json;
  this.mode = mode;
  this.notFound = notFound;
  this.cached = cached;
  this.dynamic = dynamic;
  this.cache = {};
  this.json_path = json_path;
  this.init_slider(this.current_vals[0]);
  this.queue = [];
  this.wait = false;
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

SelectionWidget.prototype = new HoloViewsWidget;


SelectionWidget.prototype.get_key = function(current_vals) {
  var key = "(";
  for (var i=0; i<this.slider_ids.length; i++)
  {
    val = this.current_vals[i];
    if (!(typeof val === 'string')) {
      if (val % 1 === 0) { val = val.toFixed(1); }
      else { val = val.toFixed(10); val = val.slice(0, val.length-1);}
    }
    key += "'" + val + "'";
    if(i != this.slider_ids.length-1) { key += ', ';}
    else if(this.slider_ids.length == 1) { key += ',';}
  }
  key += ")";
  return this.keyMap[key];
}

SelectionWidget.prototype.set_frame = function(dim_val, dim_idx){
  this.current_vals[dim_idx] = dim_val;
  var key = this.current_vals;
  if (!this.dynamic) {
    key = this.get_key(key)
  }
  if (this.dynamic || !this.cached) {
    if ((this.time !== undefined) && ((this.wait) && ((this.time + 10000) > Date.now()))) {
      this.queue.push(key);
      return
    }
    this.queue = [];
    this.time = Date.now();
    this.current_frame = key;
    this.wait = true;
    this.dynamic_update(key)
  } else if (key !== undefined) {
    this.update(key)
  }
}


/* Define the ScrubberWidget class */
function ScrubberWidget(frames, num_frames, id, interval, load_json, mode, cached, json_path, dynamic){
  this.slider_id = "_anim_slider" + id;
  this.loop_select_id = "_anim_loop_select" + id;
  this.id = id;
  this.interval = interval;
  this.current_frame = 0;
  this.direction = 0;
  this.dynamic = dynamic;
  this.timer = null;
  this.load_json = load_json;
  this.mode = mode;
  this.cached = cached;
  this.frames = frames;
  this.cache = {};
  this.length = num_frames;
  this.json_path = json_path;
  document.getElementById(this.slider_id).max = this.length - 1;
  this.init_slider(0);
  this.wait = false;
  this.queue = [];
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

ScrubberWidget.prototype = new HoloViewsWidget;

ScrubberWidget.prototype.set_frame = function(frame){
  this.current_frame = frame;
  widget = document.getElementById(this.slider_id);
  if (widget === null) {
    this.pause_animation();
    return
  }
  widget.value = this.current_frame;
  if(this.cached) {
    this.update(frame)
  } else {
    this.dynamic_update(frame)
  }
}


ScrubberWidget.prototype.get_loop_state = function(){
  var button_group = document[this.loop_select_id].state;
  for (var i = 0; i < button_group.length; i++) {
    var button = button_group[i];
    if (button.checked) {
      return button.value;
    }
  }
  return undefined;
}


ScrubberWidget.prototype.next_frame = function() {
  this.set_frame(Math.min(this.length - 1, this.current_frame + 1));
}

ScrubberWidget.prototype.previous_frame = function() {
  this.set_frame(Math.max(0, this.current_frame - 1));
}

ScrubberWidget.prototype.first_frame = function() {
  this.set_frame(0);
}

ScrubberWidget.prototype.last_frame = function() {
  this.set_frame(this.length - 1);
}

ScrubberWidget.prototype.slower = function() {
  this.interval /= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.faster = function() {
  this.interval *= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.anim_step_forward = function() {
  if(this.current_frame < this.length - 1){
    this.next_frame();
  }else{
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.first_frame();
    }else if(loop_state == "reflect"){
      this.last_frame();
      this.reverse_animation();
    }else{
      this.pause_animation();
      this.last_frame();
    }
  }
}

ScrubberWidget.prototype.anim_step_reverse = function() {
  if(this.current_frame > 0){
    this.previous_frame();
  } else {
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.last_frame();
    }else if(loop_state == "reflect"){
      this.first_frame();
      this.play_animation();
    }else{
      this.pause_animation();
      this.first_frame();
    }
  }
}

ScrubberWidget.prototype.pause_animation = function() {
  this.direction = 0;
  if (this.timer){
    clearInterval(this.timer);
    this.timer = null;
  }
}

ScrubberWidget.prototype.play_animation = function() {
  this.pause_animation();
  this.direction = 1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_forward();}, this.interval);
}

ScrubberWidget.prototype.reverse_animation = function() {
  this.pause_animation();
  this.direction = -1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_reverse();}, this.interval);
}

function extend(destination, source) {
  for (var k in source) {
    if (source.hasOwnProperty(k)) {
      destination[k] = source[k];
    }
  }
  return destination;
}

function update_widget(widget, values) {
  if (widget.hasClass("ui-slider")) {
    widget.slider('option', {
      min: 0,
      max: values.length-1,
      dim_vals: values,
      value: 0,
      dim_labels: values
	})
    widget.slider('option', 'slide').call(widget, event, {value: 0})
  } else {
    widget.empty();
    for (var i=0; i<values.length; i++){
      widget.append($("<option>", {
        value: i,
        text: values[i]
      }))
    };
    widget.data('values', values);
    widget.data('value', 0);
    widget.trigger("change");
  };
}

// Define MPL specific subclasses
function MPLSelectionWidget() {
    SelectionWidget.apply(this, arguments);
}

function MPLScrubberWidget() {
    ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
MPLSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
MPLScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var MPLMethods = {
    init_slider : function(init_val){
        if(this.load_json) {
            this.from_json()
        } else {
            this.update_cache();
        }
        this.update(0);
        if(this.mode == 'nbagg') {
            this.set_frame(init_val, 0);
        }
    },
    populate_cache : function(idx){
        var cache_id = "_anim_img"+this.id+"_"+idx;
        this.cache[idx].html(this.frames[idx]);
        if (this.embed) {
            delete this.frames[idx];
        }
    },
    process_msg : function(msg) {
        if (!(this.mode == 'nbagg')) {
            var data = msg.content.data;
            this.frames[this.current] = data;
            this.update_cache(true);
            this.update(this.current);
        }
    }
}
// Extend MPL widgets with backend specific methods
extend(MPLSelectionWidget.prototype, MPLMethods);
extend(MPLScrubberWidget.prototype, MPLMethods);

// Define Bokeh specific subclasses
function BokehSelectionWidget() {
	SelectionWidget.apply(this, arguments);
}

function BokehScrubberWidget() {
	ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
BokehSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
BokehScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var BokehMethods = {
	update_cache : function(){
		$.each(this.frames, $.proxy(function(index, frame) {
			this.frames[index] = JSON.parse(frame);
		}, this));
	},
	update : function(current){
		if (current === undefined) {
			var data = undefined;
		} else {
			var data = this.frames[current];
		}
		if (data !== undefined) {
			var doc = Bokeh.index[data.root].model.document;
			doc.apply_json_patch(data.content);
		}
	},
	init_comms : function() {
	}
}

// Extend Bokeh widgets with backend specific methods
extend(BokehSelectionWidget.prototype, BokehMethods);
extend(BokehScrubberWidget.prototype, BokehMethods);
</script>


<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<style>div.hololayout {
    display: flex;
    align-items: center;
    margin: 0;
}

div.holoframe {
	width: 75%;
}

div.holowell {
    display: flex;
    align-items: center;
    margin: 0;
}

form.holoform {
    background-color: #fafafa;
    border-radius: 5px;
    overflow: hidden;
	padding-left: 0.8em;
    padding-right: 0.8em;
    padding-top: 0.4em;
    padding-bottom: 0.4em;
}

div.holowidgets {
    padding-right: 0;
	width: 25%;
}

div.holoslider {
    min-height: 0 !important;
    height: 0.8em;
    width: 60%;
}

div.holoformgroup {
    padding-top: 0.5em;
    margin-bottom: 0.5em;
}

div.hologroup {
    padding-left: 0;
    padding-right: 0.8em;
    width: 50%;
}

.holoselect {
    width: 92%;
    margin-left: 0;
    margin-right: 0;
}

.holotext {
    width: 100%;
    padding-left:  0.5em;
    padding-right: 0;
}

.holowidgets .ui-resizable-se {
	visibility: hidden
}

.holoframe > .ui-resizable-se {
	visibility: hidden
}

.holowidgets .ui-resizable-s {
	visibility: hidden
}

div.bk-hbox {
    display: flex;
    justify-content: center;
}

div.bk-hbox div.bk-plot {
    padding: 8px;
}

div.bk-hbox div.bk-data-table {
    padding: 20px;
}
</style>


<div class="logo-block">
<img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz
AAAB+wAAAfsBxc2miwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAA6zSURB
VHic7ZtpeFRVmsf/5966taWqUlUJ2UioBBJiIBAwCZtog9IOgjqACsogKtqirT2ttt069nQ/zDzt
tI4+CrJIREFaFgWhBXpUNhHZQoKBkIUASchWla1S+3ar7r1nPkDaCAnZKoQP/D7mnPOe9/xy76n3
nFSAW9ziFoPFNED2LLK5wcyBDObkb8ZkxuaoSYlI6ZcOKq1eWFdedqNzGHQBk9RMEwFAASkk0Xw3
ETacDNi2vtvc7L0ROdw0AjoSotQVkKSvHQz/wRO1lScGModBFbDMaNRN1A4tUBCS3lk7BWhQkgpD
lG4852/+7DWr1R3uHAZVQDsbh6ZPN7CyxUrCzJMRouusj0ipRwD2uKm0Zn5d2dFwzX1TCGhnmdGo
G62Nna+isiUqhkzuKrkQaJlPEv5mFl2fvGg2t/VnzkEV8F5ioioOEWkLG86fvbpthynjdhXYZziQ
x1hC9J2NFyi8vCTt91Fh04KGip0AaG9zuCk2wQCVyoNU3Hjezee9bq92duzzTmxsRJoy+jEZZZYo
GTKJ6SJngdJqAfRzpze0+jHreUtPc7gpBLQnIYK6BYp/uGhw9YK688eu7v95ysgshcg9qSLMo3JC
4jqLKQFBgdKDPoQ+Pltb8dUyQLpeDjeVgI6EgLIQFT5tEl3rn2losHVsexbZ3EyT9wE1uGdkIPcy
BGxn8QUq1QrA5nqW5i2tLqvrrM9NK6AdkVIvL9E9bZL/oyfMVd/jqvc8LylzRBKDJSzIExwhQzuL
QYGQj4rHfFTc8mUdu3E7yoLtbTe9gI4EqVgVkug2i5+uXGo919ixbRog+3fTbQ8qJe4ZOYNfMoTI
OoshUNosgO60AisX15aeI2PSIp5KiFLI9ubb1vV3Qb2ltwLakUCDAkWX7/nHKRmmGIl9VgYsUhJm
2NXjKYADtM1ygne9QQDIXlk49FBstMKx66D1v4+XuQr7vqTe0VcBHQlRWiOCbmmSYe2SqtL6q5rJ
zsTb7lKx3FKOYC4DoqyS/B5bvLPxvD9Qtf6saxYLQGJErmDOdOMr/zo96km1nElr8bmPOBwI9COv
HnFPRIwmkSOv9kcAS4heRsidOkpeWBgZM+UBrTFAXNYL5Vf2ii9c1trNzpYdaoVil3WIc+wdk+gQ
noie3ecCcxt9ITcLAPWt/laGEO/9U6PmzZkenTtsSMQ8uYywJVW+grCstAvCIaAdArAsIWkRDDs/
KzLm2YcjY1Lv0UdW73HabE9n6V66cxSzfEmuJssTpKGVp+0vHq73FwL46eOjpMpbRAnNmJFrGJNu
Ukf9Yrz+3rghiumCKNXXWPhLYcjxGsIpoCMsIRoFITkW8AuyM8jC1+/QLx4bozCEJIq38+1rtpR6
V/yzb8eBlRb3fo5l783N0CWolAzJHaVNzkrTzlEp2bQ2q3TC5gn6wpnoQAmwSiGh2GitnTmVMc5O
UyfKWUKCIsU7+fZDKwqdT6DDpvkzAX4/+AMFjk0tDp5GRXLpQ2MUmhgDp5gxQT8+Y7hyPsMi8uxF
71H0oebujHALECjFKaW9Lm68n18wXp2kVzIcABytD5iXFzg+WVXkegpAsOOYziqo0OkK76GyquC3
ltZAzMhhqlSNmmWTE5T6e3IN05ITFLM4GdN0vtZ3ob8Jh1NAKXFbm5PtLU/eqTSlGjkNAJjdgn/N
aedXa0tdi7+t9G0FIF49rtMSEgAs1kDLkTPO7ebm4IUWeyh1bKomXqlgMG6kJmHcSM0clYLJ8XtR
1GTnbV3F6I5wCGikAb402npp1h1s7LQUZZSMIfALFOuL3UUrfnS8+rez7v9qcold5tilgHbO1fjK
9ubb17u9oshxzMiUBKXWqJNxd+fqb0tLVs4lILFnK71H0Ind7uiPgACVcFJlrb0tV6DzxqqTIhUM
CwDf1/rrVhTa33/3pGPxJYdQ2l2cbgVcQSosdx8uqnDtbGjh9SlDVSMNWhlnilfqZk42Th2ZpLpf
xrHec5e815zrr0dfBZSwzkZfqsv+1FS1KUknUwPARVvItfKUY+cn57yP7qv07UE3p8B2uhUwLk09
e0SCOrK+hbdYHYLjRIl71wWzv9jpEoeOHhGRrJAzyEyNiJuUqX0g2sBN5kGK6y2Blp5M3lsB9Qh4
y2Ja6x6+i0ucmKgwMATwhSjdUu49tKrQ/pvN5d53ml2CGwCmJipmKjgmyuaXzNeL2a0AkQ01Th5j
2DktO3Jyk8f9vcOBQHV94OK+fPumJmvQHxJoWkaKWq9Vs+yUsbq0zGT1I4RgeH2b5wef7+c7bl8F
eKgoHVVZa8ZPEORzR6sT1BzDUAD/d9F78e2Tzv99v8D+fLVTqAKAsbGamKey1Mt9Ann4eH3gTXTz
idWtAJ8PQWOk7NzSeQn/OTHDuEikVF1R4z8BQCy+6D1aWRfY0tTGG2OM8rRoPaeIj5ZHzJxszElN
VM8K8JS5WOfv8mzRnQAKoEhmt8gyPM4lU9SmBK1MCQBnW4KONT86v1hZ1PbwSXPw4JWussVjtH9Y
NCoiL9UoH/6PSu8jFrfY2t36erQHXLIEakMi1SydmzB31h3GGXFDFNPaK8Rme9B79Ixrd0WN+1ij
NRQ/doRmuFLBkHSTOm5GruG+pFjFdAmorG4IXH1Qua6ASniclfFtDYt+oUjKipPrCQB7QBQ2lrgP
fFzm+9XWUtcqJ3/5vDLDpJ79XHZk3u8nGZ42qlj1+ydtbxysCezrydp6ugmipNJ7WBPB5tydY0jP
HaVNzs3QzeE4ZpTbI+ZbnSFPbVOw9vsfnVvqWnirPyCNGD08IlqtYkh2hjZ5dErEQzoNm+6ykyOt
Lt5/PQEuSRRKo22VkydK+vvS1XEKlhCJAnsqvcVvH7f/ZU2R67eXbMEGAMiIV5oWZWiWvz5Fv2xG
sjqNJQRvn3Rs2lji/lNP19VjAQDgD7FHhujZB9OGqYxRkZxixgRDVlqS6uEOFaJUVu0rPFzctrnF
JqijImVp8dEKVWyUXDk92zAuMZ6bFwpBU1HrOw6AdhQgUooChb0+ItMbWJitSo5Ws3IAOGEOtL53
0vHZih9sC4vtofZ7Qu6523V/fmGcds1TY3V36pUsBwAbSlxnVh2xLfAD/IAIMDf7XYIkNmXfpp2l
18rkAJAy9HKFaIr/qULkeQQKy9zf1JgDB2uaeFNGijo5QsUyacNUUTOnGO42xSnv4oOwpDi1zYkc
efUc3I5Gk6PhyTuVKaOGyLUAYPGIoY9Pu/atL/L92+4q9wbflRJ2Trpm/jPjdBtfnqB/dIThcl8A
KG7hbRuKnb8qsQsVvVlTrwQAQMUlf3kwJI24Z4JhPMtcfng5GcH49GsrxJpGvvHIaeem2ma+KSjQ
lIwUdYyCY8j4dE1KzijNnIP2llF2wcXNnsoapw9XxsgYAl6k+KzUXbi2yP3KR2ecf6z3BFsBICdW
nvnIaG3eHybqX7vbpEqUMT+9OL4Qpe8VON7dXuFd39v19FoAABRVePbGGuXTszO0P7tu6lghUonE
llRdrhArLvmKdh9u29jcFiRRkfLUxBiFNiqSU9icoZQHo5mYBI1MBgBH6wMNb+U7Pnw337H4gi1Y
ciWs+uks3Z9fztUvfzxTm9Ne8XXkvQLHNytOOZeiD4e0PgkAIAYCYknKUNUDSXEKzdWNpnil7r4p
xqkjTarZMtk/K8TQ6Qve78qqvXurGwIJqcOUKfUWHsm8KGvxSP68YudXq4pcj39X49uOK2X142O0
Tz5/u/7TVybqH0rSya6ZBwD21/gubbrgWdDgEOx9WUhfBaC2ibcEBYm7a7x+ukrBMNcEZggyR0TE
T8zUPjikQ4VosQZbTpS4vqizBKvqmvjsqnpfzaZyx9JPiz1/bfGKdgD45XB1zoIMzYbfTdS/NClB
Gct0USiY3YL/g0LHy/uq/Ef6uo5+n0R/vyhp17Klpge763f8rMu6YU/zrn2nml+2WtH+Z+5IAAFc
2bUTdTDOSNa9+cQY7YLsOIXhevEkCvzph7a8laecz/Un/z4/Ae04XeL3UQb57IwU9ZDr9UuKVajv
nxp1+1UVIo/LjztZkKH59fO3G/JemqCfmaCRqbqbd90ZZ8FfjtkfAyD0J/9+C2h1hDwsSxvGjNDc
b4zk5NfrSwiQblLHzZhg+Jf4aPlUwpDqkQqa9nimbt1/TDH8OitGMaQnj+RJS6B1fbF7SY1TqO5v
/v0WAADl1f7zokgS7s7VT2DZ7pegUjBM7mjtiDZbcN4j0YrHH0rXpCtY0qPX0cVL0rv5jv/ZXend
0u/EESYBAFBU4T4Qa5TflZOhTe7pmKpaP8kCVUVw1+yhXfJWvn1P3hnXi33JsTN6PnP3hHZ8Z3/h
aLHzmkNPuPj7Bc/F/Q38CwjTpSwQXgE4Vmwry9tpfq/ZFgqFMy4AVDtCvi8rvMvOmv0N4YwbVgEA
sPM72/KVnzfspmH7HQGCRLG2yL1+z8XwvPcdCbsAANh+xPzstgMtxeGKt+6MK3/tacfvwhWvIwMi
oKEBtm0H7W+UVfkc/Y1V0BhoPlDr/w1w/eu1vjIgAgDg22OtX6/eYfnEz/focrZTHAFR+PSs56/7
q32nwpjazxgwAQCwcU/T62t3WL7r6/jVRa6/byp1rei+Z98ZUAEAhEPHPc8fKnTU9nbgtnOe8h0l
9hcGIqmODLQAHCy2Xti6v/XNRivf43f4fFvIteu854+VHnR7q9tfBlwAAGz+pnndB9vM26UebAe8
SLHujPOTPVW+rwY+sxskAAC2HrA8t2Vvc7ffP1r9o+vwR2dcr92InIAbKKC1FZ5tB1tf+/G8p8sv
N/9Q5zd/XR34LYCwV5JdccMEAMDBk45DH243r/X4xGvqxFa/GNpS7n6rwOwNWwHVE26oAADYurf1
zx/utOzt+DMKYM0p17YtZZ5VNzqfsB2HewG1WXE8PoZ7gOclbTIvynZf9JV+fqZtfgs/8F/Nu5rB
EIBmJ+8QRMmpU7EzGRsf2FzuePqYRbzh/zE26EwdrT10f6r6o8HOYzCJB9Dpff8tbnGLG8L/A/WE
roTBs2RqAAAAAElFTkSuQmCC'
     style='height:25px; border-radius:12px; display: inline-block; float: left; vertical-align: middle'></img>


  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



</div>




```python
#Request search of jobless rate in USA between 1980 and 2016
#API Keys parameters can be found at: http://blog.inqubu.com/inqstats-open-api-published-to-get-demographic-data

r = requests.get('http://inqstatsapi.inqubu.com?api_key=c0081761e5b8e007&data=jobless_rate&countries=us&years=1980:2016')
r
```




    <Response [200]>




```python
print(r.content)
```

    [
        {
            "countryCode": "us",
            "countryName": "USA",
            "jobless_rate": [
                {
                    "year": "2014",
                    "data": "6.20"
                },
                {
                    "year": "2013",
                    "data": "7.40"
                },
                {
                    "year": "2012",
                    "data": "8.20"
                },
                {
                    "year": "2011",
                    "data": "9.00"
                },
                {
                    "year": "2010",
                    "data": "9.70"
                },
                {
                    "year": "2009",
                    "data": "9.40"
                },
                {
                    "year": "2008",
                    "data": "5.90"
                },
                {
                    "year": "2007",
                    "data": "4.70"
                },
                {
                    "year": "2006",
                    "data": "4.70"
                },
                {
                    "year": "2005",
                    "data": "5.20"
                },
                {
                    "year": "2004",
                    "data": "5.60"
                },
                {
                    "year": "2003",
                    "data": "6.10"
                },
                {
                    "year": "2002",
                    "data": "5.90"
                },
                {
                    "year": "2001",
                    "data": "4.80"
                },
                {
                    "year": "2000",
                    "data": "4.10"
                },
                {
                    "year": "1999",
                    "data": "4.30"
                },
                {
                    "year": "1998",
                    "data": "4.60"
                },
                {
                    "year": "1997",
                    "data": "5.00"
                },
                {
                    "year": "1996",
                    "data": "5.50"
                },
                {
                    "year": "1995",
                    "data": "5.70"
                },
                {
                    "year": "1994",
                    "data": "6.20"
                },
                {
                    "year": "1993",
                    "data": "7.00"
                },
                {
                    "year": "1992",
                    "data": "7.60"
                },
                {
                    "year": "1991",
                    "data": "6.90"
                }
            ]
        }
    ]



```python
data = r.json()
print(type(data))
print(data)
```

    <type 'list'>
    [{u'countryName': u'USA', u'countryCode': u'us', u'jobless_rate': [{u'data': u'6.20', u'year': u'2014'}, {u'data': u'7.40', u'year': u'2013'}, {u'data': u'8.20', u'year': u'2012'}, {u'data': u'9.00', u'year': u'2011'}, {u'data': u'9.70', u'year': u'2010'}, {u'data': u'9.40', u'year': u'2009'}, {u'data': u'5.90', u'year': u'2008'}, {u'data': u'4.70', u'year': u'2007'}, {u'data': u'4.70', u'year': u'2006'}, {u'data': u'5.20', u'year': u'2005'}, {u'data': u'5.60', u'year': u'2004'}, {u'data': u'6.10', u'year': u'2003'}, {u'data': u'5.90', u'year': u'2002'}, {u'data': u'4.80', u'year': u'2001'}, {u'data': u'4.10', u'year': u'2000'}, {u'data': u'4.30', u'year': u'1999'}, {u'data': u'4.60', u'year': u'1998'}, {u'data': u'5.00', u'year': u'1997'}, {u'data': u'5.50', u'year': u'1996'}, {u'data': u'5.70', u'year': u'1995'}, {u'data': u'6.20', u'year': u'1994'}, {u'data': u'7.00', u'year': u'1993'}, {u'data': u'7.60', u'year': u'1992'}, {u'data': u'6.90', u'year': u'1991'}]}]



```python
print(r.headers)
print(r.headers["content-type"])
```

    {'Content-Length': '258', 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding', 'Keep-Alive': 'timeout=4, max=500', 'Server': 'Apache/2.4', 'Connection': 'Keep-Alive', 'Date': 'Sat, 03 Feb 2018 23:34:44 GMT', 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json; charset=utf-8'}
    application/json; charset=utf-8



```python
#Define the target url

url="http://inqstatsapi.inqubu.com?api_key=c0081761e5b8e007&data=jobless_rate&countries=us&years=1980:2016"
```


```python
data = urllib2.urlopen(url).read()
data
```




    '[\n    {\n        "countryCode": "us",\n        "countryName": "USA",\n        "jobless_rate": [\n            {\n                "year": "2014",\n                "data": "6.20"\n            },\n            {\n                "year": "2013",\n                "data": "7.40"\n            },\n            {\n                "year": "2012",\n                "data": "8.20"\n            },\n            {\n                "year": "2011",\n                "data": "9.00"\n            },\n            {\n                "year": "2010",\n                "data": "9.70"\n            },\n            {\n                "year": "2009",\n                "data": "9.40"\n            },\n            {\n                "year": "2008",\n                "data": "5.90"\n            },\n            {\n                "year": "2007",\n                "data": "4.70"\n            },\n            {\n                "year": "2006",\n                "data": "4.70"\n            },\n            {\n                "year": "2005",\n                "data": "5.20"\n            },\n            {\n                "year": "2004",\n                "data": "5.60"\n            },\n            {\n                "year": "2003",\n                "data": "6.10"\n            },\n            {\n                "year": "2002",\n                "data": "5.90"\n            },\n            {\n                "year": "2001",\n                "data": "4.80"\n            },\n            {\n                "year": "2000",\n                "data": "4.10"\n            },\n            {\n                "year": "1999",\n                "data": "4.30"\n            },\n            {\n                "year": "1998",\n                "data": "4.60"\n            },\n            {\n                "year": "1997",\n                "data": "5.00"\n            },\n            {\n                "year": "1996",\n                "data": "5.50"\n            },\n            {\n                "year": "1995",\n                "data": "5.70"\n            },\n            {\n                "year": "1994",\n                "data": "6.20"\n            },\n            {\n                "year": "1993",\n                "data": "7.00"\n            },\n            {\n                "year": "1992",\n                "data": "7.60"\n            },\n            {\n                "year": "1991",\n                "data": "6.90"\n            }\n        ]\n    }\n]'




```python
#Convert from json format to Python dict and limit variable field

job=json.loads(data)
job=json.loads(data)[0]['jobless_rate']
job
```




    [{u'data': u'6.20', u'year': u'2014'},
     {u'data': u'7.40', u'year': u'2013'},
     {u'data': u'8.20', u'year': u'2012'},
     {u'data': u'9.00', u'year': u'2011'},
     {u'data': u'9.70', u'year': u'2010'},
     {u'data': u'9.40', u'year': u'2009'},
     {u'data': u'5.90', u'year': u'2008'},
     {u'data': u'4.70', u'year': u'2007'},
     {u'data': u'4.70', u'year': u'2006'},
     {u'data': u'5.20', u'year': u'2005'},
     {u'data': u'5.60', u'year': u'2004'},
     {u'data': u'6.10', u'year': u'2003'},
     {u'data': u'5.90', u'year': u'2002'},
     {u'data': u'4.80', u'year': u'2001'},
     {u'data': u'4.10', u'year': u'2000'},
     {u'data': u'4.30', u'year': u'1999'},
     {u'data': u'4.60', u'year': u'1998'},
     {u'data': u'5.00', u'year': u'1997'},
     {u'data': u'5.50', u'year': u'1996'},
     {u'data': u'5.70', u'year': u'1995'},
     {u'data': u'6.20', u'year': u'1994'},
     {u'data': u'7.00', u'year': u'1993'},
     {u'data': u'7.60', u'year': u'1992'},
     {u'data': u'6.90', u'year': u'1991'}]




```python
#Export data into a dataframe and print basic numbers

data = pd.DataFrame(job)
data
data.describe()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data</th>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>24</td>
      <td>24</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>21</td>
      <td>24</td>
    </tr>
    <tr>
      <th>top</th>
      <td>6.20</td>
      <td>2012</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>2</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Create a new dataframe, index and change name of the first column

dfjob=data[['data', 'year']].head(23)
dfjob.columns
dfjob.columns.values[0] = 'jobless rate'
dfjob
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>jobless rate</th>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6.20</td>
      <td>2014</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7.40</td>
      <td>2013</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8.20</td>
      <td>2012</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9.00</td>
      <td>2011</td>
    </tr>
    <tr>
      <th>4</th>
      <td>9.70</td>
      <td>2010</td>
    </tr>
    <tr>
      <th>5</th>
      <td>9.40</td>
      <td>2009</td>
    </tr>
    <tr>
      <th>6</th>
      <td>5.90</td>
      <td>2008</td>
    </tr>
    <tr>
      <th>7</th>
      <td>4.70</td>
      <td>2007</td>
    </tr>
    <tr>
      <th>8</th>
      <td>4.70</td>
      <td>2006</td>
    </tr>
    <tr>
      <th>9</th>
      <td>5.20</td>
      <td>2005</td>
    </tr>
    <tr>
      <th>10</th>
      <td>5.60</td>
      <td>2004</td>
    </tr>
    <tr>
      <th>11</th>
      <td>6.10</td>
      <td>2003</td>
    </tr>
    <tr>
      <th>12</th>
      <td>5.90</td>
      <td>2002</td>
    </tr>
    <tr>
      <th>13</th>
      <td>4.80</td>
      <td>2001</td>
    </tr>
    <tr>
      <th>14</th>
      <td>4.10</td>
      <td>2000</td>
    </tr>
    <tr>
      <th>15</th>
      <td>4.30</td>
      <td>1999</td>
    </tr>
    <tr>
      <th>16</th>
      <td>4.60</td>
      <td>1998</td>
    </tr>
    <tr>
      <th>17</th>
      <td>5.00</td>
      <td>1997</td>
    </tr>
    <tr>
      <th>18</th>
      <td>5.50</td>
      <td>1996</td>
    </tr>
    <tr>
      <th>19</th>
      <td>5.70</td>
      <td>1995</td>
    </tr>
    <tr>
      <th>20</th>
      <td>6.20</td>
      <td>1994</td>
    </tr>
    <tr>
      <th>21</th>
      <td>7.00</td>
      <td>1993</td>
    </tr>
    <tr>
      <th>22</th>
      <td>7.60</td>
      <td>1992</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Convert variable type to assign a sequence argument and plot 'year' vs 'jobless rate'

dfjob=dfjob.astype(float)
```


```python
dfjob.plot(x='year', y='jobless rate', figsize=(12, 7), kind='barh')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f8a38f6db90>




![png](MILESTONE/images/output_49_1.png)



```python
#Export data and create hv table

table = hv.Table(dfjob, 'year', 'jobless rate')
table
```




<div style='display: table; margin: 0 auto;'>

<div class="bk-root">
    <div class="bk-plotdiv" id="79f09ccc-2da8-4347-bdd0-d418e121d63a"></div>
</div>
<script type="text/javascript">
  (function(root) {
  function embed_document(root) {

  var docs_json = {"fbe32507-206b-4f29-b60b-b733e3f0fb85":{"roots":{"references":[{"attributes":{},"id":"844ebea6-787e-4ed6-88bf-138f83cd03c2","type":"StringEditor"},{"attributes":{},"id":"dc5fda9d-6657-4e7c-b530-2f7d50c03f62","type":"StringFormatter"},{"attributes":{"editor":{"id":"a2f43654-52b1-4dc9-a500-543045c000d5","type":"StringEditor"},"field":"year","formatter":{"id":"dc5fda9d-6657-4e7c-b530-2f7d50c03f62","type":"StringFormatter"},"title":"year"},"id":"bb2abfd2-8aa3-4428-9291-a24f6bca5f92","type":"TableColumn"},{"attributes":{},"id":"a2f43654-52b1-4dc9-a500-543045c000d5","type":"StringEditor"},{"attributes":{"source":{"id":"9b18ac84-9418-4682-a131-9cd605ab2948","type":"ColumnDataSource"}},"id":"0e0af664-5074-4480-a5a8-726a750cea4d","type":"CDSView"},{"attributes":{"callback":null,"column_names":["jobless rate","year"],"data":{"jobless rate":{"__ndarray__":"zczMzMzMGECamZmZmZkdQGZmZmZmZiBAAAAAAAAAIkBmZmZmZmYjQM3MzMzMzCJAmpmZmZmZF0DNzMzMzMwSQM3MzMzMzBJAzczMzMzMFEBmZmZmZmYWQGZmZmZmZhhAmpmZmZmZF0AzMzMzMzMTQGZmZmZmZhBAMzMzMzMzEUBmZmZmZmYSQAAAAAAAABRAAAAAAAAAFkDNzMzMzMwWQM3MzMzMzBhAAAAAAAAAHEBmZmZmZmYeQA==","dtype":"float64","shape":[23]},"year":{"__ndarray__":"AAAAAAB4n0AAAAAAAHSfQAAAAAAAcJ9AAAAAAABsn0AAAAAAAGifQAAAAAAAZJ9AAAAAAABgn0AAAAAAAFyfQAAAAAAAWJ9AAAAAAABUn0AAAAAAAFCfQAAAAAAATJ9AAAAAAABIn0AAAAAAAESfQAAAAAAAQJ9AAAAAAAA8n0AAAAAAADifQAAAAAAANJ9AAAAAAAAwn0AAAAAAACyfQAAAAAAAKJ9AAAAAAAAkn0AAAAAAACCfQA==","dtype":"float64","shape":[23]}}},"id":"9b18ac84-9418-4682-a131-9cd605ab2948","type":"ColumnDataSource"},{"attributes":{},"id":"512b98f5-03a3-45ed-a9e4-a6ebb68aa45a","type":"StringFormatter"},{"attributes":{"columns":[{"id":"bb2abfd2-8aa3-4428-9291-a24f6bca5f92","type":"TableColumn"},{"id":"fc2d0847-8bba-47a8-95c8-62e5031bec6f","type":"TableColumn"}],"height":300,"reorderable":false,"source":{"id":"9b18ac84-9418-4682-a131-9cd605ab2948","type":"ColumnDataSource"},"view":{"id":"0e0af664-5074-4480-a5a8-726a750cea4d","type":"CDSView"},"width":400},"id":"a8cb2a75-25a7-4d7b-ae85-093fab156b8a","type":"DataTable"},{"attributes":{"editor":{"id":"844ebea6-787e-4ed6-88bf-138f83cd03c2","type":"StringEditor"},"field":"jobless rate","formatter":{"id":"512b98f5-03a3-45ed-a9e4-a6ebb68aa45a","type":"StringFormatter"},"title":"jobless rate"},"id":"fc2d0847-8bba-47a8-95c8-62e5031bec6f","type":"TableColumn"}],"root_ids":["a8cb2a75-25a7-4d7b-ae85-093fab156b8a"]},"title":"Bokeh Application","version":"0.12.13"}};
  var render_items = [{"docid":"fbe32507-206b-4f29-b60b-b733e3f0fb85","elementid":"79f09ccc-2da8-4347-bdd0-d418e121d63a","modelid":"a8cb2a75-25a7-4d7b-ae85-093fab156b8a"}];
  root.Bokeh.embed.embed_items_notebook(docs_json, render_items);

  }
  if (root.Bokeh !== undefined) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (root.Bokeh !== undefined) {
        embed_document(root);
        clearInterval(timer);
      }
      attempts++;
      if (attempts > 100) {
        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing")
        clearInterval(timer);
      }
    }, 10, root)
  }
})(window);
</script>
</div>




```python
#Create interactive plot using holoviews

hv.Curve(table) + hv.Bars(table)
```




<div style='display: table; margin: 0 auto;'>

<div class="bk-root">
    <div class="bk-plotdiv" id="ae5adb52-10c9-48cb-b0a6-c91643f32beb"></div>
</div>
<script type="text/javascript">
  (function(root) {
  function embed_document(root) {

  var docs_json = {"2cd40ee3-b36c-40ba-8c66-1c049175de10":{"roots":{"references":[{"attributes":{},"id":"a5aa2fca-6466-46b7-9b8e-79e500e5bba5","type":"ResetTool"},{"attributes":{"axis_label":"jobless rate","bounds":"auto","formatter":{"id":"d789319d-3c54-4623-bbc2-c04e2c9e8636","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"7fd6d504-07ab-4e61-a247-d11d531afef8","subtype":"Figure","type":"Plot"},"ticker":{"id":"14c974d0-7018-424d-b0cc-e00ae1c2a593","type":"BasicTicker"}},"id":"3de56ccb-9ba8-4621-8abe-136b0e961180","type":"LinearAxis"},{"attributes":{},"id":"14c974d0-7018-424d-b0cc-e00ae1c2a593","type":"BasicTicker"},{"attributes":{"toolbar":{"id":"c7eebb77-331c-4545-b26b-1ac69e79fa8b","type":"ProxyToolbar"},"toolbar_location":"above"},"id":"0a211ee8-11f2-4d05-9454-98275c9cf64e","type":"ToolbarBox"},{"attributes":{},"id":"92ae14dc-291f-447d-bf84-4ea36c46e20f","type":"ResetTool"},{"attributes":{"overlay":{"id":"08f12633-2819-49bf-aeca-55b221b2a29a","type":"BoxAnnotation"}},"id":"d8e91f40-ee3c-44d3-95b3-a0e7e3aa9270","type":"BoxZoomTool"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"b99c2a7e-40da-4a1f-a9d6-a72fc877bbeb","type":"LinearAxis"}],"left":[{"id":"87ab3bc5-2e59-4352-a0d6-d653eb9eed58","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"plot_width":300,"renderers":[{"id":"b99c2a7e-40da-4a1f-a9d6-a72fc877bbeb","type":"LinearAxis"},{"id":"75424002-0964-4442-b7b6-94ab5685f184","type":"Grid"},{"id":"87ab3bc5-2e59-4352-a0d6-d653eb9eed58","type":"LinearAxis"},{"id":"47194b83-0ab4-4793-9637-081cab6f463c","type":"Grid"},{"id":"3dddf5c2-de5b-41e7-8cab-33468582a407","type":"BoxAnnotation"},{"id":"426e493b-e9c3-4980-af05-f09adb7e880f","type":"GlyphRenderer"}],"title":{"id":"5f3d1628-eda7-4c92-b5b0-3e11ce1aaf8f","type":"Title"},"toolbar":{"id":"652795ae-07a6-46a3-8cc8-15f1e2b43f89","type":"Toolbar"},"toolbar_location":null,"x_range":{"id":"e70604cb-5195-491f-a603-5c36827a0099","type":"Range1d"},"x_scale":{"id":"1589f9a2-4cf7-4d0c-b024-cffeafa0583e","type":"LinearScale"},"y_range":{"id":"00957d9e-cbb8-49a6-97a0-3ffca4f8a974","type":"Range1d"},"y_scale":{"id":"d5930f8a-ace3-41ab-88a3-ead0e93624ba","type":"LinearScale"}},"id":"0ee4afe8-92a5-43ee-854e-caf2d7143b49","subtype":"Figure","type":"Plot"},{"attributes":{"line_alpha":0.1,"line_color":"#30a2da","line_width":2,"x":{"field":"year"},"y":{"field":"jobless rate"}},"id":"2c440dba-3ba3-490a-baf7-f4806f59db48","type":"Line"},{"attributes":{},"id":"bdfb82b0-6573-4ce3-a707-7e8be939f3db","type":"CategoricalScale"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"50ed37fc-365f-4c9c-8aab-0f9b7a320b07","type":"Title"},{"attributes":{"children":[{"id":"0a211ee8-11f2-4d05-9454-98275c9cf64e","type":"ToolbarBox"},{"id":"22325673-528b-4b07-91b1-ab87b04d01b4","type":"Column"}]},"id":"f31b25b8-9038-45ed-8953-d9d3a65741d8","type":"Column"},{"attributes":{"axis_label":"jobless rate","bounds":"auto","formatter":{"id":"32942be8-0050-4f7d-8cff-d1be62b14070","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"0ee4afe8-92a5-43ee-854e-caf2d7143b49","subtype":"Figure","type":"Plot"},"ticker":{"id":"2fbc0361-d3a5-4756-bae6-3c9fcc596960","type":"BasicTicker"}},"id":"87ab3bc5-2e59-4352-a0d6-d653eb9eed58","type":"LinearAxis"},{"attributes":{},"id":"1e85e4b5-03b0-4847-9c70-651b2599348b","type":"SaveTool"},{"attributes":{"data_source":{"id":"8146b45d-3c9b-477c-b1a9-f3e456055a4a","type":"ColumnDataSource"},"glyph":{"id":"f844e221-14e0-4460-b253-adc257ddc8ce","type":"VBar"},"hover_glyph":null,"muted_glyph":null,"nonselection_glyph":{"id":"65810800-414a-4e4f-8439-703a5f6238dc","type":"VBar"},"selection_glyph":null,"view":{"id":"24c9dff4-c6f2-4295-a307-f47a8148b216","type":"CDSView"}},"id":"d613d55e-47fd-4811-a1c7-512af997c8e8","type":"GlyphRenderer"},{"attributes":{},"id":"32942be8-0050-4f7d-8cff-d1be62b14070","type":"BasicTickFormatter"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"7fd6d504-07ab-4e61-a247-d11d531afef8","subtype":"Figure","type":"Plot"},"ticker":{"id":"b250fc2a-3c3b-4a32-9994-0a1cf15bb4a7","type":"CategoricalTicker"}},"id":"55abe363-5ba3-43ad-b828-24c9e9b5f61d","type":"Grid"},{"attributes":{"line_color":"#30a2da","line_width":2,"x":{"field":"year"},"y":{"field":"jobless rate"}},"id":"3e295c48-51a2-4ca5-be4a-d067359ff193","type":"Line"},{"attributes":{},"id":"2fbc0361-d3a5-4756-bae6-3c9fcc596960","type":"BasicTicker"},{"attributes":{"callback":null,"factors":["2014","2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000","1999","1998","1997","1996","1995","1994","1993","1992"]},"id":"984d166d-2954-425c-a1c8-4f8e18df210c","type":"FactorRange"},{"attributes":{"data_source":{"id":"108ce991-f64e-4de7-aae7-9210d379519c","type":"ColumnDataSource"},"glyph":{"id":"3e295c48-51a2-4ca5-be4a-d067359ff193","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"2fb5d06a-95d9-4f84-a0f0-8eee50eb6ea6","type":"Line"},"nonselection_glyph":{"id":"2c440dba-3ba3-490a-baf7-f4806f59db48","type":"Line"},"selection_glyph":null,"view":{"id":"1aef9c02-f4ac-4a7f-bd02-57a6b198e8ad","type":"CDSView"}},"id":"426e493b-e9c3-4980-af05-f09adb7e880f","type":"GlyphRenderer"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"value":"#30a2da"},"line_alpha":{"value":0.1},"line_color":{"value":"#000000"},"top":{"field":"jobless_rate"},"width":{"value":0.8},"x":{"field":"year"}},"id":"65810800-414a-4e4f-8439-703a5f6238dc","type":"VBar"},{"attributes":{},"id":"24b8fb59-b583-4f68-be5d-40e78b4c8249","type":"PanTool"},{"attributes":{"fill_color":{"value":"#30a2da"},"line_color":{"value":"#000000"},"top":{"field":"jobless_rate"},"width":{"value":0.8},"x":{"field":"year"}},"id":"f844e221-14e0-4460-b253-adc257ddc8ce","type":"VBar"},{"attributes":{},"id":"fafa6830-cbab-4489-8615-a86ebb797953","type":"PanTool"},{"attributes":{},"id":"56f18be3-a1f6-4f01-abd3-b026008f0ae0","type":"WheelZoomTool"},{"attributes":{"callback":null,"column_names":["jobless rate","year"],"data":{"jobless rate":{"__ndarray__":"zczMzMzMGECamZmZmZkdQGZmZmZmZiBAAAAAAAAAIkBmZmZmZmYjQM3MzMzMzCJAmpmZmZmZF0DNzMzMzMwSQM3MzMzMzBJAzczMzMzMFEBmZmZmZmYWQGZmZmZmZhhAmpmZmZmZF0AzMzMzMzMTQGZmZmZmZhBAMzMzMzMzEUBmZmZmZmYSQAAAAAAAABRAAAAAAAAAFkDNzMzMzMwWQM3MzMzMzBhAAAAAAAAAHEBmZmZmZmYeQA==","dtype":"float64","shape":[23]},"year":{"__ndarray__":"AAAAAAB4n0AAAAAAAHSfQAAAAAAAcJ9AAAAAAABsn0AAAAAAAGifQAAAAAAAZJ9AAAAAAABgn0AAAAAAAFyfQAAAAAAAWJ9AAAAAAABUn0AAAAAAAFCfQAAAAAAATJ9AAAAAAABIn0AAAAAAAESfQAAAAAAAQJ9AAAAAAAA8n0AAAAAAADifQAAAAAAANJ9AAAAAAAAwn0AAAAAAACyfQAAAAAAAKJ9AAAAAAAAkn0AAAAAAACCfQA==","dtype":"float64","shape":[23]}}},"id":"108ce991-f64e-4de7-aae7-9210d379519c","type":"ColumnDataSource"},{"attributes":{"callback":null,"end":9.7,"start":0.0},"id":"00957d9e-cbb8-49a6-97a0-3ffca4f8a974","type":"Range1d"},{"attributes":{"source":{"id":"108ce991-f64e-4de7-aae7-9210d379519c","type":"ColumnDataSource"}},"id":"1aef9c02-f4ac-4a7f-bd02-57a6b198e8ad","type":"CDSView"},{"attributes":{},"id":"dff05ea5-ca57-4d22-b3d3-3a8673c8dd98","type":"WheelZoomTool"},{"attributes":{"children":[{"id":"0ee4afe8-92a5-43ee-854e-caf2d7143b49","subtype":"Figure","type":"Plot"},{"id":"7fd6d504-07ab-4e61-a247-d11d531afef8","subtype":"Figure","type":"Plot"}]},"id":"8be9b300-571f-463b-b70e-af8b3efb22e9","type":"Row"},{"attributes":{"line_alpha":0.2,"line_color":"#30a2da","line_width":2,"x":{"field":"year"},"y":{"field":"jobless rate"}},"id":"2fb5d06a-95d9-4f84-a0f0-8eee50eb6ea6","type":"Line"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"1e85e4b5-03b0-4847-9c70-651b2599348b","type":"SaveTool"},{"id":"fafa6830-cbab-4489-8615-a86ebb797953","type":"PanTool"},{"id":"56f18be3-a1f6-4f01-abd3-b026008f0ae0","type":"WheelZoomTool"},{"id":"fc735677-f56f-47de-ba14-d6639317da40","type":"BoxZoomTool"},{"id":"92ae14dc-291f-447d-bf84-4ea36c46e20f","type":"ResetTool"}]},"id":"652795ae-07a6-46a3-8cc8-15f1e2b43f89","type":"Toolbar"},{"attributes":{"callback":null,"column_names":["year","jobless_rate"],"data":{"jobless_rate":{"__ndarray__":"zczMzMzMGECamZmZmZkdQGZmZmZmZiBAAAAAAAAAIkBmZmZmZmYjQM3MzMzMzCJAmpmZmZmZF0DNzMzMzMwSQM3MzMzMzBJAzczMzMzMFEBmZmZmZmYWQGZmZmZmZhhAmpmZmZmZF0AzMzMzMzMTQGZmZmZmZhBAMzMzMzMzEUBmZmZmZmYSQAAAAAAAABRAAAAAAAAAFkDNzMzMzMwWQM3MzMzMzBhAAAAAAAAAHEBmZmZmZmYeQA==","dtype":"float64","shape":[23]},"year":["2014","2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000","1999","1998","1997","1996","1995","1994","1993","1992"]}},"id":"8146b45d-3c9b-477c-b1a9-f3e456055a4a","type":"ColumnDataSource"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"08f12633-2819-49bf-aeca-55b221b2a29a","type":"BoxAnnotation"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"0ee4afe8-92a5-43ee-854e-caf2d7143b49","subtype":"Figure","type":"Plot"},"ticker":{"id":"2fbc0361-d3a5-4756-bae6-3c9fcc596960","type":"BasicTicker"}},"id":"47194b83-0ab4-4793-9637-081cab6f463c","type":"Grid"},{"attributes":{"source":{"id":"8146b45d-3c9b-477c-b1a9-f3e456055a4a","type":"ColumnDataSource"}},"id":"24c9dff4-c6f2-4295-a307-f47a8148b216","type":"CDSView"},{"attributes":{"callback":null,"end":2014.0,"start":1992.0},"id":"e70604cb-5195-491f-a603-5c36827a0099","type":"Range1d"},{"attributes":{"tools":[{"id":"1e85e4b5-03b0-4847-9c70-651b2599348b","type":"SaveTool"},{"id":"fafa6830-cbab-4489-8615-a86ebb797953","type":"PanTool"},{"id":"56f18be3-a1f6-4f01-abd3-b026008f0ae0","type":"WheelZoomTool"},{"id":"fc735677-f56f-47de-ba14-d6639317da40","type":"BoxZoomTool"},{"id":"92ae14dc-291f-447d-bf84-4ea36c46e20f","type":"ResetTool"},{"id":"fd945d2d-2575-4312-95a7-3c0df39f5665","type":"SaveTool"},{"id":"24b8fb59-b583-4f68-be5d-40e78b4c8249","type":"PanTool"},{"id":"dff05ea5-ca57-4d22-b3d3-3a8673c8dd98","type":"WheelZoomTool"},{"id":"d8e91f40-ee3c-44d3-95b3-a0e7e3aa9270","type":"BoxZoomTool"},{"id":"a5aa2fca-6466-46b7-9b8e-79e500e5bba5","type":"ResetTool"}]},"id":"c7eebb77-331c-4545-b26b-1ac69e79fa8b","type":"ProxyToolbar"},{"attributes":{"axis_label":"year","bounds":"auto","formatter":{"id":"08461bc6-e9c7-4ac5-9a12-d7be827c2c30","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"7fd6d504-07ab-4e61-a247-d11d531afef8","subtype":"Figure","type":"Plot"},"ticker":{"id":"b250fc2a-3c3b-4a32-9994-0a1cf15bb4a7","type":"CategoricalTicker"}},"id":"62dbaba9-c3cc-44fd-9748-6f3a4eae5bc7","type":"CategoricalAxis"},{"attributes":{},"id":"d5930f8a-ace3-41ab-88a3-ead0e93624ba","type":"LinearScale"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"0ee4afe8-92a5-43ee-854e-caf2d7143b49","subtype":"Figure","type":"Plot"},"ticker":{"id":"65388074-15e0-42b4-807a-478dd2838cc7","type":"BasicTicker"}},"id":"75424002-0964-4442-b7b6-94ab5685f184","type":"Grid"},{"attributes":{},"id":"946159cd-b37a-4e08-a397-b20cef2874af","type":"LinearScale"},{"attributes":{},"id":"d789319d-3c54-4623-bbc2-c04e2c9e8636","type":"BasicTickFormatter"},{"attributes":{"overlay":{"id":"3dddf5c2-de5b-41e7-8cab-33468582a407","type":"BoxAnnotation"}},"id":"fc735677-f56f-47de-ba14-d6639317da40","type":"BoxZoomTool"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"7fd6d504-07ab-4e61-a247-d11d531afef8","subtype":"Figure","type":"Plot"},"ticker":{"id":"14c974d0-7018-424d-b0cc-e00ae1c2a593","type":"BasicTicker"}},"id":"4deb2344-4a9e-4da1-b179-69dc7c2396a4","type":"Grid"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"3dddf5c2-de5b-41e7-8cab-33468582a407","type":"BoxAnnotation"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"62dbaba9-c3cc-44fd-9748-6f3a4eae5bc7","type":"CategoricalAxis"}],"left":[{"id":"3de56ccb-9ba8-4621-8abe-136b0e961180","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"plot_width":300,"renderers":[{"id":"62dbaba9-c3cc-44fd-9748-6f3a4eae5bc7","type":"CategoricalAxis"},{"id":"55abe363-5ba3-43ad-b828-24c9e9b5f61d","type":"Grid"},{"id":"3de56ccb-9ba8-4621-8abe-136b0e961180","type":"LinearAxis"},{"id":"4deb2344-4a9e-4da1-b179-69dc7c2396a4","type":"Grid"},{"id":"08f12633-2819-49bf-aeca-55b221b2a29a","type":"BoxAnnotation"},{"id":"d613d55e-47fd-4811-a1c7-512af997c8e8","type":"GlyphRenderer"}],"title":{"id":"50ed37fc-365f-4c9c-8aab-0f9b7a320b07","type":"Title"},"toolbar":{"id":"15618623-eb10-4eb2-8554-444d7b6a3d63","type":"Toolbar"},"toolbar_location":null,"x_range":{"id":"984d166d-2954-425c-a1c8-4f8e18df210c","type":"FactorRange"},"x_scale":{"id":"bdfb82b0-6573-4ce3-a707-7e8be939f3db","type":"CategoricalScale"},"y_range":{"id":"00957d9e-cbb8-49a6-97a0-3ffca4f8a974","type":"Range1d"},"y_scale":{"id":"946159cd-b37a-4e08-a397-b20cef2874af","type":"LinearScale"}},"id":"7fd6d504-07ab-4e61-a247-d11d531afef8","subtype":"Figure","type":"Plot"},{"attributes":{"children":[{"id":"8be9b300-571f-463b-b70e-af8b3efb22e9","type":"Row"}]},"id":"22325673-528b-4b07-91b1-ab87b04d01b4","type":"Column"},{"attributes":{},"id":"c67abd55-5161-4ae2-9009-6278381795f0","type":"BasicTickFormatter"},{"attributes":{"axis_label":"year","bounds":"auto","formatter":{"id":"c67abd55-5161-4ae2-9009-6278381795f0","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"0ee4afe8-92a5-43ee-854e-caf2d7143b49","subtype":"Figure","type":"Plot"},"ticker":{"id":"65388074-15e0-42b4-807a-478dd2838cc7","type":"BasicTicker"}},"id":"b99c2a7e-40da-4a1f-a9d6-a72fc877bbeb","type":"LinearAxis"},{"attributes":{},"id":"fd945d2d-2575-4312-95a7-3c0df39f5665","type":"SaveTool"},{"attributes":{},"id":"08461bc6-e9c7-4ac5-9a12-d7be827c2c30","type":"CategoricalTickFormatter"},{"attributes":{},"id":"1589f9a2-4cf7-4d0c-b024-cffeafa0583e","type":"LinearScale"},{"attributes":{},"id":"b250fc2a-3c3b-4a32-9994-0a1cf15bb4a7","type":"CategoricalTicker"},{"attributes":{},"id":"65388074-15e0-42b4-807a-478dd2838cc7","type":"BasicTicker"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"fd945d2d-2575-4312-95a7-3c0df39f5665","type":"SaveTool"},{"id":"24b8fb59-b583-4f68-be5d-40e78b4c8249","type":"PanTool"},{"id":"dff05ea5-ca57-4d22-b3d3-3a8673c8dd98","type":"WheelZoomTool"},{"id":"d8e91f40-ee3c-44d3-95b3-a0e7e3aa9270","type":"BoxZoomTool"},{"id":"a5aa2fca-6466-46b7-9b8e-79e500e5bba5","type":"ResetTool"}]},"id":"15618623-eb10-4eb2-8554-444d7b6a3d63","type":"Toolbar"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"5f3d1628-eda7-4c92-b5b0-3e11ce1aaf8f","type":"Title"}],"root_ids":["f31b25b8-9038-45ed-8953-d9d3a65741d8"]},"title":"Bokeh Application","version":"0.12.13"}};
  var render_items = [{"docid":"2cd40ee3-b36c-40ba-8c66-1c049175de10","elementid":"ae5adb52-10c9-48cb-b0a6-c91643f32beb","modelid":"f31b25b8-9038-45ed-8953-d9d3a65741d8"}];
  root.Bokeh.embed.embed_items_notebook(docs_json, render_items);

  }
  if (root.Bokeh !== undefined) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (root.Bokeh !== undefined) {
        embed_document(root);
        clearInterval(timer);
      }
      attempts++;
      if (attempts > 100) {
        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing")
        clearInterval(timer);
      }
    }, 10, root)
  }
})(window);
</script>
</div>




```python
#################################################################################################################################
################################################ MILESTONE PROJECT - PART 3 ######################################################

#1. Request API of stock ticker prices from Quandle WIKI dataset (two approaches with and without selection filters applied)
#2. Convert jSon data to Pandas dataframe
#3. Create two separate dataframes, one for closing prices per ticker and another one for closing, opening, adjusted closing and adjusted openening prices per ticker
#4. Analyze prices data since last month
#5. Create table and plot data (Bokeh, Holoviews)

```


```python
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144
import pandas as pd
import numpy as np
```


```python
import simplejson as json
import urllib2
import requests
import ujson as json
```


```python
from bokeh.plotting import figure, show, output_notebook
from bokeh.resources import CDN
from bokeh.embed import file_html
from ipywidgets import interact
from bokeh.io import push_notebook
from matplotlib import cm
import holoviews as hv
hv.extension('bokeh', 'matplotlib')
```





<script src="https://code.jquery.com/ui/1.10.4/jquery-ui.min.js" type="text/javascript"></script>
<script type="text/javascript">function HoloViewsWidget(){
}

HoloViewsWidget.comms = {};
HoloViewsWidget.comm_state = {};

HoloViewsWidget.prototype.init_slider = function(init_val){
  if(this.load_json) {
    this.from_json()
  } else {
    this.update_cache();
  }
}

HoloViewsWidget.prototype.populate_cache = function(idx){
  this.cache[idx].html(this.frames[idx]);
  if (this.embed) {
    delete this.frames[idx];
  }
}

HoloViewsWidget.prototype.process_error = function(msg){

}

HoloViewsWidget.prototype.from_json = function() {
  var data_url = this.json_path + this.id + '.json';
  $.getJSON(data_url, $.proxy(function(json_data) {
    this.frames = json_data;
    this.update_cache();
    this.update(0);
  }, this));
}

HoloViewsWidget.prototype.dynamic_update = function(current){
  if (current === undefined) {
    return
  }
  if(this.dynamic) {
    current = JSON.stringify(current);
  }
  function callback(initialized, msg){
    /* This callback receives data from Python as a string
       in order to parse it correctly quotes are sliced off*/
    if (msg.content.ename != undefined) {
      this.process_error(msg);
    }
    if (msg.msg_type != "execute_result") {
      console.log("Warning: HoloViews callback returned unexpected data for key: (", current, ") with the following content:", msg.content)
    } else {
      if (msg.content.data['text/plain'].includes('Complete')) {
        if (this.queue.length > 0) {
          this.time = Date.now();
          this.dynamic_update(this.queue[this.queue.length-1]);
          this.queue = [];
        } else {
          this.wait = false;
        }
        return
      }
    }
  }
  this.current = current;
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null)) {
    var kernel = Jupyter.notebook.kernel;
    callbacks = {iopub: {output: $.proxy(callback, this, this.initialized)}};
    var cmd = "holoviews.plotting.widgets.NdWidget.widgets['" + this.id + "'].update(" + current + ")";
    kernel.execute("import holoviews;" + cmd, callbacks, {silent : false});
  }
}

HoloViewsWidget.prototype.update_cache = function(force){
  var frame_len = Object.keys(this.frames).length;
  for (var i=0; i<frame_len; i++) {
    if(!this.load_json || this.dynamic)  {
      frame = Object.keys(this.frames)[i];
    } else {
      frame = i;
    }
    if(!(frame in this.cache) || force) {
      if ((frame in this.cache) && force) { this.cache[frame].remove() }
      this.cache[frame] = $('<div />').appendTo("#"+"_anim_img"+this.id).hide();
      var cache_id = "_anim_img"+this.id+"_"+frame;
      this.cache[frame].attr("id", cache_id);
      this.populate_cache(frame);
    }
  }
}

HoloViewsWidget.prototype.update = function(current){
  if(current in this.cache) {
    $.each(this.cache, function(index, value) {
      value.hide();
    });
    this.cache[current].show();
    this.wait = false;
  }
}

HoloViewsWidget.prototype.init_comms = function() {
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel !== undefined)) {
    var widget = this;
    comm_manager = Jupyter.notebook.kernel.comm_manager;
    comm_manager.register_target(this.id, function (comm) {
      comm.on_msg(function (msg) { widget.process_msg(msg) });
    });
  }
}

HoloViewsWidget.prototype.process_msg = function(msg) {
}

function SelectionWidget(frames, id, slider_ids, keyMap, dim_vals, notFound, load_json, mode, cached, json_path, dynamic){
  this.frames = frames;
  this.id = id;
  this.slider_ids = slider_ids;
  this.keyMap = keyMap
  this.current_frame = 0;
  this.current_vals = dim_vals;
  this.load_json = load_json;
  this.mode = mode;
  this.notFound = notFound;
  this.cached = cached;
  this.dynamic = dynamic;
  this.cache = {};
  this.json_path = json_path;
  this.init_slider(this.current_vals[0]);
  this.queue = [];
  this.wait = false;
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

SelectionWidget.prototype = new HoloViewsWidget;


SelectionWidget.prototype.get_key = function(current_vals) {
  var key = "(";
  for (var i=0; i<this.slider_ids.length; i++)
  {
    val = this.current_vals[i];
    if (!(typeof val === 'string')) {
      if (val % 1 === 0) { val = val.toFixed(1); }
      else { val = val.toFixed(10); val = val.slice(0, val.length-1);}
    }
    key += "'" + val + "'";
    if(i != this.slider_ids.length-1) { key += ', ';}
    else if(this.slider_ids.length == 1) { key += ',';}
  }
  key += ")";
  return this.keyMap[key];
}

SelectionWidget.prototype.set_frame = function(dim_val, dim_idx){
  this.current_vals[dim_idx] = dim_val;
  var key = this.current_vals;
  if (!this.dynamic) {
    key = this.get_key(key)
  }
  if (this.dynamic || !this.cached) {
    if ((this.time !== undefined) && ((this.wait) && ((this.time + 10000) > Date.now()))) {
      this.queue.push(key);
      return
    }
    this.queue = [];
    this.time = Date.now();
    this.current_frame = key;
    this.wait = true;
    this.dynamic_update(key)
  } else if (key !== undefined) {
    this.update(key)
  }
}


/* Define the ScrubberWidget class */
function ScrubberWidget(frames, num_frames, id, interval, load_json, mode, cached, json_path, dynamic){
  this.slider_id = "_anim_slider" + id;
  this.loop_select_id = "_anim_loop_select" + id;
  this.id = id;
  this.interval = interval;
  this.current_frame = 0;
  this.direction = 0;
  this.dynamic = dynamic;
  this.timer = null;
  this.load_json = load_json;
  this.mode = mode;
  this.cached = cached;
  this.frames = frames;
  this.cache = {};
  this.length = num_frames;
  this.json_path = json_path;
  document.getElementById(this.slider_id).max = this.length - 1;
  this.init_slider(0);
  this.wait = false;
  this.queue = [];
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

ScrubberWidget.prototype = new HoloViewsWidget;

ScrubberWidget.prototype.set_frame = function(frame){
  this.current_frame = frame;
  widget = document.getElementById(this.slider_id);
  if (widget === null) {
    this.pause_animation();
    return
  }
  widget.value = this.current_frame;
  if(this.cached) {
    this.update(frame)
  } else {
    this.dynamic_update(frame)
  }
}


ScrubberWidget.prototype.get_loop_state = function(){
  var button_group = document[this.loop_select_id].state;
  for (var i = 0; i < button_group.length; i++) {
    var button = button_group[i];
    if (button.checked) {
      return button.value;
    }
  }
  return undefined;
}


ScrubberWidget.prototype.next_frame = function() {
  this.set_frame(Math.min(this.length - 1, this.current_frame + 1));
}

ScrubberWidget.prototype.previous_frame = function() {
  this.set_frame(Math.max(0, this.current_frame - 1));
}

ScrubberWidget.prototype.first_frame = function() {
  this.set_frame(0);
}

ScrubberWidget.prototype.last_frame = function() {
  this.set_frame(this.length - 1);
}

ScrubberWidget.prototype.slower = function() {
  this.interval /= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.faster = function() {
  this.interval *= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.anim_step_forward = function() {
  if(this.current_frame < this.length - 1){
    this.next_frame();
  }else{
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.first_frame();
    }else if(loop_state == "reflect"){
      this.last_frame();
      this.reverse_animation();
    }else{
      this.pause_animation();
      this.last_frame();
    }
  }
}

ScrubberWidget.prototype.anim_step_reverse = function() {
  if(this.current_frame > 0){
    this.previous_frame();
  } else {
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.last_frame();
    }else if(loop_state == "reflect"){
      this.first_frame();
      this.play_animation();
    }else{
      this.pause_animation();
      this.first_frame();
    }
  }
}

ScrubberWidget.prototype.pause_animation = function() {
  this.direction = 0;
  if (this.timer){
    clearInterval(this.timer);
    this.timer = null;
  }
}

ScrubberWidget.prototype.play_animation = function() {
  this.pause_animation();
  this.direction = 1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_forward();}, this.interval);
}

ScrubberWidget.prototype.reverse_animation = function() {
  this.pause_animation();
  this.direction = -1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_reverse();}, this.interval);
}

function extend(destination, source) {
  for (var k in source) {
    if (source.hasOwnProperty(k)) {
      destination[k] = source[k];
    }
  }
  return destination;
}

function update_widget(widget, values) {
  if (widget.hasClass("ui-slider")) {
    widget.slider('option', {
      min: 0,
      max: values.length-1,
      dim_vals: values,
      value: 0,
      dim_labels: values
	})
    widget.slider('option', 'slide').call(widget, event, {value: 0})
  } else {
    widget.empty();
    for (var i=0; i<values.length; i++){
      widget.append($("<option>", {
        value: i,
        text: values[i]
      }))
    };
    widget.data('values', values);
    widget.data('value', 0);
    widget.trigger("change");
  };
}

// Define MPL specific subclasses
function MPLSelectionWidget() {
    SelectionWidget.apply(this, arguments);
}

function MPLScrubberWidget() {
    ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
MPLSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
MPLScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var MPLMethods = {
    init_slider : function(init_val){
        if(this.load_json) {
            this.from_json()
        } else {
            this.update_cache();
        }
        this.update(0);
        if(this.mode == 'nbagg') {
            this.set_frame(init_val, 0);
        }
    },
    populate_cache : function(idx){
        var cache_id = "_anim_img"+this.id+"_"+idx;
        this.cache[idx].html(this.frames[idx]);
        if (this.embed) {
            delete this.frames[idx];
        }
    },
    process_msg : function(msg) {
        if (!(this.mode == 'nbagg')) {
            var data = msg.content.data;
            this.frames[this.current] = data;
            this.update_cache(true);
            this.update(this.current);
        }
    }
}
// Extend MPL widgets with backend specific methods
extend(MPLSelectionWidget.prototype, MPLMethods);
extend(MPLScrubberWidget.prototype, MPLMethods);

// Define Bokeh specific subclasses
function BokehSelectionWidget() {
	SelectionWidget.apply(this, arguments);
}

function BokehScrubberWidget() {
	ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
BokehSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
BokehScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var BokehMethods = {
	update_cache : function(){
		$.each(this.frames, $.proxy(function(index, frame) {
			this.frames[index] = JSON.parse(frame);
		}, this));
	},
	update : function(current){
		if (current === undefined) {
			var data = undefined;
		} else {
			var data = this.frames[current];
		}
		if (data !== undefined) {
			var doc = Bokeh.index[data.root].model.document;
			doc.apply_json_patch(data.content);
		}
	},
	init_comms : function() {
	}
}

// Extend Bokeh widgets with backend specific methods
extend(BokehSelectionWidget.prototype, BokehMethods);
extend(BokehScrubberWidget.prototype, BokehMethods);
</script>


<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<style>div.hololayout {
    display: flex;
    align-items: center;
    margin: 0;
}

div.holoframe {
	width: 75%;
}

div.holowell {
    display: flex;
    align-items: center;
    margin: 0;
}

form.holoform {
    background-color: #fafafa;
    border-radius: 5px;
    overflow: hidden;
	padding-left: 0.8em;
    padding-right: 0.8em;
    padding-top: 0.4em;
    padding-bottom: 0.4em;
}

div.holowidgets {
    padding-right: 0;
	width: 25%;
}

div.holoslider {
    min-height: 0 !important;
    height: 0.8em;
    width: 60%;
}

div.holoformgroup {
    padding-top: 0.5em;
    margin-bottom: 0.5em;
}

div.hologroup {
    padding-left: 0;
    padding-right: 0.8em;
    width: 50%;
}

.holoselect {
    width: 92%;
    margin-left: 0;
    margin-right: 0;
}

.holotext {
    width: 100%;
    padding-left:  0.5em;
    padding-right: 0;
}

.holowidgets .ui-resizable-se {
	visibility: hidden
}

.holoframe > .ui-resizable-se {
	visibility: hidden
}

.holowidgets .ui-resizable-s {
	visibility: hidden
}

div.bk-hbox {
    display: flex;
    justify-content: center;
}

div.bk-hbox div.bk-plot {
    padding: 8px;
}

div.bk-hbox div.bk-data-table {
    padding: 20px;
}
</style>


<div class="logo-block">
<img src='data:image/png;base64,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
roTBs2RqAAAAAElFTkSuQmCC'
     style='height:25px; border-radius:12px; display: inline-block; float: left; vertical-align: middle'></img>


  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



</div>




```python
#################################################################################################################################
#3.1. GENERAL API REQUEST
```


```python
#Set url

url="https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=MhSyqwHb1N6rn5JiB7QF"
```


```python
#Search request of ticker prices

r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=MhSyqwHb1N6rn5JiB7QF')
r
```




    <Response [200]>




```python
#Return json file as python dict

ticker = r.json()
ticker
```




    {u'datatable': {u'columns': [{u'name': u'ticker', u'type': u'String'},
       {u'name': u'date', u'type': u'Date'},
       {u'name': u'open', u'type': u'BigDecimal(34,12)'},
       {u'name': u'high', u'type': u'BigDecimal(34,12)'},
       {u'name': u'low', u'type': u'BigDecimal(34,12)'},
       {u'name': u'close', u'type': u'BigDecimal(34,12)'},
       {u'name': u'volume', u'type': u'BigDecimal(37,15)'},
       {u'name': u'ex-dividend', u'type': u'BigDecimal(42,20)'},
       {u'name': u'split_ratio', u'type': u'double'},
       {u'name': u'adj_open', u'type': u'BigDecimal(50,28)'},
       {u'name': u'adj_high', u'type': u'BigDecimal(50,28)'},
       {u'name': u'adj_low', u'type': u'BigDecimal(50,28)'},
       {u'name': u'adj_close', u'type': u'BigDecimal(50,28)'},
       {u'name': u'adj_volume', u'type': u'double'}],
      u'data': [[u'A',
        u'1999-11-18',
        45.5,
        50.0,
        40.0,
        44.0,
        44739900.0,
        0.0,
        1.0,
        31.041951216877,
        34.112034304261,
        27.289627443409,
        30.018590187749,
        44739900.0],
       [u'A',
        u'1999-11-19',
        42.94,
        43.0,
        39.81,
        40.38,
        10897100.0,
        0.0,
        1.0,
        29.295415060499,
        29.336349501664,
        27.160001713052,
        27.548878904121,
        10897100.0],
       [u'A',
        u'1999-11-22',
        41.31,
        44.0,
        40.06,
        44.0,
        4705200.0,
        0.0,
        1.0,
        28.18336274218,
        30.018590187749,
        27.330561884574,
        30.018590187749,
        4705200.0],
       [u'A',
        u'1999-11-23',
        42.5,
        43.63,
        40.25,
        40.25,
        4274400.0,
        0.0,
        1.0,
        28.995229158622,
        29.766161133898,
        27.46018761493,
        27.46018761493,
        4274400.0],
       [u'A',
        u'1999-11-24',
        40.13,
        41.94,
        40.0,
        41.06,
        3464400.0,
        0.0,
        1.0,
        27.3783187326,
        28.613174374414,
        27.289627443409,
        28.012802570659,
        3464400.0],
       [u'A',
        u'1999-11-26',
        40.88,
        41.5,
        40.75,
        41.19,
        1237100.0,
        0.0,
        1.0,
        27.889999247164,
        28.312988472536,
        27.801307957973,
        28.10149385985,
        1237100.0],
       [u'A',
        u'1999-11-29',
        41.0,
        42.44,
        40.56,
        42.13,
        2914700.0,
        0.0,
        1.0,
        27.971868129494,
        28.954294717457,
        27.671682227616,
        28.74280010477,
        2914700.0],
       [u'A',
        u'1999-11-30',
        42.0,
        42.94,
        40.94,
        42.19,
        3083000.0,
        0.0,
        1.0,
        28.654108815579,
        29.295415060499,
        27.930933688329,
        28.783734545935,
        3083000.0],
       [u'A',
        u'1999-12-01',
        42.19,
        43.44,
        41.88,
        42.94,
        2115400.0,
        0.0,
        1.0,
        28.783734545935,
        29.636535403542,
        28.572239933249,
        29.295415060499,
        2115400.0],
       [u'A',
        u'1999-12-02',
        43.75,
        45.0,
        43.19,
        44.13,
        2195900.0,
        0.0,
        1.0,
        29.848030016228,
        30.700830873835,
        29.46597523202,
        30.107281476941,
        2195900.0],
       [u'A',
        u'1999-12-03',
        44.94,
        45.69,
        44.31,
        44.5,
        2175700.0,
        0.0,
        1.0,
        30.65989643267,
        31.171576947233,
        30.230084800436,
        30.359710530792,
        2175700.0],
       [u'A',
        u'1999-12-06',
        45.25,
        46.44,
        45.19,
        45.75,
        1610000.0,
        0.0,
        1.0,
        30.871391045356,
        31.683257461797,
        30.830456604191,
        31.212511388399,
        1610000.0],
       [u'A',
        u'1999-12-07',
        45.75,
        46.0,
        44.31,
        45.25,
        1585100.0,
        0.0,
        1.0,
        31.212511388399,
        31.38307155992,
        30.230084800436,
        30.871391045356,
        1585100.0],
       [u'A',
        u'1999-12-08',
        45.25,
        45.63,
        44.81,
        45.19,
        1350400.0,
        0.0,
        1.0,
        30.871391045356,
        31.130642506068,
        30.571205143478,
        30.830456604191,
        1350400.0],
       [u'A',
        u'1999-12-09',
        45.25,
        45.94,
        45.25,
        45.81,
        1451400.0,
        0.0,
        1.0,
        30.871391045356,
        31.342137118755,
        30.871391045356,
        31.253445829564,
        1451400.0],
       [u'A',
        u'1999-12-10',
        45.69,
        45.94,
        44.75,
        44.75,
        1190800.0,
        0.0,
        1.0,
        31.171576947233,
        31.342137118755,
        30.530270702313,
        30.530270702313,
        1190800.0],
       [u'A',
        u'1999-12-13',
        45.5,
        46.25,
        44.38,
        45.5,
        2875900.0,
        0.0,
        1.0,
        31.041951216877,
        31.553631731441,
        30.277841648462,
        31.041951216877,
        2875900.0],
       [u'A',
        u'1999-12-14',
        45.38,
        45.38,
        42.06,
        43.0,
        1665900.0,
        0.0,
        1.0,
        30.960082334547,
        30.960082334547,
        28.695043256744,
        29.336349501664,
        1665900.0],
       [u'A',
        u'1999-12-15',
        42.0,
        42.31,
        41.0,
        41.69,
        2087100.0,
        0.0,
        1.0,
        28.654108815579,
        28.865603428265,
        27.971868129494,
        28.442614202893,
        2087100.0],
       [u'A',
        u'1999-12-16',
        42.0,
        48.0,
        42.0,
        47.25,
        1848300.0,
        0.0,
        1.0,
        28.654108815579,
        32.74755293209,
        28.654108815579,
        32.235872417526,
        1848300.0],
       [u'A',
        u'1999-12-17',
        46.38,
        47.12,
        45.44,
        45.94,
        2652400.0,
        0.0,
        1.0,
        31.642323020632,
        32.147181128335,
        31.001016775712,
        31.342137118755,
        2652400.0],
       [u'A',
        u'1999-12-20',
        46.25,
        46.94,
        46.13,
        46.88,
        856100.0,
        0.0,
        1.0,
        31.553631731441,
        32.02437780484,
        31.471762849111,
        31.983443363675,
        856100.0],
       [u'A',
        u'1999-12-21',
        46.69,
        46.69,
        46.0,
        46.63,
        1616200.0,
        0.0,
        1.0,
        31.853817633319,
        31.853817633319,
        31.38307155992,
        31.812883192154,
        1616200.0],
       [u'A',
        u'1999-12-22',
        46.63,
        47.56,
        46.31,
        47.56,
        1363200.0,
        0.0,
        1.0,
        31.812883192154,
        32.447367030213,
        31.594566172606,
        32.447367030213,
        1363200.0],
       [u'A',
        u'1999-12-23',
        47.5,
        50.0,
        47.44,
        49.75,
        1544700.0,
        0.0,
        1.0,
        32.406432589048,
        34.112034304261,
        32.365498147883,
        33.941474132739,
        1544700.0],
       [u'A',
        u'1999-12-27',
        49.94,
        53.19,
        49.56,
        52.81,
        1451800.0,
        0.0,
        1.0,
        34.071099863096,
        36.288382092873,
        33.811848402383,
        36.02913063216,
        1451800.0],
       [u'A',
        u'1999-12-28',
        54.25,
        61.5,
        53.94,
        61.5,
        2546500.0,
        0.0,
        1.0,
        37.011557220123,
        41.957802194241,
        36.800062607436,
        41.957802194241,
        2546500.0],
       [u'A',
        u'1999-12-29',
        63.0,
        79.06,
        62.94,
        72.0,
        7524000.0,
        0.0,
        1.0,
        42.981163223369,
        53.937948641897,
        42.940228782203,
        49.121329398135,
        7524000.0],
       [u'A',
        u'1999-12-30',
        76.0,
        80.0,
        74.25,
        79.25,
        4771900.0,
        0.0,
        1.0,
        51.850292142476,
        54.579254886817,
        50.656370941827,
        54.067574372253,
        4771900.0],
       [u'A',
        u'1999-12-31',
        79.5,
        79.94,
        76.25,
        77.31,
        1381400.0,
        0.0,
        1.0,
        54.238134543775,
        54.538320445652,
        52.020852313998,
        52.744027441248,
        1381400.0],
       [u'A',
        u'2000-01-03',
        78.75,
        78.94,
        67.38,
        72.0,
        3343600.0,
        0.0,
        1.0,
        53.726454029211,
        53.856079759567,
        45.969377428422,
        49.121329398135,
        3343600.0],
       [u'A',
        u'2000-01-04',
        68.13,
        68.88,
        64.75,
        66.5,
        3408500.0,
        0.0,
        1.0,
        46.481057942986,
        46.99273845755,
        44.175084424018,
        45.369005624667,
        3408500.0],
       [u'A',
        u'2000-01-05',
        66.25,
        66.31,
        61.31,
        61.56,
        4119200.0,
        0.0,
        1.0,
        45.198445453145,
        45.239379894311,
        41.828176463885,
        41.998736635406,
        4119200.0],
       [u'A',
        u'2000-01-06',
        61.63,
        62.0,
        58.13,
        60.0,
        1812900.0,
        0.0,
        1.0,
        42.046493483432,
        42.298922537283,
        39.658651082134,
        40.934441165113,
        1812900.0],
       [u'A',
        u'2000-01-07',
        59.06,
        65.94,
        59.0,
        65.0,
        2016900.0,
        0.0,
        1.0,
        40.293134920193,
        44.986950840459,
        40.252200479028,
        44.345644595539,
        2016900.0],
       [u'A',
        u'2000-01-10',
        69.0,
        69.63,
        67.56,
        68.94,
        1536800.0,
        0.0,
        1.0,
        47.07460733988,
        47.504418972113,
        46.092180751917,
        47.033672898715,
        1536800.0],
       [u'A',
        u'2000-01-11',
        68.94,
        68.94,
        66.44,
        68.0,
        1327600.0,
        0.0,
        1.0,
        47.033672898715,
        47.033672898715,
        45.328071183502,
        46.392366653795,
        1327600.0],
       [u'A',
        u'2000-01-12',
        68.0,
        68.0,
        64.06,
        66.63,
        1022800.0,
        0.0,
        1.0,
        46.392366653795,
        46.392366653795,
        43.704338350619,
        45.457696913858,
        1022800.0],
       [u'A',
        u'2000-01-13',
        68.38,
        69.81,
        66.0,
        67.63,
        811400.0,
        0.0,
        1.0,
        46.651618114507,
        47.627222295609,
        45.027885281624,
        46.139937599943,
        811400.0],
       [u'A',
        u'2000-01-14',
        67.0,
        69.38,
        67.0,
        68.38,
        942000.0,
        0.0,
        1.0,
        45.710125967709,
        47.333858800592,
        45.710125967709,
        46.651618114507,
        942000.0],
       [u'A',
        u'2000-01-18',
        68.63,
        72.88,
        68.13,
        71.5,
        1503400.0,
        0.0,
        1.0,
        46.822178286028,
        49.72170120189,
        46.481057942986,
        48.780209055093,
        1503400.0],
       [u'A',
        u'2000-01-19',
        72.0,
        72.0,
        69.81,
        70.0,
        1877600.0,
        0.0,
        1.0,
        49.121329398135,
        49.121329398135,
        47.627222295609,
        47.756848025965,
        1877600.0],
       [u'A',
        u'2000-01-20',
        70.75,
        70.88,
        67.5,
        68.13,
        1436300.0,
        0.0,
        1.0,
        48.268528540529,
        48.35721982972,
        46.051246310752,
        46.481057942986,
        1436300.0],
       [u'A',
        u'2000-01-21',
        69.13,
        69.38,
        66.44,
        68.75,
        1372200.0,
        0.0,
        1.0,
        47.163298629071,
        47.333858800592,
        45.328071183502,
        46.904047168359,
        1372200.0],
       [u'A',
        u'2000-01-24',
        68.5,
        71.81,
        68.0,
        68.5,
        1499200.0,
        0.0,
        1.0,
        46.733486996837,
        48.991703667779,
        46.392366653795,
        46.733486996837,
        1499200.0],
       [u'A',
        u'2000-01-25',
        68.75,
        69.63,
        66.44,
        67.69,
        825300.0,
        0.0,
        1.0,
        46.904047168359,
        47.504418972113,
        45.328071183502,
        46.180872041108,
        825300.0],
       [u'A',
        u'2000-01-26',
        67.94,
        69.25,
        67.88,
        68.31,
        731300.0,
        0.0,
        1.0,
        46.351432212629,
        47.245167511401,
        46.310497771464,
        46.603861266481,
        731300.0],
       [u'A',
        u'2000-01-27',
        69.88,
        70.5,
        67.25,
        68.44,
        621300.0,
        0.0,
        1.0,
        47.674979143635,
        48.097968369008,
        45.880686139231,
        46.692552555672,
        621300.0],
       [u'A',
        u'2000-01-28',
        69.5,
        69.5,
        67.44,
        68.06,
        1151100.0,
        0.0,
        1.0,
        47.415727682922,
        47.415727682922,
        46.010311869587,
        46.43330109496,
        1151100.0],
       [u'A',
        u'2000-01-31',
        67.56,
        67.63,
        64.75,
        66.19,
        744200.0,
        0.0,
        1.0,
        46.092180751917,
        46.139937599943,
        44.175084424018,
        45.15751101198,
        744200.0],
       [u'A',
        u'2000-02-01',
        66.25,
        72.0,
        66.25,
        71.0,
        1004500.0,
        0.0,
        1.0,
        45.198445453145,
        49.121329398135,
        45.198445453145,
        48.43908871205,
        1004500.0],
       [u'A',
        u'2000-02-02',
        71.88,
        76.5,
        71.56,
        76.5,
        1391400.0,
        0.0,
        1.0,
        49.039460515805,
        52.191412485519,
        48.821143496258,
        52.191412485519,
        1391400.0],
       [u'A',
        u'2000-02-03',
        75.19,
        77.75,
        73.81,
        77.75,
        1272900.0,
        0.0,
        1.0,
        51.297677186747,
        53.044213343125,
        50.35618503995,
        53.044213343125,
        1272900.0],
       [u'A',
        u'2000-02-04',
        77.75,
        77.75,
        75.0,
        76.25,
        819500.0,
        0.0,
        1.0,
        53.044213343125,
        53.044213343125,
        51.168051456391,
        52.020852313998,
        819500.0],
       [u'A',
        u'2000-02-07',
        77.69,
        80.0,
        76.25,
        79.5,
        911500.0,
        0.0,
        1.0,
        53.00327890196,
        54.579254886817,
        52.020852313998,
        54.238134543775,
        911500.0],
       [u'A',
        u'2000-02-08',
        80.75,
        82.19,
        78.25,
        79.0,
        836700.0,
        0.0,
        1.0,
        55.090935401381,
        56.073361989344,
        53.385333686168,
        53.897014200732,
        836700.0],
       [u'A',
        u'2000-02-09',
        77.63,
        78.69,
        75.69,
        75.75,
        846100.0,
        0.0,
        1.0,
        52.962344460795,
        53.685519588046,
        51.63879752979,
        51.679731970955,
        846100.0],
       [u'A',
        u'2000-02-10',
        77.0,
        78.81,
        75.31,
        76.69,
        763100.0,
        0.0,
        1.0,
        52.532532828562,
        53.767388470376,
        51.379546069078,
        52.321038215875,
        763100.0],
       [u'A',
        u'2000-02-11',
        76.5,
        76.81,
        74.81,
        75.38,
        537700.0,
        0.0,
        1.0,
        52.191412485519,
        52.402907098205,
        51.038425726035,
        51.427302917103,
        537700.0],
       [u'A',
        u'2000-02-14',
        75.25,
        76.94,
        74.81,
        76.44,
        599200.0,
        0.0,
        1.0,
        51.338611627912,
        52.491598387396,
        51.038425726035,
        52.150478044354,
        599200.0],
       [u'A',
        u'2000-02-15',
        76.56,
        83.0,
        76.56,
        81.88,
        1443200.0,
        0.0,
        1.0,
        52.232346926684,
        56.625976945073,
        52.232346926684,
        55.861867376657,
        1443200.0],
       [u'A',
        u'2000-02-16',
        80.0,
        81.88,
        79.38,
        81.0,
        1288800.0,
        0.0,
        1.0,
        54.579254886817,
        55.861867376657,
        54.156265661444,
        55.261495572902,
        1288800.0],
       [u'A',
        u'2000-02-17',
        81.0,
        97.0,
        77.63,
        97.0,
        675900.0,
        0.0,
        1.0,
        55.261495572902,
        66.177346550266,
        52.962344460795,
        66.177346550266,
        675900.0],
       [u'A',
        u'2000-02-18',
        88.5,
        95.88,
        88.06,
        93.75,
        2904200.0,
        0.0,
        1.0,
        60.378300718542,
        65.41323698185,
        60.078114816664,
        63.960064320489,
        2904200.0],
       [u'A',
        u'2000-02-22',
        96.0,
        97.38,
        90.0,
        91.5,
        1593700.0,
        0.0,
        1.0,
        65.495105864181,
        66.436598010978,
        61.401661747669,
        62.425022776797,
        1593700.0],
       [u'A',
        u'2000-02-23',
        91.63,
        100.0,
        91.63,
        99.0,
        1208900.0,
        0.0,
        1.0,
        62.513714065988,
        68.224068608521,
        62.513714065988,
        67.541827922436,
        1208900.0],
       [u'A',
        u'2000-02-24',
        101.4,
        115.4,
        100.5,
        106.8,
        2114700.0,
        0.0,
        1.0,
        69.179205569041,
        78.730575174234,
        68.565188951564,
        72.863305273901,
        2114700.0],
       [u'A',
        u'2000-02-25',
        103.4,
        113.9,
        103.3,
        108.1,
        1465100.0,
        0.0,
        1.0,
        70.543686941211,
        77.707214145106,
        70.475462872603,
        73.750218165812,
        1465100.0],
       [u'A',
        u'2000-02-28',
        108.1,
        109.2,
        98.25,
        101.0,
        1198400.0,
        0.0,
        1.0,
        73.750218165812,
        74.500682920505,
        67.030147407872,
        68.906309294607,
        1198400.0],
       [u'A',
        u'2000-02-29',
        101.4,
        105.2,
        101.3,
        103.9,
        685300.0,
        0.0,
        1.0,
        69.179205569041,
        71.771720176165,
        69.110981500432,
        70.884807284254,
        685300.0],
       [u'A',
        u'2000-03-01',
        104.5,
        111.8,
        104.3,
        109.1,
        742400.0,
        0.0,
        1.0,
        71.294151695905,
        76.274508704327,
        71.157703558688,
        74.432458851897,
        742400.0],
       [u'A',
        u'2000-03-02',
        109.9,
        110.0,
        102.5,
        105.3,
        850000.0,
        0.0,
        1.0,
        74.978251400765,
        75.046475469374,
        69.929670323735,
        71.839944244773,
        850000.0],
       [u'A',
        u'2000-03-03',
        104.9,
        111.8,
        104.9,
        108.0,
        869700.0,
        0.0,
        1.0,
        71.567047970339,
        76.274508704327,
        71.567047970339,
        73.681994097203,
        869700.0],
       [u'A',
        u'2000-03-06',
        113.0,
        162.0,
        112.5,
        159.0,
        4072600.0,
        0.0,
        1.0,
        77.093197527629,
        110.5229911458,
        76.752077184587,
        108.47626908755,
        4072600.0],
       [u'A',
        u'2000-03-07',
        156.0,
        161.0,
        131.0,
        142.0,
        5515600.0,
        0.0,
        1.0,
        106.42954702929,
        109.84075045972,
        89.373529877163,
        96.8781774241,
        5515600.0],
       [u'A',
        u'2000-03-08',
        146.0,
        152.0,
        140.0,
        152.0,
        2828300.0,
        0.0,
        1.0,
        99.607140168441,
        103.70058428495,
        95.51369605193,
        103.70058428495,
        2828300.0],
       [u'A',
        u'2000-03-09',
        147.0,
        154.0,
        145.0,
        153.0,
        1798700.0,
        0.0,
        1.0,
        100.28938085453,
        105.06506565712,
        98.924899482356,
        104.38282497104,
        1798700.0],
       [u'A',
        u'2000-03-10',
        153.0,
        154.9,
        140.0,
        142.0,
        1773500.0,
        0.0,
        1.0,
        104.38282497104,
        105.6790822746,
        95.51369605193,
        96.8781774241,
        1773500.0],
       [u'A',
        u'2000-03-13',
        130.1,
        138.9,
        129.5,
        131.3,
        1878900.0,
        0.0,
        1.0,
        88.759513259686,
        94.763231297236,
        88.350168848035,
        89.578202082989,
        1878900.0],
       [u'A',
        u'2000-03-14',
        133.0,
        136.0,
        118.9,
        130.0,
        2520000.0,
        0.0,
        1.0,
        90.738011249334,
        92.784733307589,
        81.118417575532,
        88.691289191078,
        2520000.0],
       [u'A',
        u'2000-03-15',
        128.1,
        128.1,
        113.3,
        114.3,
        2179000.0,
        0.0,
        1.0,
        87.395031887516,
        87.395031887516,
        77.297869733455,
        77.98011041954,
        2179000.0],
       [u'A',
        u'2000-03-16',
        116.0,
        123.0,
        112.0,
        118.1,
        1981100.0,
        0.0,
        1.0,
        79.139919585885,
        83.915604388481,
        76.410956841544,
        80.572625026664,
        1981100.0],
       [u'A',
        u'2000-03-17',
        119.3,
        127.0,
        118.1,
        121.1,
        1118600.0,
        0.0,
        1.0,
        81.391313849966,
        86.644567132822,
        80.572625026664,
        82.619347084919,
        1118600.0],
       [u'A',
        u'2000-03-20',
        120.4,
        121.5,
        113.0,
        113.8,
        1016200.0,
        0.0,
        1.0,
        82.14177860466,
        82.892243359354,
        77.093197527629,
        77.638990076497,
        1016200.0],
       [u'A',
        u'2000-03-21',
        110.8,
        115.0,
        105.8,
        115.0,
        1808500.0,
        0.0,
        1.0,
        75.592268018242,
        78.4576788998,
        72.181064587816,
        78.4576788998,
        1808500.0],
       [u'A',
        u'2000-03-22',
        113.6,
        120.9,
        109.1,
        119.4,
        1407700.0,
        0.0,
        1.0,
        77.50254193928,
        82.482898947702,
        74.432458851897,
        81.459537918575,
        1407700.0],
       [u'A',
        u'2000-03-23',
        119.3,
        123.8,
        117.0,
        119.7,
        1396200.0,
        0.0,
        1.0,
        81.391313849966,
        84.46139693735,
        79.82216027197,
        81.6642101244,
        1396200.0],
       [u'A',
        u'2000-03-24',
        118.75,
        121.0,
        116.25,
        120.0,
        880200.0,
        0.0,
        1.0,
        81.016081472619,
        82.551123016311,
        79.310479757406,
        81.868882330226,
        880200.0],
       [u'A',
        u'2000-03-27',
        118.2,
        119.5,
        113.2,
        114.3,
        605700.0,
        0.0,
        1.0,
        80.640849095272,
        81.527761987183,
        77.229645664846,
        77.98011041954,
        605700.0],
       [u'A',
        u'2000-03-28',
        114.0,
        121.9,
        113.5,
        119.1,
        996100.0,
        0.0,
        1.0,
        77.775438213714,
        83.165139633788,
        77.434317870672,
        81.254865712749,
        996100.0],
       [u'A',
        u'2000-03-29',
        119.0,
        121.0,
        110.0,
        112.0,
        894400.0,
        0.0,
        1.0,
        81.186641644141,
        82.551123016311,
        75.046475469374,
        76.410956841544,
        894400.0],
       [u'A',
        u'2000-03-30',
        108.2,
        112.5,
        99.13,
        105.0,
        1455100.0,
        0.0,
        1.0,
        73.81844223442,
        76.752077184587,
        67.630519211627,
        71.635272038948,
        1455100.0],
       [u'A',
        u'2000-03-31',
        106.0,
        106.0,
        90.0,
        104.0,
        2670200.0,
        0.0,
        1.0,
        72.317512725033,
        72.317512725033,
        61.401661747669,
        70.953031352862,
        2670200.0],
       [u'A',
        u'2000-04-03',
        103.0,
        103.3,
        91.75,
        98.0,
        1452700.0,
        0.0,
        1.0,
        70.270790666777,
        70.475462872603,
        62.595582948318,
        66.859587236351,
        1452700.0],
       [u'A',
        u'2000-04-04',
        98.0,
        102.4,
        82.0,
        93.5,
        2517800.0,
        0.0,
        1.0,
        66.859587236351,
        69.861446255126,
        55.943736258988,
        63.789504148968,
        2517800.0],
       [u'A',
        u'2000-04-05',
        92.75,
        99.88,
        90.13,
        96.94,
        1508700.0,
        0.0,
        1.0,
        63.277823634404,
        68.142199726191,
        61.49035303686,
        66.136412109101,
        1508700.0],
       [u'A',
        u'2000-04-06',
        98.38,
        105.0,
        97.06,
        105.0,
        983600.0,
        0.0,
        1.0,
        67.118838697063,
        71.635272038948,
        66.218280991431,
        71.635272038948,
        983600.0],
       [u'A',
        u'2000-04-07',
        107.5,
        125.0,
        107.1,
        122.0,
        2128200.0,
        0.0,
        1.0,
        73.340873754161,
        85.280085760652,
        73.067977479726,
        83.233363702396,
        2128200.0],
       [u'A',
        u'2000-04-10',
        122.0,
        122.0,
        105.4,
        107.9,
        2114500.0,
        0.0,
        1.0,
        83.233363702396,
        83.233363702396,
        71.908168313382,
        73.613770028595,
        2114500.0],
       [u'A',
        u'2000-04-11',
        101.0,
        104.9,
        99.56,
        100.9,
        1356300.0,
        0.0,
        1.0,
        68.906309294607,
        71.567047970339,
        67.923882706644,
        68.838085225998,
        1356300.0],
       [u'A',
        u'2000-04-12',
        98.0,
        99.25,
        83.0,
        86.0,
        3112700.0,
        0.0,
        1.0,
        66.859587236351,
        67.712388093958,
        56.625976945073,
        58.672699003328,
        3112700.0],
       [u'A',
        u'2000-04-13',
        88.0,
        97.0,
        87.0,
        90.0,
        2672800.0,
        0.0,
        1.0,
        60.037180375499,
        66.177346550266,
        59.354939689414,
        61.401661747669,
        2672800.0],
       [u'A',
        u'2000-04-14',
        87.75,
        89.44,
        81.0,
        82.69,
        2047700.0,
        0.0,
        1.0,
        59.866620203978,
        61.019606963462,
        55.261495572902,
        56.414482332386,
        2047700.0],
       [u'A',
        u'2000-04-17',
        80.06,
        82.63,
        73.06,
        79.5,
        1972500.0,
        0.0,
        1.0,
        54.620189327982,
        56.373547891221,
        49.844504525386,
        54.238134543775,
        1972500.0],
       [u'A',
        u'2000-04-18',
        78.0,
        88.0,
        75.13,
        87.0,
        2688300.0,
        0.0,
        1.0,
        53.214773514647,
        60.037180375499,
        51.256742745582,
        59.354939689414,
        2688300.0],
       [u'A',
        u'2000-04-19',
        87.0,
        89.94,
        84.0,
        87.25,
        1733900.0,
        0.0,
        1.0,
        59.354939689414,
        61.360727306504,
        57.308217631158,
        59.525499860935,
        1733900.0],
       [u'A',
        u'2000-04-20',
        87.88,
        91.75,
        87.38,
        89.94,
        1039400.0,
        0.0,
        1.0,
        59.955311493169,
        62.595582948318,
        59.614191150126,
        61.360727306504,
        1039400.0],
       [u'A',
        u'2000-04-24',
        87.13,
        92.38,
        85.06,
        91.63,
        1215000.0,
        0.0,
        1.0,
        59.443630978605,
        63.025394580552,
        58.031392758408,
        62.513714065988,
        1215000.0],
       [u'A',
        u'2000-04-25',
        94.63,
        95.56,
        90.0,
        90.0,
        803500.0,
        0.0,
        1.0,
        64.560436124244,
        65.194919962303,
        61.401661747669,
        61.401661747669,
        803500.0],
       [u'A',
        u'2000-04-26',
        95.13,
        95.19,
        91.63,
        91.88,
        698500.0,
        0.0,
        1.0,
        64.901556467286,
        64.942490908452,
        62.513714065988,
        62.68427423751,
        698500.0],
       [u'A',
        u'2000-04-27',
        89.13,
        93.25,
        89.0,
        90.75,
        1631800.0,
        0.0,
        1.0,
        60.808112350775,
        63.618943977446,
        60.719421061584,
        61.913342262233,
        1631800.0],
       [u'A',
        u'2000-04-28',
        90.0,
        90.06,
        86.94,
        88.63,
        1272800.0,
        0.0,
        1.0,
        61.401661747669,
        61.442596188834,
        59.314005248249,
        60.466992007733,
        1272800.0],
       [u'A',
        u'2000-05-01',
        88.63,
        96.25,
        88.63,
        95.38,
        1356000.0,
        0.0,
        1.0,
        60.466992007733,
        65.665666035702,
        60.466992007733,
        65.072116638808,
        1356000.0],
       [u'A',
        u'2000-05-02',
        98.25,
        104.1,
        97.44,
        100.8,
        3046800.0,
        0.0,
        1.0,
        67.030147407872,
        71.021255421471,
        66.477532452143,
        68.76986115739,
        3046800.0],
       [u'A',
        u'2000-05-03',
        97.5,
        98.0,
        89.63,
        91.5,
        1664800.0,
        0.0,
        1.0,
        66.518466893308,
        66.859587236351,
        61.149232693818,
        62.425022776797,
        1664800.0],
       [u'A',
        u'2000-05-04',
        91.5,
        91.5,
        88.25,
        90.25,
        850000.0,
        0.0,
        1.0,
        62.425022776797,
        62.425022776797,
        60.20774054702,
        61.572221919191,
        850000.0],
       [u'A',
        u'2000-05-05',
        90.19,
        93.44,
        89.63,
        91.44,
        903700.0,
        0.0,
        1.0,
        61.531287478026,
        63.748569707802,
        61.149232693818,
        62.384088335632,
        903700.0],
       [u'A',
        u'2000-05-08',
        91.88,
        91.88,
        84.56,
        84.75,
        771300.0,
        0.0,
        1.0,
        62.68427423751,
        62.68427423751,
        57.690272415366,
        57.819898145722,
        771300.0],
       [u'A',
        u'2000-05-09',
        85.5,
        86.5,
        78.56,
        80.19,
        1229300.0,
        0.0,
        1.0,
        58.331578660286,
        59.013819346371,
        53.596828298854,
        54.708880617173,
        1229300.0],
       [u'A',
        u'2000-05-10',
        79.0,
        79.69,
        75.75,
        77.0,
        1145500.0,
        0.0,
        1.0,
        53.897014200732,
        54.367760274131,
        51.679731970955,
        52.532532828562,
        1145500.0],
       [u'A',
        u'2000-05-11',
        77.5,
        79.38,
        76.0,
        76.56,
        1203100.0,
        0.0,
        1.0,
        52.873653171604,
        54.156265661444,
        51.850292142476,
        52.232346926684,
        1203100.0],
       [u'A',
        u'2000-05-12',
        84.0,
        98.0,
        82.25,
        90.56,
        9703800.0,
        0.0,
        1.0,
        57.308217631158,
        66.859587236351,
        56.114296430509,
        61.783716531877,
        9703800.0],
       [u'A',
        u'2000-05-15',
        90.0,
        91.0,
        85.25,
        88.19,
        3178000.0,
        0.0,
        1.0,
        61.401661747669,
        62.083902433755,
        58.161018488765,
        60.166806105855,
        3178000.0],
       [u'A',
        u'2000-05-16',
        90.13,
        96.94,
        88.0,
        89.5,
        4127900.0,
        0.0,
        1.0,
        61.49035303686,
        66.136412109101,
        60.037180375499,
        61.060541404627,
        4127900.0],
       [u'A',
        u'2000-05-17',
        83.25,
        83.75,
        76.81,
        78.0,
        8906100.0,
        0.0,
        1.0,
        56.796537116594,
        57.137657459637,
        52.402907098205,
        53.214773514647,
        8906100.0],
       [u'A',
        u'2000-05-18',
        78.0,
        78.94,
        71.0,
        71.0,
        4401600.0,
        0.0,
        1.0,
        53.214773514647,
        53.856079759567,
        48.43908871205,
        48.43908871205,
        4401600.0],
       [u'A',
        u'2000-05-19',
        72.69,
        74.69,
        66.13,
        66.63,
        3763300.0,
        0.0,
        1.0,
        49.592075471534,
        50.956556843705,
        45.116576570815,
        45.457696913858,
        3763300.0],
       [u'A',
        u'2000-05-22',
        67.0,
        68.0,
        59.94,
        62.38,
        5594200.0,
        0.0,
        1.0,
        45.710125967709,
        46.392366653795,
        40.893506723948,
        42.558173997996,
        5594200.0],
       [u'A',
        u'2000-05-23',
        61.94,
        63.25,
        56.56,
        58.0,
        3730100.0,
        0.0,
        1.0,
        42.257988096118,
        43.15172339489,
        38.58753320498,
        39.569959792942,
        3730100.0],
       [u'A',
        u'2000-05-24',
        57.75,
        59.94,
        54.0,
        59.0,
        5691900.0,
        0.0,
        1.0,
        39.399399621421,
        40.893506723948,
        36.840997048602,
        40.252200479028,
        5691900.0],
       [u'A',
        u'2000-05-25',
        59.25,
        68.75,
        58.25,
        68.75,
        5492200.0,
        0.0,
        1.0,
        40.422760650549,
        46.904047168359,
        39.740519964464,
        46.904047168359,
        5492200.0],
       [u'A',
        u'2000-05-26',
        67.0,
        68.5,
        64.31,
        65.0,
        3545300.0,
        0.0,
        1.0,
        45.710125967709,
        46.733486996837,
        43.87489852214,
        44.345644595539,
        3545300.0],
       [u'A',
        u'2000-05-30',
        66.19,
        76.44,
        66.06,
        75.38,
        3818900.0,
        0.0,
        1.0,
        45.15751101198,
        52.150478044354,
        45.068819722789,
        51.427302917103,
        3818900.0],
       [u'A',
        u'2000-05-31',
        74.0,
        78.19,
        72.75,
        73.63,
        3153300.0,
        0.0,
        1.0,
        50.485810770306,
        53.344399245003,
        49.633009912699,
        50.233381716454,
        3153300.0],
       [u'A',
        u'2000-06-01',
        74.44,
        76.31,
        72.75,
        73.0,
        2824200.0,
        0.0,
        1.0,
        50.785996672183,
        52.061786755163,
        49.633009912699,
        49.803570084221,
        2824200.0],
       [u'A',
        u'2000-06-02',
        73.5,
        82.0,
        73.5,
        81.75,
        12222000.0,
        0.0,
        1.0,
        50.144690427263,
        55.943736258988,
        50.144690427263,
        55.773176087466,
        12222000.0],
       [u'A',
        u'2000-06-05',
        81.0,
        83.75,
        76.5,
        79.0,
        7613100.0,
        0.0,
        1.0,
        55.261495572902,
        57.137657459637,
        52.191412485519,
        53.897014200732,
        7613100.0],
       [u'A',
        u'2000-06-06',
        75.19,
        75.5,
        69.06,
        71.0,
        8713000.0,
        0.0,
        1.0,
        51.297677186747,
        51.509171799434,
        47.115541781045,
        48.43908871205,
        8713000.0],
       [u'A',
        u'2000-06-07',
        70.0,
        72.25,
        65.5,
        67.0,
        8170500.0,
        0.0,
        1.0,
        47.756848025965,
        49.291889569657,
        44.686764938582,
        45.710125967709,
        8170500.0],
       [u'A',
        u'2000-06-08',
        67.0,
        69.81,
        66.81,
        69.13,
        6846400.0,
        0.0,
        1.0,
        45.710125967709,
        47.627222295609,
        45.580500237353,
        47.163298629071,
        6846400.0],
       [u'A',
        u'2000-06-09',
        69.75,
        72.81,
        69.75,
        70.88,
        6631000.0,
        0.0,
        1.0,
        47.586287854444,
        49.673944353864,
        47.586287854444,
        48.35721982972,
        6631000.0],
       [u'A',
        u'2000-06-12',
        72.63,
        72.63,
        65.25,
        66.0,
        4059300.0,
        0.0,
        1.0,
        49.551141030369,
        49.551141030369,
        44.51620476706,
        45.027885281624,
        4059300.0],
       [u'A',
        u'2000-06-13',
        64.5,
        71.75,
        64.5,
        69.06,
        5521000.0,
        0.0,
        1.0,
        44.004524252496,
        48.950769226614,
        44.004524252496,
        47.115541781045,
        5521000.0],
       [u'A',
        u'2000-06-14',
        70.75,
        71.5,
        67.0,
        67.75,
        4013500.0,
        0.0,
        1.0,
        48.268528540529,
        48.780209055093,
        45.710125967709,
        46.221806482273,
        4013500.0],
       [u'A',
        u'2000-06-15',
        67.94,
        67.94,
        64.81,
        65.94,
        4862500.0,
        0.0,
        1.0,
        46.351432212629,
        46.351432212629,
        44.216018865183,
        44.986950840459,
        4862500.0],
       [u'A',
        u'2000-06-16',
        66.19,
        66.56,
        62.0,
        62.63,
        4640700.0,
        0.0,
        1.0,
        45.15751101198,
        45.409940065832,
        42.298922537283,
        42.728734169517,
        4640700.0],
       [u'A',
        u'2000-06-19',
        62.13,
        69.0,
        62.13,
        68.0,
        4872300.0,
        0.0,
        1.0,
        42.387613826474,
        47.07460733988,
        42.387613826474,
        46.392366653795,
        4872300.0],
       [u'A',
        u'2000-06-20',
        68.94,
        75.88,
        68.38,
        73.63,
        8382100.0,
        0.0,
        1.0,
        47.033672898715,
        51.768423260146,
        46.651618114507,
        50.233381716454,
        8382100.0],
       [u'A',
        u'2000-06-21',
        73.38,
        79.94,
        73.31,
        78.5,
        6421800.0,
        0.0,
        1.0,
        50.062821544933,
        54.538320445652,
        50.015064696907,
        53.555893857689,
        6421800.0],
       [u'A',
        u'2000-06-22',
        79.75,
        79.81,
        74.38,
        75.75,
        4816700.0,
        0.0,
        1.0,
        54.408694715296,
        54.449629156461,
        50.745062231018,
        51.679731970955,
        4816700.0],
       [u'A',
        u'2000-06-23',
        73.94,
        77.5,
        73.88,
        75.13,
        2839400.0,
        0.0,
        1.0,
        50.444876329141,
        52.873653171604,
        50.403941887976,
        51.256742745582,
        2839400.0],
       [u'A',
        u'2000-06-26',
        75.0,
        76.31,
        74.06,
        75.13,
        2735600.0,
        0.0,
        1.0,
        51.168051456391,
        52.061786755163,
        50.526745211471,
        51.256742745582,
        2735600.0],
       [u'A',
        u'2000-06-27',
        74.88,
        76.81,
        74.13,
        75.44,
        2940000.0,
        0.0,
        1.0,
        51.086182574061,
        52.402907098205,
        50.574502059497,
        51.468237358269,
        2940000.0],
       [u'A',
        u'2000-06-28',
        78.75,
        80.19,
        77.75,
        79.5,
        7078100.0,
        0.0,
        1.0,
        53.726454029211,
        54.708880617173,
        53.044213343125,
        54.238134543775,
        7078100.0],
       [u'A',
        u'2000-06-29',
        79.88,
        79.94,
        75.0,
        75.88,
        6195100.0,
        0.0,
        1.0,
        54.497386004487,
        54.538320445652,
        51.168051456391,
        51.768423260146,
        6195100.0],
       [u'A',
        u'2000-06-30',
        76.69,
        79.5,
        73.65,
        73.75,
        5922900.0,
        0.0,
        1.0,
        52.321038215875,
        54.238134543775,
        50.247026530176,
        50.315250598785,
        5922900.0],
       [u'A',
        u'2000-07-03',
        74.0,
        74.19,
        71.75,
        73.69,
        2285900.0,
        0.0,
        1.0,
        50.485810770306,
        50.615436500662,
        48.950769226614,
        50.274316157619,
        2285900.0],
       [u'A',
        u'2000-07-05',
        72.13,
        72.69,
        69.63,
        70.25,
        3862600.0,
        0.0,
        1.0,
        49.210020687327,
        49.592075471534,
        47.504418972113,
        47.927408197486,
        3862600.0],
       [u'A',
        u'2000-07-06',
        70.0,
        70.44,
        68.31,
        69.13,
        3005300.0,
        0.0,
        1.0,
        47.756848025965,
        48.057033927843,
        46.603861266481,
        47.163298629071,
        3005300.0],
       [u'A',
        u'2000-07-07',
        70.0,
        70.44,
        66.75,
        67.5,
        4286300.0,
        0.0,
        1.0,
        47.756848025965,
        48.057033927843,
        45.539565796188,
        46.051246310752,
        4286300.0],
       [u'A',
        u'2000-07-10',
        67.75,
        70.25,
        67.63,
        68.5,
        3836000.0,
        0.0,
        1.0,
        46.221806482273,
        47.927408197486,
        46.139937599943,
        46.733486996837,
        3836000.0],
       [u'A',
        u'2000-07-11',
        68.0,
        68.56,
        66.13,
        67.31,
        2987600.0,
        0.0,
        1.0,
        46.392366653795,
        46.774421438002,
        45.116576570815,
        45.921620580396,
        2987600.0],
       [u'A',
        u'2000-07-12',
        69.44,
        70.63,
        68.06,
        69.0,
        2712800.0,
        0.0,
        1.0,
        47.374793241757,
        48.186659658199,
        46.43330109496,
        47.07460733988,
        2712800.0],
       [u'A',
        u'2000-07-13',
        69.0,
        72.5,
        68.75,
        71.0,
        4177800.0,
        0.0,
        1.0,
        47.07460733988,
        49.462449741178,
        46.904047168359,
        48.43908871205,
        4177800.0],
       [u'A',
        u'2000-07-14',
        71.5,
        78.25,
        71.5,
        77.06,
        5438900.0,
        0.0,
        1.0,
        48.780209055093,
        53.385333686168,
        48.780209055093,
        52.573467269727,
        5438900.0],
       [u'A',
        u'2000-07-17',
        76.88,
        80.94,
        76.25,
        78.25,
        4410700.0,
        0.0,
        1.0,
        52.450663946231,
        55.220561131737,
        52.020852313998,
        53.385333686168,
        4410700.0],
       [u'A',
        u'2000-07-18',
        78.0,
        78.0,
        74.0,
        76.63,
        2619100.0,
        0.0,
        1.0,
        53.214773514647,
        53.214773514647,
        50.485810770306,
        52.28010377471,
        2619100.0],
       [u'A',
        u'2000-07-19',
        76.0,
        76.06,
        72.75,
        74.06,
        2531500.0,
        0.0,
        1.0,
        51.850292142476,
        51.891226583641,
        49.633009912699,
        50.526745211471,
        2531500.0],
       [u'A',
        u'2000-07-20',
        73.88,
        76.31,
        54.0,
        54.0,
        2540500.0,
        0.0,
        1.0,
        50.403941887976,
        52.061786755163,
        36.840997048602,
        36.840997048602,
        2540500.0],
       [u'A',
        u'2000-07-21',
        51.5,
        51.5,
        46.25,
        48.06,
        26067300.0,
        0.0,
        1.0,
        35.135395333389,
        35.135395333389,
        31.553631731441,
        32.788487373255,
        26067300.0],
       [u'A',
        u'2000-07-24',
        50.0,
        50.19,
        47.75,
        49.5,
        10005100.0,
        0.0,
        1.0,
        34.112034304261,
        34.241660034617,
        32.576992760569,
        33.770913961218,
        10005100.0],
       [u'A',
        u'2000-07-25',
        49.06,
        49.5,
        44.75,
        44.75,
        6534900.0,
        0.0,
        1.0,
        33.470728059341,
        33.770913961218,
        30.530270702313,
        30.530270702313,
        6534900.0],
       [u'A',
        u'2000-07-26',
        45.94,
        46.63,
        42.81,
        43.0,
        8144000.0,
        0.0,
        1.0,
        31.342137118755,
        31.812883192154,
        29.206723771308,
        29.336349501664,
        8144000.0],
       [u'A',
        u'2000-07-27',
        44.25,
        44.94,
        40.38,
        40.75,
        7045500.0,
        0.0,
        1.0,
        30.189150359271,
        30.65989643267,
        27.548878904121,
        27.801307957973,
        7045500.0],
       [u'A',
        u'2000-07-28',
        41.75,
        41.88,
        39.5,
        41.25,
        6879100.0,
        0.0,
        1.0,
        28.483548644058,
        28.572239933249,
        26.948507100366,
        28.142428301015,
        6879100.0],
       [u'A',
        u'2000-07-31',
        41.06,
        42.19,
        40.13,
        40.75,
        5760500.0,
        0.0,
        1.0,
        28.012802570659,
        28.783734545935,
        27.3783187326,
        27.801307957973,
        5760500.0],
       [u'A',
        u'2000-08-01',
        40.69,
        41.19,
        39.5,
        40.5,
        4242500.0,
        0.0,
        1.0,
        27.760373516807,
        28.10149385985,
        26.948507100366,
        27.630747786451,
        4242500.0],
       [u'A',
        u'2000-08-02',
        40.13,
        41.19,
        39.5,
        40.13,
        4827500.0,
        0.0,
        1.0,
        27.3783187326,
        28.10149385985,
        26.948507100366,
        27.3783187326,
        4827500.0],
       [u'A',
        u'2000-08-03',
        39.13,
        41.0,
        38.56,
        41.0,
        6146000.0,
        0.0,
        1.0,
        26.696078046514,
        27.971868129494,
        26.307200855446,
        27.971868129494,
        6146000.0],
       [u'A',
        u'2000-08-04',
        40.5,
        41.44,
        39.63,
        40.06,
        3685600.0,
        0.0,
        1.0,
        27.630747786451,
        28.272054031371,
        27.037198389557,
        27.330561884574,
        3685600.0],
       [u'A',
        u'2000-08-07',
        40.63,
        41.25,
        38.94,
        39.75,
        3977700.0,
        0.0,
        1.0,
        27.719439075642,
        28.142428301015,
        26.566452316158,
        27.119067271887,
        3977700.0],
       [u'A',
        u'2000-08-08',
        39.69,
        39.69,
        38.19,
        38.81,
        3659600.0,
        0.0,
        1.0,
        27.078132830722,
        27.078132830722,
        26.054771801594,
        26.477761026967,
        3659600.0],
       [u'A',
        u'2000-08-09',
        38.75,
        39.88,
        38.5,
        39.31,
        3348000.0,
        0.0,
        1.0,
        26.436826585802,
        27.207758561078,
        26.266266414281,
        26.81888137001,
        3348000.0],
       [u'A',
        u'2000-08-10',
        39.06,
        39.81,
        38.69,
        39.0,
        2234400.0,
        0.0,
        1.0,
        26.648321198488,
        27.160001713052,
        26.395892144637,
        26.607386757323,
        2234400.0],
       [u'A',
        u'2000-08-11',
        39.75,
        40.81,
        38.94,
        40.63,
        2454400.0,
        0.0,
        1.0,
        27.119067271887,
        27.842242399138,
        26.566452316158,
        27.719439075642,
        2454400.0],
       [u'A',
        u'2000-08-14',
        42.0,
        43.56,
        41.5,
        43.5,
        3960000.0,
        0.0,
        1.0,
        28.654108815579,
        29.718404285872,
        28.312988472536,
        29.677469844707,
        3960000.0],
       [u'A',
        u'2000-08-15',
        43.75,
        44.25,
        42.75,
        43.0,
        3209900.0,
        0.0,
        1.0,
        29.848030016228,
        30.189150359271,
        29.165789330143,
        29.336349501664,
        3209900.0],
       [u'A',
        u'2000-08-16',
        42.75,
        43.5,
        42.5,
        43.5,
        2247000.0,
        0.0,
        1.0,
        29.165789330143,
        29.677469844707,
        28.995229158622,
        29.677469844707,
        2247000.0],
       [u'A',
        u'2000-08-17',
        43.13,
        47.25,
        43.13,
        46.5,
        6818600.0,
        0.0,
        1.0,
        29.425040790855,
        32.235872417526,
        29.425040790855,
        31.724191902962,
        6818600.0],
       [u'A',
        u'2000-08-18',
        57.75,
        58.13,
        55.06,
        56.38,
        12720800.0,
        0.0,
        1.0,
        39.399399621421,
        39.658651082134,
        37.564172175852,
        38.464729881484,
        12720800.0],
       [u'A',
        u'2000-08-21',
        58.25,
        60.5,
        57.31,
        60.5,
        6134600.0,
        0.0,
        1.0,
        39.740519964464,
        41.275561508155,
        39.099213719544,
        41.275561508155,
        6134600.0],
       [u'A',
        u'2000-08-22',
        60.38,
        60.5,
        59.06,
        60.5,
        3556200.0,
        0.0,
        1.0,
        41.193692625825,
        41.275561508155,
        40.293134920193,
        41.275561508155,
        3556200.0],
       [u'A',
        u'2000-08-23',
        59.88,
        60.56,
        59.31,
        60.5,
        2334500.0,
        0.0,
        1.0,
        40.852572282783,
        41.316495949321,
        40.463695091714,
        41.275561508155,
        2334500.0],
       [u'A',
        u'2000-08-24',
        60.38,
        60.69,
        59.13,
        59.75,
        2168100.0,
        0.0,
        1.0,
        41.193692625825,
        41.405187238512,
        40.340891768219,
        40.763880993592,
        2168100.0],
       [u'A',
        u'2000-08-25',
        59.69,
        60.06,
        58.06,
        58.5,
        1748300.0,
        0.0,
        1.0,
        40.722946552426,
        40.975375606278,
        39.610894234108,
        39.911080135985,
        1748300.0],
       [u'A',
        u'2000-08-28',
        58.31,
        58.88,
        57.25,
        58.63,
        2653000.0,
        0.0,
        1.0,
        39.781454405629,
        40.170331596697,
        39.058279278379,
        39.999771425176,
        2653000.0],
       [u'A',
        u'2000-08-29',
        58.63,
        64.0,
        58.5,
        63.0,
        4298300.0,
        0.0,
        1.0,
        39.999771425176,
        43.663403909454,
        39.911080135985,
        42.981163223369,
        4298300.0],
       [u'A',
        u'2000-08-30',
        63.31,
        63.94,
        60.88,
        61.38,
        2474800.0,
        0.0,
        1.0,
        43.192657836055,
        43.622469468289,
        41.534812968868,
        41.87593331191,
        2474800.0],
       [u'A',
        u'2000-08-31',
        61.63,
        62.13,
        59.75,
        61.0,
        2489200.0,
        0.0,
        1.0,
        42.046493483432,
        42.387613826474,
        40.763880993592,
        41.616681851198,
        2489200.0],
       [u'A',
        u'2000-09-01',
        60.69,
        62.69,
        60.13,
        61.88,
        2244800.0,
        0.0,
        1.0,
        41.405187238512,
        42.769668610682,
        41.023132454304,
        42.217053654953,
        2244800.0],
       [u'A',
        u'2000-09-05',
        61.69,
        62.5,
        61.25,
        61.81,
        1462800.0,
        0.0,
        1.0,
        42.087427924597,
        42.640042880326,
        41.787242022719,
        42.169296806927,
        1462800.0],
       [u'A',
        u'2000-09-06',
        61.69,
        62.38,
        59.81,
        60.0,
        1599000.0,
        0.0,
        1.0,
        42.087427924597,
        42.558173997996,
        40.804815434757,
        40.934441165113,
        1599000.0],
       [u'A',
        u'2000-09-07',
        60.0,
        62.13,
        59.25,
        61.88,
        1518600.0,
        0.0,
        1.0,
        40.934441165113,
        42.387613826474,
        40.422760650549,
        42.217053654953,
        1518600.0],
       [u'A',
        u'2000-09-08',
        60.56,
        61.06,
        59.13,
        59.25,
        1441900.0,
        0.0,
        1.0,
        41.316495949321,
        41.657616292363,
        40.340891768219,
        40.422760650549,
        1441900.0],
       [u'A',
        u'2000-09-11',
        59.0,
        59.0,
        56.0,
        56.75,
        2130800.0,
        0.0,
        1.0,
        40.252200479028,
        40.252200479028,
        38.205478420772,
        38.717158935336,
        2130800.0],
       [u'A',
        u'2000-09-12',
        55.81,
        57.88,
        55.0,
        55.0,
        2024500.0,
        0.0,
        1.0,
        38.075852690416,
        39.488090910612,
        37.523237734687,
        37.523237734687,
        2024500.0],
       [u'A',
        u'2000-09-13',
        56.75,
        56.75,
        53.56,
        55.0,
        2520200.0,
        0.0,
        1.0,
        38.717158935336,
        38.717158935336,
        36.540811146724,
        37.523237734687,
        2520200.0],
       [u'A',
        u'2000-09-14',
        55.63,
        57.25,
        55.56,
        55.75,
        2553000.0,
        0.0,
        1.0,
        37.95304936692,
        39.058279278379,
        37.905292518895,
        38.034918249251,
        2553000.0],
       [u'A',
        u'2000-09-15',
        55.69,
        58.81,
        55.63,
        57.0,
        2698700.0,
        0.0,
        1.0,
        37.993983808086,
        40.122574748671,
        37.95304936692,
        38.887719106857,
        2698700.0],
       [u'A',
        u'2000-09-18',
        57.13,
        57.69,
        52.5,
        54.0,
        3383900.0,
        0.0,
        1.0,
        38.976410396048,
        39.358465180256,
        35.817636019474,
        36.840997048602,
        3383900.0],
       [u'A',
        u'2000-09-19',
        53.56,
        54.0,
        52.0,
        53.88,
        2287600.0,
        0.0,
        1.0,
        36.540811146724,
        36.840997048602,
        35.476515676431,
        36.759128166271,
        2287600.0],
       [u'A',
        u'2000-09-20',
        53.56,
        53.88,
        51.75,
        52.5,
        1407800.0,
        0.0,
        1.0,
        36.540811146724,
        36.759128166271,
        35.30595550491,
        35.817636019474,
        1407800.0],
       [u'A',
        u'2000-09-21',
        52.63,
        52.63,
        47.0,
        48.0,
        2095700.0,
        0.0,
        1.0,
        35.906327308665,
        35.906327308665,
        32.065312246005,
        32.74755293209,
        2095700.0],
       [u'A',
        u'2000-09-22',
        48.06,
        50.0,
        47.88,
        50.0,
        2464400.0,
        0.0,
        1.0,
        32.788487373255,
        34.112034304261,
        32.66568404976,
        34.112034304261,
        2464400.0],
       [u'A',
        u'2000-09-25',
        50.25,
        51.94,
        48.19,
        48.31,
        1708500.0,
        0.0,
        1.0,
        34.282594475782,
        35.435581235266,
        32.877178662446,
        32.959047544777,
        1708500.0],
       [u'A',
        u'2000-09-26',
        48.5,
        49.31,
        45.13,
        45.19,
        2181800.0,
        0.0,
        1.0,
        33.088673275133,
        33.641288230862,
        30.789522163026,
        30.830456604191,
        2181800.0],
       [u'A',
        u'2000-09-27',
        46.19,
        46.75,
        44.38,
        46.0,
        2801700.0,
        0.0,
        1.0,
        31.512697290276,
        31.894752074484,
        30.277841648462,
        31.38307155992,
        2801700.0],
       [u'A',
        u'2000-09-28',
        46.06,
        48.44,
        46.06,
        47.95,
        3021900.0,
        0.0,
        1.0,
        31.424006001085,
        33.047738833968,
        31.424006001085,
        32.713440897786,
        3021900.0],
       [u'A',
        u'2000-09-29',
        48.31,
        49.75,
        47.81,
        48.94,
        2630500.0,
        0.0,
        1.0,
        32.959047544777,
        33.941474132739,
        32.617927201734,
        33.38885917701,
        2630500.0],
       [u'A',
        u'2000-10-02',
        49.13,
        51.38,
        49.13,
        50.56,
        2151800.0,
        0.0,
        1.0,
        33.518484907367,
        35.053526451058,
        33.518484907367,
        34.494089088468,
        2151800.0],
       [u'A',
        u'2000-10-03',
        51.0,
        55.5,
        50.31,
        53.13,
        3974300.0,
        0.0,
        1.0,
        34.794274990346,
        37.864358077729,
        34.323528916947,
        36.247447651707,
        3974300.0],
       [u'A',
        u'2000-10-04',
        52.88,
        58.63,
        52.5,
        57.88,
        3956500.0,
        0.0,
        1.0,
        36.076887480186,
        39.999771425176,
        35.817636019474,
        39.488090910612,
        3956500.0],
       [u'A',
        u'2000-10-05',
        57.94,
        57.94,
        54.63,
        55.13,
        2860400.0,
        0.0,
        1.0,
        39.529025351777,
        39.529025351777,
        37.270808680835,
        37.611929023878,
        2860400.0],
       [u'A',
        u'2000-10-06',
        55.81,
        55.94,
        51.19,
        52.19,
        1997000.0,
        0.0,
        1.0,
        38.075852690416,
        38.164543979607,
        34.923900720702,
        35.606141406787,
        1997000.0],
       [u'A',
        u'2000-10-09',
        52.13,
        52.13,
        50.13,
        50.69,
        1546200.0,
        0.0,
        1.0,
        35.565206965622,
        35.565206965622,
        34.200725593452,
        34.58278037766,
        1546200.0],
       [u'A',
        u'2000-10-10',
        51.63,
        52.94,
        48.38,
        49.56,
        2210600.0,
        0.0,
        1.0,
        35.22408662258,
        36.117821921351,
        33.006804392803,
        33.811848402383,
        2210600.0],
       [u'A',
        u'2000-10-11',
        48.0,
        48.31,
        44.81,
        45.81,
        3954100.0,
        0.0,
        1.0,
        32.74755293209,
        32.959047544777,
        30.571205143478,
        31.253445829564,
        3954100.0],
       [u'A',
        u'2000-10-12',
        46.81,
        47.13,
        43.31,
        44.75,
        2987600.0,
        0.0,
        1.0,
        31.935686515649,
        32.154003535196,
        29.547844114351,
        30.530270702313,
        2987600.0],
       [u'A',
        u'2000-10-13',
        43.5,
        45.06,
        42.81,
        44.38,
        3630500.0,
        0.0,
        1.0,
        29.677469844707,
        30.741765315,
        29.206723771308,
        30.277841648462,
        3630500.0],
       [u'A',
        u'2000-10-16',
        44.88,
        48.69,
        44.56,
        46.44,
        2973700.0,
        0.0,
        1.0,
        30.618961991504,
        33.218299005489,
        30.400644971957,
        31.683257461797,
        2973700.0],
       [u'A',
        u'2000-10-17',
        46.56,
        46.63,
        42.63,
        43.31,
        2062400.0,
        0.0,
        1.0,
        31.765126344128,
        31.812883192154,
        29.083920447813,
        29.547844114351,
        2062400.0],
       [u'A',
        u'2000-10-18',
        40.56,
        42.44,
        39.25,
        40.88,
        4032800.0,
        0.0,
        1.0,
        27.671682227616,
        28.954294717457,
        26.777946928845,
        27.889999247164,
        4032800.0],
       [u'A',
        u'2000-10-19',
        42.5,
        44.94,
        42.31,
        43.75,
        3290300.0,
        0.0,
        1.0,
        28.995229158622,
        30.65989643267,
        28.865603428265,
        29.848030016228,
        3290300.0],
       [u'A',
        u'2000-10-20',
        43.75,
        47.69,
        43.69,
        46.56,
        3328800.0,
        0.0,
        1.0,
        29.848030016228,
        32.536058319404,
        29.807095575063,
        31.765126344128,
        3328800.0],
       [u'A',
        u'2000-10-23',
        46.56,
        51.88,
        45.5,
        51.06,
        3601700.0,
        0.0,
        1.0,
        31.765126344128,
        35.394646794101,
        31.041951216877,
        34.835209431511,
        3601700.0],
       [u'A',
        u'2000-10-24',
        51.06,
        51.25,
        47.5,
        48.06,
        2586600.0,
        0.0,
        1.0,
        34.835209431511,
        34.964835161867,
        32.406432589048,
        32.788487373255,
        2586600.0],
       [u'A',
        u'2000-10-25',
        44.88,
        45.31,
        42.25,
        42.63,
        3768600.0,
        0.0,
        1.0,
        30.618961991504,
        30.912325486521,
        28.8246689871,
        29.083920447813,
        3768600.0],
       [u'A',
        u'2000-10-26',
        42.63,
        44.56,
        42.0,
        44.0,
        4563000.0,
        0.0,
        1.0,
        29.083920447813,
        30.400644971957,
        28.654108815579,
        30.018590187749,
        4563000.0],
       [u'A',
        u'2000-10-27',
        45.88,
        47.25,
        44.94,
        45.75,
        3238300.0,
        0.0,
        1.0,
        31.30120267759,
        32.235872417526,
        30.65989643267,
        31.212511388399,
        3238300.0],
       [u'A',
        u'2000-10-30',
        44.81,
        46.0,
        43.75,
        45.5,
        1945300.0,
        0.0,
        1.0,
        30.571205143478,
        31.38307155992,
        29.848030016228,
        31.041951216877,
        1945300.0],
       [u'A',
        u'2000-10-31',
        45.63,
        47.63,
        45.63,
        46.31,
        2799000.0,
        0.0,
        1.0,
        31.130642506068,
        32.495123878239,
        31.130642506068,
        31.594566172606,
        2799000.0],
       [u'A',
        u'2000-11-01',
        46.0,
        47.31,
        45.56,
        46.81,
        2430700.0,
        0.0,
        1.0,
        31.38307155992,
        32.276806858692,
        31.082885658042,
        31.935686515649,
        2430700.0],
       [u'A',
        u'2000-11-02',
        47.13,
        48.69,
        46.88,
        48.13,
        2455500.0,
        0.0,
        1.0,
        32.154003535196,
        33.218299005489,
        31.983443363675,
        32.836244221281,
        2455500.0],
       [u'A',
        u'2000-11-03',
        47.63,
        47.69,
        45.81,
        46.81,
        1700100.0,
        0.0,
        1.0,
        32.495123878239,
        32.536058319404,
        31.253445829564,
        31.935686515649,
        1700100.0],
       [u'A',
        u'2000-11-06',
        46.94,
        46.94,
        45.88,
        46.38,
        1692300.0,
        0.0,
        1.0,
        32.02437780484,
        32.02437780484,
        31.30120267759,
        31.642323020632,
        1692300.0],
       [u'A',
        u'2000-11-07',
        45.63,
        46.31,
        45.56,
        45.94,
        1567600.0,
        0.0,
        1.0,
        31.130642506068,
        31.594566172606,
        31.082885658042,
        31.342137118755,
        1567600.0],
       [u'A',
        u'2000-11-08',
        45.94,
        47.25,
        43.94,
        44.38,
        1707000.0,
        0.0,
        1.0,
        31.342137118755,
        32.235872417526,
        29.977655746584,
        30.277841648462,
        1707000.0],
       [u'A',
        u'2000-11-09',
        44.63,
        44.63,
        41.56,
        43.56,
        2837900.0,
        0.0,
        1.0,
        30.448401819983,
        30.448401819983,
        28.353922913702,
        29.718404285872,
        2837900.0],
       [u'A',
        u'2000-11-10',
        42.0,
        42.75,
        39.31,
        39.44,
        3548000.0,
        0.0,
        1.0,
        28.654108815579,
        29.165789330143,
        26.81888137001,
        26.907572659201,
        3548000.0],
       [u'A',
        u'2000-11-13',
        39.19,
        40.75,
        38.06,
        39.31,
        4275600.0,
        0.0,
        1.0,
        26.73701248768,
        27.801307957973,
        25.966080512403,
        26.81888137001,
        4275600.0],
       [u'A',
        u'2000-11-14',
        40.38,
        43.06,
        40.25,
        42.63,
        2827700.0,
        0.0,
        1.0,
        27.548878904121,
        29.377283942829,
        27.46018761493,
        29.083920447813,
        2827700.0],
       [u'A',
        u'2000-11-15',
        42.75,
        44.13,
        42.25,
        43.38,
        1723800.0,
        0.0,
        1.0,
        29.165789330143,
        30.107281476941,
        28.8246689871,
        29.595600962377,
        1723800.0],
       [u'A',
        u'2000-11-16',
        42.94,
        43.69,
        41.25,
        41.63,
        1984200.0,
        0.0,
        1.0,
        29.295415060499,
        29.807095575063,
        28.142428301015,
        28.401679761727,
        1984200.0],
       [u'A',
        u'2000-11-17',
        44.0,
        47.5,
        43.81,
        47.38,
        5628100.0,
        0.0,
        1.0,
        30.018590187749,
        32.406432589048,
        29.888964457393,
        32.324563706717,
        5628100.0],
       [u'A',
        u'2000-11-20',
        46.88,
        46.94,
        43.81,
        44.63,
        2962100.0,
        0.0,
        1.0,
        31.983443363675,
        32.02437780484,
        29.888964457393,
        30.448401819983,
        2962100.0],
       [u'A',
        u'2000-11-21',
        48.63,
        50.5,
        46.31,
        48.63,
        7225100.0,
        0.0,
        1.0,
        33.177364564324,
        34.453154647303,
        31.594566172606,
        33.177364564324,
        7225100.0],
       [u'A',
        u'2000-11-22',
        48.63,
        49.0,
        45.5,
        48.0,
        2624100.0,
        0.0,
        1.0,
        33.177364564324,
        33.429793618176,
        31.041951216877,
        32.74755293209,
        2624100.0],
       [u'A',
        u'2000-11-24',
        48.88,
        51.5,
        48.69,
        50.94,
        1249300.0,
        0.0,
        1.0,
        33.347924735845,
        35.135395333389,
        33.218299005489,
        34.753340549181,
        1249300.0],
       [u'A',
        u'2000-11-27',
        50.94,
        51.94,
        50.0,
        50.5,
        2142700.0,
        0.0,
        1.0,
        34.753340549181,
        35.435581235266,
        34.112034304261,
        34.453154647303,
        2142700.0],
       [u'A',
        u'2000-11-28',
        50.5,
        52.75,
        50.44,
        50.69,
        2532300.0,
        0.0,
        1.0,
        34.453154647303,
        35.988196190995,
        34.412220206138,
        34.58278037766,
        2532300.0],
       [u'A',
        u'2000-11-29',
        51.63,
        54.0,
        51.06,
        53.88,
        3136700.0,
        0.0,
        1.0,
        35.22408662258,
        36.840997048602,
        34.835209431511,
        36.759128166271,
        3136700.0],
       [u'A',
        u'2000-11-30',
        53.0,
        53.19,
        50.63,
        52.19,
        3549800.0,
        0.0,
        1.0,
        36.158756362516,
        36.288382092873,
        34.541845936494,
        35.606141406787,
        3549800.0],
       [u'A',
        u'2000-12-01',
        52.94,
        54.69,
        52.75,
        53.0,
        2595600.0,
        0.0,
        1.0,
        36.117821921351,
        37.311743122,
        35.988196190995,
        36.158756362516,
        2595600.0],
       [u'A',
        u'2000-12-04',
        52.06,
        53.06,
        50.5,
        51.0,
        2070900.0,
        0.0,
        1.0,
        35.517450117596,
        36.199690803681,
        34.453154647303,
        34.794274990346,
        2070900.0],
       [u'A',
        u'2000-12-05',
        52.75,
        55.69,
        52.56,
        55.06,
        3914400.0,
        0.0,
        1.0,
        35.988196190995,
        37.993983808086,
        35.858570460639,
        37.564172175852,
        3914400.0],
       [u'A',
        u'2000-12-06',
        55.25,
        56.94,
        52.0,
        52.0,
        3123700.0,
        0.0,
        1.0,
        37.693797906208,
        38.846784665692,
        35.476515676431,
        35.476515676431,
        3123700.0],
       [u'A',
        u'2000-12-07',
        52.5,
        54.88,
        51.38,
        54.0,
        2188800.0,
        0.0,
        1.0,
        35.817636019474,
        37.441368852357,
        35.053526451058,
        36.840997048602,
        2188800.0],
       [u'A',
        u'2000-12-08',
        56.38,
        59.88,
        56.13,
        59.44,
        3154500.0,
        0.0,
        1.0,
        38.464729881484,
        40.852572282783,
        38.294169709963,
        40.552386380905,
        3154500.0],
       [u'A',
        u'2000-12-11',
        58.63,
        59.31,
        57.0,
        57.75,
        2275600.0,
        0.0,
        1.0,
        39.999771425176,
        40.463695091714,
        38.887719106857,
        39.399399621421,
        2275600.0],
       [u'A',
        u'2000-12-12',
        58.38,
        58.69,
        57.0,
        57.25,
        1526600.0,
        0.0,
        1.0,
        39.829211253655,
        40.040705866341,
        38.887719106857,
        39.058279278379,
        1526600.0],
       [u'A',
        u'2000-12-13',
        59.13,
        59.38,
        57.81,
        58.19,
        2929600.0,
        0.0,
        1.0,
        40.340891768219,
        40.51145193974,
        39.440334062586,
        39.699585523299,
        2929600.0],
       [u'A',
        u'2000-12-14',
        58.25,
        59.63,
        58.06,
        59.25,
        3037800.0,
        0.0,
        1.0,
        39.740519964464,
        40.682012111261,
        39.610894234108,
        40.422760650549,
        3037800.0],
       [u'A',
        u'2000-12-15',
        59.25,
        59.69,
        54.5,
        56.88,
        4328300.0,
        0.0,
        1.0,
        40.422760650549,
        40.722946552426,
        37.182117391644,
        38.805850224527,
        4328300.0],
       [u'A',
        u'2000-12-18',
        56.88,
        58.25,
        56.31,
        57.0,
        2434500.0,
        0.0,
        1.0,
        38.805850224527,
        39.740519964464,
        38.416973033458,
        38.887719106857,
        2434500.0],
       [u'A',
        u'2000-12-19',
        57.0,
        59.88,
        56.81,
        57.06,
        2345200.0,
        0.0,
        1.0,
        38.887719106857,
        40.852572282783,
        38.758093376501,
        38.928653548022,
        2345200.0],
       [u'A',
        u'2000-12-20',
        54.63,
        54.69,
        50.56,
        52.5,
        3361000.0,
        0.0,
        1.0,
        37.270808680835,
        37.311743122,
        34.494089088468,
        35.817636019474,
        3361000.0],
       [u'A',
        u'2000-12-21',
        52.5,
        53.84,
        49.88,
        51.38,
        2878200.0,
        0.0,
        1.0,
        35.817636019474,
        36.731838538828,
        34.030165421931,
        35.053526451058,
        2878200.0],
       [u'A',
        u'2000-12-22',
        51.13,
        55.75,
        51.06,
        54.69,
        1830300.0,
        0.0,
        1.0,
        34.882966279537,
        38.034918249251,
        34.835209431511,
        37.311743122,
        1830300.0],
       [u'A',
        u'2000-12-26',
        54.75,
        55.19,
        53.0,
        53.5,
        1129500.0,
        0.0,
        1.0,
        37.352677563166,
        37.652863465043,
        36.158756362516,
        36.499876705559,
        1129500.0],
       [u'A',
        u'2000-12-27',
        53.56,
        56.0,
        53.56,
        55.94,
        2681300.0,
        0.0,
        1.0,
        36.540811146724,
        38.205478420772,
        36.540811146724,
        38.164543979607,
        2681300.0],
       [u'A',
        u'2000-12-28',
        55.63,
        56.38,
        54.38,
        55.31,
        1261300.0,
        0.0,
        1.0,
        37.95304936692,
        38.464729881484,
        37.100248509314,
        37.734732347373,
        1261300.0],
       [u'A',
        u'2000-12-29',
        55.38,
        56.44,
        53.63,
        54.75,
        1480200.0,
        0.0,
        1.0,
        37.782489195399,
        38.50566432265,
        36.58856799475,
        37.352677563166,
        1480200.0],
       [u'A',
        u'2001-01-02',
        53.88,
        53.88,
        49.06,
        50.88,
        1617800.0,
        0.0,
        1.0,
        36.759128166271,
        36.759128166271,
        33.470728059341,
        34.712406108016,
        1617800.0],
       [u'A',
        u'2001-01-03',
        49.13,
        56.5,
        47.56,
        56.13,
        3220800.0,
        0.0,
        1.0,
        33.518484907367,
        38.546598763815,
        32.447367030213,
        38.294169709963,
        3220800.0],
       [u'A',
        u'2001-01-04',
        56.88,
        59.69,
        55.31,
        58.25,
        3146200.0,
        0.0,
        1.0,
        38.805850224527,
        40.722946552426,
        37.734732347373,
        39.740519964464,
        3146200.0],
       [u'A',
        u'2001-01-05',
        57.25,
        58.25,
        53.5,
        55.06,
        2344100.0,
        0.0,
        1.0,
        39.058279278379,
        39.740519964464,
        36.499876705559,
        37.564172175852,
        2344100.0],
       [u'A',
        u'2001-01-08',
        54.25,
        55.75,
        52.31,
        53.25,
        1626100.0,
        0.0,
        1.0,
        37.011557220123,
        38.034918249251,
        35.688010289118,
        36.329316534038,
        1626100.0],
       [u'A',
        u'2001-01-09',
        53.5,
        54.94,
        51.81,
        53.0,
        1769800.0,
        0.0,
        1.0,
        36.499876705559,
        37.482303293522,
        35.346889946075,
        36.158756362516,
        1769800.0],
       [u'A',
        u'2001-01-10',
        52.5,
        55.56,
        52.38,
        55.31,
        1721000.0,
        0.0,
        1.0,
        35.817636019474,
        37.905292518895,
        35.735767137144,
        37.734732347373,
        1721000.0],
       [u'A',
        u'2001-01-11',
        55.88,
        57.69,
        53.69,
        57.56,
        2515800.0,
        0.0,
        1.0,
        38.123609538442,
        39.358465180256,
        36.629502435915,
        39.269773891065,
        2515800.0],
       [u'A',
        u'2001-01-12',
        57.56,
        58.0,
        55.69,
        56.13,
        1823500.0,
        0.0,
        1.0,
        39.269773891065,
        39.569959792942,
        37.993983808086,
        38.294169709963,
        1823500.0],
       [u'A',
        u'2001-01-16',
        56.25,
        58.25,
        55.31,
        58.19,
        1860500.0,
        0.0,
        1.0,
        38.376038592293,
        39.740519964464,
        37.734732347373,
        39.699585523299,
        1860500.0],
       [u'A',
        u'2001-01-17',
        58.94,
        63.19,
        58.94,
        61.94,
        5996500.0,
        0.0,
        1.0,
        40.211266037863,
        43.110788953725,
        40.211266037863,
        42.257988096118,
        5996500.0],
       [u'A',
        u'2001-01-18',
        61.94,
        68.0,
        60.38,
        67.56,
        4991800.0,
        0.0,
        1.0,
        42.257988096118,
        46.392366653795,
        41.193692625825,
        46.092180751917,
        4991800.0],
       [u'A',
        u'2001-01-19',
        67.5,
        67.5,
        64.56,
        65.56,
        4424300.0,
        0.0,
        1.0,
        46.051246310752,
        46.051246310752,
        44.045458693661,
        44.727699379747,
        4424300.0],
       [u'A',
        u'2001-01-22',
        65.63,
        65.63,
        61.38,
        62.75,
        2018900.0,
        0.0,
        1.0,
        44.775456227773,
        44.775456227773,
        41.87593331191,
        42.810603051847,
        2018900.0],
       [u'A',
        u'2001-01-23',
        62.69,
        64.0,
        61.5,
        62.75,
        2194500.0,
        0.0,
        1.0,
        42.769668610682,
        43.663403909454,
        41.957802194241,
        42.810603051847,
        2194500.0],
       [u'A',
        u'2001-01-24',
        63.0,
        63.38,
        58.0,
        58.0,
        3779600.0,
        0.0,
        1.0,
        42.981163223369,
        43.240414684081,
        39.569959792942,
        39.569959792942,
        3779600.0],
       [u'A',
        u'2001-01-25',
        56.69,
        57.38,
        54.0,
        55.25,
        3064600.0,
        0.0,
        1.0,
        38.676224494171,
        39.14697056757,
        36.840997048602,
        37.693797906208,
        3064600.0],
       [u'A',
        u'2001-01-26',
        54.31,
        55.69,
        52.69,
        54.63,
        2668000.0,
        0.0,
        1.0,
        37.052491661288,
        37.993983808086,
        35.94726174983,
        37.270808680835,
        2668000.0],
       [u'A',
        u'2001-01-29',
        55.5,
        56.5,
        54.0,
        54.42,
        2182600.0,
        0.0,
        1.0,
        37.864358077729,
        38.546598763815,
        36.840997048602,
        37.127538136757,
        2182600.0],
       [u'A',
        u'2001-01-30',
        55.35,
        55.35,
        54.5,
        54.75,
        1709200.0,
        0.0,
        1.0,
        37.762021974817,
        37.762021974817,
        37.182117391644,
        37.352677563166,
        1709200.0],
       [u'A',
        u'2001-01-31',
        55.0,
        55.75,
        53.3,
        54.55,
        1828000.0,
        0.0,
        1.0,
        37.523237734687,
        38.034918249251,
        36.363428568342,
        37.216229425948,
        1828000.0],
       [u'A',
        u'2001-02-01',
        53.4,
        54.05,
        52.25,
        53.8,
        2496800.0,
        0.0,
        1.0,
        36.43165263695,
        36.875109082906,
        35.647075847952,
        36.704548911385,
        2496800.0],
       [u'A',
        u'2001-02-02',
        53.87,
        54.74,
        52.0,
        52.2,
        2160900.0,
        0.0,
        1.0,
        36.752305759411,
        37.345855156305,
        35.476515676431,
        35.612963813648,
        2160900.0],
       [u'A',
        u'2001-02-05',
        53.6,
        53.94,
        48.0,
        49.2,
        2645900.0,
        0.0,
        1.0,
        36.568100774168,
        36.800062607436,
        32.74755293209,
        33.566241755393,
        2645900.0],
       [u'A',
        u'2001-02-06',
        49.4,
        52.5,
        49.4,
        50.97,
        2320000.0,
        0.0,
        1.0,
        33.70268989261,
        35.817636019474,
        33.70268989261,
        34.773807769763,
        2320000.0],
       [u'A',
        u'2001-02-07',
        50.4,
        51.1,
        49.15,
        50.14,
        1269300.0,
        0.0,
        1.0,
        34.384930578695,
        34.862499058954,
        33.532129721088,
        34.207548000313,
        1269300.0],
       [u'A',
        u'2001-02-08',
        50.25,
        54.74,
        50.25,
        54.21,
        2953600.0,
        0.0,
        1.0,
        34.282594475782,
        37.345855156305,
        34.282594475782,
        36.984267592679,
        2953600.0],
       [u'A',
        u'2001-02-09',
        54.22,
        54.72,
        52.02,
        52.5,
        1748000.0,
        0.0,
        1.0,
        36.99108999954,
        37.332210342583,
        35.490160490153,
        35.817636019474,
        1748000.0],
       [u'A',
        u'2001-02-12',
        52.3,
        52.99,
        50.35,
        51.12,
        2156200.0,
        0.0,
        1.0,
        35.681187882257,
        36.151933955656,
        34.350818544391,
        34.876143872676,
        2156200.0],
       [u'A',
        u'2001-02-13',
        51.0,
        51.6,
        47.36,
        47.37,
        3140000.0,
        0.0,
        1.0,
        34.794274990346,
        35.203619401997,
        32.310918892996,
        32.317741299857,
        3140000.0],
       [u'A',
        u'2001-02-14',
        48.25,
        49.0,
        47.77,
        48.0,
        3077500.0,
        0.0,
        1.0,
        32.918113103612,
        33.429793618176,
        32.590637574291,
        32.74755293209,
        3077500.0],
       [u'A',
        u'2001-02-15',
        49.7,
        55.0,
        49.59,
        53.85,
        2828900.0,
        0.0,
        1.0,
        33.907362098435,
        37.523237734687,
        33.832315622966,
        36.738660945689,
        2828900.0],
       [u'A',
        u'2001-02-16',
        50.0,
        50.5,
        48.65,
        50.0,
        3580200.0,
        0.0,
        1.0,
        34.112034304261,
        34.453154647303,
        33.191009378046,
        34.112034304261,
        3580200.0],
       [u'A',
        u'2001-02-20',
        49.2,
        49.45,
        43.0,
        44.0,
        4540600.0,
        0.0,
        1.0,
        33.566241755393,
        33.736801926914,
        29.336349501664,
        30.018590187749,
        4540600.0],
       [u'A',
        u'2001-02-21',
        42.0,
        42.25,
        39.2,
        40.2,
        6697900.0,
        0.0,
        1.0,
        28.654108815579,
        28.8246689871,
        26.74383489454,
        27.426075580626,
        6697900.0],
       [u'A',
        u'2001-02-22',
        39.95,
        40.6,
        38.5,
        39.07,
        4806900.0,
        0.0,
        1.0,
        27.255515409104,
        27.69897185506,
        26.266266414281,
        26.655143605349,
        4806900.0],
       [u'A',
        u'2001-02-23',
        39.08,
        39.37,
        35.55,
        38.3,
        3868800.0,
        0.0,
        1.0,
        26.66196601221,
        26.859815811175,
        24.253656390329,
        26.129818277064,
        3868800.0],
       [u'A',
        u'2001-02-26',
        37.69,
        38.75,
        37.3,
        38.3,
        2662500.0,
        0.0,
        1.0,
        25.713651458552,
        26.436826585802,
        25.447577590979,
        26.129818277064,
        2662500.0],
       [u'A',
        u'2001-02-27',
        37.75,
        39.66,
        36.89,
        38.15,
        2608300.0,
        0.0,
        1.0,
        25.754585899717,
        27.05766561014,
        25.167858909684,
        26.027482174151,
        2608300.0],
       [u'A',
        u'2001-02-28',
        38.4,
        38.8,
        35.8,
        36.0,
        2525900.0,
        0.0,
        1.0,
        26.198042345672,
        26.470938620106,
        24.424216561851,
        24.560664699068,
        2525900.0],
       [u'A',
        u'2001-03-01',
        35.9,
        39.0,
        34.4,
        38.31,
        3641500.0,
        0.0,
        1.0,
        24.492440630459,
        26.607386757323,
        23.469079601331,
        26.136640683925,
        3641500.0],
       [u'A',
        u'2001-03-02',
        36.45,
        40.24,
        36.44,
        38.03,
        2455000.0,
        0.0,
        1.0,
        24.867673007806,
        27.453365208069,
        24.860850600945,
        25.945613291821,
        2455000.0],
       [u'A',
        u'2001-03-05',
        38.04,
        39.23,
        37.1,
        38.05,
        1454100.0,
        0.0,
        1.0,
        25.952435698682,
        26.764302115123,
        25.311129453761,
        25.959258105542,
        1454100.0],
       [u'A',
        u'2001-03-06',
        39.1,
        41.32,
        39.1,
        40.6,
        2673600.0,
        0.0,
        1.0,
        26.675610825932,
        28.190185149041,
        26.675610825932,
        27.69897185506,
        2673600.0],
       [u'A',
        u'2001-03-07',
        42.3,
        42.38,
        40.6,
        40.96,
        1957600.0,
        0.0,
        1.0,
        28.858781021405,
        28.913360276291,
        27.69897185506,
        27.94457850205,
        1957600.0],
       [u'A',
        u'2001-03-08',
        40.97,
        41.22,
        39.6,
        40.0,
        2030200.0,
        0.0,
        1.0,
        27.951400908911,
        28.121961080433,
        27.016731168975,
        27.289627443409,
        2030200.0],
       [u'A',
        u'2001-03-09',
        39.1,
        39.47,
        36.65,
        37.05,
        2017700.0,
        0.0,
        1.0,
        26.675610825932,
        26.928039879783,
        25.004121145023,
        25.277017419457,
        2017700.0],
       [u'A',
        u'2001-03-12',
        36.0,
        36.6,
        35.0,
        35.01,
        2435000.0,
        0.0,
        1.0,
        24.560664699068,
        24.970009110719,
        23.878424012983,
        23.885246419843,
        2435000.0],
       [u'A',
        u'2001-03-13',
        35.6,
        36.88,
        35.15,
        36.58,
        1895400.0,
        0.0,
        1.0,
        24.287768424634,
        25.161036502823,
        23.980760115895,
        24.956364296997,
        1895400.0],
       [u'A',
        u'2001-03-14',
        35.2,
        36.69,
        34.94,
        35.3,
        2636100.0,
        0.0,
        1.0,
        24.0148721502,
        25.031410772467,
        23.837489571817,
        24.083096218808,
        2636100.0],
       [u'A',
        u'2001-03-15',
        35.5,
        36.57,
        34.53,
        34.85,
        2061700.0,
        0.0,
        1.0,
        24.219544356025,
        24.949541890136,
        23.557770890522,
        23.77608791007,
        2061700.0],
       [u'A',
        u'2001-03-16',
        34.4,
        35.75,
        33.96,
        34.75,
        2965600.0,
        0.0,
        1.0,
        23.469079601331,
        24.390104527546,
        23.168893699454,
        23.707863841461,
        2965600.0],
       [u'A',
        u'2001-03-19',
        34.6,
        37.55,
        33.61,
        36.99,
        1720700.0,
        0.0,
        1.0,
        23.605527738548,
        25.6181377625,
        22.930109459324,
        25.236082978292,
        1720700.0],
       [u'A',
        u'2001-03-20',
        36.25,
        36.25,
        34.3,
        34.3,
        3020900.0,
        0.0,
        1.0,
        24.731224870589,
        24.731224870589,
        23.400855532723,
        23.400855532723,
        3020900.0],
       [u'A',
        u'2001-03-21',
        33.02,
        33.74,
        29.6,
        31.6,
        6207200.0,
        0.0,
        1.0,
        22.527587454534,
        23.018800748515,
        20.194324308122,
        21.558805680293,
        6207200.0],
       [u'A',
        u'2001-03-22',
        31.9,
        34.98,
        31.84,
        34.8,
        3294000.0,
        0.0,
        1.0,
        21.763477886118,
        23.864779199261,
        21.722543444953,
        23.741975875765,
        3294000.0],
       [u'A',
        u'2001-03-23',
        34.8,
        39.5,
        34.79,
        37.83,
        3630000.0,
        0.0,
        1.0,
        23.741975875765,
        26.948507100366,
        23.735153468905,
        25.809165154604,
        3630000.0],
       [u'A',
        u'2001-03-26',
        37.12,
        37.64,
        36.14,
        37.07,
        2086500.0,
        0.0,
        1.0,
        25.324774267483,
        25.679539424247,
        24.65617839512,
        25.290662233179,
        2086500.0],
       [u'A',
        u'2001-03-27',
        37.0,
        37.03,
        35.74,
        36.93,
        1927600.0,
        0.0,
        1.0,
        25.242905385153,
        25.263372605736,
        24.383282120686,
        25.195148537127,
        1927600.0],
       [u'A',
        u'2001-03-28',
        35.1,
        35.22,
        32.5,
        32.7,
        3046400.0,
        0.0,
        1.0,
        23.946648081591,
        24.028516963921,
        22.172822297769,
        22.309270434987,
        3046400.0],
       [u'A',
        u'2001-03-29',
        32.0,
        33.18,
        30.0,
        30.0,
        6253600.0,
        0.0,
        1.0,
        21.831701954727,
        22.636745964307,
        20.467220582556,
        20.467220582556,
        6253600.0],
       [u'A',
        u'2001-03-30',
        30.6,
        31.83,
        30.2,
        30.73,
        3849100.0,
        0.0,
        1.0,
        20.876564994208,
        21.715721038092,
        20.603668719773,
        20.965256283399,
        3849100.0],
       [u'A',
        u'2001-04-02',
        32.25,
        32.57,
        30.3,
        30.85,
        2512500.0,
        0.0,
        1.0,
        22.002262126248,
        22.220579145795,
        20.671892788382,
        21.047125165729,
        2512500.0],
       [u'A',
        u'2001-04-03',
        30.1,
        30.5,
        28.0,
        29.5,
        3635800.0,
        0.0,
        1.0,
        20.535444651165,
        20.808340925599,
        19.102739210386,
        20.126100239514,
        3635800.0],
       [u'A',
        u'2001-04-04',
        28.71,
        29.4,
        27.76,
        28.09,
        2052600.0,
        0.0,
        1.0,
        19.587130097507,
        20.057876170905,
        18.939001445726,
        19.164140872134,
        2052600.0],
       [u'A',
        u'2001-04-05',
        28.75,
        31.2,
        28.71,
        30.62,
        2396600.0,
        0.0,
        1.0,
        19.61441972495,
        21.285909405859,
        19.587130097507,
        20.890209807929,
        2396600.0],
       [u'A',
        u'2001-04-06',
        26.0,
        27.9,
        25.0,
        27.8,
        5268200.0,
        0.0,
        1.0,
        17.738257838216,
        19.034515141777,
        17.05601715213,
        18.966291073169,
        5268200.0],
       [u'A',
        u'2001-04-09',
        27.52,
        28.26,
        27.03,
        27.6,
        2070200.0,
        0.0,
        1.0,
        18.775263681065,
        19.280121788768,
        18.440965744883,
        18.829842935952,
        2070200.0],
       [u'A',
        u'2001-04-10',
        28.2,
        30.48,
        27.86,
        29.85,
        2123700.0,
        0.0,
        1.0,
        19.239187347603,
        20.794696111877,
        19.007225514334,
        20.364884479644,
        2123700.0],
       [u'A',
        u'2001-04-11',
        31.25,
        32.6,
        31.0,
        31.68,
        2382700.0,
        0.0,
        1.0,
        21.320021440163,
        22.241046366378,
        21.149461268642,
        21.61338493518,
        2382700.0],
       [u'A',
        u'2001-04-12',
        31.0,
        34.5,
        30.01,
        33.96,
        2387400.0,
        0.0,
        1.0,
        21.149461268642,
        23.53730366994,
        20.474042989417,
        23.168893699454,
        2387400.0],
       [u'A',
        u'2001-04-16',
        33.2,
        33.55,
        32.32,
        33.32,
        1555000.0,
        0.0,
        1.0,
        22.650390778029,
        22.889175018159,
        22.050018974274,
        22.732259660359,
        1555000.0],
       [u'A',
        u'2001-04-17',
        32.25,
        33.97,
        31.77,
        33.33,
        1290100.0,
        0.0,
        1.0,
        22.002262126248,
        23.175716106315,
        21.674786596927,
        22.73908206722,
        1290100.0],
       [u'A',
        u'2001-04-18',
        34.5,
        38.88,
        34.2,
        37.99,
        3571800.0,
        0.0,
        1.0,
        23.53730366994,
        26.525517874993,
        23.332631464114,
        25.918323664377,
        3571800.0],
       [u'A',
        u'2001-04-19',
        37.39,
        40.5,
        37.39,
        38.99,
        2779900.0,
        0.0,
        1.0,
        25.508979252726,
        27.630747786451,
        25.508979252726,
        26.600564350463,
        2779900.0],
       [u'A',
        u'2001-04-20',
        38.98,
        41.0,
        38.51,
        40.4,
        2551700.0,
        0.0,
        1.0,
        26.593741943602,
        27.971868129494,
        26.273088821142,
        27.562523717843,
        2551700.0],
       [u'A',
        u'2001-04-23',
        39.5,
        40.0,
        38.22,
        40.0,
        2052900.0,
        0.0,
        1.0,
        26.948507100366,
        27.289627443409,
        26.075239022177,
        27.289627443409,
        2052900.0],
       [u'A',
        u'2001-04-24',
        38.9,
        39.25,
        36.5,
        37.22,
        1933000.0,
        0.0,
        1.0,
        26.539162688715,
        26.777946928845,
        24.90178504211,
        25.392998336092,
        1933000.0],
       [u'A',
        u'2001-04-25',
        37.0,
        39.0,
        36.53,
        38.83,
        1668300.0,
        0.0,
        1.0,
        25.242905385153,
        26.607386757323,
        24.922252262693,
        26.491405840689,
        1668300.0],
       [u'A',
        u'2001-04-26',
        38.25,
        40.97,
        38.0,
        38.01,
        2125200.0,
        0.0,
        1.0,
        26.095706242759,
        27.951400908911,
        25.925146071238,
        25.931968478099,
        2125200.0],
       [u'A',
        u'2001-04-27',
        39.4,
        40.2,
        38.25,
        38.79,
        1225700.0,
        0.0,
        1.0,
        26.880283031757,
        27.426075580626,
        26.095706242759,
        26.464116213245,
        1225700.0],
       [u'A',
        u'2001-04-30',
        39.4,
        40.25,
        38.84,
        39.01,
        1208900.0,
        0.0,
        1.0,
        26.880283031757,
        27.46018761493,
        26.49822824755,
        26.614209164184,
        1208900.0],
       [u'A',
        u'2001-05-01',
        37.9,
        39.45,
        37.54,
        39.2,
        1532500.0,
        0.0,
        1.0,
        25.85692200263,
        26.914395066062,
        25.611315355639,
        26.74383489454,
        1532500.0],
       [u'A',
        u'2001-05-02',
        39.9,
        40.45,
        39.21,
        39.72,
        1288400.0,
        0.0,
        1.0,
        27.2214033748,
        27.596635752147,
        26.750657301401,
        27.098600051305,
        1288400.0],
       [u'A',
        u'2001-05-03',
        39.25,
        39.25,
        37.88,
        38.45,
        1188600.0,
        0.0,
        1.0,
        26.777946928845,
        26.777946928845,
        25.843277188908,
        26.232154379977,
        1188600.0],
       [u'A',
        u'2001-05-04',
        38.2,
        39.1,
        37.1,
        38.37,
        1786500.0,
        0.0,
        1.0,
        26.061594208455,
        26.675610825932,
        25.311129453761,
        26.17757512509,
        1786500.0],
       [u'A',
        u'2001-05-07',
        37.6,
        39.09,
        37.4,
        38.74,
        1478300.0,
        0.0,
        1.0,
        25.652249796804,
        26.668788419071,
        25.515801659587,
        26.430004178941,
        1478300.0],
       [u'A',
        u'2001-05-08',
        38.9,
        39.6,
        37.83,
        38.42,
        1145400.0,
        0.0,
        1.0,
        26.539162688715,
        27.016731168975,
        25.809165154604,
        26.211687159394,
        1145400.0],
       [u'A',
        u'2001-05-09',
        37.9,
        39.94,
        37.5,
        39.0,
        1800700.0,
        0.0,
        1.0,
        25.85692200263,
        27.248693002243,
        25.584025728196,
        26.607386757323,
        1800700.0],
       [u'A',
        u'2001-05-10',
        40.0,
        41.18,
        39.06,
        39.21,
        1765500.0,
        0.0,
        1.0,
        27.289627443409,
        28.094671452989,
        26.648321198488,
        26.750657301401,
        1765500.0],
       [u'A',
        u'2001-05-11',
        39.3,
        40.38,
        39.3,
        39.69,
        1473400.0,
        0.0,
        1.0,
        26.812058963149,
        27.548878904121,
        26.812058963149,
        27.078132830722,
        1473400.0],
       [u'A',
        u'2001-05-14',
        39.82,
        39.83,
        38.02,
        38.75,
        1249700.0,
        0.0,
        1.0,
        27.166824119913,
        27.173646526774,
        25.93879088496,
        26.436826585802,
        1249700.0],
       [u'A',
        u'2001-05-15',
        37.85,
        38.88,
        37.0,
        37.45,
        1693300.0,
        0.0,
        1.0,
        25.822809968325,
        26.525517874993,
        25.242905385153,
        25.549913693891,
        1693300.0],
       [u'A',
        u'2001-05-16',
        36.46,
        38.5,
        35.5,
        38.5,
        2288300.0,
        0.0,
        1.0,
        24.874495414667,
        26.266266414281,
        24.219544356025,
        26.266266414281,
        2288300.0],
       [u'A',
        u'2001-05-17',
        38.0,
        39.5,
        37.52,
        38.72,
        2139900.0,
        0.0,
        1.0,
        25.925146071238,
        26.948507100366,
        25.597670541917,
        26.41635936522,
        2139900.0],
       [u'A',
        u'2001-05-18',
        38.0,
        38.95,
        35.7,
        36.0,
        6660100.0,
        0.0,
        1.0,
        25.925146071238,
        26.573274723019,
        24.355992493242,
        24.560664699068,
        6660100.0],
       [u'A',
        u'2001-05-21',
        36.0,
        38.3,
        35.7,
        38.0,
        4515700.0,
        0.0,
        1.0,
        24.560664699068,
        26.129818277064,
        24.355992493242,
        25.925146071238,
        4515700.0],
       [u'A',
        u'2001-05-22',
        38.75,
        39.8,
        37.83,
        39.25,
        2514100.0,
        0.0,
        1.0,
        26.436826585802,
        27.153179306192,
        25.809165154604,
        26.777946928845,
        2514100.0],
       [u'A',
        u'2001-05-23',
        38.35,
        38.44,
        37.5,
        37.93,
        2492000.0,
        0.0,
        1.0,
        26.163930311368,
        26.225331973116,
        25.584025728196,
        25.877389223212,
        2492000.0],
       [u'A',
        u'2001-05-24',
        37.93,
        38.1,
        36.3,
        36.3,
        1964900.0,
        0.0,
        1.0,
        25.877389223212,
        25.993370139847,
        24.765336904893,
        24.765336904893,
        1964900.0],
       [u'A',
        u'2001-05-25',
        36.8,
        38.5,
        36.8,
        37.69,
        1471800.0,
        0.0,
        1.0,
        25.106457247936,
        26.266266414281,
        25.106457247936,
        25.713651458552,
        1471800.0],
       [u'A',
        u'2001-05-29',
        37.65,
        37.65,
        35.54,
        35.95,
        1590400.0,
        0.0,
        1.0,
        25.686361831108,
        25.686361831108,
        24.246833983469,
        24.526552664763,
        1590400.0],
       [u'A',
        u'2001-05-30',
        34.1,
        34.8,
        32.72,
        32.87,
        2537500.0,
        0.0,
        1.0,
        23.264407395506,
        23.741975875765,
        22.322915248708,
        22.425251351621,
        2537500.0],
       [u'A',
        u'2001-05-31',
        33.0,
        34.0,
        32.25,
        33.54,
        3306700.0,
        0.0,
        1.0,
        22.513942640812,
        23.196183326897,
        22.002262126248,
        22.882352611298,
        3306700.0],
       [u'A',
        u'2001-06-01',
        34.5,
        34.75,
        32.16,
        33.97,
        1709300.0,
        0.0,
        1.0,
        23.53730366994,
        23.707863841461,
        21.940860464501,
        23.175716106315,
        1709300.0],
       [u'A',
        u'2001-06-04',
        34.0,
        34.19,
        33.3,
        33.5,
        1579000.0,
        0.0,
        1.0,
        23.196183326897,
        23.325809057253,
        22.718614846638,
        22.855062983855,
        1579000.0],
       [u'A',
        u'2001-06-05',
        33.5,
        34.35,
        33.5,
        34.1,
        2352500.0,
        0.0,
        1.0,
        22.855062983855,
        23.434967567027,
        22.855062983855,
        23.264407395506,
        2352500.0],
       [u'A',
        u'2001-06-06',
        34.1,
        34.9,
        33.52,
        34.27,
        1434900.0,
        0.0,
        1.0,
        23.264407395506,
        23.810199944374,
        22.868707797576,
        23.38038831214,
        1434900.0],
       [u'A',
        u'2001-06-07',
        33.5,
        36.45,
        33.5,
        35.84,
        2095300.0,
        0.0,
        1.0,
        22.855062983855,
        24.867673007806,
        22.855062983855,
        24.451506189294,
        2095300.0],
       [u'A',
        u'2001-06-08',
        35.24,
        35.7,
        34.85,
        35.01,
        941100.0,
        0.0,
        1.0,
        24.042161777643,
        24.355992493242,
        23.77608791007,
        23.885246419843,
        941100.0],
       [u'A',
        u'2001-06-11',
        34.4,
        35.0,
        33.16,
        33.77,
        2280700.0,
        0.0,
        1.0,
        23.469079601331,
        23.878424012983,
        22.623101150586,
        23.039267969098,
        2280700.0],
       [u'A',
        u'2001-06-12',
        33.02,
        33.65,
        32.1,
        33.3,
        2057000.0,
        0.0,
        1.0,
        22.527587454534,
        22.957399086767,
        21.899926023335,
        22.718614846638,
        2057000.0],
       [u'A',
        u'2001-06-13',
        33.5,
        33.93,
        32.64,
        32.64,
        1136400.0,
        0.0,
        1.0,
        22.855062983855,
        23.148426478871,
        22.268335993821,
        22.268335993821,
        1136400.0],
       [u'A',
        u'2001-06-14',
        32.15,
        32.16,
        30.35,
        31.1,
        2383500.0,
        0.0,
        1.0,
        21.93403805764,
        21.940860464501,
        20.706004822686,
        21.21768533725,
        2383500.0],
       [u'A',
        u'2001-06-15',
        30.02,
        30.96,
        29.0,
        30.46,
        2862400.0,
        0.0,
        1.0,
        20.480865396278,
        21.122171641198,
        19.784979896471,
        20.781051298156,
        2862400.0],
       [u'A',
        u'2001-06-18',
        30.3,
        31.07,
        29.28,
        30.0,
        1783000.0,
        0.0,
        1.0,
        20.671892788382,
        21.197218116668,
        19.976007288575,
        20.467220582556,
        1783000.0],
       [u'A',
        u'2001-06-19',
        30.5,
        30.68,
        29.0,
        29.32,
        2357900.0,
        0.0,
        1.0,
        20.808340925599,
        20.931144249094,
        19.784979896471,
        20.003296916018,
        2357900.0],
       [u'A',
        u'2001-06-20',
        29.32,
        29.4,
        27.25,
        28.42,
        3309100.0,
        0.0,
        1.0,
        20.003296916018,
        20.057876170905,
        18.591058695822,
        19.389280298542,
        3309100.0],
       [u'A',
        u'2001-06-21',
        28.75,
        29.65,
        28.32,
        29.58,
        2232200.0,
        0.0,
        1.0,
        19.61441972495,
        20.228436342427,
        19.321056229933,
        20.180679494401,
        2232200.0],
       [u'A',
        u'2001-06-22',
        29.0,
        30.36,
        28.76,
        29.4,
        2458300.0,
        0.0,
        1.0,
        19.784979896471,
        20.712827229547,
        19.621242131811,
        20.057876170905,
        2458300.0],
       [u'A',
        u'2001-06-25',
        29.45,
        29.95,
        29.2,
        29.65,
        1656600.0,
        0.0,
        1.0,
        20.09198820521,
        20.433108548252,
        19.921428033688,
        20.228436342427,
        1656600.0],
       [u'A',
        u'2001-06-26',
        29.3,
        29.95,
        28.48,
        29.2,
        2509000.0,
        0.0,
        1.0,
        19.989652102297,
        20.433108548252,
        19.430214739707,
        19.921428033688,
        2509000.0],
       [u'A',
        u'2001-06-27',
        28.45,
        30.5,
        28.45,
        29.85,
        2418000.0,
        0.0,
        1.0,
        19.409747519124,
        20.808340925599,
        19.409747519124,
        20.364884479644,
        2418000.0],
       [u'A',
        u'2001-06-28',
        30.0,
        31.9,
        30.0,
        31.69,
        3012200.0,
        0.0,
        1.0,
        20.467220582556,
        21.763477886118,
        20.467220582556,
        21.62020734204,
        3012200.0],
       [u'A',
        u'2001-06-29',
        31.5,
        34.1,
        30.8,
        32.5,
        4018400.0,
        0.0,
        1.0,
        21.490581611684,
        23.264407395506,
        21.013013131425,
        22.172822297769,
        4018400.0],
       [u'A',
        u'2001-07-02',
        32.5,
        33.5,
        32.02,
        33.09,
        1539600.0,
        0.0,
        1.0,
        22.172822297769,
        22.855062983855,
        21.845346768449,
        22.57534430256,
        1539600.0],
       [u'A',
        u'2001-07-03',
        33.2,
        33.2,
        32.32,
        32.52,
        671600.0,
        0.0,
        1.0,
        22.650390778029,
        22.650390778029,
        22.050018974274,
        22.186467111491,
        671600.0],
       [u'A',
        u'2001-07-05',
        32.51,
        32.94,
        31.55,
        32.17,
        1484400.0,
        0.0,
        1.0,
        22.17964470463,
        22.473008199647,
        21.524693645989,
        21.947682871361,
        1484400.0],
       [u'A',
        u'2001-07-06',
        31.9,
        31.9,
        29.14,
        30.15,
        1592200.0,
        0.0,
        1.0,
        21.763477886118,
        21.763477886118,
        19.880493592523,
        20.569556685469,
        1592200.0],
       [u'A',
        u'2001-07-09',
        30.15,
        30.65,
        29.61,
        29.91,
        992800.0,
        0.0,
        1.0,
        20.569556685469,
        20.910677028512,
        20.201146714983,
        20.405818920809,
        992800.0],
       [u'A',
        u'2001-07-10',
        29.91,
        30.4,
        28.08,
        28.3,
        2423300.0,
        0.0,
        1.0,
        20.405818920809,
        20.740116856991,
        19.157318465273,
        19.307411416212,
        2423300.0],
       [u'A',
        u'2001-07-11',
        28.35,
        28.75,
        26.2,
        26.87,
        3102100.0,
        0.0,
        1.0,
        19.341523450516,
        19.61441972495,
        17.874705975433,
        18.33180723511,
        3102100.0],
       [u'A',
        u'2001-07-12',
        28.5,
        31.5,
        28.3,
        30.74,
        2467100.0,
        0.0,
        1.0,
        19.443859553429,
        21.490581611684,
        19.307411416212,
        20.972078690259,
        2467100.0],
       [u'A',
        u'2001-07-13',
        30.75,
        32.09,
        29.82,
        30.3,
        1990000.0,
        0.0,
        1.0,
        20.97890109712,
        21.893103616475,
        20.344417259061,
        20.671892788382,
        1990000.0],
       [u'A',
        u'2001-07-16',
        30.15,
        30.64,
        28.5,
        28.9,
        1595000.0,
        0.0,
        1.0,
        20.569556685469,
        20.903854621651,
        19.443859553429,
        19.716755827863,
        1595000.0],
       [u'A',
        u'2001-07-17',
        28.25,
        29.94,
        28.01,
        29.5,
        2097400.0,
        0.0,
        1.0,
        19.273299381907,
        20.426286141391,
        19.109561617247,
        20.126100239514,
        2097400.0],
       [u'A',
        u'2001-07-18',
        28.1,
        29.24,
        28.1,
        28.49,
        1045200.0,
        0.0,
        1.0,
        19.170963278995,
        19.948717661132,
        19.170963278995,
        19.437037146568,
        1045200.0],
       [u'A',
        u'2001-07-19',
        28.64,
        30.5,
        28.64,
        28.96,
        1346400.0,
        0.0,
        1.0,
        19.539373249481,
        20.808340925599,
        19.539373249481,
        19.757690269028,
        1346400.0],
       [u'A',
        u'2001-07-20',
        28.71,
        29.38,
        27.9,
        28.9,
        1470400.0,
        0.0,
        1.0,
        19.587130097507,
        20.044231357184,
        19.034515141777,
        19.716755827863,
        1470400.0],
       [u'A',
        u'2001-07-23',
        28.99,
        29.35,
        27.55,
        27.71,
        1479600.0,
        0.0,
        1.0,
        19.77815748961,
        20.023764136601,
        18.795730901648,
        18.904889411421,
        1479600.0],
       [u'A',
        u'2001-07-24',
        27.6,
        27.95,
        27.0,
        27.45,
        1773100.0,
        0.0,
        1.0,
        18.829842935952,
        19.068627176082,
        18.420498524301,
        18.727506833039,
        1773100.0],
       [u'A',
        u'2001-07-25',
        27.4,
        27.84,
        26.92,
        27.84,
        1640200.0,
        0.0,
        1.0,
        18.693394798735,
        18.993580700612,
        18.365919269414,
        18.993580700612,
        1640200.0],
       [u'A',
        u'2001-07-26',
        28.0,
        29.55,
        27.65,
        29.21,
        1820700.0,
        0.0,
        1.0,
        19.102739210386,
        20.160212273818,
        18.863954970256,
        19.928250440549,
        1820700.0],
       [u'A',
        u'2001-07-27',
        29.15,
        30.19,
        28.81,
        30.1,
        1322700.0,
        0.0,
        1.0,
        19.887315999384,
        20.596846312913,
        19.655354166115,
        20.535444651165,
        1322700.0],
       [u'A',
        u'2001-07-30',
        29.05,
        29.95,
        29.05,
        29.42,
        1294000.0,
        0.0,
        1.0,
        19.819091930775,
        20.433108548252,
        19.819091930775,
        20.071520984627,
        1294000.0],
       [u'A',
        u'2001-07-31',
        29.05,
        30.3,
        28.43,
        28.61,
        1533100.0,
        0.0,
        1.0,
        19.819091930775,
        20.671892788382,
        19.396102705403,
        19.518906028898,
        1533100.0],
       [u'A',
        u'2001-08-01',
        29.5,
        31.89,
        29.22,
        31.75,
        2514000.0,
        0.0,
        1.0,
        20.126100239514,
        21.756655479257,
        19.93507284741,
        21.661141783206,
        2514000.0],
       [u'A',
        u'2001-08-02',
        31.5,
        32.7,
        31.15,
        31.75,
        1843300.0,
        0.0,
        1.0,
        21.490581611684,
        22.309270434987,
        21.251797371554,
        21.661141783206,
        1843300.0],
       [u'A',
        u'2001-08-03',
        31.2,
        32.35,
        31.12,
        31.3,
        1014400.0,
        0.0,
        1.0,
        21.285909405859,
        22.070486194857,
        21.231330150972,
        21.354133474467,
        1014400.0],
       [u'A',
        u'2001-08-06',
        31.31,
        31.48,
        30.51,
        30.82,
        1221600.0,
        0.0,
        1.0,
        21.360955881328,
        21.476936797963,
        20.81516333246,
        21.026657945146,
        1221600.0],
       [u'A',
        u'2001-08-07',
        30.82,
        31.8,
        30.5,
        31.03,
        1057300.0,
        0.0,
        1.0,
        21.026657945146,
        21.69525381751,
        20.808340925599,
        21.169928489224,
        1057300.0],
       [u'A',
        u'2001-08-08',
        29.7,
        30.6,
        28.92,
        28.95,
        2213000.0,
        0.0,
        1.0,
        20.262548376731,
        20.876564994208,
        19.730400641584,
        19.750867862167,
        2213000.0],
       [u'A',
        u'2001-08-09',
        28.95,
        28.95,
        28.02,
        28.64,
        1156200.0,
        0.0,
        1.0,
        19.750867862167,
        19.750867862167,
        19.116384024108,
        19.539373249481,
        1156200.0],
       [u'A',
        u'2001-08-10',
        28.65,
        28.8,
        27.51,
        28.59,
        1712100.0,
        0.0,
        1.0,
        19.546195656341,
        19.648531759254,
        18.768441274204,
        19.505261215176,
        1712100.0],
       [u'A',
        u'2001-08-13',
        29.0,
        29.35,
        28.2,
        28.92,
        861200.0,
        0.0,
        1.0,
        19.784979896471,
        20.023764136601,
        19.239187347603,
        19.730400641584,
        861200.0],
       [u'A',
        u'2001-08-14',
        29.0,
        29.7,
        29.0,
        29.54,
        1560700.0,
        0.0,
        1.0,
        19.784979896471,
        20.262548376731,
        19.784979896471,
        20.153389866957,
        1560700.0],
       [u'A',
        u'2001-08-15',
        28.9,
        29.18,
        27.46,
        27.85,
        1158100.0,
        0.0,
        1.0,
        19.716755827863,
        19.907783219967,
        18.7343292399,
        19.000403107473,
        1158100.0],
       [u'A',
        u'2001-08-16',
        27.25,
        27.75,
        26.6,
        27.5,
        1797600.0,
        0.0,
        1.0,
        18.591058695822,
        18.932179038865,
        18.147602249867,
        18.761618867343,
        1797600.0],
       [u'A',
        u'2001-08-17',
        27.3,
        27.3,
        26.18,
        26.45,
        1541400.0,
        0.0,
        1.0,
        18.625170730126,
        18.625170730126,
        17.861061161711,
        18.045266146954,
        1541400.0],
       [u'A',
        u'2001-08-20',
        26.1,
        26.36,
        25.29,
        26.09,
        1600900.0,
        0.0,
        1.0,
        17.806481906824,
        17.983864485206,
        17.253866951095,
        17.799659499963,
        1600900.0],
       [u'A',
        u'2001-08-21',
        25.2,
        27.0,
        24.3,
        26.45,
        5450000.0,
        0.0,
        1.0,
        17.192465289347,
        18.420498524301,
        16.578448671871,
        18.045266146954,
        5450000.0],
       [u'A',
        u'2001-08-22',
        26.85,
        26.99,
        26.0,
        26.38,
        1812800.0,
        0.0,
        1.0,
        18.318162421388,
        18.41367611744,
        17.738257838216,
        17.997509298928,
        1812800.0],
       [u'A',
        u'2001-08-23',
        26.38,
        26.79,
        25.89,
        26.17,
        2602100.0,
        0.0,
        1.0,
        17.997509298928,
        18.277227980223,
        17.663211362746,
        17.85423875485,
        2602100.0],
       [u'A',
        u'2001-08-24',
        26.5,
        28.05,
        26.3,
        27.79,
        1401000.0,
        0.0,
        1.0,
        18.079378181258,
        19.13685124469,
        17.942930044041,
        18.959468666308,
        1401000.0],
       [u'A',
        u'2001-08-27',
        28.03,
        28.04,
        27.05,
        27.16,
        982700.0,
        0.0,
        1.0,
        19.123206430969,
        19.130028837829,
        18.454610558605,
        18.529657034074,
        982700.0],
       [u'A',
        u'2001-08-28',
        27.2,
        27.8,
        26.76,
        27.5,
        1345100.0,
        0.0,
        1.0,
        18.556946661518,
        18.966291073169,
        18.25676075964,
        18.761618867343,
        1345100.0],
       [u'A',
        u'2001-08-29',
        27.4,
        27.6,
        27.11,
        27.15,
        1383900.0,
        0.0,
        1.0,
        18.693394798735,
        18.829842935952,
        18.49554499977,
        18.522834627214,
        1383900.0],
       [u'A',
        u'2001-08-30',
        26.9,
        27.55,
        25.91,
        26.05,
        1424500.0,
        0.0,
        1.0,
        18.352274455692,
        18.795730901648,
        17.676856176468,
        17.77236987252,
        1424500.0],
       [u'A',
        u'2001-08-31',
        25.9,
        26.75,
        25.85,
        26.5,
        1029700.0,
        0.0,
        1.0,
        17.670033769607,
        18.249938352779,
        17.635921735303,
        18.079378181258,
        1029700.0],
       [u'A',
        u'2001-09-04',
        26.35,
        26.95,
        25.6,
        25.83,
        1336500.0,
        0.0,
        1.0,
        17.977042078345,
        18.386386489997,
        17.465361563781,
        17.622276921581,
        1336500.0],
       [u'A',
        u'2001-09-05',
        25.35,
        25.78,
        24.26,
        24.6,
        2946400.0,
        0.0,
        1.0,
        17.29480139226,
        17.588164887277,
        16.551159044427,
        16.783120877696,
        2946400.0],
       [u'A',
        u'2001-09-06',
        24.35,
        24.55,
        23.2,
        24.0,
        2814000.0,
        0.0,
        1.0,
        16.612560706175,
        16.749008843392,
        15.827983917177,
        16.373776466045,
        2814000.0],
       [u'A',
        u'2001-09-07',
        23.2,
        24.25,
        23.11,
        23.35,
        1683200.0,
        0.0,
        1.0,
        15.827983917177,
        16.544336637566,
        15.766582255429,
        15.93032002009,
        1683200.0],
       [u'A',
        u'2001-09-10',
        22.5,
        23.18,
        22.36,
        23.05,
        1964500.0,
        0.0,
        1.0,
        15.350415436917,
        15.814339103455,
        15.254901740865,
        15.725647814264,
        1964500.0],
       [u'A',
        u'2001-09-17',
        21.15,
        22.48,
        21.0,
        21.75,
        2540000.0,
        0.0,
        1.0,
        14.429390510702,
        15.336770623196,
        14.32705440779,
        14.838734922353,
        2540000.0],
       [u'A',
        u'2001-09-18',
        21.5,
        22.4,
        21.0,
        21.73,
        1525100.0,
        0.0,
        1.0,
        14.668174750832,
        15.282191368309,
        14.32705440779,
        14.825090108632,
        1525100.0],
       [u'A',
        u'2001-09-19',
        23.0,
        23.0,
        20.11,
        22.75,
        2926800.0,
        0.0,
        1.0,
        15.69153577996,
        15.69153577996,
        13.719860197174,
        15.520975608439,
        2926800.0],
       [u'A',
        u'2001-09-20',
        22.01,
        22.01,
        20.54,
        20.82,
        2088600.0,
        0.0,
        1.0,
        15.016117500736,
        15.016117500736,
        14.01322369219,
        14.204251084294,
        2088600.0],
       [u'A',
        u'2001-09-21',
        20.45,
        20.45,
        18.0,
        20.15,
        2917100.0,
        0.0,
        1.0,
        13.951822030443,
        13.951822030443,
        12.280332349534,
        13.747149824617,
        2917100.0],
       [u'A',
        u'2001-09-24',
        20.5,
        21.69,
        20.2,
        21.0,
        1988300.0,
        0.0,
        1.0,
        13.985934064747,
        14.797800481188,
        13.781261858921,
        14.32705440779,
        1988300.0],
       [u'A',
        u'2001-09-25',
        21.2,
        21.2,
        18.5,
        19.78,
        2465100.0,
        0.0,
        1.0,
        14.463502545007,
        14.463502545007,
        12.621452692576,
        13.494720770766,
        2465100.0],
       [u'A',
        u'2001-09-26',
        19.95,
        20.2,
        18.5,
        19.3,
        2269700.0,
        0.0,
        1.0,
        13.6107016874,
        13.781261858921,
        12.621452692576,
        13.167245241445,
        2269700.0],
       [u'A',
        u'2001-09-27',
        19.06,
        19.24,
        18.42,
        19.24,
        1807600.0,
        0.0,
        1.0,
        13.003507476784,
        13.12631080028,
        12.56687343769,
        13.12631080028,
        1807600.0],
       [u'A',
        u'2001-09-28',
        19.4,
        19.92,
        19.0,
        19.55,
        2181100.0,
        0.0,
        1.0,
        13.235469310053,
        13.590234466817,
        12.962573035619,
        13.337805412966,
        2181100.0],
       [u'A',
        u'2001-10-01',
        19.15,
        19.47,
        18.72,
        18.86,
        1402500.0,
        0.0,
        1.0,
        13.064909138532,
        13.283226158079,
        12.771545643515,
        12.867059339567,
        1402500.0],
       [u'A',
        u'2001-10-02',
        20.1,
        20.1,
        19.0,
        20.07,
        2425000.0,
        0.0,
        1.0,
        13.713037790313,
        13.713037790313,
        12.962573035619,
        13.69257056973,
        2425000.0],
       [u'A',
        u'2001-10-03',
        21.48,
        21.48,
        19.55,
        21.25,
        2930900.0,
        0.0,
        1.0,
        14.65452993711,
        14.65452993711,
        13.337805412966,
        14.497614579311,
        2930900.0],
       [u'A',
        u'2001-10-04',
        22.25,
        22.25,
        21.06,
        21.7,
        2614800.0,
        0.0,
        1.0,
        15.179855265396,
        15.179855265396,
        14.367988848955,
        14.804622888049,
        2614800.0],
       [u'A',
        u'2001-10-05',
        21.55,
        21.55,
        20.4,
        21.1,
        1946700.0,
        0.0,
        1.0,
        14.702286785136,
        14.702286785136,
        13.917709996138,
        14.395278476398,
        1946700.0],
       [u'A',
        u'2001-10-08',
        22.0,
        22.0,
        20.6,
        21.42,
        1480500.0,
        0.0,
        1.0,
        15.009295093875,
        15.009295093875,
        14.054158133355,
        14.613595495945,
        1480500.0],
       [u'A',
        u'2001-10-09',
        21.47,
        21.47,
        20.45,
        20.78,
        1303000.0,
        0.0,
        1.0,
        14.64770753025,
        14.64770753025,
        13.951822030443,
        14.176961456851,
        1303000.0],
       [u'A',
        u'2001-10-10',
        20.55,
        21.98,
        20.5,
        21.94,
        1461100.0,
        0.0,
        1.0,
        14.020046099051,
        14.995650280153,
        13.985934064747,
        14.96836065271,
        1461100.0],
       [u'A',
        u'2001-10-11',
        22.13,
        24.36,
        22.13,
        24.12,
        2878900.0,
        0.0,
        1.0,
        15.097986383066,
        16.619383113036,
        15.097986383066,
        16.455645348375,
        2878900.0],
       [u'A',
        u'2001-10-12',
        23.32,
        23.75,
        22.9,
        23.36,
        2642100.0,
        0.0,
        1.0,
        15.909852799507,
        16.203216294524,
        15.623311711351,
        15.937142426951,
        2642100.0],
       [u'A',
        u'2001-10-15',
        23.42,
        23.6,
        22.38,
        23.23,
        1816300.0,
        0.0,
        1.0,
        15.978076868116,
        16.100880191611,
        15.268546554587,
        15.84845113776,
        1816300.0],
       [u'A',
        u'2001-10-16',
        23.0,
        23.99,
        23.0,
        23.81,
        1188700.0,
        0.0,
        1.0,
        15.69153577996,
        16.366954059184,
        15.69153577996,
        16.244150735689,
        1188700.0],
       [u'A',
        u'2001-10-17',
        24.5,
        24.79,
        23.1,
        23.62,
        1997000.0,
        0.0,
        1.0,
        16.714896809088,
        16.912746608052,
        15.759759848568,
        16.114525005333,
        1997000.0],
       [u'A',
        u'2001-10-18',
        22.85,
        23.3,
        22.53,
        22.7,
        995000.0,
        0.0,
        1.0,
        15.589199677047,
        15.896207985786,
        15.3708826575,
        15.486863574134,
        995000.0],
       [u'A',
        u'2001-10-19',
        22.61,
        23.5,
        22.46,
        23.36,
        1134400.0,
        0.0,
        1.0,
        15.425461912387,
        16.032656123003,
        15.323125809474,
        15.937142426951,
        1134400.0],
       [u'A',
        u'2001-10-22',
        22.7,
        23.74,
        22.6,
        23.61,
        1031200.0,
        0.0,
        1.0,
        15.486863574134,
        16.196393887663,
        15.418639505526,
        16.107702598472,
        1031200.0],
       [u'A',
        u'2001-10-23',
        23.61,
        24.65,
        23.6,
        23.85,
        1360700.0,
        0.0,
        1.0,
        16.107702598472,
        16.817232912001,
        16.100880191611,
        16.271440363132,
        1360700.0],
       [u'A',
        u'2001-10-24',
        24.25,
        24.25,
        23.25,
        24.22,
        1171400.0,
        0.0,
        1.0,
        16.544336637566,
        16.544336637566,
        15.862095951481,
        16.523869416984,
        1171400.0],
       [u'A',
        u'2001-10-25',
        23.5,
        24.13,
        22.3,
        24.13,
        1724300.0,
        0.0,
        1.0,
        16.032656123003,
        16.462467755236,
        15.2139672997,
        16.462467755236,
        1724300.0],
       [u'A',
        u'2001-10-26',
        23.9,
        24.58,
        23.86,
        24.34,
        1376800.0,
        0.0,
        1.0,
        16.305552397437,
        16.769476063975,
        16.278262769993,
        16.605738299314,
        1376800.0],
       [u'A',
        u'2001-10-29',
        23.86,
        23.87,
        22.56,
        22.93,
        1235400.0,
        0.0,
        1.0,
        16.278262769993,
        16.285085176854,
        15.391349878082,
        15.643778931934,
        1235400.0],
       [u'A',
        u'2001-10-30',
        23.0,
        23.0,
        22.05,
        22.2,
        1375800.0,
        0.0,
        1.0,
        15.69153577996,
        15.69153577996,
        15.043407128179,
        15.145743231092,
        1375800.0],
       [u'A',
        u'2001-10-31',
        22.4,
        23.2,
        22.15,
        22.27,
        1233400.0,
        0.0,
        1.0,
        15.282191368309,
        15.827983917177,
        15.111631196788,
        15.193500079118,
        1233400.0],
       [u'A',
        u'2001-11-01',
        22.12,
        23.0,
        22.06,
        22.9,
        1103800.0,
        0.0,
        1.0,
        15.091163976205,
        15.69153577996,
        15.05022953504,
        15.623311711351,
        1103800.0],
       [u'A',
        u'2001-11-02',
        23.15,
        23.45,
        22.81,
        23.3,
        945400.0,
        0.0,
        1.0,
        15.793871882873,
        15.998544088698,
        15.561910049604,
        15.896207985786,
        945400.0],
       [u'A',
        u'2001-11-05',
        23.45,
        24.8,
        23.45,
        24.48,
        1958700.0,
        0.0,
        1.0,
        15.998544088698,
        16.919569014913,
        15.998544088698,
        16.701251995366,
        1958700.0],
       [u'A',
        u'2001-11-06',
        24.73,
        25.49,
        24.15,
        25.49,
        1648100.0,
        0.0,
        1.0,
        16.871812166887,
        17.390315088312,
        16.476112568958,
        17.390315088312,
        1648100.0],
       [u'A',
        u'2001-11-07',
        25.27,
        25.27,
        24.54,
        24.7,
        1121600.0,
        0.0,
        1.0,
        17.240222137373,
        17.240222137373,
        16.742186436531,
        16.851344946305,
        1121600.0],
       [u'A',
        u'2001-11-08',
        24.6,
        25.74,
        24.55,
        24.75,
        1924200.0,
        0.0,
        1.0,
        16.783120877696,
        17.560875259833,
        16.749008843392,
        16.885456980609,
        1924200.0],
       [u'A',
        u'2001-11-09',
        24.4,
        24.94,
        24.3,
        24.8,
        937200.0,
        0.0,
        1.0,
        16.646672740479,
        17.015082710965,
        16.578448671871,
        16.919569014913,
        937200.0],
       [u'A',
        u'2001-11-12',
        24.36,
        24.8,
        23.61,
        24.64,
        1505600.0,
        0.0,
        1.0,
        16.619383113036,
        16.919569014913,
        16.107702598472,
        16.81041050514,
        1505600.0],
       [u'A',
        u'2001-11-13',
        24.2,
        25.0,
        24.18,
        24.95,
        2126800.0,
        0.0,
        1.0,
        16.510224603262,
        17.05601715213,
        16.49657978954,
        17.021905117826,
        2126800.0],
       [u'A',
        u'2001-11-14',
        25.11,
        25.7,
        25.01,
        25.31,
        1751100.0,
        0.0,
        1.0,
        17.1310636276,
        17.53358563239,
        17.062839558991,
        17.267511764817,
        1751100.0],
       [u'A',
        u'2001-11-15',
        25.0,
        25.39,
        24.21,
        25.03,
        1911500.0,
        0.0,
        1.0,
        17.05601715213,
        17.322091019704,
        16.517047010123,
        17.076484372713,
        1911500.0],
       [u'A',
        u'2001-11-16',
        23.9,
        24.25,
        22.6,
        24.13,
        8262200.0,
        0.0,
        1.0,
        16.305552397437,
        16.544336637566,
        15.418639505526,
        16.462467755236,
        8262200.0],
       [u'A',
        u'2001-11-19',
        24.0,
        24.75,
        23.55,
        24.41,
        9296800.0,
        0.0,
        1.0,
        16.373776466045,
        16.885456980609,
        16.066768157307,
        16.65349514734,
        9296800.0],
       [u'A',
        u'2001-11-20',
        24.25,
        24.26,
        23.6,
        23.78,
        9714000.0,
        0.0,
        1.0,
        16.544336637566,
        16.551159044427,
        16.100880191611,
        16.223683515106,
        9714000.0],
       [u'A',
        u'2001-11-21',
        23.87,
        24.4,
        23.68,
        24.33,
        6107800.0,
        0.0,
        1.0,
        16.285085176854,
        16.646672740479,
        16.155459446498,
        16.598915892453,
        6107800.0],
       [u'A',
        u'2001-11-23',
        25.1,
        25.1,
        24.27,
        25.1,
        1799400.0,
        0.0,
        1.0,
        17.124241220739,
        17.124241220739,
        16.557981451288,
        17.124241220739,
        1799400.0],
       [u'A',
        u'2001-11-26',
        25.14,
        26.3,
        25.04,
        26.25,
        4920600.0,
        0.0,
        1.0,
        17.151530848182,
        17.942930044041,
        17.083306779574,
        17.908818009737,
        4920600.0],
       [u'A',
        u'2001-11-27',
        27.59,
        27.59,
        26.1,
        27.0,
        5948600.0,
        0.0,
        1.0,
        18.823020529091,
        18.823020529091,
        17.806481906824,
        18.420498524301,
        5948600.0],
       [u'A',
        u'2001-11-28',
        27.25,
        27.25,
        26.25,
        26.95,
        4284900.0,
        0.0,
        1.0,
        18.591058695822,
        18.591058695822,
        17.908818009737,
        18.386386489997,
        4284900.0],
       [u'A',
        u'2001-11-29',
        26.75,
        27.35,
        26.06,
        27.17,
        3271700.0,
        0.0,
        1.0,
        18.249938352779,
        18.659282764431,
        17.779192279381,
        18.536479440935,
        3271700.0],
       [u'A',
        u'2001-11-30',
        27.5,
        27.5,
        26.98,
        27.27,
        3364000.0,
        0.0,
        1.0,
        18.761618867343,
        18.761618867343,
        18.406853710579,
        18.604703509544,
        3364000.0],
       [u'A',
        u'2001-12-03',
        27.7,
        27.7,
        26.9,
        27.51,
        2396100.0,
        0.0,
        1.0,
        18.89806700456,
        18.89806700456,
        18.352274455692,
        18.768441274204,
        2396100.0],
       [u'A',
        u'2001-12-04',
        27.7,
        28.15,
        27.23,
        28.15,
        2442300.0,
        0.0,
        1.0,
        18.89806700456,
        19.205075313299,
        18.5774138821,
        19.205075313299,
        2442300.0],
       [u'A',
        u'2001-12-05',
        28.25,
        29.93,
        28.08,
        29.93,
        4858500.0,
        0.0,
        1.0,
        19.273299381907,
        20.41946373453,
        19.157318465273,
        20.41946373453,
        4858500.0],
       [u'A',
        u'2001-12-06',
        29.99,
        29.99,
        29.3,
        29.76,
        2227600.0,
        0.0,
        1.0,
        20.460398175696,
        20.460398175696,
        19.989652102297,
        20.303482817896,
        2227600.0],
       [u'A',
        u'2001-12-07',
        30.87,
        30.87,
        29.41,
        30.15,
        4156100.0,
        0.0,
        1.0,
        21.060769979451,
        21.060769979451,
        20.064698577766,
        20.569556685469,
        4156100.0],
       [u'A',
        u'2001-12-10',
        29.95,
        30.75,
        29.2,
        29.95,
        2616000.0,
        0.0,
        1.0,
        20.433108548252,
        20.97890109712,
        19.921428033688,
        20.433108548252,
        2616000.0],
       [u'A',
        u'2001-12-11',
        29.95,
        30.21,
        29.26,
        29.29,
        2243700.0,
        0.0,
        1.0,
        20.433108548252,
        20.610491126634,
        19.962362474853,
        19.982829695436,
        2243700.0],
       [u'A',
        u'2001-12-12',
        29.45,
        30.85,
        29.42,
        30.71,
        3600900.0,
        0.0,
        1.0,
        20.09198820521,
        21.047125165729,
        20.071520984627,
        20.951611469677,
        3600900.0],
       [u'A',
        u'2001-12-13',
        29.7,
        29.77,
        28.51,
        28.52,
        2453600.0,
        0.0,
        1.0,
        20.262548376731,
        20.310305224757,
        19.450681960289,
        19.45750436715,
        2453600.0],
       [u'A',
        u'2001-12-14',
        28.05,
        28.99,
        28.01,
        28.83,
        2178300.0,
        0.0,
        1.0,
        19.13685124469,
        19.77815748961,
        19.109561617247,
        19.668998979837,
        2178300.0],
       [u'A',
        u'2001-12-17',
        28.48,
        29.47,
        28.3,
        28.91,
        3476000.0,
        0.0,
        1.0,
        19.430214739707,
        20.105633018931,
        19.307411416212,
        19.723578234724,
        3476000.0],
       [u'A',
        u'2001-12-18',
        28.97,
        29.42,
        28.4,
        28.82,
        2155000.0,
        0.0,
        1.0,
        19.764512675889,
        20.071520984627,
        19.37563548482,
        19.662176572976,
        2155000.0],
       [u'A',
        u'2001-12-19',
        28.05,
        29.09,
        28.0,
        28.55,
        1801100.0,
        0.0,
        1.0,
        19.13685124469,
        19.846381558219,
        19.102739210386,
        19.477971587733,
        1801100.0],
       [u'A',
        u'2001-12-20',
        28.15,
        28.26,
        27.42,
        27.7,
        2848500.0,
        0.0,
        1.0,
        19.205075313299,
        19.280121788768,
        18.707039612457,
        18.89806700456,
        2848500.0],
       [u'A',
        u'2001-12-21',
        27.58,
        28.3,
        27.58,
        27.95,
        2669900.0,
        0.0,
        1.0,
        18.81619812223,
        19.307411416212,
        18.81619812223,
        19.068627176082,
        2669900.0],
       [u'A',
        u'2001-12-24',
        28.48,
        28.6,
        28.1,
        28.51,
        891400.0,
        0.0,
        1.0,
        19.430214739707,
        19.512083622037,
        19.170963278995,
        19.450681960289,
        891400.0],
       [u'A',
        u'2001-12-26',
        28.7,
        28.88,
        28.1,
        28.1,
        1764700.0,
        0.0,
        1.0,
        19.580307690646,
        19.703111014141,
        19.170963278995,
        19.170963278995,
        1764700.0],
       [u'A',
        u'2001-12-27',
        28.01,
        28.97,
        28.01,
        28.84,
        1366200.0,
        0.0,
        1.0,
        19.109561617247,
        19.764512675889,
        19.109561617247,
        19.675821386698,
        1366200.0],
       [u'A',
        u'2001-12-28',
        29.0,
        29.19,
        28.55,
        28.95,
        1144800.0,
        0.0,
        1.0,
        19.784979896471,
        19.914605626827,
        19.477971587733,
        19.750867862167,
        1144800.0],
       [u'A',
        u'2001-12-31',
        28.7,
        29.1,
        28.45,
        28.51,
        1532200.0,
        0.0,
        1.0,
        19.580307690646,
        19.85320396508,
        19.409747519124,
        19.450681960289,
        1532200.0],
       [u'A',
        u'2002-01-02',
        28.51,
        29.34,
        28.46,
        29.25,
        2159300.0,
        0.0,
        1.0,
        19.450681960289,
        20.01694172974,
        19.416569925985,
        19.955540067993,
        2159300.0],
       [u'A',
        u'2002-01-03',
        31.2,
        31.2,
        29.42,
        31.1,
        3260600.0,
        0.0,
        1.0,
        21.285909405859,
        21.285909405859,
        20.071520984627,
        21.21768533725,
        3260600.0],
       [u'A',
        u'2002-01-04',
        32.94,
        32.94,
        31.65,
        32.78,
        5118200.0,
        0.0,
        1.0,
        22.473008199647,
        22.473008199647,
        21.592917714597,
        22.363849689873,
        5118200.0],
       [u'A',
        u'2002-01-07',
        32.89,
        32.89,
        32.2,
        32.65,
        3809200.0,
        0.0,
        1.0,
        22.438896165343,
        22.438896165343,
        21.968150091944,
        22.275158400682,
        3809200.0],
       [u'A',
        u'2002-01-08',
        32.65,
        32.89,
        32.25,
        32.75,
        2495400.0,
        0.0,
        1.0,
        22.275158400682,
        22.438896165343,
        22.002262126248,
        22.343382469291,
        2495400.0],
       [u'A',
        u'2002-01-09',
        32.72,
        33.3,
        31.69,
        31.97,
        2116800.0,
        0.0,
        1.0,
        22.322915248708,
        22.718614846638,
        21.62020734204,
        21.811234734144,
        2116800.0],
       [u'A',
        u'2002-01-10',
        31.97,
        31.97,
        31.3,
        31.72,
        1238100.0,
        0.0,
        1.0,
        21.811234734144,
        21.811234734144,
        21.354133474467,
        21.640674562623,
        1238100.0],
       [u'A',
        u'2002-01-11',
        31.72,
        31.9,
        30.71,
        31.04,
        1416200.0,
        0.0,
        1.0,
        21.640674562623,
        21.763477886118,
        20.951611469677,
        21.176750896085,
        1416200.0],
       [u'A',
        u'2002-01-14',
        30.5,
        30.62,
        30.07,
        30.42,
        2229800.0,
        0.0,
        1.0,
        20.808340925599,
        20.890209807929,
        20.514977430582,
        20.753761670712,
        2229800.0],
       [u'A',
        u'2002-01-15',
        30.42,
        31.15,
        30.18,
        30.45,
        1860000.0,
        0.0,
        1.0,
        20.753761670712,
        21.251797371554,
        20.590023906052,
        20.774228891295,
        1860000.0],
       [u'A',
        u'2002-01-16',
        29.8,
        29.8,
        28.65,
        28.86,
        2558900.0,
        0.0,
        1.0,
        20.330772445339,
        20.330772445339,
        19.546195656341,
        19.689466200419,
        2558900.0],
       [u'A',
        u'2002-01-17',
        28.9,
        29.49,
        28.62,
        29.37,
        1426000.0,
        0.0,
        1.0,
        19.716755827863,
        20.119277832653,
        19.525728435759,
        20.037408950323,
        1426000.0],
       [u'A',
        u'2002-01-18',
        28.82,
        28.97,
        28.24,
        28.48,
        1949400.0,
        0.0,
        1.0,
        19.662176572976,
        19.764512675889,
        19.266476975046,
        19.430214739707,
        1949400.0],
       [u'A',
        u'2002-01-22',
        28.4,
        28.5,
        27.05,
        27.16,
        1553900.0,
        0.0,
        1.0,
        19.37563548482,
        19.443859553429,
        18.454610558605,
        18.529657034074,
        1553900.0],
       [u'A',
        u'2002-01-23',
        26.92,
        28.74,
        26.92,
        28.0,
        2202300.0,
        0.0,
        1.0,
        18.365919269414,
        19.607597318089,
        18.365919269414,
        19.102739210386,
        2202300.0],
       [u'A',
        u'2002-01-24',
        29.25,
        29.25,
        28.3,
        28.79,
        1039900.0,
        0.0,
        1.0,
        19.955540067993,
        19.955540067993,
        19.307411416212,
        19.641709352393,
        1039900.0],
       [u'A',
        u'2002-01-25',
        28.8,
        29.3,
        28.35,
        29.06,
        1695300.0,
        0.0,
        1.0,
        19.648531759254,
        19.989652102297,
        19.341523450516,
        19.825914337636,
        1695300.0],
       [u'A',
        u'2002-01-28',
        29.8,
        29.8,
        28.86,
        29.63,
        2064200.0,
        0.0,
        1.0,
        20.330772445339,
        20.330772445339,
        19.689466200419,
        20.214791528705,
        2064200.0],
       [u'A',
        u'2002-01-29',
        29.4,
        30.1,
        29.0,
        29.25,
        1572300.0,
        0.0,
        1.0,
        20.057876170905,
        20.535444651165,
        19.784979896471,
        19.955540067993,
        1572300.0],
       [u'A',
        u'2002-01-30',
        28.77,
        29.5,
        28.15,
        29.44,
        1887300.0,
        0.0,
        1.0,
        19.628064538672,
        20.126100239514,
        19.205075313299,
        20.085165798349,
        1887300.0],
       [u'A',
        u'2002-01-31',
        29.3,
        30.38,
        29.16,
        30.35,
        1971900.0,
        0.0,
        1.0,
        19.989652102297,
        20.726472043269,
        19.894138406245,
        20.706004822686,
        1971900.0],
       [u'A',
        u'2002-02-01',
        30.22,
        30.22,
        29.17,
        29.61,
        1098700.0,
        0.0,
        1.0,
        20.617313533495,
        20.617313533495,
        19.900960813106,
        20.201146714983,
        1098700.0],
       [u'A',
        u'2002-02-04',
        29.1,
        29.7,
        28.32,
        28.58,
        1110200.0,
        0.0,
        1.0,
        19.85320396508,
        20.262548376731,
        19.321056229933,
        19.498438808315,
        1110200.0],
       [u'A',
        u'2002-02-05',
        28.34,
        28.9,
        26.99,
        27.16,
        2815600.0,
        0.0,
        1.0,
        19.334701043655,
        19.716755827863,
        18.41367611744,
        18.529657034074,
        2815600.0],
       [u'A',
        u'2002-02-06',
        27.4,
        27.55,
        26.43,
        26.98,
        2653500.0,
        0.0,
        1.0,
        18.693394798735,
        18.795730901648,
        18.031621333232,
        18.406853710579,
        2653500.0],
       [u'A',
        u'2002-02-07',
        27.22,
        27.24,
        26.27,
        26.39,
        1868700.0,
        0.0,
        1.0,
        18.57059147524,
        18.584236288961,
        17.922462823459,
        18.004331705789,
        1868700.0],
       [u'A',
        u'2002-02-08',
        26.4,
        26.66,
        24.83,
        25.98,
        3096600.0,
        0.0,
        1.0,
        18.01115411265,
        18.188536691032,
        16.940036235496,
        17.724613024494,
        3096600.0],
       [u'A',
        u'2002-02-11',
        25.5,
        26.9,
        25.5,
        26.74,
        2051600.0,
        0.0,
        1.0,
        17.397137495173,
        18.352274455692,
        17.397137495173,
        18.243115945919,
        2051600.0],
       [u'A',
        u'2002-02-12',
        26.49,
        26.93,
        25.95,
        26.16,
        2353500.0,
        0.0,
        1.0,
        18.072555774397,
        18.372741676275,
        17.704145803911,
        17.847416347989,
        2353500.0],
       [u'A',
        u'2002-02-13',
        26.41,
        27.05,
        26.41,
        26.86,
        2105600.0,
        0.0,
        1.0,
        18.017976519511,
        18.454610558605,
        18.017976519511,
        18.324984828249,
        2105600.0],
       [u'A',
        u'2002-02-14',
        26.9,
        27.3,
        26.46,
        27.3,
        2220100.0,
        0.0,
        1.0,
        18.352274455692,
        18.625170730126,
        18.052088553815,
        18.625170730126,
        2220100.0],
       [u'A',
        u'2002-02-15',
        27.67,
        27.67,
        27.2,
        27.5,
        2012300.0,
        0.0,
        1.0,
        18.877599783978,
        18.877599783978,
        18.556946661518,
        18.761618867343,
        2012300.0],
       [u'A',
        u'2002-02-19',
        26.8,
        26.88,
        26.0,
        26.05,
        1679300.0,
        0.0,
        1.0,
        18.284050387084,
        18.338629641971,
        17.738257838216,
        17.77236987252,
        1679300.0],
       [u'A',
        u'2002-02-20',
        29.8,
        29.8,
        28.0,
        28.86,
        5025000.0,
        0.0,
        1.0,
        20.330772445339,
        20.330772445339,
        19.102739210386,
        19.689466200419,
        5025000.0],
       [u'A',
        u'2002-02-21',
        29.05,
        29.6,
        28.1,
        28.16,
        2415900.0,
        0.0,
        1.0,
        19.819091930775,
        20.194324308122,
        19.170963278995,
        19.21189772016,
        2415900.0],
       [u'A',
        u'2002-02-22',
        28.2,
        28.65,
        27.81,
        28.26,
        1469600.0,
        0.0,
        1.0,
        19.239187347603,
        19.546195656341,
        18.97311348003,
        19.280121788768,
        1469600.0],
       [u'A',
        u'2002-02-25',
        28.5,
        29.6,
        28.45,
        29.0,
        1340300.0,
        0.0,
        1.0,
        19.443859553429,
        20.194324308122,
        19.409747519124,
        19.784979896471,
        1340300.0],
       [u'A',
        u'2002-02-26',
        29.0,
        29.89,
        28.89,
        29.71,
        1971500.0,
        0.0,
        1.0,
        19.784979896471,
        20.392174107087,
        19.709933421002,
        20.269370783592,
        1971500.0],
       [u'A',
        u'2002-02-27',
        29.98,
        31.94,
        29.85,
        30.64,
        4580800.0,
        0.0,
        1.0,
        20.453575768835,
        21.790767513562,
        20.364884479644,
        20.903854621651,
        4580800.0],
       [u'A',
        u'2002-02-28',
        32.0,
        32.09,
        31.05,
        31.15,
        2751400.0,
        0.0,
        1.0,
        21.831701954727,
        21.893103616475,
        21.183573302946,
        21.251797371554,
        2751400.0],
       [u'A',
        u'2002-03-01',
        31.45,
        33.3,
        31.4,
        32.99,
        4482700.0,
        0.0,
        1.0,
        21.45646957738,
        22.718614846638,
        21.422357543076,
        22.507120233951,
        4482700.0],
       [u'A',
        u'2002-03-04',
        33.05,
        35.15,
        32.8,
        34.96,
        4162400.0,
        0.0,
        1.0,
        22.548054675116,
        23.980760115895,
        22.377494503595,
        23.851134385539,
        4162400.0],
       [u'A',
        u'2002-03-05',
        34.75,
        35.9,
        34.3,
        34.9,
        3441800.0,
        0.0,
        1.0,
        23.707863841461,
        24.492440630459,
        23.400855532723,
        23.810199944374,
        3441800.0],
       [u'A',
        u'2002-03-06',
        34.8,
        35.25,
        34.2,
        34.42,
        2929200.0,
        0.0,
        1.0,
        23.741975875765,
        24.048984184504,
        23.332631464114,
        23.482724415053,
        2929200.0],
       [u'A',
        u'2002-03-07',
        35.0,
        35.2,
        34.51,
        34.8,
        1820500.0,
        0.0,
        1.0,
        23.878424012983,
        24.0148721502,
        23.544126076801,
        23.741975875765,
        1820500.0],
       [u'A',
        u'2002-03-08',
        35.05,
        36.36,
        35.02,
        36.09,
        3645800.0,
        0.0,
        1.0,
        23.912536047287,
        24.806271346058,
        23.892068826704,
        24.622066360815,
        3645800.0],
       [u'A',
        u'2002-03-11',
        36.09,
        36.99,
        36.08,
        36.21,
        3198000.0,
        0.0,
        1.0,
        24.622066360815,
        25.236082978292,
        24.615243953955,
        24.703935243146,
        3198000.0],
       [u'A',
        u'2002-03-12',
        36.16,
        36.16,
        35.15,
        36.01,
        2968300.0,
        0.0,
        1.0,
        24.669823208841,
        24.669823208841,
        23.980760115895,
        24.567487105929,
        2968300.0],
       [u'A',
        u'2002-03-13',
        35.8,
        35.85,
        35.36,
        35.69,
        4996800.0,
        0.0,
        1.0,
        24.424216561851,
        24.458328596155,
        24.124030659973,
        24.349170086381,
        4996800.0],
       [u'A',
        u'2002-03-14',
        35.95,
        35.95,
        35.4,
        35.66,
        2542100.0,
        0.0,
        1.0,
        24.526552664763,
        24.526552664763,
        24.151320287417,
        24.328702865799,
        2542100.0],
       [u'A',
        u'2002-03-15',
        35.91,
        37.5,
        35.75,
        37.31,
        3266600.0,
        0.0,
        1.0,
        24.49926303732,
        25.584025728196,
        24.390104527546,
        25.454399997839,
        3266600.0],
       [u'A',
        u'2002-03-18',
        37.31,
        38.0,
        36.75,
        37.06,
        3886100.0,
        0.0,
        1.0,
        25.454399997839,
        25.925146071238,
        25.072345213632,
        25.283839826318,
        3886100.0],
       [u'A',
        u'2002-03-19',
        37.06,
        37.39,
        36.22,
        36.6,
        2195900.0,
        0.0,
        1.0,
        25.283839826318,
        25.508979252726,
        24.710757650006,
        24.970009110719,
        2195900.0],
       [u'A',
        u'2002-03-20',
        36.0,
        36.3,
        34.3,
        34.36,
        3912000.0,
        0.0,
        1.0,
        24.560664699068,
        24.765336904893,
        23.400855532723,
        23.441789973888,
        3912000.0],
       [u'A',
        u'2002-03-21',
        35.42,
        35.42,
        34.29,
        35.32,
        1655600.0,
        0.0,
        1.0,
        24.164965101138,
        24.164965101138,
        23.394033125862,
        24.09674103253,
        1655600.0],
       [u'A',
        u'2002-03-22',
        35.1,
        35.38,
        34.1,
        34.37,
        1658600.0,
        0.0,
        1.0,
        23.946648081591,
        24.137675473695,
        23.264407395506,
        23.448612380749,
        1658600.0],
       [u'A',
        u'2002-03-25',
        34.44,
        34.84,
        33.3,
        33.39,
        1764900.0,
        0.0,
        1.0,
        23.496369228775,
        23.769265503209,
        22.718614846638,
        22.780016508385,
        1764900.0],
       [u'A',
        u'2002-03-26',
        33.6,
        34.4,
        33.27,
        33.52,
        2671100.0,
        0.0,
        1.0,
        22.923287052463,
        23.469079601331,
        22.698147626055,
        22.868707797576,
        2671100.0],
       [u'A',
        u'2002-03-27',
        34.08,
        34.08,
        33.04,
        33.25,
        3846900.0,
        0.0,
        1.0,
        23.250762581784,
        23.250762581784,
        22.541232268255,
        22.684502812333,
        3846900.0],
       [u'A',
        u'2002-03-28',
        33.95,
        35.36,
        33.7,
        34.96,
        2681500.0,
        0.0,
        1.0,
        23.162071292593,
        24.124030659973,
        22.991511121072,
        23.851134385539,
        2681500.0],
       [u'A',
        u'2002-04-01',
        36.8,
        36.8,
        34.7,
        36.53,
        2581800.0,
        0.0,
        1.0,
        25.106457247936,
        25.106457247936,
        23.673751807157,
        24.922252262693,
        2581800.0],
       [u'A',
        u'2002-04-02',
        36.4,
        36.47,
        35.36,
        35.7,
        4902800.0,
        0.0,
        1.0,
        24.833560973502,
        24.881317821528,
        24.124030659973,
        24.355992493242,
        4902800.0],
       [u'A',
        u'2002-04-03',
        36.5,
        36.95,
        34.61,
        35.05,
        3012400.0,
        0.0,
        1.0,
        24.90178504211,
        25.208793350849,
        23.612350145409,
        23.912536047287,
        3012400.0],
       [u'A',
        u'2002-04-04',
        35.22,
        35.43,
        33.99,
        34.14,
        2139000.0,
        0.0,
        1.0,
        24.028516963921,
        24.171787507999,
        23.189360920036,
        23.291697022949,
        2139000.0],
       [u'A',
        u'2002-04-05',
        34.25,
        34.74,
        33.7,
        33.89,
        1048300.0,
        0.0,
        1.0,
        23.366743498419,
        23.7010414346,
        22.991511121072,
        23.121136851428,
        1048300.0],
       [u'A',
        u'2002-04-08',
        33.25,
        34.63,
        32.9,
        34.2,
        2008900.0,
        0.0,
        1.0,
        22.684502812333,
        23.625994959131,
        22.445718572204,
        23.332631464114,
        2008900.0],
       [u'A',
        u'2002-04-09',
        34.08,
        34.43,
        32.57,
        32.8,
        2099500.0,
        0.0,
        1.0,
        23.250762581784,
        23.489546821914,
        22.220579145795,
        22.377494503595,
        2099500.0],
       [u'A',
        u'2002-04-10',
        33.0,
        33.41,
        32.81,
        33.18,
        3719600.0,
        0.0,
        1.0,
        22.513942640812,
        22.793661322107,
        22.384316910456,
        22.636745964307,
        3719600.0],
       [u'A',
        u'2002-04-11',
        32.7,
        32.9,
        32.0,
        32.15,
        3395900.0,
        0.0,
        1.0,
        22.309270434987,
        22.445718572204,
        21.831701954727,
        21.93403805764,
        3395900.0],
       [u'A',
        u'2002-04-12',
        32.22,
        32.65,
        31.89,
        32.35,
        2278500.0,
        0.0,
        1.0,
        21.981794905666,
        22.275158400682,
        21.756655479257,
        22.070486194857,
        2278500.0],
       [u'A',
        u'2002-04-15',
        32.35,
        32.8,
        31.95,
        32.44,
        1722400.0,
        0.0,
        1.0,
        22.070486194857,
        22.377494503595,
        21.797589920423,
        22.131887856604,
        1722400.0],
       [u'A',
        u'2002-04-16',
        32.95,
        34.0,
        32.81,
        33.9,
        6692700.0,
        0.0,
        1.0,
        22.479830606508,
        23.196183326897,
        22.384316910456,
        23.127959258289,
        6692700.0],
       [u'A',
        u'2002-04-17',
        34.25,
        35.02,
        33.95,
        34.97,
        3086900.0,
        0.0,
        1.0,
        23.366743498419,
        23.892068826704,
        23.162071292593,
        23.8579567924,
        3086900.0],
       [u'A',
        u'2002-04-18',
        34.65,
        34.75,
        33.52,
        34.6,
        2738500.0,
        0.0,
        1.0,
        23.639639772853,
        23.707863841461,
        22.868707797576,
        23.605527738548,
        2738500.0],
       [u'A',
        u'2002-04-19',
        35.0,
        35.27,
        34.82,
        35.0,
        2657800.0,
        0.0,
        1.0,
        23.878424012983,
        24.062628998226,
        23.755620689487,
        23.878424012983,
        2657800.0],
       [u'A',
        u'2002-04-22',
        34.56,
        34.65,
        33.19,
        33.75,
        2077500.0,
        0.0,
        1.0,
        23.578238111105,
        23.639639772853,
        22.643568371168,
        23.025623155376,
        2077500.0],
       [u'A',
        u'2002-04-23',
        33.75,
        34.3,
        32.29,
        32.31,
        5850000.0,
        0.0,
        1.0,
        23.025623155376,
        23.400855532723,
        22.029551753692,
        22.043196567413,
        5850000.0],
       [u'A',
        u'2002-04-24',
        32.55,
        32.79,
        31.11,
        31.13,
        2890900.0,
        0.0,
        1.0,
        22.206934332074,
        22.370672096734,
        21.224507744111,
        21.238152557833,
        2890900.0],
       [u'A',
        u'2002-04-25',
        30.9,
        31.22,
        29.95,
        30.95,
        2459900.0,
        0.0,
        1.0,
        21.081237200033,
        21.29955421958,
        20.433108548252,
        21.115349234337,
        2459900.0],
       [u'A',
        u'2002-04-26',
        31.0,
        31.2,
        29.8,
        29.96,
        1756000.0,
        0.0,
        1.0,
        21.149461268642,
        21.285909405859,
        20.330772445339,
        20.439930955113,
        1756000.0],
       [u'A',
        u'2002-04-29',
        29.75,
        30.48,
        29.39,
        29.65,
        2876500.0,
        0.0,
        1.0,
        20.296660411035,
        20.794696111877,
        20.051053764044,
        20.228436342427,
        2876500.0],
       [u'A',
        u'2002-04-30',
        29.85,
        30.55,
        29.49,
        30.05,
        1942700.0,
        0.0,
        1.0,
        20.364884479644,
        20.842452959903,
        20.119277832653,
        20.501332616861,
        1942700.0],
       [u'A',
        u'2002-05-01',
        30.0,
        30.85,
        29.0,
        30.44,
        2466200.0,
        0.0,
        1.0,
        20.467220582556,
        21.047125165729,
        19.784979896471,
        20.767406484434,
        2466200.0],
       [u'A',
        u'2002-05-02',
        30.2,
        30.21,
        29.0,
        29.1,
        2833100.0,
        0.0,
        1.0,
        20.603668719773,
        20.610491126634,
        19.784979896471,
        19.85320396508,
        2833100.0],
       [u'A',
        u'2002-05-03',
        29.0,
        29.08,
        28.35,
        28.51,
        2505300.0,
        0.0,
        1.0,
        19.784979896471,
        19.839559151358,
        19.341523450516,
        19.450681960289,
        2505300.0],
       [u'A',
        u'2002-05-06',
        28.28,
        29.18,
        27.84,
        27.85,
        1779000.0,
        0.0,
        1.0,
        19.29376660249,
        19.907783219967,
        18.993580700612,
        19.000403107473,
        1779000.0],
       [u'A',
        u'2002-05-07',
        28.4,
        28.5,
        27.76,
        27.81,
        2540200.0,
        0.0,
        1.0,
        19.37563548482,
        19.443859553429,
        18.939001445726,
        18.97311348003,
        2540200.0],
       [u'A',
        u'2002-05-08',
        28.8,
        30.6,
        28.75,
        30.04,
        2382700.0,
        0.0,
        1.0,
        19.648531759254,
        20.876564994208,
        19.61441972495,
        20.49451021,
        2382700.0],
       [u'A',
        u'2002-05-09',
        29.75,
        30.08,
        28.66,
        28.74,
        3575500.0,
        0.0,
        1.0,
        20.296660411035,
        20.521799837443,
        19.553018063202,
        19.607597318089,
        3575500.0],
       [u'A',
        u'2002-05-10',
        28.75,
        28.94,
        27.42,
        27.95,
        2687700.0,
        0.0,
        1.0,
        19.61441972495,
        19.744045455306,
        18.707039612457,
        19.068627176082,
        2687700.0],
       [u'A',
        u'2002-05-13',
        27.95,
        28.96,
        27.7,
        28.46,
        1627100.0,
        0.0,
        1.0,
        19.068627176082,
        19.757690269028,
        18.89806700456,
        19.416569925985,
        1627100.0],
       [u'A',
        u'2002-05-14',
        30.3,
        31.25,
        29.8,
        31.05,
        3078700.0,
        0.0,
        1.0,
        20.671892788382,
        21.320021440163,
        20.330772445339,
        21.183573302946,
        3078700.0],
       [u'A',
        u'2002-05-15',
        30.0,
        30.65,
        29.72,
        29.75,
        2436000.0,
        0.0,
        1.0,
        20.467220582556,
        20.910677028512,
        20.276193190453,
        20.296660411035,
        2436000.0],
       [u'A',
        u'2002-05-16',
        29.75,
        29.8,
        29.25,
        29.6,
        2409500.0,
        0.0,
        1.0,
        20.296660411035,
        20.330772445339,
        19.955540067993,
        20.194324308122,
        2409500.0],
       [u'A',
        u'2002-05-17',
        29.7,
        30.04,
        28.5,
        30.01,
        3686500.0,
        0.0,
        1.0,
        20.262548376731,
        20.49451021,
        19.443859553429,
        20.474042989417,
        3686500.0],
       [u'A',
        u'2002-05-20',
        29.6,
        29.74,
        29.21,
        29.4,
        1851900.0,
        0.0,
        1.0,
        20.194324308122,
        20.289838004174,
        19.928250440549,
        20.057876170905,
        1851900.0],
       [u'A',
        u'2002-05-21',
        29.51,
        29.99,
        28.27,
        28.54,
        1788200.0,
        0.0,
        1.0,
        20.132922646375,
        20.460398175696,
        19.286944195629,
        19.471149180872,
        1788200.0],
       [u'A',
        u'2002-05-22',
        28.54,
        28.95,
        27.71,
        28.11,
        2672600.0,
        0.0,
        1.0,
        19.471149180872,
        19.750867862167,
        18.904889411421,
        19.177785685855,
        2672600.0],
       [u'A',
        u'2002-05-23',
        28.11,
        28.3,
        27.37,
        27.83,
        2126400.0,
        0.0,
        1.0,
        19.177785685855,
        19.307411416212,
        18.672927578152,
        18.986758293752,
        2126400.0],
       [u'A',
        u'2002-05-24',
        27.83,
        27.95,
        27.15,
        27.3,
        1888500.0,
        0.0,
        1.0,
        18.986758293752,
        19.068627176082,
        18.522834627214,
        18.625170730126,
        1888500.0],
       [u'A',
        u'2002-05-28',
        27.35,
        27.89,
        26.91,
        27.14,
        1328400.0,
        0.0,
        1.0,
        18.659282764431,
        19.027692734917,
        18.359096862553,
        18.516012220353,
        1328400.0],
       [u'A',
        u'2002-05-29',
        26.93,
        27.1,
        26.7,
        26.7,
        1226200.0,
        0.0,
        1.0,
        18.372741676275,
        18.488722592909,
        18.215826318475,
        18.215826318475,
        1226200.0],
       [u'A',
        u'2002-05-30',
        26.6,
        26.7,
        25.45,
        26.13,
        2960100.0,
        0.0,
        1.0,
        18.147602249867,
        18.215826318475,
        17.363025460869,
        17.826949127407,
        2960100.0],
       [u'A',
        u'2002-05-31',
        26.13,
        26.82,
        26.0,
        26.37,
        2138300.0,
        0.0,
        1.0,
        17.826949127407,
        18.297695200805,
        17.738257838216,
        17.990686892067,
        2138300.0],
       [u'A',
        u'2002-06-03',
        26.49,
        26.55,
        25.26,
        25.53,
        1333200.0,
        0.0,
        1.0,
        18.072555774397,
        18.113490215562,
        17.233399730513,
        17.417604715756,
        1333200.0],
       [u'A',
        u'2002-06-04',
        25.53,
        25.74,
        24.96,
        25.49,
        2009000.0,
        0.0,
        1.0,
        17.417604715756,
        17.560875259833,
        17.028727524687,
        17.390315088312,
        2009000.0],
       [u'A',
        u'2002-06-05',
        25.35,
        25.54,
        24.5,
        25.1,
        2077100.0,
        0.0,
        1.0,
        17.29480139226,
        17.424427122616,
        16.714896809088,
        17.124241220739,
        2077100.0],
       [u'A',
        u'2002-06-06',
        24.55,
        25.88,
        24.25,
        24.63,
        1582000.0,
        0.0,
        1.0,
        16.749008843392,
        17.656388955885,
        16.544336637566,
        16.803588098279,
        1582000.0],
       [u'A',
        u'2002-06-07',
        23.76,
        24.14,
        23.52,
        23.7,
        2397800.0,
        0.0,
        1.0,
        16.210038701385,
        16.469290162097,
        16.046300936724,
        16.16910426022,
        2397800.0],
       [u'A',
        u'2002-06-10',
        23.7,
        25.23,
        23.32,
        24.73,
        2615300.0,
        0.0,
        1.0,
        16.16910426022,
        17.21293250993,
        15.909852799507,
        16.871812166887,
        2615300.0],
       [u'A',
        u'2002-06-11',
        24.76,
        26.0,
        24.76,
        25.26,
        4992100.0,
        0.0,
        1.0,
        16.89227938747,
        17.738257838216,
        16.89227938747,
        17.233399730513,
        4992100.0],
       [u'A',
        u'2002-06-12',
        25.26,
        25.7,
        24.2,
        24.67,
        2433300.0,
        0.0,
        1.0,
        17.233399730513,
        17.53358563239,
        16.510224603262,
        16.830877725722,
        2433300.0],
       [u'A',
        u'2002-06-13',
        24.8,
        24.88,
        23.91,
        24.0,
        2835700.0,
        0.0,
        1.0,
        16.919569014913,
        16.9741482698,
        16.312374804297,
        16.373776466045,
        2835700.0],
       [u'A',
        u'2002-06-14',
        23.25,
        23.92,
        23.0,
        23.5,
        2160000.0,
        0.0,
        1.0,
        15.862095951481,
        16.319197211158,
        15.69153577996,
        16.032656123003,
        2160000.0],
       [u'A',
        u'2002-06-17',
        23.95,
        25.57,
        23.85,
        25.21,
        3117300.0,
        0.0,
        1.0,
        16.339664431741,
        17.444894343199,
        16.271440363132,
        17.199287696208,
        3117300.0],
       [u'A',
        u'2002-06-18',
        25.3,
        25.97,
        24.78,
        25.27,
        2408600.0,
        0.0,
        1.0,
        17.260689357956,
        17.717790617633,
        16.905924201192,
        17.240222137373,
        2408600.0],
       [u'A',
        u'2002-06-19',
        24.72,
        24.98,
        23.85,
        24.3,
        2832800.0,
        0.0,
        1.0,
        16.864989760027,
        17.042372338409,
        16.271440363132,
        16.578448671871,
        2832800.0],
       [u'A',
        u'2002-06-20',
        24.2,
        24.75,
        23.79,
        24.0,
        2750500.0,
        0.0,
        1.0,
        16.510224603262,
        16.885456980609,
        16.230505921967,
        16.373776466045,
        2750500.0],
       [u'A',
        u'2002-06-21',
        24.0,
        24.19,
        23.53,
        23.96,
        2999100.0,
        0.0,
        1.0,
        16.373776466045,
        16.503402196401,
        16.053123343585,
        16.346486838602,
        2999100.0],
       [u'A',
        u'2002-06-24',
        24.0,
        24.74,
        23.53,
        24.16,
        3115500.0,
        0.0,
        1.0,
        16.373776466045,
        16.878634573748,
        16.053123343585,
        16.482934975819,
        3115500.0],
       [u'A',
        u'2002-06-25',
        24.7,
        24.89,
        23.52,
        23.55,
        1961800.0,
        0.0,
        1.0,
        16.851344946305,
        16.980970676661,
        16.046300936724,
        16.066768157307,
        1961800.0],
       [u'A',
        u'2002-06-26',
        23.01,
        23.4,
        22.4,
        23.2,
        2350500.0,
        0.0,
        1.0,
        15.698358186821,
        15.964432054394,
        15.282191368309,
        15.827983917177,
        2350500.0],
       [u'A',
        u'2002-06-27',
        23.24,
        24.5,
        23.2,
        24.23,
        1415900.0,
        0.0,
        1.0,
        15.85527354462,
        16.714896809088,
        15.827983917177,
        16.530691823845,
        1415900.0],
       [u'A',
        u'2002-06-28',
        23.98,
        24.45,
        23.55,
        23.65,
        2284900.0,
        0.0,
        1.0,
        16.360131652323,
        16.680784774784,
        16.066768157307,
        16.134992225915,
        2284900.0],
       [u'A',
        u'2002-07-01',
        23.45,
        23.91,
        22.82,
        23.13,
        1875000.0,
        0.0,
        1.0,
        15.998544088698,
        16.312374804297,
        15.568732456465,
        15.780227069151,
        1875000.0],
       [u'A',
        u'2002-07-02',
        22.85,
        23.14,
        21.51,
        21.95,
        2903500.0,
        0.0,
        1.0,
        15.589199677047,
        15.787049476012,
        14.674997157693,
        14.97518305957,
        2903500.0],
       [u'A',
        u'2002-07-03',
        21.75,
        23.09,
        21.52,
        23.0,
        3378900.0,
        0.0,
        1.0,
        14.838734922353,
        15.752937441708,
        14.681819564554,
        15.69153577996,
        3378900.0],
       [u'A',
        u'2002-07-05',
        23.0,
        24.25,
        22.95,
        23.95,
        1751200.0,
        0.0,
        1.0,
        15.69153577996,
        16.544336637566,
        15.657423745656,
        16.339664431741,
        1751200.0],
       [u'A',
        u'2002-07-08',
        24.0,
        24.06,
        22.56,
        23.0,
        2720000.0,
        0.0,
        1.0,
        16.373776466045,
        16.41471090721,
        15.391349878082,
        15.69153577996,
        2720000.0],
       [u'A',
        u'2002-07-09',
        22.9,
        23.75,
        22.5,
        22.65,
        1915500.0,
        0.0,
        1.0,
        15.623311711351,
        16.203216294524,
        15.350415436917,
        15.45275153983,
        1915500.0],
       [u'A',
        u'2002-07-10',
        23.05,
        23.3,
        22.07,
        22.09,
        1735800.0,
        0.0,
        1.0,
        15.725647814264,
        15.896207985786,
        15.057051941901,
        15.070696755622,
        1735800.0],
       [u'A',
        u'2002-07-11',
        22.0,
        23.99,
        21.6,
        23.55,
        2706500.0,
        0.0,
        1.0,
        15.009295093875,
        16.366954059184,
        14.736398819441,
        16.066768157307,
        2706500.0],
       [u'A',
        u'2002-07-12',
        23.75,
        24.3,
        23.12,
        23.87,
        3160500.0,
        0.0,
        1.0,
        16.203216294524,
        16.578448671871,
        15.77340466229,
        16.285085176854,
        3160500.0],
       [u'A',
        u'2002-07-15',
        23.52,
        23.85,
        22.34,
        23.57,
        2051700.0,
        0.0,
        1.0,
        16.046300936724,
        16.271440363132,
        15.241256927144,
        16.080412971029,
        2051700.0],
       [u'A',
        u'2002-07-16',
        22.86,
        24.47,
        22.7,
        23.29,
        2730700.0,
        0.0,
        1.0,
        15.596022083908,
        16.694429588505,
        15.486863574134,
        15.889385578925,
        2730700.0],
       [u'A',
        u'2002-07-17',
        23.54,
        24.1,
        22.03,
        22.72,
        2571100.0,
        0.0,
        1.0,
        16.059945750446,
        16.442000534654,
        15.029762314457,
        15.500508387856,
        2571100.0],
       [u'A',
        u'2002-07-18',
        22.7,
        23.15,
        21.64,
        21.73,
        2205400.0,
        0.0,
        1.0,
        15.486863574134,
        15.793871882873,
        14.763688446884,
        14.825090108632,
        2205400.0],
       [u'A',
        u'2002-07-19',
        21.48,
        21.71,
        20.38,
        20.75,
        3318600.0,
        0.0,
        1.0,
        14.65452993711,
        14.81144529491,
        13.904065182417,
        14.156494236268,
        3318600.0],
       [u'A',
        u'2002-07-22',
        20.45,
        20.9,
        19.7,
        19.99,
        3243600.0,
        0.0,
        1.0,
        13.951822030443,
        14.258830339181,
        13.440141515879,
        13.637991314843,
        3243600.0],
       [u'A',
        u'2002-07-23',
        20.05,
        20.42,
        19.43,
        19.74,
        2947300.0,
        0.0,
        1.0,
        13.678925756009,
        13.93135480986,
        13.255936530636,
        13.467431143322,
        2947300.0],
       [u'A',
        u'2002-07-24',
        19.5,
        19.59,
        18.07,
        18.94,
        4524000.0,
        0.0,
        1.0,
        13.303693378662,
        13.365095040409,
        12.32808919756,
        12.921638594454,
        4524000.0],
       [u'A',
        u'2002-07-25',
        18.65,
        18.79,
        16.0,
        16.79,
        4512300.0,
        0.0,
        1.0,
        12.723788795489,
        12.819302491541,
        10.915850977363,
        11.454821119371,
        4512300.0],
       [u'A',
        u'2002-07-26',
        17.05,
        17.59,
        16.91,
        17.31,
        2489700.0,
        0.0,
        1.0,
        11.632203697753,
        12.000613668239,
        11.536690001701,
        11.809586276135,
        2489700.0],
       [u'A',
        u'2002-07-29',
        17.55,
        18.32,
        17.55,
        18.32,
        2147200.0,
        0.0,
        1.0,
        11.973324040796,
        12.498649369081,
        11.973324040796,
        12.498649369081,
        2147200.0],
       [u'A',
        u'2002-07-30',
        18.32,
        18.88,
        17.6,
        18.53,
        3397500.0,
        0.0,
        1.0,
        12.498649369081,
        12.880704153289,
        12.0074360751,
        12.641919913159,
        3397500.0],
       [u'A',
        u'2002-07-31',
        18.65,
        18.9,
        17.85,
        18.88,
        1637400.0,
        0.0,
        1.0,
        12.723788795489,
        12.894348967011,
        12.177996246621,
        12.880704153289,
        1637400.0],
       [u'A',
        u'2002-08-01',
        18.52,
        18.88,
        17.6,
        17.76,
        2778500.0,
        0.0,
        1.0,
        12.635097506298,
        12.880704153289,
        12.0074360751,
        12.116594584873,
        2778500.0],
       [u'A',
        u'2002-08-02',
        17.3,
        17.44,
        16.25,
        16.84,
        1880300.0,
        0.0,
        1.0,
        11.802763869274,
        11.898277565326,
        11.086411148885,
        11.488933153675,
        1880300.0],
       [u'A',
        u'2002-08-05',
        17.0,
        17.05,
        15.43,
        15.68,
        1366900.0,
        0.0,
        1.0,
        11.598091663449,
        11.632203697753,
        10.526973786295,
        10.697533957816,
        1366900.0],
       [u'A',
        u'2002-08-06',
        15.93,
        16.75,
        15.93,
        16.27,
        1420600.0,
        0.0,
        1.0,
        10.868094129337,
        11.427531491927,
        10.868094129337,
        11.100055962606,
        1420600.0],
       [u'A',
        u'2002-08-07',
        16.98,
        17.08,
        15.95,
        16.87,
        1606100.0,
        0.0,
        1.0,
        11.584446849727,
        11.652670918335,
        10.881738943059,
        11.509400374258,
        1606100.0],
       [u'A',
        u'2002-08-08',
        17.0,
        17.3,
        15.96,
        17.2,
        2114700.0,
        0.0,
        1.0,
        11.598091663449,
        11.802763869274,
        10.88856134992,
        11.734539800666,
        2114700.0],
       [u'A',
        u'2002-08-09',
        16.63,
        17.04,
        16.38,
        16.72,
        1612300.0,
        0.0,
        1.0,
        11.345662609597,
        11.625381290892,
        11.175102438076,
        11.407064271345,
        1612300.0],
       [u'A',
        u'2002-08-12',
        16.3,
        16.68,
        16.0,
        16.46,
        1128200.0,
        0.0,
        1.0,
        11.120523183189,
        11.379774643901,
        10.915850977363,
        11.229681692963,
        1128200.0],
       [u'A',
        u'2002-08-13',
        16.46,
        16.72,
        15.86,
        15.89,
        2307100.0,
        0.0,
        1.0,
        11.229681692963,
        11.407064271345,
        10.820337281312,
        10.840804501894,
        2307100.0],
       [u'A',
        u'2002-08-14',
        15.77,
        16.04,
        15.06,
        16.04,
        2497000.0,
        0.0,
        1.0,
        10.758935619564,
        10.943140604807,
        10.274544732443,
        10.943140604807,
        2497000.0],
       [u'A',
        u'2002-08-15',
        16.35,
        16.42,
        15.9,
        16.03,
        2384100.0,
        0.0,
        1.0,
        11.154635217493,
        11.202392065519,
        10.847626908755,
        10.936318197946,
        2384100.0],
       [u'A',
        u'2002-08-16',
        15.99,
        16.75,
        15.51,
        15.96,
        3422400.0,
        0.0,
        1.0,
        10.909028570503,
        11.427531491927,
        10.581553041182,
        10.88856134992,
        3422400.0],
       [u'A',
        u'2002-08-19',
        15.86,
        17.65,
        15.8,
        17.44,
        3001000.0,
        0.0,
        1.0,
        10.820337281312,
        12.041548109404,
        10.779402840146,
        11.898277565326,
        3001000.0],
       [u'A',
        u'2002-08-20',
        16.25,
        17.4,
        15.75,
        16.2,
        7678300.0,
        0.0,
        1.0,
        11.086411148885,
        11.870987937883,
        10.745290805842,
        11.05229911458,
        7678300.0],
       [u'A',
        u'2002-08-21',
        16.35,
        17.25,
        16.06,
        17.05,
        2624400.0,
        0.0,
        1.0,
        11.154635217493,
        11.76865183497,
        10.956785418529,
        11.632203697753,
        2624400.0],
       [u'A',
        u'2002-08-22',
        16.96,
        17.2,
        16.51,
        17.02,
        2460200.0,
        0.0,
        1.0,
        11.570802036005,
        11.734539800666,
        11.263793727267,
        11.61173647717,
        2460200.0],
       [u'A',
        u'2002-08-23',
        16.86,
        16.87,
        16.02,
        16.02,
        1820100.0,
        0.0,
        1.0,
        11.502577967397,
        11.509400374258,
        10.929495791085,
        10.929495791085,
        1820100.0],
       [u'A',
        u'2002-08-26',
        16.02,
        16.39,
        16.02,
        16.2,
        1596100.0,
        0.0,
        1.0,
        10.929495791085,
        11.181924844937,
        10.929495791085,
        11.05229911458,
        1596100.0],
       [u'A',
        u'2002-08-27',
        16.21,
        16.3,
        15.0,
        15.31,
        3321100.0,
        0.0,
        1.0,
        11.059121521441,
        11.120523183189,
        10.233610291278,
        10.445104903965,
        3321100.0],
       [u'A',
        u'2002-08-28',
        15.18,
        15.26,
        14.81,
        14.85,
        3298700.0,
        0.0,
        1.0,
        10.356413614774,
        10.41099286966,
        10.103984560922,
        10.131274188365,
        3298700.0],
       [u'A',
        u'2002-08-29',
        14.35,
        14.54,
        14.2,
        14.2,
        5953400.0,
        0.0,
        1.0,
        9.7901538453228,
        9.919779575679,
        9.68781774241,
        9.68781774241,
        5953400.0],
       [u'A',
        u'2002-08-30',
        13.9,
        13.91,
        13.33,
        13.43,
        3875700.0,
        0.0,
        1.0,
        9.4831455365845,
        9.4899679434453,
        9.0942683455159,
        9.1624924141244,
        3875700.0],
       [u'A',
        u'2002-09-03',
        13.33,
        13.34,
        12.76,
        12.85,
        5013800.0,
        0.0,
        1.0,
        9.0942683455159,
        9.1010907523768,
        8.7053911544473,
        8.766792816195,
        5013800.0],
       [u'A',
        u'2002-09-04',
        13.04,
        13.65,
        13.0,
        13.5,
        3318300.0,
        0.0,
        1.0,
        8.8964185465512,
        9.3125853650632,
        8.8691289191078,
        9.2102492621504,
        3318300.0],
       [u'A',
        u'2002-09-05',
        13.3,
        13.73,
        13.1,
        13.72,
        5056100.0,
        0.0,
        1.0,
        9.0738011249334,
        9.36716461995,
        8.9373529877163,
        9.3603422130891,
        5056100.0],
       [u'A',
        u'2002-09-06',
        14.05,
        14.35,
        13.89,
        14.15,
        3804400.0,
        0.0,
        1.0,
        9.5854816394973,
        9.7901538453228,
        9.4763231297236,
        9.6537057081058,
        3804400.0],
       [u'A',
        u'2002-09-09',
        14.11,
        14.8,
        13.25,
        14.73,
        3779000.0,
        0.0,
        1.0,
        9.6264160806624,
        10.097162154061,
        9.0396890906291,
        10.049405306035,
        3779000.0],
       [u'A',
        u'2002-09-10',
        14.83,
        15.6,
        14.62,
        15.27,
        3457000.0,
        0.0,
        1.0,
        10.117629374644,
        10.642954702929,
        9.9743588305658,
        10.417815276521,
        3457000.0],
       [u'A',
        u'2002-09-11',
        16.08,
        16.08,
        15.3,
        15.43,
        2107900.0,
        0.0,
        1.0,
        10.97043023225,
        10.97043023225,
        10.438282497104,
        10.526973786295,
        2107900.0],
       [u'A',
        u'2002-09-12',
        15.43,
        15.93,
        15.23,
        15.27,
        3167100.0,
        0.0,
        1.0,
        10.526973786295,
        10.868094129337,
        10.390525649078,
        10.417815276521,
        3167100.0],
       [u'A',
        u'2002-09-13',
        15.24,
        15.47,
        14.6,
        14.98,
        2388300.0,
        0.0,
        1.0,
        10.397348055939,
        10.554263413738,
        9.9607140168441,
        10.219965477557,
        2388300.0],
       [u'A',
        u'2002-09-16',
        14.9,
        15.19,
        14.32,
        14.59,
        1929300.0,
        0.0,
        1.0,
        10.16538622267,
        10.363236021634,
        9.7696866247403,
        9.9538916099833,
        1929300.0],
       [u'A',
        u'2002-09-17',
        14.9,
        15.05,
        14.6,
        14.76,
        2242700.0,
        0.0,
        1.0,
        10.16538622267,
        10.267722325582,
        9.9607140168441,
        10.069872526618,
        2242700.0],
       [u'A',
        u'2002-09-18',
        14.7,
        14.8,
        14.26,
        14.75,
        4046200.0,
        0.0,
        1.0,
        10.028938085453,
        10.097162154061,
        9.7287521835752,
        10.063050119757,
        4046200.0],
       [u'A',
        u'2002-09-19',
        14.6,
        14.6,
        14.0,
        14.07,
        2470800.0,
        0.0,
        1.0,
        9.9607140168441,
        9.9607140168441,
        9.551369605193,
        9.599126453219,
        2470800.0],
       [u'A',
        u'2002-09-20',
        14.12,
        14.31,
        13.75,
        13.97,
        2937100.0,
        0.0,
        1.0,
        9.6332384875232,
        9.7628642178794,
        9.3808094336717,
        9.5309023846104,
        2937100.0],
       [u'A',
        u'2002-09-23',
        13.9,
        13.95,
        13.24,
        13.35,
        2807400.0,
        0.0,
        1.0,
        9.4831455365845,
        9.5172575708887,
        9.0328666837682,
        9.1079131592376,
        2807400.0],
       [u'A',
        u'2002-09-24',
        13.25,
        13.7,
        13.09,
        13.2,
        3143300.0,
        0.0,
        1.0,
        9.0396890906291,
        9.3466973993674,
        8.9305305808555,
        9.0055770563248,
        3143300.0],
       [u'A',
        u'2002-09-25',
        13.4,
        14.31,
        13.32,
        14.07,
        2101000.0,
        0.0,
        1.0,
        9.1420251935419,
        9.7628642178794,
        9.0874459386551,
        9.599126453219,
        2101000.0],
       [u'A',
        u'2002-09-26',
        14.12,
        14.3,
        13.48,
        13.78,
        2978000.0,
        0.0,
        1.0,
        9.6332384875232,
        9.7560418110186,
        9.1966044484287,
        9.4012766542543,
        2978000.0],
       [u'A',
        u'2002-09-27',
        13.68,
        14.01,
        13.09,
        13.09,
        2437800.0,
        0.0,
        1.0,
        9.3330525856457,
        9.5581920120539,
        8.9305305808555,
        8.9305305808555,
        2437800.0],
       [u'A',
        u'2002-09-30',
        12.85,
        13.45,
        12.35,
        13.06,
        2661700.0,
        0.0,
        1.0,
        8.766792816195,
        9.1761372278461,
        8.4256724731524,
        8.9100633602729,
        2661700.0],
       [u'A',
        u'2002-10-01',
        13.25,
        13.25,
        12.55,
        13.05,
        3076200.0,
        0.0,
        1.0,
        9.0396890906291,
        9.0396890906291,
        8.5621206103694,
        8.9032409534121,
        3076200.0],
       [u'A',
        u'2002-10-02',
        13.04,
        13.46,
        12.5,
        12.5,
        2014100.0,
        0.0,
        1.0,
        8.8964185465512,
        9.182959634707,
        8.5280085760652,
        8.5280085760652,
        2014100.0],
       [u'A',
        u'2002-10-03',
        12.5,
        12.68,
        12.23,
        12.3,
        2346300.0,
        0.0,
        1.0,
        8.5280085760652,
        8.6508118995605,
        8.3438035908222,
        8.3915604388481,
        2346300.0],
       [u'A',
        u'2002-10-04',
        12.32,
        12.4,
        11.75,
        11.8,
        2272500.0,
        0.0,
        1.0,
        8.4052052525698,
        8.4597845074567,
        8.0163280615013,
        8.0504400958055,
        2272500.0],
       [u'A',
        u'2002-10-07',
        11.81,
        12.5,
        11.52,
        11.52,
        2553200.0,
        0.0,
        1.0,
        8.0572625026664,
        8.5280085760652,
        7.8594127037017,
        7.8594127037017,
        2553200.0],
       [u'A',
        u'2002-10-08',
        11.62,
        12.4,
        11.59,
        12.23,
        3503800.0,
        0.0,
        1.0,
        7.9276367723102,
        8.4597845074567,
        7.9071695517276,
        8.3438035908222,
        3503800.0],
       [u'A',
        u'2002-10-09',
        12.0,
        12.12,
        10.9,
        10.9,
        3284900.0,
        0.0,
        1.0,
        8.1868882330226,
        8.2687571153528,
        7.4364234783288,
        7.4364234783288,
        3284900.0],
       [u'A',
        u'2002-10-10',
        10.95,
        11.13,
        10.8,
        10.85,
        4853400.0,
        0.0,
        1.0,
        7.4705355126331,
        7.5933388361284,
        7.3681994097203,
        7.4023114440246,
        4853400.0],
       [u'A',
        u'2002-10-11',
        10.95,
        11.26,
        10.7,
        10.9,
        3775300.0,
        0.0,
        1.0,
        7.4705355126331,
        7.6820301253195,
        7.2999753411118,
        7.4364234783288,
        3775300.0],
       [u'A',
        u'2002-10-14',
        10.7,
        11.18,
        10.5,
        11.01,
        2318900.0,
        0.0,
        1.0,
        7.2999753411118,
        7.6274508704327,
        7.1635272038948,
        7.5114699537982,
        2318900.0],
       [u'A',
        u'2002-10-15',
        11.36,
        12.0,
        11.02,
        11.87,
        2482000.0,
        0.0,
        1.0,
        7.750254193928,
        8.1868882330226,
        7.5182923606591,
        8.0981969438315,
        2482000.0],
       [u'A',
        u'2002-10-16',
        11.6,
        11.8,
        11.08,
        11.25,
        2865400.0,
        0.0,
        1.0,
        7.9139919585885,
        8.0504400958055,
        7.5592268018242,
        7.6752077184587,
        2865400.0],
       [u'A',
        u'2002-10-17',
        11.95,
        12.1,
        11.8,
        12.1,
        2639400.0,
        0.0,
        1.0,
        8.1527761987183,
        8.2551123016311,
        8.0504400958055,
        8.2551123016311,
        2639400.0],
       [u'A',
        u'2002-10-18',
        12.06,
        12.18,
        11.3,
        12.1,
        3313200.0,
        0.0,
        1.0,
        8.2278226741877,
        8.3096915565179,
        7.7093197527629,
        8.2551123016311,
        3313200.0],
       [u'A',
        u'2002-10-21',
        11.9,
        12.6,
        11.59,
        12.53,
        2439200.0,
        0.0,
        1.0,
        8.1186641644141,
        8.5962326446737,
        7.9071695517276,
        8.5484757966477,
        2439200.0],
       [u'A',
        u'2002-10-22',
        12.02,
        12.4,
        11.95,
        12.3,
        2478000.0,
        0.0,
        1.0,
        8.2005330467443,
        8.4597845074567,
        8.1527761987183,
        8.3915604388481,
        2478000.0],
       [u'A',
        u'2002-10-23',
        12.2,
        12.45,
        11.7,
        12.0,
        3879500.0,
        0.0,
        1.0,
        8.3233363702396,
        8.4938965417609,
        7.982216027197,
        8.1868882330226,
        3879500.0],
       [u'A',
        u'2002-10-24',
        12.26,
        13.55,
        12.2,
        13.05,
        3087400.0,
        0.0,
        1.0,
        8.3642708114047,
        9.2443612964547,
        8.3233363702396,
        8.9032409534121,
        3087400.0],
       [u'A',
        u'2002-10-25',
        12.97,
        13.1,
        12.56,
        12.94,
        2116200.0,
        0.0,
        1.0,
        8.8486616985252,
        8.9373529877163,
        8.5689430172303,
        8.8281944779427,
        2116200.0],
       [u'A',
        u'2002-10-28',
        13.15,
        13.94,
        13.15,
        13.52,
        1927800.0,
        0.0,
        1.0,
        8.9714650220206,
        9.5104351640279,
        8.9714650220206,
        9.2238940758721,
        1927800.0],
       [u'A',
        u'2002-10-29',
        13.2,
        13.5,
        12.35,
        12.72,
        2367700.0,
        0.0,
        1.0,
        9.0055770563248,
        9.2102492621504,
        8.4256724731524,
        8.6781015270039,
        2367700.0],
       [u'A',
        u'2002-10-30',
        12.72,
        13.95,
        12.69,
        13.87,
        2594200.0,
        0.0,
        1.0,
        8.6781015270039,
        9.5172575708887,
        8.6576343064214,
        9.4626783160019,
        2594200.0],
       [u'A',
        u'2002-10-31',
        13.98,
        14.22,
        13.56,
        13.75,
        3078300.0,
        0.0,
        1.0,
        9.5377247914713,
        9.7014625561318,
        9.2511837033155,
        9.3808094336717,
        3078300.0],
       [u'A',
        u'2002-11-01',
        13.66,
        14.64,
        13.2,
        14.58,
        2138800.0,
        0.0,
        1.0,
        9.319407771924,
        9.9880036442875,
        9.0055770563248,
        9.9470692031224,
        2138800.0],
       [u'A',
        u'2002-11-04',
        14.75,
        15.65,
        14.7,
        15.03,
        2955400.0,
        0.0,
        1.0,
        10.063050119757,
        10.677066737234,
        10.028938085453,
        10.254077511861,
        2955400.0],
       [u'A',
        u'2002-11-05',
        15.0,
        15.31,
        14.69,
        15.07,
        1595500.0,
        0.0,
        1.0,
        10.233610291278,
        10.445104903965,
        10.022115678592,
        10.281367139304,
        1595500.0],
       [u'A',
        u'2002-11-06',
        15.02,
        15.3,
        14.57,
        14.96,
        1575700.0,
        0.0,
        1.0,
        10.247255105,
        10.438282497104,
        9.9402467962616,
        10.206320663835,
        1575700.0],
       [u'A',
        u'2002-11-07',
        14.74,
        14.75,
        14.01,
        14.21,
        1696200.0,
        0.0,
        1.0,
        10.056227712896,
        10.063050119757,
        9.5581920120539,
        9.6946401492709,
        1696200.0],
       [u'A',
        u'2002-11-08',
        14.0,
        14.45,
        13.78,
        14.05,
        1783200.0,
        0.0,
        1.0,
        9.551369605193,
        9.8583779139314,
        9.4012766542543,
        9.5854816394973,
        1783200.0],
       [u'A',
        u'2002-11-11',
        13.78,
        13.99,
        13.5,
        13.54,
        1176200.0,
        0.0,
        1.0,
        9.4012766542543,
        9.5445471983322,
        9.2102492621504,
        9.2375388895938,
        1176200.0],
       [u'A',
        u'2002-11-12',
        13.54,
        14.15,
        13.54,
        13.8,
        1537100.0,
        0.0,
        1.0,
        9.2375388895938,
        9.6537057081058,
        9.2375388895938,
        9.414921467976,
        1537100.0],
       [u'A',
        u'2002-11-13',
        13.5,
        13.79,
        13.19,
        13.4,
        2172900.0,
        0.0,
        1.0,
        9.2102492621504,
        9.4080990611151,
        8.998754649464,
        9.1420251935419,
        2172900.0],
       [u'A',
        u'2002-11-14',
        13.4,
        14.01,
        13.2,
        13.98,
        1679800.0,
        0.0,
        1.0,
        9.1420251935419,
        9.5581920120539,
        9.0055770563248,
        9.5377247914713,
        1679800.0],
       [u'A',
        u'2002-11-15',
        13.76,
        14.44,
        13.6,
        13.8,
        2353300.0,
        0.0,
        1.0,
        9.3876318405326,
        9.8515555070705,
        9.2784733307589,
        9.414921467976,
        2353300.0],
       [u'A',
        u'2002-11-18',
        13.7,
        14.08,
        13.52,
        13.6,
        2143500.0,
        0.0,
        1.0,
        9.3466973993674,
        9.6059488600798,
        9.2238940758721,
        9.2784733307589,
        2143500.0],
       [u'A',
        u'2002-11-19',
        14.75,
        17.07,
        14.7,
        16.6,
        13242600.0,
        0.0,
        1.0,
        10.063050119757,
        11.645848511475,
        10.028938085453,
        11.325195389015,
        13242600.0],
       [u'A',
        u'2002-11-20',
        16.59,
        17.2,
        16.01,
        17.01,
        4733100.0,
        0.0,
        1.0,
        11.318372982154,
        11.734539800666,
        10.922673384224,
        11.60491407031,
        4733100.0],
       [u'A',
        u'2002-11-21',
        17.4,
        18.54,
        17.39,
        18.24,
        5630200.0,
        0.0,
        1.0,
        11.870987937883,
        12.64874232002,
        11.864165531022,
        12.444070114194,
        5630200.0],
       [u'A',
        u'2002-11-22',
        18.25,
        18.75,
        18.0,
        18.25,
        3379800.0,
        0.0,
        1.0,
        12.450892521055,
        12.792012864098,
        12.280332349534,
        12.450892521055,
        3379800.0],
       [u'A',
        u'2002-11-25',
        18.1,
        19.6,
        17.97,
        19.53,
        3824300.0,
        0.0,
        1.0,
        12.348556418142,
        13.37191744727,
        12.259865128951,
        13.324160599244,
        3824300.0],
       [u'A',
        u'2002-11-26',
        19.63,
        19.63,
        18.68,
        18.76,
        2935000.0,
        0.0,
        1.0,
        13.392384667853,
        13.392384667853,
        12.744256016072,
        12.798835270959,
        2935000.0],
       [u'A',
        u'2002-11-27',
        18.95,
        19.6,
        18.86,
        19.58,
        1769000.0,
        0.0,
        1.0,
        12.928461001315,
        13.37191744727,
        12.867059339567,
        13.358272633549,
        1769000.0],
       [u'A',
        u'2002-11-29',
        19.59,
        19.65,
        19.14,
        19.41,
        861200.0,
        0.0,
        1.0,
        13.365095040409,
        13.406029481574,
        13.058086731671,
        13.242291716914,
        861200.0],
       [u'A',
        u'2002-12-02',
        19.75,
        20.15,
        18.9,
        19.3,
        1987500.0,
        0.0,
        1.0,
        13.474253550183,
        13.747149824617,
        12.894348967011,
        13.167245241445,
        1987500.0],
       [u'A',
        u'2002-12-03',
        19.05,
        19.06,
        18.0,
        18.06,
        2846600.0,
        0.0,
        1.0,
        12.996685069923,
        13.003507476784,
        12.280332349534,
        12.321266790699,
        2846600.0],
       [u'A',
        u'2002-12-04',
        17.55,
        17.56,
        16.72,
        17.11,
        3844100.0,
        0.0,
        1.0,
        11.973324040796,
        11.980146447656,
        11.407064271345,
        11.673138138918,
        3844100.0],
       [u'A',
        u'2002-12-05',
        17.35,
        17.47,
        16.9,
        16.95,
        1548000.0,
        0.0,
        1.0,
        11.836875903578,
        11.918744785909,
        11.52986759484,
        11.563979629144,
        1548000.0],
       [u'A',
        u'2002-12-06',
        16.82,
        17.17,
        16.46,
        16.79,
        2175200.0,
        0.0,
        1.0,
        11.475288339953,
        11.714072580083,
        11.229681692963,
        11.454821119371,
        2175200.0],
       [u'A',
        u'2002-12-09',
        16.6,
        16.8,
        16.35,
        16.4,
        2601700.0,
        0.0,
        1.0,
        11.325195389015,
        11.461643526232,
        11.154635217493,
        11.188747251798,
        2601700.0],
       [u'A',
        u'2002-12-10',
        16.41,
        17.18,
        16.41,
        17.16,
        2271500.0,
        0.0,
        1.0,
        11.195569658658,
        11.720894986944,
        11.195569658658,
        11.707250173222,
        2271500.0],
       [u'A',
        u'2002-12-11',
        16.96,
        17.79,
        16.83,
        17.32,
        2231500.0,
        0.0,
        1.0,
        11.570802036005,
        12.137061805456,
        11.482110746814,
        11.816408682996,
        2231500.0],
       [u'A',
        u'2002-12-12',
        17.25,
        17.64,
        17.0,
        17.18,
        2582100.0,
        0.0,
        1.0,
        11.76865183497,
        12.034725702543,
        11.598091663449,
        11.720894986944,
        2582100.0],
       [u'A',
        u'2002-12-13',
        17.0,
        17.2,
        16.59,
        17.2,
        2122700.0,
        0.0,
        1.0,
        11.598091663449,
        11.734539800666,
        11.318372982154,
        11.734539800666,
        2122700.0],
       [u'A',
        u'2002-12-16',
        17.2,
        17.73,
        17.16,
        17.62,
        1507400.0,
        0.0,
        1.0,
        11.734539800666,
        12.096127364291,
        11.707250173222,
        12.021080888821,
        1507400.0],
       [u'A',
        u'2002-12-17',
        17.62,
        17.93,
        17.12,
        17.4,
        1294600.0,
        0.0,
        1.0,
        12.021080888821,
        12.232575501508,
        11.679960545779,
        11.870987937883,
        1294600.0],
       [u'A',
        u'2002-12-18',
        17.2,
        18.91,
        16.6,
        16.85,
        1446700.0,
        0.0,
        1.0,
        11.734539800666,
        12.901171373871,
        11.325195389015,
        11.495755560536,
        1446700.0],
       [u'A',
        u'2002-12-19',
        16.6,
        17.16,
        16.47,
        16.76,
        1984900.0,
        0.0,
        1.0,
        11.325195389015,
        11.707250173222,
        11.236504099823,
        11.434353898788,
        1984900.0],
       [u'A',
        u'2002-12-20',
        16.8,
        18.0,
        16.8,
        18.0,
        3652700.0,
        0.0,
        1.0,
        11.461643526232,
        12.280332349534,
        11.461643526232,
        12.280332349534,
        3652700.0],
       [u'A',
        u'2002-12-23',
        17.91,
        18.67,
        17.84,
        18.54,
        3042500.0,
        0.0,
        1.0,
        12.218930687786,
        12.737433609211,
        12.17117383976,
        12.64874232002,
        3042500.0],
       [u'A',
        u'2002-12-24',
        18.37,
        18.49,
        18.13,
        18.23,
        793600.0,
        0.0,
        1.0,
        12.532761403385,
        12.614630285716,
        12.369023638725,
        12.437247707333,
        793600.0],
       [u'A',
        u'2002-12-26',
        18.33,
        18.67,
        18.24,
        18.3,
        1223200.0,
        0.0,
        1.0,
        12.505471775942,
        12.737433609211,
        12.444070114194,
        12.485004555359,
        1223200.0],
       [u'A',
        u'2002-12-27',
        18.15,
        18.49,
        18.11,
        18.2,
        1114700.0,
        0.0,
        1.0,
        12.382668452447,
        12.614630285716,
        12.355378825003,
        12.416780486751,
        1114700.0],
       [u'A',
        u'2002-12-30',
        18.05,
        18.26,
        17.55,
        18.01,
        1643300.0,
        0.0,
        1.0,
        12.314444383838,
        12.457714927916,
        11.973324040796,
        12.287154756395,
        1643300.0],
       [u'A',
        u'2002-12-31',
        17.95,
        18.19,
        17.79,
        17.96,
        1164500.0,
        0.0,
        1.0,
        12.24622031523,
        12.40995807989,
        12.137061805456,
        12.25304272209,
        1164500.0],
       [u'A',
        u'2003-01-02',
        18.22,
        19.19,
        18.14,
        19.14,
        2418500.0,
        0.0,
        1.0,
        12.430425300473,
        13.092198765975,
        12.375846045586,
        13.058086731671,
        2418500.0],
       [u'A',
        u'2003-01-03',
        19.0,
        19.44,
        18.82,
        19.05,
        1875900.0,
        0.0,
        1.0,
        12.962573035619,
        13.262758937497,
        12.839769712124,
        12.996685069923,
        1875900.0],
       [u'A',
        u'2003-01-06',
        19.0,
        20.11,
        19.0,
        19.96,
        3969600.0,
        0.0,
        1.0,
        12.962573035619,
        13.719860197174,
        12.962573035619,
        13.617524094261,
        3969600.0],
       [u'A',
        u'2003-01-07',
        19.92,
        20.3,
        19.68,
        19.78,
        2419800.0,
        0.0,
        1.0,
        13.590234466817,
        13.84948592753,
        13.426496702157,
        13.494720770766,
        2419800.0],
       [u'A',
        u'2003-01-08',
        19.7,
        19.7,
        18.77,
        18.82,
        2284600.0,
        0.0,
        1.0,
        13.440141515879,
        13.440141515879,
        12.805657677819,
        12.839769712124,
        2284600.0],
       [u'A',
        u'2003-01-09',
        18.95,
        19.75,
        18.95,
        19.57,
        3224400.0,
        0.0,
        1.0,
        12.928461001315,
        13.474253550183,
        12.928461001315,
        13.351450226688,
        3224400.0],
       [u'A',
        u'2003-01-10',
        19.4,
        20.0,
        19.19,
        19.9,
        2996400.0,
        0.0,
        1.0,
        13.235469310053,
        13.644813721704,
        13.092198765975,
        13.576589653096,
        2996400.0],
       [u'A',
        u'2003-01-13',
        19.98,
        20.22,
        19.4,
        19.62,
        1285200.0,
        0.0,
        1.0,
        13.631168907983,
        13.794906672643,
        13.235469310053,
        13.385562260992,
        1285200.0],
       [u'A',
        u'2003-01-14',
        19.62,
        20.06,
        19.51,
        19.91,
        2868100.0,
        0.0,
        1.0,
        13.385562260992,
        13.685748162869,
        13.310515785523,
        13.583412059957,
        2868100.0],
       [u'A',
        u'2003-01-15',
        19.92,
        20.0,
        18.73,
        18.88,
        2722800.0,
        0.0,
        1.0,
        13.590234466817,
        13.644813721704,
        12.778368050376,
        12.880704153289,
        2722800.0],
       [u'A',
        u'2003-01-16',
        19.2,
        19.49,
        18.56,
        18.68,
        2071000.0,
        0.0,
        1.0,
        13.099021172836,
        13.296870971801,
        12.662387133742,
        12.744256016072,
        2071000.0],
       [u'A',
        u'2003-01-17',
        18.43,
        18.44,
        17.82,
        18.05,
        1508100.0,
        0.0,
        1.0,
        12.573695844551,
        12.580518251411,
        12.157529026039,
        12.314444383838,
        1508100.0],
       [u'A',
        u'2003-01-21',
        18.4,
        18.5,
        17.65,
        17.69,
        1804900.0,
        0.0,
        1.0,
        12.553228623968,
        12.621452692576,
        12.041548109404,
        12.068837736847,
        1804900.0],
       [u'A',
        u'2003-01-22',
        17.55,
        17.76,
        17.38,
        17.42,
        2198100.0,
        0.0,
        1.0,
        11.973324040796,
        12.116594584873,
        11.857343124161,
        11.884632751604,
        2198100.0],
       [u'A',
        u'2003-01-23',
        17.65,
        17.83,
        17.13,
        17.37,
        2454300.0,
        0.0,
        1.0,
        12.041548109404,
        12.164351432899,
        11.68678295264,
        11.8505207173,
        2454300.0],
       [u'A',
        u'2003-01-24',
        17.38,
        17.56,
        16.7,
        16.7,
        2545500.0,
        0.0,
        1.0,
        11.857343124161,
        11.980146447656,
        11.393419457623,
        11.393419457623,
        2545500.0],
       [u'A',
        u'2003-01-27',
        16.36,
        16.72,
        16.12,
        16.23,
        1909700.0,
        0.0,
        1.0,
        11.161457624354,
        11.407064271345,
        10.997719859694,
        11.072766335163,
        1909700.0],
       [u'A',
        u'2003-01-28',
        16.33,
        16.9,
        16.2,
        16.8,
        2255000.0,
        0.0,
        1.0,
        11.140990403772,
        11.52986759484,
        11.05229911458,
        11.461643526232,
        2255000.0],
       [u'A',
        u'2003-01-29',
        16.33,
        16.9,
        16.2,
        16.8,
        2045300.0,
        0.0,
        1.0,
        11.140990403772,
        11.52986759484,
        11.05229911458,
        11.461643526232,
        2045300.0],
       [u'A',
        u'2003-01-30',
        17.0,
        17.0,
        16.01,
        16.14,
        1397200.0,
        0.0,
        1.0,
        11.598091663449,
        11.598091663449,
        10.922673384224,
        11.011364673415,
        1397200.0],
       [u'A',
        u'2003-01-31',
        16.0,
        16.7,
        15.82,
        16.48,
        2228400.0,
        0.0,
        1.0,
        10.915850977363,
        11.393419457623,
        10.793047653868,
        11.243326506684,
        2228400.0],
       [u'A',
        u'2003-02-03',
        16.48,
        16.82,
        16.25,
        16.49,
        1410900.0,
        0.0,
        1.0,
        11.243326506684,
        11.475288339953,
        11.086411148885,
        11.250148913545,
        1410900.0],
       [u'A',
        u'2003-02-04',
        16.49,
        16.49,
        15.76,
        16.3,
        1366400.0,
        0.0,
        1.0,
        11.250148913545,
        11.250148913545,
        10.752113212703,
        11.120523183189,
        1366400.0],
       [u'A',
        u'2003-02-05',
        16.3,
        16.82,
        16.1,
        16.32,
        2489000.0,
        0.0,
        1.0,
        11.120523183189,
        11.475288339953,
        10.984075045972,
        11.134167996911,
        2489000.0],
       [u'A',
        u'2003-02-06',
        16.32,
        16.32,
        12.26,
        12.26,
        16184600.0,
        0.0,
        1.0,
        11.134167996911,
        11.134167996911,
        8.3642708114047,
        8.3642708114047,
        16184600.0],
       [u'A',
        u'2003-02-07',
        12.26,
        12.35,
        11.3,
        11.45,
        8229400.0,
        0.0,
        1.0,
        8.3642708114047,
        8.4256724731524,
        7.7093197527629,
        7.8116558556757,
        8229400.0],
       [u'A',
        u'2003-02-10',
        11.45,
        11.96,
        11.4,
        11.73,
        6566600.0,
        0.0,
        1.0,
        7.8116558556757,
        8.1595986055792,
        7.7775438213714,
        8.0026832477796,
        6566600.0],
       [u'A',
        u'2003-02-11',
        11.98,
        12.24,
        11.9,
        12.05,
        3864000.0,
        0.0,
        1.0,
        8.1732434193009,
        8.350625997683,
        8.1186641644141,
        8.2210002673268,
        3864000.0],
       [u'A',
        u'2003-02-12',
        12.05,
        12.54,
        12.0,
        12.43,
        4749100.0,
        0.0,
        1.0,
        8.2210002673268,
        8.5552982035086,
        8.1868882330226,
        8.4802517280392,
        4749100.0],
       [u'A',
        u'2003-02-13',
        12.73,
        12.82,
        12.15,
        12.45,
        4152000.0,
        0.0,
        1.0,
        8.6849239338648,
        8.7463255956125,
        8.2892243359354,
        8.4938965417609,
        4152000.0],
       [u'A',
        u'2003-02-14',
        12.35,
        12.6,
        12.12,
        12.49,
        2077700.0,
        0.0,
        1.0,
        8.4256724731524,
        8.5962326446737,
        8.2687571153528,
        8.5211861692043,
        2077700.0],
       [u'A',
        u'2003-02-18',
        12.62,
        12.77,
        12.5,
        12.7,
        2139200.0,
        0.0,
        1.0,
        8.6098774583954,
        8.7122135613082,
        8.5280085760652,
        8.6644567132822,
        2139200.0],
       [u'A',
        u'2003-02-19',
        12.65,
        12.66,
        12.34,
        12.53,
        2603800.0,
        0.0,
        1.0,
        8.630344678978,
        8.6371670858388,
        8.4188500662915,
        8.5484757966477,
        2603800.0],
       [u'A',
        u'2003-02-20',
        12.58,
        12.93,
        12.42,
        12.6,
        3053000.0,
        0.0,
        1.0,
        8.582587830952,
        8.8213720710818,
        8.4734293211784,
        8.5962326446737,
        3053000.0],
       [u'A',
        u'2003-02-21',
        12.95,
        13.7,
        12.64,
        13.45,
        4564300.0,
        0.0,
        1.0,
        8.8350168848035,
        9.3466973993674,
        8.6235222721171,
        9.1761372278461,
        4564300.0],
       [u'A',
        u'2003-02-24',
        13.3,
        13.3,
        12.92,
        12.99,
        2031400.0,
        0.0,
        1.0,
        9.0738011249334,
        9.0738011249334,
        8.814549664221,
        8.8623065122469,
        2031400.0],
       [u'A',
        u'2003-02-25',
        12.94,
        13.19,
        12.63,
        13.18,
        1954400.0,
        0.0,
        1.0,
        8.8281944779427,
        8.998754649464,
        8.6166998652563,
        8.9919322426031,
        1954400.0],
       [u'A',
        u'2003-02-26',
        13.18,
        13.38,
        12.75,
        12.8,
        2253800.0,
        0.0,
        1.0,
        8.9919322426031,
        9.1283803798202,
        8.6985687475865,
        8.7326807818907,
        2253800.0],
       [u'A',
        u'2003-02-27',
        12.88,
        13.19,
        12.88,
        13.1,
        1720300.0,
        0.0,
        1.0,
        8.7872600367776,
        8.998754649464,
        8.7872600367776,
        8.9373529877163,
        1720300.0],
       [u'A',
        u'2003-02-28',
        13.17,
        13.5,
        13.08,
        13.2,
        1832100.0,
        0.0,
        1.0,
        8.9851098357423,
        9.2102492621504,
        8.9237081739946,
        9.0055770563248,
        1832100.0],
       [u'A',
        u'2003-03-03',
        13.4,
        13.65,
        12.91,
        13.02,
        1460100.0,
        0.0,
        1.0,
        9.1420251935419,
        9.3125853650632,
        8.8077272573601,
        8.8827737328295,
        1460100.0],
       [u'A',
        u'2003-03-04',
        13.03,
        13.13,
        12.76,
        12.85,
        1602600.0,
        0.0,
        1.0,
        8.8895961396903,
        8.9578202082989,
        8.7053911544473,
        8.766792816195,
        1602600.0],
       [u'A',
        u'2003-03-05',
        12.77,
        13.03,
        12.62,
        13.03,
        2177400.0,
        0.0,
        1.0,
        8.7122135613082,
        8.8895961396903,
        8.6098774583954,
        8.8895961396903,
        2177400.0],
       [u'A',
        u'2003-03-06',
        12.93,
        13.06,
        12.6,
        13.06,
        1627900.0,
        0.0,
        1.0,
        8.8213720710818,
        8.9100633602729,
        8.5962326446737,
        8.9100633602729,
        1627900.0],
       [u'A',
        u'2003-03-07',
        12.96,
        13.39,
        12.84,
        13.39,
        2037100.0,
        0.0,
        1.0,
        8.8418392916644,
        9.135202786681,
        8.7599704093342,
        9.135202786681,
        2037100.0],
       [u'A',
        u'2003-03-10',
        13.15,
        13.15,
        12.79,
        12.93,
        2238200.0,
        0.0,
        1.0,
        8.9714650220206,
        8.9714650220206,
        8.7258583750299,
        8.8213720710818,
        2238200.0],
       [u'A',
        u'2003-03-11',
        12.85,
        12.98,
        12.45,
        12.56,
        1553800.0,
        0.0,
        1.0,
        8.766792816195,
        8.8554841053861,
        8.4938965417609,
        8.5689430172303,
        1553800.0],
       [u'A',
        u'2003-03-12',
        12.56,
        12.56,
        12.11,
        12.41,
        2557300.0,
        0.0,
        1.0,
        8.5689430172303,
        8.5689430172303,
        8.2619347084919,
        8.4666069143175,
        2557300.0],
       [u'A',
        u'2003-03-13',
        12.85,
        13.03,
        12.49,
        13.03,
        1839800.0,
        0.0,
        1.0,
        8.766792816195,
        8.8895961396903,
        8.5211861692043,
        8.8895961396903,
        1839800.0],
       [u'A',
        u'2003-03-14',
        13.2,
        13.55,
        13.16,
        13.39,
        1687600.0,
        0.0,
        1.0,
        9.0055770563248,
        9.2443612964547,
        8.9782874288814,
        9.135202786681,
        1687600.0],
       [u'A',
        u'2003-03-17',
        13.39,
        14.14,
        13.01,
        14.06,
        1809800.0,
        0.0,
        1.0,
        9.135202786681,
        9.6468833012449,
        8.8759513259686,
        9.5923040463581,
        1809800.0],
       [u'A',
        u'2003-03-18',
        14.06,
        14.8,
        13.92,
        14.8,
        3120300.0,
        0.0,
        1.0,
        9.5923040463581,
        10.097162154061,
        9.4967903503062,
        10.097162154061,
        3120300.0],
       [u'A',
        u'2003-03-19',
        14.65,
        14.8,
        14.0,
        14.66,
        3151600.0,
        0.0,
        1.0,
        9.9948260511484,
        10.097162154061,
        9.551369605193,
        10.001648458009,
        3151600.0],
       [u'A',
        u'2003-03-20',
        14.45,
        15.0,
        14.15,
        14.83,
        2069600.0,
        0.0,
        1.0,
        9.8583779139314,
        10.233610291278,
        9.6537057081058,
        10.117629374644,
        2069600.0],
       [u'A',
        u'2003-03-21',
        15.0,
        15.0,
        14.5,
        14.8,
        1840400.0,
        0.0,
        1.0,
        10.233610291278,
        10.233610291278,
        9.8924899482356,
        10.097162154061,
        1840400.0],
       [u'A',
        u'2003-03-24',
        14.65,
        14.74,
        14.19,
        14.26,
        1476400.0,
        0.0,
        1.0,
        9.9948260511484,
        10.056227712896,
        9.6809953355492,
        9.7287521835752,
        1476400.0],
       [u'A',
        u'2003-03-25',
        14.22,
        14.27,
        13.98,
        14.2,
        2458600.0,
        0.0,
        1.0,
        9.7014625561318,
        9.735574590436,
        9.5377247914713,
        9.68781774241,
        2458600.0],
       [u'A',
        u'2003-03-26',
        14.12,
        14.17,
        13.9,
        14.04,
        1611800.0,
        0.0,
        1.0,
        9.6332384875232,
        9.6673505218275,
        9.4831455365845,
        9.5786592326364,
        1611800.0],
       [u'A',
        u'2003-03-27',
        14.0,
        14.26,
        13.81,
        14.14,
        1422800.0,
        0.0,
        1.0,
        9.551369605193,
        9.7287521835752,
        9.4217438748368,
        9.6468833012449,
        1422800.0],
       [u'A',
        u'2003-03-28',
        14.04,
        14.18,
        13.85,
        13.92,
        817100.0,
        0.0,
        1.0,
        9.5786592326364,
        9.6741729286883,
        9.4490335022802,
        9.4967903503062,
        817100.0],
       [u'A',
        u'2003-03-31',
        13.38,
        13.47,
        13.0,
        13.15,
        1846100.0,
        0.0,
        1.0,
        9.1283803798202,
        9.1897820415678,
        8.8691289191078,
        8.9714650220206,
        1846100.0],
       [u'A',
        u'2003-04-01',
        13.18,
        13.57,
        13.15,
        13.5,
        1166800.0,
        0.0,
        1.0,
        8.9919322426031,
        9.2580061101764,
        8.9714650220206,
        9.2102492621504,
        1166800.0],
       [u'A',
        u'2003-04-02',
        13.86,
        14.559,
        13.82,
        14.36,
        2447300.0,
        0.0,
        1.0,
        9.4558559091411,
        9.9327421487146,
        9.4285662816977,
        9.7969762521837,
        2447300.0],
       [u'A',
        u'2003-04-03',
        14.36,
        14.6,
        14.06,
        14.4,
        1430700.0,
        0.0,
        1.0,
        9.7969762521837,
        9.9607140168441,
        9.5923040463581,
        9.8242658796271,
        1430700.0],
       [u'A',
        u'2003-04-04',
        14.52,
        14.52,
        14.09,
        14.36,
        2223100.0,
        0.0,
        1.0,
        9.9061347619573,
        9.9061347619573,
        9.6127712669407,
        9.7969762521837,
        2223100.0],
       [u'A',
        u'2003-04-07',
        14.78,
        15.13,
        14.21,
        14.28,
        1717400.0,
        0.0,
        1.0,
        10.083517340339,
        10.322301580469,
        9.6946401492709,
        9.7423969972969,
        1717400.0],
       [u'A',
        u'2003-04-08',
        14.28,
        14.53,
        14.12,
        14.32,
        1307900.0,
        0.0,
        1.0,
        9.7423969972969,
        9.9129571688182,
        9.6332384875232,
        9.7696866247403,
        1307900.0],
       [u'A',
        u'2003-04-09',
        14.33,
        14.52,
        13.46,
        13.73,
        2408400.0,
        0.0,
        1.0,
        9.7765090316011,
        9.9061347619573,
        9.182959634707,
        9.36716461995,
        2408400.0],
       [u'A',
        u'2003-04-10',
        13.75,
        14.14,
        13.72,
        14.08,
        1639600.0,
        0.0,
        1.0,
        9.3808094336717,
        9.6468833012449,
        9.3603422130891,
        9.6059488600798,
        1639600.0],
       [u'A',
        u'2003-04-11',
        14.4,
        14.55,
        13.83,
        13.99,
        1448100.0,
        0.0,
        1.0,
        9.8242658796271,
        9.9266019825399,
        9.4353886885585,
        9.5445471983322,
        1448100.0],
       [u'A',
        u'2003-04-14',
        13.95,
        14.13,
        13.88,
        14.1,
        1430700.0,
        0.0,
        1.0,
        9.5172575708887,
        9.6400608943841,
        9.4695007228628,
        9.6195936738015,
        1430700.0],
       [u'A',
        u'2003-04-15',
        14.1,
        14.27,
        13.94,
        14.18,
        2161700.0,
        0.0,
        1.0,
        9.6195936738015,
        9.735574590436,
        9.5104351640279,
        9.6741729286883,
        2161700.0],
       [u'A',
        u'2003-04-16',
        14.45,
        14.9,
        14.38,
        14.6,
        1775200.0,
        0.0,
        1.0,
        9.8583779139314,
        10.16538622267,
        9.8106210659054,
        9.9607140168441,
        1775200.0],
       [u'A',
        u'2003-04-17',
        14.5,
        14.96,
        14.39,
        14.94,
        1107500.0,
        0.0,
        1.0,
        9.8924899482356,
        10.206320663835,
        9.8174434727662,
        10.192675850113,
        1107500.0],
       [u'A',
        u'2003-04-21',
        14.95,
        15.29,
        14.8,
        15.28,
        1658800.0,
        0.0,
        1.0,
        10.199498256974,
        10.431460090243,
        10.097162154061,
        10.424637683382,
        1658800.0],
       [u'A',
        u'2003-04-22',
        15.15,
        15.59,
        15.08,
        15.52,
        2155200.0,
        0.0,
        1.0,
        10.335946394191,
        10.636132296068,
        10.288189546165,
        10.588375448043,
        2155200.0],
       [u'A',
        u'2003-04-23',
        15.45,
        16.4,
        15.41,
        16.23,
        2217600.0,
        0.0,
        1.0,
        10.540618600017,
        11.188747251798,
        10.513328972573,
        11.072766335163,
        2217600.0],
       [u'A',
        u'2003-04-24',
        16.07,
        16.18,
        15.77,
        15.9,
        1772300.0,
        0.0,
        1.0,
        10.963607825389,
        11.038654300859,
        10.758935619564,
        10.847626908755,
        1772300.0],
       [u'A',
        u'2003-04-25',
        15.9,
        15.91,
        15.45,
        15.62,
        2783300.0,
        0.0,
        1.0,
        10.847626908755,
        10.854449315616,
        10.540618600017,
        10.656599516651,
        2783300.0],
       [u'A',
        u'2003-04-28',
        15.51,
        16.01,
        15.44,
        16.01,
        1506400.0,
        0.0,
        1.0,
        10.581553041182,
        10.922673384224,
        10.533796193156,
        10.922673384224,
        1506400.0],
       [u'A',
        u'2003-04-29',
        15.88,
        16.23,
        15.55,
        16.11,
        1760200.0,
        0.0,
        1.0,
        10.833982095033,
        11.072766335163,
        10.608842668625,
        10.990897452833,
        1760200.0],
       [u'A',
        u'2003-04-30',
        16.03,
        16.26,
        15.78,
        16.02,
        1799500.0,
        0.0,
        1.0,
        10.936318197946,
        11.093233555746,
        10.765758026425,
        10.929495791085,
        1799500.0],
       [u'A',
        u'2003-05-01',
        16.02,
        16.25,
        15.55,
        16.19,
        1440400.0,
        0.0,
        1.0,
        10.929495791085,
        11.086411148885,
        10.608842668625,
        11.04547670772,
        1440400.0],
       [u'A',
        u'2003-05-02',
        16.15,
        16.31,
        16.04,
        16.25,
        2323100.0,
        0.0,
        1.0,
        11.018187080276,
        11.12734559005,
        10.943140604807,
        11.086411148885,
        2323100.0],
       [u'A',
        u'2003-05-05',
        16.33,
        16.44,
        15.95,
        16.0,
        2787500.0,
        0.0,
        1.0,
        11.140990403772,
        11.216036879241,
        10.881738943059,
        10.915850977363,
        2787500.0],
       [u'A',
        u'2003-05-06',
        15.9,
        16.21,
        15.85,
        16.07,
        2125100.0,
        0.0,
        1.0,
        10.847626908755,
        11.059121521441,
        10.813514874451,
        10.963607825389,
        2125100.0],
       [u'A',
        u'2003-05-07',
        15.85,
        16.24,
        15.79,
        15.99,
        1944400.0,
        0.0,
        1.0,
        10.813514874451,
        11.079588742024,
        10.772580433286,
        10.909028570503,
        1944400.0],
       [u'A',
        u'2003-05-08',
        15.76,
        16.05,
        15.75,
        16.02,
        2793200.0,
        0.0,
        1.0,
        10.752113212703,
        10.949963011668,
        10.745290805842,
        10.929495791085,
        2793200.0],
       [u'A',
        u'2003-05-09',
        16.05,
        16.37,
        16.04,
        16.33,
        1443800.0,
        0.0,
        1.0,
        10.949963011668,
        11.168280031215,
        10.943140604807,
        11.140990403772,
        1443800.0],
       [u'A',
        u'2003-05-12',
        15.72,
        16.39,
        15.72,
        16.3,
        3329400.0,
        0.0,
        1.0,
        10.72482358526,
        11.181924844937,
        10.72482358526,
        11.120523183189,
        3329400.0],
       [u'A',
        u'2003-05-13',
        16.3,
        16.5,
        16.09,
        16.24,
        1270500.0,
        0.0,
        1.0,
        11.120523183189,
        11.256971320406,
        10.977252639111,
        11.079588742024,
        1270500.0],
       [u'A',
        u'2003-05-14',
        16.32,
        16.38,
        16.0,
        16.29,
        1606800.0,
        0.0,
        1.0,
        11.134167996911,
        11.175102438076,
        10.915850977363,
        11.113700776328,
        1606800.0],
       [u'A',
        u'2003-05-15',
        16.45,
        16.74,
        16.3,
        16.71,
        1851300.0,
        0.0,
        1.0,
        11.222859286102,
        11.420709085066,
        11.120523183189,
        11.400241864484,
        1851300.0],
       [u'A',
        u'2003-05-16',
        16.5,
        16.55,
        16.01,
        16.51,
        1912400.0,
        0.0,
        1.0,
        11.256971320406,
        11.29108335471,
        10.922673384224,
        11.263793727267,
        1912400.0],
       [u'A',
        u'2003-05-19',
        16.1,
        16.24,
        15.48,
        15.51,
        2748700.0,
        0.0,
        1.0,
        10.984075045972,
        11.079588742024,
        10.561085820599,
        10.581553041182,
        2748700.0],
       [u'A',
        u'2003-05-20',
        16.05,
        16.39,
        15.94,
        16.04,
        3873000.0,
        0.0,
        1.0,
        10.949963011668,
        11.181924844937,
        10.874916536198,
        10.943140604807,
        3873000.0],
       [u'A',
        u'2003-05-21',
        15.97,
        16.07,
        15.55,
        15.85,
        2142400.0,
        0.0,
        1.0,
        10.895383756781,
        10.963607825389,
        10.608842668625,
        10.813514874451,
        2142400.0],
       [u'A',
        u'2003-05-22',
        15.86,
        16.25,
        15.85,
        16.16,
        2189900.0,
        0.0,
        1.0,
        10.820337281312,
        11.086411148885,
        10.813514874451,
        11.025009487137,
        2189900.0],
       [u'A',
        u'2003-05-23',
        16.1,
        16.39,
        15.93,
        16.26,
        2417800.0,
        0.0,
        1.0,
        10.984075045972,
        11.181924844937,
        10.868094129337,
        11.093233555746,
        2417800.0],
       [u'A',
        u'2003-05-27',
        15.95,
        17.25,
        15.82,
        17.15,
        2796200.0,
        0.0,
        1.0,
        10.881738943059,
        11.76865183497,
        10.793047653868,
        11.700427766361,
        2796200.0],
       [u'A',
        u'2003-05-28',
        17.13,
        17.7,
        17.1,
        17.65,
        3149600.0,
        0.0,
        1.0,
        11.68678295264,
        12.075660143708,
        11.666315732057,
        12.041548109404,
        3149600.0],
       [u'A',
        u'2003-05-29',
        17.57,
        18.0,
        17.41,
        17.64,
        1960700.0,
        0.0,
        1.0,
        11.986968854517,
        12.280332349534,
        11.877810344744,
        12.034725702543,
        1960700.0],
       [u'A',
        u'2003-05-30',
        17.64,
        18.33,
        17.64,
        18.13,
        2480300.0,
        0.0,
        1.0,
        12.034725702543,
        12.505471775942,
        12.034725702543,
        12.369023638725,
        2480300.0],
       [u'A',
        u'2003-06-02',
        19.0,
        19.13,
        18.55,
        18.73,
        4507100.0,
        0.0,
        1.0,
        12.962573035619,
        13.05126432481,
        12.655564726881,
        12.778368050376,
        4507100.0],
       [u'A',
        u'2003-06-03',
        18.73,
        19.08,
        18.62,
        19.05,
        2891100.0,
        0.0,
        1.0,
        12.778368050376,
        13.017152290506,
        12.703321574907,
        12.996685069923,
        2891100.0],
       [u'A',
        u'2003-06-04',
        19.0,
        19.95,
        18.99,
        19.91,
        2056200.0,
        0.0,
        1.0,
        12.962573035619,
        13.6107016874,
        12.955750628758,
        13.583412059957,
        2056200.0],
       [u'A',
        u'2003-06-05',
        19.75,
        19.8,
        19.24,
        19.65,
        2961200.0,
        0.0,
        1.0,
        13.474253550183,
        13.508365584487,
        13.12631080028,
        13.406029481574,
        2961200.0],
       [u'A',
        u'2003-06-06',
        19.75,
        19.9,
        19.2,
        19.31,
        3144100.0,
        0.0,
        1.0,
        13.474253550183,
        13.576589653096,
        13.099021172836,
        13.174067648305,
        3144100.0],
       [u'A',
        u'2003-06-09',
        19.0,
        19.31,
        18.64,
        18.79,
        1858600.0,
        0.0,
        1.0,
        12.962573035619,
        13.174067648305,
        12.716966388628,
        12.819302491541,
        1858600.0],
       [u'A',
        u'2003-06-10',
        18.8,
        18.97,
        18.51,
        18.8,
        2320100.0,
        0.0,
        1.0,
        12.826124898402,
        12.942105815037,
        12.628275099437,
        12.826124898402,
        2320100.0],
       [u'A',
        u'2003-06-11',
        18.8,
        19.0,
        16.6,
        18.89,
        1862400.0,
        0.0,
        1.0,
        12.826124898402,
        12.962573035619,
        11.325195389015,
        12.88752656015,
        1862400.0],
       [u'A',
        u'2003-06-12',
        18.89,
        18.89,
        18.32,
        18.84,
        1098700.0,
        0.0,
        1.0,
        12.88752656015,
        12.88752656015,
        12.498649369081,
        12.853414525845,
        1098700.0],
       [u'A',
        u'2003-06-13',
        18.81,
        19.15,
        18.71,
        18.92,
        2455400.0,
        0.0,
        1.0,
        12.832947305263,
        13.064909138532,
        12.764723236654,
        12.907993780732,
        2455400.0],
       [u'A',
        u'2003-06-16',
        18.98,
        19.31,
        18.93,
        19.24,
        1927200.0,
        0.0,
        1.0,
        12.948928221897,
        13.174067648305,
        12.914816187593,
        13.12631080028,
        1927200.0],
       [u'A',
        u'2003-06-17',
        19.47,
        19.5,
        19.1,
        19.24,
        1431000.0,
        0.0,
        1.0,
        13.283226158079,
        13.303693378662,
        13.030797104228,
        13.12631080028,
        1431000.0],
       [u'A',
        u'2003-06-18',
        19.2,
        19.78,
        19.0,
        19.56,
        1346600.0,
        0.0,
        1.0,
        13.099021172836,
        13.494720770766,
        12.962573035619,
        13.344627819827,
        1346600.0],
       [u'A',
        u'2003-06-19',
        19.6,
        19.74,
        19.0,
        19.26,
        1781000.0,
        0.0,
        1.0,
        13.37191744727,
        13.467431143322,
        12.962573035619,
        13.139955614001,
        1781000.0],
       [u'A',
        u'2003-06-20',
        19.5,
        19.55,
        19.0,
        19.06,
        2249200.0,
        0.0,
        1.0,
        13.303693378662,
        13.337805412966,
        12.962573035619,
        13.003507476784,
        2249200.0],
       [u'A',
        u'2003-06-23',
        19.0,
        19.09,
        18.8,
        18.89,
        1522800.0,
        0.0,
        1.0,
        12.962573035619,
        13.023974697367,
        12.826124898402,
        12.88752656015,
        1522800.0],
       [u'A',
        u'2003-06-24',
        18.8,
        18.88,
        18.35,
        18.75,
        2033500.0,
        0.0,
        1.0,
        12.826124898402,
        12.880704153289,
        12.519116589664,
        12.792012864098,
        2033500.0],
       [u'A',
        u'2003-06-25',
        18.52,
        19.01,
        18.52,
        18.92,
        2315200.0,
        0.0,
        1.0,
        12.635097506298,
        12.96939544248,
        12.635097506298,
        12.907993780732,
        2315200.0],
       [u'A',
        u'2003-06-26',
        18.9,
        19.45,
        18.65,
        19.35,
        2414000.0,
        0.0,
        1.0,
        12.894348967011,
        13.269581344357,
        12.723788795489,
        13.201357275749,
        2414000.0],
       [u'A',
        u'2003-06-27',
        19.15,
        19.94,
        19.05,
        19.55,
        2504600.0,
        0.0,
        1.0,
        13.064909138532,
        13.603879280539,
        12.996685069923,
        13.337805412966,
        2504600.0],
       [u'A',
        u'2003-06-30',
        19.5,
        19.76,
        19.46,
        19.55,
        1691200.0,
        0.0,
        1.0,
        13.303693378662,
        13.481075957044,
        13.276403751218,
        13.337805412966,
        1691200.0],
       [u'A',
        u'2003-07-01',
        19.46,
        19.91,
        19.3,
        19.91,
        3151500.0,
        0.0,
        1.0,
        13.276403751218,
        13.583412059957,
        13.167245241445,
        13.583412059957,
        3151500.0],
       [u'A',
        u'2003-07-02',
        19.95,
        20.34,
        19.76,
        20.3,
        3892000.0,
        0.0,
        1.0,
        13.6107016874,
        13.876775554973,
        13.481075957044,
        13.84948592753,
        3892000.0],
       [u'A',
        u'2003-07-03',
        20.18,
        20.19,
        19.82,
        19.99,
        1802100.0,
        0.0,
        1.0,
        13.7676170452,
        13.77443945206,
        13.522010398209,
        13.637991314843,
        1802100.0],
       [u'A',
        u'2003-07-07',
        20.14,
        21.29,
        20.14,
        21.29,
        4271200.0,
        0.0,
        1.0,
        13.740327417756,
        14.524904206754,
        13.740327417756,
        14.524904206754,
        4271200.0],
       [u'A',
        u'2003-07-08',
        21.29,
        21.71,
        20.87,
        21.68,
        2095700.0,
        0.0,
        1.0,
        14.524904206754,
        14.81144529491,
        14.238363118598,
        14.790978074327,
        2095700.0],
       [u'A',
        u'2003-07-09',
        21.66,
        21.95,
        21.01,
        21.77,
        2351100.0,
        0.0,
        1.0,
        14.777333260606,
        14.97518305957,
        14.33387681465,
        14.852379736075,
        2351100.0],
       [u'A',
        u'2003-07-10',
        21.38,
        21.38,
        20.76,
        21.06,
        1810400.0,
        0.0,
        1.0,
        14.586305868502,
        14.586305868502,
        14.163316643129,
        14.367988848955,
        1810400.0],
       [u'A',
        u'2003-07-11',
        21.15,
        21.76,
        21.02,
        21.7,
        2226200.0,
        0.0,
        1.0,
        14.429390510702,
        14.845557329214,
        14.340699221511,
        14.804622888049,
        2226200.0],
       [u'A',
        u'2003-07-14',
        21.95,
        22.4,
        21.92,
        22.15,
        3555800.0,
        0.0,
        1.0,
        14.97518305957,
        15.282191368309,
        14.954715838988,
        15.111631196788,
        3555800.0],
       [u'A',
        u'2003-07-15',
        22.3,
        22.64,
        22.01,
        22.23,
        3841800.0,
        0.0,
        1.0,
        15.2139672997,
        15.445929132969,
        15.016117500736,
        15.166210451674,
        3841800.0],
       [u'A',
        u'2003-07-16',
        22.28,
        22.36,
        21.42,
        21.94,
        3313100.0,
        0.0,
        1.0,
        15.200322485979,
        15.254901740865,
        14.613595495945,
        14.96836065271,
        3313100.0],
       [u'A',
        u'2003-07-17',
        21.7,
        21.81,
        20.78,
        21.1,
        3835500.0,
        0.0,
        1.0,
        14.804622888049,
        14.879669363519,
        14.176961456851,
        14.395278476398,
        3835500.0],
       [u'A',
        u'2003-07-18',
        21.2,
        21.42,
        20.89,
        21.24,
        1465800.0,
        0.0,
        1.0,
        14.463502545007,
        14.613595495945,
        14.25200793232,
        14.49079217245,
        1465800.0],
       [u'A',
        u'2003-07-21',
        21.0,
        21.46,
        20.42,
        20.51,
        2658500.0,
        0.0,
        1.0,
        14.32705440779,
        14.640885123389,
        13.93135480986,
        13.992756471608,
        2658500.0],
       [u'A',
        u'2003-07-22',
        20.8,
        21.5,
        20.8,
        21.48,
        2246900.0,
        0.0,
        1.0,
        14.190606270572,
        14.668174750832,
        14.190606270572,
        14.65452993711,
        2246900.0],
       [u'A',
        u'2003-07-23',
        21.53,
        21.68,
        20.95,
        21.65,
        1672000.0,
        0.0,
        1.0,
        14.688641971415,
        14.790978074327,
        14.292942373485,
        14.770510853745,
        1672000.0],
       [u'A',
        u'2003-07-24',
        21.71,
        22.27,
        21.51,
        21.62,
        2358700.0,
        0.0,
        1.0,
        14.81144529491,
        15.193500079118,
        14.674997157693,
        14.750043633162,
        2358700.0],
       [u'A',
        u'2003-07-25',
        21.65,
        21.8,
        21.3,
        21.73,
        1446900.0,
        0.0,
        1.0,
        14.770510853745,
        14.872846956658,
        14.531726613615,
        14.825090108632,
        1446900.0],
       [u'A',
        u'2003-07-28',
        21.65,
        22.15,
        21.52,
        21.97,
        1429000.0,
        0.0,
        1.0,
        14.770510853745,
        15.111631196788,
        14.681819564554,
        14.988827873292,
        1429000.0],
       [u'A',
        u'2003-07-29',
        21.99,
        22.09,
        21.66,
        21.94,
        2009700.0,
        0.0,
        1.0,
        15.002472687014,
        15.070696755622,
        14.777333260606,
        14.96836065271,
        2009700.0],
       [u'A',
        u'2003-07-30',
        21.94,
        21.98,
        21.46,
        21.55,
        1598000.0,
        0.0,
        1.0,
        14.96836065271,
        14.995650280153,
        14.640885123389,
        14.702286785136,
        1598000.0],
       [u'A',
        u'2003-07-31',
        21.7,
        22.11,
        21.5,
        21.73,
        1559600.0,
        0.0,
        1.0,
        14.804622888049,
        15.084341569344,
        14.668174750832,
        14.825090108632,
        1559600.0],
       [u'A',
        u'2003-08-01',
        21.73,
        21.85,
        21.32,
        21.55,
        1374600.0,
        0.0,
        1.0,
        14.825090108632,
        14.906958990962,
        14.545371427337,
        14.702286785136,
        1374600.0],
       [u'A',
        u'2003-08-04',
        21.52,
        21.81,
        21.12,
        21.56,
        1180100.0,
        0.0,
        1.0,
        14.681819564554,
        14.879669363519,
        14.40892329012,
        14.709109191997,
        1180100.0],
       [u'A',
        u'2003-08-05',
        21.46,
        21.7,
        20.8,
        20.83,
        2021100.0,
        0.0,
        1.0,
        14.640885123389,
        14.804622888049,
        14.190606270572,
        14.211073491155,
        2021100.0],
       [u'A',
        u'2003-08-06',
        20.76,
        20.9,
        20.32,
        20.58,
        1408300.0,
        0.0,
        1.0,
        14.163316643129,
        14.258830339181,
        13.863130741252,
        14.040513319634,
        1408300.0],
       [u'A',
        u'2003-08-07',
        20.48,
        20.78,
        20.31,
        20.67,
        1149200.0,
        0.0,
        1.0,
        13.972289251025,
        14.176961456851,
        13.856308334391,
        14.101914981381,
        1149200.0],
       [u'A',
        u'2003-08-08',
        20.73,
        21.02,
        20.52,
        20.69,
        1015700.0,
        0.0,
        1.0,
        14.142849422547,
        14.340699221511,
        13.999578878469,
        14.115559795103,
        1015700.0],
       [u'A',
        u'2003-08-11',
        20.79,
        21.08,
        20.69,
        21.02,
        989900.0,
        0.0,
        1.0,
        14.183783863712,
        14.381633662676,
        14.115559795103,
        14.340699221511,
        989900.0],
       [u'A',
        u'2003-08-12',
        21.05,
        21.29,
        20.85,
        21.25,
        1085600.0,
        0.0,
        1.0,
        14.361166442094,
        14.524904206754,
        14.224718304877,
        14.497614579311,
        1085600.0],
       [u'A',
        u'2003-08-13',
        21.3,
        21.63,
        21.1,
        21.49,
        1232200.0,
        0.0,
        1.0,
        14.531726613615,
        14.756866040023,
        14.395278476398,
        14.661352343971,
        1232200.0],
       [u'A',
        u'2003-08-14',
        21.45,
        21.79,
        21.15,
        21.76,
        1246400.0,
        0.0,
        1.0,
        14.634062716528,
        14.866024549797,
        14.429390510702,
        14.845557329214,
        1246400.0],
       [u'A',
        u'2003-08-15',
        21.66,
        21.87,
        21.54,
        21.78,
        481200.0,
        0.0,
        1.0,
        14.777333260606,
        14.920603804684,
        14.695464378276,
        14.859202142936,
        481200.0],
       [u'A',
        u'2003-08-18',
        21.78,
        22.52,
        21.76,
        22.46,
        1913500.0,
        0.0,
        1.0,
        14.859202142936,
        15.364060250639,
        14.845557329214,
        15.323125809474,
        1913500.0],
       [u'A',
        u'2003-08-19',
        23.26,
        24.38,
        23.16,
        24.29,
        6866600.0,
        0.0,
        1.0,
        15.868918358342,
        16.633027926758,
        15.800694289734,
        16.57162626501,
        6866600.0],
       [u'A',
        u'2003-08-20',
        23.92,
        24.53,
        23.84,
        24.38,
        3147600.0,
        0.0,
        1.0,
        16.319197211158,
        16.73536402967,
        16.264617956272,
        16.633027926758,
        3147600.0],
       [u'A',
        u'2003-08-21',
        24.43,
        25.28,
        24.42,
        24.89,
        1855800.0,
        0.0,
        1.0,
        16.667139961062,
        17.247044544234,
        16.660317554201,
        16.980970676661,
        1855800.0],
       [u'A',
        u'2003-08-22',
        25.17,
        25.3,
        24.23,
        24.31,
        2946000.0,
        0.0,
        1.0,
        17.171998068765,
        17.260689357956,
        16.530691823845,
        16.585271078732,
        2946000.0],
       [u'A',
        u'2003-08-25',
        24.18,
        24.38,
        23.98,
        24.11,
        1327900.0,
        0.0,
        1.0,
        16.49657978954,
        16.633027926758,
        16.360131652323,
        16.448822941515,
        1327900.0],
       [u'A',
        u'2003-08-26',
        23.87,
        24.05,
        23.58,
        24.0,
        2301800.0,
        0.0,
        1.0,
        16.285085176854,
        16.407888500349,
        16.087235377889,
        16.373776466045,
        2301800.0],
       [u'A',
        u'2003-08-27',
        23.95,
        24.72,
        23.87,
        24.5,
        3229700.0,
        0.0,
        1.0,
        16.339664431741,
        16.864989760027,
        16.285085176854,
        16.714896809088,
        3229700.0],
       [u'A',
        u'2003-08-28',
        24.49,
        24.57,
        24.15,
        24.29,
        2331600.0,
        0.0,
        1.0,
        16.708074402227,
        16.762653657114,
        16.476112568958,
        16.57162626501,
        2331600.0],
       [u'A',
        u'2003-08-29',
        24.15,
        24.34,
        24.08,
        24.32,
        1902800.0,
        0.0,
        1.0,
        16.476112568958,
        16.605738299314,
        16.428355720932,
        16.592093485592,
        1902800.0],
       [u'A',
        u'2003-09-02',
        24.4,
        24.74,
        24.201,
        24.67,
        3536900.0,
        0.0,
        1.0,
        16.646672740479,
        16.878634573748,
        16.510906843948,
        16.830877725722,
        3536900.0],
       [u'A',
        u'2003-09-03',
        24.6,
        24.7,
        24.3,
        24.5,
        3728100.0,
        0.0,
        1.0,
        16.783120877696,
        16.851344946305,
        16.578448671871,
        16.714896809088,
        3728100.0],
       [u'A',
        u'2003-09-04',
        24.5,
        25.19,
        24.5,
        25.15,
        3061600.0,
        0.0,
        1.0,
        16.714896809088,
        17.185642882487,
        16.714896809088,
        17.158353255043,
        3061600.0],
       [u'A',
        u'2003-09-05',
        25.15,
        25.62,
        24.84,
        25.5,
        4030300.0,
        0.0,
        1.0,
        17.158353255043,
        17.479006377503,
        16.946858642357,
        17.397137495173,
        4030300.0],
       [u'A',
        u'2003-09-08',
        25.43,
        26.48,
        25.43,
        26.43,
        3397400.0,
        0.0,
        1.0,
        17.349380647147,
        18.065733367536,
        17.349380647147,
        18.031621333232,
        3397400.0],
       [u'A',
        u'2003-09-09',
        26.3,
        26.43,
        25.7,
        25.88,
        2428300.0,
        0.0,
        1.0,
        17.942930044041,
        18.031621333232,
        17.53358563239,
        17.656388955885,
        2428300.0],
       [u'A',
        u'2003-09-10',
        25.4,
        25.58,
        24.41,
        24.49,
        2869700.0,
        0.0,
        1.0,
        17.328913426564,
        17.45171675006,
        16.65349514734,
        16.708074402227,
        2869700.0],
       [u'A',
        u'2003-09-11',
        24.57,
        25.18,
        24.45,
        25.04,
        2079000.0,
        0.0,
        1.0,
        16.762653657114,
        17.178820475626,
        16.680784774784,
        17.083306779574,
        2079000.0],
       [u'A',
        u'2003-09-12',
        25.04,
        25.114,
        24.55,
        24.97,
        2017700.0,
        0.0,
        1.0,
        17.083306779574,
        17.133792590344,
        16.749008843392,
        17.035549931548,
        2017700.0],
       [u'A',
        u'2003-09-15',
        24.8,
        25.0,
        24.42,
        24.5,
        1335700.0,
        0.0,
        1.0,
        16.919569014913,
        17.05601715213,
        16.660317554201,
        16.714896809088,
        1335700.0],
       [u'A',
        u'2003-09-16',
        24.32,
        24.84,
        24.25,
        24.67,
        2927200.0,
        0.0,
        1.0,
        16.592093485592,
        16.946858642357,
        16.544336637566,
        16.830877725722,
        2927200.0],
       [u'A',
        u'2003-09-17',
        24.7,
        24.75,
        24.25,
        24.6,
        2357600.0,
        0.0,
        1.0,
        16.851344946305,
        16.885456980609,
        16.544336637566,
        16.783120877696,
        2357600.0],
       [u'A',
        u'2003-09-18',
        24.35,
        24.73,
        24.2,
        24.56,
        2012200.0,
        0.0,
        1.0,
        16.612560706175,
        16.871812166887,
        16.510224603262,
        16.755831250253,
        2012200.0],
       [u'A',
        u'2003-09-19',
        24.6,
        25.09,
        24.55,
        25.04,
        3367600.0,
        0.0,
        1.0,
        16.783120877696,
        17.117418813878,
        16.749008843392,
        17.083306779574,
        3367600.0],
       [u'A',
        u'2003-09-22',
        24.55,
        24.68,
        24.2,
        24.43,
        1654100.0,
        0.0,
        1.0,
        16.749008843392,
        16.837700132583,
        16.510224603262,
        16.667139961062,
        1654100.0],
       [u'A',
        u'2003-09-23',
        24.31,
        24.689,
        24.31,
        24.65,
        1306100.0,
        0.0,
        1.0,
        16.585271078732,
        16.843840298758,
        16.585271078732,
        16.817232912001,
        1306100.0],
       [u'A',
        u'2003-09-24',
        24.65,
        24.65,
        23.07,
        23.07,
        3432100.0,
        0.0,
        1.0,
        16.817232912001,
        16.817232912001,
        15.739292627986,
        15.739292627986,
        3432100.0],
       [u'A',
        u'2003-09-25',
        23.17,
        23.82,
        22.77,
        22.82,
        2290400.0,
        0.0,
        1.0,
        15.807516696594,
        16.25097314255,
        15.53462042216,
        15.568732456465,
        2290400.0],
       [u'A',
        u'2003-09-26',
        22.7,
        22.94,
        22.31,
        22.38,
        1572500.0,
        0.0,
        1.0,
        15.486863574134,
        15.650601338795,
        15.220789706561,
        15.268546554587,
        1572500.0],
       [u'A',
        u'2003-09-29',
        22.46,
        22.9,
        22.2,
        22.66,
        1407300.0,
        0.0,
        1.0,
        15.323125809474,
        15.623311711351,
        15.145743231092,
        15.459573946691,
        1407300.0],
       [u'A',
        u'2003-09-30',
        22.52,
        22.52,
        22.1,
        22.11,
        1465400.0,
        0.0,
        1.0,
        15.364060250639,
        15.364060250639,
        15.077519162483,
        15.084341569344,
        1465400.0],
       [u'A',
        u'2003-10-01',
        22.15,
        22.52,
        22.04,
        22.25,
        2385800.0,
        0.0,
        1.0,
        15.111631196788,
        15.364060250639,
        15.036584721318,
        15.179855265396,
        2385800.0],
       [u'A',
        u'2003-10-02',
        22.1,
        22.18,
        21.84,
        21.99,
        2410700.0,
        0.0,
        1.0,
        15.077519162483,
        15.13209841737,
        14.900136584101,
        15.002472687014,
        2410700.0],
       [u'A',
        u'2003-10-03',
        23.1,
        23.47,
        22.22,
        23.0,
        3772400.0,
        0.0,
        1.0,
        15.759759848568,
        16.01218890242,
        15.159388044813,
        15.69153577996,
        3772400.0],
       [u'A',
        u'2003-10-06',
        23.0,
        23.23,
        22.81,
        23.03,
        977600.0,
        0.0,
        1.0,
        15.69153577996,
        15.84845113776,
        15.561910049604,
        15.712003000542,
        977600.0],
       [u'A',
        u'2003-10-07',
        22.9,
        23.56,
        22.7,
        23.43,
        1940500.0,
        0.0,
        1.0,
        15.623311711351,
        16.073590564168,
        15.486863574134,
        15.984899274977,
        1940500.0],
       [u'A',
        u'2003-10-08',
        23.68,
        23.75,
        23.22,
        23.41,
        1645900.0,
        0.0,
        1.0,
        16.155459446498,
        16.203216294524,
        15.841628730899,
        15.971254461255,
        1645900.0],
       [u'A',
        u'2003-10-09',
        23.41,
        23.96,
        23.41,
        23.63,
        1504800.0,
        0.0,
        1.0,
        15.971254461255,
        16.346486838602,
        15.971254461255,
        16.121347412194,
        1504800.0],
       [u'A',
        u'2003-10-10',
        23.54,
        23.79,
        23.48,
        23.7,
        894800.0,
        0.0,
        1.0,
        16.059945750446,
        16.230505921967,
        16.019011309281,
        16.16910426022,
        894800.0],
       [u'A',
        u'2003-10-13',
        23.8,
        23.98,
        23.7,
        23.88,
        963500.0,
        0.0,
        1.0,
        16.237328328828,
        16.360131652323,
        16.16910426022,
        16.291907583715,
        963500.0],
       [u'A',
        u'2003-10-14',
        23.8,
        24.15,
        23.72,
        24.07,
        1592400.0,
        0.0,
        1.0,
        16.237328328828,
        16.476112568958,
        16.182749073941,
        16.421533314071,
        1592400.0],
       [u'A',
        u'2003-10-15',
        24.37,
        24.5,
        24.04,
        24.24,
        2216000.0,
        0.0,
        1.0,
        16.626205519897,
        16.714896809088,
        16.401066093489,
        16.537514230706,
        2216000.0],
       [u'A',
        u'2003-10-16',
        24.2,
        24.39,
        24.02,
        24.32,
        1662800.0,
        0.0,
        1.0,
        16.510224603262,
        16.639850333618,
        16.387421279767,
        16.592093485592,
        1662800.0],
       [u'A',
        u'2003-10-17',
        24.29,
        24.29,
        23.84,
        23.98,
        1812900.0,
        0.0,
        1.0,
        16.57162626501,
        16.57162626501,
        16.264617956272,
        16.360131652323,
        1812900.0],
       [u'A',
        u'2003-10-20',
        23.9,
        23.99,
        23.65,
        23.83,
        926400.0,
        0.0,
        1.0,
        16.305552397437,
        16.366954059184,
        16.134992225915,
        16.257795549411,
        926400.0],
       [u'A',
        u'2003-10-21',
        23.77,
        24.22,
        23.7,
        24.02,
        1531900.0,
        0.0,
        1.0,
        16.216861108246,
        16.523869416984,
        16.16910426022,
        16.387421279767,
        1531900.0],
       [u'A',
        u'2003-10-22',
        23.8,
        23.84,
        23.3,
        23.48,
        1055100.0,
        0.0,
        1.0,
        16.237328328828,
        16.264617956272,
        15.896207985786,
        16.019011309281,
        1055100.0],
       [u'A',
        u'2003-10-23',
        23.48,
        23.48,
        22.65,
        22.97,
        1671900.0,
        0.0,
        1.0,
        16.019011309281,
        16.019011309281,
        15.45275153983,
        15.671068559377,
        1671900.0],
       [u'A',
        u'2003-10-24',
        22.97,
        23.09,
        22.65,
        23.07,
        1235600.0,
        0.0,
        1.0,
        15.671068559377,
        15.752937441708,
        15.45275153983,
        15.739292627986,
        1235600.0],
       [u'A',
        u'2003-10-27',
        23.12,
        23.15,
        22.72,
        22.87,
        1087900.0,
        0.0,
        1.0,
        15.77340466229,
        15.793871882873,
        15.500508387856,
        15.602844490769,
        1087900.0],
       [u'A',
        u'2003-10-28',
        23.0,
        24.0,
        22.98,
        24.0,
        2032400.0,
        0.0,
        1.0,
        15.69153577996,
        16.373776466045,
        15.677890966238,
        16.373776466045,
        2032400.0],
       [u'A',
        u'2003-10-29',
        23.99,
        24.19,
        23.79,
        24.09,
        1791900.0,
        0.0,
        1.0,
        16.366954059184,
        16.503402196401,
        16.230505921967,
        16.435178127793,
        1791900.0],
       [u'A',
        u'2003-10-30',
        24.25,
        25.31,
        24.19,
        24.81,
        4712800.0,
        0.0,
        1.0,
        16.544336637566,
        17.267511764817,
        16.503402196401,
        16.926391421774,
        4712800.0],
       [u'A',
        u'2003-10-31',
        24.95,
        25.02,
        24.64,
        24.92,
        1933900.0,
        0.0,
        1.0,
        17.021905117826,
        17.069661965852,
        16.81041050514,
        17.001437897244,
        1933900.0],
       [u'A',
        u'2003-11-03',
        24.99,
        25.4,
        24.97,
        25.29,
        2266300.0,
        0.0,
        1.0,
        17.04919474527,
        17.328913426564,
        17.035549931548,
        17.253866951095,
        2266300.0],
       [u'A',
        u'2003-11-04',
        25.29,
        25.55,
        25.15,
        25.4,
        2495000.0,
        0.0,
        1.0,
        17.253866951095,
        17.431249529477,
        17.158353255043,
        17.328913426564,
        2495000.0],
       [u'A',
        u'2003-11-05',
        25.25,
        25.65,
        25.15,
        25.6,
        1496800.0,
        0.0,
        1.0,
        17.226577323652,
        17.499473598086,
        17.158353255043,
        17.465361563781,
        1496800.0],
       [u'A',
        u'2003-11-06',
        25.6,
        26.27,
        25.6,
        26.27,
        2585400.0,
        0.0,
        1.0,
        17.465361563781,
        17.922462823459,
        17.465361563781,
        17.922462823459,
        2585400.0],
       [u'A',
        u'2003-11-07',
        26.27,
        27.2,
        26.04,
        26.82,
        3289400.0,
        0.0,
        1.0,
        17.922462823459,
        18.556946661518,
        17.765547465659,
        18.297695200805,
        3289400.0],
       [u'A',
        u'2003-11-10',
        26.7,
        26.79,
        25.76,
        25.87,
        2051600.0,
        0.0,
        1.0,
        18.215826318475,
        18.277227980223,
        17.574520073555,
        17.649566549025,
        2051600.0],
       [u'A',
        u'2003-11-11',
        25.7,
        26.2,
        25.5,
        25.97,
        1864700.0,
        0.0,
        1.0,
        17.53358563239,
        17.874705975433,
        17.397137495173,
        17.717790617633,
        1864700.0],
       ...]},
     u'meta': {u'next_cursor_id': u'djFfMTAwMDFfMTUxNzcxMzYyNw=='}}




```python
ticker_data=ticker['datatable']
ticker_data.keys()
```




    [u'data', u'columns']




```python
#See keys

ticker.keys()
```




    [u'meta', u'datatable']




```python
#FROM HERE ON
#################################################################################################################################
#FOLLOW A) OR B)
```


```python
#################################################################################################################################
```


```python
#3.1.A) OBTAIN A DATAFRAME OF CLOSING PRICES OF EACH TICKER FROM THE LAST MONTH

#Select last  month prices

ticker_col=ticker_data['columns']
ticker1=ticker_data['data'][4557:4578]
ticker2=ticker_data['data'][4872:4893]
ticker3=ticker_data['data'][7981:8002]
ticker4=ticker_data['data'][9274:9292]

import pandas
df1=pandas.DataFrame.from_dict(ticker1, orient='columns')
df1.drop(df1.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df1.columns = ['Ticker', 'Date', 'Price']
df2=pandas.DataFrame.from_dict(ticker2, orient='columns')
df2.drop(df2.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df2.columns = ['Ticker', 'Date', 'Price']
df3=pandas.DataFrame.from_dict(ticker3, orient='columns')
df3.drop(df3.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df3.columns = ['Ticker', 'Date', 'Price']
df4=pandas.DataFrame.from_dict(ticker4, orient='columns')
df4.drop(df4.columns[[2,3,4,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
df4.columns = ['Ticker', 'Date', 'Price']
dfs = [df1, df2, df3, df4]
dfs = pd.concat(dfs)
```


```python
out=dfs.pivot(index= 'Date', columns='Ticker', values='Price')
out
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Ticker</th>
      <th>A</th>
      <th>AA</th>
      <th>AAL</th>
      <th>AAMC</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-01-02</th>
      <td>67.60</td>
      <td>55.17</td>
      <td>52.990</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-03</th>
      <td>69.32</td>
      <td>54.50</td>
      <td>52.330</td>
      <td>77.9500</td>
    </tr>
    <tr>
      <th>2018-01-04</th>
      <td>68.80</td>
      <td>54.70</td>
      <td>52.670</td>
      <td>80.2000</td>
    </tr>
    <tr>
      <th>2018-01-05</th>
      <td>69.90</td>
      <td>54.09</td>
      <td>52.650</td>
      <td>80.2000</td>
    </tr>
    <tr>
      <th>2018-01-08</th>
      <td>70.05</td>
      <td>55.00</td>
      <td>52.130</td>
      <td>80.2000</td>
    </tr>
    <tr>
      <th>2018-01-09</th>
      <td>71.77</td>
      <td>54.20</td>
      <td>52.080</td>
      <td>79.0000</td>
    </tr>
    <tr>
      <th>2018-01-10</th>
      <td>70.79</td>
      <td>56.17</td>
      <td>53.780</td>
      <td>79.0000</td>
    </tr>
    <tr>
      <th>2018-01-11</th>
      <td>70.80</td>
      <td>56.91</td>
      <td>56.420</td>
      <td>79.9900</td>
    </tr>
    <tr>
      <th>2018-01-12</th>
      <td>71.73</td>
      <td>56.76</td>
      <td>58.470</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-16</th>
      <td>71.23</td>
      <td>56.24</td>
      <td>57.985</td>
      <td>75.9500</td>
    </tr>
    <tr>
      <th>2018-01-17</th>
      <td>72.06</td>
      <td>56.99</td>
      <td>58.160</td>
      <td>71.5010</td>
    </tr>
    <tr>
      <th>2018-01-18</th>
      <td>72.19</td>
      <td>53.00</td>
      <td>58.340</td>
      <td>71.5010</td>
    </tr>
    <tr>
      <th>2018-01-19</th>
      <td>73.07</td>
      <td>53.10</td>
      <td>58.060</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-22</th>
      <td>73.48</td>
      <td>52.94</td>
      <td>58.100</td>
      <td>66.1803</td>
    </tr>
    <tr>
      <th>2018-01-23</th>
      <td>73.44</td>
      <td>52.49</td>
      <td>58.290</td>
      <td>67.7000</td>
    </tr>
    <tr>
      <th>2018-01-24</th>
      <td>73.58</td>
      <td>53.30</td>
      <td>54.790</td>
      <td>69.6647</td>
    </tr>
    <tr>
      <th>2018-01-25</th>
      <td>73.86</td>
      <td>53.11</td>
      <td>53.050</td>
      <td>69.6647</td>
    </tr>
    <tr>
      <th>2018-01-26</th>
      <td>74.82</td>
      <td>54.00</td>
      <td>53.070</td>
      <td>68.1500</td>
    </tr>
    <tr>
      <th>2018-01-29</th>
      <td>74.53</td>
      <td>54.49</td>
      <td>52.680</td>
      <td>68.1500</td>
    </tr>
    <tr>
      <th>2018-01-30</th>
      <td>72.99</td>
      <td>52.52</td>
      <td>52.590</td>
      <td>69.0241</td>
    </tr>
    <tr>
      <th>2018-01-31</th>
      <td>73.43</td>
      <td>52.02</td>
      <td>54.320</td>
      <td>69.0241</td>
    </tr>
  </tbody>
</table>
</div>




```python
out.plot.box(figsize=(8, 5))
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fb65cb301d0>




![png](MILESTONE/images/output_66_1.png)



```python
#Bar plots of Date per Ticker prices

out.plot.bar(colormap='Greens',stacked=True, figsize=(11, 7),legend='top_right')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fb65c6eaf10>




![png](MILESTONE/images/output_67_1.png)



```python
names = [('Price', 'Stock Input')]
ds = hv.Dataset(dfs, ['Date', 'Ticker'], names)
```


```python
%%opts Curve [width=800 height=550] {+framewise}
ds.to(hv.Curve, 'Date','Price')
```




<div class="hololayout row row-fluid">
  <div class="holoframe" id="display_area570f422d49154300b007f5029aae3354">
    <div id="_anim_img570f422d49154300b007f5029aae3354">

      <div style='display: table; margin: 0 auto;'>

<div class="bk-root">
    <div class="bk-plotdiv" id="5b2ff9e6-44ed-4ab1-bfae-d56856935b00"></div>
</div>
<script type="text/javascript">
  (function(root) {
  function embed_document(root) {

  var docs_json = {"bd3813df-9c45-4cfd-8338-2b163a98e238":{"roots":{"references":[{"attributes":{"plot":null,"text":"Ticker: A","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"619258c5-1ea8-4e22-9e2f-ae962427e80a","type":"Title"},{"attributes":{"axis_label":"Stock Input","bounds":"auto","formatter":{"id":"65e971dc-2a3a-413b-bf05-f50e9c9dbb99","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"72107dbe-54e8-4f86-aa29-13748f33f86c","subtype":"Figure","type":"Plot"},"ticker":{"id":"640bc0c1-5348-4dc9-bab3-7cd6f28352f6","type":"BasicTicker"}},"id":"5670939d-c005-4ee5-b92b-cc9273f179f2","type":"LinearAxis"},{"attributes":{},"id":"51c0df7d-e746-4a9e-b973-19ee8a90cdd4","type":"LinearScale"},{"attributes":{"line_alpha":0.1,"line_color":"#30a2da","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"ba8e62e4-b246-4f29-9438-37f3e224e534","type":"Line"},{"attributes":{},"id":"640bc0c1-5348-4dc9-bab3-7cd6f28352f6","type":"BasicTicker"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"87e4ca3a-641c-4c02-abb0-3fcd61bbd1c3","type":"CategoricalAxis"}],"left":[{"id":"5670939d-c005-4ee5-b92b-cc9273f179f2","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":550,"plot_width":800,"renderers":[{"id":"87e4ca3a-641c-4c02-abb0-3fcd61bbd1c3","type":"CategoricalAxis"},{"id":"148f86be-7fd3-4015-a264-02afb9e86399","type":"Grid"},{"id":"5670939d-c005-4ee5-b92b-cc9273f179f2","type":"LinearAxis"},{"id":"5634623b-626f-44c6-bd70-b8dcfd353661","type":"Grid"},{"id":"d845eb9a-41a8-43b3-8fdd-9e5df9e96ed4","type":"BoxAnnotation"},{"id":"de203bb2-283b-4ee8-b12b-ad9b0ccdd07e","type":"GlyphRenderer"}],"title":{"id":"619258c5-1ea8-4e22-9e2f-ae962427e80a","type":"Title"},"toolbar":{"id":"7dc4b009-0d89-4085-9c8f-f6e8821f1946","type":"Toolbar"},"x_range":{"id":"ade6d5ea-8a97-4aaf-ae6e-d7f66c0cf05f","type":"FactorRange"},"x_scale":{"id":"51ed41ad-154b-4d82-9f19-6ee426ed3a15","type":"CategoricalScale"},"y_range":{"id":"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb","type":"Range1d"},"y_scale":{"id":"51c0df7d-e746-4a9e-b973-19ee8a90cdd4","type":"LinearScale"}},"id":"72107dbe-54e8-4f86-aa29-13748f33f86c","subtype":"Figure","type":"Plot"},{"attributes":{"overlay":{"id":"d845eb9a-41a8-43b3-8fdd-9e5df9e96ed4","type":"BoxAnnotation"}},"id":"3e5c1df0-1f6c-4a96-958a-4e2866779ab4","type":"BoxZoomTool"},{"attributes":{},"id":"65e971dc-2a3a-413b-bf05-f50e9c9dbb99","type":"BasicTickFormatter"},{"attributes":{"callback":null,"end":74.82,"start":67.6},"id":"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb","type":"Range1d"},{"attributes":{},"id":"28736c83-8c19-402f-9e44-907832afa583","type":"SaveTool"},{"attributes":{},"id":"7d59f26e-463c-4df6-8aba-81b716d63077","type":"CategoricalTickFormatter"},{"attributes":{},"id":"ac725027-996a-4627-b5ec-a7e2252cf51d","type":"PanTool"},{"attributes":{"axis_label":"Date","bounds":"auto","formatter":{"id":"7d59f26e-463c-4df6-8aba-81b716d63077","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"72107dbe-54e8-4f86-aa29-13748f33f86c","subtype":"Figure","type":"Plot"},"ticker":{"id":"6ac6020a-cbe9-4ed7-ab4e-ef82e23b57a1","type":"CategoricalTicker"}},"id":"87e4ca3a-641c-4c02-abb0-3fcd61bbd1c3","type":"CategoricalAxis"},{"attributes":{},"id":"51ed41ad-154b-4d82-9f19-6ee426ed3a15","type":"CategoricalScale"},{"attributes":{},"id":"ce5fe665-0599-4562-8b5d-a5f679e2685a","type":"WheelZoomTool"},{"attributes":{"data_source":{"id":"574c9214-f116-48de-870f-2fec93b5c748","type":"ColumnDataSource"},"glyph":{"id":"3a47cc18-208e-4f9f-8e7c-7fbe10240011","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"4fb4d923-b096-4509-b443-293693132393","type":"Line"},"nonselection_glyph":{"id":"ba8e62e4-b246-4f29-9438-37f3e224e534","type":"Line"},"selection_glyph":null,"view":{"id":"dff49bc8-a625-4693-8c90-b7cc082f9673","type":"CDSView"}},"id":"de203bb2-283b-4ee8-b12b-ad9b0ccdd07e","type":"GlyphRenderer"},{"attributes":{},"id":"b0d23a9a-e763-4087-9884-765813edb86e","type":"ResetTool"},{"attributes":{"line_color":"#30a2da","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"3a47cc18-208e-4f9f-8e7c-7fbe10240011","type":"Line"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"d845eb9a-41a8-43b3-8fdd-9e5df9e96ed4","type":"BoxAnnotation"},{"attributes":{"line_alpha":0.2,"line_color":"#30a2da","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"4fb4d923-b096-4509-b443-293693132393","type":"Line"},{"attributes":{},"id":"6ac6020a-cbe9-4ed7-ab4e-ef82e23b57a1","type":"CategoricalTicker"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"72107dbe-54e8-4f86-aa29-13748f33f86c","subtype":"Figure","type":"Plot"},"ticker":{"id":"640bc0c1-5348-4dc9-bab3-7cd6f28352f6","type":"BasicTicker"}},"id":"5634623b-626f-44c6-bd70-b8dcfd353661","type":"Grid"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"ZmZmZmbmUEAUrkfhelRRQDMzMzMzM1FAmpmZmZl5UUAzMzMzM4NRQOF6FK5H8VFAw/UoXI+yUUAzMzMzM7NRQB+F61G47lFAH4XrUbjOUUCkcD0K1wNSQFyPwvUoDFJAFK5H4XpEUkAfhetRuF5SQFyPwvUoXFJAhetRuB5lUkDXo3A9CndSQBSuR+F6tFJAUrgeheuhUkCPwvUoXD9SQOxRuB6FW1JA","dtype":"float64","shape":[21]}}},"id":"574c9214-f116-48de-870f-2fec93b5c748","type":"ColumnDataSource"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"28736c83-8c19-402f-9e44-907832afa583","type":"SaveTool"},{"id":"ac725027-996a-4627-b5ec-a7e2252cf51d","type":"PanTool"},{"id":"ce5fe665-0599-4562-8b5d-a5f679e2685a","type":"WheelZoomTool"},{"id":"3e5c1df0-1f6c-4a96-958a-4e2866779ab4","type":"BoxZoomTool"},{"id":"b0d23a9a-e763-4087-9884-765813edb86e","type":"ResetTool"}]},"id":"7dc4b009-0d89-4085-9c8f-f6e8821f1946","type":"Toolbar"},{"attributes":{"source":{"id":"574c9214-f116-48de-870f-2fec93b5c748","type":"ColumnDataSource"}},"id":"dff49bc8-a625-4693-8c90-b7cc082f9673","type":"CDSView"},{"attributes":{"callback":null,"factors":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"]},"id":"ade6d5ea-8a97-4aaf-ae6e-d7f66c0cf05f","type":"FactorRange"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"72107dbe-54e8-4f86-aa29-13748f33f86c","subtype":"Figure","type":"Plot"},"ticker":{"id":"6ac6020a-cbe9-4ed7-ab4e-ef82e23b57a1","type":"CategoricalTicker"}},"id":"148f86be-7fd3-4015-a264-02afb9e86399","type":"Grid"}],"root_ids":["72107dbe-54e8-4f86-aa29-13748f33f86c"]},"title":"Bokeh Application","version":"0.12.13"}};
  var render_items = [{"docid":"bd3813df-9c45-4cfd-8338-2b163a98e238","elementid":"5b2ff9e6-44ed-4ab1-bfae-d56856935b00","modelid":"72107dbe-54e8-4f86-aa29-13748f33f86c"}];
  root.Bokeh.embed.embed_items_notebook(docs_json, render_items);

  }
  if (root.Bokeh !== undefined) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (root.Bokeh !== undefined) {
        embed_document(root);
        clearInterval(timer);
      }
      attempts++;
      if (attempts > 100) {
        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing")
        clearInterval(timer);
      }
    }, 10, root)
  }
})(window);
</script>
</div>

    </div>
  </div>
  <div class="holowidgets" id="widget_area570f422d49154300b007f5029aae3354">
    <form class="holoform well" id="form570f422d49154300b007f5029aae3354">


        <div class="form-group control-group holoformgroup" style=''>
          <label for="textInput570f422d49154300b007f5029aae3354_Ticker"><strong>Ticker:</strong></label>
          <select class="holoselect form-control" id="_anim_widget570f422d49154300b007f5029aae3354_Ticker" >
          </select>
        </div>
        <script>
        function init_dropdown() {
        var widget = $("#_anim_widget570f422d49154300b007f5029aae3354_Ticker");
        var vals = ['A', 'AA', 'AAL', 'AAMC'];
        var labels = ['A', 'AA', 'AAL', 'AAMC'];
        widget.data('values', vals)
        for (var i=0; i<vals.length; i++){
			if (false) {
		       var val = vals[i];
			} else {
			   var val = i;
			}
            widget.append($("<option>", {
                value: val,
                text: labels[i]
            }));
        };
        widget.data("next_vals", {});
        widget.on('change', function(event, ui) {
		    if (false) {
                var dim_val = parseInt(this.value);
			} else {
			    var dim_val = $.data(this, 'values')[this.value];
			}
            var next_vals = $.data(this, "next_vals");
            if (Object.keys(next_vals).length > 0) {
                var new_vals = next_vals[dim_val];
                var next_widget = $('#_anim_widget570f422d49154300b007f5029aae3354_');
                update_widget(next_widget, new_vals);
            }
			if (anim570f422d49154300b007f5029aae3354) {
                anim570f422d49154300b007f5029aae3354.set_frame(dim_val, 0);
            }

        });
        }
        $(document).ready(init_dropdown)
        </script>


        </form>
    </div>
</div>


<script language="javascript">
/* Instantiate the BokehSelectionWidget class. */
/* The IDs given should match those used in the template above. */
(function() {
	if (jQuery.ui !== undefined) {
		$("#display_area570f422d49154300b007f5029aae3354").resizable({
			resize: function(event, ui) {
				$("#widget_area570f422d49154300b007f5029aae3354").width($(this).parent().width()-ui.size.width);
			}
		});
		$("#widget_area570f422d49154300b007f5029aae3354").resizable();
	}
    var widget_ids = new Array(1);

    widget_ids[0] = "_anim_widget570f422d49154300b007f5029aae3354_Ticker";

    var frame_data = {"0": "{\"content\":{\"events\":[{\"attr\":\"factors\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"ade6d5ea-8a97-4aaf-ae6e-d7f66c0cf05f\",\"type\":\"FactorRange\"},\"new\":[\"2018-01-02\",\"2018-01-03\",\"2018-01-04\",\"2018-01-05\",\"2018-01-08\",\"2018-01-09\",\"2018-01-10\",\"2018-01-11\",\"2018-01-12\",\"2018-01-16\",\"2018-01-17\",\"2018-01-18\",\"2018-01-19\",\"2018-01-22\",\"2018-01-23\",\"2018-01-24\",\"2018-01-25\",\"2018-01-26\",\"2018-01-29\",\"2018-01-30\",\"2018-01-31\"]},{\"attr\":\"start\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":67.6},{\"attr\":\"end\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":74.82},{\"attr\":\"text\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"619258c5-1ea8-4e22-9e2f-ae962427e80a\",\"type\":\"Title\"},\"new\":\"Ticker: A\"},{\"cols\":[\"Date\",\"Price\"],\"column_source\":{\"id\":\"574c9214-f116-48de-870f-2fec93b5c748\",\"type\":\"ColumnDataSource\"},\"kind\":\"ColumnDataChanged\",\"new\":{\"Date\":[\"2018-01-02\",\"2018-01-03\",\"2018-01-04\",\"2018-01-05\",\"2018-01-08\",\"2018-01-09\",\"2018-01-10\",\"2018-01-11\",\"2018-01-12\",\"2018-01-16\",\"2018-01-17\",\"2018-01-18\",\"2018-01-19\",\"2018-01-22\",\"2018-01-23\",\"2018-01-24\",\"2018-01-25\",\"2018-01-26\",\"2018-01-29\",\"2018-01-30\",\"2018-01-31\"],\"Price\":{\"__ndarray__\":\"ZmZmZmbmUEAUrkfhelRRQDMzMzMzM1FAmpmZmZl5UUAzMzMzM4NRQOF6FK5H8VFAw/UoXI+yUUAzMzMzM7NRQB+F61G47lFAH4XrUbjOUUCkcD0K1wNSQFyPwvUoDFJAFK5H4XpEUkAfhetRuF5SQFyPwvUoXFJAhetRuB5lUkDXo3A9CndSQBSuR+F6tFJAUrgeheuhUkCPwvUoXD9SQOxRuB6FW1JA\",\"dtype\":\"float64\",\"shape\":[21]}}},{\"cols\":[\"Date\",\"Price\"],\"column_source\":{\"id\":\"574c9214-f116-48de-870f-2fec93b5c748\",\"type\":\"ColumnDataSource\"},\"kind\":\"ColumnDataChanged\",\"new\":{\"Date\":[\"2018-01-02\",\"2018-01-03\",\"2018-01-04\",\"2018-01-05\",\"2018-01-08\",\"2018-01-09\",\"2018-01-10\",\"2018-01-11\",\"2018-01-12\",\"2018-01-16\",\"2018-01-17\",\"2018-01-18\",\"2018-01-19\",\"2018-01-22\",\"2018-01-23\",\"2018-01-24\",\"2018-01-25\",\"2018-01-26\",\"2018-01-29\",\"2018-01-30\",\"2018-01-31\"],\"Price\":{\"__ndarray__\":\"ZmZmZmbmUEAUrkfhelRRQDMzMzMzM1FAmpmZmZl5UUAzMzMzM4NRQOF6FK5H8VFAw/UoXI+yUUAzMzMzM7NRQB+F61G47lFAH4XrUbjOUUCkcD0K1wNSQFyPwvUoDFJAFK5H4XpEUkAfhetRuF5SQFyPwvUoXFJAhetRuB5lUkDXo3A9CndSQBSuR+F6tFJAUrgeheuhUkCPwvUoXD9SQOxRuB6FW1JA\",\"dtype\":\"float64\",\"shape\":[21]}}}],\"references\":[]},\"root\":\"72107dbe-54e8-4f86-aa29-13748f33f86c\"}", "1": "{\"content\":{\"events\":[{\"attr\":\"start\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":52.02},{\"attr\":\"end\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":56.99},{\"attr\":\"text\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"619258c5-1ea8-4e22-9e2f-ae962427e80a\",\"type\":\"Title\"},\"new\":\"Ticker: AA\"},{\"cols\":[\"Date\",\"Price\"],\"column_source\":{\"id\":\"574c9214-f116-48de-870f-2fec93b5c748\",\"type\":\"ColumnDataSource\"},\"kind\":\"ColumnDataChanged\",\"new\":{\"Date\":[\"2018-01-02\",\"2018-01-03\",\"2018-01-04\",\"2018-01-05\",\"2018-01-08\",\"2018-01-09\",\"2018-01-10\",\"2018-01-11\",\"2018-01-12\",\"2018-01-16\",\"2018-01-17\",\"2018-01-18\",\"2018-01-19\",\"2018-01-22\",\"2018-01-23\",\"2018-01-24\",\"2018-01-25\",\"2018-01-26\",\"2018-01-29\",\"2018-01-30\",\"2018-01-31\"],\"Price\":{\"__ndarray__\":\"9ihcj8KVS0AAAAAAAEBLQJqZmZmZWUtA7FG4HoULS0AAAAAAAIBLQJqZmZmZGUtA9ihcj8IVTEAUrkfhenRMQOF6FK5HYUxAH4XrUbgeTEAfhetRuH5MQAAAAAAAgEpAzczMzMyMSkC4HoXrUXhKQB+F61G4PkpAZmZmZmamSkCuR+F6FI5KQAAAAAAAAEtAH4XrUbg+S0DD9Shcj0JKQMP1KFyPAkpA\",\"dtype\":\"float64\",\"shape\":[21]}}}],\"references\":[]},\"root\":\"72107dbe-54e8-4f86-aa29-13748f33f86c\"}", "2": "{\"content\":{\"events\":[{\"attr\":\"start\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":52.08},{\"attr\":\"end\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":58.47},{\"attr\":\"text\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"619258c5-1ea8-4e22-9e2f-ae962427e80a\",\"type\":\"Title\"},\"new\":\"Ticker: AAL\"},{\"cols\":[\"Date\",\"Price\"],\"column_source\":{\"id\":\"574c9214-f116-48de-870f-2fec93b5c748\",\"type\":\"ColumnDataSource\"},\"kind\":\"ColumnDataChanged\",\"new\":{\"Date\":[\"2018-01-02\",\"2018-01-03\",\"2018-01-04\",\"2018-01-05\",\"2018-01-08\",\"2018-01-09\",\"2018-01-10\",\"2018-01-11\",\"2018-01-12\",\"2018-01-16\",\"2018-01-17\",\"2018-01-18\",\"2018-01-19\",\"2018-01-22\",\"2018-01-23\",\"2018-01-24\",\"2018-01-25\",\"2018-01-26\",\"2018-01-29\",\"2018-01-30\",\"2018-01-31\"],\"Price\":{\"__ndarray__\":\"H4XrUbh+SkAK16NwPSpKQPYoXI/CVUpAMzMzMzNTSkBxPQrXoxBKQArXo3A9CkpApHA9CtfjSkD2KFyPwjVMQFyPwvUoPE1ArkfhehT+TEAUrkfhehRNQOxRuB6FK01ASOF6FK4HTUDNzMzMzAxNQIXrUbgeJU1AhetRuB5lS0BmZmZmZoZKQClcj8L1iEpA16NwPQpXSkDsUbgehUtKQClcj8L1KEtA\",\"dtype\":\"float64\",\"shape\":[21]}}}],\"references\":[]},\"root\":\"72107dbe-54e8-4f86-aa29-13748f33f86c\"}", "3": "{\"content\":{\"events\":[{\"attr\":\"factors\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"ade6d5ea-8a97-4aaf-ae6e-d7f66c0cf05f\",\"type\":\"FactorRange\"},\"new\":[\"2018-01-03\",\"2018-01-04\",\"2018-01-05\",\"2018-01-08\",\"2018-01-09\",\"2018-01-10\",\"2018-01-11\",\"2018-01-16\",\"2018-01-17\",\"2018-01-18\",\"2018-01-22\",\"2018-01-23\",\"2018-01-24\",\"2018-01-25\",\"2018-01-26\",\"2018-01-29\",\"2018-01-30\",\"2018-01-31\"]},{\"attr\":\"start\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":66.1803},{\"attr\":\"end\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"fcdd1685-4b1e-42d3-9e33-6fb4aeb9ecfb\",\"type\":\"Range1d\"},\"new\":80.2},{\"attr\":\"text\",\"kind\":\"ModelChanged\",\"model\":{\"id\":\"619258c5-1ea8-4e22-9e2f-ae962427e80a\",\"type\":\"Title\"},\"new\":\"Ticker: AAMC\"},{\"cols\":[\"Date\",\"Price\"],\"column_source\":{\"id\":\"574c9214-f116-48de-870f-2fec93b5c748\",\"type\":\"ColumnDataSource\"},\"kind\":\"ColumnDataChanged\",\"new\":{\"Date\":[\"2018-01-03\",\"2018-01-04\",\"2018-01-05\",\"2018-01-08\",\"2018-01-09\",\"2018-01-10\",\"2018-01-11\",\"2018-01-16\",\"2018-01-17\",\"2018-01-18\",\"2018-01-22\",\"2018-01-23\",\"2018-01-24\",\"2018-01-25\",\"2018-01-26\",\"2018-01-29\",\"2018-01-30\",\"2018-01-31\"],\"Price\":{\"__ndarray__\":\"zczMzMx8U0DNzMzMzAxUQM3MzMzMDFRAzczMzMwMVEAAAAAAAMBTQAAAAAAAwFNAj8L1KFz/U0DNzMzMzPxSQPLSTWIQ4FFA8tJNYhDgUUAB3gIJiotQQM3MzMzM7FBArWnecYpqUUCtad5ximpRQJqZmZmZCVFAmpmZmZkJUUBa9bnaikFRQFr1udqKQVFA\",\"dtype\":\"float64\",\"shape\":[18]}}}],\"references\":[]},\"root\":\"72107dbe-54e8-4f86-aa29-13748f33f86c\"}"};
    var dim_vals = ['A'];
    var keyMap = {"('A',)": 0, "('AA',)": 1, "('AAL',)": 2, "('AAMC',)": 3};
    var notFound = "<h2 style='vertical-align: middle>No frame at selected dimension value.<h2>";
    function create_widget() {
        setTimeout(function() {
            anim570f422d49154300b007f5029aae3354 = new BokehSelectionWidget(frame_data, "570f422d49154300b007f5029aae3354", widget_ids,
				keyMap, dim_vals, notFound, false, "default",
				true, "./json_figures/", false);
        }, 0);
    }

    create_widget();

})();
</script>




```python
%%opts Bars [width=900 height=400 tools=['hover'] group_index=1 legend_position='top_right']
Tickers = ['A', 'AA', 'AAL', 'AAMC']
ds.select(Ticker=Tickers).to(hv.Bars, ['Date','Ticker'], 'Price').sort()
```




<div style='display: table; margin: 0 auto;'>

<div class="bk-root">
    <div class="bk-plotdiv" id="1cdfbc47-2364-47e1-8d6d-20de98f7fd6f"></div>
</div>
<script type="text/javascript">
  (function(root) {
  function embed_document(root) {

  var docs_json = {"12748b16-8336-4f3d-9203-2aabc902151d":{"roots":{"references":[{"attributes":{"callback":null,"column_names":["xoffsets","Date","Price","Ticker"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31","2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31","2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-16","2018-01-17","2018-01-18","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"ZmZmZmbmUEAUrkfhelRRQDMzMzMzM1FAmpmZmZl5UUAzMzMzM4NRQOF6FK5H8VFAw/UoXI+yUUAzMzMzM7NRQB+F61G47lFAH4XrUbjOUUCkcD0K1wNSQFyPwvUoDFJAFK5H4XpEUkAfhetRuF5SQFyPwvUoXFJAhetRuB5lUkDXo3A9CndSQBSuR+F6tFJAUrgeheuhUkCPwvUoXD9SQOxRuB6FW1JA9ihcj8KVS0AAAAAAAEBLQJqZmZmZWUtA7FG4HoULS0AAAAAAAIBLQJqZmZmZGUtA9ihcj8IVTEAUrkfhenRMQOF6FK5HYUxAH4XrUbgeTEAfhetRuH5MQAAAAAAAgEpAzczMzMyMSkC4HoXrUXhKQB+F61G4PkpAZmZmZmamSkCuR+F6FI5KQAAAAAAAAEtAH4XrUbg+S0DD9Shcj0JKQMP1KFyPAkpAH4XrUbh+SkAK16NwPSpKQPYoXI/CVUpAMzMzMzNTSkBxPQrXoxBKQArXo3A9CkpApHA9CtfjSkD2KFyPwjVMQFyPwvUoPE1ArkfhehT+TEAUrkfhehRNQOxRuB6FK01ASOF6FK4HTUDNzMzMzAxNQIXrUbgeJU1AhetRuB5lS0BmZmZmZoZKQClcj8L1iEpA16NwPQpXSkDsUbgehUtKQClcj8L1KEtAzczMzMx8U0DNzMzMzAxUQM3MzMzMDFRAzczMzMwMVEAAAAAAAMBTQAAAAAAAwFNAj8L1KFz/U0DNzMzMzPxSQPLSTWIQ4FFA8tJNYhDgUUAB3gIJiotQQM3MzMzM7FBArWnecYpqUUCtad5ximpRQJqZmZmZCVFAmpmZmZkJUUBa9bnaikFRQFr1udqKQVFA","dtype":"float64","shape":[81]},"Ticker":["A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","A","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AA","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAL","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC","AAMC"],"xoffsets":[["2018-01-02","A"],["2018-01-03","A"],["2018-01-04","A"],["2018-01-05","A"],["2018-01-08","A"],["2018-01-09","A"],["2018-01-10","A"],["2018-01-11","A"],["2018-01-12","A"],["2018-01-16","A"],["2018-01-17","A"],["2018-01-18","A"],["2018-01-19","A"],["2018-01-22","A"],["2018-01-23","A"],["2018-01-24","A"],["2018-01-25","A"],["2018-01-26","A"],["2018-01-29","A"],["2018-01-30","A"],["2018-01-31","A"],["2018-01-02","AA"],["2018-01-03","AA"],["2018-01-04","AA"],["2018-01-05","AA"],["2018-01-08","AA"],["2018-01-09","AA"],["2018-01-10","AA"],["2018-01-11","AA"],["2018-01-12","AA"],["2018-01-16","AA"],["2018-01-17","AA"],["2018-01-18","AA"],["2018-01-19","AA"],["2018-01-22","AA"],["2018-01-23","AA"],["2018-01-24","AA"],["2018-01-25","AA"],["2018-01-26","AA"],["2018-01-29","AA"],["2018-01-30","AA"],["2018-01-31","AA"],["2018-01-02","AAL"],["2018-01-03","AAL"],["2018-01-04","AAL"],["2018-01-05","AAL"],["2018-01-08","AAL"],["2018-01-09","AAL"],["2018-01-10","AAL"],["2018-01-11","AAL"],["2018-01-12","AAL"],["2018-01-16","AAL"],["2018-01-17","AAL"],["2018-01-18","AAL"],["2018-01-19","AAL"],["2018-01-22","AAL"],["2018-01-23","AAL"],["2018-01-24","AAL"],["2018-01-25","AAL"],["2018-01-26","AAL"],["2018-01-29","AAL"],["2018-01-30","AAL"],["2018-01-31","AAL"],["2018-01-03","AAMC"],["2018-01-04","AAMC"],["2018-01-05","AAMC"],["2018-01-08","AAMC"],["2018-01-09","AAMC"],["2018-01-10","AAMC"],["2018-01-11","AAMC"],["2018-01-16","AAMC"],["2018-01-17","AAMC"],["2018-01-18","AAMC"],["2018-01-22","AAMC"],["2018-01-23","AAMC"],["2018-01-24","AAMC"],["2018-01-25","AAMC"],["2018-01-26","AAMC"],["2018-01-29","AAMC"],["2018-01-30","AAMC"],["2018-01-31","AAMC"]]}},"id":"64a5bbee-12eb-4ea2-b5c7-2bef8f56f9d4","type":"ColumnDataSource"},{"attributes":{},"id":"cb3ca427-ebdd-4975-a476-39cb384be1e0","type":"CategoricalTicker"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"de728a47-5ac5-4e11-9f3f-13403631492d","subtype":"Figure","type":"Plot"},"ticker":{"id":"cb3ca427-ebdd-4975-a476-39cb384be1e0","type":"CategoricalTicker"}},"id":"38cdd446-216a-4a4c-8a8d-a29ea0d113e6","type":"Grid"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"7f2a4dac-79fc-4670-82a8-32b65f953a47","type":"BoxAnnotation"},{"attributes":{"items":[{"id":"155bccb0-092d-4f4f-ac39-477b4bbc7155","type":"LegendItem"}],"plot":{"id":"de728a47-5ac5-4e11-9f3f-13403631492d","subtype":"Figure","type":"Plot"}},"id":"d8a3732b-23ba-4e80-bd0d-8feedbda5cae","type":"Legend"},{"attributes":{"fill_alpha":{"value":0.1},"fill_color":{"field":"Ticker","transform":{"id":"4f632779-7474-4ce1-b679-83c3b4cca0d3","type":"CategoricalColorMapper"}},"line_alpha":{"value":0.1},"line_color":{"value":"#000000"},"top":{"field":"Price"},"width":{"value":0.8},"x":{"field":"xoffsets"}},"id":"236620d5-a8d5-494c-a352-340fa6af5537","type":"VBar"},{"attributes":{},"id":"922c2ccd-e170-4c8b-8e2b-5ab4ece1a699","type":"CategoricalScale"},{"attributes":{"overlay":{"id":"7f2a4dac-79fc-4670-82a8-32b65f953a47","type":"BoxAnnotation"}},"id":"55d9e495-dd88-4715-9b1c-a698ba3f07ae","type":"BoxZoomTool"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"de728a47-5ac5-4e11-9f3f-13403631492d","subtype":"Figure","type":"Plot"},"ticker":{"id":"2a67facf-4380-4a69-8cff-1cdc771c501e","type":"BasicTicker"}},"id":"ac87e49f-152f-4392-af17-dd0ff86675ab","type":"Grid"},{"attributes":{},"id":"2a67facf-4380-4a69-8cff-1cdc771c501e","type":"BasicTicker"},{"attributes":{"data_source":{"id":"64a5bbee-12eb-4ea2-b5c7-2bef8f56f9d4","type":"ColumnDataSource"},"glyph":{"id":"9421db44-b663-4c7d-8a82-e76e24e0c1c1","type":"VBar"},"hover_glyph":null,"muted_glyph":null,"nonselection_glyph":{"id":"236620d5-a8d5-494c-a352-340fa6af5537","type":"VBar"},"selection_glyph":null,"view":{"id":"77e25566-5517-4d12-b8a3-0f3532d82ec9","type":"CDSView"}},"id":"95eaa799-cfbb-4998-be5e-8bd01da78ae0","type":"GlyphRenderer"},{"attributes":{"factors":["A","AA","AAL","AAMC"],"palette":["#30a2da","#fc4f30","#e5ae38","#6d904f"]},"id":"4f632779-7474-4ce1-b679-83c3b4cca0d3","type":"CategoricalColorMapper"},{"attributes":{"source":{"id":"64a5bbee-12eb-4ea2-b5c7-2bef8f56f9d4","type":"ColumnDataSource"}},"id":"77e25566-5517-4d12-b8a3-0f3532d82ec9","type":"CDSView"},{"attributes":{},"id":"3356d8fd-11dd-4c3b-be8f-911bb864c447","type":"PanTool"},{"attributes":{"callback":null,"factors":[["2018-01-02","A"],["2018-01-02","AA"],["2018-01-02","AAL"],["2018-01-02","AAMC"],["2018-01-03","A"],["2018-01-03","AA"],["2018-01-03","AAL"],["2018-01-03","AAMC"],["2018-01-04","A"],["2018-01-04","AA"],["2018-01-04","AAL"],["2018-01-04","AAMC"],["2018-01-05","A"],["2018-01-05","AA"],["2018-01-05","AAL"],["2018-01-05","AAMC"],["2018-01-08","A"],["2018-01-08","AA"],["2018-01-08","AAL"],["2018-01-08","AAMC"],["2018-01-09","A"],["2018-01-09","AA"],["2018-01-09","AAL"],["2018-01-09","AAMC"],["2018-01-10","A"],["2018-01-10","AA"],["2018-01-10","AAL"],["2018-01-10","AAMC"],["2018-01-11","A"],["2018-01-11","AA"],["2018-01-11","AAL"],["2018-01-11","AAMC"],["2018-01-12","A"],["2018-01-12","AA"],["2018-01-12","AAL"],["2018-01-12","AAMC"],["2018-01-16","A"],["2018-01-16","AA"],["2018-01-16","AAL"],["2018-01-16","AAMC"],["2018-01-17","A"],["2018-01-17","AA"],["2018-01-17","AAL"],["2018-01-17","AAMC"],["2018-01-18","A"],["2018-01-18","AA"],["2018-01-18","AAL"],["2018-01-18","AAMC"],["2018-01-19","A"],["2018-01-19","AA"],["2018-01-19","AAL"],["2018-01-19","AAMC"],["2018-01-22","A"],["2018-01-22","AA"],["2018-01-22","AAL"],["2018-01-22","AAMC"],["2018-01-23","A"],["2018-01-23","AA"],["2018-01-23","AAL"],["2018-01-23","AAMC"],["2018-01-24","A"],["2018-01-24","AA"],["2018-01-24","AAL"],["2018-01-24","AAMC"],["2018-01-25","A"],["2018-01-25","AA"],["2018-01-25","AAL"],["2018-01-25","AAMC"],["2018-01-26","A"],["2018-01-26","AA"],["2018-01-26","AAL"],["2018-01-26","AAMC"],["2018-01-29","A"],["2018-01-29","AA"],["2018-01-29","AAL"],["2018-01-29","AAMC"],["2018-01-30","A"],["2018-01-30","AA"],["2018-01-30","AAL"],["2018-01-30","AAMC"],["2018-01-31","A"],["2018-01-31","AA"],["2018-01-31","AAL"],["2018-01-31","AAMC"]]},"id":"9b3d4d35-fa34-41d1-aae3-d4cd1f0afeac","type":"FactorRange"},{"attributes":{},"id":"13950666-0f2a-4588-abe8-a942b44c729f","type":"ResetTool"},{"attributes":{},"id":"e2e779b9-6b8c-406e-8c52-b99b05342234","type":"BasicTickFormatter"},{"attributes":{},"id":"e2455892-1b34-4be6-a941-0103889250f6","type":"WheelZoomTool"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"76520f73-d33b-4230-bf26-c587a25d6d71","type":"HoverTool"},{"id":"81416728-37d6-44e3-bd8d-d35d1528b900","type":"SaveTool"},{"id":"3356d8fd-11dd-4c3b-be8f-911bb864c447","type":"PanTool"},{"id":"e2455892-1b34-4be6-a941-0103889250f6","type":"WheelZoomTool"},{"id":"55d9e495-dd88-4715-9b1c-a698ba3f07ae","type":"BoxZoomTool"},{"id":"13950666-0f2a-4588-abe8-a942b44c729f","type":"ResetTool"}]},"id":"1fd9007b-fc8e-41a1-8328-229343a72e09","type":"Toolbar"},{"attributes":{"fill_color":{"field":"Ticker","transform":{"id":"4f632779-7474-4ce1-b679-83c3b4cca0d3","type":"CategoricalColorMapper"}},"line_color":{"value":"#000000"},"top":{"field":"Price"},"width":{"value":0.8},"x":{"field":"xoffsets"}},"id":"9421db44-b663-4c7d-8a82-e76e24e0c1c1","type":"VBar"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"82d3a428-6580-4400-bfc2-c287aa45d972","type":"Title"},{"attributes":{"callback":null,"end":80.2},"id":"72323dbe-6f0f-4e9c-be29-a8a17bcab2af","type":"Range1d"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"7c24ad0d-6de2-4790-b41d-be583dde4dd5","type":"CategoricalAxis"}],"left":[{"id":"9a650ab5-4242-45e4-aedc-0ed9aa8cd558","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":400,"plot_width":900,"renderers":[{"id":"7c24ad0d-6de2-4790-b41d-be583dde4dd5","type":"CategoricalAxis"},{"id":"38cdd446-216a-4a4c-8a8d-a29ea0d113e6","type":"Grid"},{"id":"9a650ab5-4242-45e4-aedc-0ed9aa8cd558","type":"LinearAxis"},{"id":"ac87e49f-152f-4392-af17-dd0ff86675ab","type":"Grid"},{"id":"7f2a4dac-79fc-4670-82a8-32b65f953a47","type":"BoxAnnotation"},{"id":"d8a3732b-23ba-4e80-bd0d-8feedbda5cae","type":"Legend"},{"id":"95eaa799-cfbb-4998-be5e-8bd01da78ae0","type":"GlyphRenderer"}],"title":{"id":"82d3a428-6580-4400-bfc2-c287aa45d972","type":"Title"},"toolbar":{"id":"1fd9007b-fc8e-41a1-8328-229343a72e09","type":"Toolbar"},"x_range":{"id":"9b3d4d35-fa34-41d1-aae3-d4cd1f0afeac","type":"FactorRange"},"x_scale":{"id":"922c2ccd-e170-4c8b-8e2b-5ab4ece1a699","type":"CategoricalScale"},"y_range":{"id":"72323dbe-6f0f-4e9c-be29-a8a17bcab2af","type":"Range1d"},"y_scale":{"id":"0db42ae4-d85a-479d-9177-01f97c4b0499","type":"LinearScale"}},"id":"de728a47-5ac5-4e11-9f3f-13403631492d","subtype":"Figure","type":"Plot"},{"attributes":{"axis_label":"Date, Ticker","bounds":"auto","formatter":{"id":"6a832956-9889-4d1a-a90a-7773228d736a","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"de728a47-5ac5-4e11-9f3f-13403631492d","subtype":"Figure","type":"Plot"},"ticker":{"id":"cb3ca427-ebdd-4975-a476-39cb384be1e0","type":"CategoricalTicker"}},"id":"7c24ad0d-6de2-4790-b41d-be583dde4dd5","type":"CategoricalAxis"},{"attributes":{},"id":"81416728-37d6-44e3-bd8d-d35d1528b900","type":"SaveTool"},{"attributes":{},"id":"0db42ae4-d85a-479d-9177-01f97c4b0499","type":"LinearScale"},{"attributes":{},"id":"6a832956-9889-4d1a-a90a-7773228d736a","type":"CategoricalTickFormatter"},{"attributes":{"label":{"field":"Ticker"},"renderers":[{"id":"95eaa799-cfbb-4998-be5e-8bd01da78ae0","type":"GlyphRenderer"}]},"id":"155bccb0-092d-4f4f-ac39-477b4bbc7155","type":"LegendItem"},{"attributes":{"callback":null,"renderers":[{"id":"95eaa799-cfbb-4998-be5e-8bd01da78ae0","type":"GlyphRenderer"}],"tooltips":[["Date","@{Date}"],["Ticker","@{Ticker}"],["Stock Input","@{Price}"]]},"id":"76520f73-d33b-4230-bf26-c587a25d6d71","type":"HoverTool"},{"attributes":{"axis_label":"Stock Input","bounds":"auto","formatter":{"id":"e2e779b9-6b8c-406e-8c52-b99b05342234","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"de728a47-5ac5-4e11-9f3f-13403631492d","subtype":"Figure","type":"Plot"},"ticker":{"id":"2a67facf-4380-4a69-8cff-1cdc771c501e","type":"BasicTicker"}},"id":"9a650ab5-4242-45e4-aedc-0ed9aa8cd558","type":"LinearAxis"}],"root_ids":["de728a47-5ac5-4e11-9f3f-13403631492d"]},"title":"Bokeh Application","version":"0.12.13"}};
  var render_items = [{"docid":"12748b16-8336-4f3d-9203-2aabc902151d","elementid":"1cdfbc47-2364-47e1-8d6d-20de98f7fd6f","modelid":"de728a47-5ac5-4e11-9f3f-13403631492d"}];
  root.Bokeh.embed.embed_items_notebook(docs_json, render_items);

  }
  if (root.Bokeh !== undefined) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (root.Bokeh !== undefined) {
        embed_document(root);
        clearInterval(timer);
      }
      attempts++;
      if (attempts > 100) {
        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing")
        clearInterval(timer);
      }
    }, 10, root)
  }
})(window);
</script>
</div>




```python
%%opts Curve [width=200] (color='indianred')
Tickers = ['A', 'AA', 'AAL', 'AAMC']
grouped = ds.select(Ticker=Tickers).to(hv.Curve, 'Date', 'Price')
grouped.grid('Ticker')
```




<div style='display: table; margin: 0 auto;'>

<div class="bk-root">
    <div class="bk-plotdiv" id="d702f325-6c69-4f16-8948-9f3b5672a50b"></div>
</div>
<script type="text/javascript">
  (function(root) {
  function embed_document(root) {

  var docs_json = {"1e40b652-9752-4c48-816e-7cbfbf2a7086":{"roots":{"references":[{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"d83de144-37f6-457f-ac42-b005a1ac3237","subtype":"Figure","type":"Plot"},"ticker":{"id":"a4a3c38f-b865-47cf-85a6-7474c864462c","type":"CategoricalTicker"}},"id":"dbef0a02-f041-4eb2-af31-f97bf5cc3381","type":"Grid"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"3c35610f-de4f-4803-9218-91e4e22746cf","type":"BoxAnnotation"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"39650cfc-a47d-4a9d-b843-1a619a25da7c","subtype":"Figure","type":"Plot"},"ticker":{"id":"bb39fe6d-1c66-46e7-b113-c6c924999c3a","type":"BasicTicker"}},"id":"a5b775a5-e030-456c-a910-63d620b9bee0","type":"Grid"},{"attributes":{},"id":"181fbf79-7789-4080-add0-44284d68b0a4","type":"BasicTicker"},{"attributes":{"source":{"id":"60e8ac28-5f58-41bb-b1e2-a97f2e48e2a9","type":"ColumnDataSource"}},"id":"7c47205d-29a7-4079-9d44-1e553d89a947","type":"CDSView"},{"attributes":{"children":[{"id":"09643cba-dfbf-4fd4-8868-ad381e1b9223","type":"Row"}]},"id":"44e2299b-cd60-4619-b2e2-ca4910c7939a","type":"Column"},{"attributes":{},"id":"f2b5fd8b-bc12-4513-addd-41ad68bb4b41","type":"PanTool"},{"attributes":{"callback":null,"factors":["2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-16","2018-01-17","2018-01-18","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"]},"id":"167e99df-4795-423c-b336-f4cb9ab03e3c","type":"FactorRange"},{"attributes":{"overlay":{"id":"289373c9-719f-4fac-896c-0d58a92d6f0a","type":"BoxAnnotation"}},"id":"a16e7a9b-bd0d-4af8-88b0-f8d818b9764f","type":"BoxZoomTool"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"a650c1f3-56d7-43aa-b7bc-e2ebb0d1d808","type":"Title"},{"attributes":{"callback":null},"id":"03c20f64-2325-418a-8250-3982a15fb98f","type":"Range1d"},{"attributes":{},"id":"b338c03c-727e-405a-8281-1d3d2c92471d","type":"PanTool"},{"attributes":{},"id":"00501c8a-b138-43a1-8029-5d6cb55e479c","type":"CategoricalTicker"},{"attributes":{"line_alpha":0.2,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"426d3f52-e1d6-44f8-b097-b97a2222ba9b","type":"Line"},{"attributes":{"axis_label":"Ticker","formatter":{"id":"9f482e1a-2e92-4439-980c-ca30de9febc4","type":"CategoricalTickFormatter"},"major_label_orientation":0.0,"major_label_text_baseline":"middle","plot":{"id":"77e742eb-00c0-4c88-b1b7-284d25b1bb76","subtype":"Figure","type":"Plot"},"ticker":{"id":"38b76bba-2870-442f-9fe0-3aef0000c8ab","type":"CategoricalTicker"}},"id":"9791aef2-b6d3-4c2c-a038-97921d71c3c8","type":"CategoricalAxis"},{"attributes":{},"id":"33cf5f51-c074-4fbb-b333-134dc06d8b66","type":"CategoricalTicker"},{"attributes":{},"id":"48b6fe8d-42ec-4022-b243-0792c5c3cd22","type":"SaveTool"},{"attributes":{"tools":[{"id":"aacaa118-fdc6-4913-8af8-fff0c28db26b","type":"SaveTool"},{"id":"ed63accf-16d0-4216-8dec-6ea5644da4fd","type":"PanTool"},{"id":"740c3c96-2f39-4c5d-94ff-26b2e65b5882","type":"WheelZoomTool"},{"id":"3e6d9220-fa71-42bd-8482-fb8a47bc1ec8","type":"BoxZoomTool"},{"id":"aa645273-2d28-4431-973f-c68bf793cb5c","type":"ResetTool"},{"id":"98247dcf-ff44-4263-abaf-3ce06e38208a","type":"SaveTool"},{"id":"f2b5fd8b-bc12-4513-addd-41ad68bb4b41","type":"PanTool"},{"id":"011043bd-1a2a-4217-a051-909e1b4a43ae","type":"WheelZoomTool"},{"id":"2d7769b9-4934-47fb-bb50-ea304f94a36f","type":"BoxZoomTool"},{"id":"6ebac775-726b-4c75-98c6-fcbdd53089b7","type":"ResetTool"},{"id":"48b6fe8d-42ec-4022-b243-0792c5c3cd22","type":"SaveTool"},{"id":"60e11b5d-a707-4471-a0b2-08bacf0e70e3","type":"PanTool"},{"id":"fe0e40c7-f155-4aa3-9598-d7ce516a7c3d","type":"WheelZoomTool"},{"id":"65ef88c2-9afc-46c2-a096-89105e2aa412","type":"BoxZoomTool"},{"id":"c8aa312f-b1c7-40cf-8a63-f6ae3d4afd7a","type":"ResetTool"},{"id":"fdf44910-a124-47ae-a063-b5402031d3bb","type":"SaveTool"},{"id":"d8640b45-ff2d-4da0-ac31-d8732b59ca5d","type":"PanTool"},{"id":"4bf322e0-96fa-4659-82af-11341a347b2f","type":"WheelZoomTool"},{"id":"a16e7a9b-bd0d-4af8-88b0-f8d818b9764f","type":"BoxZoomTool"},{"id":"3f3c668e-8ea3-4d0b-b430-124ecb48d183","type":"ResetTool"}]},"id":"87de771a-6de5-4585-a9a7-cafdf9fda91e","type":"ProxyToolbar"},{"attributes":{},"id":"3620497b-242a-4f8d-bb52-083dd4366134","type":"BasicTickFormatter"},{"attributes":{},"id":"e5eccd52-dfab-4aea-8f56-b4c1edf56a36","type":"ResetTool"},{"attributes":{},"id":"bb39fe6d-1c66-46e7-b113-c6c924999c3a","type":"BasicTicker"},{"attributes":{},"id":"011043bd-1a2a-4217-a051-909e1b4a43ae","type":"WheelZoomTool"},{"attributes":{},"id":"98247dcf-ff44-4263-abaf-3ce06e38208a","type":"SaveTool"},{"attributes":{},"id":"4e80f1d3-7660-4ad2-8101-a6c9ff06d3c4","type":"CategoricalTickFormatter"},{"attributes":{},"id":"b3284b74-1106-419e-91bd-f4e5c2990195","type":"CategoricalScale"},{"attributes":{},"id":"2344d6cb-3ba5-4c79-8b39-fb7b7e770e39","type":"BasicTicker"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"39650cfc-a47d-4a9d-b843-1a619a25da7c","subtype":"Figure","type":"Plot"},"ticker":{"id":"feb96dba-c545-4248-8b7c-1db6cf154951","type":"CategoricalTicker"}},"id":"fa3ee477-3dcd-4243-9bcb-9571f7f5efdb","type":"Grid"},{"attributes":{},"id":"60e11b5d-a707-4471-a0b2-08bacf0e70e3","type":"PanTool"},{"attributes":{},"id":"aa645273-2d28-4431-973f-c68bf793cb5c","type":"ResetTool"},{"attributes":{"overlay":{"id":"2378188e-8a3f-4862-bcc1-ef9a4495fbe8","type":"BoxAnnotation"}},"id":"27986a1b-692d-4168-aced-f5b2d0e605a5","type":"BoxZoomTool"},{"attributes":{"grid_line_alpha":{"value":0},"plot":{"id":"77e742eb-00c0-4c88-b1b7-284d25b1bb76","subtype":"Figure","type":"Plot"},"ticker":{"id":"38b76bba-2870-442f-9fe0-3aef0000c8ab","type":"CategoricalTicker"}},"id":"124425db-8d2e-4c9f-b2fc-dc892d8b9e22","type":"Grid"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"d83de144-37f6-457f-ac42-b005a1ac3237","subtype":"Figure","type":"Plot"},"ticker":{"id":"2344d6cb-3ba5-4c79-8b39-fb7b7e770e39","type":"BasicTicker"}},"id":"e6e50eb3-cb52-43a7-a299-725b92befb90","type":"Grid"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"fdf44910-a124-47ae-a063-b5402031d3bb","type":"SaveTool"},{"id":"d8640b45-ff2d-4da0-ac31-d8732b59ca5d","type":"PanTool"},{"id":"4bf322e0-96fa-4659-82af-11341a347b2f","type":"WheelZoomTool"},{"id":"a16e7a9b-bd0d-4af8-88b0-f8d818b9764f","type":"BoxZoomTool"},{"id":"3f3c668e-8ea3-4d0b-b430-124ecb48d183","type":"ResetTool"}]},"id":"1177acf6-63f8-4aba-b0bf-36c2ebb48445","type":"Toolbar"},{"attributes":{},"id":"aacaa118-fdc6-4913-8af8-fff0c28db26b","type":"SaveTool"},{"attributes":{"children":[{"id":"81bc8513-b115-4f47-aaff-4efa4b5a6766","type":"Column"},{"id":"77e742eb-00c0-4c88-b1b7-284d25b1bb76","subtype":"Figure","type":"Plot"}]},"id":"a9a8b629-18ec-49be-92dc-dc3c5b91053a","type":"Column"},{"attributes":{},"id":"d0611471-a4b3-47c5-98ae-331b8d50503d","type":"LinearScale"},{"attributes":{},"id":"d8640b45-ff2d-4da0-ac31-d8732b59ca5d","type":"PanTool"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"ZmZmZmbmUEAUrkfhelRRQDMzMzMzM1FAmpmZmZl5UUAzMzMzM4NRQOF6FK5H8VFAw/UoXI+yUUAzMzMzM7NRQB+F61G47lFAH4XrUbjOUUCkcD0K1wNSQFyPwvUoDFJAFK5H4XpEUkAfhetRuF5SQFyPwvUoXFJAhetRuB5lUkDXo3A9CndSQBSuR+F6tFJAUrgeheuhUkCPwvUoXD9SQOxRuB6FW1JA","dtype":"float64","shape":[21]}}},"id":"0e682a3b-58b4-462d-a746-1810b0965002","type":"ColumnDataSource"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"98247dcf-ff44-4263-abaf-3ce06e38208a","type":"SaveTool"},{"id":"f2b5fd8b-bc12-4513-addd-41ad68bb4b41","type":"PanTool"},{"id":"011043bd-1a2a-4217-a051-909e1b4a43ae","type":"WheelZoomTool"},{"id":"2d7769b9-4934-47fb-bb50-ea304f94a36f","type":"BoxZoomTool"},{"id":"6ebac775-726b-4c75-98c6-fcbdd53089b7","type":"ResetTool"}]},"id":"45952ae9-f6b7-4587-b190-0aa7a913b34d","type":"Toolbar"},{"attributes":{},"id":"c2889052-9f23-46fe-ba9d-a3f35c581687","type":"CategoricalTickFormatter"},{"attributes":{"axis_label":"Date","bounds":"auto","formatter":{"id":"97ccd268-9378-430c-978e-4d2f2487d95b","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"39650cfc-a47d-4a9d-b843-1a619a25da7c","subtype":"Figure","type":"Plot"},"ticker":{"id":"feb96dba-c545-4248-8b7c-1db6cf154951","type":"CategoricalTicker"},"visible":false},"id":"1a696739-0c19-4253-b2a3-b6c8ae7aee47","type":"CategoricalAxis"},{"attributes":{"dimension":1,"grid_line_alpha":{"value":0},"plot":{"id":"77e742eb-00c0-4c88-b1b7-284d25b1bb76","subtype":"Figure","type":"Plot"},"ticker":{"id":"e815bc25-6be7-4e02-812c-b435219393ba","type":"BasicTicker"}},"id":"d8f9b74c-04a3-41e0-9bba-9345fd4c33a1","type":"Grid"},{"attributes":{"line_alpha":0.2,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"102ddc29-ec07-44a3-948b-b0105b4d25a5","type":"Line"},{"attributes":{"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"bcc94ea9-6246-4362-bb63-b3e03a4f2ffa","type":"Line"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"5a83dad6-ae62-462c-b1dd-1b20f47dd60b","type":"BoxAnnotation"},{"attributes":{"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"b6e678c9-2b23-4de4-8da8-3f1eaaddb326","type":"Line"},{"attributes":{},"id":"740c3c96-2f39-4c5d-94ff-26b2e65b5882","type":"WheelZoomTool"},{"attributes":{},"id":"ed63accf-16d0-4216-8dec-6ea5644da4fd","type":"PanTool"},{"attributes":{"callback":null,"factors":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"]},"id":"8b82e6b6-2034-4d8f-9a99-6d289945e34f","type":"FactorRange"},{"attributes":{},"id":"feb96dba-c545-4248-8b7c-1db6cf154951","type":"CategoricalTicker"},{"attributes":{},"id":"a4a3c38f-b865-47cf-85a6-7474c864462c","type":"CategoricalTicker"},{"attributes":{},"id":"46809484-db34-4c66-a31d-746becaf38ff","type":"CategoricalScale"},{"attributes":{},"id":"e815bc25-6be7-4e02-812c-b435219393ba","type":"BasicTicker"},{"attributes":{},"id":"fe0e40c7-f155-4aa3-9598-d7ce516a7c3d","type":"WheelZoomTool"},{"attributes":{},"id":"a15bfa0f-05f8-4d50-aa7f-ba3c8871e67a","type":"WheelZoomTool"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"H4XrUbh+SkAK16NwPSpKQPYoXI/CVUpAMzMzMzNTSkBxPQrXoxBKQArXo3A9CkpApHA9CtfjSkD2KFyPwjVMQFyPwvUoPE1ArkfhehT+TEAUrkfhehRNQOxRuB6FK01ASOF6FK4HTUDNzMzMzAxNQIXrUbgeJU1AhetRuB5lS0BmZmZmZoZKQClcj8L1iEpA16NwPQpXSkDsUbgehUtKQClcj8L1KEtA","dtype":"float64","shape":[21]}}},"id":"7bac8a75-f823-4645-bdd3-357d736d5cc7","type":"ColumnDataSource"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"1dd1c716-7c8b-4f8f-984d-3011c8e694f4","type":"CategoricalAxis"}],"left":[{"id":"c3713969-0708-4f28-bfd6-a0975ec94ff3","type":"LinearAxis"}],"min_border_bottom":3,"min_border_left":3,"min_border_right":3,"min_border_top":3,"plot_height":120,"plot_width":200,"renderers":[{"id":"1dd1c716-7c8b-4f8f-984d-3011c8e694f4","type":"CategoricalAxis"},{"id":"7ae07475-18ad-487a-b090-7f13b3119ef5","type":"Grid"},{"id":"c3713969-0708-4f28-bfd6-a0975ec94ff3","type":"LinearAxis"},{"id":"7c0b1c49-e050-4965-a9d6-0cd646309382","type":"Grid"},{"id":"289373c9-719f-4fac-896c-0d58a92d6f0a","type":"BoxAnnotation"},{"id":"5a2cd04d-9990-477e-a322-5809ab787854","type":"GlyphRenderer"}],"title":{"id":"04f24017-d84c-4a49-81a4-3e9c3f291dee","type":"Title"},"toolbar":{"id":"1177acf6-63f8-4aba-b0bf-36c2ebb48445","type":"Toolbar"},"toolbar_location":null,"x_range":{"id":"167e99df-4795-423c-b336-f4cb9ab03e3c","type":"FactorRange"},"x_scale":{"id":"86cc6118-aa5d-4144-8a8c-c849c2c898d1","type":"CategoricalScale"},"y_range":{"id":"09ee7d65-4e80-4790-8a3e-6ed0b9b3cad4","type":"Range1d"},"y_scale":{"id":"d0611471-a4b3-47c5-98ae-331b8d50503d","type":"LinearScale"}},"id":"c2eda267-c6c2-4b5e-a9dc-d45bb9033137","subtype":"Figure","type":"Plot"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"b338c03c-727e-405a-8281-1d3d2c92471d","type":"PanTool"},{"id":"a15bfa0f-05f8-4d50-aa7f-ba3c8871e67a","type":"WheelZoomTool"},{"id":"27986a1b-692d-4168-aced-f5b2d0e605a5","type":"BoxZoomTool"},{"id":"0559bc25-ab22-4292-8a72-9cb57d04d054","type":"SaveTool"},{"id":"e5eccd52-dfab-4aea-8f56-b4c1edf56a36","type":"ResetTool"},{"id":"73f52d9a-4ca3-4a04-b896-d8526ca5bacd","type":"HelpTool"}]},"id":"bbeee331-ddcc-4da7-a900-129fca80491b","type":"Toolbar"},{"attributes":{},"id":"34ec1bbd-3db6-4026-942a-44025d231957","type":"CategoricalScale"},{"attributes":{"children":[{"id":"c73030be-d3ba-4209-b496-20ce1b8137a9","type":"ToolbarBox"},{"id":"44e2299b-cd60-4619-b2e2-ca4910c7939a","type":"Column"}]},"id":"81bc8513-b115-4f47-aaff-4efa4b5a6766","type":"Column"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"289373c9-719f-4fac-896c-0d58a92d6f0a","type":"BoxAnnotation"},{"attributes":{},"id":"2b51d9fa-28b4-4c39-bd34-5ecc1fee5ba1","type":"BasicTickFormatter"},{"attributes":{"data_source":{"id":"60e8ac28-5f58-41bb-b1e2-a97f2e48e2a9","type":"ColumnDataSource"},"glyph":{"id":"f0af38c6-3576-4149-b8e0-d4ab846d72f2","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"102ddc29-ec07-44a3-948b-b0105b4d25a5","type":"Line"},"nonselection_glyph":{"id":"b079d553-cfaa-42aa-9b46-53416237fe31","type":"Line"},"selection_glyph":null,"view":{"id":"7c47205d-29a7-4079-9d44-1e553d89a947","type":"CDSView"}},"id":"5a2cd04d-9990-477e-a322-5809ab787854","type":"GlyphRenderer"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"7df64f67-7281-4ffd-ade4-7dbaf7293643","type":"CategoricalAxis"}],"left":[{"id":"1f0517d3-c43a-4135-aab4-0f615ae88cba","type":"LinearAxis"}],"min_border_bottom":3,"min_border_left":3,"min_border_right":3,"min_border_top":3,"plot_height":120,"plot_width":200,"renderers":[{"id":"7df64f67-7281-4ffd-ade4-7dbaf7293643","type":"CategoricalAxis"},{"id":"dbef0a02-f041-4eb2-af31-f97bf5cc3381","type":"Grid"},{"id":"1f0517d3-c43a-4135-aab4-0f615ae88cba","type":"LinearAxis"},{"id":"e6e50eb3-cb52-43a7-a299-725b92befb90","type":"Grid"},{"id":"5a83dad6-ae62-462c-b1dd-1b20f47dd60b","type":"BoxAnnotation"},{"id":"a1b0eee3-b282-4c1c-8e85-c660665ed1b0","type":"GlyphRenderer"}],"title":{"id":"a650c1f3-56d7-43aa-b7bc-e2ebb0d1d808","type":"Title"},"toolbar":{"id":"b2990378-ea0e-487f-9f00-e4f957890354","type":"Toolbar"},"toolbar_location":null,"x_range":{"id":"60f7d032-340d-4449-aaa1-2592af6cb63a","type":"FactorRange"},"x_scale":{"id":"ce83f2f3-092a-49ab-802b-42f765d652d3","type":"CategoricalScale"},"y_range":{"id":"09ee7d65-4e80-4790-8a3e-6ed0b9b3cad4","type":"Range1d"},"y_scale":{"id":"dc220d7a-7bd4-47fc-900f-c2a34141f7e6","type":"LinearScale"}},"id":"d83de144-37f6-457f-ac42-b005a1ac3237","subtype":"Figure","type":"Plot"},{"attributes":{"line_alpha":0.1,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"7c10ecd6-a2f7-4426-88e2-58e374295e56","type":"Line"},{"attributes":{},"id":"6ebac775-726b-4c75-98c6-fcbdd53089b7","type":"ResetTool"},{"attributes":{},"id":"97ccd268-9378-430c-978e-4d2f2487d95b","type":"CategoricalTickFormatter"},{"attributes":{"callback":null,"end":80.2,"start":52.02},"id":"09ee7d65-4e80-4790-8a3e-6ed0b9b3cad4","type":"Range1d"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"1a696739-0c19-4253-b2a3-b6c8ae7aee47","type":"CategoricalAxis"}],"left":[{"id":"996c50cf-0504-4fef-9532-c98483d0ee53","type":"LinearAxis"}],"min_border_bottom":3,"min_border_left":3,"min_border_right":3,"min_border_top":3,"plot_height":120,"plot_width":200,"renderers":[{"id":"1a696739-0c19-4253-b2a3-b6c8ae7aee47","type":"CategoricalAxis"},{"id":"fa3ee477-3dcd-4243-9bcb-9571f7f5efdb","type":"Grid"},{"id":"996c50cf-0504-4fef-9532-c98483d0ee53","type":"LinearAxis"},{"id":"a5b775a5-e030-456c-a910-63d620b9bee0","type":"Grid"},{"id":"3c35610f-de4f-4803-9218-91e4e22746cf","type":"BoxAnnotation"},{"id":"ebb55f70-d3a0-43f2-9107-a9e09fa852ec","type":"GlyphRenderer"}],"title":{"id":"15d34276-00f1-4089-95fb-c3e40bc3844b","type":"Title"},"toolbar":{"id":"2d10363e-f40a-42e4-80e4-3af9ca68eec5","type":"Toolbar"},"toolbar_location":null,"x_range":{"id":"8b82e6b6-2034-4d8f-9a99-6d289945e34f","type":"FactorRange"},"x_scale":{"id":"34ec1bbd-3db6-4026-942a-44025d231957","type":"CategoricalScale"},"y_range":{"id":"09ee7d65-4e80-4790-8a3e-6ed0b9b3cad4","type":"Range1d"},"y_scale":{"id":"2182a22a-b03d-4e48-813e-8c33b9d0fcc4","type":"LinearScale"}},"id":"39650cfc-a47d-4a9d-b843-1a619a25da7c","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"9f482e1a-2e92-4439-980c-ca30de9febc4","type":"CategoricalTickFormatter"},{"attributes":{"overlay":{"id":"0ab7272b-7ec1-40b7-8113-fbb909755374","type":"BoxAnnotation"}},"id":"2d7769b9-4934-47fb-bb50-ea304f94a36f","type":"BoxZoomTool"},{"attributes":{},"id":"73f52d9a-4ca3-4a04-b896-d8526ca5bacd","type":"HelpTool"},{"attributes":{"source":{"id":"7bac8a75-f823-4645-bdd3-357d736d5cc7","type":"ColumnDataSource"}},"id":"54be3765-d734-4419-9366-d539ea283f4f","type":"CDSView"},{"attributes":{},"id":"f1175442-d60f-4d70-af11-9a934bd2c195","type":"BasicTickFormatter"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"c2eda267-c6c2-4b5e-a9dc-d45bb9033137","subtype":"Figure","type":"Plot"},"ticker":{"id":"181fbf79-7789-4080-add0-44284d68b0a4","type":"BasicTicker"}},"id":"7c0b1c49-e050-4965-a9d6-0cd646309382","type":"Grid"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"aacaa118-fdc6-4913-8af8-fff0c28db26b","type":"SaveTool"},{"id":"ed63accf-16d0-4216-8dec-6ea5644da4fd","type":"PanTool"},{"id":"740c3c96-2f39-4c5d-94ff-26b2e65b5882","type":"WheelZoomTool"},{"id":"3e6d9220-fa71-42bd-8482-fb8a47bc1ec8","type":"BoxZoomTool"},{"id":"aa645273-2d28-4431-973f-c68bf793cb5c","type":"ResetTool"}]},"id":"2d10363e-f40a-42e4-80e4-3af9ca68eec5","type":"Toolbar"},{"attributes":{},"id":"c8aa312f-b1c7-40cf-8a63-f6ae3d4afd7a","type":"ResetTool"},{"attributes":{"axis_label":"Stock Input","bounds":"auto","formatter":{"id":"2b51d9fa-28b4-4c39-bd34-5ecc1fee5ba1","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"c2eda267-c6c2-4b5e-a9dc-d45bb9033137","subtype":"Figure","type":"Plot"},"ticker":{"id":"181fbf79-7789-4080-add0-44284d68b0a4","type":"BasicTicker"},"visible":false},"id":"c3713969-0708-4f28-bfd6-a0975ec94ff3","type":"LinearAxis"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-16","2018-01-17","2018-01-18","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"zczMzMx8U0DNzMzMzAxUQM3MzMzMDFRAzczMzMwMVEAAAAAAAMBTQAAAAAAAwFNAj8L1KFz/U0DNzMzMzPxSQPLSTWIQ4FFA8tJNYhDgUUAB3gIJiotQQM3MzMzM7FBArWnecYpqUUCtad5ximpRQJqZmZmZCVFAmpmZmZkJUUBa9bnaikFRQFr1udqKQVFA","dtype":"float64","shape":[18]}}},"id":"60e8ac28-5f58-41bb-b1e2-a97f2e48e2a9","type":"ColumnDataSource"},{"attributes":{"callback":{"id":"1a7c4130-8a8f-4478-9fe2-9a0e721428df","type":"CustomJS"},"factors":["A","AA","AAL","AAMC"]},"id":"7d4b7f5a-9602-47db-8fd8-092b11509443","type":"FactorRange"},{"attributes":{},"id":"0559bc25-ab22-4292-8a72-9cb57d04d054","type":"SaveTool"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"9ihcj8KVS0AAAAAAAEBLQJqZmZmZWUtA7FG4HoULS0AAAAAAAIBLQJqZmZmZGUtA9ihcj8IVTEAUrkfhenRMQOF6FK5HYUxAH4XrUbgeTEAfhetRuH5MQAAAAAAAgEpAzczMzMyMSkC4HoXrUXhKQB+F61G4PkpAZmZmZmamSkCuR+F6FI5KQAAAAAAAAEtAH4XrUbg+S0DD9Shcj0JKQMP1KFyPAkpA","dtype":"float64","shape":[21]}}},"id":"f60d27b2-f204-48fa-9b44-77838ac05d2f","type":"ColumnDataSource"},{"attributes":{},"id":"2182a22a-b03d-4e48-813e-8c33b9d0fcc4","type":"LinearScale"},{"attributes":{"line_alpha":0.1,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"4af6e763-f4aa-40ec-aac7-f59046a70e72","type":"Line"},{"attributes":{"line_alpha":0.1,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"2b496052-95ba-4bf3-94e4-4d44fe43d618","type":"Line"},{"attributes":{"axis_label":"Stock Input","bounds":"auto","formatter":{"id":"e82b2e9f-f92d-4634-935f-a65cb0425f78","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"39650cfc-a47d-4a9d-b843-1a619a25da7c","subtype":"Figure","type":"Plot"},"ticker":{"id":"bb39fe6d-1c66-46e7-b113-c6c924999c3a","type":"BasicTicker"},"visible":false},"id":"996c50cf-0504-4fef-9532-c98483d0ee53","type":"LinearAxis"},{"attributes":{"overlay":{"id":"5a83dad6-ae62-462c-b1dd-1b20f47dd60b","type":"BoxAnnotation"}},"id":"65ef88c2-9afc-46c2-a096-89105e2aa412","type":"BoxZoomTool"},{"attributes":{"data_source":{"id":"7bac8a75-f823-4645-bdd3-357d736d5cc7","type":"ColumnDataSource"},"glyph":{"id":"bcc94ea9-6246-4362-bb63-b3e03a4f2ffa","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"c19d38b8-2a50-4d50-b15e-d1f9d5caf0fe","type":"Line"},"nonselection_glyph":{"id":"4af6e763-f4aa-40ec-aac7-f59046a70e72","type":"Line"},"selection_glyph":null,"view":{"id":"54be3765-d734-4419-9366-d539ea283f4f","type":"CDSView"}},"id":"a1b0eee3-b282-4c1c-8e85-c660665ed1b0","type":"GlyphRenderer"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"04f24017-d84c-4a49-81a4-3e9c3f291dee","type":"Title"},{"attributes":{"plot":null,"text":""},"id":"a335f6f6-be1a-41e4-a1fc-b84a7ca1cf43","type":"Title"},{"attributes":{"toolbar":{"id":"87de771a-6de5-4585-a9a7-cafdf9fda91e","type":"ProxyToolbar"},"toolbar_location":"above"},"id":"c73030be-d3ba-4209-b496-20ce1b8137a9","type":"ToolbarBox"},{"attributes":{"axis_label":"Stock Input","bounds":"auto","formatter":{"id":"d2977c9c-eb25-4314-a8ba-989d2fe489be","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"a08bbd1f-384d-42e6-9c26-ca39882b9873","subtype":"Figure","type":"Plot"},"ticker":{"id":"ac523ef9-7257-4a14-b73e-8c7e389bde6b","type":"BasicTicker"},"visible":false},"id":"60042780-076e-46be-a967-cb87946ed8f7","type":"LinearAxis"},{"attributes":{},"id":"4bf322e0-96fa-4659-82af-11341a347b2f","type":"WheelZoomTool"},{"attributes":{},"id":"ce83f2f3-092a-49ab-802b-42f765d652d3","type":"CategoricalScale"},{"attributes":{"args":{"range":{"id":"7d4b7f5a-9602-47db-8fd8-092b11509443","type":"FactorRange"}},"code":"range.setv({start: 0, end: range.factors.length})"},"id":"1a7c4130-8a8f-4478-9fe2-9a0e721428df","type":"CustomJS"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"9f172038-70be-4159-8e37-b3f1169b2f88","type":"Title"},{"attributes":{"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"f0af38c6-3576-4149-b8e0-d4ab846d72f2","type":"Line"},{"attributes":{"line_alpha":0.2,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"c19d38b8-2a50-4d50-b15e-d1f9d5caf0fe","type":"Line"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"c2eda267-c6c2-4b5e-a9dc-d45bb9033137","subtype":"Figure","type":"Plot"},"ticker":{"id":"00501c8a-b138-43a1-8029-5d6cb55e479c","type":"CategoricalTicker"}},"id":"7ae07475-18ad-487a-b090-7f13b3119ef5","type":"Grid"},{"attributes":{},"id":"d2977c9c-eb25-4314-a8ba-989d2fe489be","type":"BasicTickFormatter"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"2378188e-8a3f-4862-bcc1-ef9a4495fbe8","type":"BoxAnnotation"},{"attributes":{"line_alpha":0.2,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"c84b471e-d2e5-4fdc-8020-1028acee8676","type":"Line"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"15d34276-00f1-4089-95fb-c3e40bc3844b","type":"Title"},{"attributes":{"below":[{"id":"9791aef2-b6d3-4c2c-a038-97921d71c3c8","type":"CategoricalAxis"}],"left":[{"id":"569cf78b-5370-4513-b80a-902a82978870","type":"LinearAxis"}],"outline_line_alpha":{"value":0},"plot_height":53,"plot_width":800,"renderers":[{"id":"9791aef2-b6d3-4c2c-a038-97921d71c3c8","type":"CategoricalAxis"},{"id":"124425db-8d2e-4c9f-b2fc-dc892d8b9e22","type":"Grid"},{"id":"569cf78b-5370-4513-b80a-902a82978870","type":"LinearAxis"},{"id":"d8f9b74c-04a3-41e0-9bba-9345fd4c33a1","type":"Grid"},{"id":"2378188e-8a3f-4862-bcc1-ef9a4495fbe8","type":"BoxAnnotation"}],"title":{"id":"a335f6f6-be1a-41e4-a1fc-b84a7ca1cf43","type":"Title"},"toolbar":{"id":"bbeee331-ddcc-4da7-a900-129fca80491b","type":"Toolbar"},"toolbar_location":null,"x_range":{"id":"7d4b7f5a-9602-47db-8fd8-092b11509443","type":"FactorRange"},"x_scale":{"id":"46809484-db34-4c66-a31d-746becaf38ff","type":"CategoricalScale"},"y_range":{"id":"03c20f64-2325-418a-8250-3982a15fb98f","type":"Range1d"},"y_scale":{"id":"106a3236-6665-4429-8c1e-3bd178aff408","type":"LinearScale"}},"id":"77e742eb-00c0-4c88-b1b7-284d25b1bb76","subtype":"Figure","type":"Plot"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"b0fa55aa-37b0-4795-abc7-a7623b8d6cb7","type":"CategoricalAxis"}],"left":[{"id":"60042780-076e-46be-a967-cb87946ed8f7","type":"LinearAxis"}],"min_border_bottom":3,"min_border_left":3,"min_border_right":3,"min_border_top":3,"plot_height":120,"plot_width":200,"renderers":[{"id":"b0fa55aa-37b0-4795-abc7-a7623b8d6cb7","type":"CategoricalAxis"},{"id":"cbf7be83-2c41-4f80-8d9a-a23eb7030a49","type":"Grid"},{"id":"60042780-076e-46be-a967-cb87946ed8f7","type":"LinearAxis"},{"id":"4f049535-b7bd-4d55-91fd-c69c470578f5","type":"Grid"},{"id":"0ab7272b-7ec1-40b7-8113-fbb909755374","type":"BoxAnnotation"},{"id":"0f1550e8-330f-453e-9504-71bd7f4d9a54","type":"GlyphRenderer"}],"title":{"id":"9f172038-70be-4159-8e37-b3f1169b2f88","type":"Title"},"toolbar":{"id":"45952ae9-f6b7-4587-b190-0aa7a913b34d","type":"Toolbar"},"toolbar_location":null,"x_range":{"id":"79987d0f-71c2-45b5-8b39-d784c8197352","type":"FactorRange"},"x_scale":{"id":"b3284b74-1106-419e-91bd-f4e5c2990195","type":"CategoricalScale"},"y_range":{"id":"09ee7d65-4e80-4790-8a3e-6ed0b9b3cad4","type":"Range1d"},"y_scale":{"id":"2d79e5d5-fdf1-4183-9dde-e67683ace1ab","type":"LinearScale"}},"id":"a08bbd1f-384d-42e6-9c26-ca39882b9873","subtype":"Figure","type":"Plot"},{"attributes":{},"id":"dc220d7a-7bd4-47fc-900f-c2a34141f7e6","type":"LinearScale"},{"attributes":{},"id":"2d79e5d5-fdf1-4183-9dde-e67683ace1ab","type":"LinearScale"},{"attributes":{"overlay":{"id":"3c35610f-de4f-4803-9218-91e4e22746cf","type":"BoxAnnotation"}},"id":"3e6d9220-fa71-42bd-8482-fb8a47bc1ec8","type":"BoxZoomTool"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"a08bbd1f-384d-42e6-9c26-ca39882b9873","subtype":"Figure","type":"Plot"},"ticker":{"id":"ac523ef9-7257-4a14-b73e-8c7e389bde6b","type":"BasicTicker"}},"id":"4f049535-b7bd-4d55-91fd-c69c470578f5","type":"Grid"},{"attributes":{},"id":"e82b2e9f-f92d-4634-935f-a65cb0425f78","type":"BasicTickFormatter"},{"attributes":{"axis_label":"Date","bounds":"auto","formatter":{"id":"c2889052-9f23-46fe-ba9d-a3f35c581687","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"c2eda267-c6c2-4b5e-a9dc-d45bb9033137","subtype":"Figure","type":"Plot"},"ticker":{"id":"00501c8a-b138-43a1-8029-5d6cb55e479c","type":"CategoricalTicker"},"visible":false},"id":"1dd1c716-7c8b-4f8f-984d-3011c8e694f4","type":"CategoricalAxis"},{"attributes":{"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"f26de116-ff33-4b06-b51d-d85f9eb7ea44","type":"Line"},{"attributes":{},"id":"ac523ef9-7257-4a14-b73e-8c7e389bde6b","type":"BasicTicker"},{"attributes":{"data_source":{"id":"f60d27b2-f204-48fa-9b44-77838ac05d2f","type":"ColumnDataSource"},"glyph":{"id":"f26de116-ff33-4b06-b51d-d85f9eb7ea44","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"c84b471e-d2e5-4fdc-8020-1028acee8676","type":"Line"},"nonselection_glyph":{"id":"2b496052-95ba-4bf3-94e4-4d44fe43d618","type":"Line"},"selection_glyph":null,"view":{"id":"31a29a58-4856-408b-bbf4-1365fd1fb284","type":"CDSView"}},"id":"0f1550e8-330f-453e-9504-71bd7f4d9a54","type":"GlyphRenderer"},{"attributes":{},"id":"106a3236-6665-4429-8c1e-3bd178aff408","type":"LinearScale"},{"attributes":{"axis_label":"Date","bounds":"auto","formatter":{"id":"4dfb2a1a-5e91-4d7d-9623-90627a6b87e8","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"a08bbd1f-384d-42e6-9c26-ca39882b9873","subtype":"Figure","type":"Plot"},"ticker":{"id":"33cf5f51-c074-4fbb-b333-134dc06d8b66","type":"CategoricalTicker"},"visible":false},"id":"b0fa55aa-37b0-4795-abc7-a7623b8d6cb7","type":"CategoricalAxis"},{"attributes":{},"id":"fdf44910-a124-47ae-a063-b5402031d3bb","type":"SaveTool"},{"attributes":{"children":[{"id":"39650cfc-a47d-4a9d-b843-1a619a25da7c","subtype":"Figure","type":"Plot"},{"id":"a08bbd1f-384d-42e6-9c26-ca39882b9873","subtype":"Figure","type":"Plot"},{"id":"d83de144-37f6-457f-ac42-b005a1ac3237","subtype":"Figure","type":"Plot"},{"id":"c2eda267-c6c2-4b5e-a9dc-d45bb9033137","subtype":"Figure","type":"Plot"}]},"id":"09643cba-dfbf-4fd4-8868-ad381e1b9223","type":"Row"},{"attributes":{"source":{"id":"f60d27b2-f204-48fa-9b44-77838ac05d2f","type":"ColumnDataSource"}},"id":"31a29a58-4856-408b-bbf4-1365fd1fb284","type":"CDSView"},{"attributes":{},"id":"38b76bba-2870-442f-9fe0-3aef0000c8ab","type":"CategoricalTicker"},{"attributes":{},"id":"86cc6118-aa5d-4144-8a8c-c849c2c898d1","type":"CategoricalScale"},{"attributes":{"formatter":{"id":"f1175442-d60f-4d70-af11-9a934bd2c195","type":"BasicTickFormatter"},"plot":{"id":"77e742eb-00c0-4c88-b1b7-284d25b1bb76","subtype":"Figure","type":"Plot"},"ticker":{"id":"e815bc25-6be7-4e02-812c-b435219393ba","type":"BasicTicker"},"visible":false},"id":"569cf78b-5370-4513-b80a-902a82978870","type":"LinearAxis"},{"attributes":{},"id":"4dfb2a1a-5e91-4d7d-9623-90627a6b87e8","type":"CategoricalTickFormatter"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"48b6fe8d-42ec-4022-b243-0792c5c3cd22","type":"SaveTool"},{"id":"60e11b5d-a707-4471-a0b2-08bacf0e70e3","type":"PanTool"},{"id":"fe0e40c7-f155-4aa3-9598-d7ce516a7c3d","type":"WheelZoomTool"},{"id":"65ef88c2-9afc-46c2-a096-89105e2aa412","type":"BoxZoomTool"},{"id":"c8aa312f-b1c7-40cf-8a63-f6ae3d4afd7a","type":"ResetTool"}]},"id":"b2990378-ea0e-487f-9f00-e4f957890354","type":"Toolbar"},{"attributes":{"line_alpha":0.1,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"b079d553-cfaa-42aa-9b46-53416237fe31","type":"Line"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"a08bbd1f-384d-42e6-9c26-ca39882b9873","subtype":"Figure","type":"Plot"},"ticker":{"id":"33cf5f51-c074-4fbb-b333-134dc06d8b66","type":"CategoricalTicker"}},"id":"cbf7be83-2c41-4f80-8d9a-a23eb7030a49","type":"Grid"},{"attributes":{"data_source":{"id":"0e682a3b-58b4-462d-a746-1810b0965002","type":"ColumnDataSource"},"glyph":{"id":"b6e678c9-2b23-4de4-8da8-3f1eaaddb326","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"426d3f52-e1d6-44f8-b097-b97a2222ba9b","type":"Line"},"nonselection_glyph":{"id":"7c10ecd6-a2f7-4426-88e2-58e374295e56","type":"Line"},"selection_glyph":null,"view":{"id":"94903b82-cd59-4141-9604-032fffc0b651","type":"CDSView"}},"id":"ebb55f70-d3a0-43f2-9107-a9e09fa852ec","type":"GlyphRenderer"},{"attributes":{"axis_label":"Date","bounds":"auto","formatter":{"id":"4e80f1d3-7660-4ad2-8101-a6c9ff06d3c4","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"d83de144-37f6-457f-ac42-b005a1ac3237","subtype":"Figure","type":"Plot"},"ticker":{"id":"a4a3c38f-b865-47cf-85a6-7474c864462c","type":"CategoricalTicker"},"visible":false},"id":"7df64f67-7281-4ffd-ade4-7dbaf7293643","type":"CategoricalAxis"},{"attributes":{"callback":null,"factors":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"]},"id":"79987d0f-71c2-45b5-8b39-d784c8197352","type":"FactorRange"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"0ab7272b-7ec1-40b7-8113-fbb909755374","type":"BoxAnnotation"},{"attributes":{"axis_label":"Stock Input","bounds":"auto","formatter":{"id":"3620497b-242a-4f8d-bb52-083dd4366134","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"d83de144-37f6-457f-ac42-b005a1ac3237","subtype":"Figure","type":"Plot"},"ticker":{"id":"2344d6cb-3ba5-4c79-8b39-fb7b7e770e39","type":"BasicTicker"},"visible":false},"id":"1f0517d3-c43a-4135-aab4-0f615ae88cba","type":"LinearAxis"},{"attributes":{"source":{"id":"0e682a3b-58b4-462d-a746-1810b0965002","type":"ColumnDataSource"}},"id":"94903b82-cd59-4141-9604-032fffc0b651","type":"CDSView"},{"attributes":{},"id":"3f3c668e-8ea3-4d0b-b430-124ecb48d183","type":"ResetTool"},{"attributes":{"callback":null,"factors":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"]},"id":"60f7d032-340d-4449-aaa1-2592af6cb63a","type":"FactorRange"}],"root_ids":["a9a8b629-18ec-49be-92dc-dc3c5b91053a"]},"title":"Bokeh Application","version":"0.12.13"}};
  var render_items = [{"docid":"1e40b652-9752-4c48-816e-7cbfbf2a7086","elementid":"d702f325-6c69-4f16-8948-9f3b5672a50b","modelid":"a9a8b629-18ec-49be-92dc-dc3c5b91053a"}];
  root.Bokeh.embed.embed_items_notebook(docs_json, render_items);

  }
  if (root.Bokeh !== undefined) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (root.Bokeh !== undefined) {
        embed_document(root);
        clearInterval(timer);
      }
      attempts++;
      if (attempts > 100) {
        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing")
        clearInterval(timer);
      }
    }, 10, root)
  }
})(window);
</script>
</div>




```python
%%opts Curve [width=600] (color=Cycle(values=['indianred', 'slateblue', 'lightseagreen', 'coral']))
grouped.overlay('Ticker')

```




<div style='display: table; margin: 0 auto;'>

<div class="bk-root">
    <div class="bk-plotdiv" id="c7e9efe7-ca23-4b56-abb5-dfe832bd15c5"></div>
</div>
<script type="text/javascript">
  (function(root) {
  function embed_document(root) {

  var docs_json = {"536dfeaf-3a35-41b7-8390-604c85001cf5":{"roots":{"references":[{"attributes":{"callback":null,"factors":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"]},"id":"6c013649-09a3-4e9e-b7c8-d6c888d45143","type":"FactorRange"},{"attributes":{"label":{"value":"AA"},"renderers":[{"id":"3b64989a-d051-43d4-bf1e-ca9595ef5691","type":"GlyphRenderer"}]},"id":"277dd3b7-939e-42d6-b627-c8df6c845b0a","type":"LegendItem"},{"attributes":{"dimension":1,"grid_line_color":{"value":null},"plot":{"id":"bea70512-44fb-4fca-b26b-a9fa5149491b","subtype":"Figure","type":"Plot"},"ticker":{"id":"052a8ffa-c29b-43c6-90ec-0a2bc59be61f","type":"BasicTicker"}},"id":"64e76ea9-0455-4b81-93cf-959c3b700913","type":"Grid"},{"attributes":{"axis_label":"Date","bounds":"auto","formatter":{"id":"ce6d8572-c6af-40ad-b3d7-237fbd10824f","type":"CategoricalTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"bea70512-44fb-4fca-b26b-a9fa5149491b","subtype":"Figure","type":"Plot"},"ticker":{"id":"e80a1ea2-e730-4fdc-b67a-4ac0e317812e","type":"CategoricalTicker"}},"id":"d49e2660-f70e-43e9-aff3-b98c7cd711cc","type":"CategoricalAxis"},{"attributes":{"label":{"value":"AAL"},"renderers":[{"id":"73f3dbae-f939-41ea-996d-d789b06e106f","type":"GlyphRenderer"}]},"id":"c902a876-1ea7-4039-8619-a30593be94b5","type":"LegendItem"},{"attributes":{"data_source":{"id":"4d455555-db12-46e5-9296-1ff9c1b485fa","type":"ColumnDataSource"},"glyph":{"id":"4e493011-053f-4ce4-86f3-c3e8cbe4cc4f","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"7f474756-1199-4323-a452-5822e4310ecb","type":"Line"},"nonselection_glyph":{"id":"3103a4f4-c6a1-4ed2-9a0f-3ca4a19c304a","type":"Line"},"selection_glyph":null,"view":{"id":"8733ff97-a7d1-47a1-b99d-882dc19f4656","type":"CDSView"}},"id":"32f7bc28-1306-45fb-8c3a-fc0cc353338e","type":"GlyphRenderer"},{"attributes":{"data_source":{"id":"32b8a6a8-a9c1-42f5-9a35-26e1168c96d7","type":"ColumnDataSource"},"glyph":{"id":"2bf00859-d5ec-4576-addc-10329ad289f4","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"5818de70-a900-4749-bd62-99237e585546","type":"Line"},"nonselection_glyph":{"id":"5d101ad1-d3d4-4eaa-9f85-a61721e8f646","type":"Line"},"selection_glyph":null,"view":{"id":"8f325110-fabe-4aed-87df-9035db7cd225","type":"CDSView"}},"id":"3b64989a-d051-43d4-bf1e-ca9595ef5691","type":"GlyphRenderer"},{"attributes":{},"id":"8a832788-ef55-40ac-aba7-2c67368644ed","type":"PanTool"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"ZmZmZmbmUEAUrkfhelRRQDMzMzMzM1FAmpmZmZl5UUAzMzMzM4NRQOF6FK5H8VFAw/UoXI+yUUAzMzMzM7NRQB+F61G47lFAH4XrUbjOUUCkcD0K1wNSQFyPwvUoDFJAFK5H4XpEUkAfhetRuF5SQFyPwvUoXFJAhetRuB5lUkDXo3A9CndSQBSuR+F6tFJAUrgeheuhUkCPwvUoXD9SQOxRuB6FW1JA","dtype":"float64","shape":[21]}}},"id":"f7538f57-2071-44d6-ad25-3c83a1be734e","type":"ColumnDataSource"},{"attributes":{"click_policy":"mute","items":[{"id":"a411bc85-8f5e-4257-a077-961459e230b5","type":"LegendItem"},{"id":"277dd3b7-939e-42d6-b627-c8df6c845b0a","type":"LegendItem"},{"id":"c902a876-1ea7-4039-8619-a30593be94b5","type":"LegendItem"},{"id":"76cd33af-fab0-40c0-ab14-b3e6fbdd3c65","type":"LegendItem"}],"plot":{"id":"bea70512-44fb-4fca-b26b-a9fa5149491b","subtype":"Figure","type":"Plot"}},"id":"fa8ab96e-b644-45c3-984a-bae834530380","type":"Legend"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-16","2018-01-17","2018-01-18","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"zczMzMx8U0DNzMzMzAxUQM3MzMzMDFRAzczMzMwMVEAAAAAAAMBTQAAAAAAAwFNAj8L1KFz/U0DNzMzMzPxSQPLSTWIQ4FFA8tJNYhDgUUAB3gIJiotQQM3MzMzM7FBArWnecYpqUUCtad5ximpRQJqZmZmZCVFAmpmZmZkJUUBa9bnaikFRQFr1udqKQVFA","dtype":"float64","shape":[18]}}},"id":"4d455555-db12-46e5-9296-1ff9c1b485fa","type":"ColumnDataSource"},{"attributes":{"line_alpha":0.2,"line_color":"#FF7F50","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"7f474756-1199-4323-a452-5822e4310ecb","type":"Line"},{"attributes":{},"id":"c9f239e1-025b-45f8-bd8c-daf3e4960b1e","type":"BasicTickFormatter"},{"attributes":{"line_alpha":0.2,"line_color":"#6A5ACD","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"5818de70-a900-4749-bd62-99237e585546","type":"Line"},{"attributes":{"overlay":{"id":"9d8190b1-d437-43fe-a50a-fd11f4462549","type":"BoxAnnotation"}},"id":"dc8f43c0-7e1e-4a16-a67f-75586663be98","type":"BoxZoomTool"},{"attributes":{"line_alpha":0.1,"line_color":"#20B2AA","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"d0dfcebb-ad2d-411f-8927-5aeed9e809af","type":"Line"},{"attributes":{"data_source":{"id":"fd6cf218-43bd-4c4d-a4d2-60315ce41b29","type":"ColumnDataSource"},"glyph":{"id":"173d2874-8957-4a04-a7f1-6d7377c0428c","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"5b420ebd-b9af-48b9-a86c-ec676d9421cc","type":"Line"},"nonselection_glyph":{"id":"d0dfcebb-ad2d-411f-8927-5aeed9e809af","type":"Line"},"selection_glyph":null,"view":{"id":"98adfccb-6b09-455c-8bab-9900bea66b41","type":"CDSView"}},"id":"73f3dbae-f939-41ea-996d-d789b06e106f","type":"GlyphRenderer"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"H4XrUbh+SkAK16NwPSpKQPYoXI/CVUpAMzMzMzNTSkBxPQrXoxBKQArXo3A9CkpApHA9CtfjSkD2KFyPwjVMQFyPwvUoPE1ArkfhehT+TEAUrkfhehRNQOxRuB6FK01ASOF6FK4HTUDNzMzMzAxNQIXrUbgeJU1AhetRuB5lS0BmZmZmZoZKQClcj8L1iEpA16NwPQpXSkDsUbgehUtKQClcj8L1KEtA","dtype":"float64","shape":[21]}}},"id":"fd6cf218-43bd-4c4d-a4d2-60315ce41b29","type":"ColumnDataSource"},{"attributes":{"line_color":"#20B2AA","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"173d2874-8957-4a04-a7f1-6d7377c0428c","type":"Line"},{"attributes":{"source":{"id":"f7538f57-2071-44d6-ad25-3c83a1be734e","type":"ColumnDataSource"}},"id":"ed95e5a1-d002-48c8-89bc-55cf5e787698","type":"CDSView"},{"attributes":{"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"0a115273-18f4-4fe9-b327-38d5f395b1ef","type":"Line"},{"attributes":{"source":{"id":"fd6cf218-43bd-4c4d-a4d2-60315ce41b29","type":"ColumnDataSource"}},"id":"98adfccb-6b09-455c-8bab-9900bea66b41","type":"CDSView"},{"attributes":{"line_alpha":0.1,"line_color":"#6A5ACD","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"5d101ad1-d3d4-4eaa-9f85-a61721e8f646","type":"Line"},{"attributes":{},"id":"052a8ffa-c29b-43c6-90ec-0a2bc59be61f","type":"BasicTicker"},{"attributes":{},"id":"32bff5fd-9b6b-48a6-9ab1-864855169ea8","type":"LinearScale"},{"attributes":{"plot":null,"text":"","text_color":{"value":"black"},"text_font_size":{"value":"12pt"}},"id":"bb4f250d-b65c-4a1d-a769-b633e8754bde","type":"Title"},{"attributes":{"line_color":"#FF7F50","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"4e493011-053f-4ce4-86f3-c3e8cbe4cc4f","type":"Line"},{"attributes":{"line_alpha":0.2,"line_color":"#20B2AA","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"5b420ebd-b9af-48b9-a86c-ec676d9421cc","type":"Line"},{"attributes":{},"id":"f9628133-a0b8-4cd8-bcd4-9c1606cb5f57","type":"SaveTool"},{"attributes":{"background_fill_color":{"value":"white"},"below":[{"id":"d49e2660-f70e-43e9-aff3-b98c7cd711cc","type":"CategoricalAxis"}],"left":[{"id":"806e9874-dd34-44df-ba61-bc1ec0601684","type":"LinearAxis"}],"min_border_bottom":10,"min_border_left":10,"min_border_right":10,"min_border_top":10,"plot_height":300,"renderers":[{"id":"d49e2660-f70e-43e9-aff3-b98c7cd711cc","type":"CategoricalAxis"},{"id":"6db9c682-5a6b-4f17-bad5-fb786a0d3855","type":"Grid"},{"id":"806e9874-dd34-44df-ba61-bc1ec0601684","type":"LinearAxis"},{"id":"64e76ea9-0455-4b81-93cf-959c3b700913","type":"Grid"},{"id":"9d8190b1-d437-43fe-a50a-fd11f4462549","type":"BoxAnnotation"},{"id":"fa8ab96e-b644-45c3-984a-bae834530380","type":"Legend"},{"id":"eb191ccb-6da6-484a-b861-478aa679ef38","type":"GlyphRenderer"},{"id":"3b64989a-d051-43d4-bf1e-ca9595ef5691","type":"GlyphRenderer"},{"id":"73f3dbae-f939-41ea-996d-d789b06e106f","type":"GlyphRenderer"},{"id":"32f7bc28-1306-45fb-8c3a-fc0cc353338e","type":"GlyphRenderer"}],"title":{"id":"bb4f250d-b65c-4a1d-a769-b633e8754bde","type":"Title"},"toolbar":{"id":"9bcfeadc-11d3-4046-88ad-81072722750a","type":"Toolbar"},"x_range":{"id":"6c013649-09a3-4e9e-b7c8-d6c888d45143","type":"FactorRange"},"x_scale":{"id":"ec599ed2-0b12-4908-a63c-b4a967e6316b","type":"CategoricalScale"},"y_range":{"id":"1add6815-978f-486c-973a-d6897737078d","type":"Range1d"},"y_scale":{"id":"32bff5fd-9b6b-48a6-9ab1-864855169ea8","type":"LinearScale"}},"id":"bea70512-44fb-4fca-b26b-a9fa5149491b","subtype":"Figure","type":"Plot"},{"attributes":{"label":{"value":"AAMC"},"renderers":[{"id":"32f7bc28-1306-45fb-8c3a-fc0cc353338e","type":"GlyphRenderer"}]},"id":"76cd33af-fab0-40c0-ab14-b3e6fbdd3c65","type":"LegendItem"},{"attributes":{"data_source":{"id":"f7538f57-2071-44d6-ad25-3c83a1be734e","type":"ColumnDataSource"},"glyph":{"id":"0a115273-18f4-4fe9-b327-38d5f395b1ef","type":"Line"},"hover_glyph":null,"muted_glyph":{"id":"b31c8a6c-be59-40a8-8365-fee95bd29e83","type":"Line"},"nonselection_glyph":{"id":"535f4154-611c-4e1d-b6dd-41877cc051de","type":"Line"},"selection_glyph":null,"view":{"id":"ed95e5a1-d002-48c8-89bc-55cf5e787698","type":"CDSView"}},"id":"eb191ccb-6da6-484a-b861-478aa679ef38","type":"GlyphRenderer"},{"attributes":{"label":{"value":"A"},"renderers":[{"id":"eb191ccb-6da6-484a-b861-478aa679ef38","type":"GlyphRenderer"}]},"id":"a411bc85-8f5e-4257-a077-961459e230b5","type":"LegendItem"},{"attributes":{"callback":null,"end":80.2,"start":52.02},"id":"1add6815-978f-486c-973a-d6897737078d","type":"Range1d"},{"attributes":{"line_alpha":0.1,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"535f4154-611c-4e1d-b6dd-41877cc051de","type":"Line"},{"attributes":{},"id":"ec599ed2-0b12-4908-a63c-b4a967e6316b","type":"CategoricalScale"},{"attributes":{"line_color":"#6A5ACD","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"2bf00859-d5ec-4576-addc-10329ad289f4","type":"Line"},{"attributes":{"source":{"id":"32b8a6a8-a9c1-42f5-9a35-26e1168c96d7","type":"ColumnDataSource"}},"id":"8f325110-fabe-4aed-87df-9035db7cd225","type":"CDSView"},{"attributes":{},"id":"ce6d8572-c6af-40ad-b3d7-237fbd10824f","type":"CategoricalTickFormatter"},{"attributes":{},"id":"e80a1ea2-e730-4fdc-b67a-4ac0e317812e","type":"CategoricalTicker"},{"attributes":{"callback":null,"column_names":["Date","Price"],"data":{"Date":["2018-01-02","2018-01-03","2018-01-04","2018-01-05","2018-01-08","2018-01-09","2018-01-10","2018-01-11","2018-01-12","2018-01-16","2018-01-17","2018-01-18","2018-01-19","2018-01-22","2018-01-23","2018-01-24","2018-01-25","2018-01-26","2018-01-29","2018-01-30","2018-01-31"],"Price":{"__ndarray__":"9ihcj8KVS0AAAAAAAEBLQJqZmZmZWUtA7FG4HoULS0AAAAAAAIBLQJqZmZmZGUtA9ihcj8IVTEAUrkfhenRMQOF6FK5HYUxAH4XrUbgeTEAfhetRuH5MQAAAAAAAgEpAzczMzMyMSkC4HoXrUXhKQB+F61G4PkpAZmZmZmamSkCuR+F6FI5KQAAAAAAAAEtAH4XrUbg+S0DD9Shcj0JKQMP1KFyPAkpA","dtype":"float64","shape":[21]}}},"id":"32b8a6a8-a9c1-42f5-9a35-26e1168c96d7","type":"ColumnDataSource"},{"attributes":{"axis_label":"Stock Input","bounds":"auto","formatter":{"id":"c9f239e1-025b-45f8-bd8c-daf3e4960b1e","type":"BasicTickFormatter"},"major_label_orientation":"horizontal","plot":{"id":"bea70512-44fb-4fca-b26b-a9fa5149491b","subtype":"Figure","type":"Plot"},"ticker":{"id":"052a8ffa-c29b-43c6-90ec-0a2bc59be61f","type":"BasicTicker"}},"id":"806e9874-dd34-44df-ba61-bc1ec0601684","type":"LinearAxis"},{"attributes":{"grid_line_color":{"value":null},"plot":{"id":"bea70512-44fb-4fca-b26b-a9fa5149491b","subtype":"Figure","type":"Plot"},"ticker":{"id":"e80a1ea2-e730-4fdc-b67a-4ac0e317812e","type":"CategoricalTicker"}},"id":"6db9c682-5a6b-4f17-bad5-fb786a0d3855","type":"Grid"},{"attributes":{"source":{"id":"4d455555-db12-46e5-9296-1ff9c1b485fa","type":"ColumnDataSource"}},"id":"8733ff97-a7d1-47a1-b99d-882dc19f4656","type":"CDSView"},{"attributes":{"line_alpha":0.2,"line_color":"#CD5C5C","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"b31c8a6c-be59-40a8-8365-fee95bd29e83","type":"Line"},{"attributes":{"line_alpha":0.1,"line_color":"#FF7F50","line_width":2,"x":{"field":"Date"},"y":{"field":"Price"}},"id":"3103a4f4-c6a1-4ed2-9a0f-3ca4a19c304a","type":"Line"},{"attributes":{},"id":"7c972568-3d3c-4aad-9bb1-5d82a909220d","type":"ResetTool"},{"attributes":{},"id":"f66c1f40-6618-4a5d-b468-ed7874b80fdb","type":"WheelZoomTool"},{"attributes":{"active_drag":"auto","active_inspect":"auto","active_scroll":"auto","active_tap":"auto","tools":[{"id":"f9628133-a0b8-4cd8-bcd4-9c1606cb5f57","type":"SaveTool"},{"id":"8a832788-ef55-40ac-aba7-2c67368644ed","type":"PanTool"},{"id":"f66c1f40-6618-4a5d-b468-ed7874b80fdb","type":"WheelZoomTool"},{"id":"dc8f43c0-7e1e-4a16-a67f-75586663be98","type":"BoxZoomTool"},{"id":"7c972568-3d3c-4aad-9bb1-5d82a909220d","type":"ResetTool"}]},"id":"9bcfeadc-11d3-4046-88ad-81072722750a","type":"Toolbar"},{"attributes":{"bottom_units":"screen","fill_alpha":{"value":0.5},"fill_color":{"value":"lightgrey"},"left_units":"screen","level":"overlay","line_alpha":{"value":1.0},"line_color":{"value":"black"},"line_dash":[4,4],"line_width":{"value":2},"plot":null,"render_mode":"css","right_units":"screen","top_units":"screen"},"id":"9d8190b1-d437-43fe-a50a-fd11f4462549","type":"BoxAnnotation"}],"root_ids":["bea70512-44fb-4fca-b26b-a9fa5149491b"]},"title":"Bokeh Application","version":"0.12.13"}};
  var render_items = [{"docid":"536dfeaf-3a35-41b7-8390-604c85001cf5","elementid":"c7e9efe7-ca23-4b56-abb5-dfe832bd15c5","modelid":"bea70512-44fb-4fca-b26b-a9fa5149491b"}];
  root.Bokeh.embed.embed_items_notebook(docs_json, render_items);

  }
  if (root.Bokeh !== undefined) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (root.Bokeh !== undefined) {
        embed_document(root);
        clearInterval(timer);
      }
      attempts++;
      if (attempts > 100) {
        console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing")
        clearInterval(timer);
      }
    }, 10, root)
  }
})(window);
</script>
</div>




```python
#JUMP TO LINE 34 FOR ADDITIONAL SUMMARY STATISTICS AND GRAPH VISUALIZATION
```


```python
#################################################################################################################################
```


```python
#3.1.B) OBTAIN A DATAFRAME OF CLOSING, OPENING, ADJUSTED CLOSING AND ADJUSTED OPENING PRICRES FROM THE LAST MONTH FOR EACH TICKER

#Select last  month prices

ticker_col=ticker_data['columns']
ticker1=ticker_data['data'][4557:4578]
ticker2=ticker_data['data'][4872:4893]
ticker3=ticker_data['data'][7981:8002]
ticker4=ticker_data['data'][9274:9292]

import pandas
df1=pandas.DataFrame.from_dict(ticker1, orient='columns')
df1.drop(df1.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df1.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
df2=pandas.DataFrame.from_dict(ticker2, orient='columns')
df2.drop(df2.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df2.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
df3=pandas.DataFrame.from_dict(ticker3, orient='columns')
df3.drop(df3.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df3.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
df4=pandas.DataFrame.from_dict(ticker4, orient='columns')
df4.drop(df4.columns[[3,4,6,7,8,10,11,13]], axis=1, inplace=True)
df4.columns = ['Ticker', 'Date', 'Open Price', 'Close Price','Adj Open Price', 'Adj Close Price']
dfs = [df1, df2, df3, df4]
dfs = pd.concat(dfs)
dfs

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ticker</th>
      <th>Date</th>
      <th>Open Price</th>
      <th>Close Price</th>
      <th>Adj Open Price</th>
      <th>Adj Close Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>2018-01-02</td>
      <td>67.4200</td>
      <td>67.6000</td>
      <td>67.4200</td>
      <td>67.6000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>2018-01-03</td>
      <td>67.6200</td>
      <td>69.3200</td>
      <td>67.6200</td>
      <td>69.3200</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>2018-01-04</td>
      <td>69.5400</td>
      <td>68.8000</td>
      <td>69.5400</td>
      <td>68.8000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A</td>
      <td>2018-01-05</td>
      <td>68.7300</td>
      <td>69.9000</td>
      <td>68.7300</td>
      <td>69.9000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A</td>
      <td>2018-01-08</td>
      <td>69.7300</td>
      <td>70.0500</td>
      <td>69.7300</td>
      <td>70.0500</td>
    </tr>
    <tr>
      <th>5</th>
      <td>A</td>
      <td>2018-01-09</td>
      <td>70.6800</td>
      <td>71.7700</td>
      <td>70.6800</td>
      <td>71.7700</td>
    </tr>
    <tr>
      <th>6</th>
      <td>A</td>
      <td>2018-01-10</td>
      <td>71.4500</td>
      <td>70.7900</td>
      <td>71.4500</td>
      <td>70.7900</td>
    </tr>
    <tr>
      <th>7</th>
      <td>A</td>
      <td>2018-01-11</td>
      <td>70.9200</td>
      <td>70.8000</td>
      <td>70.9200</td>
      <td>70.8000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>A</td>
      <td>2018-01-12</td>
      <td>70.7300</td>
      <td>71.7300</td>
      <td>70.7300</td>
      <td>71.7300</td>
    </tr>
    <tr>
      <th>9</th>
      <td>A</td>
      <td>2018-01-16</td>
      <td>72.0200</td>
      <td>71.2300</td>
      <td>72.0200</td>
      <td>71.2300</td>
    </tr>
    <tr>
      <th>10</th>
      <td>A</td>
      <td>2018-01-17</td>
      <td>71.7200</td>
      <td>72.0600</td>
      <td>71.7200</td>
      <td>72.0600</td>
    </tr>
    <tr>
      <th>11</th>
      <td>A</td>
      <td>2018-01-18</td>
      <td>72.2000</td>
      <td>72.1900</td>
      <td>72.2000</td>
      <td>72.1900</td>
    </tr>
    <tr>
      <th>12</th>
      <td>A</td>
      <td>2018-01-19</td>
      <td>72.4800</td>
      <td>73.0700</td>
      <td>72.4800</td>
      <td>73.0700</td>
    </tr>
    <tr>
      <th>13</th>
      <td>A</td>
      <td>2018-01-22</td>
      <td>73.1700</td>
      <td>73.4800</td>
      <td>73.1700</td>
      <td>73.4800</td>
    </tr>
    <tr>
      <th>14</th>
      <td>A</td>
      <td>2018-01-23</td>
      <td>74.0500</td>
      <td>73.4400</td>
      <td>74.0500</td>
      <td>73.4400</td>
    </tr>
    <tr>
      <th>15</th>
      <td>A</td>
      <td>2018-01-24</td>
      <td>73.6600</td>
      <td>73.5800</td>
      <td>73.6600</td>
      <td>73.5800</td>
    </tr>
    <tr>
      <th>16</th>
      <td>A</td>
      <td>2018-01-25</td>
      <td>74.1700</td>
      <td>73.8600</td>
      <td>74.1700</td>
      <td>73.8600</td>
    </tr>
    <tr>
      <th>17</th>
      <td>A</td>
      <td>2018-01-26</td>
      <td>74.3000</td>
      <td>74.8200</td>
      <td>74.3000</td>
      <td>74.8200</td>
    </tr>
    <tr>
      <th>18</th>
      <td>A</td>
      <td>2018-01-29</td>
      <td>74.4800</td>
      <td>74.5300</td>
      <td>74.4800</td>
      <td>74.5300</td>
    </tr>
    <tr>
      <th>19</th>
      <td>A</td>
      <td>2018-01-30</td>
      <td>73.9900</td>
      <td>72.9900</td>
      <td>73.9900</td>
      <td>72.9900</td>
    </tr>
    <tr>
      <th>20</th>
      <td>A</td>
      <td>2018-01-31</td>
      <td>73.7700</td>
      <td>73.4300</td>
      <td>73.7700</td>
      <td>73.4300</td>
    </tr>
    <tr>
      <th>0</th>
      <td>AA</td>
      <td>2018-01-02</td>
      <td>54.0600</td>
      <td>55.1700</td>
      <td>54.0600</td>
      <td>55.1700</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AA</td>
      <td>2018-01-03</td>
      <td>54.9200</td>
      <td>54.5000</td>
      <td>54.9200</td>
      <td>54.5000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AA</td>
      <td>2018-01-04</td>
      <td>54.8100</td>
      <td>54.7000</td>
      <td>54.8100</td>
      <td>54.7000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AA</td>
      <td>2018-01-05</td>
      <td>54.6500</td>
      <td>54.0900</td>
      <td>54.6500</td>
      <td>54.0900</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AA</td>
      <td>2018-01-08</td>
      <td>53.9600</td>
      <td>55.0000</td>
      <td>53.9600</td>
      <td>55.0000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>AA</td>
      <td>2018-01-09</td>
      <td>55.0000</td>
      <td>54.2000</td>
      <td>55.0000</td>
      <td>54.2000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>AA</td>
      <td>2018-01-10</td>
      <td>54.3700</td>
      <td>56.1700</td>
      <td>54.3700</td>
      <td>56.1700</td>
    </tr>
    <tr>
      <th>7</th>
      <td>AA</td>
      <td>2018-01-11</td>
      <td>56.6000</td>
      <td>56.9100</td>
      <td>56.6000</td>
      <td>56.9100</td>
    </tr>
    <tr>
      <th>8</th>
      <td>AA</td>
      <td>2018-01-12</td>
      <td>57.0500</td>
      <td>56.7600</td>
      <td>57.0500</td>
      <td>56.7600</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>AAL</td>
      <td>2018-01-16</td>
      <td>58.7900</td>
      <td>57.9850</td>
      <td>58.7900</td>
      <td>57.9850</td>
    </tr>
    <tr>
      <th>10</th>
      <td>AAL</td>
      <td>2018-01-17</td>
      <td>58.3100</td>
      <td>58.1600</td>
      <td>58.3100</td>
      <td>58.1600</td>
    </tr>
    <tr>
      <th>11</th>
      <td>AAL</td>
      <td>2018-01-18</td>
      <td>58.0000</td>
      <td>58.3400</td>
      <td>58.0000</td>
      <td>58.3400</td>
    </tr>
    <tr>
      <th>12</th>
      <td>AAL</td>
      <td>2018-01-19</td>
      <td>58.5900</td>
      <td>58.0600</td>
      <td>58.5900</td>
      <td>58.0600</td>
    </tr>
    <tr>
      <th>13</th>
      <td>AAL</td>
      <td>2018-01-22</td>
      <td>57.9900</td>
      <td>58.1000</td>
      <td>57.9900</td>
      <td>58.1000</td>
    </tr>
    <tr>
      <th>14</th>
      <td>AAL</td>
      <td>2018-01-23</td>
      <td>57.7400</td>
      <td>58.2900</td>
      <td>57.7400</td>
      <td>58.2900</td>
    </tr>
    <tr>
      <th>15</th>
      <td>AAL</td>
      <td>2018-01-24</td>
      <td>54.3500</td>
      <td>54.7900</td>
      <td>54.3500</td>
      <td>54.7900</td>
    </tr>
    <tr>
      <th>16</th>
      <td>AAL</td>
      <td>2018-01-25</td>
      <td>54.0000</td>
      <td>53.0500</td>
      <td>54.0000</td>
      <td>53.0500</td>
    </tr>
    <tr>
      <th>17</th>
      <td>AAL</td>
      <td>2018-01-26</td>
      <td>53.6500</td>
      <td>53.0700</td>
      <td>53.6500</td>
      <td>53.0700</td>
    </tr>
    <tr>
      <th>18</th>
      <td>AAL</td>
      <td>2018-01-29</td>
      <td>52.7900</td>
      <td>52.6800</td>
      <td>52.7900</td>
      <td>52.6800</td>
    </tr>
    <tr>
      <th>19</th>
      <td>AAL</td>
      <td>2018-01-30</td>
      <td>52.4500</td>
      <td>52.5900</td>
      <td>52.4500</td>
      <td>52.5900</td>
    </tr>
    <tr>
      <th>20</th>
      <td>AAL</td>
      <td>2018-01-31</td>
      <td>53.0800</td>
      <td>54.3200</td>
      <td>53.0800</td>
      <td>54.3200</td>
    </tr>
    <tr>
      <th>0</th>
      <td>AAMC</td>
      <td>2018-01-03</td>
      <td>77.9500</td>
      <td>77.9500</td>
      <td>77.9500</td>
      <td>77.9500</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AAMC</td>
      <td>2018-01-04</td>
      <td>80.2000</td>
      <td>80.2000</td>
      <td>80.2000</td>
      <td>80.2000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AAMC</td>
      <td>2018-01-05</td>
      <td>80.2000</td>
      <td>80.2000</td>
      <td>80.2000</td>
      <td>80.2000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AAMC</td>
      <td>2018-01-08</td>
      <td>80.2000</td>
      <td>80.2000</td>
      <td>80.2000</td>
      <td>80.2000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AAMC</td>
      <td>2018-01-09</td>
      <td>79.0000</td>
      <td>79.0000</td>
      <td>79.0000</td>
      <td>79.0000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>AAMC</td>
      <td>2018-01-10</td>
      <td>79.0000</td>
      <td>79.0000</td>
      <td>79.0000</td>
      <td>79.0000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>AAMC</td>
      <td>2018-01-11</td>
      <td>79.9900</td>
      <td>79.9900</td>
      <td>79.9900</td>
      <td>79.9900</td>
    </tr>
    <tr>
      <th>7</th>
      <td>AAMC</td>
      <td>2018-01-16</td>
      <td>75.9500</td>
      <td>75.9500</td>
      <td>75.9500</td>
      <td>75.9500</td>
    </tr>
    <tr>
      <th>8</th>
      <td>AAMC</td>
      <td>2018-01-17</td>
      <td>71.5010</td>
      <td>71.5010</td>
      <td>71.5010</td>
      <td>71.5010</td>
    </tr>
    <tr>
      <th>9</th>
      <td>AAMC</td>
      <td>2018-01-18</td>
      <td>71.5010</td>
      <td>71.5010</td>
      <td>71.5010</td>
      <td>71.5010</td>
    </tr>
    <tr>
      <th>10</th>
      <td>AAMC</td>
      <td>2018-01-22</td>
      <td>69.4000</td>
      <td>66.1803</td>
      <td>69.4000</td>
      <td>66.1803</td>
    </tr>
    <tr>
      <th>11</th>
      <td>AAMC</td>
      <td>2018-01-23</td>
      <td>67.7000</td>
      <td>67.7000</td>
      <td>67.7000</td>
      <td>67.7000</td>
    </tr>
    <tr>
      <th>12</th>
      <td>AAMC</td>
      <td>2018-01-24</td>
      <td>69.6500</td>
      <td>69.6647</td>
      <td>69.6500</td>
      <td>69.6647</td>
    </tr>
    <tr>
      <th>13</th>
      <td>AAMC</td>
      <td>2018-01-25</td>
      <td>69.6647</td>
      <td>69.6647</td>
      <td>69.6647</td>
      <td>69.6647</td>
    </tr>
    <tr>
      <th>14</th>
      <td>AAMC</td>
      <td>2018-01-26</td>
      <td>67.9000</td>
      <td>68.1500</td>
      <td>67.9000</td>
      <td>68.1500</td>
    </tr>
    <tr>
      <th>15</th>
      <td>AAMC</td>
      <td>2018-01-29</td>
      <td>68.1500</td>
      <td>68.1500</td>
      <td>68.1500</td>
      <td>68.1500</td>
    </tr>
    <tr>
      <th>16</th>
      <td>AAMC</td>
      <td>2018-01-30</td>
      <td>66.9500</td>
      <td>69.0241</td>
      <td>66.9500</td>
      <td>69.0241</td>
    </tr>
    <tr>
      <th>17</th>
      <td>AAMC</td>
      <td>2018-01-31</td>
      <td>69.0241</td>
      <td>69.0241</td>
      <td>69.0241</td>
      <td>69.0241</td>
    </tr>
  </tbody>
</table>
<p>81 rows × 6 columns</p>
</div>




```python
#Create a new dataframe 'Date' from previous dataframe that will be used as an index

dfsd=dfs.loc[:, 'Date']
dfsd1=dfsd.drop_duplicates()
dfsd1
```




    0     2018-01-02
    1     2018-01-03
    2     2018-01-04
    3     2018-01-05
    4     2018-01-08
    5     2018-01-09
    6     2018-01-10
    7     2018-01-11
    8     2018-01-12
    9     2018-01-16
    10    2018-01-17
    11    2018-01-18
    12    2018-01-19
    13    2018-01-22
    14    2018-01-23
    15    2018-01-24
    16    2018-01-25
    17    2018-01-26
    18    2018-01-29
    19    2018-01-30
    20    2018-01-31
    Name: Date, dtype: object




```python
#Re-order the columns in the dataframe:

#1.  Assign multi-index columns from tuples

multicols = pd.MultiIndex.from_tuples([('A','Open Price'),('A','Close Price'),('A','Adj Open Price'),('A','Adj Close Price'),
                                       ('AA','Open Price'),('AA','Close Price'),('AA','Adj Open Price'),('AA','Adj Close Price'),
                                       ('AAL','Open Price'),('AAL','Close Price'),('AAL','Adj Open Price'),('AAL','Adj Close Price'),
                                       ('AAMC','Open Price'),('AAMC','Close Price'),('AAMC','Adj Open Price'),('AAMC','Adj Close Price')],
                                       names=['Ticker', 'Price'])

#2. Create an empty dataframe using the former newly created 'Date' index and the multi-index columns from step 1

index = dfsd1
out = pd.DataFrame(index=index,columns=multicols).sort_index().sort_index(axis=1)
out
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Ticker</th>
      <th colspan="4" halign="left">A</th>
      <th colspan="4" halign="left">AA</th>
      <th colspan="4" halign="left">AAL</th>
      <th colspan="4" halign="left">AAMC</th>
    </tr>
    <tr>
      <th>Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-01-02</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-03</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-04</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-05</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-08</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-09</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-10</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-11</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-12</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-16</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-17</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-18</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-19</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-22</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-23</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-24</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-25</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-26</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-29</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-30</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2018-01-31</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
dfs['Open Price'] = dfs['Open Price'].fillna(dfs['Open Price'].mean())
dfs['Close Price'] = dfs['Close Price'].fillna(dfs['Close Price'].mean())
dfs['Adj Open Price'] = dfs['Adj Open Price'].fillna(dfs['Adj Open Price'].mean())
dfs['Adj Close Price'] = dfs['Adj Close Price'].fillna(dfs['Adj Close Price'].mean())

dfs=dfs[['Open Price', 'Close Price', 'Adj Open Price', 'Adj Close Price']]
```


```python
#3. Create another dataframe based on the combined dataframes (1,2,3,4, dfs) containing the actual values of ticker prices

#Group columns  by 'Ticker' name, pivot column index rows to column and imputate missing cases

dfill = (dfs.groupby('Ticker').apply(lambda g:g.set_index('Date') [['Open Price', 'Close Price', 'Adj Open Price', 'Adj Close Price']]).unstack(level=0).fillna(dfs['Close Price'].mean()))

#Delete column and adjust the multi-index column

dfill.columns=dfill.columns.droplevel()
print dfill

```

    Ticker          A     AA    AAL       AAMC      A     AA     AAL       AAMC  \
    Date
    2018-01-02  67.42  54.06  52.33  63.298085  67.60  55.17  52.990  63.298085
    2018-01-03  67.62  54.92  52.86  77.950000  69.32  54.50  52.330  77.950000
    2018-01-04  69.54  54.81  52.48  80.200000  68.80  54.70  52.670  80.200000
    2018-01-05  68.73  54.65  52.78  80.200000  69.90  54.09  52.650  80.200000
    2018-01-08  69.73  53.96  52.60  80.200000  70.05  55.00  52.130  80.200000
    2018-01-09  70.68  55.00  52.97  79.000000  71.77  54.20  52.080  79.000000
    2018-01-10  71.45  54.37  53.23  79.000000  70.79  56.17  53.780  79.000000
    2018-01-11  70.92  56.60  54.49  79.990000  70.80  56.91  56.420  79.990000
    2018-01-12  70.73  57.05  56.56  63.298085  71.73  56.76  58.470  63.298085
    2018-01-16  72.02  56.09  58.79  75.950000  71.23  56.24  57.985  75.950000
    2018-01-17  71.72  56.03  58.31  71.501000  72.06  56.99  58.160  71.501000
    2018-01-18  72.20  53.67  58.00  71.501000  72.19  53.00  58.340  71.501000
    2018-01-19  72.48  52.86  58.59  63.298085  73.07  53.10  58.060  63.298085
    2018-01-22  73.17  52.80  57.99  69.400000  73.48  52.94  58.100  66.180300
    2018-01-23  74.05  52.34  57.74  67.700000  73.44  52.49  58.290  67.700000
    2018-01-24  73.66  52.90  54.35  69.650000  73.58  53.30  54.790  69.664700
    2018-01-25  74.17  53.74  54.00  69.664700  73.86  53.11  53.050  69.664700
    2018-01-26  74.30  53.55  53.65  67.900000  74.82  54.00  53.070  68.150000
    2018-01-29  74.48  53.89  52.79  68.150000  74.53  54.49  52.680  68.150000
    2018-01-30  73.99  53.67  52.45  66.950000  72.99  52.52  52.590  69.024100
    2018-01-31  73.77  52.75  53.08  69.024100  73.43  52.02  54.320  69.024100

    Ticker          A     AA    AAL       AAMC      A     AA     AAL       AAMC
    Date
    2018-01-02  67.42  54.06  52.33  63.298085  67.60  55.17  52.990  63.298085
    2018-01-03  67.62  54.92  52.86  77.950000  69.32  54.50  52.330  77.950000
    2018-01-04  69.54  54.81  52.48  80.200000  68.80  54.70  52.670  80.200000
    2018-01-05  68.73  54.65  52.78  80.200000  69.90  54.09  52.650  80.200000
    2018-01-08  69.73  53.96  52.60  80.200000  70.05  55.00  52.130  80.200000
    2018-01-09  70.68  55.00  52.97  79.000000  71.77  54.20  52.080  79.000000
    2018-01-10  71.45  54.37  53.23  79.000000  70.79  56.17  53.780  79.000000
    2018-01-11  70.92  56.60  54.49  79.990000  70.80  56.91  56.420  79.990000
    2018-01-12  70.73  57.05  56.56  63.298085  71.73  56.76  58.470  63.298085
    2018-01-16  72.02  56.09  58.79  75.950000  71.23  56.24  57.985  75.950000
    2018-01-17  71.72  56.03  58.31  71.501000  72.06  56.99  58.160  71.501000
    2018-01-18  72.20  53.67  58.00  71.501000  72.19  53.00  58.340  71.501000
    2018-01-19  72.48  52.86  58.59  63.298085  73.07  53.10  58.060  63.298085
    2018-01-22  73.17  52.80  57.99  69.400000  73.48  52.94  58.100  66.180300
    2018-01-23  74.05  52.34  57.74  67.700000  73.44  52.49  58.290  67.700000
    2018-01-24  73.66  52.90  54.35  69.650000  73.58  53.30  54.790  69.664700
    2018-01-25  74.17  53.74  54.00  69.664700  73.86  53.11  53.050  69.664700
    2018-01-26  74.30  53.55  53.65  67.900000  74.82  54.00  53.070  68.150000
    2018-01-29  74.48  53.89  52.79  68.150000  74.53  54.49  52.680  68.150000
    2018-01-30  73.99  53.67  52.45  66.950000  72.99  52.52  52.590  69.024100
    2018-01-31  73.77  52.75  53.08  69.024100  73.43  52.02  54.320  69.024100



```python
#Reset the indices of the two dataframes

out = out.reset_index(drop=True)
dfill = dfill.reset_index(drop=True)

#Rebuild the empty dataframe

out = pd.DataFrame(out)

#Assign length of columns and copy price values within each price category and ticker from one to another dataframe

sLength = len(out['A'])
out['A']= dfill['A'].values
out['AA']= dfill['AA'].values
out['AAL']= dfill['AAL'].values
out['AAMC']= dfill['AAMC'].values

```


```python
#Add the column 'Date' indexed in the dataframe

out['Date'] = dfsd1
out
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Ticker</th>
      <th colspan="4" halign="left">A</th>
      <th colspan="4" halign="left">AA</th>
      <th colspan="4" halign="left">AAL</th>
      <th colspan="4" halign="left">AAMC</th>
      <th>Date</th>
    </tr>
    <tr>
      <th>Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>67.42</td>
      <td>67.60</td>
      <td>67.42</td>
      <td>67.60</td>
      <td>54.06</td>
      <td>55.17</td>
      <td>54.06</td>
      <td>55.17</td>
      <td>52.33</td>
      <td>52.990</td>
      <td>52.33</td>
      <td>52.990</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>2018-01-02</td>
    </tr>
    <tr>
      <th>1</th>
      <td>67.62</td>
      <td>69.32</td>
      <td>67.62</td>
      <td>69.32</td>
      <td>54.92</td>
      <td>54.50</td>
      <td>54.92</td>
      <td>54.50</td>
      <td>52.86</td>
      <td>52.330</td>
      <td>52.86</td>
      <td>52.330</td>
      <td>77.950000</td>
      <td>77.950000</td>
      <td>77.950000</td>
      <td>77.950000</td>
      <td>2018-01-03</td>
    </tr>
    <tr>
      <th>2</th>
      <td>69.54</td>
      <td>68.80</td>
      <td>69.54</td>
      <td>68.80</td>
      <td>54.81</td>
      <td>54.70</td>
      <td>54.81</td>
      <td>54.70</td>
      <td>52.48</td>
      <td>52.670</td>
      <td>52.48</td>
      <td>52.670</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>2018-01-04</td>
    </tr>
    <tr>
      <th>3</th>
      <td>68.73</td>
      <td>69.90</td>
      <td>68.73</td>
      <td>69.90</td>
      <td>54.65</td>
      <td>54.09</td>
      <td>54.65</td>
      <td>54.09</td>
      <td>52.78</td>
      <td>52.650</td>
      <td>52.78</td>
      <td>52.650</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>2018-01-05</td>
    </tr>
    <tr>
      <th>4</th>
      <td>69.73</td>
      <td>70.05</td>
      <td>69.73</td>
      <td>70.05</td>
      <td>53.96</td>
      <td>55.00</td>
      <td>53.96</td>
      <td>55.00</td>
      <td>52.60</td>
      <td>52.130</td>
      <td>52.60</td>
      <td>52.130</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>2018-01-08</td>
    </tr>
    <tr>
      <th>5</th>
      <td>70.68</td>
      <td>71.77</td>
      <td>70.68</td>
      <td>71.77</td>
      <td>55.00</td>
      <td>54.20</td>
      <td>55.00</td>
      <td>54.20</td>
      <td>52.97</td>
      <td>52.080</td>
      <td>52.97</td>
      <td>52.080</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>2018-01-09</td>
    </tr>
    <tr>
      <th>6</th>
      <td>71.45</td>
      <td>70.79</td>
      <td>71.45</td>
      <td>70.79</td>
      <td>54.37</td>
      <td>56.17</td>
      <td>54.37</td>
      <td>56.17</td>
      <td>53.23</td>
      <td>53.780</td>
      <td>53.23</td>
      <td>53.780</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>2018-01-10</td>
    </tr>
    <tr>
      <th>7</th>
      <td>70.92</td>
      <td>70.80</td>
      <td>70.92</td>
      <td>70.80</td>
      <td>56.60</td>
      <td>56.91</td>
      <td>56.60</td>
      <td>56.91</td>
      <td>54.49</td>
      <td>56.420</td>
      <td>54.49</td>
      <td>56.420</td>
      <td>79.990000</td>
      <td>79.990000</td>
      <td>79.990000</td>
      <td>79.990000</td>
      <td>2018-01-11</td>
    </tr>
    <tr>
      <th>8</th>
      <td>70.73</td>
      <td>71.73</td>
      <td>70.73</td>
      <td>71.73</td>
      <td>57.05</td>
      <td>56.76</td>
      <td>57.05</td>
      <td>56.76</td>
      <td>56.56</td>
      <td>58.470</td>
      <td>56.56</td>
      <td>58.470</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>2018-01-12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>72.02</td>
      <td>71.23</td>
      <td>72.02</td>
      <td>71.23</td>
      <td>56.09</td>
      <td>56.24</td>
      <td>56.09</td>
      <td>56.24</td>
      <td>58.79</td>
      <td>57.985</td>
      <td>58.79</td>
      <td>57.985</td>
      <td>75.950000</td>
      <td>75.950000</td>
      <td>75.950000</td>
      <td>75.950000</td>
      <td>2018-01-16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>71.72</td>
      <td>72.06</td>
      <td>71.72</td>
      <td>72.06</td>
      <td>56.03</td>
      <td>56.99</td>
      <td>56.03</td>
      <td>56.99</td>
      <td>58.31</td>
      <td>58.160</td>
      <td>58.31</td>
      <td>58.160</td>
      <td>71.501000</td>
      <td>71.501000</td>
      <td>71.501000</td>
      <td>71.501000</td>
      <td>2018-01-17</td>
    </tr>
    <tr>
      <th>11</th>
      <td>72.20</td>
      <td>72.19</td>
      <td>72.20</td>
      <td>72.19</td>
      <td>53.67</td>
      <td>53.00</td>
      <td>53.67</td>
      <td>53.00</td>
      <td>58.00</td>
      <td>58.340</td>
      <td>58.00</td>
      <td>58.340</td>
      <td>71.501000</td>
      <td>71.501000</td>
      <td>71.501000</td>
      <td>71.501000</td>
      <td>2018-01-18</td>
    </tr>
    <tr>
      <th>12</th>
      <td>72.48</td>
      <td>73.07</td>
      <td>72.48</td>
      <td>73.07</td>
      <td>52.86</td>
      <td>53.10</td>
      <td>52.86</td>
      <td>53.10</td>
      <td>58.59</td>
      <td>58.060</td>
      <td>58.59</td>
      <td>58.060</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>2018-01-19</td>
    </tr>
    <tr>
      <th>13</th>
      <td>73.17</td>
      <td>73.48</td>
      <td>73.17</td>
      <td>73.48</td>
      <td>52.80</td>
      <td>52.94</td>
      <td>52.80</td>
      <td>52.94</td>
      <td>57.99</td>
      <td>58.100</td>
      <td>57.99</td>
      <td>58.100</td>
      <td>69.400000</td>
      <td>66.180300</td>
      <td>69.400000</td>
      <td>66.180300</td>
      <td>2018-01-22</td>
    </tr>
    <tr>
      <th>14</th>
      <td>74.05</td>
      <td>73.44</td>
      <td>74.05</td>
      <td>73.44</td>
      <td>52.34</td>
      <td>52.49</td>
      <td>52.34</td>
      <td>52.49</td>
      <td>57.74</td>
      <td>58.290</td>
      <td>57.74</td>
      <td>58.290</td>
      <td>67.700000</td>
      <td>67.700000</td>
      <td>67.700000</td>
      <td>67.700000</td>
      <td>2018-01-23</td>
    </tr>
    <tr>
      <th>15</th>
      <td>73.66</td>
      <td>73.58</td>
      <td>73.66</td>
      <td>73.58</td>
      <td>52.90</td>
      <td>53.30</td>
      <td>52.90</td>
      <td>53.30</td>
      <td>54.35</td>
      <td>54.790</td>
      <td>54.35</td>
      <td>54.790</td>
      <td>69.650000</td>
      <td>69.664700</td>
      <td>69.650000</td>
      <td>69.664700</td>
      <td>2018-01-24</td>
    </tr>
    <tr>
      <th>16</th>
      <td>74.17</td>
      <td>73.86</td>
      <td>74.17</td>
      <td>73.86</td>
      <td>53.74</td>
      <td>53.11</td>
      <td>53.74</td>
      <td>53.11</td>
      <td>54.00</td>
      <td>53.050</td>
      <td>54.00</td>
      <td>53.050</td>
      <td>69.664700</td>
      <td>69.664700</td>
      <td>69.664700</td>
      <td>69.664700</td>
      <td>2018-01-25</td>
    </tr>
    <tr>
      <th>17</th>
      <td>74.30</td>
      <td>74.82</td>
      <td>74.30</td>
      <td>74.82</td>
      <td>53.55</td>
      <td>54.00</td>
      <td>53.55</td>
      <td>54.00</td>
      <td>53.65</td>
      <td>53.070</td>
      <td>53.65</td>
      <td>53.070</td>
      <td>67.900000</td>
      <td>68.150000</td>
      <td>67.900000</td>
      <td>68.150000</td>
      <td>2018-01-26</td>
    </tr>
    <tr>
      <th>18</th>
      <td>74.48</td>
      <td>74.53</td>
      <td>74.48</td>
      <td>74.53</td>
      <td>53.89</td>
      <td>54.49</td>
      <td>53.89</td>
      <td>54.49</td>
      <td>52.79</td>
      <td>52.680</td>
      <td>52.79</td>
      <td>52.680</td>
      <td>68.150000</td>
      <td>68.150000</td>
      <td>68.150000</td>
      <td>68.150000</td>
      <td>2018-01-29</td>
    </tr>
    <tr>
      <th>19</th>
      <td>73.99</td>
      <td>72.99</td>
      <td>73.99</td>
      <td>72.99</td>
      <td>53.67</td>
      <td>52.52</td>
      <td>53.67</td>
      <td>52.52</td>
      <td>52.45</td>
      <td>52.590</td>
      <td>52.45</td>
      <td>52.590</td>
      <td>66.950000</td>
      <td>69.024100</td>
      <td>66.950000</td>
      <td>69.024100</td>
      <td>2018-01-30</td>
    </tr>
    <tr>
      <th>20</th>
      <td>73.77</td>
      <td>73.43</td>
      <td>73.77</td>
      <td>73.43</td>
      <td>52.75</td>
      <td>52.02</td>
      <td>52.75</td>
      <td>52.02</td>
      <td>53.08</td>
      <td>54.320</td>
      <td>53.08</td>
      <td>54.320</td>
      <td>69.024100</td>
      <td>69.024100</td>
      <td>69.024100</td>
      <td>69.024100</td>
      <td>2018-01-31</td>
    </tr>
  </tbody>
</table>
</div>




```python
out.describe()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Ticker</th>
      <th colspan="4" halign="left">A</th>
      <th colspan="4" halign="left">AA</th>
      <th colspan="4" halign="left">AAL</th>
      <th colspan="4" halign="left">AAMC</th>
    </tr>
    <tr>
      <th>Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
      <th>Adj Close Price</th>
      <th>Adj Open Price</th>
      <th>Close Price</th>
      <th>Open Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
      <td>21.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>71.753810</td>
      <td>71.878095</td>
      <td>71.753810</td>
      <td>71.878095</td>
      <td>54.271905</td>
      <td>54.366667</td>
      <td>54.271905</td>
      <td>54.366667</td>
      <td>54.763810</td>
      <td>54.902619</td>
      <td>54.763810</td>
      <td>54.902619</td>
      <td>72.086907</td>
      <td>72.044960</td>
      <td>72.086907</td>
      <td>72.044960</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2.208258</td>
      <td>1.963269</td>
      <td>2.208258</td>
      <td>1.963269</td>
      <td>1.319730</td>
      <td>1.548106</td>
      <td>1.319730</td>
      <td>1.548106</td>
      <td>2.444354</td>
      <td>2.581703</td>
      <td>2.444354</td>
      <td>2.581703</td>
      <td>6.100375</td>
      <td>6.135201</td>
      <td>6.100375</td>
      <td>6.135201</td>
    </tr>
    <tr>
      <th>min</th>
      <td>67.420000</td>
      <td>67.600000</td>
      <td>67.420000</td>
      <td>67.600000</td>
      <td>52.340000</td>
      <td>52.020000</td>
      <td>52.340000</td>
      <td>52.020000</td>
      <td>52.330000</td>
      <td>52.080000</td>
      <td>52.330000</td>
      <td>52.080000</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
      <td>63.298085</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>70.680000</td>
      <td>70.790000</td>
      <td>70.680000</td>
      <td>70.790000</td>
      <td>53.550000</td>
      <td>53.100000</td>
      <td>53.550000</td>
      <td>53.100000</td>
      <td>52.790000</td>
      <td>52.670000</td>
      <td>52.790000</td>
      <td>52.670000</td>
      <td>67.900000</td>
      <td>68.150000</td>
      <td>67.900000</td>
      <td>68.150000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>72.020000</td>
      <td>72.060000</td>
      <td>72.020000</td>
      <td>72.060000</td>
      <td>53.960000</td>
      <td>54.200000</td>
      <td>53.960000</td>
      <td>54.200000</td>
      <td>53.650000</td>
      <td>53.780000</td>
      <td>53.650000</td>
      <td>53.780000</td>
      <td>69.664700</td>
      <td>69.664700</td>
      <td>69.664700</td>
      <td>69.664700</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>73.770000</td>
      <td>73.440000</td>
      <td>73.770000</td>
      <td>73.440000</td>
      <td>54.920000</td>
      <td>55.170000</td>
      <td>54.920000</td>
      <td>55.170000</td>
      <td>57.740000</td>
      <td>58.060000</td>
      <td>57.740000</td>
      <td>58.060000</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>79.000000</td>
      <td>79.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>74.480000</td>
      <td>74.820000</td>
      <td>74.480000</td>
      <td>74.820000</td>
      <td>57.050000</td>
      <td>56.990000</td>
      <td>57.050000</td>
      <td>56.990000</td>
      <td>58.790000</td>
      <td>58.470000</td>
      <td>58.790000</td>
      <td>58.470000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
      <td>80.200000</td>
    </tr>
  </tbody>
</table>
</div>




```python
out.columns
```




    MultiIndex(levels=[[u'A', u'AA', u'AAL', u'AAMC', u'Date'], [u'Adj Close Price', u'Adj Open Price', u'Close Price', u'Open Price', u'']],
               labels=[[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4], [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 4]],
               names=[u'Ticker', u'Price'])




```python
#FROM HERE ON THE RESULTS CHANGE DEPENDING ON WHETHER YOU CHOSE 3.1.A, 3.1.B!!!!!
################################################################################################################################
#RESULTS SUMMARY STATISTICS AND DATA PLOT
```


```python
#Show summary statistics

print out.describe()

#Calculate/plot mean-error values of each Ticker

mean = out.mean()
error = out.std()
mean
error
```

    Ticker               A                                                    AA  \
    Price  Adj Close Price Adj Open Price Close Price Open Price Adj Close Price
    count        21.000000      21.000000   21.000000  21.000000       21.000000
    mean         71.753810      71.878095   71.753810  71.878095       54.271905
    std           2.208258       1.963269    2.208258   1.963269        1.319730
    min          67.420000      67.600000   67.420000  67.600000       52.340000
    25%          70.680000      70.790000   70.680000  70.790000       53.550000
    50%          72.020000      72.060000   72.020000  72.060000       53.960000
    75%          73.770000      73.440000   73.770000  73.440000       54.920000
    max          74.480000      74.820000   74.480000  74.820000       57.050000

    Ticker                                                   AAL                 \
    Price  Adj Open Price Close Price Open Price Adj Close Price Adj Open Price
    count       21.000000   21.000000  21.000000       21.000000      21.000000
    mean        54.366667   54.271905  54.366667       54.763810      54.902619
    std          1.548106    1.319730   1.548106        2.444354       2.581703
    min         52.020000   52.340000  52.020000       52.330000      52.080000
    25%         53.100000   53.550000  53.100000       52.790000      52.670000
    50%         54.200000   53.960000  54.200000       53.650000      53.780000
    75%         55.170000   54.920000  55.170000       57.740000      58.060000
    max         56.990000   57.050000  56.990000       58.790000      58.470000

    Ticker                                   AAMC                             \
    Price  Close Price Open Price Adj Close Price Adj Open Price Close Price
    count    21.000000  21.000000       21.000000      21.000000   21.000000
    mean     54.763810  54.902619       72.075207      72.033259   72.075207
    std       2.444354   2.581703        6.118120       6.152761    6.118120
    min      52.330000  52.080000       63.216183      63.216183   63.216183
    25%      52.790000  52.670000       67.900000      68.150000   67.900000
    50%      53.650000  53.780000       69.664700      69.664700   69.664700
    75%      57.740000  58.060000       79.000000      79.000000   79.000000
    max      58.790000  58.470000       80.200000      80.200000   80.200000

    Ticker
    Price  Open Price
    count   21.000000
    mean    72.033259
    std      6.152761
    min     63.216183
    25%     68.150000
    50%     69.664700
    75%     79.000000
    max     80.200000





    Ticker  Price
    A       Adj Close Price    2.208258
            Adj Open Price     1.963269
            Close Price        2.208258
            Open Price         1.963269
    AA      Adj Close Price    1.319730
            Adj Open Price     1.548106
            Close Price        1.319730
            Open Price         1.548106
    AAL     Adj Close Price    2.444354
            Adj Open Price     2.581703
            Close Price        2.444354
            Open Price         2.581703
    AAMC    Adj Close Price    6.118120
            Adj Open Price     6.152761
            Close Price        6.118120
            Open Price         6.152761
    dtype: float64




```python
#Mean+Error bar plot

fig, ax = plt.subplots()
mean.plot.bar(yerr=error, ax=ax)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fb65c320390>




![png](MILESTONE/images/output_86_1.png)



```python
out.plot.area(stacked=False,figsize=(11, 8))
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fb65c038dd0>




![png](MILESTONE/images/output_87_1.png)



```python
out.plot(subplots=True, figsize=(10, 10))
```




    array([<matplotlib.axes._subplots.AxesSubplot object at 0x7fb654d8a7d0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654ce2bd0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654c67dd0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb65c36c790>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb65c2c2110>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654c2f7d0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654bb0a10>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654bd54d0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654ab0650>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654a475d0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb6549b0110>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb6549342d0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654894a10>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb654818bd0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb6547970d0>,
           <matplotlib.axes._subplots.AxesSubplot object at 0x7fb65471c290>], dtype=object)




![png](MILESTONE/images/output_88_1.png)



```python
plt.figure()
out.plot(colormap=cm.cubehelix,figsize=(12, 7))
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fb65415d7d0>




    <matplotlib.figure.Figure at 0x7fb65416b790>



![png](MILESTONE/images/output_89_2.png)



```python
output_notebook()
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="9e3c67e8-17b9-444b-ad89-b46c384ad36c">Loading BokehJS ...</span>
    </div>





```python
################################################################################################################################
#3.2.SPECIFIC API REQUEST (Filter by columns 'date', 'ticker' and ticker prices)
```


```python
%matplotlib inline
import matplotlib
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 144
```


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simplejson as json
import urllib2
import requests
import ujson as json

```


```python
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from matplotlib import cm
import holoviews as hv
hv.extension('bokeh', 'matplotlib')
```





<script src="https://code.jquery.com/ui/1.10.4/jquery-ui.min.js" type="text/javascript"></script>
<script type="text/javascript">function HoloViewsWidget(){
}

HoloViewsWidget.comms = {};
HoloViewsWidget.comm_state = {};

HoloViewsWidget.prototype.init_slider = function(init_val){
  if(this.load_json) {
    this.from_json()
  } else {
    this.update_cache();
  }
}

HoloViewsWidget.prototype.populate_cache = function(idx){
  this.cache[idx].html(this.frames[idx]);
  if (this.embed) {
    delete this.frames[idx];
  }
}

HoloViewsWidget.prototype.process_error = function(msg){

}

HoloViewsWidget.prototype.from_json = function() {
  var data_url = this.json_path + this.id + '.json';
  $.getJSON(data_url, $.proxy(function(json_data) {
    this.frames = json_data;
    this.update_cache();
    this.update(0);
  }, this));
}

HoloViewsWidget.prototype.dynamic_update = function(current){
  if (current === undefined) {
    return
  }
  if(this.dynamic) {
    current = JSON.stringify(current);
  }
  function callback(initialized, msg){
    /* This callback receives data from Python as a string
       in order to parse it correctly quotes are sliced off*/
    if (msg.content.ename != undefined) {
      this.process_error(msg);
    }
    if (msg.msg_type != "execute_result") {
      console.log("Warning: HoloViews callback returned unexpected data for key: (", current, ") with the following content:", msg.content)
    } else {
      if (msg.content.data['text/plain'].includes('Complete')) {
        if (this.queue.length > 0) {
          this.time = Date.now();
          this.dynamic_update(this.queue[this.queue.length-1]);
          this.queue = [];
        } else {
          this.wait = false;
        }
        return
      }
    }
  }
  this.current = current;
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel != null)) {
    var kernel = Jupyter.notebook.kernel;
    callbacks = {iopub: {output: $.proxy(callback, this, this.initialized)}};
    var cmd = "holoviews.plotting.widgets.NdWidget.widgets['" + this.id + "'].update(" + current + ")";
    kernel.execute("import holoviews;" + cmd, callbacks, {silent : false});
  }
}

HoloViewsWidget.prototype.update_cache = function(force){
  var frame_len = Object.keys(this.frames).length;
  for (var i=0; i<frame_len; i++) {
    if(!this.load_json || this.dynamic)  {
      frame = Object.keys(this.frames)[i];
    } else {
      frame = i;
    }
    if(!(frame in this.cache) || force) {
      if ((frame in this.cache) && force) { this.cache[frame].remove() }
      this.cache[frame] = $('<div />').appendTo("#"+"_anim_img"+this.id).hide();
      var cache_id = "_anim_img"+this.id+"_"+frame;
      this.cache[frame].attr("id", cache_id);
      this.populate_cache(frame);
    }
  }
}

HoloViewsWidget.prototype.update = function(current){
  if(current in this.cache) {
    $.each(this.cache, function(index, value) {
      value.hide();
    });
    this.cache[current].show();
    this.wait = false;
  }
}

HoloViewsWidget.prototype.init_comms = function() {
  if ((window.Jupyter !== undefined) && (Jupyter.notebook.kernel !== undefined)) {
    var widget = this;
    comm_manager = Jupyter.notebook.kernel.comm_manager;
    comm_manager.register_target(this.id, function (comm) {
      comm.on_msg(function (msg) { widget.process_msg(msg) });
    });
  }
}

HoloViewsWidget.prototype.process_msg = function(msg) {
}

function SelectionWidget(frames, id, slider_ids, keyMap, dim_vals, notFound, load_json, mode, cached, json_path, dynamic){
  this.frames = frames;
  this.id = id;
  this.slider_ids = slider_ids;
  this.keyMap = keyMap
  this.current_frame = 0;
  this.current_vals = dim_vals;
  this.load_json = load_json;
  this.mode = mode;
  this.notFound = notFound;
  this.cached = cached;
  this.dynamic = dynamic;
  this.cache = {};
  this.json_path = json_path;
  this.init_slider(this.current_vals[0]);
  this.queue = [];
  this.wait = false;
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

SelectionWidget.prototype = new HoloViewsWidget;


SelectionWidget.prototype.get_key = function(current_vals) {
  var key = "(";
  for (var i=0; i<this.slider_ids.length; i++)
  {
    val = this.current_vals[i];
    if (!(typeof val === 'string')) {
      if (val % 1 === 0) { val = val.toFixed(1); }
      else { val = val.toFixed(10); val = val.slice(0, val.length-1);}
    }
    key += "'" + val + "'";
    if(i != this.slider_ids.length-1) { key += ', ';}
    else if(this.slider_ids.length == 1) { key += ',';}
  }
  key += ")";
  return this.keyMap[key];
}

SelectionWidget.prototype.set_frame = function(dim_val, dim_idx){
  this.current_vals[dim_idx] = dim_val;
  var key = this.current_vals;
  if (!this.dynamic) {
    key = this.get_key(key)
  }
  if (this.dynamic || !this.cached) {
    if ((this.time !== undefined) && ((this.wait) && ((this.time + 10000) > Date.now()))) {
      this.queue.push(key);
      return
    }
    this.queue = [];
    this.time = Date.now();
    this.current_frame = key;
    this.wait = true;
    this.dynamic_update(key)
  } else if (key !== undefined) {
    this.update(key)
  }
}


/* Define the ScrubberWidget class */
function ScrubberWidget(frames, num_frames, id, interval, load_json, mode, cached, json_path, dynamic){
  this.slider_id = "_anim_slider" + id;
  this.loop_select_id = "_anim_loop_select" + id;
  this.id = id;
  this.interval = interval;
  this.current_frame = 0;
  this.direction = 0;
  this.dynamic = dynamic;
  this.timer = null;
  this.load_json = load_json;
  this.mode = mode;
  this.cached = cached;
  this.frames = frames;
  this.cache = {};
  this.length = num_frames;
  this.json_path = json_path;
  document.getElementById(this.slider_id).max = this.length - 1;
  this.init_slider(0);
  this.wait = false;
  this.queue = [];
  if (!this.cached || this.dynamic) {
    this.init_comms()
  }
}

ScrubberWidget.prototype = new HoloViewsWidget;

ScrubberWidget.prototype.set_frame = function(frame){
  this.current_frame = frame;
  widget = document.getElementById(this.slider_id);
  if (widget === null) {
    this.pause_animation();
    return
  }
  widget.value = this.current_frame;
  if(this.cached) {
    this.update(frame)
  } else {
    this.dynamic_update(frame)
  }
}


ScrubberWidget.prototype.get_loop_state = function(){
  var button_group = document[this.loop_select_id].state;
  for (var i = 0; i < button_group.length; i++) {
    var button = button_group[i];
    if (button.checked) {
      return button.value;
    }
  }
  return undefined;
}


ScrubberWidget.prototype.next_frame = function() {
  this.set_frame(Math.min(this.length - 1, this.current_frame + 1));
}

ScrubberWidget.prototype.previous_frame = function() {
  this.set_frame(Math.max(0, this.current_frame - 1));
}

ScrubberWidget.prototype.first_frame = function() {
  this.set_frame(0);
}

ScrubberWidget.prototype.last_frame = function() {
  this.set_frame(this.length - 1);
}

ScrubberWidget.prototype.slower = function() {
  this.interval /= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.faster = function() {
  this.interval *= 0.7;
  if(this.direction > 0){this.play_animation();}
  else if(this.direction < 0){this.reverse_animation();}
}

ScrubberWidget.prototype.anim_step_forward = function() {
  if(this.current_frame < this.length - 1){
    this.next_frame();
  }else{
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.first_frame();
    }else if(loop_state == "reflect"){
      this.last_frame();
      this.reverse_animation();
    }else{
      this.pause_animation();
      this.last_frame();
    }
  }
}

ScrubberWidget.prototype.anim_step_reverse = function() {
  if(this.current_frame > 0){
    this.previous_frame();
  } else {
    var loop_state = this.get_loop_state();
    if(loop_state == "loop"){
      this.last_frame();
    }else if(loop_state == "reflect"){
      this.first_frame();
      this.play_animation();
    }else{
      this.pause_animation();
      this.first_frame();
    }
  }
}

ScrubberWidget.prototype.pause_animation = function() {
  this.direction = 0;
  if (this.timer){
    clearInterval(this.timer);
    this.timer = null;
  }
}

ScrubberWidget.prototype.play_animation = function() {
  this.pause_animation();
  this.direction = 1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_forward();}, this.interval);
}

ScrubberWidget.prototype.reverse_animation = function() {
  this.pause_animation();
  this.direction = -1;
  var t = this;
  if (!this.timer) this.timer = setInterval(function(){t.anim_step_reverse();}, this.interval);
}

function extend(destination, source) {
  for (var k in source) {
    if (source.hasOwnProperty(k)) {
      destination[k] = source[k];
    }
  }
  return destination;
}

function update_widget(widget, values) {
  if (widget.hasClass("ui-slider")) {
    widget.slider('option', {
      min: 0,
      max: values.length-1,
      dim_vals: values,
      value: 0,
      dim_labels: values
	})
    widget.slider('option', 'slide').call(widget, event, {value: 0})
  } else {
    widget.empty();
    for (var i=0; i<values.length; i++){
      widget.append($("<option>", {
        value: i,
        text: values[i]
      }))
    };
    widget.data('values', values);
    widget.data('value', 0);
    widget.trigger("change");
  };
}

// Define MPL specific subclasses
function MPLSelectionWidget() {
    SelectionWidget.apply(this, arguments);
}

function MPLScrubberWidget() {
    ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
MPLSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
MPLScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var MPLMethods = {
    init_slider : function(init_val){
        if(this.load_json) {
            this.from_json()
        } else {
            this.update_cache();
        }
        this.update(0);
        if(this.mode == 'nbagg') {
            this.set_frame(init_val, 0);
        }
    },
    populate_cache : function(idx){
        var cache_id = "_anim_img"+this.id+"_"+idx;
        this.cache[idx].html(this.frames[idx]);
        if (this.embed) {
            delete this.frames[idx];
        }
    },
    process_msg : function(msg) {
        if (!(this.mode == 'nbagg')) {
            var data = msg.content.data;
            this.frames[this.current] = data;
            this.update_cache(true);
            this.update(this.current);
        }
    }
}
// Extend MPL widgets with backend specific methods
extend(MPLSelectionWidget.prototype, MPLMethods);
extend(MPLScrubberWidget.prototype, MPLMethods);

// Define Bokeh specific subclasses
function BokehSelectionWidget() {
	SelectionWidget.apply(this, arguments);
}

function BokehScrubberWidget() {
	ScrubberWidget.apply(this, arguments);
}

// Let them inherit from the baseclasses
BokehSelectionWidget.prototype = Object.create(SelectionWidget.prototype);
BokehScrubberWidget.prototype = Object.create(ScrubberWidget.prototype);

// Define methods to override on widgets
var BokehMethods = {
	update_cache : function(){
		$.each(this.frames, $.proxy(function(index, frame) {
			this.frames[index] = JSON.parse(frame);
		}, this));
	},
	update : function(current){
		if (current === undefined) {
			var data = undefined;
		} else {
			var data = this.frames[current];
		}
		if (data !== undefined) {
			var doc = Bokeh.index[data.root].model.document;
			doc.apply_json_patch(data.content);
		}
	},
	init_comms : function() {
	}
}

// Extend Bokeh widgets with backend specific methods
extend(BokehSelectionWidget.prototype, BokehMethods);
extend(BokehScrubberWidget.prototype, BokehMethods);
</script>


<link rel="stylesheet" href="https://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<style>div.hololayout {
    display: flex;
    align-items: center;
    margin: 0;
}

div.holoframe {
	width: 75%;
}

div.holowell {
    display: flex;
    align-items: center;
    margin: 0;
}

form.holoform {
    background-color: #fafafa;
    border-radius: 5px;
    overflow: hidden;
	padding-left: 0.8em;
    padding-right: 0.8em;
    padding-top: 0.4em;
    padding-bottom: 0.4em;
}

div.holowidgets {
    padding-right: 0;
	width: 25%;
}

div.holoslider {
    min-height: 0 !important;
    height: 0.8em;
    width: 60%;
}

div.holoformgroup {
    padding-top: 0.5em;
    margin-bottom: 0.5em;
}

div.hologroup {
    padding-left: 0;
    padding-right: 0.8em;
    width: 50%;
}

.holoselect {
    width: 92%;
    margin-left: 0;
    margin-right: 0;
}

.holotext {
    width: 100%;
    padding-left:  0.5em;
    padding-right: 0;
}

.holowidgets .ui-resizable-se {
	visibility: hidden
}

.holoframe > .ui-resizable-se {
	visibility: hidden
}

.holowidgets .ui-resizable-s {
	visibility: hidden
}

div.bk-hbox {
    display: flex;
    justify-content: center;
}

div.bk-hbox div.bk-plot {
    padding: 8px;
}

div.bk-hbox div.bk-data-table {
    padding: 20px;
}
</style>


<div class="logo-block">
<img src='data:image/png;base64,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
roTBs2RqAAAAAElFTkSuQmCC'
     style='height:25px; border-radius:12px; display: inline-block; float: left; vertical-align: middle'></img>


  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



  <img src='data:image/png;base64,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'
       style='height:15px; border-radius:12px; display: inline-block; float: left'></img>



</div>




```python
#3.2.1 Either use:

import quandl
quandl.ApiConfig.api_key = 'MhSyqwHb1N6rn5JiB7QF'
dfs=quandl.get_table('WIKI/PRICES',qopts={'columns': ['ticker','date','open','close','adj_open','adj_close','date']},date='2018-1-1,2018-1-2,2018-1-3,2018-1-4,2018-1-5,2018-1-6,2018-1-7,2018-1-8,2018-1-9,2018-1-10,2018-1-11,2018-1-12,2018-1-13,2018-1-14,2018-1-15,2018-1-16,2018-1-17,2018-1-18,2018-1-19,2018-1-20,2018-1-21,2018-1-22,2018-1-23,2018-1-24,2018-1-25,2018-1-26,2018-1-27,2018-1-28,2018-1-29,2018-1-30,2018-1-31')
dfs

#3.2.2. or:

#r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?qopts.columns=ticker,date,open,close,adj_open,adj_close&date=2018-1-1,2018-1-2,2018-1-3,2018-1-4,2018-1-5,2018-1-6,2018-1-7,2018-1-8,2018-1-9,2018-1-10,2018-1-11,2018-1-12,2018-1-13,2018-1-14,2018-1-15,2018-1-16,2018-1-17,2018-1-18,2018-1-19,2018-1-20,2018-1-21,2018-1-22,2018-1-23,2018-1-24,2018-1-25,2018-1-26,2018-1-27,2018-1-28,2018-1-29,2018-1-30,2018-1-31&api_key=MhSyqwHb1N6rn5JiB7QF')
#qt = r.json()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ticker</th>
      <th>date</th>
      <th>open</th>
      <th>close</th>
      <th>adj_open</th>
      <th>adj_close</th>
    </tr>
    <tr>
      <th>None</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>2018-01-02</td>
      <td>67.42</td>
      <td>67.60</td>
      <td>67.42</td>
      <td>67.60</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>2018-01-03</td>
      <td>67.62</td>
      <td>69.32</td>
      <td>67.62</td>
      <td>69.32</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>2018-01-04</td>
      <td>69.54</td>
      <td>68.80</td>
      <td>69.54</td>
      <td>68.80</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A</td>
      <td>2018-01-05</td>
      <td>68.73</td>
      <td>69.90</td>
      <td>68.73</td>
      <td>69.90</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A</td>
      <td>2018-01-08</td>
      <td>69.73</td>
      <td>70.05</td>
      <td>69.73</td>
      <td>70.05</td>
    </tr>
    <tr>
      <th>5</th>
      <td>A</td>
      <td>2018-01-09</td>
      <td>70.68</td>
      <td>71.77</td>
      <td>70.68</td>
      <td>71.77</td>
    </tr>
    <tr>
      <th>6</th>
      <td>A</td>
      <td>2018-01-10</td>
      <td>71.45</td>
      <td>70.79</td>
      <td>71.45</td>
      <td>70.79</td>
    </tr>
    <tr>
      <th>7</th>
      <td>A</td>
      <td>2018-01-11</td>
      <td>70.92</td>
      <td>70.80</td>
      <td>70.92</td>
      <td>70.80</td>
    </tr>
    <tr>
      <th>8</th>
      <td>A</td>
      <td>2018-01-12</td>
      <td>70.73</td>
      <td>71.73</td>
      <td>70.73</td>
      <td>71.73</td>
    </tr>
    <tr>
      <th>9</th>
      <td>A</td>
      <td>2018-01-16</td>
      <td>72.02</td>
      <td>71.23</td>
      <td>72.02</td>
      <td>71.23</td>
    </tr>
    <tr>
      <th>10</th>
      <td>A</td>
      <td>2018-01-17</td>
      <td>71.72</td>
      <td>72.06</td>
      <td>71.72</td>
      <td>72.06</td>
    </tr>
    <tr>
      <th>11</th>
      <td>A</td>
      <td>2018-01-18</td>
      <td>72.20</td>
      <td>72.19</td>
      <td>72.20</td>
      <td>72.19</td>
    </tr>
    <tr>
      <th>12</th>
      <td>A</td>
      <td>2018-01-19</td>
      <td>72.48</td>
      <td>73.07</td>
      <td>72.48</td>
      <td>73.07</td>
    </tr>
    <tr>
      <th>13</th>
      <td>A</td>
      <td>2018-01-22</td>
      <td>73.17</td>
      <td>73.48</td>
      <td>73.17</td>
      <td>73.48</td>
    </tr>
    <tr>
      <th>14</th>
      <td>A</td>
      <td>2018-01-23</td>
      <td>74.05</td>
      <td>73.44</td>
      <td>74.05</td>
      <td>73.44</td>
    </tr>
    <tr>
      <th>15</th>
      <td>A</td>
      <td>2018-01-24</td>
      <td>73.66</td>
      <td>73.58</td>
      <td>73.66</td>
      <td>73.58</td>
    </tr>
    <tr>
      <th>16</th>
      <td>A</td>
      <td>2018-01-25</td>
      <td>74.17</td>
      <td>73.86</td>
      <td>74.17</td>
      <td>73.86</td>
    </tr>
    <tr>
      <th>17</th>
      <td>A</td>
      <td>2018-01-26</td>
      <td>74.30</td>
      <td>74.82</td>
      <td>74.30</td>
      <td>74.82</td>
    </tr>
    <tr>
      <th>18</th>
      <td>A</td>
      <td>2018-01-29</td>
      <td>74.48</td>
      <td>74.53</td>
      <td>74.48</td>
      <td>74.53</td>
    </tr>
    <tr>
      <th>19</th>
      <td>A</td>
      <td>2018-01-30</td>
      <td>73.99</td>
      <td>72.99</td>
      <td>73.99</td>
      <td>72.99</td>
    </tr>
    <tr>
      <th>20</th>
      <td>A</td>
      <td>2018-01-31</td>
      <td>73.77</td>
      <td>73.43</td>
      <td>73.77</td>
      <td>73.43</td>
    </tr>
    <tr>
      <th>21</th>
      <td>AA</td>
      <td>2018-01-02</td>
      <td>54.06</td>
      <td>55.17</td>
      <td>54.06</td>
      <td>55.17</td>
    </tr>
    <tr>
      <th>22</th>
      <td>AA</td>
      <td>2018-01-03</td>
      <td>54.92</td>
      <td>54.50</td>
      <td>54.92</td>
      <td>54.50</td>
    </tr>
    <tr>
      <th>23</th>
      <td>AA</td>
      <td>2018-01-04</td>
      <td>54.81</td>
      <td>54.70</td>
      <td>54.81</td>
      <td>54.70</td>
    </tr>
    <tr>
      <th>24</th>
      <td>AA</td>
      <td>2018-01-05</td>
      <td>54.65</td>
      <td>54.09</td>
      <td>54.65</td>
      <td>54.09</td>
    </tr>
    <tr>
      <th>25</th>
      <td>AA</td>
      <td>2018-01-08</td>
      <td>53.96</td>
      <td>55.00</td>
      <td>53.96</td>
      <td>55.00</td>
    </tr>
    <tr>
      <th>26</th>
      <td>AA</td>
      <td>2018-01-09</td>
      <td>55.00</td>
      <td>54.20</td>
      <td>55.00</td>
      <td>54.20</td>
    </tr>
    <tr>
      <th>27</th>
      <td>AA</td>
      <td>2018-01-10</td>
      <td>54.37</td>
      <td>56.17</td>
      <td>54.37</td>
      <td>56.17</td>
    </tr>
    <tr>
      <th>28</th>
      <td>AA</td>
      <td>2018-01-11</td>
      <td>56.60</td>
      <td>56.91</td>
      <td>56.60</td>
      <td>56.91</td>
    </tr>
    <tr>
      <th>29</th>
      <td>AA</td>
      <td>2018-01-12</td>
      <td>57.05</td>
      <td>56.76</td>
      <td>57.05</td>
      <td>56.76</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>9970</th>
      <td>CMG</td>
      <td>2018-01-18</td>
      <td>334.51</td>
      <td>337.53</td>
      <td>334.51</td>
      <td>337.53</td>
    </tr>
    <tr>
      <th>9971</th>
      <td>CMG</td>
      <td>2018-01-19</td>
      <td>339.25</td>
      <td>343.87</td>
      <td>339.25</td>
      <td>343.87</td>
    </tr>
    <tr>
      <th>9972</th>
      <td>CMG</td>
      <td>2018-01-22</td>
      <td>340.00</td>
      <td>330.00</td>
      <td>340.00</td>
      <td>330.00</td>
    </tr>
    <tr>
      <th>9973</th>
      <td>CMG</td>
      <td>2018-01-23</td>
      <td>330.00</td>
      <td>328.71</td>
      <td>330.00</td>
      <td>328.71</td>
    </tr>
    <tr>
      <th>9974</th>
      <td>CMG</td>
      <td>2018-01-24</td>
      <td>329.92</td>
      <td>329.53</td>
      <td>329.92</td>
      <td>329.53</td>
    </tr>
    <tr>
      <th>9975</th>
      <td>CMG</td>
      <td>2018-01-25</td>
      <td>330.34</td>
      <td>333.97</td>
      <td>330.34</td>
      <td>333.97</td>
    </tr>
    <tr>
      <th>9976</th>
      <td>CMG</td>
      <td>2018-01-26</td>
      <td>332.56</td>
      <td>330.23</td>
      <td>332.56</td>
      <td>330.23</td>
    </tr>
    <tr>
      <th>9977</th>
      <td>CMG</td>
      <td>2018-01-29</td>
      <td>327.00</td>
      <td>332.33</td>
      <td>327.00</td>
      <td>332.33</td>
    </tr>
    <tr>
      <th>9978</th>
      <td>CMG</td>
      <td>2018-01-30</td>
      <td>329.69</td>
      <td>322.08</td>
      <td>329.69</td>
      <td>322.08</td>
    </tr>
    <tr>
      <th>9979</th>
      <td>CMG</td>
      <td>2018-01-31</td>
      <td>322.87</td>
      <td>324.76</td>
      <td>322.87</td>
      <td>324.76</td>
    </tr>
    <tr>
      <th>9980</th>
      <td>CMI</td>
      <td>2018-01-02</td>
      <td>177.51</td>
      <td>177.06</td>
      <td>177.51</td>
      <td>177.06</td>
    </tr>
    <tr>
      <th>9981</th>
      <td>CMI</td>
      <td>2018-01-03</td>
      <td>177.34</td>
      <td>179.01</td>
      <td>177.34</td>
      <td>179.01</td>
    </tr>
    <tr>
      <th>9982</th>
      <td>CMI</td>
      <td>2018-01-04</td>
      <td>179.62</td>
      <td>181.75</td>
      <td>179.62</td>
      <td>181.75</td>
    </tr>
    <tr>
      <th>9983</th>
      <td>CMI</td>
      <td>2018-01-05</td>
      <td>182.02</td>
      <td>181.46</td>
      <td>182.02</td>
      <td>181.46</td>
    </tr>
    <tr>
      <th>9984</th>
      <td>CMI</td>
      <td>2018-01-08</td>
      <td>181.13</td>
      <td>182.12</td>
      <td>181.13</td>
      <td>182.12</td>
    </tr>
    <tr>
      <th>9985</th>
      <td>CMI</td>
      <td>2018-01-09</td>
      <td>182.48</td>
      <td>181.96</td>
      <td>182.48</td>
      <td>181.96</td>
    </tr>
    <tr>
      <th>9986</th>
      <td>CMI</td>
      <td>2018-01-10</td>
      <td>181.86</td>
      <td>180.56</td>
      <td>181.86</td>
      <td>180.56</td>
    </tr>
    <tr>
      <th>9987</th>
      <td>CMI</td>
      <td>2018-01-11</td>
      <td>181.24</td>
      <td>183.90</td>
      <td>181.24</td>
      <td>183.90</td>
    </tr>
    <tr>
      <th>9988</th>
      <td>CMI</td>
      <td>2018-01-12</td>
      <td>183.89</td>
      <td>184.18</td>
      <td>183.89</td>
      <td>184.18</td>
    </tr>
    <tr>
      <th>9989</th>
      <td>CMI</td>
      <td>2018-01-16</td>
      <td>184.81</td>
      <td>182.55</td>
      <td>184.81</td>
      <td>182.55</td>
    </tr>
    <tr>
      <th>9990</th>
      <td>CMI</td>
      <td>2018-01-17</td>
      <td>182.74</td>
      <td>183.69</td>
      <td>182.74</td>
      <td>183.69</td>
    </tr>
    <tr>
      <th>9991</th>
      <td>CMI</td>
      <td>2018-01-18</td>
      <td>183.37</td>
      <td>183.72</td>
      <td>183.37</td>
      <td>183.72</td>
    </tr>
    <tr>
      <th>9992</th>
      <td>CMI</td>
      <td>2018-01-19</td>
      <td>187.16</td>
      <td>189.08</td>
      <td>187.16</td>
      <td>189.08</td>
    </tr>
    <tr>
      <th>9993</th>
      <td>CMI</td>
      <td>2018-01-22</td>
      <td>188.80</td>
      <td>189.58</td>
      <td>188.80</td>
      <td>189.58</td>
    </tr>
    <tr>
      <th>9994</th>
      <td>CMI</td>
      <td>2018-01-23</td>
      <td>189.99</td>
      <td>188.43</td>
      <td>189.99</td>
      <td>188.43</td>
    </tr>
    <tr>
      <th>9995</th>
      <td>CMI</td>
      <td>2018-01-24</td>
      <td>189.22</td>
      <td>188.35</td>
      <td>189.22</td>
      <td>188.35</td>
    </tr>
    <tr>
      <th>9996</th>
      <td>CMI</td>
      <td>2018-01-25</td>
      <td>189.98</td>
      <td>189.40</td>
      <td>189.98</td>
      <td>189.40</td>
    </tr>
    <tr>
      <th>9997</th>
      <td>CMI</td>
      <td>2018-01-26</td>
      <td>190.28</td>
      <td>192.50</td>
      <td>190.28</td>
      <td>192.50</td>
    </tr>
    <tr>
      <th>9998</th>
      <td>CMI</td>
      <td>2018-01-29</td>
      <td>192.05</td>
      <td>190.81</td>
      <td>192.05</td>
      <td>190.81</td>
    </tr>
    <tr>
      <th>9999</th>
      <td>CMI</td>
      <td>2018-01-30</td>
      <td>189.22</td>
      <td>187.25</td>
      <td>189.22</td>
      <td>187.25</td>
    </tr>
  </tbody>
</table>
<p>10000 rows × 6 columns</p>
</div>




```python
#Create a new dataframe 'date' from previous dataframe that will be used as an index

dfsd=dfs.loc[:, 'date']
dfsd1=dfsd.drop_duplicates()
dfsd1
```




    None
    0    2018-01-02
    1    2018-01-03
    2    2018-01-04
    3    2018-01-05
    4    2018-01-08
    5    2018-01-09
    6    2018-01-10
    7    2018-01-11
    8    2018-01-12
    9    2018-01-16
    10   2018-01-17
    11   2018-01-18
    12   2018-01-19
    13   2018-01-22
    14   2018-01-23
    15   2018-01-24
    16   2018-01-25
    17   2018-01-26
    18   2018-01-29
    19   2018-01-30
    20   2018-01-31
    Name: date, dtype: datetime64[ns]




```python
#Create a new dataframe using grouping variables 'ticker' and 'prices' and indexed by date

outg = (dfs.groupby('ticker').apply(lambda g:g.set_index('date')[['open','close','adj_open','adj_close']]).unstack(level=0).fillna(dfs['close'].mean()))

#Delete column and adjust the multi-index column

print outg

```

                 open                                                         \
    ticker          A     AA    AAL        AAMC    AAN   AAOI   AAON     AAP
    date
    2018-01-02  67.42  54.06  52.33  724.662246  39.81  37.80  36.95  100.90
    2018-01-03  67.62  54.92  52.86   77.950000  39.43  38.27  36.95  106.42
    2018-01-04  69.54  54.81  52.48   80.200000  39.98  37.95  37.70  107.75
    2018-01-05  68.73  54.65  52.78   80.200000  39.85  38.70  37.55  111.96
    2018-01-08  69.73  53.96  52.60   80.200000  39.83  38.90  37.95  112.05
    2018-01-09  70.68  55.00  52.97   79.000000  40.82  38.14  37.45  111.69
    2018-01-10  71.45  54.37  53.23   79.000000  40.09  35.04  36.90  110.27
    2018-01-11  70.92  56.60  54.49   79.990000  39.16  35.37  36.15  110.70
    2018-01-12  70.73  57.05  56.56  724.662246  41.19  36.31  36.40  114.38
    2018-01-16  72.02  56.09  58.79   75.950000  41.54  35.69  36.75  116.76
    2018-01-17  71.72  56.03  58.31   71.501000  41.48  34.00  36.30  114.74
    2018-01-18  72.20  53.67  58.00   71.501000  40.42  33.73  36.25  115.67
    2018-01-19  72.48  52.86  58.59  724.662246  40.60  34.87  36.10  116.24
    2018-01-22  73.17  52.80  57.99   69.400000  42.08  34.98  37.20  116.88
    2018-01-23  74.05  52.34  57.74   67.700000  42.30  34.42  36.30  117.74
    2018-01-24  73.66  52.90  54.35   69.650000  41.19  34.92  36.20  119.26
    2018-01-25  74.17  53.74  54.00   69.664700  41.80  34.32  36.10  121.12
    2018-01-26  74.30  53.55  53.65   67.900000  41.86  34.91  36.20  123.34
    2018-01-29  74.48  53.89  52.79   68.150000  42.50  34.63  36.10  123.52
    2018-01-30  73.99  53.67  52.45   66.950000  41.39  32.74  36.00  121.57
    2018-01-31  73.77  52.75  53.08   69.024100  42.13  33.01  36.20  119.86

                                   ...     adj_close                               \
    ticker         AAPL    AAT     ...          CLVS    CLW     CLX    CMA    CMC
    date                           ...
    2018-01-02  170.160  38.30     ...         66.05  46.20  144.99  86.57  22.77
    2018-01-03  172.530  38.19     ...         66.64  46.15  143.43  86.54  24.30
    2018-01-04  172.540  37.81     ...         67.72  46.80  145.69  87.51  24.48
    2018-01-05  173.440  37.15     ...         66.49  48.40  145.73  88.47  24.90
    2018-01-08  174.350  37.11     ...         62.98  49.80  146.44  88.72  25.28
    2018-01-09  174.550  37.20     ...         62.01  50.15  146.16  90.37  25.04
    2018-01-10  173.160  36.37     ...         62.78  49.35  144.43  91.31  25.27
    2018-01-11  174.590  36.36     ...         59.88  50.30  141.99  92.52  25.82
    2018-01-12  176.180  36.34     ...         59.01  49.40  140.96  93.04  25.16
    2018-01-16  177.900  36.16     ...         55.41  47.85  142.41  93.79  24.59
    2018-01-17  176.150  36.18     ...         54.93  49.20  144.32  94.76  24.84
    2018-01-18  179.370  36.27     ...         55.87  49.20  143.14  93.81  25.09
    2018-01-19  178.610  35.73     ...         56.76  50.25  143.86  94.99  24.82
    2018-01-22  177.300  36.22     ...         60.67  49.50  144.48  95.21  25.02
    2018-01-23  177.300  36.40     ...         64.10  49.05  143.52  95.25  24.88
    2018-01-24  177.250  36.61     ...         61.25  48.30  142.25  95.53  24.99
    2018-01-25  174.505  36.24     ...         61.40  47.60  146.13  94.70  24.87
    2018-01-26  172.000  36.25     ...         61.75  47.35  142.64  95.81  25.27
    2018-01-29  170.160  35.63     ...         62.39  46.90  140.96  95.15  25.26
    2018-01-30  165.525  34.90     ...         60.97  47.60  141.76  94.76  24.55
    2018-01-31  166.870  34.99     ...         60.50  47.05  141.69  95.22  24.04


    ticker       CMCO  CMCSA     CME     CMG         CMI
    date
    2018-01-02  41.15  41.07  144.79  292.95  177.060000
    2018-01-03  40.81  40.41  147.11  309.00  179.010000
    2018-01-04  40.66  40.67  148.68  307.11  181.750000
    2018-01-05  40.28  41.04  149.65  313.79  181.460000
    2018-01-08  41.38  40.48  151.73  318.47  182.120000
    2018-01-09  43.54  40.61  152.63  319.37  181.960000
    2018-01-10  42.60  41.09  152.90  321.80  180.560000
    2018-01-11  43.00  42.60  152.81  325.50  183.900000
    2018-01-12  42.91  42.44  152.73  327.34  184.180000
    2018-01-16  42.47  41.82  152.20  327.37  182.550000
    2018-01-17  42.82  41.68  151.45  334.63  183.690000
    2018-01-18  42.79  41.85  152.21  337.53  183.720000
    2018-01-19  44.42  42.50  154.28  343.87  189.080000
    2018-01-22  44.25  42.89  155.45  330.00  189.580000
    2018-01-23  43.17  42.44  154.25  328.71  188.430000
    2018-01-24  42.57  42.99  154.99  329.53  188.350000
    2018-01-25  42.44  42.14  154.17  333.97  189.400000
    2018-01-26  42.05  42.80  155.16  330.23  192.500000
    2018-01-29  41.81  41.98  153.45  332.33  190.810000
    2018-01-30  41.41  42.34  153.33  322.08  187.250000
    2018-01-31  40.95  42.53  153.48  324.76  724.662246

    [21 rows x 1908 columns]



```python
names = [('ticker','AA')]
ds = hv.Dataset(outg, ['open','close','adj_open','adj_close'], names)
```


```python
%%opts Curve [width=800 height=550] {+framewise}
ds.to(hv.Curve, 'open')
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-157-8795b07a8357> in <module>()
    ----> 1 ds.to(hv.Curve, 'open')


    /opt/conda/lib/python2.7/site-packages/holoviews/core/data/__init__.pyc in __call__(self, new_type, kdims, vdims, groupby, sort, **kwargs)
        141             return element.sort() if sort else element
        142         group = selected.groupby(groupby, container_type=HoloMap,
    --> 143                                  group_type=new_type, **params)
        144         if sort:
        145             return group.map(lambda x: x.sort(), [new_type])


    /opt/conda/lib/python2.7/site-packages/holoviews/core/data/__init__.pyc in groupby(self, dimensions, container_type, group_type, dynamic, **kwargs)
        534
        535         return self.interface.groupby(self, dim_names, container_type,
    --> 536                                       group_type, **kwargs)
        537
        538     def __len__(self):


    /opt/conda/lib/python2.7/site-packages/holoviews/core/data/pandas.pyc in groupby(cls, columns, dimensions, container_type, group_type, **kwargs)
        152         group_by = [d.name for d in index_dims]
        153         data = [(k, group_type(v, **group_kwargs)) for k, v in
    --> 154                 columns.data.groupby(group_by, sort=False)]
        155         if issubclass(container_type, NdMapping):
        156             with item_check(False):


    /opt/conda/lib/python2.7/site-packages/pandas/core/generic.pyc in groupby(self, by, axis, level, as_index, sort, group_keys, squeeze, **kwargs)
       4269         return groupby(self, by=by, axis=axis, level=level, as_index=as_index,
       4270                        sort=sort, group_keys=group_keys, squeeze=squeeze,
    -> 4271                        **kwargs)
       4272
       4273     def asfreq(self, freq, method=None, how=None, normalize=False,


    /opt/conda/lib/python2.7/site-packages/pandas/core/groupby.pyc in groupby(obj, by, **kwds)
       1624         raise TypeError('invalid type: %s' % type(obj))
       1625
    -> 1626     return klass(obj, by, **kwds)
       1627
       1628


    /opt/conda/lib/python2.7/site-packages/pandas/core/groupby.pyc in __init__(self, obj, keys, axis, level, grouper, exclusions, selection, as_index, sort, group_keys, squeeze, **kwargs)
        390                                                     level=level,
        391                                                     sort=sort,
    --> 392                                                     mutated=self.mutated)
        393
        394         self.obj = obj


    /opt/conda/lib/python2.7/site-packages/pandas/core/groupby.pyc in _get_grouper(obj, key, axis, level, sort, mutated)
       2636                         sort=sort,
       2637                         in_axis=in_axis) \
    -> 2638             if not isinstance(gpr, Grouping) else gpr
       2639
       2640         groupings.append(ping)


    /opt/conda/lib/python2.7/site-packages/pandas/core/groupby.pyc in __init__(self, index, grouper, obj, name, level, sort, in_axis)
       2417                 if getattr(self.grouper, 'ndim', 1) != 1:
       2418                     t = self.name or str(type(self.grouper))
    -> 2419                     raise ValueError("Grouper for '%s' not 1-dimensional" % t)
       2420                 self.grouper = self.index.map(self.grouper)
       2421                 if not (hasattr(self.grouper, "__len__") and


    ValueError: Grouper for 'close' not 1-dimensional



```python
#Remove index
outg = outg.reset_index(drop=True)

#Add the previously generated dataframe index to the final dataframe

outg['date'] = dfsd1

#View the final table

outg
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="10" halign="left">open</th>
      <th>...</th>
      <th colspan="9" halign="left">adj_close</th>
      <th>date</th>
    </tr>
    <tr>
      <th>ticker</th>
      <th>A</th>
      <th>AA</th>
      <th>AAL</th>
      <th>AAMC</th>
      <th>AAN</th>
      <th>AAOI</th>
      <th>AAON</th>
      <th>AAP</th>
      <th>AAPL</th>
      <th>AAT</th>
      <th>...</th>
      <th>CLW</th>
      <th>CLX</th>
      <th>CMA</th>
      <th>CMC</th>
      <th>CMCO</th>
      <th>CMCSA</th>
      <th>CME</th>
      <th>CMG</th>
      <th>CMI</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>67.42</td>
      <td>54.06</td>
      <td>52.33</td>
      <td>724.662246</td>
      <td>39.81</td>
      <td>37.80</td>
      <td>36.95</td>
      <td>100.90</td>
      <td>170.160</td>
      <td>38.30</td>
      <td>...</td>
      <td>46.20</td>
      <td>144.99</td>
      <td>86.57</td>
      <td>22.77</td>
      <td>41.15</td>
      <td>41.07</td>
      <td>144.79</td>
      <td>292.95</td>
      <td>177.060000</td>
      <td>2018-01-02</td>
    </tr>
    <tr>
      <th>1</th>
      <td>67.62</td>
      <td>54.92</td>
      <td>52.86</td>
      <td>77.950000</td>
      <td>39.43</td>
      <td>38.27</td>
      <td>36.95</td>
      <td>106.42</td>
      <td>172.530</td>
      <td>38.19</td>
      <td>...</td>
      <td>46.15</td>
      <td>143.43</td>
      <td>86.54</td>
      <td>24.30</td>
      <td>40.81</td>
      <td>40.41</td>
      <td>147.11</td>
      <td>309.00</td>
      <td>179.010000</td>
      <td>2018-01-03</td>
    </tr>
    <tr>
      <th>2</th>
      <td>69.54</td>
      <td>54.81</td>
      <td>52.48</td>
      <td>80.200000</td>
      <td>39.98</td>
      <td>37.95</td>
      <td>37.70</td>
      <td>107.75</td>
      <td>172.540</td>
      <td>37.81</td>
      <td>...</td>
      <td>46.80</td>
      <td>145.69</td>
      <td>87.51</td>
      <td>24.48</td>
      <td>40.66</td>
      <td>40.67</td>
      <td>148.68</td>
      <td>307.11</td>
      <td>181.750000</td>
      <td>2018-01-04</td>
    </tr>
    <tr>
      <th>3</th>
      <td>68.73</td>
      <td>54.65</td>
      <td>52.78</td>
      <td>80.200000</td>
      <td>39.85</td>
      <td>38.70</td>
      <td>37.55</td>
      <td>111.96</td>
      <td>173.440</td>
      <td>37.15</td>
      <td>...</td>
      <td>48.40</td>
      <td>145.73</td>
      <td>88.47</td>
      <td>24.90</td>
      <td>40.28</td>
      <td>41.04</td>
      <td>149.65</td>
      <td>313.79</td>
      <td>181.460000</td>
      <td>2018-01-05</td>
    </tr>
    <tr>
      <th>4</th>
      <td>69.73</td>
      <td>53.96</td>
      <td>52.60</td>
      <td>80.200000</td>
      <td>39.83</td>
      <td>38.90</td>
      <td>37.95</td>
      <td>112.05</td>
      <td>174.350</td>
      <td>37.11</td>
      <td>...</td>
      <td>49.80</td>
      <td>146.44</td>
      <td>88.72</td>
      <td>25.28</td>
      <td>41.38</td>
      <td>40.48</td>
      <td>151.73</td>
      <td>318.47</td>
      <td>182.120000</td>
      <td>2018-01-08</td>
    </tr>
    <tr>
      <th>5</th>
      <td>70.68</td>
      <td>55.00</td>
      <td>52.97</td>
      <td>79.000000</td>
      <td>40.82</td>
      <td>38.14</td>
      <td>37.45</td>
      <td>111.69</td>
      <td>174.550</td>
      <td>37.20</td>
      <td>...</td>
      <td>50.15</td>
      <td>146.16</td>
      <td>90.37</td>
      <td>25.04</td>
      <td>43.54</td>
      <td>40.61</td>
      <td>152.63</td>
      <td>319.37</td>
      <td>181.960000</td>
      <td>2018-01-09</td>
    </tr>
    <tr>
      <th>6</th>
      <td>71.45</td>
      <td>54.37</td>
      <td>53.23</td>
      <td>79.000000</td>
      <td>40.09</td>
      <td>35.04</td>
      <td>36.90</td>
      <td>110.27</td>
      <td>173.160</td>
      <td>36.37</td>
      <td>...</td>
      <td>49.35</td>
      <td>144.43</td>
      <td>91.31</td>
      <td>25.27</td>
      <td>42.60</td>
      <td>41.09</td>
      <td>152.90</td>
      <td>321.80</td>
      <td>180.560000</td>
      <td>2018-01-10</td>
    </tr>
    <tr>
      <th>7</th>
      <td>70.92</td>
      <td>56.60</td>
      <td>54.49</td>
      <td>79.990000</td>
      <td>39.16</td>
      <td>35.37</td>
      <td>36.15</td>
      <td>110.70</td>
      <td>174.590</td>
      <td>36.36</td>
      <td>...</td>
      <td>50.30</td>
      <td>141.99</td>
      <td>92.52</td>
      <td>25.82</td>
      <td>43.00</td>
      <td>42.60</td>
      <td>152.81</td>
      <td>325.50</td>
      <td>183.900000</td>
      <td>2018-01-11</td>
    </tr>
    <tr>
      <th>8</th>
      <td>70.73</td>
      <td>57.05</td>
      <td>56.56</td>
      <td>724.662246</td>
      <td>41.19</td>
      <td>36.31</td>
      <td>36.40</td>
      <td>114.38</td>
      <td>176.180</td>
      <td>36.34</td>
      <td>...</td>
      <td>49.40</td>
      <td>140.96</td>
      <td>93.04</td>
      <td>25.16</td>
      <td>42.91</td>
      <td>42.44</td>
      <td>152.73</td>
      <td>327.34</td>
      <td>184.180000</td>
      <td>2018-01-12</td>
    </tr>
    <tr>
      <th>9</th>
      <td>72.02</td>
      <td>56.09</td>
      <td>58.79</td>
      <td>75.950000</td>
      <td>41.54</td>
      <td>35.69</td>
      <td>36.75</td>
      <td>116.76</td>
      <td>177.900</td>
      <td>36.16</td>
      <td>...</td>
      <td>47.85</td>
      <td>142.41</td>
      <td>93.79</td>
      <td>24.59</td>
      <td>42.47</td>
      <td>41.82</td>
      <td>152.20</td>
      <td>327.37</td>
      <td>182.550000</td>
      <td>2018-01-16</td>
    </tr>
    <tr>
      <th>10</th>
      <td>71.72</td>
      <td>56.03</td>
      <td>58.31</td>
      <td>71.501000</td>
      <td>41.48</td>
      <td>34.00</td>
      <td>36.30</td>
      <td>114.74</td>
      <td>176.150</td>
      <td>36.18</td>
      <td>...</td>
      <td>49.20</td>
      <td>144.32</td>
      <td>94.76</td>
      <td>24.84</td>
      <td>42.82</td>
      <td>41.68</td>
      <td>151.45</td>
      <td>334.63</td>
      <td>183.690000</td>
      <td>2018-01-17</td>
    </tr>
    <tr>
      <th>11</th>
      <td>72.20</td>
      <td>53.67</td>
      <td>58.00</td>
      <td>71.501000</td>
      <td>40.42</td>
      <td>33.73</td>
      <td>36.25</td>
      <td>115.67</td>
      <td>179.370</td>
      <td>36.27</td>
      <td>...</td>
      <td>49.20</td>
      <td>143.14</td>
      <td>93.81</td>
      <td>25.09</td>
      <td>42.79</td>
      <td>41.85</td>
      <td>152.21</td>
      <td>337.53</td>
      <td>183.720000</td>
      <td>2018-01-18</td>
    </tr>
    <tr>
      <th>12</th>
      <td>72.48</td>
      <td>52.86</td>
      <td>58.59</td>
      <td>724.662246</td>
      <td>40.60</td>
      <td>34.87</td>
      <td>36.10</td>
      <td>116.24</td>
      <td>178.610</td>
      <td>35.73</td>
      <td>...</td>
      <td>50.25</td>
      <td>143.86</td>
      <td>94.99</td>
      <td>24.82</td>
      <td>44.42</td>
      <td>42.50</td>
      <td>154.28</td>
      <td>343.87</td>
      <td>189.080000</td>
      <td>2018-01-19</td>
    </tr>
    <tr>
      <th>13</th>
      <td>73.17</td>
      <td>52.80</td>
      <td>57.99</td>
      <td>69.400000</td>
      <td>42.08</td>
      <td>34.98</td>
      <td>37.20</td>
      <td>116.88</td>
      <td>177.300</td>
      <td>36.22</td>
      <td>...</td>
      <td>49.50</td>
      <td>144.48</td>
      <td>95.21</td>
      <td>25.02</td>
      <td>44.25</td>
      <td>42.89</td>
      <td>155.45</td>
      <td>330.00</td>
      <td>189.580000</td>
      <td>2018-01-22</td>
    </tr>
    <tr>
      <th>14</th>
      <td>74.05</td>
      <td>52.34</td>
      <td>57.74</td>
      <td>67.700000</td>
      <td>42.30</td>
      <td>34.42</td>
      <td>36.30</td>
      <td>117.74</td>
      <td>177.300</td>
      <td>36.40</td>
      <td>...</td>
      <td>49.05</td>
      <td>143.52</td>
      <td>95.25</td>
      <td>24.88</td>
      <td>43.17</td>
      <td>42.44</td>
      <td>154.25</td>
      <td>328.71</td>
      <td>188.430000</td>
      <td>2018-01-23</td>
    </tr>
    <tr>
      <th>15</th>
      <td>73.66</td>
      <td>52.90</td>
      <td>54.35</td>
      <td>69.650000</td>
      <td>41.19</td>
      <td>34.92</td>
      <td>36.20</td>
      <td>119.26</td>
      <td>177.250</td>
      <td>36.61</td>
      <td>...</td>
      <td>48.30</td>
      <td>142.25</td>
      <td>95.53</td>
      <td>24.99</td>
      <td>42.57</td>
      <td>42.99</td>
      <td>154.99</td>
      <td>329.53</td>
      <td>188.350000</td>
      <td>2018-01-24</td>
    </tr>
    <tr>
      <th>16</th>
      <td>74.17</td>
      <td>53.74</td>
      <td>54.00</td>
      <td>69.664700</td>
      <td>41.80</td>
      <td>34.32</td>
      <td>36.10</td>
      <td>121.12</td>
      <td>174.505</td>
      <td>36.24</td>
      <td>...</td>
      <td>47.60</td>
      <td>146.13</td>
      <td>94.70</td>
      <td>24.87</td>
      <td>42.44</td>
      <td>42.14</td>
      <td>154.17</td>
      <td>333.97</td>
      <td>189.400000</td>
      <td>2018-01-25</td>
    </tr>
    <tr>
      <th>17</th>
      <td>74.30</td>
      <td>53.55</td>
      <td>53.65</td>
      <td>67.900000</td>
      <td>41.86</td>
      <td>34.91</td>
      <td>36.20</td>
      <td>123.34</td>
      <td>172.000</td>
      <td>36.25</td>
      <td>...</td>
      <td>47.35</td>
      <td>142.64</td>
      <td>95.81</td>
      <td>25.27</td>
      <td>42.05</td>
      <td>42.80</td>
      <td>155.16</td>
      <td>330.23</td>
      <td>192.500000</td>
      <td>2018-01-26</td>
    </tr>
    <tr>
      <th>18</th>
      <td>74.48</td>
      <td>53.89</td>
      <td>52.79</td>
      <td>68.150000</td>
      <td>42.50</td>
      <td>34.63</td>
      <td>36.10</td>
      <td>123.52</td>
      <td>170.160</td>
      <td>35.63</td>
      <td>...</td>
      <td>46.90</td>
      <td>140.96</td>
      <td>95.15</td>
      <td>25.26</td>
      <td>41.81</td>
      <td>41.98</td>
      <td>153.45</td>
      <td>332.33</td>
      <td>190.810000</td>
      <td>2018-01-29</td>
    </tr>
    <tr>
      <th>19</th>
      <td>73.99</td>
      <td>53.67</td>
      <td>52.45</td>
      <td>66.950000</td>
      <td>41.39</td>
      <td>32.74</td>
      <td>36.00</td>
      <td>121.57</td>
      <td>165.525</td>
      <td>34.90</td>
      <td>...</td>
      <td>47.60</td>
      <td>141.76</td>
      <td>94.76</td>
      <td>24.55</td>
      <td>41.41</td>
      <td>42.34</td>
      <td>153.33</td>
      <td>322.08</td>
      <td>187.250000</td>
      <td>2018-01-30</td>
    </tr>
    <tr>
      <th>20</th>
      <td>73.77</td>
      <td>52.75</td>
      <td>53.08</td>
      <td>69.024100</td>
      <td>42.13</td>
      <td>33.01</td>
      <td>36.20</td>
      <td>119.86</td>
      <td>166.870</td>
      <td>34.99</td>
      <td>...</td>
      <td>47.05</td>
      <td>141.69</td>
      <td>95.22</td>
      <td>24.04</td>
      <td>40.95</td>
      <td>42.53</td>
      <td>153.48</td>
      <td>324.76</td>
      <td>724.662246</td>
      <td>2018-01-31</td>
    </tr>
  </tbody>
</table>
<p>21 rows × 1909 columns</p>
</div>




```python
#See elements ordered

sorted(outg)
```




    [(u'adj_close', u'A'),
     (u'adj_close', u'AA'),
     (u'adj_close', u'AAL'),
     (u'adj_close', u'AAMC'),
     (u'adj_close', u'AAN'),
     (u'adj_close', u'AAOI'),
     (u'adj_close', u'AAON'),
     (u'adj_close', u'AAP'),
     (u'adj_close', u'AAPL'),
     (u'adj_close', u'AAT'),
     (u'adj_close', u'AAWW'),
     (u'adj_close', u'ABAX'),
     (u'adj_close', u'ABBV'),
     (u'adj_close', u'ABC'),
     (u'adj_close', u'ABCB'),
     (u'adj_close', u'ABG'),
     (u'adj_close', u'ABM'),
     (u'adj_close', u'ABMD'),
     (u'adj_close', u'ABT'),
     (u'adj_close', u'ACAD'),
     (u'adj_close', u'ACC'),
     (u'adj_close', u'ACCO'),
     (u'adj_close', u'ACET'),
     (u'adj_close', u'ACGL'),
     (u'adj_close', u'ACHC'),
     (u'adj_close', u'ACHN'),
     (u'adj_close', u'ACIW'),
     (u'adj_close', u'ACLS'),
     (u'adj_close', u'ACM'),
     (u'adj_close', u'ACN'),
     (u'adj_close', u'ACOR'),
     (u'adj_close', u'ACRE'),
     (u'adj_close', u'ACRX'),
     (u'adj_close', u'ACTG'),
     (u'adj_close', u'ACXM'),
     (u'adj_close', u'ADBE'),
     (u'adj_close', u'ADC'),
     (u'adj_close', u'ADES'),
     (u'adj_close', u'ADI'),
     (u'adj_close', u'ADM'),
     (u'adj_close', u'ADMS'),
     (u'adj_close', u'ADP'),
     (u'adj_close', u'ADS'),
     (u'adj_close', u'ADSK'),
     (u'adj_close', u'ADTN'),
     (u'adj_close', u'ADUS'),
     (u'adj_close', u'AE'),
     (u'adj_close', u'AEE'),
     (u'adj_close', u'AEGN'),
     (u'adj_close', u'AEIS'),
     (u'adj_close', u'AEL'),
     (u'adj_close', u'AEO'),
     (u'adj_close', u'AEP'),
     (u'adj_close', u'AERI'),
     (u'adj_close', u'AES'),
     (u'adj_close', u'AET'),
     (u'adj_close', u'AFAM'),
     (u'adj_close', u'AFG'),
     (u'adj_close', u'AFH'),
     (u'adj_close', u'AFL'),
     (u'adj_close', u'AFSI'),
     (u'adj_close', u'AGCO'),
     (u'adj_close', u'AGEN'),
     (u'adj_close', u'AGII'),
     (u'adj_close', u'AGIO'),
     (u'adj_close', u'AGM'),
     (u'adj_close', u'AGN'),
     (u'adj_close', u'AGNC'),
     (u'adj_close', u'AGO'),
     (u'adj_close', u'AGTC'),
     (u'adj_close', u'AGX'),
     (u'adj_close', u'AGYS'),
     (u'adj_close', u'AHC'),
     (u'adj_close', u'AHH'),
     (u'adj_close', u'AHL'),
     (u'adj_close', u'AHP'),
     (u'adj_close', u'AHT'),
     (u'adj_close', u'AI'),
     (u'adj_close', u'AIG'),
     (u'adj_close', u'AIMC'),
     (u'adj_close', u'AIN'),
     (u'adj_close', u'AINV'),
     (u'adj_close', u'AIR'),
     (u'adj_close', u'AIT'),
     (u'adj_close', u'AIV'),
     (u'adj_close', u'AIZ'),
     (u'adj_close', u'AJG'),
     (u'adj_close', u'AKAM'),
     (u'adj_close', u'AKAO'),
     (u'adj_close', u'AKBA'),
     (u'adj_close', u'AKR'),
     (u'adj_close', u'AKRX'),
     (u'adj_close', u'AKS'),
     (u'adj_close', u'AL'),
     (u'adj_close', u'ALB'),
     (u'adj_close', u'ALCO'),
     (u'adj_close', u'ALDR'),
     (u'adj_close', u'ALE'),
     (u'adj_close', u'ALEX'),
     (u'adj_close', u'ALG'),
     (u'adj_close', u'ALGN'),
     (u'adj_close', u'ALGT'),
     (u'adj_close', u'ALIM'),
     (u'adj_close', u'ALK'),
     (u'adj_close', u'ALKS'),
     (u'adj_close', u'ALL'),
     (u'adj_close', u'ALLE'),
     (u'adj_close', u'ALNY'),
     (u'adj_close', u'ALOG'),
     (u'adj_close', u'ALSN'),
     (u'adj_close', u'ALX'),
     (u'adj_close', u'ALXN'),
     (u'adj_close', u'AMAG'),
     (u'adj_close', u'AMAT'),
     (u'adj_close', u'AMBA'),
     (u'adj_close', u'AMBC'),
     (u'adj_close', u'AMBR'),
     (u'adj_close', u'AMC'),
     (u'adj_close', u'AMCX'),
     (u'adj_close', u'AMD'),
     (u'adj_close', u'AME'),
     (u'adj_close', u'AMED'),
     (u'adj_close', u'AMG'),
     (u'adj_close', u'AMGN'),
     (u'adj_close', u'AMKR'),
     (u'adj_close', u'AMNB'),
     (u'adj_close', u'AMP'),
     (u'adj_close', u'AMPE'),
     (u'adj_close', u'AMRC'),
     (u'adj_close', u'AMRS'),
     (u'adj_close', u'AMSC'),
     (u'adj_close', u'AMSF'),
     (u'adj_close', u'AMSWA'),
     (u'adj_close', u'AMT'),
     (u'adj_close', u'AMTD'),
     (u'adj_close', u'AMWD'),
     (u'adj_close', u'AMZN'),
     (u'adj_close', u'ANAT'),
     (u'adj_close', u'ANCX'),
     (u'adj_close', u'ANDE'),
     (u'adj_close', u'ANDV'),
     (u'adj_close', u'ANF'),
     (u'adj_close', u'ANGI'),
     (u'adj_close', u'ANGO'),
     (u'adj_close', u'ANH'),
     (u'adj_close', u'ANIK'),
     (u'adj_close', u'ANIP'),
     (u'adj_close', u'ANSS'),
     (u'adj_close', u'ANTM'),
     (u'adj_close', u'AOI'),
     (u'adj_close', u'AON'),
     (u'adj_close', u'AOS'),
     (u'adj_close', u'AOSL'),
     (u'adj_close', u'AP'),
     (u'adj_close', u'APA'),
     (u'adj_close', u'APAM'),
     (u'adj_close', u'APC'),
     (u'adj_close', u'APD'),
     (u'adj_close', u'APEI'),
     (u'adj_close', u'APH'),
     (u'adj_close', u'APOG'),
     (u'adj_close', u'APTV'),
     (u'adj_close', u'ARAY'),
     (u'adj_close', u'ARC'),
     (u'adj_close', u'ARCB'),
     (u'adj_close', u'ARCC'),
     (u'adj_close', u'ARCW'),
     (u'adj_close', u'ARE'),
     (u'adj_close', u'AREX'),
     (u'adj_close', u'ARI'),
     (u'adj_close', u'ARII'),
     (u'adj_close', u'ARNA'),
     (u'adj_close', u'ARNC'),
     (u'adj_close', u'AROW'),
     (u'adj_close', u'ARQL'),
     (u'adj_close', u'ARR'),
     (u'adj_close', u'ARRS'),
     (u'adj_close', u'ARRY'),
     (u'adj_close', u'ARTNA'),
     (u'adj_close', u'ARW'),
     (u'adj_close', u'ARWR'),
     (u'adj_close', u'ASC'),
     (u'adj_close', u'ASCMA'),
     (u'adj_close', u'ASGN'),
     (u'adj_close', u'ASH'),
     (u'adj_close', u'ASNA'),
     (u'adj_close', u'ASPS'),
     (u'adj_close', u'ASTE'),
     (u'adj_close', u'AT'),
     (u'adj_close', u'ATEC'),
     (u'adj_close', u'ATEN'),
     (u'adj_close', u'ATHN'),
     (u'adj_close', u'ATLO'),
     (u'adj_close', u'ATNI'),
     (u'adj_close', u'ATNM'),
     (u'adj_close', u'ATO'),
     (u'adj_close', u'ATR'),
     (u'adj_close', u'ATRC'),
     (u'adj_close', u'ATRI'),
     (u'adj_close', u'ATRO'),
     (u'adj_close', u'ATRS'),
     (u'adj_close', u'ATSG'),
     (u'adj_close', u'ATU'),
     (u'adj_close', u'ATVI'),
     (u'adj_close', u'AVA'),
     (u'adj_close', u'AVAV'),
     (u'adj_close', u'AVB'),
     (u'adj_close', u'AVD'),
     (u'adj_close', u'AVEO'),
     (u'adj_close', u'AVGO'),
     (u'adj_close', u'AVHI'),
     (u'adj_close', u'AVID'),
     (u'adj_close', u'AVNW'),
     (u'adj_close', u'AVT'),
     (u'adj_close', u'AVX'),
     (u'adj_close', u'AVY'),
     (u'adj_close', u'AWI'),
     (u'adj_close', u'AWK'),
     (u'adj_close', u'AWR'),
     (u'adj_close', u'AXAS'),
     (u'adj_close', u'AXDX'),
     (u'adj_close', u'AXE'),
     (u'adj_close', u'AXL'),
     (u'adj_close', u'AXP'),
     (u'adj_close', u'AXS'),
     (u'adj_close', u'AYI'),
     (u'adj_close', u'AYR'),
     (u'adj_close', u'AZO'),
     (u'adj_close', u'AZPN'),
     (u'adj_close', u'AZZ'),
     (u'adj_close', u'B'),
     (u'adj_close', u'BA'),
     (u'adj_close', u'BABY'),
     (u'adj_close', u'BAC'),
     (u'adj_close', u'BAH'),
     (u'adj_close', u'BANC'),
     (u'adj_close', u'BANF'),
     (u'adj_close', u'BANR'),
     (u'adj_close', u'BAS'),
     (u'adj_close', u'BAX'),
     (u'adj_close', u'BBG'),
     (u'adj_close', u'BBGI'),
     (u'adj_close', u'BBOX'),
     (u'adj_close', u'BBRG'),
     (u'adj_close', u'BBSI'),
     (u'adj_close', u'BBT'),
     (u'adj_close', u'BBW'),
     (u'adj_close', u'BBX'),
     (u'adj_close', u'BBY'),
     (u'adj_close', u'BC'),
     (u'adj_close', u'BCC'),
     (u'adj_close', u'BCEI'),
     (u'adj_close', u'BCO'),
     (u'adj_close', u'BCOR'),
     (u'adj_close', u'BCOV'),
     (u'adj_close', u'BCPC'),
     (u'adj_close', u'BCRX'),
     (u'adj_close', u'BDC'),
     (u'adj_close', u'BDGE'),
     (u'adj_close', u'BDN'),
     (u'adj_close', u'BDSI'),
     (u'adj_close', u'BDX'),
     (u'adj_close', u'BEAT'),
     (u'adj_close', u'BECN'),
     (u'adj_close', u'BELFB'),
     (u'adj_close', u'BEN'),
     (u'adj_close', u'BERY'),
     (u'adj_close', u'BFAM'),
     (u'adj_close', u'BFIN'),
     (u'adj_close', u'BFS'),
     (u'adj_close', u'BF_B'),
     (u'adj_close', u'BG'),
     (u'adj_close', u'BGC'),
     (u'adj_close', u'BGCP'),
     (u'adj_close', u'BGFV'),
     (u'adj_close', u'BGG'),
     (u'adj_close', u'BGS'),
     (u'adj_close', u'BH'),
     (u'adj_close', u'BHB'),
     (u'adj_close', u'BHE'),
     (u'adj_close', u'BHF'),
     (u'adj_close', u'BHGE'),
     (u'adj_close', u'BHLB'),
     (u'adj_close', u'BID'),
     (u'adj_close', u'BIDU'),
     (u'adj_close', u'BIG'),
     (u'adj_close', u'BIIB'),
     (u'adj_close', u'BIO'),
     (u'adj_close', u'BIOL'),
     (u'adj_close', u'BIOS'),
     (u'adj_close', u'BJRI'),
     (u'adj_close', u'BK'),
     (u'adj_close', u'BKCC'),
     (u'adj_close', u'BKD'),
     (u'adj_close', u'BKE'),
     (u'adj_close', u'BKH'),
     (u'adj_close', u'BKMU'),
     (u'adj_close', u'BKS'),
     (u'adj_close', u'BKU'),
     (u'adj_close', u'BLDR'),
     (u'adj_close', u'BLK'),
     (u'adj_close', u'BLKB'),
     (u'adj_close', u'BLL'),
     (u'adj_close', u'BLMN'),
     (u'adj_close', u'BLUE'),
     (u'adj_close', u'BLX'),
     (u'adj_close', u'BMI'),
     (u'adj_close', u'BMRC'),
     (u'adj_close', u'BMRN'),
     (u'adj_close', u'BMS'),
     (u'adj_close', u'BMTC'),
     (u'adj_close', u'BMY'),
     (u'adj_close', u'BNCL'),
     (u'adj_close', u'BNFT'),
     (u'adj_close', u'BOBE'),
     (u'adj_close', u'BOFI'),
     (u'adj_close', u'BOH'),
     (u'adj_close', u'BOKF'),
     (u'adj_close', u'BOOM'),
     (u'adj_close', u'BP'),
     (u'adj_close', u'BPFH'),
     (u'adj_close', u'BPI'),
     (u'adj_close', u'BPOP'),
     (u'adj_close', u'BPTH'),
     (u'adj_close', u'BR'),
     (u'adj_close', u'BRC'),
     (u'adj_close', u'BREW'),
     (u'adj_close', u'BRKL'),
     (u'adj_close', u'BRKR'),
     (u'adj_close', u'BRKS'),
     (u'adj_close', u'BRK_A'),
     (u'adj_close', u'BRK_B'),
     (u'adj_close', u'BRO'),
     (u'adj_close', u'BRS'),
     (u'adj_close', u'BRSS'),
     (u'adj_close', u'BRT'),
     (u'adj_close', u'BSET'),
     (u'adj_close', u'BSFT'),
     (u'adj_close', u'BSRR'),
     (u'adj_close', u'BSTC'),
     (u'adj_close', u'BSX'),
     (u'adj_close', u'BTU'),
     (u'adj_close', u'BTX'),
     (u'adj_close', u'BURL'),
     (u'adj_close', u'BUSE'),
     (u'adj_close', u'BV'),
     (u'adj_close', u'BWA'),
     (u'adj_close', u'BWINB'),
     (u'adj_close', u'BWLD'),
     (u'adj_close', u'BXC'),
     (u'adj_close', u'BXP'),
     (u'adj_close', u'BXS'),
     (u'adj_close', u'BYD'),
     (u'adj_close', u'BZH'),
     (u'adj_close', u'C'),
     (u'adj_close', u'CA'),
     (u'adj_close', u'CAC'),
     (u'adj_close', u'CACC'),
     (u'adj_close', u'CACI'),
     (u'adj_close', u'CAG'),
     (u'adj_close', u'CAH'),
     (u'adj_close', u'CAKE'),
     (u'adj_close', u'CALD'),
     (u'adj_close', u'CALL'),
     (u'adj_close', u'CALM'),
     (u'adj_close', u'CALX'),
     (u'adj_close', u'CAMP'),
     (u'adj_close', u'CAR'),
     (u'adj_close', u'CARA'),
     (u'adj_close', u'CARB'),
     (u'adj_close', u'CASH'),
     (u'adj_close', u'CASS'),
     (u'adj_close', u'CASY'),
     (u'adj_close', u'CAT'),
     (u'adj_close', u'CATM'),
     (u'adj_close', u'CATO'),
     (u'adj_close', u'CATY'),
     (u'adj_close', u'CAVM'),
     (u'adj_close', u'CB'),
     (u'adj_close', u'CBB'),
     (u'adj_close', u'CBG'),
     (u'adj_close', u'CBI'),
     (u'adj_close', u'CBK'),
     (u'adj_close', u'CBL'),
     (u'adj_close', u'CBM'),
     (u'adj_close', u'CBOE'),
     (u'adj_close', u'CBPX'),
     (u'adj_close', u'CBRL'),
     (u'adj_close', u'CBS'),
     (u'adj_close', u'CBSH'),
     (u'adj_close', u'CBT'),
     (u'adj_close', u'CBU'),
     (u'adj_close', u'CBZ'),
     (u'adj_close', u'CCBG'),
     (u'adj_close', u'CCC'),
     (u'adj_close', u'CCE'),
     (u'adj_close', u'CCF'),
     (u'adj_close', u'CCI'),
     (u'adj_close', u'CCK'),
     (u'adj_close', u'CCL'),
     (u'adj_close', u'CCMP'),
     (u'adj_close', u'CCNE'),
     (u'adj_close', u'CCO'),
     (u'adj_close', u'CCOI'),
     (u'adj_close', u'CCRN'),
     (u'adj_close', u'CCXI'),
     (u'adj_close', u'CDE'),
     (u'adj_close', u'CDNS'),
     (u'adj_close', u'CDR'),
     (u'adj_close', u'CE'),
     (u'adj_close', u'CECE'),
     (u'adj_close', u'CECO'),
     (u'adj_close', u'CELG'),
     (u'adj_close', u'CENTA'),
     (u'adj_close', u'CENX'),
     (u'adj_close', u'CERN'),
     (u'adj_close', u'CERS'),
     (u'adj_close', u'CETV'),
     (u'adj_close', u'CEVA'),
     (u'adj_close', u'CF'),
     (u'adj_close', u'CFFI'),
     (u'adj_close', u'CFFN'),
     (u'adj_close', u'CFG'),
     (u'adj_close', u'CFR'),
     (u'adj_close', u'CFX'),
     (u'adj_close', u'CGI'),
     (u'adj_close', u'CGNX'),
     (u'adj_close', u'CHCO'),
     (u'adj_close', u'CHD'),
     (u'adj_close', u'CHDN'),
     (u'adj_close', u'CHE'),
     (u'adj_close', u'CHEF'),
     (u'adj_close', u'CHFC'),
     (u'adj_close', u'CHFN'),
     (u'adj_close', u'CHGG'),
     (u'adj_close', u'CHH'),
     (u'adj_close', u'CHK'),
     (u'adj_close', u'CHKP'),
     (u'adj_close', u'CHMG'),
     (u'adj_close', u'CHRW'),
     (u'adj_close', u'CHS'),
     (u'adj_close', u'CHSP'),
     (u'adj_close', u'CHTR'),
     (u'adj_close', u'CHUY'),
     (u'adj_close', u'CI'),
     (u'adj_close', u'CIA'),
     (u'adj_close', u'CIDM'),
     (u'adj_close', u'CIEN'),
     (u'adj_close', u'CIM'),
     (u'adj_close', u'CINF'),
     (u'adj_close', u'CIR'),
     (u'adj_close', u'CIT'),
     (u'adj_close', u'CIX'),
     (u'adj_close', u'CKH'),
     (u'adj_close', u'CL'),
     (u'adj_close', u'CLCT'),
     (u'adj_close', u'CLD'),
     (u'adj_close', u'CLDT'),
     (u'adj_close', u'CLDX'),
     (u'adj_close', u'CLF'),
     (u'adj_close', u'CLFD'),
     (u'adj_close', u'CLGX'),
     (u'adj_close', u'CLH'),
     (u'adj_close', u'CLI'),
     (u'adj_close', u'CLNE'),
     (u'adj_close', u'CLR'),
     (u'adj_close', u'CLUB'),
     (u'adj_close', u'CLVS'),
     (u'adj_close', u'CLW'),
     (u'adj_close', u'CLX'),
     (u'adj_close', u'CMA'),
     (u'adj_close', u'CMC'),
     (u'adj_close', u'CMCO'),
     (u'adj_close', u'CMCSA'),
     (u'adj_close', u'CME'),
     (u'adj_close', u'CMG'),
     (u'adj_close', u'CMI'),
     (u'adj_open', u'A'),
     (u'adj_open', u'AA'),
     (u'adj_open', u'AAL'),
     (u'adj_open', u'AAMC'),
     (u'adj_open', u'AAN'),
     (u'adj_open', u'AAOI'),
     (u'adj_open', u'AAON'),
     (u'adj_open', u'AAP'),
     (u'adj_open', u'AAPL'),
     (u'adj_open', u'AAT'),
     (u'adj_open', u'AAWW'),
     (u'adj_open', u'ABAX'),
     (u'adj_open', u'ABBV'),
     (u'adj_open', u'ABC'),
     (u'adj_open', u'ABCB'),
     (u'adj_open', u'ABG'),
     (u'adj_open', u'ABM'),
     (u'adj_open', u'ABMD'),
     (u'adj_open', u'ABT'),
     (u'adj_open', u'ACAD'),
     (u'adj_open', u'ACC'),
     (u'adj_open', u'ACCO'),
     (u'adj_open', u'ACET'),
     (u'adj_open', u'ACGL'),
     (u'adj_open', u'ACHC'),
     (u'adj_open', u'ACHN'),
     (u'adj_open', u'ACIW'),
     (u'adj_open', u'ACLS'),
     (u'adj_open', u'ACM'),
     (u'adj_open', u'ACN'),
     (u'adj_open', u'ACOR'),
     (u'adj_open', u'ACRE'),
     (u'adj_open', u'ACRX'),
     (u'adj_open', u'ACTG'),
     (u'adj_open', u'ACXM'),
     (u'adj_open', u'ADBE'),
     (u'adj_open', u'ADC'),
     (u'adj_open', u'ADES'),
     (u'adj_open', u'ADI'),
     (u'adj_open', u'ADM'),
     (u'adj_open', u'ADMS'),
     (u'adj_open', u'ADP'),
     (u'adj_open', u'ADS'),
     (u'adj_open', u'ADSK'),
     (u'adj_open', u'ADTN'),
     (u'adj_open', u'ADUS'),
     (u'adj_open', u'AE'),
     (u'adj_open', u'AEE'),
     (u'adj_open', u'AEGN'),
     (u'adj_open', u'AEIS'),
     (u'adj_open', u'AEL'),
     (u'adj_open', u'AEO'),
     (u'adj_open', u'AEP'),
     (u'adj_open', u'AERI'),
     (u'adj_open', u'AES'),
     (u'adj_open', u'AET'),
     (u'adj_open', u'AFAM'),
     (u'adj_open', u'AFG'),
     (u'adj_open', u'AFH'),
     (u'adj_open', u'AFL'),
     (u'adj_open', u'AFSI'),
     (u'adj_open', u'AGCO'),
     (u'adj_open', u'AGEN'),
     (u'adj_open', u'AGII'),
     (u'adj_open', u'AGIO'),
     (u'adj_open', u'AGM'),
     (u'adj_open', u'AGN'),
     (u'adj_open', u'AGNC'),
     (u'adj_open', u'AGO'),
     (u'adj_open', u'AGTC'),
     (u'adj_open', u'AGX'),
     (u'adj_open', u'AGYS'),
     (u'adj_open', u'AHC'),
     (u'adj_open', u'AHH'),
     (u'adj_open', u'AHL'),
     (u'adj_open', u'AHP'),
     (u'adj_open', u'AHT'),
     (u'adj_open', u'AI'),
     (u'adj_open', u'AIG'),
     (u'adj_open', u'AIMC'),
     (u'adj_open', u'AIN'),
     (u'adj_open', u'AINV'),
     (u'adj_open', u'AIR'),
     (u'adj_open', u'AIT'),
     (u'adj_open', u'AIV'),
     (u'adj_open', u'AIZ'),
     (u'adj_open', u'AJG'),
     (u'adj_open', u'AKAM'),
     (u'adj_open', u'AKAO'),
     (u'adj_open', u'AKBA'),
     (u'adj_open', u'AKR'),
     (u'adj_open', u'AKRX'),
     (u'adj_open', u'AKS'),
     (u'adj_open', u'AL'),
     (u'adj_open', u'ALB'),
     (u'adj_open', u'ALCO'),
     (u'adj_open', u'ALDR'),
     (u'adj_open', u'ALE'),
     (u'adj_open', u'ALEX'),
     (u'adj_open', u'ALG'),
     (u'adj_open', u'ALGN'),
     (u'adj_open', u'ALGT'),
     (u'adj_open', u'ALIM'),
     (u'adj_open', u'ALK'),
     (u'adj_open', u'ALKS'),
     (u'adj_open', u'ALL'),
     (u'adj_open', u'ALLE'),
     (u'adj_open', u'ALNY'),
     (u'adj_open', u'ALOG'),
     (u'adj_open', u'ALSN'),
     (u'adj_open', u'ALX'),
     (u'adj_open', u'ALXN'),
     (u'adj_open', u'AMAG'),
     (u'adj_open', u'AMAT'),
     (u'adj_open', u'AMBA'),
     (u'adj_open', u'AMBC'),
     (u'adj_open', u'AMBR'),
     (u'adj_open', u'AMC'),
     (u'adj_open', u'AMCX'),
     (u'adj_open', u'AMD'),
     (u'adj_open', u'AME'),
     (u'adj_open', u'AMED'),
     (u'adj_open', u'AMG'),
     (u'adj_open', u'AMGN'),
     (u'adj_open', u'AMKR'),
     (u'adj_open', u'AMNB'),
     (u'adj_open', u'AMP'),
     (u'adj_open', u'AMPE'),
     (u'adj_open', u'AMRC'),
     (u'adj_open', u'AMRS'),
     (u'adj_open', u'AMSC'),
     (u'adj_open', u'AMSF'),
     (u'adj_open', u'AMSWA'),
     (u'adj_open', u'AMT'),
     (u'adj_open', u'AMTD'),
     (u'adj_open', u'AMWD'),
     (u'adj_open', u'AMZN'),
     (u'adj_open', u'ANAT'),
     (u'adj_open', u'ANCX'),
     (u'adj_open', u'ANDE'),
     (u'adj_open', u'ANDV'),
     (u'adj_open', u'ANF'),
     (u'adj_open', u'ANGI'),
     (u'adj_open', u'ANGO'),
     (u'adj_open', u'ANH'),
     (u'adj_open', u'ANIK'),
     (u'adj_open', u'ANIP'),
     (u'adj_open', u'ANSS'),
     (u'adj_open', u'ANTM'),
     (u'adj_open', u'AOI'),
     (u'adj_open', u'AON'),
     (u'adj_open', u'AOS'),
     (u'adj_open', u'AOSL'),
     (u'adj_open', u'AP'),
     (u'adj_open', u'APA'),
     (u'adj_open', u'APAM'),
     (u'adj_open', u'APC'),
     (u'adj_open', u'APD'),
     (u'adj_open', u'APEI'),
     (u'adj_open', u'APH'),
     (u'adj_open', u'APOG'),
     (u'adj_open', u'APTV'),
     (u'adj_open', u'ARAY'),
     (u'adj_open', u'ARC'),
     (u'adj_open', u'ARCB'),
     (u'adj_open', u'ARCC'),
     (u'adj_open', u'ARCW'),
     (u'adj_open', u'ARE'),
     (u'adj_open', u'AREX'),
     (u'adj_open', u'ARI'),
     (u'adj_open', u'ARII'),
     (u'adj_open', u'ARNA'),
     (u'adj_open', u'ARNC'),
     (u'adj_open', u'AROW'),
     (u'adj_open', u'ARQL'),
     (u'adj_open', u'ARR'),
     (u'adj_open', u'ARRS'),
     (u'adj_open', u'ARRY'),
     (u'adj_open', u'ARTNA'),
     (u'adj_open', u'ARW'),
     (u'adj_open', u'ARWR'),
     (u'adj_open', u'ASC'),
     (u'adj_open', u'ASCMA'),
     (u'adj_open', u'ASGN'),
     (u'adj_open', u'ASH'),
     (u'adj_open', u'ASNA'),
     (u'adj_open', u'ASPS'),
     (u'adj_open', u'ASTE'),
     (u'adj_open', u'AT'),
     (u'adj_open', u'ATEC'),
     (u'adj_open', u'ATEN'),
     (u'adj_open', u'ATHN'),
     (u'adj_open', u'ATLO'),
     (u'adj_open', u'ATNI'),
     (u'adj_open', u'ATNM'),
     (u'adj_open', u'ATO'),
     (u'adj_open', u'ATR'),
     (u'adj_open', u'ATRC'),
     (u'adj_open', u'ATRI'),
     (u'adj_open', u'ATRO'),
     (u'adj_open', u'ATRS'),
     (u'adj_open', u'ATSG'),
     (u'adj_open', u'ATU'),
     (u'adj_open', u'ATVI'),
     (u'adj_open', u'AVA'),
     (u'adj_open', u'AVAV'),
     (u'adj_open', u'AVB'),
     (u'adj_open', u'AVD'),
     (u'adj_open', u'AVEO'),
     (u'adj_open', u'AVGO'),
     (u'adj_open', u'AVHI'),
     (u'adj_open', u'AVID'),
     (u'adj_open', u'AVNW'),
     (u'adj_open', u'AVT'),
     (u'adj_open', u'AVX'),
     (u'adj_open', u'AVY'),
     (u'adj_open', u'AWI'),
     (u'adj_open', u'AWK'),
     (u'adj_open', u'AWR'),
     (u'adj_open', u'AXAS'),
     (u'adj_open', u'AXDX'),
     (u'adj_open', u'AXE'),
     (u'adj_open', u'AXL'),
     (u'adj_open', u'AXP'),
     (u'adj_open', u'AXS'),
     (u'adj_open', u'AYI'),
     (u'adj_open', u'AYR'),
     (u'adj_open', u'AZO'),
     (u'adj_open', u'AZPN'),
     (u'adj_open', u'AZZ'),
     (u'adj_open', u'B'),
     (u'adj_open', u'BA'),
     (u'adj_open', u'BABY'),
     (u'adj_open', u'BAC'),
     (u'adj_open', u'BAH'),
     (u'adj_open', u'BANC'),
     (u'adj_open', u'BANF'),
     (u'adj_open', u'BANR'),
     (u'adj_open', u'BAS'),
     (u'adj_open', u'BAX'),
     (u'adj_open', u'BBG'),
     (u'adj_open', u'BBGI'),
     (u'adj_open', u'BBOX'),
     (u'adj_open', u'BBRG'),
     (u'adj_open', u'BBSI'),
     (u'adj_open', u'BBT'),
     (u'adj_open', u'BBW'),
     (u'adj_open', u'BBX'),
     (u'adj_open', u'BBY'),
     (u'adj_open', u'BC'),
     (u'adj_open', u'BCC'),
     (u'adj_open', u'BCEI'),
     (u'adj_open', u'BCO'),
     (u'adj_open', u'BCOR'),
     (u'adj_open', u'BCOV'),
     (u'adj_open', u'BCPC'),
     (u'adj_open', u'BCRX'),
     (u'adj_open', u'BDC'),
     (u'adj_open', u'BDGE'),
     (u'adj_open', u'BDN'),
     (u'adj_open', u'BDSI'),
     (u'adj_open', u'BDX'),
     (u'adj_open', u'BEAT'),
     (u'adj_open', u'BECN'),
     (u'adj_open', u'BELFB'),
     (u'adj_open', u'BEN'),
     (u'adj_open', u'BERY'),
     (u'adj_open', u'BFAM'),
     (u'adj_open', u'BFIN'),
     (u'adj_open', u'BFS'),
     (u'adj_open', u'BF_B'),
     (u'adj_open', u'BG'),
     (u'adj_open', u'BGC'),
     (u'adj_open', u'BGCP'),
     (u'adj_open', u'BGFV'),
     (u'adj_open', u'BGG'),
     (u'adj_open', u'BGS'),
     (u'adj_open', u'BH'),
     (u'adj_open', u'BHB'),
     (u'adj_open', u'BHE'),
     (u'adj_open', u'BHF'),
     (u'adj_open', u'BHGE'),
     (u'adj_open', u'BHLB'),
     (u'adj_open', u'BID'),
     (u'adj_open', u'BIDU'),
     (u'adj_open', u'BIG'),
     (u'adj_open', u'BIIB'),
     (u'adj_open', u'BIO'),
     (u'adj_open', u'BIOL'),
     (u'adj_open', u'BIOS'),
     (u'adj_open', u'BJRI'),
     (u'adj_open', u'BK'),
     (u'adj_open', u'BKCC'),
     (u'adj_open', u'BKD'),
     (u'adj_open', u'BKE'),
     (u'adj_open', u'BKH'),
     (u'adj_open', u'BKMU'),
     (u'adj_open', u'BKS'),
     (u'adj_open', u'BKU'),
     (u'adj_open', u'BLDR'),
     (u'adj_open', u'BLK'),
     (u'adj_open', u'BLKB'),
     (u'adj_open', u'BLL'),
     (u'adj_open', u'BLMN'),
     (u'adj_open', u'BLUE'),
     (u'adj_open', u'BLX'),
     (u'adj_open', u'BMI'),
     (u'adj_open', u'BMRC'),
     (u'adj_open', u'BMRN'),
     (u'adj_open', u'BMS'),
     (u'adj_open', u'BMTC'),
     (u'adj_open', u'BMY'),
     (u'adj_open', u'BNCL'),
     (u'adj_open', u'BNFT'),
     (u'adj_open', u'BOBE'),
     (u'adj_open', u'BOFI'),
     (u'adj_open', u'BOH'),
     (u'adj_open', u'BOKF'),
     (u'adj_open', u'BOOM'),
     (u'adj_open', u'BP'),
     (u'adj_open', u'BPFH'),
     (u'adj_open', u'BPI'),
     (u'adj_open', u'BPOP'),
     (u'adj_open', u'BPTH'),
     (u'adj_open', u'BR'),
     (u'adj_open', u'BRC'),
     (u'adj_open', u'BREW'),
     (u'adj_open', u'BRKL'),
     (u'adj_open', u'BRKR'),
     (u'adj_open', u'BRKS'),
     (u'adj_open', u'BRK_A'),
     (u'adj_open', u'BRK_B'),
     (u'adj_open', u'BRO'),
     (u'adj_open', u'BRS'),
     (u'adj_open', u'BRSS'),
     (u'adj_open', u'BRT'),
     (u'adj_open', u'BSET'),
     (u'adj_open', u'BSFT'),
     (u'adj_open', u'BSRR'),
     (u'adj_open', u'BSTC'),
     (u'adj_open', u'BSX'),
     (u'adj_open', u'BTU'),
     (u'adj_open', u'BTX'),
     (u'adj_open', u'BURL'),
     (u'adj_open', u'BUSE'),
     (u'adj_open', u'BV'),
     (u'adj_open', u'BWA'),
     (u'adj_open', u'BWINB'),
     (u'adj_open', u'BWLD'),
     (u'adj_open', u'BXC'),
     (u'adj_open', u'BXP'),
     (u'adj_open', u'BXS'),
     (u'adj_open', u'BYD'),
     (u'adj_open', u'BZH'),
     (u'adj_open', u'C'),
     (u'adj_open', u'CA'),
     (u'adj_open', u'CAC'),
     (u'adj_open', u'CACC'),
     (u'adj_open', u'CACI'),
     (u'adj_open', u'CAG'),
     (u'adj_open', u'CAH'),
     (u'adj_open', u'CAKE'),
     (u'adj_open', u'CALD'),
     (u'adj_open', u'CALL'),
     (u'adj_open', u'CALM'),
     (u'adj_open', u'CALX'),
     (u'adj_open', u'CAMP'),
     (u'adj_open', u'CAR'),
     (u'adj_open', u'CARA'),
     (u'adj_open', u'CARB'),
     (u'adj_open', u'CASH'),
     (u'adj_open', u'CASS'),
     (u'adj_open', u'CASY'),
     (u'adj_open', u'CAT'),
     (u'adj_open', u'CATM'),
     (u'adj_open', u'CATO'),
     (u'adj_open', u'CATY'),
     (u'adj_open', u'CAVM'),
     (u'adj_open', u'CB'),
     (u'adj_open', u'CBB'),
     (u'adj_open', u'CBG'),
     (u'adj_open', u'CBI'),
     (u'adj_open', u'CBK'),
     (u'adj_open', u'CBL'),
     (u'adj_open', u'CBM'),
     (u'adj_open', u'CBOE'),
     (u'adj_open', u'CBPX'),
     (u'adj_open', u'CBRL'),
     (u'adj_open', u'CBS'),
     (u'adj_open', u'CBSH'),
     (u'adj_open', u'CBT'),
     (u'adj_open', u'CBU'),
     (u'adj_open', u'CBZ'),
     (u'adj_open', u'CCBG'),
     (u'adj_open', u'CCC'),
     (u'adj_open', u'CCE'),
     (u'adj_open', u'CCF'),
     (u'adj_open', u'CCI'),
     (u'adj_open', u'CCK'),
     (u'adj_open', u'CCL'),
     (u'adj_open', u'CCMP'),
     (u'adj_open', u'CCNE'),
     (u'adj_open', u'CCO'),
     (u'adj_open', u'CCOI'),
     (u'adj_open', u'CCRN'),
     (u'adj_open', u'CCXI'),
     (u'adj_open', u'CDE'),
     (u'adj_open', u'CDNS'),
     (u'adj_open', u'CDR'),
     (u'adj_open', u'CE'),
     (u'adj_open', u'CECE'),
     (u'adj_open', u'CECO'),
     (u'adj_open', u'CELG'),
     (u'adj_open', u'CENTA'),
     (u'adj_open', u'CENX'),
     (u'adj_open', u'CERN'),
     (u'adj_open', u'CERS'),
     (u'adj_open', u'CETV'),
     (u'adj_open', u'CEVA'),
     (u'adj_open', u'CF'),
     (u'adj_open', u'CFFI'),
     (u'adj_open', u'CFFN'),
     (u'adj_open', u'CFG'),
     (u'adj_open', u'CFR'),
     (u'adj_open', u'CFX'),
     (u'adj_open', u'CGI'),
     (u'adj_open', u'CGNX'),
     (u'adj_open', u'CHCO'),
     (u'adj_open', u'CHD'),
     (u'adj_open', u'CHDN'),
     (u'adj_open', u'CHE'),
     (u'adj_open', u'CHEF'),
     (u'adj_open', u'CHFC'),
     (u'adj_open', u'CHFN'),
     (u'adj_open', u'CHGG'),
     (u'adj_open', u'CHH'),
     (u'adj_open', u'CHK'),
     (u'adj_open', u'CHKP'),
     (u'adj_open', u'CHMG'),
     (u'adj_open', u'CHRW'),
     (u'adj_open', u'CHS'),
     (u'adj_open', u'CHSP'),
     (u'adj_open', u'CHTR'),
     (u'adj_open', u'CHUY'),
     (u'adj_open', u'CI'),
     (u'adj_open', u'CIA'),
     (u'adj_open', u'CIDM'),
     (u'adj_open', u'CIEN'),
     (u'adj_open', u'CIM'),
     (u'adj_open', u'CINF'),
     (u'adj_open', u'CIR'),
     (u'adj_open', u'CIT'),
     (u'adj_open', u'CIX'),
     (u'adj_open', u'CKH'),
     (u'adj_open', u'CL'),
     (u'adj_open', u'CLCT'),
     (u'adj_open', u'CLD'),
     (u'adj_open', u'CLDT'),
     (u'adj_open', u'CLDX'),
     (u'adj_open', u'CLF'),
     (u'adj_open', u'CLFD'),
     (u'adj_open', u'CLGX'),
     (u'adj_open', u'CLH'),
     (u'adj_open', u'CLI'),
     (u'adj_open', u'CLNE'),
     (u'adj_open', u'CLR'),
     (u'adj_open', u'CLUB'),
     (u'adj_open', u'CLVS'),
     (u'adj_open', u'CLW'),
     (u'adj_open', u'CLX'),
     (u'adj_open', u'CMA'),
     (u'adj_open', u'CMC'),
     (u'adj_open', u'CMCO'),
     (u'adj_open', u'CMCSA'),
     (u'adj_open', u'CME'),
     (u'adj_open', u'CMG'),
     (u'adj_open', u'CMI'),
     (u'close', u'A'),
     (u'close', u'AA'),
     (u'close', u'AAL'),
     (u'close', u'AAMC'),
     (u'close', u'AAN'),
     (u'close', u'AAOI'),
     (u'close', u'AAON'),
     (u'close', u'AAP'),
     (u'close', u'AAPL'),
     (u'close', u'AAT'),
     (u'close', u'AAWW'),
     (u'close', u'ABAX'),
     (u'close', u'ABBV'),
     (u'close', u'ABC'),
     (u'close', u'ABCB'),
     (u'close', u'ABG'),
     (u'close', u'ABM'),
     (u'close', u'ABMD'),
     (u'close', u'ABT'),
     (u'close', u'ACAD'),
     (u'close', u'ACC'),
     (u'close', u'ACCO'),
     (u'close', u'ACET'),
     (u'close', u'ACGL'),
     (u'close', u'ACHC'),
     (u'close', u'ACHN'),
     (u'close', u'ACIW'),
     (u'close', u'ACLS'),
     (u'close', u'ACM'),
     (u'close', u'ACN'),
     (u'close', u'ACOR'),
     (u'close', u'ACRE'),
     (u'close', u'ACRX'),
     (u'close', u'ACTG'),
     (u'close', u'ACXM'),
     (u'close', u'ADBE'),
     (u'close', u'ADC'),
     (u'close', u'ADES'),
     (u'close', u'ADI'),
     (u'close', u'ADM'),
     (u'close', u'ADMS'),
     (u'close', u'ADP'),
     (u'close', u'ADS'),
     (u'close', u'ADSK'),
     (u'close', u'ADTN'),
     (u'close', u'ADUS'),
     ...]




```python
#Show summary statistics

print outg.describe()
```

                 open                                                         \
    ticker          A         AA        AAL        AAMC       AAN       AAOI
    count   21.000000  21.000000  21.000000   21.000000  21.00000  21.000000
    mean    71.753810  54.271905  54.763810  166.567502  40.92619  35.652381
    std      2.208258   1.319730   2.444354  233.518526   1.01858   1.897843
    min     67.420000  52.340000  52.330000   66.950000  39.16000  32.740000
    25%     70.680000  53.550000  52.790000   69.400000  39.98000  34.420000
    50%     72.020000  53.960000  53.650000   75.950000  41.19000  34.980000
    75%     73.770000  54.920000  57.740000   80.200000  41.80000  37.800000
    max     74.480000  57.050000  58.790000  724.662246  42.50000  38.900000

                                                             ...      adj_close  \
    ticker       AAON         AAP        AAPL        AAT     ...           CLVS
    count   21.000000   21.000000   21.000000  21.000000     ...      21.000000
    mean    36.652381  114.896190  174.020952  36.495714     ...      61.407619
    std      0.610425    5.812213    3.670836   0.890222     ...       3.657316
    min     36.000000  100.900000  165.525000  34.900000     ...      54.930000
    25%     36.200000  111.690000  172.530000  36.180000     ...      59.880000
    50%     36.300000  115.670000  174.505000  36.340000     ...      61.400000
    75%     36.950000  119.260000  177.250000  37.110000     ...      62.980000
    max     37.950000  123.520000  179.370000  38.300000     ...      67.720000

                                                                               \
    ticker        CLW         CLX        CMA        CMC       CMCO      CMCSA
    count   21.000000   21.000000  21.000000  21.000000  21.000000  21.000000
    mean    48.400000  143.665714  92.572857  24.820952  42.260952  41.827143
    std      1.343503    1.757668   3.212082   0.610393   1.144980   0.851758
    min     46.150000  140.960000  86.540000  22.770000  40.280000  40.410000
    25%     47.350000  142.250000  90.370000  24.590000  41.380000  41.070000
    50%     48.400000  143.520000  93.810000  24.900000  42.470000  41.980000
    75%     49.400000  144.990000  95.150000  25.160000  42.910000  42.500000
    max     50.300000  146.440000  95.810000  25.820000  44.420000  42.990000


    ticker         CME         CMG         CMI
    count    21.000000   21.000000   21.000000
    mean    152.259524  324.301905  210.572488
    std       2.699462   11.510498  117.866002
    min     144.790000  292.950000  177.060000
    25%     151.730000  319.370000  181.960000
    50%     152.810000  327.340000  183.900000
    75%     154.170000  330.230000  189.080000
    max     155.450000  343.870000  724.662246

    [8 rows x 1908 columns]



```python
outg.plot(x='date', y='close', figsize=(12, 7), kind='line')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fb64fb20dd0>




![png](MILESTONE/images/output_103_1.png)



```python
outg.set_index('date').query("Close Price").sort_values('Close Price', ascending=False).plot.bar(rot=0, width=1)
```


      File "<unknown>", line 1
        Close Price
                  ^
    SyntaxError: invalid syntax




```python

```
