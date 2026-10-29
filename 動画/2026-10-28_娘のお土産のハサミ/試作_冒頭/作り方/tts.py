import sys, multiprocessing
from pathlib import Path
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
V=Path('/home/user/voicevox')
ort=Onnxruntime.load_once(filename=str(V/'voicevox_onnxruntime-linux-x64-1.17.3/lib/libvoicevox_onnxruntime.so.1.17.3'))
syn=Synthesizer(ort, OpenJtalk(str(V/'open_jtalk_dic_utf_8-1.11')), cpu_num_threads=max(multiprocessing.cpu_count(),2))
with VoiceModelFile.open(str(V/'15_0160.vvm')) as m: syn.load_voice_model(m)
# usage: tts.py style_id outdir prefix text...
style=int(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True); pre=sys.argv[3]
for i,t in enumerate(sys.argv[4:],1):
    q=syn.create_audio_query(t,style)
    (out/f'{pre}{i:02d}.wav').write_bytes(syn.synthesis(q,style)); print('ok',i,t)
