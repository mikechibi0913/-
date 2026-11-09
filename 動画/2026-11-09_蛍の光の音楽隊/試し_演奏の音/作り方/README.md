# 試しの演奏の音の作り方（2026-11-09）

- 曲：蛍の光（オールド・ラング・サイン）の元の4拍子の旋律（スコットランド民謡）。閉店の「別れのワルツ」（3拍子の編曲）は使っていない
- 速さ：1分に48拍（本編 第8章「ふだんの半分ほどのゆっくりした旋律」に合わせた）。1番の8小節・約43秒
- 楽器の音：FluidR3_GM（Frank Wen・MIT License）。規約は `調べもの/2026-11-09_演奏の音を作る道具の規約.md`
  - クラリネット＝General MIDI 72番（プログラム71）／バグパイプ＝110番（プログラム109）
- 第8章版：バグパイプは旋律の約半分から、低いファ（F3）1音だけを小さく入れ、少しずつ大きくした（本編「低い音だけを、そっと」「主役にならないよう」）

## 作り直し方
1. `sudo apt-get install fluidsynth fluid-soundfont-gm`（Ubuntu）
2. `python3 make_midi.py ..`（MIDIを2つ作る）
3. `fluidsynth -ni -g 0.8 -r 44100 -F 出力.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 入力.mid`
4. `ffmpeg -i 出力.wav -af "loudnorm=I=-20:TP=-2" -b:a 192k 出力.mp3`

## 概要欄のクレジット（入れる場合の案）
楽器の音：FluidR3_GM（Frank Wen・MIT License）
