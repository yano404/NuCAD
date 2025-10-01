# NuCAD

![PyPI - Version](https://img.shields.io/pypi/v/nucad)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nucad)
[![Publish to PyPI](https://github.com/yano404/NuCAD/actions/workflows/pypi.yml/badge.svg)](https://github.com/yano404/NuCAD/actions/workflows/pypi.yml)

NuCAD is a CAD tool focused on designing nuclear physics experimental instruments.


## Getting Started

### NuCAD Installation via PIP

```
pip install nucad
```

NuCAD depends on [CadQuery](https://github.com/CadQuery/cadquery) and [OCP](https://github.com/CadQuery/OCP).
If you have any troubles, consider to install cadquery using `mamba`.

```
mamba create -n nucad -c conda-forge \
  python=3.12 numpy cadquery ocp
mamba activate nucad
pip install pycatima nucad
```

### Using NuCAD in Apptainer

1. Clone the apptainer definition file.
  ```
  git clone https://github.com/yano404/nucad_apptainer.git
  ```

2. Build SIF container.
  ```
  cd nucad_apptainer
  apptainer build nucad.sif nucad.def
  ```

3. Run the container.
  ```
  apptainer run nucad.sif
  ```

4. Visit http://localhost:54321 in your web browser.
   You will see Jupyter Lab running on the port.

### Building NuCAD from Source

1. Clone this repository.
  ```sh
  git clone https://github.com/yano404/NuCAD.git
  ```
2. Build NuCAD by using `uv` .
  ```sh
  cd /path/to/nucad
  uv build
  ```
3. Install NuCAD to your enviroment.
  ```sh
  pip install .
  ```


## License

Copyright (c) 2025 Takayuki YANO

The source code is licensed under the MIT License, see LICENSE.