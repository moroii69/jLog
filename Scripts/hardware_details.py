import os
import platform
import psutil
import cpuinfo
import socket
import requests
import subprocess
import re
import time
from datetime import datetime

# Get user's desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# File to save the hardware details
filename = os.path.join(desktop_path, "Hardware_Details.txt")

def run_command(command):
    """Run a command and return its output."""
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError:
        return "N/A"

def get_public_ip():
    """Fetch the public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=text')
        return response.text.strip()
    except requests.RequestException:
        return "N/A"

def get_system_info():
    info = []

    # Basic system info
    info.append(f"1. Operating System: {platform.system()} {platform.release()} {platform.version()}")
    info.append(f"2. Architecture: {platform.architecture()[0]}")
    info.append(f"3. Machine: {platform.machine()}")
    info.append(f"4. Processor: {platform.processor()}")

    # Computer Model and Serial Number (Windows-specific)
    if platform.system() == "Windows":
        model = run_command('wmic computersystem get model /value')
        serial_number = run_command('wmic bios get serialnumber /value')
        info.append(f"5. Computer Model: {model.split('=')[1] if '=' in model else 'N/A'}")
        info.append(f"6. Serial Number: {serial_number.split('=')[1] if '=' in serial_number else 'N/A'}")
    else:
        info.append("5. Computer Model: N/A (Non-Windows system)")
        info.append("6. Serial Number: N/A (Non-Windows system)")

    # CPU info
    cpu_info = cpuinfo.get_cpu_info()
    info.append(f"7. CPU Model: {cpu_info['brand_raw']}")
    info.append(f"8. CPU Cores: {psutil.cpu_count(logical=False)}")
    info.append(f"9. CPU Threads: {psutil.cpu_count(logical=True)}")
    info.append(f"10. CPU Frequency: {psutil.cpu_freq().current} MHz")
    info.append(f"11. CPU Max Frequency: {psutil.cpu_freq().max} MHz")
    info.append(f"12. CPU Min Frequency: {psutil.cpu_freq().min} MHz")

    # Memory info
    virtual_memory = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()
    info.append(f"13. Total RAM: {virtual_memory.total / (1024 ** 3):.2f} GB")
    info.append(f"14. Available RAM: {virtual_memory.available / (1024 ** 3):.2f} GB")
    info.append(f"15. Used RAM: {virtual_memory.used / (1024 ** 3):.2f} GB")
    info.append(f"16. Total Swap: {swap_memory.total / (1024 ** 3):.2f} GB")
    info.append(f"17. Available Swap: {swap_memory.free / (1024 ** 3):.2f} GB")
    info.append(f"18. Used Swap: {swap_memory.used / (1024 ** 3):.2f} GB")

    # Disk info
    disk_partitions = psutil.disk_partitions()
    for i, partition in enumerate(disk_partitions, start=19):
        partition_info = psutil.disk_usage(partition.mountpoint)
        info.append(f"{i}. Disk Partition {i-18}: {partition.device}")
        info.append(f"  - Mount Point: {partition.mountpoint}")
        info.append(f"  - File System Type: {partition.fstype}")
        info.append(f"  - Total Size: {partition_info.total / (1024 ** 3):.2f} GB")
        info.append(f"  - Used: {partition_info.used / (1024 ** 3):.2f} GB")
        info.append(f"  - Free: {partition_info.free / (1024 ** 3):.2f} GB")

    # Battery info (if available)
    battery = psutil.sensors_battery()
    if battery:
        info.append(f"{i+1}. Battery: {battery.percent}%")
        info.append(f"{i+2}. Power Plugged In: {battery.power_plugged}")
    else:
        info.append(f"{i+1}. Battery: N/A")
        info.append(f"{i+2}. Power Plugged In: N/A")

    # Network info
    info.append(f"{i+3}. Network Interfaces:")
    net_if_addrs = psutil.net_if_addrs()
    for interface, addrs in net_if_addrs.items():
        info.append(f"  - Interface: {interface}")
        for addr in addrs:
            info.append(f"    - Address: {addr.address} (Family: {addr.family})")

    # System boot time and uptime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    info.append(f"{i+4}. System Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    info.append(f"{i+5}. System Uptime: {str(datetime.now() - boot_time).split('.')[0]}")

    # CPU usage
    info.append(f"{i+6}. CPU Usage Per Core:")
    for idx, usage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        info.append(f"  - Core {idx}: {usage}%")

    # CPU temperature (if available)
    try:
        temperatures = psutil.sensors_temperatures()
        if 'coretemp' in temperatures:
            info.append(f"{i+7}. CPU Temperature:")
            for temp in temperatures['coretemp']:
                info.append(f"  - {temp.label}: {temp.current}°C")
        else:
            info.append(f"{i+7}. CPU Temperature: Not Available")
    except Exception as e:
        info.append(f"{i+7}. CPU Temperature: Error - {str(e)}")

    # GPU info (basic, if applicable)
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        for idx, gpu in enumerate(gpus):
            info.append(f"{i+8+idx}. GPU {idx}: {gpu.name}")
            info.append(f"  - Memory Total: {gpu.memoryTotal} MB")
            info.append(f"  - Memory Free: {gpu.memoryFree} MB")
            info.append(f"  - Memory Used: {gpu.memoryUsed} MB")
            info.append(f"  - GPU Load: {gpu.load * 100}%")
    except ImportError:
        info.append(f"{i+8}. GPU Info: Not Available (Install GPUtil for more details)")

    # Motherboard info (requires additional utilities or manual input)
    info.append(f"{i+9}. Motherboard: Not Available (Requires specific tools)")

    # Memory (RAM) details
    try:
        ram_info = run_command('wmic memorychip get capacity, speed, manufacturer')
        ram_lines = ram_info.split('\n')[1:]  # Skip header line
        for idx, line in enumerate(ram_lines):
            if line.strip():
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 3:
                    info.append(f"{i+10+idx}. RAM Module {idx+1}:")
                    info.append(f"  - Capacity: {int(parts[0]) / (1024 ** 2):.2f} GB")
                    info.append(f"  - Speed: {parts[1]} MHz")
                    info.append(f"  - Manufacturer: {parts[2]}")
    except Exception as e:
        info.append(f"{i+10}. RAM Details: Error - {str(e)}")

    # Case and PSU info (requires physical inspection)
    info.append(f"{i+13}. Case Model and Manufacturer: Not Available (Requires physical inspection)")
    info.append(f"{i+14}. PSU Model and Manufacturer: Not Available (Requires physical inspection)")

    # Optical Drive info (if present)
    info.append(f"{i+15}. Optical Drive: {run_command('wmic cdrom get caption /value').split('=')[1] if '=' in run_command('wmic cdrom get caption /value') else 'N/A'}")

    # Sound Card info (if not integrated)
    info.append(f"{i+16}. Sound Card: {run_command('wmic sounddev get caption /value').split('=')[1] if '=' in run_command('wmic sounddev get caption /value') else 'N/A'}")

    # USB Ports info
    info.append(f"{i+17}. USB Ports: Check physically or through system settings")

    # BIOS/UEFI Version
    if platform.system() == "Windows":
        info.append(f"{i+18}. BIOS/UEFI Version: {run_command('wmic bios get smbiosbiosversion /value').split('=')[1] if '=' in run_command('wmic bios get smbiosbiosversion /value') else 'N/A'}")
    else:
        info.append(f"{i+18}. BIOS/UEFI Version: N/A (Non-Windows system)")

    # Wi-Fi Card info
    info.append(f"{i+19}. Wi-Fi Card: {run_command('wmic nic get description /value').split('=')[1] if '=' in run_command('wmic nic get description /value') else 'N/A'}")

    # Peripherals
    info.append(f"{i+20}. Peripherals: Check physically or through system settings")

    # Expansion Cards info
    info.append(f"{i+21}. Expansion Cards: Check physically or through system settings")

    # Public IP address
    info.append(f"{i+22}. Public IP Address: {get_public_ip()}")

    # Network Throughput
    info.append("23. Network Throughput (bytes per second):")
    prev_bytes_sent = psutil.net_io_counters().bytes_sent
    prev_bytes_recv = psutil.net_io_counters().bytes_recv
    time.sleep(1)
    curr_bytes_sent = psutil.net_io_counters().bytes_sent
    curr_bytes_recv = psutil.net_io_counters().bytes_recv
    info.append(f"  - Bytes Sent: {curr_bytes_sent - prev_bytes_sent}")
    info.append(f"  - Bytes Received: {curr_bytes_recv - prev_bytes_recv}")

    # Default Gateways and DNS Servers (Windows-specific)
    if platform.system() == "Windows":
        gateways = run_command('wmic nicconfig get defaultipgateway /value')
        dns_servers = run_command('wmic nicconfig get dnsserversearchorder /value')
        info.append(f"24. Default Gateways: {gateways.replace('=', ':').replace('\\n', ', ')}")
        info.append(f"25. DNS Servers: {dns_servers.replace('=', ':').replace('\\n', ', ')}")

    # MAC Addresses and Network Interface Status
    info.append("26. MAC Addresses and Network Status:")
    for iface, addr_list in psutil.net_if_addrs().items():
        info.append(f"  - Interface: {iface}")
        for addr in addr_list:
            if addr.family == psutil.AF_LINK:
                info.append(f"    - MAC Address: {addr.address}")
        info.append(f"    - Status: {'Up' if psutil.net_if_stats()[iface].isup else 'Down'}")
        info.append(f"    - Speed: {psutil.net_if_stats()[iface].speed} Mbps")

    # Network Interfaces' Names and Descriptions (Windows-specific)
    if platform.system() == "Windows":
        interface_names = run_command('wmic nic get description /value')
        info.append(f"27. Network Interface Names and Descriptions: {interface_names.replace('=', ':').replace('\\n', ', ')}")

    # Save to file
    with open(filename, "w") as file:
        file.write(f"Hardware and Network Details - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("\n".join(info))

    print(f"Hardware and network details saved to {filename}")

if __name__ == "__main__":
    get_system_info()
