import os

# main
DIR = os.path.abspath(os.path.dirname(__file__))
IMGDIR = os.path.join(DIR, 'imgs')
DATADIR = os.path.join(DIR, 'data')
LOGFILENAME = raw_input("Participant: ")
LOGFILE = os.path.join(DATADIR, LOGFILENAME)

# display
DISPTYPE = 'pygame'
DISPSIZE = (1280,1024)

# validation points
#PXY = [0.15, 0.5, 0.85]
PXhor = [0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 0.65, 0.8, 0.85, 0.9, 0.95]
PYhor = [0.15, 0.5, 0.85]
CALIBPOINTShor = []
for y in PYhor:
    for x in PXhor:
        if y != 0.5:
            CALIBPOINTShor.append((int(x*DISPSIZE[0]),(int(y*DISPSIZE[1]))))
                else:
                    CALIBPOINTShor.append((int((1-x)*DISPSIZE[0]),(int(y*DISPSIZE[1]))))

PXver = [0.15, 0.5, 0.85]
PYver = [0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 0.65, 0.8, 0.85, 0.9, 0.95]
CALIBPOINTSver = []
for x in PXver:
    for y in PYver:
        if x != 0.5:
            CALIBPOINTSver.append((int(x*DISPSIZE[0]),(int(y*DISPSIZE[1]))))
                else:
                    CALIBPOINTSver.append((int(x*DISPSIZE[0]),(int((1-y)*DISPSIZE[1]))))

# images
IMAGES = []
for imgname in os.listdir(IMGDIR):
    IMAGES.append(os.path.join(IMGDIR, imgname))

# light-dark
PUPTRIALS = 10
SACTRIALS = 10

# timing
ITIval = 100
ITI = 1000
POINTTIME = 2000
IMGTIME = 10000
BASELINETIME = 200
PUPTRIALTIME = 2500

# trackers
TRACKERTYPE = 'eyetribe'
DUMMYMODE = False
