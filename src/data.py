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
