# YAMERO's German Syllatype

This is the system plugin for YAMERO's German Syllatype system, designed by [YAMERO](https://github.com/YAMEROOOO) and implemented by [Kaoffie](https://github.com/Kaoffie).

Older versions of this system on PyPI can be found under the name [plover-delta-de](https://pypi.org/project/plover-delta-de/).

## Contents:

- [YAMERO's German Syllatype](#yameros-german-syllatype)
  - [Contents:](#contents)
  - [Introduction:](#introduction)
  - [Rules:](#rules)
  - [Hidden letters:](#hidden-letters)
  - [Other combinations:](#other-combinations)
  - [Dictionary Formats](#dictionary-formats)
    - [JSYL Dictionaries](#jsyl-dictionaries)
    - [SYL Dictionaries](#syl-dictionaries)
  - [TLDR](#tldr)
      - [Layout](#layout)
      - [Steno order](#steno-order)
      - [Details](#details)
  - [Dealing with Conflicting Words](#dealing-with-conflicting-words)
      - [1. Option:](#1-option)
      - [2. Option:](#2-option)
      - [3. Option:](#3-option)
  - [List of Conflicting Words](#list-of-conflicting-words)
  - [Addendum](#addendum)


## Introduction:

This chapter will explain basic terms like stroke, steno order and raw steno while talking a bit about the basics of plover. More information can be found on the [Steno Glossary](https://github.com/openstenoproject/plover/wiki/Glossary). 

The basic idea of stenography is to write words faster than typing the letters one by one. This is accomplished by pressing multiple keys on a keyboard (which is usually a special machine, but can also be a normal NKRO-keyboard). Pressing multiple buttons at once is called a stroke, and the program "Plover" translates these strokes via a dictionary into regular words. 

Plover is just the base program and what pressing each key will output will be decided by the theory which is being used. Theories are often in the form of plugins one can install, as well as dictionaries which need to be added in order for the plugin to work. For a more in-depth (and probably way better) explanation, check out the YouTube playlist "[Plover And Stenography](https://www.youtube.com/playlist?list=PLatiIGGUmVcvXHf-uiScllH33-mY_Lc1_)" by [Aerick](https://github.com/aerickt); while it mainly focuses on the basic English theory, it is still generally helpful for understanding how plover works. 

Another basic concept is steno order. The keys on a steno keyboard follow an order that usually goes from left to right (as one would write and read in most languages). tThere is usually a bank of consonants on the left, a bank of vowels at the bottom and a bank of consonants on the right (a bank is referring to multiple keys, usually 4 for the vowels and 8 to 12 for the consonants). 

Pressing any of the keys with no added dictionary will output the raw steno of the input. Raw steno just means that the output looks like each key that was pressed in a single string of characters. For example:

| Keys | Left Bank | Right Bank |
|:---:|:---:|:---:|
| `T` | `T` | `-T` |
| `S` | `S` | `-S` |
| `S` and `T` | `ST` | `-TS` |

The raw steno for pressing `T` in the left bank would look like this: `T`, while the raw steno for pressing `T` in the right bank would look like this: `-T`. When there is a "-" before the letter, this means that the key being pressed is on the right. This is used to distinguish the keys that are on both sides. If the key is on the left, then there would be no "-", but sometimes for the sake of clarity, we may write `T-`. 

If there are keys from the middle bank pressed (like trying to write "sos") there is no need to differentiate, so it would look like `SOS` (and not `S-O-S`). If more than one key is pressed in either bank, the order of these keys is determined by the steno order of the corresponding theory, so if the steno order is `STAOEUTS` (with the banks `[ST]`, `[AOEU]` and `[TS]`, where `ST` are the keys in the left bank, `AOEU` are the keys in the middle bank and `TS` are the keys in the right bank) then pressing `STOST` would get the output `STOTS` instead. 

Each stroke will always follow the steno order of the layout used. Two strokes are separated by a `/`; it is not possible for a key to appear two times in either part of the Stroke (all the keys in a stroke are pressed simultaneously, thus one cannot click a key two times) so something like `SSOTT` is not a possible stroke.

An example with this theory would be this:
`^F*AR>/<TNIU/^PNERT>` which would translate to "Hallo Welt" (Hello World).

> Reminder: These instructions are for this German theory and thus my further examples will revolve around this theory.

The steno layout and order for my theory are the following and can also be seen in the image below:

Layout:
```
F- T- N- *- ^    -> -* -N -T -F <
K- S- P- R- ^    -> -R -P -S -K <
         A  E     I  U
```

Steno order:
`SKFPTNR*AEIURNTPSKF*>`

![keys](https://user-images.githubusercontent.com/71076286/196929655-74b2221c-be4d-4d86-bf3f-631639927a7b.png)


## Rules:

This system is orthographic. This means that all words are written as one would spell them. Try, for example, writing the word "kauft". It will be written by pressing the `K-` key, the `A` and the `U` key, as well as the keys `-F` and `-T`. Other words like "reis", "stern" or "pfau" work in the same way. On the other hand, words like "clown" will need letters that are not present on the keyboard. Further explanation for this will follow in the next chapter. 

Right now though, this chapter will only talk about the basics of this plugin. Each word has to be written in syllables, and those syllables have to have vowels in the middle and optionally consonants on the sides. There can't be syllables such as "Safe" (which is an English word used by Germans) because there are vowels in the middle AND at the end of the syllable. (Remember that a stroke has three parts, an initial part with only consonants from the left bank, a middle part with only vowels from the middle bank, and a final part with only consonants from the right bank.) Hence, "Safe" would have to be split into 2 Syllables in order to be written. Pressing `SA` and the `FE` would be the way, though trying this out will output "sa fe" instead of "Safe". 

Here, the `^` and `<` keys are needed, also called "capitalize-key" or "c-key" and "glue-(together)-key" or "g-key". These (as their names suggest) capitalize a syllable or "glue" a syllable to the previous one (that is the reason why the arrows point in these directions). To capitalize a syllable, one simply needs to press the c-key together with the other keys of the stroke. In the example of "Safe" one would press `^SA` to get "Sa". Now to glue the second syllable to the first one simply presses the g-key together with the syllable that needs to be attached to the previously written part. Doing this together will output "Safe" (by inputting `^SA/<FE`).

The reason this is so different from most other stenography systems (that usually operate on words rather than syllables that need to be "glued" together manually) is that the nature of the German language requires such a system. In German one can combine a lot of words (especially nouns) and get a perfectly fine German word. Like "Müll" ("trash") and "Eimer" ("bucket") gives "Mülleimer" ("trashcan"). So far so good, but in German this keeps on going further: "Plastikmülleimerdeckel" ("plastic trashcan lid") is one German word and there are a lot of those really long ones.

## Hidden letters:

Some letters like "d" and "m" can't be found on the keys. To access these, a special key labeled `*` is needed. Pressing `*` and `T` on one side (either right or left) will output a "d". This works for most letters, and the "counterparts" to each letter are in the following table:

| output | input |
| :---: | :---: |
| h | `-F*` |
| g | `-K*` |
| b | `-P*` |
| z | `-S*` |
| m | `-N*` |
| d | `-T*` |


> These can of course be written on both sides, for the sake of simplicity this will only cover the left side if it is different from the right side.

The only letter which does not have a counterpart here is the `R` key. The reason behind this and the further uses of this key (as well as it’s hidden counterpart) will be explained later on.

As one can see, the counterparts are usually the "softer" versions of the letters (`T` and "d", `K` and "g" as well as `P` and "b"). The reason `S` is in the layout instead of being the "soft" counterpart of "z" is just because the letter "s" is used more frequently in German language (this is also true for the other letters). Others like `N` and "m" are just counterparts out of obvious reasons. `F` and "h" just have their reason to be counterparts due to there being no German words with an "f" and an "h" together at either the end or the start of a syllable; therefore one won't run into issues of needing to press `F` and `F*`(h) on the same side in the same stroke. As a mnemonic, one can think about the `F` being a really "soft" sound and the "h" being even "softer" (they also look pretty alike).

But there are still letters missing, like c, j, l, o, q, v, w, x, y and ß, as well as the so called "umlaute" ä, ö and ü. Due to most of these being sparely used in the German language, they are hidden behind combinations of letters. Some of them are intuitive, whilst others aren’t. This theory is build to be as intuitive as possible, but especially here the randomness starts to take place. There is no need to worry if this gets a little confusing at first, it is just a matter of memorization and practice. The missing letters are in the following table:


| Output | Input | Explanation |
| :---: | :---: | :---: |
| c | `-PK` |This combination is purely random |
| j | `*I` | "i" looks kind of like "j" so "j" is the counterpart of `I` |
| l (Left L) | `TN-` | This combination is random |
| l (Right L) | `-R>` | This is random aswell and will be explained in the next chapter |
| o | `IU` | One vowel had to go and "o" was the least common, also "o" usually never appears together with either "i" or "u" |
| q | `-NPK` | Words that start with "q" usually sound like "kw" (which is `KNP`) |
| v | `-NPF` | Similar to the "q" but here it is just because the "v" looks like a "w" (or at least half a "w") and is used similar to "f" |
| w | `-NP` | This combination is purely random |
| x | `-RPSK` | The "x" in a word usually sounds like a "ks" (though `R` and `P` are random) |
| y | `EU*` | "y" in the middle of a word sounds like "ü" (which also can be written as "ue"). The `*` is there to clarify the difference between "y" and "ue". |
| ä | `AEI` | To differetiate "ae" and "ä" an `I` was added (because German has no "Ï") |
| ö | `AIU` | Since "o" is `IU` just doing `EIU` would be the same as "ü" so it had to be another combination with `IU` (the only one being left was `AIU`) |
| ü | `EIU` | Same as "ä" (and also the reason why "y" can’t be `EIU`) |
| ß | `-PSK` | This combination is purely random |

> Here the letter "l" has two input methods, depending on the side the l is needed.

## Other combinations:

There are some other issues one can run into while trying to write certain words like "bann", "zahm" or "siel". These require other combinations as well as the `>` key (which acts as another extra key similar to the `*` and is not to be confused with the g-key). 

Usually the `>` key is used to double a letter like the "n" in "bann". To write "bann" one simply strokes `P*AN>`. The same works with most of the other letters except for "r" and "l" which, due to "l" being `-R>` on the right side, have other combinations which will be listed below. Also, if a vowel needs to be doubled like in "see" or "tee" one simply types the vowel along with the `>` and the right `*` (so "see" would be `SE*>` and "tee" would be `TE*>`). The `>` key can also be used if the `*` needs to be doubled, like in the word "zahm" which would be `S*ANF**` (rearranged from `S*AF*N*`) but needs to be stroked as `S*ANF*>`. 

As seen in the above chapter, the `>` key is also used to write the letter "l" on the right side. Furthermore, the `>` key can be used to distinguish "chs" from "sch" as in "Lachs" (`^TNASKF>`) and "lasch" (`TNASKF`). As seen there, the combination for writing an "sch" is `SKF` (which makes sense due to `K` being similar to "c" and "h" being the counterpart to `F`). Therefore, the "ch" alone with no "s" in the same part of the stroke is `KF`. The only time when a `S` is pressed together with a `KF` in the same bank but does not form an "sch" or "chs" is when this `S` is used to stroke a "z" as in "schluchz" (`SKFTNUSKF*`). This is really important due to words like "nachts" and "nascht" being stroked the same way. For the "ck" another combination of letters is needed, which can also be seen below.

Another problem occurs with the word "siel" which requires the same inputs as "seil" (`SEIR>`). Thus, every "ie" needs to be stroked as `AE` instead of `EI` (a pony for this are english words like "beamer", where the "ea" sounds like a german "ie" as in "biegen".

Here are all the combinations from this chapter:

| Output | Input |
| :---: | :---: |
| ff | `-F>` |
| pp | `-P>` |
| bb | `-P*>` |
| nn | `-N>` |
| mm | `-N*>` |
| gg | `-K*>` |
| ss | `-S>` |
| zz | `-S*>` |
| tt | `-T*>` |
| rr | `-RNP` |
| ll | `-RNP>` |
| aa | `A*>` |
| ee | `E*>` |
| oo | `IU*>` |
| sch | `-SKF` |
| chs | `-SKF>` |
| ch | `-KF` |
| ck | `-RPK` |
| ie | `AE` |


## Dictionary Formats

This system supports all regular dictionary formats, such as json. It also comes with support for two additional formats: **DSD**, and **DWD**. In both formats, keys within the left bank (`SKFPTNR*`), vowel bank (`AEIU`), and right banks (`-RNTPSKF*>`) can be arranged in any order within the bank itself.


### JSYL Dictionaries

```jsyl
{
"STE/NUI": "steno",
"STE/NUI/K*RAF": "stenograf",
"STE/NUI/K*RA/PF*EA": "stenographie"
}
```

### SYL Dictionaries

Use `\:` to escape `:` as in: `03\:00: TR*EIURF*`.

```
steno: STE/NUI
stenograf: STE/NUI/K*RAF
stenographie: STE/NUI/K*RA/PF*AE
```

## TLDR

If you know a lot about stenography already, this is the section for you. 

Here is the steno order and layout again:

#### Layout

```
F- T- N- *- ^    -> -* -N -T -F <
K- S- P- R- ^    -> -R -P -S -K <
         A  E     I  U
```

#### Steno order

`SKFPTNR*AEIURNTPSKF*>`

#### Details

The theory is orthographic and revolves around typing each syllable instead of each word, so the syllable has to be attached to the previous one if needed. To do that, the `<` (also called the g(lue)-key) is used together with the second syllable. Syllables that can't be written in one stroke are treated as separate syllables (so "safe" is `SA/<FE`).

Capitalization is achieved by pressing `^` (also called the c(apitalize)-key) together with the syllable that needs to be capitalized.

The `>` key is used to double letters (as well as the `*` if needed) or to create an "l" on the right side or differentiating "sch" from "chs" (though combinations of "ch" and "z" do NOT require the addition of the `>` key as in "schluchz" (`SKFTNUSKF*`) for example).

Missing Letters and other combinations can be accessed by these key combinations:

| output | input | | output | input | | output | input | | output | input |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| h | `-F*` | | g | `-K*` | | b | `-P*` | | z | `-S*` |
| m | `-N*` | | d | `-T*` | | c | `-PK` | | j | `*I` |
| l- | `TN-` | | -l | `-R>` | | o | `IU` | | q | `-NPK` |
| v | `-NPF` | | w | `-NP` | | x | `-RPSK` | | y | `EU*` |
| ä | `AEI` | | ö | `AIU` | | ü | `EIU` | | ß | `-PSK` |
| ff | `-F>` | | pp | `-P>` | | bb | `-P*>` | | nn | `-N>` |
| mm | `-N*>` | | gg | `-K*>` | | ss | `-S>` | | zz | `-S*>` |
| tt | `-T*>` | | rr | `-RNP` | | ll | `-RNP>` | | aa | `A*>` |
| ee | `E*>` | | oo | `IU*>` | | sch | `-SKF` | | chs | `-SKF>` |
| ch | `-KF` | | ck | `-RPK` | | ie | `AE` |

(Keep in mind that all combinations work for the left side as well, except for the ones where the left side has a different input)

## Dealing with Conflicting Words

Some words will still create issues because they have the same stroke as some other word. To differentiate them, the first working option in the following list should be used:

#### 1. Option:
**Example:** hemd=`F*ENT*>`=hemmt ; **Solution:** hem?=`F*ENT*>` ; hemd=`F*E_*NT.*T` ; hemmt=`F*E_*NT.*NT`

Replace the part of the translation where the disambiguation happened with a "?" to indicate to the user that further input is required. Then in the second stroke, the user can input the missing letters that got replaced by the "?" (without the need to add the g-key).

#### 2. Option:
**Example:** samt=`SANT*`=sand ; **Solution:** sant?=`SANT*` ; samt=`SAN*T.*N` ; sand=`SANT*.*T`

Replace the part of the translation where the disambiguation occurs with the unchanged form of the characters (in this case the counterpart "m" will change back to "n" or the counterpart "d" will change back to "t") and add a "?" at the part where the disambiguation happened to indicate to the user that further input is required. Then in the second stroke, the user can input the counterpart of the letter which needs to be changed (without the need to add the g-key).

#### 3. Option:
**Example:** psi=`SPI`=spi ; **Solution:** psi=`SPI*` ; spi=`SPI`

Add a `-*` (or a `->` if `-*` is already used) in the raw steno of the syllable that is not in steno order (or is the one which uses hidden letters). If this creates an issue with another entry, add the `*-` (or a `->` if `*-` is already used) in the raw steno of the syllable that is not in steno order (or is the one which uses hidden letters).
Note: This Option requires memorization of this disambiguation.

## List of Conflicting Words

The conflicting words are listed in .dwd:

| Option | Conflicts | |
| :---: | :---: | :---: |
| 2 | samt, `SAN*T.*N` | sand, `SANT*.*T` |
| 2 | brems, `PR*E*NS.*N` | brenz, `PR*E*NS.*S` |
| 3 | psi, `SPI*` | spi, `SPI` |
| 1 | hemd, `F*E_*NT.*T` | hemmt, `F*E_*NT.*NT` |
| 3 | tou, `TIU*` | to, `TIU` |

If more disambiguations are found, they will be added here.

## Addendum

First and foremost, I would like to thank [Kathy](https://github.com/Kaoffie) for creating this plugin for me. Without her constant help and quick implementation of changes to the plugin, I wouldn't have been able to create this theory in the first place. Furthermore, I want to thank the people on the plover discord that helped me out and weren't annoyed of my constant questionings regarding steno topics. 

Also, I want to say something regarding this theory and myself. This has been a passion project of mine since 2021 and was (except for the plugin) all done by me. I changed the theory multiple times as well as the dictionary and ended up translating all the (at the time of writing this around 5500) syllables by myself, so if there are any mistakes in there I'm sorry. That said, the best place to reach out to me would be my discord (YAMERO#3100) or via the [plover discord server](https://discord.gg/f47aYcst9B) where I will be talking about new improvements and updates from now on. I appreciate everyone who is willing to help me out on this project, even if it's just finding some mistakes or missing syllables and sending them to me. Be aware though that I worked on this theory a long time now, and thought about the layout and other improvement ideas dozens of times and most of them will have some issues that will create more problems than before, so I can confidently say that this is the best theory I can craft and there won't be any major changes to it, so please respect that.

**Last but not least, have fun writing!**

