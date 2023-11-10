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
| SRECFIX x | Trigger fixed-length Session Record on all armed Tracks where x is the length to record in bars. If you use this on a MIDI track, make sure that global quantization if OFF if x is less than 1 | SRECFIX 4, SRECFIX 8, SRCFIX 0.5
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
 
To operate on a different Track, specify the Track followed by a slash ( / ) before the Action name:
 * Specify the Track number `2/VOL >` 
 * or a return letter `A/VOL >`
 * or MST for Master `MST/VOL >` 
 * or SEL for the Selected Track `SEL/VOL`
 * or a track name enclosed in quotes `"My Track"/VOL >`
 * or use the `<` and `>` keywords to operate on Tracks prior to or after the Selected Track `</MUTE, >/PLAY, >4/VOL >`
 * or `x-x` for a range of tracks: `5-8/SEND A >` or `2-B/VOL RND` or `8-MST/PAN RESET` or `SEL-"My Track"/MUTE` or `>->4/PAN >` 
 * or to ALL for all tracks `ALL/PLAY`
 
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
| SNAP | Store/recall snapshot of Track and Device settings. See Snap Action below for more info | SNAP, SNAP DEV, SNAP MIX, SNAP MIX+, SNAP PLAY
| SOLO | Toggle, turn on or turn off Track Solo. | SOLO, SOLO ON, SOLO OFF
| STOP | Stop the playing Clip on the Track. | -
| STOP NQ | Stop the playing Clip on the Track immediately (not quantized). | -
| VOL x | Adjust Track Volume. This is a Continuous Parameter. | VOL <, VOL >, VOL RESET, VOL RND, VOL 50, VOL 100
| XFADE or XFADE x | Toggle Track Crossfade assignment or set a particular state where x is the state to set. | XFADE, XFADE A, XFADE B, XFADE OFF
| XFADER x | Adjust Master Crossfader (Master Track only). This is a continuous parameter. | MST/XFADER <, MST/XFADER >, MST/XFADER RESET, MST/XFADER RND, MST/XFADER 50, MST/XFADER 100
 
### Details for SNAP Actions
 
X-Clips, and only X-Clips, can store and recall Snapshots of Track and Device settings. The Snap Action is a Track-based Action, but differs from other Actions as it cannot be used in an Action List. Upon playing an X-Clip with a Snap Action, the related settings will be stored in the X-Clip’s name along with your identifier.

You can use modifiers to Snapshot multiple tracks, for example: 1-4/SNAP DEVALL MIX+
 
| Action | Description | Examples 
| --- | --- | --- 
| SNAP DEV | Store the settings of the first Device on the Track | -
| SNAP DEVx | Store the settings of the Device where x is the number of the Device | SNAP DEV2, SNAP DEV8
| SNAP DEVx-y | Store the settings of the Devices in the specified range where x is the Device number to start with and y is the Device number to end with. There should be no space before or after the hyphen. To operate on all Devices, specify ALL | SNAP DEV1-4, SNAP DEV2-5, SNAP DEVALL
| SNAP MIX | Store the Volume, Pan and Sends settings of the Track | -
| SNAP MIX+ | Store the Volume, Pan, Sends, Mute, Solo and Crossfade settings of the Track |  -
| SNAP MIX- | Store the Volume, Pan, Mute, Solo and Crossfade settings of the Track |  -
| SNAP MIXS | Store the Sends settings of the Track | -
| SNAP PLAY | Store the playing status of the Track. This does not apply to Group Tracks, Return Tracks or the Master Track. | -
 
### SNAP Tracks
 
By default, SNAP actions are recalled immediately. If you want a smooth transition between mix values, you can use a Snap Track.

How to create and use SNAP Tracks?

* Create a new MIDI Track and rename it to 'CLYPHX SNAP'
* In clips below, create your snap actions. For example, add a few clips '[] 2/SNAP MIX' to capture mix parameters of the 2nd track
* After capturing the parameters, click again on a clip and now the parameters will transition to the new saved state

To control the transition speed, rename the track to 'CLYPHX SNAPE [value]', where value can be:

* a number, in hundreds of milliseconds. Increase the value for slower transitions, 10 is one second.
* S plus beats number, S4 for example, to have a transition during 4 beats.

