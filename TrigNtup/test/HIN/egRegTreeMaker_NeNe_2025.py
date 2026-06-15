isCrabJob=False #script seds this if its a crab job

# Import configurations
import FWCore.ParameterSet.Config as cms
import os
import sys
# set up process
from Configuration.Eras.Era_Run3_2025_NEON_cff import Run3_2025_NEON
process = cms.Process("EGREGTREE",Run3_2025_NEON)

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis') 
options.register('isMC',True,options.multiplicity.singleton,options.varType.bool," whether we are running on MC or not")
options.parseArguments()

print(options.inputFiles)
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles),  
                          )


# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(5000),
    limit = cms.untracked.int32(10000000)
)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

#Load geometry
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag

#gt doesnt really matter much as no reco but nice to get it right
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_mcRun3_2025_forNeNe_realistic_v9', '')


process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Geometry.CaloEventSetup.CaloTowerConstituents_cfi")
process.load("Configuration.StandardSequences.Services_cff")

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputFile)
)

process.egRegTreeMaker = cms.EDAnalyzer("EGRegTreeMaker",
                                        verticesTag = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                        rhoTag = cms.InputTag("fixedGridRhoFastjetAllTmp"),
                                        genPartsTag = cms.InputTag("prunedGenParticles"),
                                        puSumTag = cms.InputTag("addPileupInfo"),
                                        scTag = cms.VInputTag("particleFlowSuperClusterECAL:particleFlowSuperClusterECALBarrel","particleFlowSuperClusterECAL:particleFlowSuperClusterECALEndcapWithPreshower"),
                                        scAltTag = cms.VInputTag("particleFlowSuperClusterECALNoThres:particleFlowSuperClusterECALBarrel","particleFlowSuperClusterECALNoThres:particleFlowSuperClusterECALEndcapWithPreshower"),
                                        ecalHitsEBTag = cms.InputTag("reducedEgamma","reducedEBRecHits"),
                                        ecalHitsEETag = cms.InputTag("reducedEgamma","reducedEERecHits"),
                                        elesTag = cms.InputTag("slimmedElectrons"), 
                                        phosTag = cms.InputTag("slimmedPhotons"),
                                        elesAltTag = cms.VInputTag(),
                                        phosAltTag = cms.VInputTag()
                                        )

process.egRegTreeMaker.verticesTag = cms.InputTag("offlinePrimaryVertices")
process.egRegTreeMaker.rhoTag = cms.InputTag("fixedGridRhoFastjetAllTmp")
process.egRegTreeMaker.genPartsTag = cms.InputTag("genParticles")
process.egRegTreeMaker.elesTag = cms.InputTag("gedGsfElectrons")
process.egRegTreeMaker.phosTag = cms.InputTag("gedPhotons")
process.egRegTreeMaker.ecalHitsEBTag = cms.InputTag("reducedEcalRecHitsEB")
process.egRegTreeMaker.ecalHitsEETag = cms.InputTag("reducedEcalRecHitsEE")

process.load("SHarper.TrigNtup.rePFSuperCluster_cff")

process.p = cms.Path(process.rePFSuperClusterThresSeq*process.egRegTreeMaker)

# Add HI FJ rho
centralityTable = cms.vdouble(
    0, 4.10985, 4.77625, 5.26157, 5.68513, 6.07021, 6.42387, 6.75839, 7.07004, 7.37778, 7.68672, 7.98486, 8.28043, 8.57545, 8.86176, 9.14369, 9.42725, 9.71304, 10.0147, 10.3105, 10.6073, 10.9038, 11.2042, 11.5095, 11.8193, 12.1275, 12.446, 12.7678, 13.095, 13.4164, 13.7444, 14.0892, 14.4311, 14.784, 15.1463, 15.5155, 15.8793, 16.2598, 16.6363, 17.0308, 17.4318, 17.8363, 18.2507, 18.6695, 19.1158, 19.5598, 20.0042, 20.4468, 20.9093, 21.3787, 21.8542, 22.3545, 22.8449, 23.3585, 23.8655,
    24.3914, 24.928, 25.4831, 26.0269, 26.6125, 27.1776, 27.7521, 28.3604, 28.9708, 29.5734, 30.2092, 30.8553, 31.5125, 32.1607, 32.8557, 33.5435, 34.248, 34.9785, 35.7214, 36.4689, 37.2423, 38.0336, 38.8336, 39.651, 40.464, 41.3046, 42.1642, 43.0373, 43.9275, 44.8478, 45.784, 46.6997, 47.6568, 48.6178, 49.6245, 50.6359, 51.6727, 52.7001, 53.7518, 54.8302, 55.9117, 57.0425, 58.1931, 59.375, 60.5682, 61.7735, 62.9594, 64.1904, 65.4397, 66.7374, 68.0604, 69.3719, 70.7033, 72.0891, 73.4636,
    74.8995, 76.3443, 77.8348, 79.3369, 80.8528, 82.3963, 83.9709, 85.5451, 87.1865, 88.8456, 90.4798, 92.1981, 93.9828, 95.7577, 97.5642, 99.4073, 101.278, 103.22, 105.137, 107.099, 109.138, 111.174, 113.263, 115.385, 117.522, 119.691, 121.983, 124.244, 126.547, 128.864, 131.327, 133.831, 136.317, 138.873, 141.404, 144.05, 146.784, 149.55, 152.275, 155.033, 157.909, 160.833, 163.726, 166.732, 169.794, 172.864, 176.065, 179.353, 182.606, 185.968, 189.345, 192.925, 196.385, 199.963,
    203.548, 207.266, 211.009, 214.894, 218.785, 222.834, 226.924, 231.082, 235.36, 239.681, 244.136, 248.668, 253.374, 258.162, 263.07, 268.116, 273.287, 278.555, 284.024, 289.552, 295.42, 301.42, 307.779, 314.293, 321.209, 328.506, 336.377, 344.46, 353.27, 362.966, 373.42, 385.572, 399.896, 416.711, 439.198, 473.479, 752.978
)
from SHarper.TrigNtup.hiFJRhoProducer import addHiFJRho
process = addHiFJRho(process, table=centralityTable, label="PFhf")
