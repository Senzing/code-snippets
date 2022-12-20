#!/usr/bin/env bash

# Signal trapping.

handle_term()
{
   echo "signal received, sleep-infinity exiting."
   exit 0
}

trap 'handle_term' TERM

# =============================================================================
# Main
# =============================================================================

echo "/app/sleep-infinitely.sh is sleeping infinitely."

# Sleep in a manner that allows "docker stop ..." to shutdown gracefully.

sleep infinity &
wait
