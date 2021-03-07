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
| LOADDEV x | x is the name of the native Live device (as shown in the Browser) to load onto the selected Track. | LOADDEV AMP, LOADDEV AUTO FILTER, LOADDEV CHORUS 
| LOADM4L x | x the name of the M4L device (as shown in the Browser, but without the .amxd) to load onto the selected Track. Only M4L devices in the root of the main M4L folders can be loaded. | LOADM4L LFO, LOADM4L MAX CUTKILLER, LOADM4L ENVELOPE
| LOC x | x is the name of the Arrangement Locator to jump to. | LOC VERSE 1, LOC HOOK
| LOC < or > | Jump to the Prev/Next Arrangement Locator. | LOC <, LOC >
| LOCLOOP x | x is the name of the Arrangement Locator to jump to. Also, the arrangement Loop Start position will move to the position of this Locator. | LOCLOOP VERSE 1, LOCLOOP HOOK
| LOOP | Toggle, turn on or turn off Arrangement Loop. | LOOP, LOOP ON, LOOP OFF
| LOOP x | x is the Arrangement Loop Length to set in Bars. | LOOP 4, LOOP 16
| LOOP *x | x is the value to multiply the Arrangement Loop Length by. | LOOP *0.5, LOOP *2
| LOOP < or > | Move the Arrangement Loop Backward/Forward by its length. | LOOP <, LOOP >
| LOOP <x or >x | Move the Arrangement Loop Backward/Forward by x number of beats. | LOOP <4, LOOP >16
| LOOP RESET | Reset Arrangement Loop Start position to 1.1.1. | -
| METRO | Toggle, turn on or turn off Metronome. | METRO, METRO ON, METRO OFF
| MIDI x | x is the MIDI message (of any type/length) to send. | MIDI 144 0 127, MIDI 192 6, MIDI 240 1 2 3 4 247
| MIDI CC x y z | Send a MIDI Control Change message where x is the Channel (in the range of 1 – 16), y is the Control number (in the range of 0 – 127) and z is the Value (in the range of 0 – 127). | MIDI CC 1 0 127, MIDI CC 16 10 127
| MIDI NOTE x y z | Send a MIDI Note message where x is the Channel (in the range of 1 – 16), y is the Note number (in the range of 0 – 127) and z is the Velocity (in the range of 0 – 127). This will send a Note message with virtually no length. | MIDI NOTE 1 0 127, MIDI NOTE 16 10 127
| MIDI PC x y | Send a MIDI Program Change message where x is the Channel (in the range of 1 – 16) and y is the Value (in the range of 0 – 127). | MIDI PC 1 0, MIDI PC 16 10
| OVER | Toggle, turn on or turn off Overdub. | OVER, OVER ON, OVER OFF
| PIN | Toggle, turn on or turn off Punch In. | PIN, PIN ON, PIN OFF
| POUT | Toggle, turn on or turn off Punch Out. | POUT, POUT ON, POUT OFF
| PSEQ RESET | Reset all PSEQ Action Lists, so that they start back at their beginning. | -
| REC | Toggle, turn on or turn off Arrangement Record. | REC, REC ON, REC OFF
| REDO or UNDO | Redo or Undo. | REDO, UNDO
| RESTART | Restart Arrangement at Position 1.1.1. | -
| RQ | Toggle Record Quantization value between None and the last value. | -
| RQ x | x is the Record Quantization value to set. | RQ NONE, RQ 1/4, RQ 1/8, RQ 1/8T, RQ 1/8 + 1/8T, RQ 1/16, RQ 1/16T, RQ 1/16 + 1/16T, RQ 1/32
| RQ < or > | Select the Prev/Next Record Quantization value. | RQ <, RQ >
| RPT | Toggle Note Repeat on/off. | -
| RPT x | x is the Note Repeat rate to set. | RPT OFF, RPT 1/4, RPT 1/4T, RPT 1/8, RPT 1/8T, RPT 1/16, RPT 1/16T, RPT 1/32, RPT 1/32T
| RTRIG | Retrigger all Clips that are currently recording. | -
| SATM | Toggle, turn on or turn off Automation Arm. | SATM, SATM ON, SATM OFF
| SCENE | When accessed via an X-Clip, Launch the Scene the X-Clip is on. Otherwise, Launch the selected Scene. | -
| SCENE x | x is the Scene number of the Scene to Launch. Specify SEL for the selected Scene. You can alternatively specify the Scene’s name enclosed in quotes. | SCENE 10, SCENE 3, SCENE SEL, SCENE “My Scene”
| SCENE RND | Launch a randomly selected Scene. | -
| SCENE RNDx-y | Launch a randomly selected Scene in the range of x-y (where both x and y are in the range of 1 – the number of Scenes in the Set). | SCENE RND5-10, SCENE RND96-142
| SCENE < or > | Launch the Prev/Next Scene relative to the last launched Scene.| SCENE <, SCENE >
| SCENE <x or >x | Launch the Scene that is x-Scenes prior to or after the last launched Scene. | SCENE <5, SCENE >3
| SETCONT | Continue playback from the stop point. This is only useful when accessed from an X-Control. | -
| SETFOLD | Toggle, turn on or turn off Track Fold for all Tracks. SETFOLD, SETFOLD ON, SETFOLD OFF
| SETJUMP x | x is the number of beats to jump the Arrangement’s Playback Position Backward/Forward by. | JUMP 1, JUMP -5, JUMP 7
| SETLOC | Add a Locator at the current Arrangement position or, if a Locator already exists at the position, delete the Locator. | -
| SETSTOP | Stop playback. This will actually toggle playback state, so it can be used to start/stop playback when accessed from an X-Control. | - 
| SHOWCLIP | Show Clip View. | -
| SHOWDETAIL | Toggle between showing and hiding Detail View. | -
| SHOWDEV | Show Track View. | -
| SIG x/y | x is the Time Signature Numerator value and y is the Denominator value. | SIG 4/4, SIG 6/8, SIG 16/2
| SREC | Toggle, turn on or turn off Session Record. | SREC, SREC ON, SREC OFF
| SRECFIX x | Trigger fixed-length Session Record on all armed Tracks where x is the length to record in bars. | SRECFIX 4, SRECFIX 8, SRCFIX 0.5
| STOPALL | Stop all Clips. | -
| STOPALL NQ | Stop all Clips immediately (not quantized). | -
| SWAP | Open the Browser and activate hotswapping for the selected Device. | -
| SWAP x | x is the name of the preset (as shown in the Browser, but without the .adv or .adg) to hotswap into the selected native Live device. Only presets that exist in the Device’s folder (or sub-folders within its folder) can be swapped. | SWAP BASS ROUNDUP, SWAP SWIRL, SWAP KIT-CORE 606
| SWAP < or > | Swap to the Prev/Next preset (with wrapping) for the selected native Live device. Only presets that exist in the Device’s folder (or sub-folders within its folder) can be swapped. Also, the navigation here is done alphabetically (sub-folders will be entered into alphabetically as well), so it won’t necessarily line up with how you’d navigate in the Browser. | SWAP <, SWAP >
| SWING x | x is the Note Repeat (RPT) Swing amount (in the range of 0 – 100) to set. | SWING 50, SWING 0
| SWING < or > | Dec/Inc Note Repeat (RPT) Swing amount by increment of 1. | SWING <,SWING >
| SWING < x or > x | Dec/Inc Note Repeat (RPT) Swing amount by increment of x. | SWING <2, SWING >10
| TAPBPM | Tap tempo. | -
| TGLBRWSR | Toggle the Browser and move the Focus to it or the main Focus. | -
| TGLDETAIL | Toggle between Clip and Track View. | -
| TGLMAIN | Toggle between Session and Arrangement View. | -
| UNARM | Unarm all armable Tracks. | -
| UNMUTE | Unmute all Tracks. | -
| UNSOLO | Unsolo all Tracks. | -
 
The MIDI Actions send MIDI messages to the MIDI port selected as the Output port for the ClyphX control surface. Also, all values in MIDI Actions
should be entered in decimal.

The SCENE related Actions do not actually Launch Scenes, they Launch every Clip on a Scene. For this reason, they will function similar to Launching
Scenes when Start Recording on Scene Launch is turned on.