Each clip can also have different timing values. Just edit the '[]' part, and add 'SP:'. For example [ID SP:40] or
[ID SP:S8].


 
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
| DEV SET | This Action is only accessible to X-Clips and should not be combined with other Actions. This will capture the values of the 8 Macros in a Rack and add them to the X-Clip’s name, thus creating a Dev Set x Action. Once the Dev Set x Action has been created, you can then combine it with other Actions if you like. | -
| DEV SET x | x is a space-separated list of 8 Continuous Parameter values/keywords that will set the values of all 8 Macros in a Rack at once. | DEV SET 0 10 20 30 40 50 60 70, DEV SET 1 RND 3 > < 127 0 <5
| LOOPER | Toggle, turn on or turn off Looper’s On/Off switch. Works only on the 1st looper | LOOPER, LOOPER ON, LOOPER OFF
| LOOPER x | x is the Looper state to set. Works only on the 1st looper | LOOPER STOP, LOOPER REC, LOOPER PLAY, LOOPER OVER
| LOOPER REV | Toggle, turn on or turn off Looper’s Reverse switch. Works only on the 1st looper | LOOPER REV, LOOPER REV ON, LOOPER REV OFF

## Track actions for Drum racks

These actions will apply to the first drum rack on the track. 

DR PAD actions operate on the current selected drum rack pad. To operate on the 2nd visible Drum Rack Pad, add 2 after the PAD keyword: DR PAD2 MUTE

| Action | Description | Examples 
| --- | --- | --- 
| DR PAD MUTE | Toggle, turn on or turn off Drum Rack Pad Mute. | DR PAD MUTE, DR PAD MUTE ON, DR PAD MUTE OFF
| DR PAD PAN x | Adjust Drum Rack Pad Pan. This is a continuous parameter. | DR PAD PAN <, DR PAD PAN >, DR PAD PAN RESET, DR PAD PAN RND, DR PAD PAN 50, DR PAD PAN 100
| DR PAD SEL | Select the Drum Rack Pad. | -
| DR PAD SEND ltr x | ltr is the letter of the Drum Rack Pad Send to adjust. This is a continuous parameter. | DR PAD SEND A <, DR PAD SEND A >, DR PAD SEND A RESET, DR PAD SEND A RND, DR PAD SEND A 50, DR PAD SEND A 100
| DR PAD SOLO | Toggle, turn on or turn off Drum Rack Pad Solo. | DR PAD SOLO, DR PAD SOLO ON, DR PAD SOLO OFF
| DR PAD VOL x | Adjust Drum Rack Pad Volume. This is a Continuous Parameter. | DR PAD VOL <, DR PAD VOL >, DR PAD VOL RESET, DR PAD VOL RND, DR PAD VOL 50, DR PAD VOL 100
| DR SCOLL < or > | Scroll the Drum Rack Selector down or up by increment of 1. | DR SCROLL <, DR SCROLL >
| DR SCOLL <x or >x | Scroll the Drum Rack Selector down or up by increment of x. | DR SCROLL <4, DR SCROLL >8
| DR UNMUTE | Unmute all Drum Rack Pads. | -
| DR UNSOLO | Unsolo all Drum Rack Pads. | -

## Track actions for Clips

The actions will apply to the playing Clip or if no Clip is playing, to the selected slot on the track. To operate on a different Clip, specify the slot
number of the Clip after the word CLIP: 5/CLIP1 LOOP *2

To operate on the selected slot or the Clip selected in Arrangement View, specify SEL
(CLIPSEL WARP). You can also specify the Clip name enclosed in quotes (1/CLIP"MyClip" LOOP).

By default, the Clip Note Actions (CLIP NOTES) will apply to all the Notes in a MIDI Clip that fall
within the Loop Start/End markers (if Loop is on) or the Start/End markers (if Loop is off). To operate
just on a particular pitch (or a range of pitches), specify the name (or number) of the pitch (or range)
after the word NOTES. 

For example: CLIP NOTESC#3 REV, CLIP NOTESF4-F#5 VELO <<, CLIP NOTES60 NUDGE >

To operate on Notes that fall on a particular time position (or a range of time positions) in the Clip,
specify the position (or range) and use @ as a prefix. Positions should be specified in absolute beat time
(where 1/4 note is equal to 1.0). So, in 4/4, beat 1 would be 0.0, beat 2 would be 1.0, etc. For example: CLIP NOTES @1.0 GATE >, CLIP NOTES @0.5-1.5 SPLIT

