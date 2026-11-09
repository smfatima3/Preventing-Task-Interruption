import modal
import simple_diagnostics as d
d.IMAGE=modal.Image.from_id('im-01M6ZX270TBSE6ZYSSW8VCFD1W')
cmd=d.COMMANDS['simple_native'][1].replace("headless=True)","headless=True, render_hz=50, physics_dt=0.002)")
d.COMMANDS['native_timing_corrected']=('RTX-PRO-6000',cmd)
d.run('native_timing_corrected')
