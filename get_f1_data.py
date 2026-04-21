import fastf1
import json
import math
import os
import pandas as pd

print("正在连接 F1 官方接口，自动抓取包含【差距】和【安全车】的完整战术数据...")

if not os.path.exists('./cache'):
    os.makedirs('./cache')
fastf1.Cache.enable_cache('./cache')

# --- 加载比赛数据 ---
session = fastf1.get_session(2026, 'China', 'R')
session.load()
laps = session.laps

# --- 提取车队映射 ---
driver_teams = {}
for driver_number in session.drivers:
    driver_info = session.get_driver(driver_number)
    driver_teams[driver_info['Abbreviation']] = driver_info['TeamName']

# --- 提取包含Gap的排位数据 ---
race_data = []
for lap_num, lap_group in laps.groupby('LapNumber'):
    # 领跑者
    leader = lap_group[lap_group['Position'] == 1].iloc[0] if not lap_group[lap_group['Position'] == 1].empty else None
    
    if leader is None or pd.isna(leader['Time']):
        continue
        
    leader_time = leader['Time']

    for _, lap in lap_group.iterrows():
        driver, pos, driver_time = lap['Driver'], lap['Position'], lap['Time']
        
        if not any(math.isnan(x) for x in [lap_num, pos]) and pd.notna(driver_time):
            # 计算时间差
            time_delta = driver_time - leader_time
            # 将 timedelta 转换为总秒数
            gap_seconds = time_delta.total_seconds()
            
            race_data.append({
                "driver": driver, 
                "team": driver_teams.get(driver, "Unknown"),
                "lap": int(lap_num), 
                "position": int(pos),
                "gap": round(gap_seconds, 3) 
            })

print(f"✅ 成功计算了 {len(race_data)} 条包含Gap的圈速数据！")

# --- 提取进站数据 ---
pit_stops = []
for _, row in laps.loc[laps['PitInTime'].notna()].iterrows():
    if row['Driver'] in driver_teams:
        stop_duration_val = row['PitOutTime'] - row['PitInTime'] if pd.notna(row['PitOutTime']) else None
        pit_stops.append({
            "driver": row['Driver'],
            "lap": int(row['LapNumber']),
            "compound": row['Compound'],
            "stopDuration": stop_duration_val.total_seconds() if stop_duration_val else None
        })

# --- 提取轮胎使用数据 ---
stints = []
for _, stint_group in laps.groupby(['Driver', 'Stint']):
    first_lap_of_stint = stint_group.iloc[0]
    if pd.notna(first_lap_of_stint['Compound']):
        stints.append({
            "driver": first_lap_of_stint['Driver'],
            "startLap": int(first_lap_of_stint['LapNumber']),
            "compound": first_lap_of_stint['Compound']
        })

# --- 提取SC和VSC时段 ---
safety_cars = []
track_status = session.track_status
SC_STATUS, VSC_STATUS = '4', '6'
current_sc_period = None

for index, row in track_status.iterrows():
    status, time = row['Status'], row['Time']
    
    if status in [SC_STATUS, VSC_STATUS] and current_sc_period is None:
        try:
            lap_at_time = laps.loc[laps['Time'] >= time].iloc[0]['LapNumber']
            current_sc_period = {
                "type": "SC" if status == SC_STATUS else "VSC",
                "startLap": int(lap_at_time)
            }
        except IndexError:
            # 如果安全车在第一圈开始前就出动，则从第一圈算起
            current_sc_period = {
                "type": "SC" if status == SC_STATUS else "VSC",
                "startLap": 1
            }
            
    elif status == '1' and current_sc_period is not None:
        try:
            lap_at_time = laps.loc[laps['Time'] >= time].iloc[0]['LapNumber']
            current_sc_period["endLap"] = int(lap_at_time)
            safety_cars.append(current_sc_period)
        except IndexError:
            # 如果比赛在安全车带领下结束
            current_sc_period["endLap"] = int(laps['LapNumber'].max())
            safety_cars.append(current_sc_period)
        current_sc_period = None

final_data = {
    "raceData": race_data,
    "pitStops": pit_stops,
    "stints": stints,
    "safetyCars": safety_cars
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=2)

print(f"✅ 成功自动抓取到 {len(safety_cars)} 段安全车时段！")