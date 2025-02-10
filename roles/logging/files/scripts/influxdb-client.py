#!/usr/bin/env python3
from influxdb import InfluxDBClient
import argparse
import time
import re
import os


EMPTY_FIELD = "NA"
MAX_PRIORITIES = 64

# the first three zeros are padding
megaflow_hit_rates = [
    0.0,
    0.0,
    0.0,
    71.6,
    75.4,
    78.4,
    79.8,
    79.2,
    79.3,
    77.9,
    77.0,
    75.7,
    74.5,
    73.5,
    73.0,
    72.3,
    71.6,
    70.9,
    70.5,
    70.8,
    71.1,
    71.3,
    71.7,
    72.1,
    72.6,
    72.7,
    72.6,
    72.3,
    71.9,
    71.6,
    71.2,
    70.9,
    70.6,
    70.2,
    69.9,
    69.5,
    69.2,
    68.9,
    68.6,
    68.6,
    68.6,
    68.7,
    68.8,
    69.0,
    69.2,
    69.4,
    69.3,
    69.3,
    69.1,
    68.9,
    68.8,
    68.6,
    68.4,
    68.2,
    68.0,
    67.8,
    67.6,
    67.3,
    67.1,
    66.9,
    66.8,
    66.7,
    66.6,
    66.6,
    66.6,
    66.6,
]

megaflow_upcalls = [
    0,
    0,
    0,
    7727,
    18092,
    26014,
    33245,
    39255,
    44920,
    50273,
    55329,
    60346,
    65299,
    70561,
    75395,
    80271,
    84888,
    90038,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93116,
    93121,
]

megaflow_rule_space = [
    0,
    0,
    0,
    7726,
    18091,
    26013,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
    32000,
]


def get_cache_occupancy_map_for_one_table(table_id, priorities):
    cache_occ_per_table_dict = {}
    cache_occ_per_table_dict[f"cache_occupancy_table_{table_id}"] = EMPTY_FIELD
    cache_occ_per_table_dict[f"cache_recycled_table_{table_id}"] = EMPTY_FIELD
    cache_occ_per_table_dict[f"cache_recycle_rate_table_{table_id}"] = EMPTY_FIELD
    cache_occ_per_table_dict[f"cache_masks_table_{table_id}"] = EMPTY_FIELD
    for p in range(priorities):
        cache_occ_per_table_dict[f"cache_table_{table_id}_priority_{p}"] = 0
    return cache_occ_per_table_dict


def get_cache_occupancy_map(tables, priorities):
    cache_occ_dict = {}
    for t in range(tables):
        cache_occ_dict.update(
            get_cache_occupancy_map_for_one_table(t, priorities))
    return cache_occ_dict


