
# make figure of frequency changes
python scripts/PigeonAnalyticsDelQ.py > modelData/delQ.txt

# make figure of d/dq of del-q
python scripts/PigeonAnalyticsd-dQ.py > modelData/DdelQ.txt

# mmake data for figure of d_a-d_A
python scripts/PigeonAnalytics-da-dA.py > modelData/da-dA.txt

