# Reproduction de LFA sur contrôleur ONOS

_Article MISC n° 109_

_Flavien Joly-Pottuz / Stefano Secci_ | _**CNAM PARIS**_

_**CNAM PARIS**_


## utilis.py
```
root@misc:/opt/LFA-Attack-ONOS/scripts# python3 utilis.py --help
usage: utilis.py [-h] [--info] [--create] [--clean] [--swap]

optional arguments:
  -h, --help  show this help message and exit
  --info      Print OVS infos
  --create    Create s1,s2 and s3 and connect to c1
  --clean     Delete s1,s2 and s3, reload c1 to wipe config
  --swap      Swap ONOS versions
```

## audit.py
```
root@misc:/opt/LFA-Attack-ONOS/scripts# python3 audit_lldp.py --help
usage: audit_lldp.py [-h] --target TARGET [--nohup]

optional arguments:
  -h, --help       show this help message and exit
  --target TARGET  Target - used for cmd generation !
  --nohup          Use nohup for cmd generation
```

## lldp_forge.py
```
root@misc:/opt/LFA-Attack-ONOS/scripts# python3 lldp_forge.py --help
usage: lldp_forge.py [-h] --delta DELTA --eth-mac-src ETH_MAC_SRC
                     [--eth-mac-dst ETH_MAC_DST] --chassis-mac CHASSIS_MAC
                     --source-port SOURCE_PORT

optional arguments:
  -h, --help            show this help message and exit
  --delta DELTA         Time between two LLDP packet
  --eth-mac-src ETH_MAC_SRC
                        Source MAC Address of LLDP packet (fingerprint)
  --eth-mac-dst ETH_MAC_DST
                        Destination MAC Address of LLDP packet (LLDP or BDDP)
  --chassis-mac CHASSIS_MAC
                        Target Chassis MA@ | format XX:XX:XX:XX:XX:XX
  --source-port SOURCE_PORT
                        Target port ID
```