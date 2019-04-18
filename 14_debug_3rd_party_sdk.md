# Inspect an Objective-C SDK with lldb
#### dump the classes
https://github.com/DerekSelander/LLDB
```
dclass -o my_app
```

#### search classes on Heap
```
(lldb) search RSADeviceInfo
<RSADeviceInfo: 0x1d019e780>
```
#### Inspect interesting Methods
```
(lldb) methods 0x1d019e780
<RSADeviceInfo: 0x1d019e780>:
in RSADeviceInfo:
	Properties:
		@property (retain) NSString* Timestamp;  (@synthesize Timestamp = Timestamp;)
		@property (retain) NSString* HardwareID;  (@synthesize HardwareID = HardwareID;)
		@property (retain) NSString* SIM_ID;  (@synthesize SIM_ID = SIM_ID;)
		@property (retain) NSString* PhoneNumber;  (@synthesize PhoneNumber = PhoneNumber;)
		@property (retain) RSAGeoLocationInfo* GeoLocation;  (@synthesize GeoLocation = GeoLocation;)
		@property (retain) NSString* DeviceModel;  (@synthesize DeviceModel = DeviceModel;)
```
#### Invoke instance methods
```
(lldb) po [0x1d019e780 DeviceName]
Security iPhone 8

(lldb) po [0x1d019e780 DeviceModel]
iPhone

(lldb) po [0x1d019e780 jailBreak]
0x0000000000000005  // very jailbroken
```
#### Create a class
```
(lldb) settings set target.language objc

(lldb) exp RSADeviceInfo *$rsa = (id)[[RSADeviceInfo alloc] init]

(lldb) po $rsa
<RSADeviceInfo: 0x1c819ddc0>
```

