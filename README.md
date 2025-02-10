# Gigaflow Artifact for ASPLOS '25

In this repository, we share the ansible playbook as well as the source code for the various components of the Gigaflow OVS framework as described in the ASPLOS '25 paper.

- OVS Gigaflow - https://github.com/Gigaflow-Cache/ovs-gigaflow.git
- Traffic Generator - https://github.com/Gigaflow-Cache/traffic-generator.git

## Usage

- First, clone this repository and its submodules.
```
git clone https://github.com/Gigaflow-Cache/Gigaflow-Artifact-ASPLOS2025.git artifact-asplos25
cd artifact-asplos25 && git submodule update --init --recursive
```

- Second, start the ansible docker by using the following command.
```
make ansible
```

## Contact Us 
- [Annus Zulfiqar](https://annuszulfiqar2021.github.io/)
- [Ali Imran](https://www.linkedin.com/in/ali-imran-936a30202/)
- [Venkat Kunaparaju](https://www.linkedin.com/in/venkat-kunaparaju-3b8832232/)
- [Ben Pfaff](https://www.linkedin.com/in/ben-pfaff-414a262bb/)
- [Gianni Antichi](https://www.linkedin.com/in/gianniantichi/)
- [Muhammad Shahbaz](https://mshahbaz.gitlab.io/)

