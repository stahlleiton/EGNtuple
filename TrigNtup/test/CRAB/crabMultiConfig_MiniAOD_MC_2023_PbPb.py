from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

# We want to put all the CRAB project directories from the tasks we submit here into one common directory.
# That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
from CRABClient.UserUtilities import config
config = config()

date = '2026_06_11'
config.section_("General")
config.General.workArea = 'crab_projects/'+date
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = "../HIN/egRegTreeMaker_MiniAOD_PbPb_2023.py"
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 750

config.section_('Data')
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'global'

config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_US_*', 'T2_US_Caltech', 'T2_US_Wisconsin', 'T2_US_Nebraska', 'T2_US_Purdue', 'T2_US_UCSD', 'T2_CH_CERN']

def submit(config):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))

#############################################################################################
## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
#############################################################################################

dataMap = {}
dataMap["DoubleElectron_FlatPt1To500_RealEcalIC"] = { "PD": "/EE_FlatPT-1to500_TuneCP5_5p36TeV_Pythia8PtGun/HINPbPbSpring23MiniAOD-forCalibration_132X_mcRun3_2023_realistic_HI_v9-v2/MINIAODSIM" }
dataMap["DoublePhoton_FlatPt10To500_RealEcalIC"] = { "PD": "/GG_FlatPT-10to500_TuneCP5_5p36TeV_Pythia8PtGun/HINPbPbSpring23MiniAOD-forCalibration_132X_mcRun3_2023_realistic_HI_v9-v2/MINIAODSIM" }
dataMap["DoubleElectron_FlatPt1To500_IdealEcalIC"] = { "PD": "/EE_FlatPT-1to500_TuneCP5_5p36TeV_Pythia8PtGun/HINPbPbSpring23MiniAOD-ECALIdealIC_forCalibrationECALIdealIC_132X_mcRun3_2023_realistic_HI_v9-v2/MINIAODSIM" }
dataMap["DoublePhoton_FlatPt10To500_IdealEcalIC"] = { "PD": "/GG_FlatPT-10to500_TuneCP5_5p36TeV_Pythia8PtGun/HINPbPbSpring23MiniAOD-ECALIdealIC_forCalibrationECALIdealIC_132X_mcRun3_2023_realistic_HI_v9-v2/MINIAODSIM" }

## Submit the muon PDs
for key, val in dataMap.items():
    config.General.requestName = 'EGTree_'+key+'_Hydjet_MiniAOD_MC_HIRun2023_'+date
    config.Data.inputDataset = val["PD"]
    config.Data.outputDatasetTag = config.General.requestName
    config.Data.outLFNDirBase = '/store/group/phys_heavyions/anstahll/CERN/PbPb2023/NTUple/EGTree/'+date

    print("Submitting CRAB job for: "+val["PD"])
    submit(config)
