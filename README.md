# Gigaflow Artifact for ASPLOS '25

In this repository, we share the ansible playbook as well as the source code for the various components of the Gigaflow OVS framework as described in the ASPLOS '25 paper.

- OVS Gigaflow - https://github.com/gigaflow-vswitch/gvs.git
- Traffic Generator - https://github.com/gigaflow-vswitch/tgen.git

## Setup

> Note: All dependencies and their installation is managed via Ansible which we run through a `docker` container. The only required dependency for this setup is installing docker. Follow the steps specified at this [link](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) and then allow non-root users to use docker by following these [steps](https://docs.docker.com/engine/install/linux-postinstall/).

The experiment setup requires 3 servers: 
- Collector (to store rulesets/traces and collect logs)
- OVS Device-under-Test (to run `gvs`)
- Tgen (to send/receive traffic)

We use ansible to orcherstrate all experiments using these three machines. Therefore, we require `root` access to each of them. To populate for each machine, update the `inventory.ini` file as following:

```yml
[NODES]
TGEN ansible_host=<tgen-ip> ansible_user=<tgen-username> ansible_password=<tgen-password> ansible_sudo_pass=<tgen-root-password>
OVS ansible_host=<ovs-ip> ansible_user=<ovs-username> ansible_password=<ovs-password> ansible_sudo_pass=<ovs-root-password>

[STORAGE]
NGAS ansible_host=<collector-ip> ansible_user=<collector-username> ansible_password=<collector-password> ansible_sudo_pass=<collector-root-password> ansible_ssh_user=<collector-username> ansible_ssh_pass=<collector-root-password>
```

## Usage

- Start the ansible docker by using the following command.
```sh
make ansible
```

## Contact Us 
- [Annus Zulfiqar](https://annuszulfiqar2021.github.io/)
- [Ali Imran](https://www.linkedin.com/in/ali-imran-936a30202/)
- [Venkat Kunaparaju](https://www.linkedin.com/in/venkat-kunaparaju-3b8832232/)
- [Ben Pfaff](https://www.linkedin.com/in/ben-pfaff-414a262bb/)
- [Gianni Antichi](https://www.linkedin.com/in/gianniantichi/)
- [Muhammad Shahbaz](https://mshahbaz.gitlab.io/)

