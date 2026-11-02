"""nm000405 (review-1102): verify Julien's 2 Nov statement and build movement-onset events.

Rule (authors' neuromodulation/ECoG_vs_STN `Figure 1/Feature Plot/Feature Mean.ipynb`): onsets where
np.diff(y > 0) == 1, y = MOV_*_CLEAN, subjects 000 001 004-010 013 014 (49 runs).
Counts computed several ways: per run (pure rising edges), per run including a >0 segment that starts at the
first sample, and per session with the runs concatenated in run order (as the notebooks concatenate).
Writes OUT/summary.json and OUT/events/<relpath>_events.tsv (one row per >0 segment).
Data: annexed .eeg/.vhdr/.vmrk fetched read-only from the public NEMAR S3 by key (sha256 checked).
"""
import glob, json, os, re, sys
import numpy as np
import mne

sys.path.insert(0, sys.argv[3])
import s3fetch  # noqa: E402

mne.set_log_level("ERROR")
REPO, OUT = sys.argv[1], sys.argv[2]
SUBS = ['000', '001', '004', '005', '006', '007', '008', '009', '010', '013', '014']
TAB = dict(zip(SUBS, [128, 464, 213, 285, 381, 84, 161, 131, 547, 86, 205]))
os.makedirs(f"{OUT}/events", exist_ok=True)


def runkey(p):
    return int(re.search(r'run-(\d+)', p).group(1))


summary = {"runs": {}, "per_subject": {}, "table1": TAB}
for s in SUBS:
    per = {"rise": 0, "rise_plus_start": 0, "concat_session": 0, "n_runs": 0, "segments_at_start": 0}
    for sesdir in sorted(glob.glob(f"{REPO}/sub-{s}/ses-*")):
        vh = sorted((os.path.relpath(p, REPO) for p in glob.glob(f"{sesdir}/ieeg/*_ieeg.vhdr")), key=runkey)
        conc = {"LEFT": [], "RIGHT": []}
        for v in vh:
            b = v[:-5]
            loc = s3fetch.materialize(REPO, [b + ".vhdr", b + ".vmrk", b + ".eeg"], "/work/nm000405", ds="nm000405")
            raw = mne.io.read_raw_brainvision(loc[b + ".vhdr"], preload=True)
            sf = raw.info["sfreq"]
            rows = []
            rr = {"sfreq": float(sf), "n_times": int(raw.n_times)}
            for side in ("LEFT", "RIGHT"):
                x = raw.get_data(picks=[f"MOV_{side}_CLEAN"])[0]
                conc[side].append(x)
                pos = x > 0
                d = np.diff(pos.astype(np.int8))
                st = [int(i) for i in np.flatnonzero(d == 1) + 1]
                en = [int(i) for i in np.flatnonzero(d == -1) + 1]
                at0 = bool(pos[0])
                if at0:
                    st = [0] + st
                if pos[-1]:
                    en = en + [len(x)]
                assert len(st) == len(en)
                rr[f"rise_{side}"] = int((d == 1).sum())
                rr[f"start_at_0_{side}"] = at0
                rr[f"open_end_{side}"] = bool(pos[-1])
                for a, e in zip(st, en):
                    rows.append((a / sf, (e - a) / sf, int(a), f"movement_onset_{side.lower()}" if a > 0 else f"movement_ongoing_at_start_{side.lower()}",
                                 f"MOV_{side}_CLEAN", float(x[a:e].max()), "yes" if e == len(x) else "no"))
            rows.sort(key=lambda r: (r[0], r[3]))
            # events file name: drop the desc entity (sidecars of these runs are named without desc)
            ev = re.sub(r"_desc-[^_]+_ieeg$", "_events.tsv", b)
            os.makedirs(os.path.dirname(f"{OUT}/events/{ev}"), exist_ok=True)
            with open(f"{OUT}/events/{ev}", "w") as f:
                f.write("onset\tduration\tsample\ttrial_type\tsource_channel\tpeak_value\tends_at_recording_end\n")
                for r in rows:
                    f.write(f"{r[0]:.3f}\t{r[1]:.3f}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]:.6g}\t{r[6]}\n")
            rr["n_rows"] = len(rows)
            summary["runs"][b] = rr
            per["rise"] += rr["rise_LEFT"] + rr["rise_RIGHT"]
            per["segments_at_start"] += int(rr["start_at_0_LEFT"]) + int(rr["start_at_0_RIGHT"])
            per["n_runs"] += 1
            print(b, json.dumps(rr), flush=True)
        for side in ("LEFT", "RIGHT"):
            y = np.concatenate(conc[side])
            per["concat_session"] += int((np.diff((y > 0).astype(np.int8)) == 1).sum())
    per["rise_plus_start"] = per["rise"] + per["segments_at_start"]
    per["table1"] = TAB[s]
    summary["per_subject"][s] = per
    print(s, json.dumps(per), flush=True)
tot = {k: sum(v[k] for v in summary["per_subject"].values()) for k in ("rise", "rise_plus_start", "concat_session", "n_runs", "segments_at_start")}
tot["table1"] = sum(TAB.values())
tot["match_table1_rise"] = sum(v["rise"] == v["table1"] for v in summary["per_subject"].values())
tot["match_table1_concat"] = sum(v["concat_session"] == v["table1"] for v in summary["per_subject"].values())
summary["totals"] = tot
json.dump(summary, open(f"{OUT}/summary.json", "w"), indent=1)
print("TOTALS", json.dumps(tot))
print("DONE")
