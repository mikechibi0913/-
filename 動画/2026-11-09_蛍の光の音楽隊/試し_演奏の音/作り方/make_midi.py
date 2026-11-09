# 蛍の光（オールド・ラング・サイン）の元の4拍子の旋律を、MIDIにする（しなちゃん・2026-11-09）
# 使い方：python3 make_midi.py 出力フォルダ
# 「別れのワルツ」（3拍子の編曲）は使わない。元のスコットランド民謡の旋律だけ
import struct, sys, os
out = sys.argv[1] if len(sys.argv) > 1 else '.'
TPB = 480  # 1拍の長さ
N = {'C4':60,'D4':62,'F4':65,'G4':67,'A4':69,'C5':72,'D5':74,'F2':41,'C3':48,'F3':53}
q=1; dq=1.5; e=0.5; h=2; dh=3
melody = [('C4',q),
 ('F4',dq),('F4',e),('F4',q),('A4',q), ('G4',dq),('F4',e),('G4',q),('A4',q),
 ('F4',dq),('F4',e),('A4',q),('C5',q), ('D5',dh),('D5',q),
 ('C5',dq),('A4',e),('A4',q),('F4',q), ('G4',dq),('F4',e),('G4',q),('A4',q),
 ('F4',dq),('D4',e),('D4',q),('C4',q), ('F4',dh+1)]

def vlq(n):
    b=[n & 0x7F]; n >>= 7
    while n: b.insert(0,(n & 0x7F)|0x80); n >>= 7
    return bytes(b)

def track(events):  # events: (tick, bytes)
    events.sort(key=lambda x: x[0]); data=b''; now=0
    for t,ev in events: data+=vlq(t-now)+ev; now=t
    data+=vlq(0)+b'\xff\x2f\x00'
    return b'MTrk'+struct.pack('>I',len(data))+data

def song(bpm, with_pipe):
    us=int(60_000_000/bpm)
    meta=[(0,b'\xff\x51\x03'+us.to_bytes(3,'big')),(0,b'\xff\x58\x04\x04\x02\x18\x08')]
    cl=[(0,bytes([0xC0,71])),(0,bytes([0xB0,91,70])),(0,bytes([0xB0,7,100]))]  # 72番クラリネット・残響
    t=0
    for i,(n,l) in enumerate(melody):
        dur=int(l*TPB); vel=58 if i<1 else 64
        cl+=[(t,bytes([0x90,N[n],vel])),(t+int(dur*0.95),bytes([0x80,N[n],0]))]
        t+=dur
    total=t
    tracks=[track(meta),track(cl)]
    if with_pipe:
        # バグパイプ（110番）は、旋律が半分すぎたところから、低い音だけをそっと（主役にならない）
        start=int(total*0.47)
        pp=[(0,bytes([0xC1,109])),(0,bytes([0xB1,7,80])),(0,bytes([0xB1,91,90]))]
        for nn in ('F3',):
            pp+=[(start,bytes([0x91,N[nn],90])),(total,bytes([0x81,N[nn],0]))]
        # 少しずつ大きくする（息を細く削った音から）
        for k in range(12):
            pp.append((start+k*TPB//2,bytes([0xB1,11,50+k*6])))
        tracks.append(track(pp))
    head=b'MThd'+struct.pack('>IHHH',6,1,len(tracks),TPB)
    return head+b''.join(tracks)

os.makedirs(out,exist_ok=True)
open(os.path.join(out,'第6章_クラリネットだけ.mid'),'wb').write(song(48,False))
open(os.path.join(out,'第8章_クラリネットとバグパイプ.mid'),'wb').write(song(48,True))
print('ok')
