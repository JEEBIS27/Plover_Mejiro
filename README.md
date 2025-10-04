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
![image](https://github.com/user-attachments/assets/1235dff7-703a-4e50-8ba2-946b88834139)

```
#  S  T  Y  I  U    U  I  Y  T  S  *
#  S  K  N  A  U    U  A  N  K  S  *
               n    n             
            t  k    k  t
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
| --- | 前回の母音 |
| あ段   | `A`   |
| い段   | `I`   |
| う段   | `U`   |
| え段   | `IA`  |
| お段   | `AU`   |
| や段   | `YA`  |
| ゆ段   | `YU` |
| よ段   | `YAU`  |

※母音キーを入力しなかった場合、直前に入力した文字の母音を引き継ぎます

####（例）
`AUn-KAU``TI-SIn` → 「温故知新」

`AUn-K``TI-Sn` → 「温故知新」

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
| ま行     | `SK`   |
| ら行     | `ST`   |
| わ/を    | `SKN`   |
| が行     | `KN`  |
| ざ行     | `NS` |
| だ行     | `TN`  |
| ば行     | `TKN` |
| ぱ行     | `STK` |
| ふぁ行     | `STN` |
| ぁぃぅ等    | `STKN` |

※「段」と「行」を組み合わせることで五十音を作ることができます.

また、規則として、Nと同時押しで濁音化しています.

#### (例)
「か行」`K` +「あ段」`A` = `KA` →「か」

「が行」`KN` + 「あ段」`A` = `KNA` → 「が」

---
### 2音目(Extra)

| 出力      | 入力 |
| ------- | ---- |
| ん       | `n`  |
| つ       | `t`  |
| く       | `k`  |
| ち       | `nt` |
| き       | `nk` |
| っ (促音)  | `tk` |
| ー（外来長音)| `ntk` |

※ このキーを組み合わせると音の最後に二音目の音を追加できます.

これは、特に音読みの漢字に対して使います

#### (例)
`TAk` →「たく」,`SAn` →「さん」

---
### 特別な母音(Special Vowels)

「あ・い・う・え・お・や・ゆ・よ」以外の組み合わせのときは、日本語で高頻度で出現する二重母音を打てるようになっています

#### 特別な母音一覧
|  出力  |  入力  |
| --- | --- |
| あい  | `Y` |
| えい  | `YIA` |
| うい  | `IU` |
| よう  | `YI` |
| ゆう   | `YIU` |
| おう  | `IAU` |
| うう  | `YIAU` |

---
### 特殊(Special)

| 機能 | 入力  |
| --- | --- |
| 繰り返す | `#` |
| 略語符号 | `*` |

※`#`を押すと,全体の出力がもう一度繰り返されます.

`TKAn-TAtkn` →「ハンター」

`TKAn#TAtkn` →「ハンターハンター」

※`*`は、略語か音節ストロークかの区別に使います
  Mejiro_users.jsonで登録する略語には最後に*をつけることを推奨しています

####（例）
`KAU-SKYU` → 「コミュ」

`KAU-SKYU*` → 「コミュニケーション」

また、最後の文字が「ん」かつ最後から二文字目の母音が「い」の時は、最後に「ぐ」を追加して出力する機能もあります

####（例）

`TKNY-KIn` → 「バイキン」

`TKNY-KIn*` → 「バイキング」

---
## もっと詳しく知りたい方は(More To Know the Theory)

[note](https://note.com/jeebis_keyboard/n/ndb99792d80e9)
  (It's written in only Japanease)
