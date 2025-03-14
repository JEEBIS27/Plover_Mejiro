#*YTKNSAIOUtkn#*YTKNSAIOUtkn
import re

LONGEST_KEY = 1

def lookup(key):
    assert len(key) <= LONGEST_KEY
    stroke = key[0]

    if stroke == "#":
        print("key error*")
        raise KeyError

    regex = re.compile(r"(\*?)(Y?)(T?K?N?S?)(A?I?O?U?)(t?k?n?)(\-?#?)(\*?)(Y?)(T?K?N?S?)(A?I?O?U?)(t?k?n?)(1?2?3?4?5?6?7?8?9?0?)")
    regex_groups = re.search(regex, stroke)

    LeftAsterisk = regex_groups.group(1)
    LeftY = regex_groups.group(2)
    LeftConsonant = regex_groups.group(3)
    LeftVowel = regex_groups.group(4)
    LeftParticle = regex_groups.group(5)
    MiddleHyphen = regex_groups.group(6)
    RightAsterisk = regex_groups.group(7)
    RightY = regex_groups.group(8)
    RightConsonant = regex_groups.group(9)
    RightVowel = regex_groups.group(10)
    RightParticle = regex_groups.group(11)
    Numbers = regex_groups.group(12)

    print("LeftAsterisk\tLeftConsonant\tLeftVowel\tLeftParticle")
    print(LeftAsterisk + "\t\t" + LeftConsonant + "\t\t" + LeftVowel + "\t\t" + LeftParticle)

    print("RightAsterisk\tRightConsonant\tRightVowel\tRightParticle")
    print(RightAsterisk + "\t\t" + RightConsonant + "\t\t" + RightVowel + "\t\t" + RightParticle)

    #頻出順→『n,t,k,s,r,m,h,d,g,w,z,b,j,p』

    Consonants =    ["","t","k","n","s","h","m","z","g","r","d","w","p","x","b","f"]
    listconsonant = ["","T","K","N","S","TK","TN","TS","NS","KS","KN","TKN","TNS","TKNS","TKS","KNS"]

    #Vowels =    ["u","a","i","o","ii","e","ou","yuu","oo","ui"]
    #Vowels2 =   ["you","ai","ya","yo","yu","ei","oi","aa","ae","uu"]
    Vowels =    ["u","a","i","o","ya","e","ou","yuu","yu","aa"]
    Vowels2 =   ["you","ai","yo","oi","ui","ei","oo","ii","ae","uu"]
    listvowel = ["","A","I","O","U","AI","AO","IU","OU","AIO"]
    
    excepts_in = ["ni","nu","nyuu","nyou",
                  "mi","mu",
                  "wu","wya","wyu","wyo","wyuu","wyou","wii","wui","wuu","wei",
                  "di","du","de","dya","dyo","dyuu","dyou","dii","dei",
                  "fu","fyuu","fyou"]
    excepts_out = ["nu","ni","nyou","nyuu",
                   "mu","mi",
                   "u","yaa","iu","yone","ee","ue","wi","ao","uxu","we",
                   "thi","de","du","tye","sye","dhi","dei","zye","di",
                   "vu","qa","qo"]

    if LeftVowel not in listvowel:
         LeftVowel = listvowel[9]
    if RightVowel not in listvowel:
         RightVowel = listvowel[9]

    def Make(Ys,Conso,Vowel):

        output = ""
        
        if not Ys and not Conso and not Vowel:
            output = ""
        else:
            output = Consonants[listconsonant.index(Conso)]

            if Ys:
                #Yが入力されていたら
                output += Vowels2[listvowel.index(Vowel)]
            else:
                #そうでないとき
                output += Vowels[listvowel.index(Vowel)]

            if output in excepts_in:
                output = excepts_out[excepts_in.index(output)]
        print(output)
        return output

    resultL = Make(LeftY,LeftConsonant,LeftVowel)
    resultR = ""
    result = ""

    if resultL or RightY or RightConsonant or RightVowel:#ひだりに入力がある時だけ右の音を出す
        resultR = Make(RightY,RightConsonant,RightVowel)

    listParticle = ["","n","t","k","tk","tn","kn","tkn"]
    listSecondWord = ["","xn","tu","ku","xtu","ti","ki","-"]
    listLParticle = ["","}{#Space}{","}{#F6}{","}{#F7}{","}{#F8}{","}{#F9}{","}{#F10}{","}{#F10}{#F10}{"]
    listRParticle = ["","}{#Return}{",".",",","?",".}{#Return}{",",}{#Return}{","!"]

    めいし = ["ko","ta","to","ki","mo","ha"]
    助詞 = ["","no","de","ga","wo","ni","ha","mo"]
    名詞 = ["koto","tame","tokoro","toki","mono","hanasi"]

    どうし = ["","i","su","a","na","da","de","yu"]
    動詞 = [["desu","nai","ta","masu","masita","nakaxtuta","masexn","masexndesita"],
          ["iru","inai","ita","imasu","imasita","inakaxtuta","imasexn","imasexndesita"],
          ["suru","sinai","sita","simasu","simasita","sinakaxtuta","simasexn","simasexndesita"],
          ["aru","nai","axtuta","arimasu","arimasita","nakaxtuta","arimasexn","arimasexndesita"],
          ["naru","naranai","naxtuta","narimasu","nasimasita","naranakaxtuta","narimasexn","narimasexndesita"],
          ["dearu","dehanai","daxtuta","desu","desita","dehanakaxtuta","dehaarimasexn","dehaarimasexndesita"],
          ["dekiru","dekinai","dekita","dekimasu","dekimasita","dekinakaxtuta","dekimasexn","dekimasexndesita"],
          ["iu","iwanai","ixtuta","iimasu","iimasita","iwanakaxtuta","iimasexn","iimasexndesita"]]
    
    if LeftAsterisk and (resultL or LeftParticle):
            if resultL in どうし:
                resultL = 動詞[どうし.index(resultL)][listParticle.index(LeftParticle)]
            elif resultL in めいし:
                resultL = 名詞[めいし.index(resultL)] + 助詞[listParticle.index(LeftParticle)]
    if RightAsterisk and (resultR or RightParticle):
            if resultR in どうし:
                resultR = 動詞[どうし.index(resultR)][listParticle.index(RightParticle)]
            elif resultR in めいし:
                resultR = 名詞[めいし.index(resultR)] + 助詞[listParticle.index(RightParticle)]
    
    #LeftParticleになにかあって左の指の入力もあるとき
    if not LeftAsterisk and LeftParticle and (resultL or resultR):
        resultL += listSecondWord[listParticle.index(LeftParticle)]
        print(resultL)
    #RightParticleになにかあって右の指の入力もあるとき
    if not RightAsterisk and RightParticle and (resultR or resultL and LeftParticle):
        resultR += listSecondWord[listParticle.index(RightParticle)]
        print(resultR)
    elif  not resultL and not resultR:#どちらの指にも入力が無いとき
        if not Numbers:
            result = listLParticle[listParticle.index(LeftParticle)] + listRParticle[listParticle.index(RightParticle)]
        else:
            result = Numbers

    if result == "":
        result = resultL + resultR

    if not resultL and resultR and not LeftParticle:
        print("右手略語")
        return ""
    else:
        print("{^" + result + "^}")
        return "{^" + result + "^}"
