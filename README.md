[![DOI](https://img.shields.io/badge/DOI-10.82901%2Fnemar.nm000405-blue)](https://doi.org/10.82901/nemar.nm000405)

# Intraoperative ECoG + STN LFP during grip force in Parkinson's disease (Merk et al. 2022)

Replication data for: Merk T. et al. (2022) "Electrocorticography is superior to subthalamic local field potentials
for movement decoding in Parkinson's disease", eLife 11:e75126, https://doi.org/10.7554/eLife.75126.
Source: Harvard Dataverse, https://doi.org/10.7910/DVN/IO2FLM (v1.0, 2022-04-19), licence CC0 1.0.

16 participants with Parkinson's disease (University of Pittsburgh Medical Center), 73 runs of an intraoperative grip-force
task recorded during bilateral STN-DBS lead implantation. Each run contains a subdural ECoG strip over sensorimotor
cortex (ECOG_*), the four contacts of the DBS lead in the subthalamic nucleus (STN_*, where present), and grip-force
channels (MOV_LEFT/MOV_RIGHT; MOV_*_CLEAN are the authors' noise- and drift-cleaned force traces).
Sessions `ses-left` / `ses-right` are the hemispheres as labelled by the authors.

## Why this is a derivative dataset
The paper states that ECoG and STN signals were filtered (0.3-7.5 kHz) and digitised at 30 kHz (Grapevine, Ripple Inc)
and that "all signals were resampled to 1 kHz for offline analysis". The released signals are these 1 kHz resampled
signals, so this deposit is labelled `DatasetType: derivative` and every signal file carries `desc-1kHz`. Values are
exactly those of the Dataverse release (BrainVision float32); only file names and folders changed.

## Changes relative to the Dataverse release
- Files sorted into `sub-*/ses-*/ieeg/` (Dataverse stores them flat). Data files renamed `..._desc-1kHz_ieeg.*`; the
  DataFile/MarkerFile lines in .vhdr/.vmrk follow the new names.
- Per-run `space-mni_electrodes.tsv` tables merged into one per session (identical contacts; force channels dropped).
- `*_ieeg.json`: hardware/filter/reference facts added from the paper methods (the release said "BrainProducts", which is
  the pybv writer default, not the amplifier).
- `participants.tsv`: the column `center_ID` (hospital DBS case numbers) is removed for privacy, also from the sourcedata copy.
- Not deposited: `ea_ui.mat`, `ea_ui-1.mat`, `ea_ui-2.mat` (Lead-DBS GUI state files, no data).
- `sourcedata/dataverse-IO2FLM/`: all other original metadata files as released (incl. per-subject `sub-*_electrodes*.tsv`
  in mm and the per-run electrode tables; `-1` suffixes are Dataverse duplicate-name renames).

## Not stated by the source (left as n/a)
Age and handedness per participant (the paper's Table 1 lists 11 patients and does not map onto these 16 IDs);
the exact MNI template; anti-aliasing filter used for resampling.

## Ethics
Informed consent was obtained under protocol #PRO13110420 approved by the Institutional Review Board of the University
of Pittsburgh (paper methods).

## Additional metadata and localisation (added 2026-10-08)

Compiled after the upload from the article, its supplement and the source deposit (each statement names its source). Text and sidecar metadata only; no data file was changed.

**Recording system.** Signals were acquired with a Grapevine neural interface processor (Ripple Inc): ECoG and STN signals filtered at 0.3–7.5 kHz, amplified and digitised at 30 kHz, then resampled to 1 kHz for offline analysis (paper, Methods "Electrophysiological recordings"). The deposit files are BrainVision (`Manufacturer` "BrainProducts" in the sidecar, i.e. the export format) at SamplingFrequency 1000 Hz with PowerLineFrequency 60 (all 73 `*_ieeg.json`). The deposit's `iEEGReference` is n/a.

**Reference scheme.** The montage was referential, with the reference electrode in the scalp and the ground over the acromion process. STN LFPs from all four contacts were referenced offline in a bipolar montage (paper, Methods).

**Electrode types.** ECoG came from subdural strips placed temporarily through standard frontal burr holes near the coronal suture, aimed posteriorly toward the hand-knob motor cortex. Strips had six contacts (left n=5 patients, right n=3), eight contacts (left 3, right 3) or twenty-eight contacts (left 2, right 2). STN LFP came from the clinical DBS lead (Medtronic model 3389, 4 contacts). Details are in Supplementary file 1a of the paper. Source: paper, Methods.

**Localisation method.** For the subdural strips, preoperative MRI, intraoperative fluoroscopy and postoperative CT were aligned (Randazzo et al. 2016). CT and MRI were co-registered with SPM and rendered with Osirix v7.5 and FreeSurfer v5.3. Contacts were projected from the fluoroscopic image onto the cortical surface. The DBS contacts were reconstructed with Lead-DBS: preoperative MRI and postoperative CT were co-registered and normalised to MNI 2009b NLIN ASYM space. All contacts were "localized and transformed into MNI space" (paper, Methods "Electrode localization"; Figure 1B; coordinates in Figure 1—source data 1, elife-75126-fig1-data1.csv). The deposit has subject-level `sub-XXX_electrodes*.tsv` (mm, coordsystem "MNI") for all 16 subjects. The session-level `*_space-mni_electrodes.tsv` of this dataset carry the same positions in metres; their column `atlas_label_AAL3v1` adds an AAL3v1 atlas lookup of these coordinates (ieeg-atlas `coord_regions.py`, nearest labelled voxel; a derived label, not given by the authors). STN contacts are in the subthalamic nucleus per their channel names; AAL3 has no STN label, so their lookup names the nearest AAL3 structure.

## Units correction (2026-10-16)

The released BrainVision headers declare 0.1 µV per stored unit, but with that scaling every subject's median channel standard deviation is 1.8e7-7.3e7 µV (18-73 V), which is physically impossible for ECoG/STN LFP. The release does not state the true unit, so the voltage channels are now labelled `n/a` in channels.tsv. The stored values are unchanged; relative amplitudes within a recording are unaffected. Review: NEMAR curator, 2026-10-15 (the same recording is also in nm000466).

2026-10-17: the four movement channels (`MOV_RIGHT`, `MOV_LEFT`, `MOV_RIGHT_CLEAN`, `MOV_LEFT_CLEAN`, type MISC) are now also labelled `n/a` in channels.tsv, because nothing in the release shows they are in µV. Values unchanged.

## Reading with MNE (added 2026-10-17, version 1.0.4)

MNE and MNE-BIDS take the scale from the BrainVision header, not from channels.tsv. The headers still declare
`0.1 µV` per stored unit for every channel, so `mne_bids.read_raw_bids` / `mne.io.read_raw_brainvision` return the ECoG
and STN channels with standard deviations of tens of volts (robust SD 1.7e7-4.0e7 µV in the runs checked on
2026-10-17). These numbers are not physical voltages: treat the ECoG/STN values as arbitrary units (channels.tsv `n/a`,
see "Units correction"); relative amplitudes within a recording are unaffected. The amplitudes would be typical
ECoG/LFP values (tens of µV) if divided by 1e6, but the release does not state the scale, so no factor is applied here.
The same holds for the movement channels (`MOV_*`): their headers say µV, channels.tsv `n/a`. The `.vhdr` headers are
left as released.
