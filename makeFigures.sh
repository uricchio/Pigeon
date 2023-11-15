# tomorrow
# CHECK 1. make phoenix temp dist figure with best fit dist for summer months (skew normal)
# CHECK 2. remake the figure with inc and decreasing (d_A-d_a) proportions of the dist
# 3. make sim figure showing how outcomes can range
# 4. work on pigeon sims (more realistic version of earlier ones)
# 5. add NCZ

# make Phoenix temp data
#python simpleSimCode/scripts/tempParams.py > tempData/Phoenix.TMax.params.txt

# make plots of d_A-d_a
#python simpleSimCode/scripts/tempAbove_x_T.py 38 > tempData/diff_dA_da.x_T.txt


# simulate pop-gen for different T thresholds
# first argument to the script is the temp at which recessive aa birds 
# experience their upper critical threshold (UCT)
# second argument is dx_T, difference in UCT between morphs 
# third argument is rate per yaer of increase in mean temp (in degrees C)
python simpleSimCode/scripts/sim.py  2 0.02 > simData/sim.dx_T.2.d.0.02.txt
python simpleSimCode/scripts/sim.py  0.5 0.05 > simData/sim.dx_T.0.5.d.0.05.txt
python simpleSimCode/scripts/sim.py  0.5 0.1 > simData/sim.dx_T.0.5.d.0.1.txt
