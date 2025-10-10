# メジロ式速記(Mejiro)v2

メジロ式速記は、Plover用の日本語の速記システムです

直観的な**子音＋母音＋追加音**の組み合わせで
片手で1音節、両手で2音節を一気に入力でき、

両手の10本指をフル活用した効率的な日本語入力を体験できます

---
## レイアウト(Layout)
このシステムは、メジロ式専用キーボード（Mejiro31）や、速記用キーボード（Uni v4）、スペースバーが2つあるキーボードで使うことができます

もちろん一般的なキーボードでも使うことはできますが、より快適に使うためには親指のキーが分かれているものを使うことをおすすめします

![image](https://github.com/user-attachments/assets/1235dff7-703a-4e50-8ba2-946b88834139)

```
# S T Y I U    U I Y T S *
# S K N A U    U A N K S *
         n      n             
        t k    k t
```
GeminiPRでは以下のようなレイアウトを想定しています
```
#1 S1 T P H *1    *3 F P L T D
#2 S2 K W R *2    *4 R B G S Z
           #3     #4             
           A O    E U
```
キーボードを使う場合は次のような配列を想定しています
```
esc q w e r t y u i o p [
tab a s d f g h j k l ; '
     z x c v b n m , . 
        space enter   
```
※ これはあなたのキーボード配置と異なる可能性があります
異なる場合はPloveメニューの歯車マーク``configuration``から``machine``タブを開き、キー配置を変更してください

---
## 使い方(How to use)

### 母音(Vowels)

| 出力  | 入力  |
| ---- | ---- |
| あ段  | `A`  |
| い段  | `I`  |
| う段  | `U`  |
| え段  | `IA` |
| お段  | `AU` |
| や段  | `YA` |
| ゆ段  | `YU` |
| よ段  | `YAU`|

---
### 子音(Consonants)

| 出力   | 入力   |
| ----- | ------ |
| あ行   | (なし) |
| か行   | `K`    |
| さ行   | `S`    |
| た行   | `T`    |
| な行   | `N`    |
| は行   | `TK`   |
| ま行   | `SKN`  |
| ら行   | `ST`   |
| わ行   | `SK`  |
| が行   | `KN`   |
| ざ行   | `NS`   |
| だ行   | `TN`   |
| ば行   | `TKN`  |
| パ行   | `STK`  |
| ファ行 | `STKN`   |
| ぁ行   | `STN` |

「段」と「行」を組み合わせることで五十音を作ることができます

※ 法則として、Nと同時押しで濁音化しています

#### (例)
か行`K`+あ段`A` = `KA` →「か」

が行`KN`+あ段`A` = `KNA` →「が」

---
### 2音目(Extra)

| 出力 |  入力  |
| --- | ----- |
| ん   | `n`  |
| つ   | `t`  |
| く   | `k`  |
| ち   | `nt` |
| き   | `nk` |
| っ   | `tk` |
| ー   | `ntk`|

このキーを組み合わせると音の最後に二音目の音を追加できます.

#### (例1)「ん・つ・く・ち・き」は特に音読みの漢字に対して使います
`TAk` `SAn` →「沢山」

#### (例2) 「ー」は外来語に対して使います
`TAntk` `SNAn` →「ターザン」

---
### 特別な母音(Special Vowels)

「あ・い・う・え・お・や・ゆ・よ」以外の組み合わせのときは、日本語で高頻度で出現する二重母音を打てるようになっています

| 出力 |  入力  |
| --- | ----- |
| あい | `Y`   |
| えい | `YIA` |
| うい | `IU`  |
| よう | `YI`  |
| ゆう | `YIU` |
| おう | `IAU` |
| うう | `YIAU`|

※ 母音キーを入力しなかった場合、直前に入力した文字の母音を引き継ぎます

#### (例)
普通に入力すると…

`AUn-KAU` `TI-SIn` → 「温故知新」

母音を省略すると…

`AUn-K` `TI-Sn` → 「温故知新」

二重母音も引き継げます

`KY-KN` `SI-I` → 「甲斐甲斐しい」

同じストロークでも直前の母音によって結果が変化します

`TNA` `K-SK` → 「だから」
`TO` `K-SK` → 「ところ」

---
### 特殊なキー(Special keys)

|   機能   | 入力 |
| ------- | --- |
| 繰り返し  | `#` |
| 略語符号  | `*` |

※`#`を押すと,全体の出力がもう一度繰り返されます.

`TKAn-Tntk` →「ハンター」

`TKAn#Tntk` →「ハンターハンター」

※`*`は、略語か音節ストロークかの区別に使います
  Mejiro_Users.jsonで登録する略語には最後に*をつけることを推奨しています

#### (例)

`KAU-SKYU` → 「コミュ」

`KAU-SKYU*` → 「コミュニケーション」

また、略語として登録してなくても、最後の文字が「ん」かつ最後から二文字目の母音が「い」の時は、最後に「ぐ」を追加して出力する機能もあります

#### (例)

`TKNY-KIn` → 「バイキン」

`TKNY-KIn*` → 「バイキング」

---
## もっと詳しく知りたい方は(More To Know the Theory)

最新情報は[**X**](https://x.com/jeebis_steno?s=21&t=mUKcrYIKFRt4MZLfN8wIjg)や[**note**](https://note.com/jeebis_keyboard)をご確認ください

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