def get_empty_ovs_perf_map():
    basic_map = {

        "pipeline": EMPTY_FIELD,

        "rx_packets": EMPTY_FIELD,
        "rx_packets_kpps": EMPTY_FIELD,
        "rx_packets_cycles_pkt": EMPTY_FIELD,

        "datapath_pass": EMPTY_FIELD,
        "datapath_pass_pkt": EMPTY_FIELD,

        "phwol_hits": EMPTY_FIELD,
        "phwol_hits_perc": EMPTY_FIELD,

        "mfex_opt_hits": EMPTY_FIELD,
        "mfex_opt_hits_perc": EMPTY_FIELD,

        "smc_hits": EMPTY_FIELD,
        "smc_hits_perc": EMPTY_FIELD,

        "emc_hits": EMPTY_FIELD,
        "emc_hits_perc": EMPTY_FIELD,

        "SMC_hits": EMPTY_FIELD,
        "SMC_hits_perc": EMPTY_FIELD,

        "Megaflow_hits": EMPTY_FIELD,
        "Megaflow_hits_perc": EMPTY_FIELD,
        "Megaflow_subtbl_hit": EMPTY_FIELD,

        "upcalls": EMPTY_FIELD,
        "upcalls_perc": EMPTY_FIELD,
        "upcalls_us_upcall": EMPTY_FIELD,

        "lost_upcalls": EMPTY_FIELD,
        "lost_upcalls_perc": EMPTY_FIELD,

        "upcall_cycles": EMPTY_FIELD,

        "gigaflow_hits": EMPTY_FIELD,
        "gigaflow_hits_perc": EMPTY_FIELD,

        "lookup_cycles": EMPTY_FIELD,
        "lookup_cycles_per_upcall": EMPTY_FIELD,
        "lookup_cycles_perc_upcall_std_dev": EMPTY_FIELD,
        "lookup_cycles_perc_upcall": EMPTY_FIELD,

        "mapping_cycles": EMPTY_FIELD,
        "mapping_cycles_per_upcall": EMPTY_FIELD,
        "mapping_cycles_perc_upcall_std_dev": EMPTY_FIELD,
        "mapping_cycles_perc_upcall": EMPTY_FIELD,

        "optimizer_cycles": EMPTY_FIELD,
        "optimizer_cycles_per_upcall": EMPTY_FIELD,
        "optimizer_cycles_perc_upcall_std_dev": EMPTY_FIELD,
        "optimizer_cycles_perc_mapping": EMPTY_FIELD,

        "composition_cycles": EMPTY_FIELD,
        "composition_cycles_per_upcall": EMPTY_FIELD,
        "composition_cycles_perc_upcall_std_dev": EMPTY_FIELD,
        "composition_cycles_perc_mapping": EMPTY_FIELD,

        "state_update_cycles": EMPTY_FIELD,
        "state_update_cycles_per_upcall": EMPTY_FIELD,
        "state_update_cycles_perc_upcall_std_dev": EMPTY_FIELD,
        "state_update_cycles_perc_mapping": EMPTY_FIELD,

        "flow_setup_cycles": EMPTY_FIELD,
        "flow_setup_cycles_per_upcall": EMPTY_FIELD,
        "flow_setup_cycles_perc_upcall_std_dev": EMPTY_FIELD,
        "flow_setup_cycles_perc_upcall": EMPTY_FIELD,

        "batch_update_cycles": EMPTY_FIELD,
        "batch_update_cycles_per_batch": EMPTY_FIELD,
        "batch_update_cycles_perc_batch_std_dev": EMPTY_FIELD,

        "unique_mappings": EMPTY_FIELD,
        "rule_space": EMPTY_FIELD,

        "cache_occupancy": EMPTY_FIELD,
        "cache_recycled": EMPTY_FIELD,
        "cache_recycle_rate": EMPTY_FIELD,
    }

    tx_map = {
        "tx_packets": EMPTY_FIELD,
        "tx_packets_kpps": EMPTY_FIELD,
        "tx_batches": EMPTY_FIELD,
        "tx_batches_pkts_batch": EMPTY_FIELD,
    }

    return {**basic_map, **get_cache_occupancy_map(tables=8, priorities=64), **tx_map}


def table_stats_parser(values):
    table_stats_keys = list(get_cache_occupancy_map_for_one_table(
        table_id=0, priorities=MAX_PRIORITIES).keys())
    table_stats = [0]*len(table_stats_keys)
    # cache occupancy, recycled, recycle rate, masks
    table_stats[:4] = values[:4]
    # cache table priorities
    for i in range(4, len(values), 2):
        this_priority = int(values[i])
        this_priority_util = int(values[i+1])
        table_stats[4+this_priority] = this_priority_util
    return table_stats


def add_vals_to_ovs_perf_map(perf_map, val_list, vals):
    if len(val_list) != len(vals):
        print(f"Error: len(val_list) != len(vals) for {val_list} and {vals}")
        for val in val_list:
            perf_map[val] = -1
        return
    for idx, val in enumerate(val_list):
        # perf_map[val] = vals[idx]
        # if this value was float string, make it flooat, otherwise int
        try:
            perf_map[val] = float(vals[idx])
        except ValueError:
            try:
                perf_map[val] = int(vals[idx])
            except ValueError:
                perf_map[val] = vals[idx]
    return


