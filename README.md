# scrcpy helper application

## what it does
this helper application, available as either a python script or a executable file (needs to be built from the python file with pyinstaller) is intended to automate connection of a PC to a Android smartphone that has wireless debugging enabled.

## requirements
this script uses nmap to scan for open ports on your system, so you need nmap to be installed. this can be achieved by using the official installer from (link) https://nmap.org/download
the script as well as the executable file need to be placed in the same folder as scrcpy.
of course, also a smartphone running Android as OS is needed. on the smartphone, wireless debugging must be enabled - recommended way is using the quick settings tile. the smartphone should have a static IP adress to make sure the cofigured IP adress can be reliably found.

### background information regarding IP adress use
I did try using MDNS or bonjour to search for the smartphone device name on the network, but due to either skill issues or windows issues or a mix of both, I was unable to get that to work. as a result, I set a static IP adress for my phone and use that.

## options
the default parameters with which scrcpy is called are:
	1. --max-size=1080 
	2. --tcpip=IP:PORT
	3. --turn-screen-off
	4. --keyboard=uhid
	5. --mouse=uhid

## initial setup
the IP adress needs to be configured in the script. just edit the 
> ip = "IP ADRESS HERE"

line at the beginning of the script.
it's possible that you need to adjust the range of port numbers to scan, if so this can be done by changing the values in the line 
> command  =  f"& {nmap_cmd}  {ip} -p 30000-51000"

it is also possible that the path to nmap needs to be adjusted according to your system, the default is
> nmap_path  =  r"C:\Program Files (x86)\Nmap\nmap.exe"

## usage
1. enable wireless debugging on the phone
2. start the script / executable
3. use scrcpy
