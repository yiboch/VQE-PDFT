#!/bin/bash

target_dirs=("point1" "point2" "point3" "point4")

echo "starting four-point"

for point_dir in "${target_dirs[@]}"; do
    if [ -d "$point_dir" ]; then
        echo -e "\nInside: $point_dir"
        
        echo "Running order preview："
        
        find "$point_dir" -type f -name "[1-8]_*.py" | sort -t_ -k1n | while read -r file; do
            echo "  will execute: $(basename "$file")"
        done
        
        echo -e "\nstart runing："
        
        find "$point_dir" -type f -name "[1-8]_*.py" | sort -t_ -k1n | while read -r python_file; do
            echo "  runing: $(basename "$python_file")"
            python3 "$python_file"
            
            
            if [ $? -eq 0 ]; then
                echo "  ✓ SUCCESS: $(basename "$python_file")"
            else
                echo "  ✗ FaILED: $(basename "$python_file")"
            fi
            echo "  ------------------------"
        done
    else
        echo "WARNING: $point_dir folder does not exists"
    fi
done

echo -e "\n所有文件执行完成！"