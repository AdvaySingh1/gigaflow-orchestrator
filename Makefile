export PROJECT_ROOT ?= $(PWD)
export ANSIBLE_CONFIG ?= $(PROJECT_ROOT)/ansible.cfg
export ANSIBLE_INVENTORY ?= $(PROJECT_ROOT)/inventory.ini
# export ANSIBLE_VAULT_PASSWORD_FILE ?= $(PROJECT_ROOT)/vault_pass.txt

export GVS_PLAYBOOK ?= $(PROJECT_ROOT)/gvs.yml

export RETRIEVE_PLAYBOOK ?= $(PROJECT_ROOT)/retrieve.yml
export RULES_PLAYBOOK ?= $(PROJECT_ROOT)/rules.yml
export TGEN_PLAYBOOK ?= $(PROJECT_ROOT)/tgen.yml
export COLLECTOR_PLAYBOOK ?= $(PROJECT_ROOT)/collector.yml

export GVS_EE_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/gvs_ee_experiment.yml
export GVS_BM_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/gvs_bm_experiment.yml
export GVS_DEMO_EXPERIMENT_PLAYBOOK ?= $(PROJECT_ROOT)/gvs_demo_experiment.yml

ansible:
	sh ./scripts/ansible

ping:
	ansible all -m ping
# TODO: Delete
trial-switch:
	ansible-playbook $(GVS_PLAYBOOK) --tags trial-switch

install-dataset:
	ansible-playbook $(RETRIEVE_PLAYBOOK) --tags install-dataset

uninstall-dataset:
	ansible-playbook $(RETRIEVE_PLAYBOOK) --tags uninstall-dataset

install-gvs:
	ansible-playbook $(GVS_PLAYBOOK) --tags install-gvs

uninstall-gvs:
	ansible-playbook $(GVS_PLAYBOOK) --tags uninstall-gvs

start-switch-gvs:
	ansible-playbook $(GVS_PLAYBOOK) --tags start-switch

stop-switch-gvs:
	ansible-playbook $(GVS_PLAYBOOK) --tags stop-switch

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
	ansible-playbook $(GVS_EE_EXPERIMENT_PLAYBOOK)

run-gvs-bm-experiment:
	ansible-playbook $(GVS_BM_EXPERIMENT_PLAYBOOK)

run-gvs-experiment: \
	run-gvs-ee-experiment \
	run-gvs-bm-experiment

run-gvs-demo-experiment:
	ansible-playbook $(GVS_DEMO_EXPERIMENT_PLAYBOOK)

teardown-gvs-experiment: \
	uninstall-tgen uninstall-gvs uninstall-dataset