You can specify both a pitch (or pitch range) and a position (or position range) to operate on. For example: CLIP NOTESC3-F3 @4.0 DEL

| Action | Description | Examples 
| --- | --- | --- 
| CLIP | Toggle, turn on or turn off the Clip’s Activator switch. | CLIP, CLIP ON, CLIP OFF
| CLIP CENT x | x is the Audio Clip detune value to set. | CLIP CENT -12, CLIP CENT 3
| CLIP CENT < or > | Dec/Inc Audio Clip detune value by increment of 1. | CLIP CENT <, CLIP CENT >
| CLIP CENT <x or >x | Dec/Inc Audio Clip detune value by increment of x. | CLIP CENT <5, CLIP CENT >7
| CLIP CHOP | Duplicates the Clip 8 times and sets evenly distributed start/loop start positions, starting from the Clip’s current Start/Loop Start. As with any duplication of a Clip, this will overwrite Clips that exist in the Clip Slots beneath the Clip that will be duplicated. | -
| CLIP CHOP x | Same as CLIP CHOP, but x is the number of times the Clip will be duplicated. | CHOP 4, CHOP 16, CHOP 32
| CLIP CUE x | x is the position of the cue in absolute beat time. This is different than the bar/beat/sixteenths position shown in Live’s Clip View. For example, position 1.1.1 is 0 in absolute beat time | CLIP CUE 2, CLIP CUE 5.25
| CLIP CUE < or > | Move the cue point Backward/Forward by increment of 1 beat | CLIP CUE <, CLIP CUE >
| CLIP CUE <x or >x | Move the cue point Backward/Forward by increment of x beats | CLIP CUE <0.5, CLIP CUE >2
| CLIP DEL | Deletes the Clip | -
| CLIP DUPE | Duplicates the Clip |  -
| CLIP END x | x is the Clip End to set in beats | CLIP END 4, CLIP END 16
| CLIP END < or > | Dec/Inc the Clip’s End by 1 beat |  CLIP END <, CLIP END >
| CLIP END <x or >x |  Dec/Inc the Clip’s End by increment of x beats | CLIP END <2, CLIP END >0.5
| CLIP ENVCLR | Clears all envelopes from the Clip | -
| CLIP ENVCAP | Creates envelopes in the Clip for the current settings of the associated track’s mixer and/or Devices | CLIP ENVCAP, CLIP ENVCAP DEV, CLIP ENVCAP MIX
| CLIP ENVCAP DEV | Capture the settings of the first Device on the Track | -
| CLIP ENVCAP DEVx | Capture the settings of the Device where x is the number of the Device | CLIP ENVCAP DEV2, CLIP ENVCAP DEV3
| CLIP ENVCAP DEVx-y | Capture the settings of the Devices in the specified range where x is the device number to start with and y is the Device number to end with. To operate on all Devices specify ALL. | CLIP ENVCAP DEV1-4, CLIP ENVCAP DEV2-5, CLIP ENVCAP DEVALL
| CLIP ENVCAP MIX | Capture the Volume, Pan and Sends settings of the Track | -
| CLIP ENVCAP MIX- | Capture the Volume and Pan settings of the Track | -
| CLIP ENVCAP MIXS | Capture the Sends settings of the Track | -
| CLIP ENVCLR x | x is the parameter associated with the envelope to clear from the clip | CLIP ENVCLR VOL, CLIP ENVCLR DEV2 B1 P6
| CLIP ENVHIDE | Hides the Clip’s envelope view. This actually applies to all Clips | -
| CLIP ENVINS x y |  x is the parameter to insert an envelope for in the Clip and y is the type of envelope to insert. This will first clear the parameter’s envelope if one exists. The types of envelopes are: IRAMP – Linear increasing ramp. DRAMP – Linear decreasing ramp. IPYR – Linear increase until midpoint and then linear decrease. DPYR – Linear decrease until midpoint and then linear increase. SAW – Saw wave synced to 1/4 notes. SQR – Square wave synced to 1/4 notes. If the Clip is looping, the envelope will start and end within the loop. Otherwise, the envelope will span the entire length of the Clip. Envelopes can only be inserted for parameters that are not quantized. Examples of quantized parameters are an on/off switch or a filter type chooser. | CLIP ENVINS PAN SAW, CLIP ENVINS DEV P5 IRAMP, CLIP ENVINS SEND A DPYR, CLIP ENVINS SEL SQR
| CLIP ENVINS x y a b | Same as above except that a is the minimum value and b is the max value of the envelope. These values are specified in terms of percentages (in the range of 0 – 100) of the parameter’s max value | CLIP ENVINS PAN SAW 50 75, CLIP ENVINS DEV P5 IRAMP 0 10, CLIP ENVINS SEND A DPYR 20 60, CLIP ENVINS SEL SQR 75 100
| CLIP ENVSHOW | Shows the Clip’s envelope view. This actually applies to all Clips | -
| CLIP ENVSHOW x | x is the parameter associated with the envelope to show in envelope view | CLIP ENVSHOW VOL, CLIP ENVSHOW DEV2 B1 P6, CLIP ENVSHOW SEL
| CLIP EXTEND | Doubles the Loop Length of the MIDI Clip and duplicates its content. If Loop is on, will zoom out to show the entire Loop. | -
| CLIP GAIN x | x is the Audio Clip Gain to set in the range of 0 – 127 | CLIP GAIN 0, CLIP GAIN 64,
| CLIP GAIN < or > | Dec/Inc Audio Clip Gain by increment of 1. | CLIP GAIN <, CLIP GAIN >
| CLIP GAIN <x or >x | Dec/Inc Audio Clip Gain by increment of x | CLIP GAIN <5, CLIP GAIN >2
| CLIP GRID x | x is the fixed grid setting to apply to the Clip. | CLIP GRID OFF, CLIP GRID 8 BARS, CLIP GRID 4 BARS, CLIP GRID 2 BARS, CLIP GRID 1 BAR, CLIP GRID 1/2, CLIP GRID 1/4, CLIP GRID 1/8, CLIP GRID 1/16, CLIP GRID 1/32
| CLIP LOOP | Toggle, turn on or turn off Clip Loop | CLIP LOOP, CLIP LOOP ON, CLIP LOOP OFF
| CLIP LOOP x | x is the Loop Length to set in Bars. If the Clip is playing, this will move the start of the Loop to the current Playback Position (using Beat quantization). To use Bar quantization, add a ‘B’ after the Length | CLIP LOOP 0.25, CLIP LOOP 0.5, CLIP LOOP 2, CLIP LOOP 0.5B, CLIP LOOP 2B
| CLIP LOOP *x | x is the value to multiply the Loop Length by | CLIP LOOP *0.5, CLIP LOOP *2
| CLIP LOOP < or > | Move the Clip Loop Backward/Forward by its length | CLIP LOOP <, CLIP LOOP >
| CLIP LOOP <x or >x | Move the Clip Loop Backward/Forward by x number of beats | CLIP LOOP <4, CLIP LOOP >16
| CLIP LOOP END x | x is the Clip Loop End (End if Loop is off) to set in beats | CLIP LOOP END 4, CLIP LOOP END 16
| CLIP LOOP END < or > | Dec/Inc the Clip Loop End (End if Loop is off) by 1 beat | CLIP LOOP END <, CLIP LOOP END >
| CLIP LOOP END <x or >x | Dec/Inc the Clip Loop End (End if Loop is off) by increment of x | CLIP LOOP END <2, CLIP LOOP END >0.5
| CLIP LOOP RESET | Reset Clip Loop Start to 1.1.1 and Clip Loop End to Clip End Marker |  -
| CLIP LOOP SHOW | Zoom in or out to show the Clip’s entire Loop. This will do nothing if the Clip isn’t visible or its Loop is off. | -
| CLIP LOOP START x | x is the Clip Loop Start (Start if Loop is off) to set in beats |  CLIP LOOP START 4, CLIP LOOP START 8
| CLIP LOOP START < or > | Dec/Inc the Clip Loop Start (Start if Loop is off) by 1 beat | CLIP LOOP START <, CLIP LOOP START >
| CLIP LOOP START <x or >x | Dec/Inc the Clip Loop Start (Start if Loop is off) by increment of x | CLIP LOOP START <2, CLIP LOOP START >0.5
| CLIP NAME x | x is the new name for the Clip. The new name will be capitalized| CLIP NAME DRUMS
| CLIP NOTES | Toggle, turn on or turn off the mute status of Notes | CLIP NOTES, CLIP NOTES ON, CLIP NOTES OFF
| CLIP NOTES CMB | Combine each set of two consecutive Notes into a single Note | -
| CLIP NOTES COMP | Compress the duration of Notes | -
| CLIP NOTES DEL | Delete Notes |  -
| CLIP NOTES EXP | Expand the duration of Notes |  -
| CLIP NOTES GATE < or > | Dec/Inc the length of Notes by one 128th note |  CLIP NOTES GATE <, CLIP NOTES GATE >
| CLIP NOTES GATE <x or >x | Dec/Inc the length of Notes by x 128th notes |  CLIP NOTES GATE <4, CLIP NOTES GATE >8
| CLIP NOTES INV | Invert the pitches of Notes |  -
| CLIP NOTES NUDGE < or > | Nudge Notes Backward/Forward by one 128th note |  CLIP NOTES NUDGE <, CLIP NOTES NUDGE >
| CLIP NOTES NUDGE <x or >x | Nudge Notes Backward/Forward by x 128th notes |  CLIP NOTES NUDGE <4, CLIP NOTES NUDGE >8
| CLIP NOTES REV | Reverse the position of Notes|  -
| CLIP NOTES SCRN | Scramble the pitches of Notes while maintaining rhythm | -
| CLIP NOTES SCRP | Scramble the position of Notes while maintaining pitches |  -
| CLIP NOTES SPLIT | Split each Note into two equally sized Notes |  -
| CLIP NOTES VELO x | x is the Note velocity to set |  CLIP NOTES VELO 64, CLIP NOTES VELO 127
| CLIP NOTES VELO < or > | Dec/Inc the velocity of Notes by increment of 1 |  CLIP NOTES VELO <, CLIP NOTES VELO >
| CLIP NOTES VELO <x or >x | Dec/Inc the velocity of Notes by increment of x |  CLIP NOTES VELO <5, CLIP NOTES VELO >10,
| CLIP NOTES VELO << or CLIP NOTES VELO >> | Apply a decrescendo (descending velocities) or a crescendo (ascending velocities) to Notes. | CLIP NOTES VELO <<, CLIP NOTES VELO >>
| CLIP NOTES VELO RND | Randomize the velocity of Notes | -
| CLIP QNTZ x | x is the value to Quantize the Clip’s Notes or Warp markers to | CLIP QNTZ 1/4, CLIP QNTZ 1/8, CLIP QNTZ 1/8T, CLIP QNTZ 1/8 + 1/8T, CLIP QNTZ 1/16, CLIP QNTZ 1/16T, CLIP QNTZ 1/16 + 1/16T, CLIP QNTZ 1/32
| CLIP QNTZ x y | Same as CLIP QNTZ X, but y is the Strength of quantization (in the range of 0 - 100) to apply | CLIP QNTZ 1/16 50, CLIP QNTZ 1/8 25
| CLIP QNTZ x y z | Same as CLIP QNTZ X Y, but z is the amount of Swing (in the range of 0 - 100) to apply. | CLIP QNTZ 1/16 100 50, CLIP QNTZ 1/16 50 25
| CLIP QNTZ n x CLIP QNTZ n x y CLIP QNTZ n x y z | Same as the CLIP QNTZ Actions listed above, but n is the pitch name or Pitch Range to Quantize | CLIP QNTZ C3 1/8, CLIP QNTZ D#4-C5 1/32 50, CLIP QNTZ E1 1/16 50 25
| CLIP SEMI x | x is the Audio Clip Transpose value to set |  CLIP SEMI -12, CLIP SEMI 5
| CLIP SEMI < or > | Dec/Inc Audio Clip Transpose value or Notes pitch by 1 semitone | CLIP SEMI <, CLIP SEMI >
| CLIP SEMI <x or >x | Dec/Inc Audio Clip Transpose value or Notes pitch by x semitones | CLIP SEMI <5, CLIP SEMI >10
| CLIP SIG x/y | x is the Time Signature Numerator value and y is the Time Signature denominator value | CLIP SIG 4/4, CLIP SIG 6/8, CLIP SIG 16/2
| CLIP SPLIT x | x is the length of the segments (in beats) to split a Clip into. This will duplicate the Clip and set each segment to be the specified length. As with any duplication of a Clip, this will overwrite Clips that exist in the Clip Slots beneath the Clip that will be duplicated. | CLIP SPLIT 1, CLIP SPLIT 0.25, CLIP SPLIT 4
| CLIP START x | x is the Clip Start to set in beats | CLIP START 4, CLIP START 16
| CLIP START < or > | Dec/Inc the Clip’s Start by 1 beat | CLIP START <, CLIP START >
| CLIP START <x or >x | Dec/Inc the Clip’s Start by increment of x | CLIP START <2, CLIP START >0.5
| CLIP TGRID | Toggle, turn on or turn off the Clip’s triplet grid setting | CLIP TGRID, CLIP TGRID ON, CLIP TGRID OFF
| CLIP WARP | Toggle, turn on or turn off the Clip’s Warp switch | CLIP WARP, CLIP WARP ON, CLIP WARP OFF
| CLIP WARPMODE x | x is the name of the Warp Mode (as shown in the Warp Mode menu) to set. This cannot be applied if the Warp Mode is currently REX. | CLIP WARPMODE BEATS, CLIP WARPMODE COMPLEX
| CLIP WARPMODE < or > | Move to the Prev/Next Warp Mode. This cannot be applied if the Warp Mode is currently REX. | CLIP WARPMODE <, CLIP WARPMODE >

