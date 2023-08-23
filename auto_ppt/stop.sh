#!/bin/bash

# 查找占用5000端口的进程PID，并取第一个pid
pid=$(lsof -t -i:5000 | head -n 1)

# 如果找到了PID，则优雅地终止进程
if [ -n "$pid" ]; then
    echo "Found a process with PID $pid on port 5000. Terminating the process gracefully..."
    kill $pid
    sleep 5  # 等待5秒给进程时间完成清理（可根据需要调整等待时间）

    # 如果进程仍在运行，使用SIGKILL强制终止
    if ps -p $pid > /dev/null; then
        echo "The process did not terminate gracefully. Forcing termination using SIGKILL..."
        kill -9 $pid
    fi
else
    echo "No process found on port 5000. No action needed."
fi
