"""E0 controller-resource smoke check, not E1/E2 evidence."""
import modal
import simple_diagnostics as d
d.IMAGE=modal.Image.from_id('im-01M6ZX270TBSE6ZYSSW8VCFD1W')
d.COMMANDS['controller_resource_check']=('RTX-PRO-6000','''set -eu
cd /workspace/simple
MUJOCO_GL=egl .venv/bin/python - <<'PY'
import json, numpy as np
import gymnasium as gym
import simple.envs
from simple.core.action import ActionCmd
env=gym.make('simple/G1WholebodyBendPickMP-v0',target='primitive:cube',sim_mode='mujoco',headless=True,render_hz=50,physics_dt=.002)
env.reset(seed=11)
e=env.unwrapped
for i in range(100):
    e.mujoco.apply_action(ActionCmd('loco_command',command=[0,0,0,0,0,0,0,0],motion_type='stand',keep_waist_pose=False))
    e.mujoco.step(render=False)
    print(json.dumps({'step':i,'sim_time_s':float(e.mujoco.mjData.time),'root_position_m':e.mujoco.mjData.qpos[:3].tolist(),'finite':bool(np.isfinite(e.mujoco.mjData.qpos).all())}),flush=True)
env.close()
PY
''')
d.run('controller_resource_check')
