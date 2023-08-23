#!/bin/bash

# 查找占用5000端口的进程PID
pid=$(lsof -t -i:5000)

# 如果找到了PID，则终止进程
if [ -n "$pid" ]; then
    echo "Found a process with PID $pid on port 5000. Terminating the process..."
    kill -9 $pid
else
    echo "No process found on port 5000. No action needed."
fi