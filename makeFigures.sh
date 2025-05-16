# make temp data
python simpleSimCode/scripts/tempParams.py > tempData/Phoenix.TMax.params.txt
python simpleSimCode/scripts/tempParamsNY.py > tempData/NewYork.TMax.params.txt

# make data for plots of d_A-d_a
python simpleSimCode/scripts/tempAbove_x_T.py  > tempData/diff_dA_da.x_T.txt
python simpleSimCode/scripts/tempAbove_x_TNY.py  > tempData/diff_dA_da.x_T.NY.txt

# simulate pop-gen for different T thresholds
# first argument is dx_T, difference in UCT between morphs 
# second argument is rate per year of increase in mean temp (in degrees C)
python simpleSimCode/scripts/sim.py  0.5 0.05 noFlip > simData/sim.dx_T.0.5.d.0.05.noFlip.txt
python simpleSimCode/scripts/sim.py  0.5 0.05 Flip > simData/sim.dx_T.0.5.d.0.05.Flip.txt

python simpleSimCode/scripts/sim.py 1 0.05 noFlip > simData/sim.dx_T.1.d.0.05.noFlip.txt
python simpleSimCode/scripts/sim.py 1 0.05 Flip > simData/sim.dx_T.1.d.0.05.Flip.txt

# simulate pigeon populations
python scripts/simPigeonPop.py 0.02 tempData/Phoenix.GHCND:USW00023183.tMax.csv > simData/sim.Pigeon.d.0.02.Phoenix.txt
python scripts/simPigeonPop.py 0.1 tempData/Phoenix.GHCND:USW00023183.tMax.csv  > simData/sim.Pigeon.d.0.1.Phoenix.txt
python scripts/simPigeonPop.py 0.02 tempData/Manhattan.GHCND:USW00094728.tMax.csv > simData/sim.Pigeon.d.0.02.Manhattan.txt
python scripts/simPigeonPop.py 0.1 tempData/Manhattan.GHCND:USW00094728.tMax.csv > simData/sim.Pigeon.d.0.1.Manhattan.txt

