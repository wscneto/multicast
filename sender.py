#!/usr/bin/env python3
"""Simple UDP multicast sender for distributed systems demos."""

from __future__ import annotations

import argparse
import socket
import sys
import time


def build_sender_socket(ttl: int, interface_ip: str | None, loopback: bool) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    if interface_ip:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface_ip))

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, int(loopback))
    return sock


def send_message(sock: socket.socket, group: str, port: int, message: str) -> None:
    payload = message.encode("utf-8")
    sock.sendto(payload, (group, port))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send messages to a UDP multicast group.")
    parser.add_argument("--group", default="239.255.10.10", help="Multicast group IP")
    parser.add_argument("--port", type=int, default=5007, help="Multicast UDP port")
    parser.add_argument("--ttl", type=int, default=1, help="Multicast TTL (1 = local network)")
    parser.add_argument(
        "--interface",
        help="Local interface IP used to send multicast (optional).",
    )
    parser.add_argument(
        "--no-loopback",
        action="store_true",
        help="Disable multicast loopback to local receivers on the same host.",
    )
    parser.add_argument(
        "--message",
        help="If provided, send this message once (or repeatedly with --interval).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.0,
        help="Seconds between repeated sends when using --message.",
    )
    return parser.parse_args()


def run_interactive(sock: socket.socket, group: str, port: int) -> None:
    print("Interactive mode. Type a message and press Enter.")
    print("Type /exit to stop.")
    while True:
        try:
            text = input("> ").strip()
        except EOFError:
            print("\nInput ended.")
            return

        if not text:
            continue
        if text.lower() == "/exit":
            return

        send_message(sock, group, port, text)
        print(f"Sent: {text}")


def run_fixed_message(
    sock: socket.socket,
    group: str,
    port: int,
    message: str,
    interval: float,
) -> None:
    if interval <= 0:
        send_message(sock, group, port, message)
        print(f"Sent once: {message}")
        return

    count = 1
    print(f"Sending every {interval:.2f}s. Press Ctrl+C to stop.")
    while True:
        tagged_message = f"{message} #{count}"
        send_message(sock, group, port, tagged_message)
        print(f"Sent: {tagged_message}")
        count += 1
        time.sleep(interval)


def main() -> int:
    args = parse_args()

    if not (0 <= args.ttl <= 255):
        print("Error: --ttl must be between 0 and 255.", file=sys.stderr)
        return 2
    if not (1 <= args.port <= 65535):
        print("Error: --port must be between 1 and 65535.", file=sys.stderr)
        return 2

    sock = build_sender_socket(args.ttl, args.interface, loopback=not args.no_loopback)

    try:
        if args.message is None:
            run_interactive(sock, args.group, args.port)
        else:
            run_fixed_message(sock, args.group, args.port, args.message, args.interval)
    except KeyboardInterrupt:
        print("\nSender stopped by user.")
    finally:
        sock.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())