export PROJECT_ROOT ?= $(PWD)
export ANSIBLE_CONFIG ?= $(PROJECT_ROOT)/ansible.cfg
export ANSIBLE_INVENTORY ?= $(PROJECT_ROOT)/inventory.ini
export ANSIBLE_VAULT_PASSWORD_FILE ?= $(PROJECT_ROOT)/vault_pass.txt

export OVS_DPDK_PLAYBOOK ?= $(PROJECT_ROOT)/ovs_dpdk.yml
export OVS_ACCEL_PLAYBOOK ?= $(PROJECT_ROOT)/gvs.yml

export RETRIEVE_PLAYBOOK ?= $(PROJECT_ROOT)/retrieve.yml
export RULES_PLAYBOOK ?= $(PROJECT_ROOT)/rules.yml
export TGEN_PLAYBOOK ?= $(PROJECT_ROOT)/tgen.yml
export COLLECTOR_PLAYBOOK ?= $(PROJECT_ROOT)/collector.yml

export OVS_DPDK_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/ovs_dpdk_experiment.yml
export OVS_ACCEL_EE_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/ovs_accel_ee_experiment.yml
export OVS_ACCEL_BM_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/ovs_accel_bm_experiment.yml
export OVS_ACCEL_DEMO_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/ovs_accel_demo_experiment.yml
export OVS_ACCEL_DYNAMIC_WORKLOAD_BM_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/ovs_accel_dynamic_workload_bm_experiment.yml

ansible:
	sh ./scripts/ansible

ping:
	ansible all -m ping

install-dataset:
	ansible-playbook $(RETRIEVE_PLAYBOOK) --tags install-dataset

uninstall-dataset:
	ansible-playbook $(RETRIEVE_PLAYBOOK) --tags uninstall-dataset

install-ovs-dpdk:
	ansible-playbook $(OVS_DPDK_PLAYBOOK) --tags install-ovs-dpdk

uninstall-ovs-dpdk:
	ansible-playbook $(OVS_DPDK_PLAYBOOK) --tags uninstall-ovs-dpdk

install-gvs:
	ansible-playbook $(OVS_ACCEL_PLAYBOOK) --tags install-gvs

uninstall-gvs:
	ansible-playbook $(OVS_ACCEL_PLAYBOOK) --tags uninstall-gvs

start-switch-ovs-dpdk:
	ansible-playbook $(OVS_DPDK_PLAYBOOK) --tags start-switch

stop-switch-ovs-dpdk:
	ansible-playbook $(OVS_DPDK_PLAYBOOK) --tags stop-switch

start-switch-gvs:
	ansible-playbook $(OVS_ACCEL_PLAYBOOK) --tags start-switch

stop-switch-gvs:
	ansible-playbook $(OVS_ACCEL_PLAYBOOK) --tags stop-switch

install-rules:
	ansible-playbook $(RULES_PLAYBOOK) --tags install-rules

uninstall-rules:
	ansible-playbook $(RULES_PLAYBOOK) --tags uninstall-rules

install-tgen:
	ansible-playbook $(TGEN_PLAYBOOK) --tags install-tgen-dpdk

uninstall-tgen:
	ansible-playbook $(TGEN_PLAYBOOK) --tags uninstall-tgen-dpdk

resetup-tgen-scripts:
	ansible-playbook $(TGEN_PLAYBOOK) --tags resetup-tgen-scripts

start-tgen:
	ansible-playbook $(TGEN_PLAYBOOK) --tags start-tgen

stop-tgen:
	ansible-playbook $(TGEN_PLAYBOOK) --tags stop-tgen

collect-logs:
	ansible-playbook $(COLLECTOR_PLAYBOOK) --tags collect-logs

discard-logs:
	ansible-playbook $(COLLECTOR_PLAYBOOK) --tags discard-logs

test-ovs-dpdk-end-to-end: \
	install-dataset install-ovs-dpdk install-tgen \
	discard-logs \
	start-switch-ovs-dpdk install-rules \
	start-tgen stop-tgen \
	uninstall-rules stop-switch-ovs-dpdk \
	collect-logs \
	uninstall-tgen uninstall-ovs-dpdk uninstall-dataset

setup-ovs-dpdk-experiment: \
	install-dataset install-ovs-dpdk install-tgen

run-ovs-dpdk-experiment:
	ansible-playbook $(OVS_DPDK_EXPERIMENT_PLAYBOOK)

teardown-ovs-dpdk-experiment: \
	uninstall-tgen uninstall-ovs-dpdk uninstall-dataset

test-gvs-end-to-end: \
	install-dataset install-gvs install-tgen \
	discard-logs \
	start-switch-gvs install-rules \
	start-tgen stop-tgen \
	uninstall-rules stop-switch-gvs \
	collect-logs \
	uninstall-tgen uninstall-gvs uninstall-dataset

setup-gvs-experiment: \
	install-dataset install-gvs install-tgen

run-gvs-ee-experiment:
	ansible-playbook $(OVS_ACCEL_EE_EXPERIMENT_PLAYBOOK)

run-gvs-bm-experiment:
	ansible-playbook $(OVS_ACCEL_BM_EXPERIMENT_PLAYBOOK)

run-gvs-experiment: \
	run-gvs-ee-experiment \
	run-gvs-bm-experiment

run-gvs-demo-experiment:
	ansible-playbook $(OVS_ACCEL_DEMO_EXPERIMENT_PLAYBOOK)

run-gvs-dynamic-workload-bm-experiment:
	ansible-playbook $(OVS_ACCEL_DYNAMIC_WORKLOAD_BM_EXPERIMENT_PLAYBOOK)

teardown-gvs-experiment: \
	uninstall-tgen uninstall-gvs uninstall-dataset