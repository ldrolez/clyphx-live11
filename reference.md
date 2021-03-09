## Global Actions

The MIDI Actions send MIDI messages to the MIDI port selected as the Output port for the ClyphX control surface. Also, all values in MIDI Actions
should be entered in decimal.

The SCENE related Actions do not actually Launch Scenes, they Launch every Clip on a Scene. For this reason, they will function similar to Launching
Scenes when Start Recording on Scene Launch is turned on.

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
 
## Track actions

| Action | Description | Examples 
| --- | --- | --- 
| ADDCLIP | Creates a 1 Bar MIDI Clip in the selected Clip Slot on the Track. | -
| ADDCLIP x | x is the Scene number of the Clip Slot where a 1 Bar MIDI Clip will be created. Specify SEL for the selected Scene. | ADDCLIP 10, ADDCLIP 3, ADDCLIP SEL
| ADDCLIP x y | x is the Scene number of the Clip Slot where a MIDI Clip will be created that is y Bars long. Specify SEL for the selected Scene. | ADDCLIP 10 4, ADDCLIP 3 8, ADDCLIP SEL 0.25
| ARM | Toggle, turn on or turn off Track Arm. | ARM, ARM ON, ARM OFF
| CUE | Adjust Preview Volume (Master Track only). This is a Continuous Parameter. | MST/CUE <, MST/CUE >, MST/CUE RESET, MST/CUE RND, MST/CUE 50, MST/CUE 100
| DEL | Deletes the Track. It is not possible to Delete a Track if it’s the only Track in the Set. Returns and the Master cannot be Deleted. | -
| DELDEV x | x is the number of the Device (based on the Device’s position on the Track) to Delete. Only top-level Devices (Devices that aren’t inside of Racks) can be Deleted. | DELDEV 1, DELDEV 5
| DUPE | Duplicates the Track. Returns and the Master cannot be Duplicated. | -
| FOLD | Toggle, turn on or turn off Track Fold. | FOLD, FOLD ON, FOLD OFF
| IN x | Select a Track Input Routing. x is the name of the Track Input Routing selection. | IN COMPUTER KEYBOARD
| IN < or > | Select the Prev/Next Track Input Routing selection. | IN <, IN >
| INSUB x | Select a Track Input sub-routing. x is the name of the Track Input Sub-Routing selection. | INSUB CH. 1
| INSUB < or > | Select the Prev/Next Track Input Sub-Routing selection. | INSUB <, INSUB >
| JUMP x | x is the number of beats to jump the Playback Position of the playing Clip on the Track Backward/Forward by. | JUMP 1, JUMP -5, JUMP 7
| MON or MON x | Toggle Track Monitoring state or set a particular state where x is the state to set. | MON, MON IN, MON AUTO, MON OFF
| MUTE | Toggle, turn on or turn off Track Mute. | MUTE, MUTE ON, MUTE OFF
| NAME x | x is the new name for the Track. The new name will be capitalized. | NAME BKG VOCALS
| OUT x | Select a Track Ouput Routing. x is the name of the Track Output Routing selection. | OUT TO MT PLAYER 1
| OUT < or > | Select the Prev/Next Track Output Routing selection. | OUT <, OUT >
| OUTSUB x | Select a Track Ouput sub-routing. x is the name of the Track Output Sub-Routing selection. | OUTSUB CH. 10
| OUTSUB < or > | Select the Prev/Next Track Output Sub-Routing selection. | OUTSUB <, OUTSUB >
| PAN x | Adjust Track Pan. This is a Continuous Parameter. | PAN <, PAN >, PAN RESET, PAN RND, PAN 50, PAN 100
| PLAY | When accessed via an X-Clip, Launch the Clip Slot on the same Scene as the X-Clip. Otherwise, re-Launch the playing Clip Slot or Launch the Clip Slot at the selected Scene. | -
| PLAY x | x is the Scene number of the Clip Slot to Launch. Specify SEL for the selected Scene. You can alternatively specify the name of the Clip enclosed in quotes. | PLAY 10, PLAY 3, PLAY SEL, PLAY “My Clip”
| PLAY RND | Launch a Clip Slot at a randomly selected Scene. | -
| PLAY RNDx-y | Launch a Clip Slot at a randomly selected Scene in the range of x-y (where both x and y are in the range of 1 – the number of Scenes in the Set). | PLAY RND5-10, PLAY RND96-142 
| PLAY < or > | Launch the Prev/Next Clip Slot relative to the playing Clip. This will not launch empty slots and does not apply to Group Tracks. | PLAY <, PLAY >
| PLAY <x or >x | Launch the Clip Slot that is x-Scenes prior to or after the playing Clip. This does not apply to Group Tracks. | PLAY <5, PLAY >3
| PLAYL | Launch a Clip with Legato using the current Global Quantization value. | PLAYL “My Clip”, PLAYL RND, PLAYL >
| PLAYQ | Launch a Clip at a specific quantization (regardless of the current Global Quantization value or the Clip’s Launch Quantization). The quantization values that can be used are the same as those mentioned for the GQ Action. | PLAYQ NONE “My Clip”, PLAYQ 1 BAR RND, PLAYQ 1/4 >
| PLAYLQ | This is a combination of the previous two variations |  -
| RENAMEALL | Rename all the Clips on the Track based on the Track’s name. | -
| RENAMEALL x | Rename all the Clips on the Track where x is the base name to use. | RENAMEALL DRUMS
| SEL | Select the Track and highlight the playing Clip or the Clip at the selected Scene. | -
| SEL x | Select the Track and a particular Slot where x is the Scene number of the Slot. | SEL 10, SEL 3
| SEND ltr x | ltr is the letter of the Track Send to adjust. This is a Continuous Parameter. | SEND A <, SEND A >, SEND A RESET, SEND A RND, SEND A 50, SEND A 100
| SNAP | Store/recall snapshot of Track and Device settings. See Snap Action for more info on this. | SNAP, SNAP DEV, SNAP MIX, SNAP MIX+, SNAP PLAY
| SOLO | Toggle, turn on or turn off Track Solo. | SOLO, SOLO ON, SOLO OFF
| STOP | Stop the playing Clip on the Track. | -
| STOP NQ | Stop the playing Clip on the Track immediately (not quantized). | -
| VOL x | Adjust Track Volume. This is a Continuous Parameter. | VOL <, VOL >, VOL RESET, VOL RND, VOL 50, VOL 100
| XFADE or XFADE x | Toggle Track Crossfade assignment or set a particular state where x is the state to set. | XFADE, XFADE A, XFADE B, XFADE OFF
| XFADER x | Adjust Master Crossfader (Master Track only). This is a continuous parameter. | MST/XFADER <, MST/XFADER >, MST/XFADER RESET, MST/XFADER RND, MST/XFADER 50, MST/XFADER 100
 
