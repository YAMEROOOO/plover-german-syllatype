# Delta's German Stenography

This is the system plugin for Delta's German stenography system, designed by [delta](https://github.com/YAMEROOOO) and implemented by Kaoffie.

Layout: 
```
T- R- S- *- -_   ^ -* -N -S -F -e
N- P- K- F- <    ^ -R -P -K -T -e
         E- I-  -A -U"
```

Steno order: `#<^SKFPTNR*EAIURNPSKFTe_*`

## Dictionary Formats

This system supports all regular dictionary formats, such as json. It also comes with support for two additional formats: **DSD**, and **DWD**. In both formats, keys within the left bank (`SKFPTNR*`), vowel bank (`EAIU`), and right banks (`-RNPSKFTe_*`) can be arranged in any order within the bank itself, and the final `-e` key is written as a capital `E`.


### DSD Dictionaries

```json
{
"STE.NUI": "steno",
"STE.NUI.K*RAF": "stenograf",
"STE.NUI.K*RA.PF*EA": "stenographie"
}
```

### DWD Dictionaries

Use `\,` to escape commas.

```
steno, STE.NUI
stenograf, STE.NUI.K*RAF
stenographie, STE.NUI.K*RA.PF*EA
```