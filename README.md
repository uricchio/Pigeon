# Multimodal selection and the evolution of plumage on a changing planet

Code in this directory corresponds to the analyses presented in Wright-Lichter et al,
"Multimodal selection and the evolution of plumage on a changing planet." Instructions 
for generating each of the figures are included below.

## Code installation

The code uses a `setup.py` file to install. If you have `Python3` installed, you should be able to install the source by 
running `python setup.py install` at the command line. If you do not have root priveleges, you can try `python setup.py install --user`.

There is a second set of source files in the directory `simpleSimCode`. To install this software, `cd` into this directory and run the 
same command (`python setup.py install`) as above.

Some additional software may be required to run some of the commands. This includes [`numpy`](https://numpy.org/), [`scipy`](https://scipy.org/), and [`mpmath`](https://mpmath.org/). 

## Data

To make the data for the figures, first run `./makeAnalyticalFigData.sh` and `./makeFigures.sh`. The latter file may take some time (minutes) to execute.

## Figures

### Figure 1
To make Figure 1, first run `./makeAnalyticalFigData.sh`. To plot the data, use the `R` script in `scripts/ModelFigs.R`.

### Figures 2 & 3
To make Figures 2 and 3, first run `./makeFigures.sh`. To plot the data, use the R script in `scripts/empPhoenixTemp.R`. This script uses data from
the file 'tempData/Phoenix.tMax.1940.txt', which includes max daily temperatures (converted to Celcius) from Phoenix in 1940. The original data from the weather station is contained in the file  `tempData/Phoenix.GHCND:USW00023183.tMax.csv`.

### Figures 4 & 5
To make Figures 4 and 5, first run `./makeFigures.sh`. The code for plotting thess figures is contained in `scripts/popGenModels.R`.