## Control surface actions

Control Surface Actions relate to other Control Surface scripts that are selected in Live’s Control Surface section, in Preferences – MIDI/Sync.
In the actions below N is the number of the Control Surface to operate on, in the range of 1 to 6. This numbering is based on the number of Control Surface scripts that are selected. For example, if only two scripts are selected, the second script will be CS2 even if the script is selected in Control Surface slot #6.
You can alternatively specify the one-word name of the Control Surface to operate on enclosed in quotes (such as CS”APC20” RING T1), with spaces replaced by underscores. 

| Action | Description | Examples 
| --- | --- | --- 
| CSN x/ACTION NAME | Apply a Track, Device, Drum Rack, Clip or Clip Cue Action to channel strip number x | CS1 2/MUTE, CS"APC40" 3/DEV RND, CS3 7/CLIP SEMI >
| CSN x-y/ACTION NAME | Apply a Track, Device, Drum Rack, Clip or Clip Cue Action to channel strip numbers x-y. There should be no space before or after the hyphen. To operate on all Channel Strips, specify ALL | CS1 1-3/FOLD, CS"Push" 3-8/DEV, CS2 ALL/CLIP START >
| CSN BANK x | Move the surface track bank selection forward or backward by x and select the first Track in the new Bank selection. Use 'First' or 'Last' to select the First/Last Track Bank. This works even with Surfaces without Track Banks, like User Remote Scripts for example. | CS1 BANK 1, CS"MPD32" BANK -1, CS2 BANK 8, CS2 FIRST, CS2 BANK LAST
| CSN COLORS x y z | Change the color of the Clip Launch LEDs where x is the color to use for playing clips, y is the color to use for recording Clips and z is the color to use for stopped Clips. The available colors are: Amber, Green and Red. Only applies to the APC40, APC20 and Launchpad | CS1 COLORS RED AMBER GREEN, CS"APC20" COLORS GREEN RED AMBER
| CSN DEV LOCK | Toggle the surface’s lock on Devices. This requires that the surface has Device Controls. | CS2 DEV LOCK
| CSN METRO ON or CSN METRO OFF | Cause the APC's Clip Stop buttons or the Launchpad’s RightSide buttons (in every mode except for User 1) to display a visual metronome. The buttons will still function as usual. Only applies to the APC40, APC20 and Launchpad | CS2 METRO ON, CS"Launchpad" METRO OFF
| CSN RING Tx Sy | x is the name or number of the first track outlined by the ring, y is the name of number of the first Scene outlined by the ring. Only one of these has to be specified so that you can change the scene offset without changing the track offset and vice versa. Only on surfaces which have a grid selector | CS1 RING T1 S20, CS"APC40" RING S"My Scene", CS4 RING T5, CS"Push" RING T"The Track" S100
| CSN RING T< or > S< or > | Move the ring Backward/Forward by increment of 1 track and/or 1 scene. Only of these has to be specified so that you can increment Tracks without incrementing Scenes and vice versa. | CS"APC40" RING T> S<, CS3 RING T<, CS1 RING T>, CS4 RING S<, CS4 RING S>
| CSN RING T<x or >x S<x or >x | Move the ring Backward/Forward by increment of x Tracks and/or x Scenes. Only of these has to be specified so that you can increment Tracks without incrementing Scenes and vice versa. | CS"APC40" RING T>4 S<8, CS1 RING T<2, CS1 RING T>10, CS4 RING S<20, CS4 RING S>5
| CSN RING LAST | Moves the ring back to the position it was at prior to triggering one of the Ring Actions described above. | CS"APC40" RING LAST, CS1 RING LAST
| CSN RINGLINK T S | Causes the Surface's ring to be linked to the selected Track and/or Scene. Only of these has to be specified so that you can link to Tracks without linking to Scenes and vice versa. You can also specify CENTER, which will cause the ring to be centered around the selected Track and/or Scene. | CS"APC20" RINGLINK T S, CS2 RINGLINK T CENTER, CS"Push" RINGLINK S
| CSN RINGLINK OFF | Turns the Surface's ring linking off. | CS"APC20" RINGLINK OFF, CS2 RINGLINK OFF
| CSN RPT | Toggle Note Repeat on/off | CS2 RPT, CS"MPD32" RPT
| CSN RPT x | x is the note repeat rate to set | CS1 RPT OFF, CS1 RPT 1/4, CS1 RPT 1/4T, CS1 RPT 1/8, CS1 RPT 1/8T, CS1 RPT 1/16, CS1 RPT 1/16T, CS1 RPT 1/32, CS1 RPT 1/32T

