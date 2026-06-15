from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

# We want to put all the CRAB project directories from the tasks we submit here into one common directory.
# That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
from CRABClient.UserUtilities import config
config = config()

date = '2026_05_30'
config.section_("General")
config.General.workArea = 'crab_projects/'+date
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = "../HIN/egRegTreeMaker_lowPtGsdElectron_UPC_2024.py"
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 750

config.section_('Data')
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publication = False
config.Data.allowNonValidInputDataset = True
config.Data.inputDBS = 'phys03'

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
dataMap["LowPtGsfEle_DoubleElectron_FlatPt0p5To50_RealEcalIC" ] = { "PD": "/PGUN_5p36TeV_2024Run3/anstahll-DoubleElectron_FlatPt0p5To50_PGUN_2024Run3_RECO_2026_05_18-4a3eb98bd450897871fde3aa25de1b83/USER" }
dataMap["LowPtGsfEle_DoubleElectron_FlatPt0p5To50_IdealEcalIC"] = { "PD": "/PGUN_5p36TeV_2024Run3/anstahll-DoubleElectron_FlatPt0p5To50_ECALIdealIC_PGUN_2024Run3_RECO_2026_05_18-cd9d857126dc4ed312c597677ad5b38a/USER" }

## Submit the muon PDs
for key, val in dataMap.items():
    config.General.requestName = 'EGTree_'+key+'_UPC_MC_HIRun2024_'+date
    config.Data.inputDataset = val["PD"]
    config.Data.outputDatasetTag = config.General.requestName
    config.Data.outLFNDirBase = '/store/group/phys_heavyions/anstahll/CERN/PbPb2024/NTUple/EGTree/'+date

    print("Submitting CRAB job for: "+val["PD"])
    submit(config)
