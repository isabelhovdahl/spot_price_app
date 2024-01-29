#!/usr/bin/env python
# coding: utf-8

# In[119]:


import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from dash import Dash, dcc, html


# In[120]:


#from dash import jupyter_dash
#jupyter_dash.default_mode = 'external'


# In[121]:


import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css'


# # Electricity price dashboard

# **Get data**

# In[17]:


# Import data
df = pd.read_csv('2023_01_DayAheadPrices_12.1.D.csv', sep = '\t')

# Convert to datetime
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Choose 60 min resolution (only Austria and Germany offers 15 min resolution)
df = df[df['ResolutionCode'] == 'PT60M'].copy()

#print(df['MapCode'].nunique())
#print(df['DateTime'].nunique())
#df


# In[125]:


# Extract Bergen price area
df_no5 = df[df['MapCode'] == 'NO5'].copy()

# Extract first day
subset = df_no5[(df_no5['DateTime'].dt.month == 1) & (df_no5['DateTime'].dt.day == 1)].copy()
subset.sort_values('DateTime', inplace = True)
subset.set_index('DateTime', inplace = True)

#subset


# In[126]:


# Create the desired time range
t_index = pd.DatetimeIndex(pd.date_range(start = '2023-01-01 00:00:00', end = '2023-01-01 23:59:00', freq = '15min'))
#t_index = pd.DatetimeIndex(pd.date_range(start = subset.index.min(), end = subset.index.max() + pd.Timedelta(minutes = 59), freq = '15min'))

# Resample
subset_new = subset.reindex(t_index, method = 'ffill')
#subset_new


# **Line plot**

# In[127]:


fig = px.line(
    subset_new,
    y = 'Price',
    line_shape='hv'
)

fig.update_layout(
    title = 'Day-ahead prices', 
    title_x = 0.5,
    xaxis_title = 'Time [Hours]',
    yaxis_title = 'Price per MTU [EUR / MWh]',
    xaxis_tickformat = '%H:%M',
    hovermode="x unified"
)



# **Table**

# In[166]:


subset_tab = subset.reset_index().rename(columns = {'Price' : 'Day-ahead price'})
subset_tab['DateTime'] = subset_tab['DateTime'].dt.strftime('%H:%M')
subset_tab['temp'] = subset_tab['DateTime'].shift(-1)
subset_tab.fillna('00:00', inplace = True)
subset_tab['MTU'] = subset_tab['DateTime'] + ' - ' + subset_tab['temp']

subset_tab = subset_tab[['MTU', 'Day-ahead price']].copy()

#subset_tab


# In[167]:


table = dbc.Table.from_dataframe(subset_tab, striped=True, bordered=True, hover=True)


# **Create app**

# In[168]:


app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP, dbc_css])
server = app.server

text = """Data is extracted from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)."""

app.layout = dbc.Container(
    children = [
        
        # Header
        html.H1('Electricity price dashboard'),
        dcc.Markdown(text),
        
        # Add graph
        dcc.Graph(figure = fig),
        
        # Add table
        table
        
        
    ],
    className = 'dbc'
)
if __name__ == '__main__':
    app.run(debug = True)


# In[ ]:





# In[ ]:




