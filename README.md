# CSAW'18: The Maple Cookie Army github - Eléonore Carpentier & Corentin Thomasset
**Maple Cookie Army for the win !**

🏆  EDIT: We did it! We won the European final of the Embedded security Challenge 🏆 


[Winners](https://csaw.engineering.nyu.edu/esc/csaw18-winners)

### 2018 Challenge Description
>*Lean Enterprise Advanced Knowledge Solutions (LEAKS) is a private technology company that gets awarded most of the defense and military contracts of the country of IoTilandia. Given the sensitive nature of its contracts, LEAKS employs **a complete air-gap separation** for all its internal networks, ensuring no data is leaked through public connections.*

>*A recent presidential order requires that all IoTilandia companies, including LEAKS, "IoTize" [sic] their infrastructure by making everything smarter; coffee makers, fridges, chairs, and light bulbs. To abide to this presidential order, LEAKS has installed sophisticated smart light bulbs in their offices and connected them to their internal network.*

>*In the CSAW Embedded Systems Challenge 2018 (ESC18), you are tasked to exploit these newly installed smart light bulbs to exfiltrate IoTlandia secrets, **bridging the air-gapped networks** of LEAKS.*



### Références & documentation
---
* [CSAW ESC Github](https://github.com/momalab/csaw_esc_2018)
#### Attacks
* [Ingenious Lightbulb Hack Can Cause Seizures, Spy On 'Air-Gapped' Networks](https://www.forbes.com/sites/thomasbrewster/2016/04/01/philips-lightbulb-hack-epileptic-seizures-data-theft/#57cff12678de)
* [Ops, hackers can exfiltrate data from air-gapped networks through a malware controlled via a scanner](https://securityaffairs.co/wordpress/58264/hacking/air-gapped-network-scanner-hack.html)
* [Researchers Shine Light on Smart-Bulb Data Theft](https://threatpost.com/researchers-shine-light-on-smart-bulb-data-theft/137003/)
#### Reverse engineering Magic Blue Bluetooth Bulb
* [Reverse Engineering a Bluetooth Lightbulb](https://medium.com/@urish/reverse-engineering-a-bluetooth-lightbulb-56580fcb7546)
* [Even More Bluetooh Smart Bulb Hacking](https://medium.com/@urish/even-more-bluetooth-smart-bulb-hacking-fe888a1ab601): Dump du firmware 
* [Inside The Bulb: Adventures in Reverse Engineering Smart Bulb Firmware](https://hackernoon.com/inside-the-bulb-adventures-in-reverse-engineering-smart-bulb-firmware-1b81ce2694a6)
#### Javascipt Bluetooth API
* [Web Bluetooth API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API)
* [Interact with Bluetooth devices on the Web](https://developers.google.com/web/updates/2015/07/interact-with-ble-devices-on-the-web)
* [An introduction to the Web Bluetooth API](https://dev.opera.com/articles/web-bluetooth-intro/)
* Bluetooth internals chrome page: chrome://bluetooth-internals/
#### Python API
* [Magicblue](https://github.com/Betree/magicblue)
#### Sniffer
* [Reverse Engineering a Bluetooth Low Energy Light Bulb using Bluefruit BLE Sniffer](https://learn.adafruit.com/reverse-engineering-a-bluetooth-low-energy-light-bulb)
* [Exploiting Bluetooth Low Energy using Gattacker for IoT - Step-by-Step Guide](https://blog.attify.com/hacking-bluetooth-low-energy/)
* [How To: Building a BlueSniper Rifle](https://www.smallnetbuilder.com/wireless/wireless-howto/24256-howtobluesniperpt1?showall=&start=3)
