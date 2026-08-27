"""Shared SONICOM data loading utilities for the DAFx 2026 HRTF tutorial notebooks."""
import os
import glob

import numpy as np
import sofar as sf


def load_real_sonicom(path):
    """Load one real SONICOM subject from a single .sofa file."""
    sofa = sf.read_sofa(path)
    hrir = sofa.Data_IR                      # [n_positions, 2, n_taps]
    positions = sofa.SourcePosition           # [n_positions, 3]: az, el, dist
    fs = sofa.Data_SamplingRate
    return hrir, positions, fs


def load_real_sonicom_dir(dir_path):
    """Load every *.sofa file in dir_path as one subject each.
    Assumes all subjects share the same measurement grid (true for SONICOM)."""
    paths = sorted(glob.glob(os.path.join(dir_path, "*.sofa")))
    if not paths:
        raise ValueError(f"No .sofa files found in {dir_path}")
    all_hrir, positions, fs, subject_ids = [], None, None, []
    for p in paths:
        hrir_i, positions_i, fs_i = load_real_sonicom(p)
        if positions is None:
            positions, fs = positions_i, fs_i
        all_hrir.append(hrir_i)
        subject_ids.append(os.path.splitext(os.path.basename(p))[0])
    hrir = np.stack(all_hrir, axis=0)  # [n_subjects, n_positions, 2, n_taps]
    return hrir, positions, np.array(subject_ids), fs


def synthesize_sonicom_like(n_subjects=5, n_taps=200, fs=44100):
    """Fake but grid-accurate SONICOM-style sampling + toy HRIRs, so a
    notebook is runnable before real .sofa files are wired up."""
    azimuths = np.arange(0, 360, 5)  # 72 azimuths

    def elevations_for(az):
        # SONICOM: every 10 deg between -30/30, every 15 deg outside, single pole sample at +90
        dense = np.arange(-30, 31, 10)
        sparse_low = np.arange(-45, -30, 15)
        sparse_high = np.arange(45, 91, 15)
        return np.concatenate([sparse_low, dense, sparse_high])

    rows = []
    for az in azimuths:
        for el in elevations_for(az):
            if el == 90 and az != 0:
                continue  # only one measurement at the pole, per SONICOM spec
            rows.append((az, el, 1.5))
    positions = np.array(rows, dtype=np.float32)  # ~793 rows
    n_dir = positions.shape[0]

    t = np.arange(n_taps) / fs
    hrir = np.zeros((n_subjects, n_dir, 2, n_taps), dtype=np.float32)
    for s in range(n_subjects):
        head_radius_scale = 0.85 + 0.3 * np.random.rand()
        for d in range(n_dir):
            az_rad = np.deg2rad(positions[d, 0])
            itd = 0.0006 * np.sin(az_rad) * head_radius_scale
            for ear, sign in enumerate([-1, 1]):
                delay = max(0.0, itd * sign + 0.001)
                env = np.exp(-t / (0.0008 + 0.0002 * np.random.rand()))
                carrier = np.sin(2 * np.pi * (1500 + 300 * ear) * (t - delay))
                hrir[s, d, ear] = (env * carrier).astype(np.float32)
    subject_ids = np.array([f"synthetic_{i:02d}" for i in range(n_subjects)])
    return hrir, positions, subject_ids, fs


def hrir_to_hrtf_db(hrir_1d, fs, n_fft=512):
    """FFT a single 1D HRIR to (freqs, magnitude in dB)."""
    spec = np.fft.rfft(hrir_1d, n=n_fft)
    freqs = np.fft.rfftfreq(n_fft, d=1 / fs)
    mag_db = 20 * np.log10(np.abs(spec) + 1e-8)
    return freqs, mag_db


def hrir_to_log_mag(hrir_batch, n_freq_bins, n_fft=512):
    """FFT a batch of HRIRs (any leading shape) to log-magnitude, truncated to n_freq_bins."""
    spec = np.fft.rfft(hrir_batch, n=n_fft, axis=-1)
    return 20 * np.log10(np.abs(spec) + 1e-8)[..., :n_freq_bins]
