import FWCore.ParameterSet.Config as cms

def addHiFJRho(process, table=None, tag=None, label=None, isMiniAOD=False):
    if table:
        process.centralityBin = cms.EDProducer('HICentralityBinProducer', table = table)
    else:
        process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
    if tag:
        process.GlobalTag.snapshotTime = cms.string("9999-12-31 23:59:59.000")
        process.GlobalTag.toGet.extend([
            cms.PSet(
                record = cms.string("HeavyIonRcd"),
                tag = cms.string(tag),
                connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
                label = cms.untracked.string(label)
            ),
        ])
    process.centralityBin.Centrality = cms.InputTag("hiCentrality")
    process.centralityBin.centralityVariable = cms.string(label)
    from RecoHI.HiJetAlgos.hiPuRhoProducer_cfi import hiPuRhoProducer
    process.hiPuRhoForSC = hiPuRhoProducer.clone(src = 'towerMaker')
    process.egRegTreeMaker.centTag = cms. InputTag(f"centralityBin:{label}")
    process.egRegTreeMaker.etaMapTag = cms.InputTag("hiPuRhoForSC:mapEtaEdges")
    process.egRegTreeMaker.rhoMapTag = cms.InputTag("hiPuRhoForSC:mapToRho")

    process.rhoSeq = cms.Sequence(process.centralityBin * process.hiPuRhoForSC)
    process.p.insert(0,process.rhoSeq)

    if isMiniAOD:
        process.load('RecoHI.HiJetAlgos.PackedPFTowers_cfi')
        process.rhoSeq.insert(0,process.PackedPFTowers)
        process.hiPuRhoForSC.src = "PackedPFTowers"

    return process