## Track actions for Devices

Device actions are track-based and will apply to the device selected on the track, or on the 1st device. If you want to operate on a different Device, add a number after DEV: DEV3 RESET, will reset the 3rd device and, 2/DEV3 RND, will randomize the 3rd device on track 2.

A device name can also be specified with quotes (i.e. DEV"Auto Filter" RND).

| Action | Description | Examples 
| --- | --- | --- 
| DEV | Toggle, turn on or turn off Device On/Off switch. | DEV, DEV ON, DEV OFF
| DEV CHAINc MUTE | Toggle, turn on or turn off Chain Mute where c is the number of the Chain. | DEV CHAIN2 MUTE, DEV CHAIN4 MUTE ON, DEV CHAIN1 MUTE OFF
| DEV CHAINc PAN x | Adjust Chain Pan where c is the number of the Chain. This is a Continuous Parameter. | DEV CHAIN2 PAN <, DEV CHAIN4 PAN >, DEV CHAIN6 PAN RESET, DEV CHAIN2 PAN RND, DEV CHAIN25 PAN 50
| DEV CHAINc SOLO | Toggle, turn on or turn off Chain Solo where c is the number of the Chain. | DEV CHAIN2 SOLO, DEV CHAIN4 SOLO ON, DEV CHAIN1 SOLO OFF
| DEV CHAINc VOL x | Adjust Chain Volume where c is the number of the Chain. This is a Continuous Parameter. | DEV CHAIN2 VOL <, DEV CHAIN4 VOL >, DEV CHAIN6 VOL RESET, DEV CHAIN2 VOL RND, DEV CHAIN25 VOL 50
| DEV CS x | Adjust Device Chain Selector value. This is a Continuous Parameter. | DEV CS <, DEV CS >, DEV CS RESET, DEV CS RND, DEV CS 50, DEV CS 100
| DEV CSEL x | x is the number of the Chain to select. | DEV CSEL 10, DEV CSEL 3
| DEV CSEL < or > | Navigate to the Prev/Next Chain. | DEV CSEL <, DEV CSEL >
| DEV Bn Pp x | Adjust Device Bank parameter 1 - 8 where n in the number of the bank and p in the number of the parameter within the bank to adjust. This is a Continuous Parameter. | DEV B1 P1 <, DEV B2 P1 >, DEV B3 P1 RESET, DEV B4 P1 RND, DEV B5 P1 50, DEV B6 P1 100
| DEV Pp x | Adjust Device Best-of-Bank parameter 1 - 8 where p in the number of the parameter (or macros in the case of rack) to adjust. This is a Continuous Parameter. | DEV P1 <, DEV P1 >, DEV P1 RESET, DEV P1 RND, DEV P1 50, DEV P1 100
| DEV RND | Randomize Device parameters. Will not affect Chain Selectors, on/off switches or multi-option controls | -
| DEV RESET | Reset Device parameters. Will not affect Chain Selectors, on/off switches or multi-option controls | -
| DEV SEL | Select the Device and bring the Track it is on into view. If the Device is nested in a Rack and is hidden, it cannot be selected. | -
| DEV SET This Action is only accessible to X-Clips and should not be combined with other Actions. This will capture the values of the 8 Macros in a Rack and add them to the X-Clip’s name, thus creating a Dev Set x Action. Once the Dev Set x Action has been created, you can then combine it with other Actions if you like. | -
| DEV SET x | x is a space-separated list of 8 Continuous Parameter values/keywords that will set the values of all 8 Macros in a Rack at once. | DEV SET 0 10 20 30 40 50 60 70, DEV SET 1 RND 3 > < 127 0 <5
| LOOPER | Toggle, turn on or turn off Looper’s On/Off switch. Works only on the 1st looper | LOOPER, LOOPER ON, LOOPER OFF
| LOOPER x | x is the Looper state to set. Works only on the 1st looper | LOOPER STOP, LOOPER REC, LOOPER PLAY, LOOPER OVER
| LOOPER REV | Toggle, turn on or turn off Looper’s Reverse switch. Works only on the 1st looper | LOOPER REV, LOOPER REV ON, LOOPER REV OFF
