import random
import numpy as np
import matplotlib.pyplot as plt
#  import matplotlib.ticker as ticker


# Run Set up

number_of_external_iterations = 1      # Decision iterations, leave value as 1, to run only uncertainty. The idea is to couple any optimizer in the future
number_of_internal_iterations = 1000  # uncertainty iteration numbers
break_statement = 30000                # to get out of the loop in advance or by prevention.
total_iterations_counter = 0
external_counter = 1
internal_counter = 0

# Data Entry

CTE = 7758                      # constant for Field units 

area_mode = 2000                # Area in acre
area_mult_min = 0.85
area_mult_max = 1.05

thickness_mode = 80             # thickness in ft
thickness_mult_min = 0.85
thickness_mult_max = 1.1

ntg_min = 0.8                   # Net To Gross in fraccion
ntg_max = 1.0

porosity_mu = 0.20              # Porosity in fraccion
porosity_sigma = 0.00025

swi_mu = 0.105                  # Swi in fraccion
swi_sigma = 0.0002
swi_histogram = []

boi_min = 1.05                  # Boi in RB/STB
boi_max = 1.12

# ouput variables

area_histogram = []
thickness_histogram = []
ntg_histogram = []
poro_histogram = []
boi_histogram = []
ooip_histogram = []

print(f'| TotalIte | ExterIte | IterInter | Area (Acre)| Thicknes (ft)|  NTG  | porosity |  Swi |  Boi  | OOIP (Mstb) |')


while external_counter < number_of_external_iterations + 1:
    while internal_counter < number_of_internal_iterations:
        # print(external_counter, internal_counter)
        internal_counter += 1   # contador = contador + 1
        total_iterations_counter += 1

        area_iteracion = random.triangular(area_mode * area_mult_min, area_mode * area_mult_max, area_mode)
        area_histogram.append(area_iteracion)
        
        thickness_iteracion = random.triangular(thickness_mode * thickness_mult_min, thickness_mode * thickness_mult_max, thickness_mode)
        thickness_histogram.append(thickness_iteracion)
        
        ntg_iteracion = random.uniform(ntg_min, ntg_max)
        ntg_histogram.append(ntg_iteracion)
        
        poro_iteracion = random.normalvariate(porosity_mu, porosity_sigma)
        poro_histogram.append(poro_iteracion)      
        
        swi_iteracion = (-0.66 * poro_iteracion + 0.215) * random.uniform(0.998, 1.002)
        swi_histogram.append(swi_iteracion) 
        
        #swi_iteracion = random.normalvariate(swi_mu, swi_sigma)
        #swi_histogram.append(swi_iteracion)  
        
        boi_iteracion = random.uniform(boi_min, boi_max)
        boi_histogram.append(boi_iteracion) 

        ooip_iteracion = (CTE * area_iteracion * thickness_iteracion * ntg_iteracion * poro_iteracion * (1 - swi_iteracion) / boi_iteracion) / 1e6
        ooip_histogram.append(ooip_iteracion)   

        print(f'| {total_iterations_counter:8d} | {external_counter:9d}| {internal_counter:8} | {round(area_iteracion,2):12}| {round(thickness_iteracion,3):13}| {round(ntg_iteracion,2):6}| {round(poro_iteracion,4):10}| {round(swi_iteracion,3):5}| {round(boi_iteracion,3):6}| {round(ooip_iteracion,3):12}| ')
        if (internal_counter >= break_statement):
            break

    external_counter += 1
    internal_counter =0

# print(ooip_histogram)
# print(poro_histogram)

#  fig, ooip = plt.subplots()

fig = plt.figure(figsize = (15, 15))
fig.tight_layout()
#  ax1 = fig.add_subplot(1,2,1)

plt.style.use('tableau-colorblind10')
plt.rcParams.update({'figure.autolayout': True})

plt.subplot(421)
area_results = plt.hist(area_histogram, bins = 100)
plt.xlabel('Area (acres)')
plt.show()

plt.subplot(422)
thickness_results = plt.hist(thickness_histogram, bins = 100)
plt.xlabel('Thickness (ft)')
plt.show()

plt.subplot(423)
ntg_results = plt.hist(ntg_histogram,  bins = 100)
plt.xlabel('NTG')
plt.show()

plt.subplot(424)
poro_results = plt.hist(poro_histogram, bins = 100)  
plt.xlabel('Poro')
plt.show()

plt.subplot(425)
swi_results = plt.hist(swi_histogram,  bins = 100)
plt.xlabel('Swi')
plt.show()

plt.subplot(426)
boi_results = plt.hist(boi_histogram,  bins = 100)
plt.xlabel('Boi')
plt.show()
 
plt.subplot(427)
plt.scatter(poro_histogram ,swi_histogram)
plt.xlabel('Poro')
plt.ylabel('Swi')
plt.show()

plt.subplot(428)
ooip_results = plt.hist(ooip_histogram, bins = 100)
plt.yscale('linear')
plt.xscale('linear')
# plt.title('OOIP')
plt.xlabel('OOIP (MSTB')
# plt.ylabel('Probability')
# plt.axis([40, 160, 0, 0.03])
# plt.grid(True)
plt.show()

plt.savefig('OOIP_plots.pdf')
