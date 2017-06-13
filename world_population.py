import json

import urllib.request

import pygal.maps.world

from pygal.style import LightColorizedStyle as LCS, RotateStyle as RS
from pygal_maps_world.maps import World

from country_codes import get_country_code

# Load data
with urllib.request.urlopen("http://data.okfn.org/data/core/population/r/population.json") as url:
    data = json.loads(url.read().decode())

# Build a dictionary of population data.
cc_populations = {}
for pop_dict in data:
    if pop_dict['Year'] == '2014':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        code = get_country_code(country_name)
        if code:
            cc_populations[code] = population

# Group the countries into 3 population levels.
tier_1, tier_2, tier_3 = {}, {}, {}
for cc, pop in cc_populations.items():
    if pop < 10000000:
        tier_1[cc] = pop
    elif pop < 1000000000:
        tier_2[cc] = pop
    else:
        tier_3[cc] = pop

# See how many countries are in each level.
print(len(tier_1), len(tier_2), len(tier_3))

wm_style = RS('#336699', base_style=LCS)
wm = World(style=wm_style)
wm.title = 'World Population in 2014, by Country'
wm.add('0-10m', tier_1)
wm.add('10m-1bn', tier_2)
wm.add('>1bn', tier_3)

wm.render_to_file('world_population.svg')
