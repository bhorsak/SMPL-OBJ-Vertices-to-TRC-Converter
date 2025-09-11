# SMPL Vertices to TRC Converter  

This repository provides a Python script to convert **SMPL mesh outputs** (e.g. from CameraHMR, see References, or similar) into **trc files** for use in biomechanics and motion analysis software (e.g., OpenSim).  

The script searches through a given folder hierarchy, extracts marker positions from `.obj` files using predefined vertex IDs, and writes the results into TRC files.  

---

## Features  
- Is compatible with **OpenCap folder structure**.  
- Looks for  a **user-defined folder** (e.g., `CameraHMR`, etc.).  
- Recursively searches subfolders for `.obj` files.  
- Extracts marker positions using predefined **SMPL vertex IDs**.  
- Automatically saves results to `MarkerData_<tag>` folders, preserving the folder hierarchy.  

---

## Requirements  
- Python 3.8+
- It expects the *.obj files to be consecutively numbered *_1.obj, *_2.obj, etc. (see data example)
- The following Python packages:  
  ```bash
  pip install numpy
  ```
---

## User Settings  

Inside the script you must set the following parameters:  

- **`initial_marker_vertices`**: Dictionary mapping marker names (e.g., `RASI`, `LASI`) to SMPL vertex IDs.  
- **`frame_rate`**: Frame rate at which the `.obj` files were generated.  
- **`root_folder`**: Path to the root folder containing the OpenCap data.  
- **`search_tag`**: The folder to search for (e.g., `"CameraHMR"`).  

Example configuration in the script:  
```python
frame_rate = 60
root_folder = r".\data"
search_tag = "CameraHMR"
```

---

## Usage  

1. Place your *.obj data in the `data/` directory (or set `root_folder` to another location).  
2. Adjust the **user settings** in the script (`frame_rate`, `root_folder`, `search_tag`).  
3. Run the script:  
   ```bash
   python smpl_to_trc.py
   ```
4. Output TRC files will be written to a folder named `MarkerData_<search_tag>` at the same hierarchy level as the source folder. 

Example:  
```
data/
└── Subject01/
    └── CameraHMR/
        └── Trial01/
            ├── frame_000.obj
            ├── frame_001.obj
            └── ...
```

After running for example with `search_tag = "CameraHMR"`, you will get:  
```
data/
└── Subject01/
    └── MarkerData_CameraHMR/
        └── Trial01.trc
```

---

## Author  
- **Brian Horsak** – brian.horsak@fhstp.ac.at  
- Updated by ChatGPT, 03/2025


## Citing
If you use this code please consider to cite the following paper since this code was developed during this study:

Horsak, B., Simonlehner, M., Quehenberger, V., Dumphart, B., Slijepčević, D., Kranzl, A., 2025. A gait lab in your pocket? Accuracy and reliability of monocular smartphone-based markerless 3D gait analysis in pathological gait. Gait & Posture, ESMAC 2025 Abstract 121, 91–92. https://doi.org/10.1016/j.gaitpost.2025.07.102

@article{horsakGaitLabYour2025,
  title = {A Gait Lab in Your Pocket? {{Accuracy}} and Reliability of Monocular Smartphone-Based Markerless {{3D}} Gait Analysis in Pathological Gait},
  shorttitle = {A Gait Lab in Your Pocket?},
  author = {Horsak, Brian and Simonlehner, Mark and Quehenberger, Viktoria and Dumphart, Bernhard and Slijep{\v c}evi{\'c}, Djordje and Kranzl, Andreas},
  year = {2025},
  journal = {Gait \& Posture},
  series = {{{ESMAC}} 2025 {{Abstract}}},
  volume = {121},
  pages = {91--92},
  issn = {0966-6362},
  doi = {10.1016/j.gaitpost.2025.07.102}
}



## SMPL Reference
The code was based on output SMPL/OBJ files using CameraHMR: 

Patel, P., Black, M.J., 2024. CameraHMR: Aligning People with Perspective. https://doi.org/10.48550/arXiv.2411.08128

@misc{patelCameraHMRAligningPeople2024,
  title = {{{CameraHMR}}: {{Aligning People}} with {{Perspective}}},
  shorttitle = {{{CameraHMR}}},
  author = {Patel, Priyanka and Black, Michael J.},
  year = {2024},
  number = {arXiv:2411.08128},
  eprint = {2411.08128},
  primaryclass = {cs},
  publisher = {arXiv},
  doi = {10.48550/arXiv.2411.08128},
  archiveprefix = {arXiv},
}

