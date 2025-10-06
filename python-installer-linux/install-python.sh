#!/bin/bash


REQUIRED_COMMANDS=("make" "wget" "build-essential" "openssl" "libssl-dev" "zlib1g-dev")


log() {
    echo -e "\e[2m$1\e[0m"
}

check_command() {
    command -v "$1" > /dev/null 2>&1
}

check_required_commands() {
    log "Checking commands..."

    missing_commands=()

    for cmd in "${REQUIRED_COMMANDS[@]}"; do
        if ! check_command "$cmd"; then
            missing_commands+=("$cmd")
        fi
    done

    if [ ${#missing_commands[@]} -ne 0 ]; then
        echo "Commands to download: ${missing_commands[@]}"
    else
        echo "All commands are available."
    fi

    exit 1
}

main() {
    check_required_commands
    echo "Post"
}

main
