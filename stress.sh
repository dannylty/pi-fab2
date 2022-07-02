#!/bin/bash
fab2 p '.local/bin/stressberry-run -n $HOSTNAME -d 900 stress_${HOSTNAME}.out'
fab2 p 'sudo mv stress_${HOSTNAME}.out share/stressberry/stress_${HOSTNAME}.out'
PREFIX="share/stressberry/stress_"
ssh pi@pi0 -t "MPLBACKEND=Agg stressberry-plot ${PREFIX}pi0.out ${PREFIX}pi1.out ${PREFIX}pi2.out ${PREFIX}pi3.out -o sb.png && sudo mv sb.png share/stressberry/sb.png"

