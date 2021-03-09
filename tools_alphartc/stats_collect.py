#!/usr/bin/env python3

import sys
import re
import json


def load_stats(log_path: str):
    stats_pattern = r"\(remote_estimator_proxy\.cc:129\):(.*)"
    stats_pattern = re.compile(stats_pattern)
    stats_list = []
    with open(log_path, "r") as fd:
        line = fd.readline()
        while line:
            stats = stats_pattern.search(line)
            line = fd.readline()
            if not stats:
                continue
            stats = json.loads(stats.group(1))
            stats_list.append(stats)
    return stats_list


def to_gym_stats(stats_list: list):
    gym_stats_list = []
    for stats in stats_list:
        pkt_info = stats["packetInfo"]
        pkt_header_info = pkt_info["header"]
        gym_stats_list.append(
            {
                "send_time_ms": pkt_header_info["sendTimestamp"],
                "arrival_time_ms": pkt_info["arrivalTimeMs"],
                "payload_type": pkt_header_info["payloadType"],
                "sequence_number": pkt_header_info["sequenceNumber"],
                "ssrc": pkt_header_info["ssrc"],
                "padding_length": pkt_header_info["paddingLength"],
                "header_length": pkt_header_info["headerLength"],
                "payload_size": pkt_info["payloadSize"],
            }
        )
    return gym_stats_list


if __name__ == "__main__":
    stats = load_stats(sys.argv[1])
    stats = to_gym_stats(stats)
    stats = json.dumps(stats)
    print(stats)
