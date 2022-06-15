# Rasa_sx机器人开发手册
### 数据库数据结构
```
- yeleng
  - device_name(id = computer140)
    - os_machine_value
      - cpu_IDLE
      - MEM
    - power_value
      - CPU
      - MEM
      - TOtal
    - temperature
      - CPU0_Temp
      - CPU0_VR_Temp
      - CPU1_Temp
      - CPU1_VR_Temp
      - DIMMG0
      - DIMMG1
      - Inlet
      - outlet
      - PCH
      - Psu0
      - Psu1
```
### os_machine_value
```
from(bucket: "yeleng")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["device_name"] == "computer140")
  |> filter(fn: (r) => r["_field"] == "os_machine_value")
  |> filter(fn: (r) => r["os_machine_type"] == "CPU_IDLE" or r["os_machine_type"] == "MEM_USED_PERCENT")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```
### power_value
```
from(bucket: "yeleng")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["device_name"] == "computer140")
  |> filter(fn: (r) => r["_field"] == "power_value")
  |> filter(fn: (r) => r["power_type"] == "CPU_Total_Power_value" or r["power_type"] == "MEM_Total_Power_value" or r["power_type"] == "Total_Power_value")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```
### temperature_value
```
from(bucket: "yeleng")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["device_name"] == "computer140")
  |> filter(fn: (r) => r["_field"] == "temperature_value")
  |> filter(fn: (r) => r["temperature_type"] == "CPU0_Temp_value" or r["temperature_type"] == "CPU0_VR_Temp_value" or r["temperature_type"] == "CPU1_Temp_value" or r["temperature_type"] == "CPU1_VR_Temp_value" or r["temperature_type"] == "DIMMG1_Temp_value" or r["temperature_type"] == "DIMMG0_Temp_value" or r["temperature_type"] == "Inlet_Temp_value" or r["temperature_type"] == "Outlet_Temp_value" or r["temperature_type"] == "PCH_Temp_value" or r["temperature_type"] == "PSU0_Temp_value" or r["temperature_type"] == "PSU1_Temp_value")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```