## PUSH Actions

Applies to PUSH and PUSH 2 control surfaces, and they should be enabled in your Live preferences.

| Action | Description | Examples 
| --- | --- | --- 
| PUSH DRINS | Cause Push to enter the standard Note Mode. This allows you to use Note Mode to control a Drum Rack. This will have no effect if the selected Track is not a MIDI Track. | -
| PUSH MODE x | x is the Push mode to select. For the most part, these work in the same way they would work when pressing buttons on Push. | PUSH MODE SESSION, PUSH MODE NOTE, PUSH MODE STOP, PUSH MODE SOLO, PUSH MODE MUTE, PUSH MODE VOLUME, PUSH MODE PAN, PUSH MODE TRACK, PUSH MODE CLIP, PUSH MODE DEVICE, PUSH MODE MIX
| PUSH MSG | Temporarily shows a message in Push's display. | PUSH MSG TRIGGER VERSE IN 2 BARS
| PUSH SCL | This Action is only accessible to X-Clips and should not be combined with other Actions. This will capture the current scale settings from Note Mode and store them in the X-Clip. Once settings have been stored, you can then add other Actions if you like or copy the stored settings and paste them into the Action List of other X-Trigger types. | -
| PUSH SCL FIXED | Toggle, turn on or turn off the Push’s Fixed function | PUSH SCL FIXED, PUSH SCL FIXED ON, PUSH SCL FIXED OFF
| PUSH SCL INKEY | Toggle, turn on or turn off the Push’s In Key function | PUSH SCL INKEY, PUSH SCL INKEY ON, PUSH SCL INKEY OFF
| PUSH SCL OCT < or > | Move to the Prev/Next Octave offset in Note Mode | PUSH SCL OCT <, PUSH SCL OCT >
| PUSH SCL ROOT x | x is the Root Note to use in Note Mode | PUSH SCL ROOT D, PUSH SCL ROOT F#
| PUSH SCL ROOT < or > | Move to the Prev/Next Root Note to use in Note Mode | PUSH SCL ROOT <, PUSH SCL ROOT >
| PUSH SCL TYPE x | x is the name of the Scale Type as shown in Push’s display to use in Note Mode  | PUSH SCL TYPE MAJOR, PUSH SCL TYPE MINOR PENTATONIC
| PUSH SCL TYPE < or > | Move to the Prev/Next Scale Type to use in Note Mode | PUSH SCL TYPE <, PUSH SCL TYPE >
| PUSH SEQ x | x is the name of the Clip Notes Action to apply to the note lane currently being edited by Push’s Drum step-sequencer | PUSH SEQ VELO RND, PUSH SEQ CMB
 
 
