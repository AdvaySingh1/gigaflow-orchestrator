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
GVS ansible_host=<ovs-ip> ansible_user=<ovs-username> ansible_password=<ovs-password> ansible_sudo_pass=<ovs-root-password>

[STORAGE]
COLLECTOR ansible_host=<collector-ip> ansible_user=<collector-username> ansible_password=<collector-password> ansible_sudo_pass=<collector-root-password> ansible_ssh_user=<collector-username> ansible_ssh_pass=<collector-root-password>
```

# Usage

- Start the Ansible docker by using the following command.
```sh
make ansible
```

- Test connectivity between all three machines:
```sh
make ping
```

Run all the following commands from within this Ansible docker container.

## Run All Experiments (End-to-End and Microbenchmarks)

To setup and run all end-to-end and microbenchmark experiments, run the following sequence of commands:

```sh
# retrieve rulesets and traffic from COLLECTOR and place them on OVS and TGEN
# this will also install gvs (gvs with Gigaflow), the traffic generator, and all their dependencies
make setup-gvs-experiment

# run end-to-end (ee) experiments and microbenchmarks (bm)
# and loop over all the available rulesets and microbenchmark configurations
# and for each of them, setup the switch and traffic generators, send/receive the traffic
# and collect OVS/TGEN logs and place them on the COLLECTOR machine
make run-gvs-experiment

# teardown the experiment: this will uninstall gvs and tgen and clear logs from local machines; logs will remain saved on the COLLECTOR machine
make teardown-gvs-experiment
```

## Run End-to-End Experiments

To setup and run only end-to-end experiments:

```sh
# retrieve rulesets and traffic from COLLECTOR and place them on OVS and TGEN
# this will also install gvs (gvs with Gigaflow), the traffic generator, and all their dependencies
make setup-gvs-experiment

# run end-to-end (ee) experiments and microbenchmarks (bm)
# and loop over all the available rulesets and for each of them, setup the switch and traffic generators, send/receive the traffic
# and collect OVS/TGEN logs and place them on the COLLECTOR machine
make run-gvs-ee-experiment

# teardown the experiment: this will uninstall gvs and tgen and clear logs from local machines; logs will remain saved on the COLLECTOR machine
make teardown-gvs-experiment
```

## Run Microbenchmarks
To setup and run only microbenchmark experiments:

```sh
# retrieve rulesets and traffic from COLLECTOR and place them on OVS and TGEN
# this will also install gvs (gvs with Gigaflow), the traffic generator, and all their dependencies
make setup-gvs-experiment

# run end-to-end (ee) experiments and microbenchmarks (bm)
# and loop over all the available rulesets and for each of them, setup the switch and traffic generators, send/receive the traffic
# and collect OVS/TGEN logs and place them on the COLLECTOR machine
make run-gvs-bm-experiment

# teardown the experiment: this will uninstall gvs and tgen and clear logs from local machines; logs will remain saved on the COLLECTOR machine
make teardown-gvs-experiment
```

## Run Specific Experiment for One vSwitch Pipeline

To setup and run a specific experiment (with a given locality, pipeline, and Gigaflow tables configuration), modify the following variables in [vars/main.yml](vars/main.yml).

```yml

# the locality (high/low) to pick the correct traffic
# choose an option from locality_static
locality_dynamic:
  current:
    locality: "high-locality"

# the pipeline to install and send traffic for
# choose an option from pipelines_static
pipelines_dynamic: 
  current: 
    name: "cord-ofdpa"
    sub_path: "cord/ofdpa"

# the Gigaflow tables and entries limit in each of them
# choose an option from gigaflow_static
gigaflow_dynamic:
  experiment: "ee" # this is just the name for the logs directory
  options:
      gigaflow_tables_limit: 4
      gigaflow_max_entries: 8000
```

Once these variables are setup, run the following sequence of commands. 

```sh
# sync the pipelines/traffic from COLLECTOR to NODES
make install-dataset 

# install the switch (with dependencies)
make install-gvs 

# install the traffic generators (with dependencies)
make install-tgen

# start the gigaflow-virtual-switch
# and install the pipeline rules in the switch
make start-switch-gvs 
make install-rules

# start the traffic (this will stop automatically)
make start-tgen

# cleanup after the traffic is sent
make stop-tgen

# uninstall the rules from the switch and stop it
make uninstall-rules 
make stop-switch-gvs

# copy logs from gvs and tgen to the collector machine
make collect-logs

# uninstall the tgen, gvs, and delete datasets
make uninstall-tgen 
make uninstall-gvs 
make uninstall-dataset
```

# Reference

Please cite this paper when using Gigaflow:

```bibtex
@inproceedings{zulfiqar2025gigaflow,
  title = {{Gigaflow: Pipeline-Aware Sub-Traversal Caching for Modern SmartNICs}},
  author = {Zulfiqar, Annus and Imran, Ali and Kunaparaju, Venkat and Antichi, Gianni and Pfaff, Ben and Shahbaz, Muhammad},
  booktitle = {ACM ASPLOS},
  year = {2025},
}
```

# Contact Us 
- [Annus Zulfiqar](https://annuszulfiqar2021.github.io/)
- [Ali Imran](https://www.linkedin.com/in/ali-imran-936a30202/)
- [Venkat Kunaparaju](https://www.linkedin.com/in/venkat-kunaparaju-3b8832232/)
- [Ben Pfaff](https://www.linkedin.com/in/ben-pfaff-414a262bb/)
- [Gianni Antichi](https://www.linkedin.com/in/gianniantichi/)
- [Muhammad Shahbaz](https://mshahbaz.gitlab.io/)

