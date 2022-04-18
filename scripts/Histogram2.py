import altair as alt
from vega_datasets import data

iris = data.iris()

xrange = (3, 9)
yrange = (1, 6)

points = alt.Chart(iris).mark_circle().encode(
    alt.X('sepalLength', scale=alt.Scale(domain=xrange)),
    alt.Y('sepalWidth', scale=alt.Scale(domain=yrange)),
    color='species',
)

top_hist = alt.Chart(iris).mark_area(
    opacity=.4, interpolate='step'
).encode(
    alt.X('sepalLength:Q', 
          bin=alt.Bin(maxbins=20, extent=xrange), 
          stack=None, 
          scale=alt.Scale(domain=xrange),
         ),
    alt.Y('count(*):Q', 
          stack=None, 
         ),
    alt.Color('species:N'),
).properties(height=60)

right_hist = alt.Chart(iris).mark_area(
    opacity=.4, interpolate='step'
).encode(
    alt.Y('sepalWidth:Q', 
          bin=alt.Bin(maxbins=20, extent=yrange), 
          stack=None,
          scale=alt.Scale(domain=yrange),
         ),
    alt.X('count(*):Q', 
          stack=None, 
         ),
    alt.Color('species:N'),
).properties(width=60)

chart = top_hist & (points | right_hist)

chart.save('outputFiles/Tophistogram.html')