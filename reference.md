## Global Actions

| Action | Description | Examples 
| --- | --- | --- 
| ADDAUDIO | Creates an Audio Track at the end of the Track list. | - 
| ADDAUDIO x | Creates an Audio Track where x is the Track Number of the new Track. | ADDAUDIO 1, ADDAUDIO 10
| ADDMIDI | Creates a MIDI Track at the end of the Track list. | -
| ADDMIDI x | Creates a MIDI Track where x is the Track Number of the new Track. | ADDMIDI 1, ADDMIDI 10
| ADDRETURN | Creates a Return Track at the end of the Return list. | -
| ADDSCENE | Creates a Scene at the end of the Scenes list. | -
| ADDSCENE x | Creates a Scene where x is the Scene Number of the new Scene. | ADDSCENE 1, ADDSCENE 10
| B2A | Back to Arrangement. | -
| BPM x | x is the Tempo to set in BPMs. | BPM 100, BPM 85.53
| BPM *x | x is the value to multiply the Tempo by. | BPM *0.5, BPM *2
| BPM < or > | Dec/Inc Tempo by increment of 1-BPM. | BPM <, BPM >
| BPM <x or >x | Dec/Inc Tempo by increment of x-BPM. | BPM <2, BPM >0.5
| BPM RAMP x y | Smoothly Ramp up/down the Tempo where x is the Ramp duration (in Beats) and y is the Tempo (in BPMs) at the end of the Ramp. | BPM RAMP 8 100, BPM RAMP 4 85.53
| BPM RAMP x *y | Smoothly Ramp up/down the Tempo where x is the Ramp duration (in Beats) and y is the value to multiply the current Tempo by. | BPM RAMP 16 *2, BPM RAMP 4 *0.75
| DEBUG | Activate debugging mode, which causes ClyphX to log events as they occur to assist in Troubleshooting. | -
| DELSCENE | When accessed via an X-Clip, delete the Scene the X-Clip is on. Otherwise, delete the selected Scene. In both cases, it is not possible to delete a Scene if it’s the only Scene in the Set. | -
| DELSCENE x | x is the Scene number to delete. Specify SEL for the selected Scene. It is not possible to delete a Scene if it’s the only Scene in the Set. | DELSCENE 10, DELSCENE 3, DELSCENE SEL
| DEVFIRST or DEVLAST | Move to the First or Last Device on the selected Track. | DEVFIRST, DEVLAST
| DEVLEFT or DEVRIGHT | Move Left or Right between Devices on the selected Track.  | DEVLEFT, DEVRIGHT
| DUMMY T| his Action does nothing. This is intended for use with PSEQ Action Lists and LSEQ and DEFAULT WITH STOP X-Clips. | -
| DUPESCENE | When accessed via an X-Clip, Duplicate the Scene the X-Clip is on. Otherwise, Duplicate the selected Scene. | -
| DUPESCENE x | x is the Scene number to Duplicate. Specify SEL for the selected Scene. | DUPESCENE 10, DUPESCENE 3, DUPESCENE SEL
| FOCBRWSR | Move the Focus to the Browser and show the Browser if it isn’t visible. | -
| FOCDETAIL | Move the Focus to Detail View and show Detail View if it isn’t visible. | -
| FOCMAIN | Move the Focus to the Main Focus. | -
| GQ | Toggle Global Quantization value between None and the last value. | -
| GQ x | x is the Global Quantization value to set. | GQ NONE, GQ 8 BARS, GQ 4 BARS, GQ 2 BARS, GQ 1 BAR, GQ 1/2, GQ 1/2T, GQ 1/4, GQ 1/4T, GQ 1/8, GQ 1/8T, GQ 1/16, GQ 1/16T, GQ 1/32
| GQ < or > | Select the Prev/Next Global Quantization value. | GQ <, GQ >
| GRV x | x is the Global Groove amount to set. | GRV 50, GRV 0
| GRV < or > | Dec/Inc Global Groove amount by increment of 1. | GRV <, GRV >
| GRV <x or >x | Dec/Inc Global Groove amount by increment of x. | GRV <2, GRV >10
| HZOOM x or VZOOM x | Horizontally or vertically zoom in on the selected Track in Arrangement View where x is the number of times to zoom. Positive numbers zoom in, negative numbers zoom out. For vertical zooming, you can also include the word ALL, which will cause all Tracks to be vertically zoomed. | HZOOM 1, HZOOM -50, VZOOM 50, VZOOM -1, VZOOM ALL-50 
| INSAUDIO or INSMIDI | Inserts an Audio or MIDI Track to the right of the selected Track that will be armed and routed from the selected Track. This will not perform an insertion if the selected Track is not the correct type. For example, if the selected Track doesn't have Audio output, INSAUDIO will do nothing. | INSAUDIO, INSMIDI
| LEFT or RIGHT or UP or DOWN | Move Left or Right or Up or Down in Session or Arrangement View. | LEFT, RIGHT, UP, DOWN 
 
