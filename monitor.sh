#!/bin/bash

mkdir -p logs

time_stamp=$(date +"%Y/%m/%d %H:%M:%S")

cpu_usage=$( top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}' ) # -bn1 means simple text output "buffer" and n1 means only 1 iteration simple text format
mem_usage=$( free -m | grep "Mem" | awk '{print (($3-$6)/$2)*100}' )
disc_usage=$( df -h / | awk 'NR==2{print $5}' ) # df -h / gives output only of root filesystem

load_average=$( uptime | awk -F"load average:" '{print $2}' )
uptime=$( uptime -p )

log_file="logs/monitor_$(date +"%d-%m-%Y").log"

echo "[$time_stamp] CPU: ${cpu_usage} | RAM: ${mem_usage} | Disc: ${disc_usage} | LoadAvg: ${load_average} | Up Time: ${uptime}" >> "$log_file"

echo "Cpu Usage is: ${cpu_usage}"
echo "Memory Usage is: ${mem_usage}"
echo "Disc Usage is: ${disc_usage}" 
echo "Uptime is: ${uptime}"
echo "Load Average is: ${load_average}"

# Top 5 Memory Consuming Processes
echo "[$time_stamp] Top 5 Memory Consuming Processes:" >> "$log_file"
ps -aux --sort=-%mem | awk 'NR<=6{printf "%s\t%s\t%s\t%s\n", $1, $2, $4, $11}' >> "$log_file"
echo "------------------------------------------------------" >> "$log_file"