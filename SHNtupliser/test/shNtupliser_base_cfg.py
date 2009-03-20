#shamelessly stolen from PatAnalyzerSkeleton_cfg.py

# Import configurations
import FWCore.ParameterSet.Config as cms

# set up process
process = cms.Process("HEEPAnalyzer")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkSummary = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(500),
    limit = cms.untracked.int32(10000000)
)
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(500),
    limit = cms.untracked.int32(10000000)
)
process.MessageLogger.suppressWarning = cms.untracked.vstring("selectedLayer1Hemispheres") #a noisy module with silly warnings
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATLayer0Summary')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATLayer0Summary = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

# Load geometry
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('IDEAL_V9::All')
process.load("Configuration.StandardSequences.MagneticField_cff")


process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

#from PhysicsTools.PatAlgos.patLayer0_cff import *
#from PhysicsTools.PatAlgos.patLayer1_cff import  *
#time to patify things with custom heep settings
#process.load("PhysicsTools.PatAlgos.patLayer0_cff")
#process.load("PhysicsTools.PatAlgos.patLayer1_cff")
process.load("SHarper.HEEPAnalyzer.HEEPPatConfig_cfi");
#from SHarper.HEEPAnalyzer.HEEPPatConfig_cfi import *

# input heep analyzer sequence
process.load("SHarper.HEEPAnalyzer.HEEPAnalyzer_cfi")
process.load("SHarper.SHNtupliser.shNtupliser_cfi")
process.shNtupliser.datasetCode = DATASETCODE
process.shNtupliser.sampleWeight = SAMPLEWEIGHT
process.shNtupliser.outputFilename="OUTPUTFILE"

process.source = cms.Source ("PoolSource",fileNames = cms.untracked.vstring('dummy'))

process.PoolSource.fileNames = ['file:/scratch/sharper/cmsswDataFiles/zee_relVal_219.root']



# define path 'p': PAT Layer 0, PAT Layer 1, and the analyzer
process.p = cms.Path(#process.patLayer0*
                     #process.patLayer1)
#                     process.eleIsoDepositEcalFromHitsFast*
#                     process.eleIsoDepositEcalFromHits*
#                      process.eleIsoDepositHcalFromHits*
                     process.heepPATSequence*
                     process.shNtupliser)


# load the pat layer 1 event content
#process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")

# setup event content: drop everything before PAT
#process.patEventContent = cms.PSet(
#    outputCommands = cms.untracked.vstring('drop *')
#)

# extend event content to include PAT objects
#process.patEventContent.outputCommands.extend(process.patLayer1EventContent.outputCommands)


# talk to output module
#process.out = cms.OutputModule("PoolOutputModule",
#    process.patEventSelection,
#    process.patEventContent,
#    verbose = cms.untracked.bool(False),
#    fileName = cms.untracked.string('PatAnalyzerSkeletonSkim.root')
#)

# define output path
#process.outpath = cms.EndPath(process.out)

