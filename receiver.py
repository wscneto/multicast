#!/usr/bin/env python3
"""Simple UDP multicast receiver for distributed systems demos."""

from __future__ import annotations

import argparse
import socket
import struct
import sys
from datetime import datetime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Receive messages from a UDP multicast group.")
    parser.add_argument("--group", default="239.255.10.10", help="Multicast group IP")
    parser.add_argument("--port", type=int, default=5007, help="Multicast UDP port")
    parser.add_argument(
        "--bind",
        default="0.0.0.0",
        help="Local IP to bind (0.0.0.0 listens on all interfaces)",
    )
    parser.add_argument(
        "--interface",
        default="0.0.0.0",
        help="Interface IP used to join multicast group (0.0.0.0 = default route)",
    )
    parser.add_argument("--buffer", type=int, default=2048, help="Receive buffer size")
    return parser.parse_args()


def build_receiver_socket(
    group: str,
    port: int,
    bind_ip: str,
    interface_ip: str,
) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if hasattr(socket, "SO_REUSEPORT"):
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except OSError:
            pass

    sock.bind((bind_ip, port))

    membership = struct.pack("4s4s", socket.inet_aton(group), socket.inet_aton(interface_ip))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)

    return sock


def main() -> int:
    args = parse_args()

    if not (1 <= args.port <= 65535):
        print("Error: --port must be between 1 and 65535.", file=sys.stderr)
        return 2
    if args.buffer <= 0:
        print("Error: --buffer must be greater than 0.", file=sys.stderr)
        return 2

    try:
        sock = build_receiver_socket(args.group, args.port, args.bind, args.interface)
    except OSError as exc:
        print(f"Socket setup failed: {exc}", file=sys.stderr)
        return 1

    print(f"Listening on multicast group {args.group}:{args.port}")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            data, sender = sock.recvfrom(args.buffer)
            message = data.decode("utf-8", errors="replace")
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] {sender[0]}:{sender[1]} -> {message}")
    except KeyboardInterrupt:
        print("\nReceiver stopped by user.")
    finally:
        sock.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())