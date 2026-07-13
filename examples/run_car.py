import os
import dynamic_sound as ds

HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "resources", "sounds", "suv_dirt_road.wav")
OUT  = os.path.join(HERE, "_tmp", "dynamicsound_car.wav")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# 車：x=5m横, z=1m高さ, y=+150→-150 を20秒で通過（マイク前を通る）
source_path = ds.Path([[0.0, 5, 150, 1,  1,0,0,0],
                       [20.0,5,-150, 1,  1,0,0,0]])
# 地面反射（z=-1の鏡像）
reflection_path = ds.Path([[0.0, 5, 150,-1,  1,0,0,0],
                           [20.0,5,-150,-1,  1,0,0,0]])
# 4chマイク（原点・±2cm）
microphone_path = ds.Path([[0.0,0,0,1, 1,0,0,0],[20.0,0,0,1, 1,0,0,0]])

sim = ds.Simulation(temperature=20, pressure=1, relative_humidity=50)
mic = ds.microphones.MicrophoneArray(file_path=OUT, sample_rate=8192, positions=[
    (0.02,0,0, 1,0,0,0),(0,0.02,0, 1,0,0,0),(-0.02,0,0, 1,0,0,0),(0,-0.02,0, 1,0,0,0)])
sim.add_microphone(path=microphone_path, microphone=mic)
src = ds.sources.AudioFile(filename=RES, gain_db=20)
sim.add_source(path=source_path, source=src)         # 直接音
sim.add_source(path=reflection_path, source=src)     # 地面反射
print("running simulation...")
sim.run()

import soundfile as sf
y, srr = sf.read(OUT)
print(f"DONE -> {OUT}")
print(f"shape={y.shape}  sr={srr}  dur={len(y)/srr:.1f}s  (4ch = car passing + Doppler + 1/r + air abs + ground)")