def parse_performance_from_pmd_log(perf):
    parsed_perf = get_empty_ovs_perf_map()
    perf = [x for x in str(perf).split('\n') if x]
    for this_line in perf:
        # print and parse line by line
        values = re.findall(r"[-+]?\d*\.\d+|\d+", this_line)
        if "Rx packets" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["rx_packets", "rx_packets_kpps", "rx_packets_cycles_pkt"], values)
        elif "Datapath passes" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["datapath_pass", "datapath_pass_pkt"], values)
        elif "PHWOL hits" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["phwol_hits", "phwol_hits_perc"], values)
        elif "MFEX Opt hits" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["mfex_opt_hits", "mfex_opt_hits_perc"], values)
        elif "Simple Match hit" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["smc_hits", "smc_hits_perc"], values)
        elif "EMC hits" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["emc_hits", "emc_hits_perc"], values)
        elif "SMC hits" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["SMC_hits", "SMC_hits_perc"], values)
        elif "Megaflow hits" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, [
                                     "Megaflow_hits", "Megaflow_hits_perc", "Megaflow_subtbl_hit"], values)
        elif "Upcalls" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["upcalls", "upcalls_perc", "upcalls_us_upcall"], values)
        elif "Lost upcalls" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["lost_upcalls", "lost_upcalls_perc"], values)
        elif "Upcall cycles" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["upcall_cycles"], values)
        elif "- Hits" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["gigaflow_hits", "gigaflow_hits_perc"], values)
        elif "- Lookup cycles" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["lookup_cycles", "lookup_cycles_per_upcall",
                                     "lookup_cycles_perc_upcall_std_dev", "lookup_cycles_perc_upcall"], values)
        elif "- Mapping cycles" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["mapping_cycles", "mapping_cycles_per_upcall",
                                     "mapping_cycles_perc_upcall_std_dev", "mapping_cycles_perc_upcall"], values)
        elif "- Optimizer:" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["optimizer_cycles", "optimizer_cycles_per_upcall",
                                     "optimizer_cycles_perc_upcall_std_dev", "optimizer_cycles_perc_mapping"], values)
        elif "- Composition:" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["composition_cycles", "composition_cycles_per_upcall",
                                     "composition_cycles_perc_upcall_std_dev", "composition_cycles_perc_mapping"], values)
        elif "- State update" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["state_update_cycles", "state_update_cycles_per_upcall",
                                     "state_update_cycles_perc_upcall_std_dev", "state_update_cycles_perc_mapping"], values)
        elif "- Setup cycles" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["flow_setup_cycles", "flow_setup_cycles_per_upcall",
                                     "flow_setup_cycles_perc_upcall_std_dev", "flow_setup_cycles_perc_upcall"], values)
        elif "- Batch update" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, [
                                     "batch_update_cycles", "batch_update_cycles_per_batch", "batch_update_cycles_perc_batch_std_dev"], values)
        elif "- Unique mappings" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["unique_mappings"], values)
        elif "- Rule space" in this_line:
            add_vals_to_ovs_perf_map(parsed_perf, ["rule_space"], values)
        elif "- Cache occupancy" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["cache_occupancy", "cache_recycled", "cache_recycle_rate"], values)
        # parse cache occupancy statistics per Gigaflow table
        elif "- Table-" in this_line:
            table_id = values[0]
            table_stats_keys = list(get_cache_occupancy_map_for_one_table(
                table_id, priorities=MAX_PRIORITIES).keys())
            # add_vals_to_ovs_perf_map(parsed_perf, table_stats_keys, values[1:]) # this is the old way
            add_vals_to_ovs_perf_map(
                parsed_perf, table_stats_keys, table_stats_parser(values[1:]))
        elif "Tx packets" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["tx_packets", "tx_packets_kpps"], values)
        elif "Tx batches" in this_line:
            add_vals_to_ovs_perf_map(
                parsed_perf, ["tx_batches", "tx_batches_pkts_batch"], values)
        elif "Histogram" in this_line:
            # we don't need anything beyond this point..
            break
    return parsed_perf


