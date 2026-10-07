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
