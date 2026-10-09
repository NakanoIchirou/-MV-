"""Portable assembly of retained shots; optionally rebuild selected still slots."""
import os,sys,json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'06_工程与核验/缓存'
for key in ('TEMP','TMP','TMPDIR'):os.environ[key]=str(WORK/'temp')
os.environ['PYTHONPYCACHEPREFIX']=str(WORK/'python-bytecode')
os.environ['XDG_CACHE_HOME']=str(WORK)
(WORK/'temp').mkdir(parents=True,exist_ok=True)
FF=ROOT/'06_工程与核验/工具/ffmpeg.exe'
ENGINE=ROOT/'06_工程与核验/工程.json'

def run(args):
    p=subprocess.run([str(x) for x in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-4000:])
    return p.stdout
def rebuild(job,audio):
    from PIL import Image,ImageOps
    frames=job.get('slots')
    if not frames:raise ValueError(job['id']+' 保留原视频，不从首尾图补动画。')
    start=[];clock=0;prepared=[]
    for slot in frames:
        start.append(clock);clock+=slot['hold_frames']
        im=Image.open(ROOT/slot['file']).convert('RGBA');bg=Image.new('RGBA',im.size,'black');bg.alpha_composite(im)
        prepared.append(ImageOps.pad(bg.convert('RGB'),(1920,1080),method=Image.Resampling.LANCZOS,color='black'))
    expr='+'.join(f'if(eq(N,{i}),{v},0)' for i,v in enumerate(start+[clock]));stage=WORK/(job['id']+'-timing.mp4')
    args=[FF,'-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1920x1080','-framerate','60','-i','pipe:0','-vf',"setpts='"+expr+"'",'-fps_mode','vfr','-c:v','libx264','-preset','fast','-qp','16','-x264-params','keyint=1:min-keyint=1:scenecut=0:aq-mode=0','-pix_fmt','yuv420p','-an','-video_track_timescale','15360',stage]
    with (WORK/(job['id']+'.log')).open('wb') as log:
        p=subprocess.Popen([str(x) for x in args],stdin=subprocess.PIPE,stdout=log,stderr=log)
        for im in prepared+[prepared[-1]]:p.stdin.write(im.tobytes())
        p.stdin.close();assert p.wait()==0
    run([FF,'-y','-v','error','-i',stage,'-ss',str(job['start_seconds']),'-i',audio,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','320k','-t',str(clock/60),'-movflags','+faststart',ROOT/job['file']])

def main():
    engine=json.loads(ENGINE.read_text(encoding='utf-8'));jobs=engine['jobs'];audio=ROOT/engine['audio']
    args=sys.argv[1:];check_only='--check' in args;args=[x for x in args if x!='--check'];selected=args[1:] if args[:1]==['--rebuild'] else args
    if check_only and selected:raise ValueError('--check 不修改格位，请单独运行。')
    for mid in selected:
        job=next((j for j in jobs if j['id']==mid),None)
        if not job:raise ValueError('未知镜号 '+mid)
        rebuild(job,audio);print(mid+' 已重制',flush=True)
    for j in jobs:run([FF,'-y','-v','error','-i',ROOT/j['file'],'-map','0:v','-an','-c:v','copy','-video_track_timescale','15360',WORK/(j['id']+'.mp4')])
    listing=WORK/'concat.txt';listing.write_text('\n'.join("file '"+j['id']+".mp4'\nduration "+str(j['duration_seconds']) for j in jobs),encoding='utf-8')
    silent=WORK/'joined.mp4'
    run([FF,'-y','-v','error','-f','concat','-safe','0','-i',listing,'-map','0:v','-c:v','copy','-an',silent])
    # Export to a temporary file first, preserving the deliverable on failure.
    output=ROOT/engine['output'];candidate=WORK/'new-export.mp4'
    run([FF,'-y','-v','error','-i',silent,'-i',audio,'-map','0:v','-map','1:a','-vf','fps=60','-c:v','libx264','-preset','fast','-crf','18','-profile:v','high','-level:v','4.2','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-t',str(engine['duration_seconds']),'-movflags','+faststart',candidate])
    if check_only:
        p=run([FF,'-v','error','-i',candidate,'-map','0:v','-c','copy','-f','framecrc','pipe:1']).decode()
        packets=[line for line in p.splitlines() if line and not line.startswith('#')];assert len(packets)==6532
        print('独立重导出验证通过，共6532帧；基准成片未改动。',flush=True)
        return
    os.replace(candidate,output)
    front_jobs=[j for j in jobs if j['id'] in [f'M{i}' for i in range(1,13)]]
    listing=WORK/'front.txt';listing.write_text('\n'.join("file '"+j['id']+".mp4'\nduration "+str(j['duration_seconds']) for j in front_jobs),encoding='utf-8')
    front=WORK/'front-silent.mp4';run([FF,'-y','-v','error','-f','concat','-safe','0','-i',listing,'-map','0:v','-c:v','copy','-an',front])
    candidate=WORK/'new-front.mp4';run([FF,'-y','-v','error','-i',front,'-ss','2','-i',audio,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','320k','-t','48.4','-movflags','+faststart',candidate]);os.replace(candidate,ROOT/engine['front_output'])
    print('已导出 '+str(output)+'，同时更新前十二镜。',flush=True)
    print('修改后的文件会与归档时的校验清单不同；原清单仅记录 v25 基准。',flush=True)

if __name__=='__main__':main()
