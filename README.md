# Gigaflow Artifact for ASPLOS '25

In this repository, we share the ansible playbook as well as the source code for the various components of the Gigaflow OVS framework as described in the ASPLOS '25 paper.

- OVS Gigaflow - https://github.com/gigaflow-vswitch/gvs.git
- Traffic Generator - https://github.com/gigaflow-vswitch/tgen.git

# Setup

> Note: All dependencies and their installation is managed via Ansible which we run through a `docker` container. The only required dependency for this setup is installing docker. Follow the steps specified at this [link](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) and then allow non-root users to use docker by following these [steps](https://docs.docker.com/engine/install/linux-postinstall/).

The experiment setup requires 3 servers: 
- Collector (to store rulesets/traces and collect logs)
- OVS Device-under-Test (to run `gvs`)
- Tgen (to send/receive traffic)

We use Ansible to orcherstrate all experiments using these three machines. Therefore, we require `root` access to each of them. To populate for each machine, update the `inventory.ini` file as following:

```yml
[NODES]
TGEN ansible_host=<tgen-ip> ansible_user=<tgen-username> ansible_password=<tgen-password> ansible_sudo_pass=<tgen-root-password>
OVS ansible_host=<ovs-ip> ansible_user=<ovs-username> ansible_password=<ovs-password> ansible_sudo_pass=<ovs-root-password>

[STORAGE]
NGAS ansible_host=<collector-ip> ansible_user=<collector-username> ansible_password=<collector-password> ansible_sudo_pass=<collector-root-password> ansible_ssh_user=<collector-username> ansible_ssh_pass=<collector-root-password>
```

# Running Experiments

- Start the Ansible docker by using the following command.
```sh
make ansible
```

- Test connectivity between all three machines:
```sh
make ping
```

- To setup and run all end-to-end and microbenchmark experiments, run the following sequence of commands:
```sh
# retrieve rulesets and traffic from NGAS (collector) and place them on OVS and TGEN
make setup-ovs-accel-experiment

# run end-to-end (ee) experiments and microbenchmarks (bm)
# this will install gvs (gvs with Gigaflow), the traffic generator, and all their dependencies
# and loop over all the available rulesets and microbenchmark configurations
# and for each of them, setup the switch and traffic generators, send/receive the traffic
# and collect OVS/TGEN logs and place them on the NGAS (collector) machine
make run-ovs-accel-experiments

# teardown the experiment: this will uninstall gvs and tgen and clear logs from local machines; logs will remain saved on the NGAS (collector) machine
make teardown-ovs-accel-experiment
```

## Contact Us 
- [Annus Zulfiqar](https://annuszulfiqar2021.github.io/)
- [Ali Imran](https://www.linkedin.com/in/ali-imran-936a30202/)
- [Venkat Kunaparaju](https://www.linkedin.com/in/venkat-kunaparaju-3b8832232/)
- [Ben Pfaff](https://www.linkedin.com/in/ben-pfaff-414a262bb/)
- [Gianni Antichi](https://www.linkedin.com/in/gianniantichi/)
- [Muhammad Shahbaz](https://mshahbaz.gitlab.io/)

