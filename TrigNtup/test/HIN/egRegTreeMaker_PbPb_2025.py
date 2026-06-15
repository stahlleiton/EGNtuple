isCrabJob=False #script seds this if its a crab job

# Import configurations
import FWCore.ParameterSet.Config as cms
import os
import sys
# set up process
from Configuration.Eras.Era_Run3_pp_on_PbPb_2025_cff import Run3_pp_on_PbPb_2025
process = cms.Process("EGREGTREE",Run3_pp_on_PbPb_2025)

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
process.GlobalTag = GlobalTag(process.GlobalTag, '151X_mcRun3_2025_realistic_HI_v5', '')


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
    0, 15.2567, 16.5869, 17.7164, 18.7771, 19.8259, 20.8725,
    21.9415, 23.03, 24.1338, 25.2921, 26.5003, 27.7502, 29.0122,
    30.3343, 31.6946, 33.1416, 34.6258, 36.1713, 37.7827, 39.4411,
    41.1718, 42.9749, 44.8974, 46.883, 48.9524, 51.0916, 53.3323,
    55.6408, 58.0649, 60.6023, 63.2016, 65.9605, 68.8081, 71.7928,
    74.8417, 78.0372, 81.2674, 84.7142, 88.2653, 91.973, 95.756,
    99.7385, 103.87, 108.155, 112.658, 117.341, 122.085, 126.984,
    132.198, 137.547, 143.113, 148.798, 154.851, 161.124, 167.461,
    174.005, 180.891, 187.872, 195.069, 202.626, 210.502, 218.482,
    226.854, 235.309, 243.996, 252.974, 262.408, 271.848, 281.74,
    292.053, 302.543, 313.054, 324.202, 335.351, 346.907, 358.679,
    370.716, 383.175, 395.552, 408.729, 422.268, 436.014, 450.042,
    464.405, 478.717, 493.898, 509.325, 524.957, 540.665, 557.062,
    573.763, 590.998, 608.356, 626.246, 644.608, 663.452, 682.563,
    701.84, 721.494, 741.886, 762.783, 784.176, 805.609, 827.874,
    850.059, 873.245, 896.555, 920.424, 944.915, 969.848, 994.383,
    1019.8, 1045.85, 1072.34, 1099.59, 1126.62, 1154.3, 1182.62,
    1211.94, 1241.59, 1271.28, 1301.61, 1332.56, 1363.79, 1396.02,
    1428.41, 1460.9, 1494.94, 1529.72, 1565.02, 1600.6, 1636.24,
    1672.45, 1709.28, 1747.01, 1785.14, 1823.74, 1863.64, 1903.22,
    1943.11, 1985.32, 2026.87, 2069.91, 2113.73, 2157.51, 2202.34,
    2247.96, 2294.12, 2341.64, 2390.25, 2439.25, 2489.06, 2538.66,
    2590.97, 2644.1, 2696.53, 2750.01, 2804.87, 2860.73, 2915.77,
    2972.64, 3029.84, 3090.17, 3150.83, 3212, 3275.72, 3338.62,
    3402.85, 3469.18, 3533.52, 3601.27, 3669.84, 3739.15, 3809.53,
    3883.17, 3958.06, 4033.4, 4110.77, 4190.74, 4270.28, 4351.17,
    4433.83, 4518.34, 4603.65, 4691.6, 4780.52, 4871.81, 4965.45,
    5059.63, 5158.9, 5258.13, 5361.17, 5467.02, 5574.72, 5683.76,
    5795.82, 5916.42, 6052.37, 6230.91, 7380.58
)
from SHarper.TrigNtup.hiFJRhoProducer import addHiFJRho
process = addHiFJRho(process, table=centralityTable, label="HFtowers")
