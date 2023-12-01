# tomorrow
# remake figures for sims with correcion added
# fix calc of d_A-d_a in new pigeon sim and see if that gets it to work
# CHECK 1. make phoenix temp dist figure with best fit dist for summer months (skew normal)
# CHECK 2. remake the figure with inc and decreasing (d_A-d_a) proportions of the dist
# CHECK 3. make sim figure showing how outcomes can range
# CHECK 4. work on pigeon sims (more realistic version of earlier ones)

# make temp data
#python simpleSimCode/scripts/tempParams.py > tempData/Phoenix.TMax.params.txt
#python simpleSimCode/scripts/tempParamsNY.py > tempData/NewYork.TMax.params.txt

# make plots of d_A-d_a
#python simpleSimCode/scripts/tempAbove_x_T.py  > tempData/diff_dA_da.x_T.txt
#python simpleSimCode/scripts/tempAbove_x_TNY.py  > tempData/diff_dA_da.x_T.NY.txt

# simulate pop-gen for different T thresholds
# first argument is dx_T, difference in UCT between morphs 
# second argument is rate per yaer of increase in mean temp (in degrees C)
#python simpleSimCode/scripts/sim.py  2 0.02 > simData/sim.dx_T.2.d.0.02.txt
#python simpleSimCode/scripts/sim.py  0.5 0.05 > simData/sim.dx_T.0.5.d.0.05.txt
#python simpleSimCode/scripts/sim.py  0.5 0.1 > simData/sim.dx_T.0.5.d.0.1.txt

# simulate pigeon populations
python scripts/simPigeonPop.py 0.02 /Users/telemacher/projects/Pigeon/tempData/Phoenix.GHCND:USW00023183.tMax.csv > simData/sim.Pigeon.d.0.02.Phoenix.txt
python scripts/simPigeonPop.py 0.1 /Users/telemacher/projects/Pigeon/tempData/Phoenix.GHCND:USW00023183.tMax.csv  > simData/sim.Pigeon.d.0.1.Phoenix.txt
python scripts/simPigeonPop.py 0.02 /Users/telemacher/projects/Pigeon/tempData/Manhattan.GHCND:USW00094728.tMax.csv > simData/sim.Pigeon.d.0.02.Manhattan.txt
python scripts/simPigeonPop.py 0.1 /Users/telemacher/projects/Pigeon/tempData/Manhattan.GHCND:USW00094728.tMax.csv > simData/sim.Pigeon.d.0.1.Manhattan.txt

