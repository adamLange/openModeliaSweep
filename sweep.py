from joblib import Parallel, delayed
import os
from hashlib import md5
from shutil import copyfile
import numpy as np

outputDir = 'output'

# parameter1 and parameter2 are the parameters to be swept
# there can be more of course, just change the function
# to suit your needs.

def command(parameter1,parameter2): 
  startingDirectory = os.getcwd()
  hshString = '{},{}'.format(parameter1,parameter2) # add all of your paramters to be hashed
  hsh = md5(hshString).hexdigest()

  if os.path.exists(outputDir+'/{}/done'.format(hsh)):
    print('done with this case already')
    os.chdir(startingDirectory)
    return False

  if not os.path.exists(outputDir+'/{}'.format(hsh)):
    os.mkdir(outputDir+'/{}'.format(hsh))

  # copy modelName_init.xml and modelName_info.json to
  # the directory where you will run this script from.
  xmlName = 'modelName_init.xml'
  jsonName = 'modelName_info.json'
  copyfile(xmlName,outputDir+'/{}/{}'.format(hsh,xmlName))
  copyfile(jsonName,outputDir+'/{}/{}'.format(hsh,jsonName))
  os.chdir(outputDir+'/{}'.format(hsh))
  cwd = os.getcwd()

  ovr  = ''
  ovr += "outputFormat=mat\n"
  ovr += "startTime=0\n"
  ovr += 'stopTime=0.2\n'
  ovr += 'stepSize=4e-6\n'
  ovr += 'tolerance=1e-12\n'
  ovr += "variableFilter=.*\n"
  ovr += 'parameter1={}\n'.format(parameter1)
  ovr += 'parameter2={}\n'.format(parameter2)

  f = open('override.txt','w')
  f.write(ovr)
  f.close()

  # modelName is the executable created by omc compiler
  # change to match the name of your executable.
  # Copy the executable into the directory where you
  # run this script from.
  cmd = "../../modelName "\
        +"-r=output.mat ".format(hsh)\
        +"-overrideFile=override.txt "\
        +"-jacobian=coloredNumerical -noEventEmit -w -lv=LOG_STATS"

  os.system(cmd)
  os.system('touch done')
  os.chdir(startingDirectory)
  return True

# This might be a little confusing, but this is
# simply doing a parallel, nested for loop.
Parallel(n_jobs=4)(delayed(command)(cr,afr,exh,T_inlet,prf)
  for parameter1 in np.linspace(0,10)
  for parameter2 in np.linspace(0,5)
  )


#Alternatively, you could use nested for loops:
#
#
#for parameter1 in np.linspace(0,10):
#
#  for parameter2 in np.linspace(0,5):
#
#    command(paramater1,parameter2)
#

