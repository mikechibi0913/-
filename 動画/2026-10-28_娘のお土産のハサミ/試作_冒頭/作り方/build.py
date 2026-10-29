import subprocess, sys
from pathlib import Path
S=Path(sys.argv[1]); out=Path(sys.argv[2]); src=Path(sys.argv[3])
lines=src.read_text(encoding='utf-8').split('\n---')[0].strip().splitlines()
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(f)]))
lead=0.8; t=lead; ev=[]; parts=[]
for i,l in enumerate(lines,1):
    f=S/'lines'/f'line{i:02d}.wav'; d=dur(f)
    gap=1.0 if l.endswith('…') else (0.2 if i==12 else 0.5)
    if i==1: gap=1.3
    ev.append((t,t+d+(0.15 if i!=12 else 0.1),l)); parts.append((f,d,gap)); t+=d+gap
total=t+1.5
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h}:{m:02d}:{s:05.2f}"
ass=["[Script Info]","ScriptType: v4.00+","PlayResX: 1920","PlayResY: 1080","",
"[V4+ Styles]","Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Main,IPAGothic,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,5,2,2,80,80,90,1",
"Style: Center,IPAGothic,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,0,5,80,80,0,1",
"Style: Credit,IPAGothic,30,&H00DDDDDD,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,2,0,9,40,40,30,1","",
"[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for i,(a,b,l) in enumerate(ev,1):
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},{'Center' if i==1 else 'Main'},,0,0,0,,{{\\fad(250,250)}}{l}")
ass.append(f"Dialogue: 0,{ts(0)},{ts(total)},Credit,,0,0,0,,VOICEVOX:青山龍星")
(S/'op.ass').write_text('\n'.join(ass)+'\n',encoding='utf-8')
# audio
inputs=[]; fc=[]
for k,(f,d,g) in enumerate(parts):
    inputs+=['-i',str(f)]; fc.append(f"[{k}:a]aresample=48000,apad=pad_dur={g}[a{k}]")
fc.append(f"aevalsrc=0:d={lead}:s=48000[s0]")
fc.append("[s0]"+''.join(f"[a{k}]" for k in range(len(parts)))+f"concat=n={len(parts)+1}:v=0:a=1,apad=pad_dur=1.5[aout]")
subprocess.run(['ffmpeg','-y','-v','error',*inputs,'-filter_complex',';'.join(fc),'-map','[aout]',str(S/'op.wav')],check=True)
end1=ev[0][1]+0.6
vf=f"drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:enable='lt(t,{end1:.2f})',ass={S/'op.ass'}"
subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i',f'color=c=0x2B1C14:s=1920x1080:r=30:d={total:.2f}','-i',str(S/'op.wav'),
 '-vf',vf,'-c:v','libx264','-pix_fmt','yuv420p','-preset','medium','-crf','23','-c:a','aac','-b:a','160k','-shortest',str(out)],check=True)
print('total',round(total,1))