def int_or_zero(value):
    if value == EMPTY_FIELD:
        return 0
    return int(value)


def float_or_zero(value):
    if value == EMPTY_FIELD:
        return 0.0
    return float(value)


def collect_samples(db_name):
    db_client = InfluxDBClient(host='localhost', port=8086)
    # Drop (clear) the database
    print("Dropping database..")
    db_client.drop_database(db_name)
    # Create the database
    print("Creating new (clean) database..")
    db_client.create_database(db_name)
    db_client.switch_database(db_name)
    samples = 0
    while True:
        perf_log = os.popen("ovs-appctl dpif-netdev/pmd-perf-show").read()
        if perf_log:
            parsed_ovs_perf = parse_performance_from_pmd_log(perf_log)
            this_sample = {

                # gigaflow hit rate
                "gf_hit_rate": float_or_zero(parsed_ovs_perf["gigaflow_hits_perc"]),
                # upcalls
                "upcalls": int_or_zero(parsed_ovs_perf["upcalls"]),
                # rule space
                "rulespace": int_or_zero(parsed_ovs_perf["rule_space"]),
                # total cache entries
                "cache_entries": int_or_zero(parsed_ovs_perf["cache_occupancy"]),
                # cache entries in table 1
                "cache_entries_g1": int_or_zero(parsed_ovs_perf["cache_occupancy_table_0"]),
                # cache entries in table 2
                "cache_entries_g2": int_or_zero(parsed_ovs_perf["cache_occupancy_table_1"]),
                # cache entries in table 3
                "cache_entries_g3": int_or_zero(parsed_ovs_perf["cache_occupancy_table_2"]),
                # cache entries in table 4
                "cache_entries_g4": int_or_zero(parsed_ovs_perf["cache_occupancy_table_3"]),
                # overall share rate
                "share_rate": float_or_zero(parsed_ovs_perf["cache_recycle_rate"]),
                # share rate in table 1
                "share_rate_g1": float_or_zero(parsed_ovs_perf["cache_recycle_rate_table_0"]),
                # share rate in table 2
                "share_rate_g2": float_or_zero(parsed_ovs_perf["cache_recycle_rate_table_1"]),
                # share rate in table 3
                "share_rate_g3": float_or_zero(parsed_ovs_perf["cache_recycle_rate_table_2"]),
                # share rate in table 4
                "share_rate_g4": float_or_zero(parsed_ovs_perf["cache_recycle_rate_table_3"]),

                # megaflow hit rate in a parallel experiment
                "mf_hit_rate": megaflow_hit_rates[samples],
                # megaflow upcalls in a parallel experiment
                "mf_upcalls": megaflow_upcalls[samples],
                # megaflow rule space in a parallel experiment
                "mf_rulespace": megaflow_rule_space[samples],
                # megaflow cache entries in a parallel experiment
                "mf_cache_entries": megaflow_rule_space[samples],
            }

            db_client.write_points([{
                "measurement": "ovs_perf",  # table
                # "tags": {}, # repeating properties
                "fields": this_sample,  # anything that changes
            }])

            print(f"{samples} => {this_sample}")
            samples += 1
        else:
            print("No samples retreived..")
        time.sleep(5)


def main():
    CLI = argparse.ArgumentParser()
    CLI.add_argument("--db", type=str)
    args = CLI.parse_args()
    print("Starting GVS performance sampler..")
    collect_samples(db_name=args.db)


if __name__ == "__main__":
    main()
