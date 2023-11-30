# Import required modules/packages/library
from pprint import pprint
import re

# Create regular expression to to match Gigabit interface names
gig_pattern = re.compile(r'(GigabitEthernet)(\d\/\d\/\d\/\d)')

# Create a dictionary to hold the count of routes
# forwarded out each interface
routes = {}

# Read all lines of IP routing information 
file = open('ip-routes.txt', 'r')
for line in file:

    # Match for Gigabit Ethernet
    match = gig_pattern.search(line)

    # Check to see if we matched the Gig Ethernet string
    if match:
        intf = match.group(2) # get the interface from the match
        routes[intf] = routes[intf]+1 if intf in routes else 1

# Display heading
print('')
print('Number of routes per interface')
print('------------------------------')

# Display the routes per Gigabit interface
pprint(routes)

# Display a blank line to make easier to read
print('')

# Close the file
file.close()

# # Import required modules/packages/library
from pprint import pprint

# Display heading
print('')
print('Counts of different OS-types for all deices')
print('-------------------------------------')

# Create a dictionary of OS types
os_types = {'Cisco IOS':    {'count': 0, 'devs': []},
            'Cisco Nexus':  {'conut': 0, 'devs': []},
            'Cisco IOS-XR': {'count': 0, 'devs': []},
            'Cisco IOS-XE': {'count': 0, 'devs': []}}

# Read all lines of IP routing information
file = open('devices-06.txt', 'r')
for line in file:

    # Put device info into list
    device_info_list = line.strip().split(',')

    # Put device information into dictionary for this one device
    device_info = {} # Create a dictionary of device info
    device_info['name'] = device_info_list[0]
    device_info['os-type'] = device_info_list[1]

    # get the device name
    name = device_info['name']

    # Get the OS-type for comparisons
    os = device_info['os-type']

# Based on the OS-type, increment the count and add name to list
if os == 'ios':
    os_types['Cisco IOS']['count'] += 1
    os_types['Cisco IOS']['devs'].append(name)
elif os == 'nx-os':
    os_types['Cisco Nexus']['count'] += 1
    os_types['Cisco Nexus']['devs'].append(name)
elif os == 'ios-xr':
    os_types['Cisco IOS-XR']['count'] += 1
    os_types['Cisco IOS-XR']['devs'].append(name)
elif os == 'ios-xe':
    os_types['Cisco IOS-XE']['count'] += 1
    os_types['Cisco IOS-XE']['devs'].append(name)
else:
    print("  Warning: unknown device type:", os)

# Display the OS types
pprint(os_types)

# Display a blank line make easier to read
print('')

# Close the file
file.close()

# Import required modules/packages/library
import pexpect
from pprint import pprint
import re

# Display heading
print('')
print(' Interfaces, routes list, routes details')
print('------------------------------------')

# Create regular expressions to match interfaces and OSPF
OSPF_pattern = re.compile(r'0.+')
intf_pattern = re.compile(r'(GigabitEthernet)(\d')

# Create regular expressions to match prefix and routes
prefix_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/?\d?\d?)')
route_pattern = re.compile(r'via (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# Connet to device and run 'show ip route' command
print('----- connecting telnet 192.168.56.101 with prne/cisco123!')

session = pexpect.spawn('telent 192.168.56.101', enconding='utf-8, timeout=20')
result = session.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])

# Check for failure
if result != 0:
    print('Timeout or unexpected reply from device')
    exit()

# Enter username
session.sendline('prne')
result = session.expect('Password:')

# Enter password 
session.sendline('cisco123!')
result = session.expect('>')

# Must set terminal lenght to zero fro long replies, no pauses
print('----- setting terminal lenght to 0')
session.sendline('terminal lenght 0')
result = session.expect('>')

# Run the 'show ip route' command on device
print('--- successfully logged into device, running show ip route command')
session.sendline('show ip route')
result = session.expect('>')

# Display the output of the command, for comparison
print('---- show ip route output:')
show_ip_route_output = session.before
print('show_ip_route_output')

# Get the output from the command into a list of lines from the output
routes_list = show_ip_route_output.splitlines()

# Create dictionary to hold number of routes per interface
intf_routes = {}

#Go through the list of routes to get routes per interface
for route in routes_list:
    OSPF_match = OSPF_pattern.search(route)
    if OSPF_match:

        # Match for GigabitEthernet interfaces
        intf_match = intf_pattern.search(route)

        # Check to see if we matched the GigabitEthernet interfaces string
        if intf_match:
            # Get the interface from the match
            intf = intf_match.group(2)

            # if route list not yet created, do so now
            if intf not in intf_routes:
                intf_routes[intf] = []

            # Extract the prefix (destination IP address/subnet)
            prefix_match = prefix_pattern.search(route)
            prefix = prefix_match.group(1)

            # Extract the route
            route_match = route_pattern.search(route)
            next_hop = route_match.group(1)

            # Create dictionary for this route,
            # and add it to the list
            route = {'prefix': prefix, 'next-hop': next_hop}
            intf_routes[intf].append(route)
        
        # Display a blank line to make easier to read
        print('')

        # Display a title
        print('OSPF routes out of GigabitEthernet interfaces')
        
        # Display the GigabitEthernet interfaces routes
        pprint(intf_routes)
        # Display a blank line to make easier to read
        print('')

        # Close the file
        file.close()

