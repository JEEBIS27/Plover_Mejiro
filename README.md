# メジロ式速記(Plover Mejiro)

Plover用の日本語の速記システム

A Japanese stenography system for Plover.

![image](https://github.com/user-attachments/assets/6763813f-cf4d-448d-9acd-da6e0faac4e6)

---
## メジロ式をインストールする(Installing Mejiro)

このプラグインをPyPIでないプラグインとしてインストールします.

(手動でこれをインストールする場合は``Plover wiki``の[Plugins not on PyPI](https://plover.wiki/index.php/Plugins#Plugins_not_on_PyPI)に従ってください.)

Install this plugin as a non-PyPI plugin.

(To install this manually, follow the section under [Plugins not on PyPI](https://plover.wiki/index.php/Plugins#Plugins_not_on_PyPI) on the Plover wiki.)

---
## メジロ式を起動する(Activating Mejiro)

このプラグインをインストールしたあと,次のようにしてPloverで起動します.

Ploveメニューの歯車マーク``configuration``から``Systems``タブを開き,``Mejiro``システムを選択して起動します.

After installing this plugin, you need to turn it on in Plover:

In Plover's ``configuration``, go to the ``Systems`` tab, and change the active system to ``Mejiro``.

---
## レイアウト(Layout)
このシステムは普通のQwertyキーボードでも使うことができます.

より快適に使うためには親指のキーが分かれているものを使うことをおすすめします.

You can use this steno with a QWERTY keyboard, though it’s better with one that has more than two thumb keys, such as space and others.
![image](https://github.com/user-attachments/assets/8f78564c-b86d-4b81-91cd-e9d8f7063da9)
```
#  Y  K  S  I  U  U  I  S  K  Y  *
#  Y  T  N  A  O  O  A  N  T  Y  *
   -  -  -  t  k  k  t  -  -  -
               n  n             
```
キーボード上では次のようになっています.

which originally look like
```
esc q  w  e  r  t  y  u  i  o  p  [
tab a  s  d  f  g  h  j  k  l  ;  '
    z  x  c  v  b  n  m  ,  .  
            space  enter   
```
※あなたのキーボード配置とは異なる可能性があります.異なる場合,Ploveメニューの歯車マーク``configuration``から``machine``タブを開き,キー配置を変更してください.

The default key layout may be different from your keyboard. If so, in Plover's ``configuration``, go to the ``Systems`` tab, and change the layout.

---
## 使い方(How to use)

### 母音(Vowels)

| 出力  | 入力    |
| --- | ----- |
| あ段   | `A`   |
| い段   | `I`   |
| う段   | (なし)  |
| え段   | `AI`  |
| お段   | `O`   |
| や段   | `U`  |
| ゆ段   | `OU` |
| よ段   | `YI`  |

※「う段」は母音キーを使わず子音キーのみで入力,
  「あ行」の「う」単体は「わ行」の `TKN` のみで入力します.

---
### 子音(Consonants)

| 出力     | 入力    |
| ------ | ----- |
| あ行     | (なし)  |
| か行     | `K`   |
| さ行     | `S`   |
| た行     | `T`   |
| な行     | `N`  |
| は行     | `TK`   |
| ま行     | `TN`   |
| ら行     | `KS`   |
| わ/を    | `TKN`   |
| が行     | `NS`  |
| ざ行     | `TS` |
| だ行     | `KN`  |
| ば行     | `TKS` |
| ぱ行     | `TNS` |
| ふぁ行     | `KNS` |
| ぁぃぅ等    | `TKNS` |

※「段」と「行」を組み合わせることで五十音を作ることができます.

#### (例)
「か行」`K` +「あ段」`A` = `KA` →「か」

---
### 2音目(Extra)

| 出力      | 入力   |
| ------- | ---- |
| つ       | `t`  |
| く       | `k`  |
| ん       | `n`  |
| ち       | `tn` |
| き       | `kn` |
| っ (促音)  | `tk` |
| ー（外来長音)| `tkn` |

※このキーを組み合わせると音の最後に二音目の音を追加できます.
  特に音読みの漢字に対して使います

#### (例)
`TAk` →「たく」,`SAn` →「さん」

---
### Y母音(Special Vowels)

母音は,`Y`キーを押しているかそうでないかによって変化します.

#### 通常時(Yなし)
|  出力  |  入力  |
| ----- | ----- |
| う   | (なし)  |
| あ   | `A`   |
| い   | `I`   |
| お   | `O`   |
| や   | `U`  |
| え   | `AI`  |
| おう  | `AO`  |
| ゆ   | `OU` |
| ゆう  | `IU`  |
| あう  | `AIOU` |

#### Yと同時(Yあり)
|  出力  |  入力  |
|  ---  |  ---  |
| よう  | `Y` |
| あい  | `YA` |
| よ   | `YI` |
| おい  | `YO` |
| うい  | `YU` |
| えい  | `YAI` |
| おお  | `YAO` |
| あえ  | `YOU` |
| いい  | `YIU` |
| うう  | `YAIOU` |

---
### 特殊(Special)

| 機能 | 入力  |
| --- | --- |
| 繰り返す | `#` |
| 略語モード | `*` |

※`#`を押すと,全体の出力がもう一度繰り返されます.

`TKAn-TAtkn` →「ハンター」

`TKAn#TAtkn` →「ハンターハンター」

※`*`を押すと,略語モードで動作します.
  Verb辞書を使うためにも,あなた独自の略語のuser辞書を使うためにも必要です.

---
## もっと詳しく知りたい方は(To Learn Theory)

[note](https://note.com/jeebis_keyboard/n/ndb99792d80e9)
  (It's written in only Japanease)
