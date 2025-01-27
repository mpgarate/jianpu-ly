#!/usr/bin/env python
# (can be run with either Python 2 or Python 3)

r"""
# Jianpu (numbered musical notaion) for Lilypond
# v1.823 (c) 2012-2025 Silas S. Brown
# v1.826 (c) 2024 Unbored

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Homepage: http://ssb22.user.srcf.net/mwrhome/jianpu-ly.py
# Git repository: https://github.com/ssb22/jianpu-ly
# and on GitLab: https://gitlab.com/ssb22/jianpu-ly
# and on Bitbucket: https://bitbucket.org/ssb22/jianpu-ly
# and at https://gitlab.developers.cam.ac.uk/ssb22/jianpu-ly
# and in China: https://gitee.com/ssb22/jianpu-ly

# (The following docstring format is fixed, see --html)
Run jianpu-ly < text-file > ly-file (or jianpu-ly text-files > ly-file)
Text files are whitespace-separated and can contain:
Scale going up: 1 2 3 4 5 6 7 1'
Accidentals: 1 #1 2 b2 1
Octaves: 1,, 1, 1 1' 1''
Shortcuts for 1' and 2': 8 9
Percussion beat: x
Change base octave: < >
Semiquaver, quaver, crotchet (16/8/4th notes): s1 q1 1
Dotted versions of the above (50% longer): s1. q1. 1.
Demisemiquaver, hemidemisemiquaver (32/64th notes): d1 h1
Minims (half notes) use dashes: 1 -
Dotted minim: 1 - -
Semibreve (whole note): 1 - - -
Time signature: 4/4
Time signature with quaver anacrusis (8th-note pickup): 4/4,8
Key signature (major): 1=Bb
Key signature (minor): 6=F#
Tempo: 4=85
Lyrics: L: here are the syl- la- bles (all on one line)
Lyrics (verse 1): L: 1. Here is verse one
Lyrics (verse 2): L: 2. Here is verse two
Hanzi lyrics (auto space): H: hanzi (with or without spaces)
Lilypond headers: title=the title (on a line of its own)
Guitar chords: chords=c2. g:7 c (on own line)
Fret diagrams: frets=guitar (on own line)
Multiple parts: NextPart
Instrument of current part: instrument=Flute (on a line of its own)
Multiple movements: NextScore
Prohibit page breaks until end of this movement: OnePage
Suppress bar numbers: NoBarNums
Suppress first-line indent: NoIndent
Ragged last line: RaggedLast
Old-style time signature: SeparateTimesig 1=C 4/4
Indonesian 'not angka' style: angka
Add a Western staff doubling the tune: WithStaff
Tuplets: 3[ q1 q1 q1 ]
Grace notes before: g[#45] 1
Grace notes after: 1 ['1]g
Grace notes with durations: g[d4d5s6] 1
Simple chords: ,13'5 1 1b3 1 (chord numbers are sorted automatically)
Da capo: 1 1 Fine 1 1 1 1 1 1 DC
Repeat (with alternate endings): R{ 1 1 1 } A{ 2 | 3 }
Short repeats (percent): R4{ 1 2 }
Ties (like Lilypond's, if you don't want dashes): 1 ~ 1
Slurs (like Lilypond's): 1 ( 2 )
Erhu fingering (applies to previous note): Fr=0 Fr=4
Erhu symbol (applies to previous note): souyin harmonic up down bend tilde
Tremolo: 1/// - 1///5 -
Rehearsal letters: letterA letterB
Multibar rest: R*8
Dynamics (applies to previous note): \p \mp \f
Other 1-word Lilypond \ commands: \fermata \> \! \( \) etc
Text: ^"above note" _"below note"
Harmonic symbols above main notes: Harm: (music) :Harm (main music)
Other Lilypond code: LP: (block of code) :LP (each delimeter at start of its line)
Unicode approximation instead of Lilypond: Unicode
Ignored: % a comment
"""

import sys,os,re,shutil
from fractions import Fraction as F # requires Python 2.6+
if type(u"")==type(""): # Python 3
    unichr,xrange = chr,range
    from string import ascii_letters as letters
else: from string import letters # Python 2
def asUnicode(l):
    if type(l)==type(u""): return l
    return l.decode('utf-8')
try: from commands import getoutput
except: from subprocess import getoutput

def lilypond_minor_version():
    global _lilypond_minor_version
    try: return _lilypond_minor_version
    except: pass
    cmd = lilypond_command()
    if cmd:
        m=re.match(r".*ond-2\.([1-9][0-9])\.",cmd)
        if m: _lilypond_minor_version = int(m.group(1))
        else: _lilypond_minor_version = int(getoutput(cmd+" --version").split()[2].split('.')[1])
    else: _lilypond_minor_version = 22 # assume 2.22 if we can't figure it out
    return _lilypond_minor_version

def lilypond_command():
    if hasattr(shutil,'which'):
        w = shutil.which('lilypond')
        if w: return 'lilypond'
    elif not sys.platform.startswith("win"):
        cmd = getoutput('which lilypond 2>/dev/null')
        if os.path.exists(cmd): return 'lilypond'
        placesToTry = ['/Applications/LilyPond.app/Contents/Resources/bin/lilypond'] # e.g. from Mac OS 10.4-10.14 Intel build https://web.archive.org/web/20221121202056/https://lilypond.org/download/binaries/darwin-x86/lilypond-2.22.2-1.darwin-x86.tar.bz2 (unpacked and moved to /Applications), or similarly 2.20 for macOS 10.15+ from https://gitlab.com/marnen/lilypond-mac-builder/-/package_files/9872804/download
        placesToTry = ['/Applications/LilyPond-2.22.2.app/Contents/Resources/bin/lilypond','/Applications/LilyPond-2.20.0.app/Contents/Resources/bin/lilypond'] + placesToTry # if renamed from the above (try specific versions 1st, in case default is older)
        placesToTry += ['lilypond-2.24.0/bin/lilypond','/opt/lilypond-2.24.0/bin/lilypond'] # if unpacked 2.24 (which drops the .app; in macOS 13, might need first to manually open at least lilypond and gs binaries for Gatekeeper approval if installing it this way)
        for t in placesToTry:
            if os.path.exists(t): return t

staff_size = float(os.environ.get("j2ly_staff_size",20))
# Normal: j2ly_staff_size=20
# Large: j2ly_staff_size=25.2
# Small: j2ly_staff_size=17.82
# Tiny: j2ly_staff_size=15.87
lyric_size = float(os.environ.get("j2ly_lyric_size",staff_size))

three_dots = u"\u22EE"
if not type(u"")==type(""): three_dots = three_dots.encode('utf-8') # Python 2

def find_grace_height(music):
    # Need 3.5 if there's demisemiquavers with 2 octaves below.
    # Can have 2.5 if there aren't any of those
    # (Probably looks better if height is the same throughout the score,
    # so we scan ahead to find what the most complex thing is.
    # Could also change height every time, but would need to
    # check if high-quality published music does that.
    # Change every time would require differently parameterised versions of jianpu-grace-curve-stencil though.)
    global grace_height
    grace_height = 2.5
    for word in music.split():
        if word.startswith("g[") or word.endswith("]g"):
            if "d" in word or ",," in word:
                grace_height = 3.5 ; break
                # TODO: more options, e.g. 3.0 if "d" but not ",," ?  (will need to update grace_height dictionary in all_scores_start also)

def all_scores_start(inDat):
    if lilypond_minor_version() < 20: errExit("Lilypond 2.18 and below is no longer supported") # 2.20 is in Ubuntu 20.04 LTS and 2.22 can be installed on a 2011 Mac; if you're stuck on an older EOL'd distro without Internet, use jianpu-ly 1.825 or earlier
    r = r"""\version "2.%d.0"
#(set-global-staff-size %g)""" % ((
    22 if "g[" in inDat or "]g" in inDat else 20),staff_size)
    r += r"""

% un-comment the next line to remove Lilypond tagline:
% \header { tagline="" }

% comment out the next line if you're debugging jianpu-ly
% (but best leave it un-commented in production, since
% the point-and-click locations won't go to the user input)
\pointAndClickOff

\paper {
  print-all-headers = ##t %% allow per-score headers

  % un-comment the next line for A5:
  % #(set-default-paper-size "a5" )

  % un-comment the next line for no page numbers:
  % print-page-number = ##f

  % un-comment the next 3 lines for a binding edge:
  % two-sided = ##t
  % inner-margin = 20\mm
  % outer-margin = 10\mm

  % un-comment the next line for a more space-saving header layout:
  % scoreTitleMarkup = \markup { \center-column { \fill-line { \magnify #1.5 { \bold { \fromproperty #'header:dedication } } \magnify #1.5 { \bold { \fromproperty #'header:title } } \fromproperty #'header:composer } \fill-line { \fromproperty #'header:instrument \fromproperty #'header:subtitle \smaller{\fromproperty #'header:subsubtitle } } } }
"""
    if os.path.exists("/Library/Fonts/Arial Unicode.ttf"): r += r"""
  % As jianpu-ly was run on a Mac, we include a Mac fonts workaround.
  % The Mac version of Lilypond 2.18 used Arial Unicode MS as a
  % fallback even in the Serif font, but 2.20 drops this in Serif
  % (using it only in Sans), which means any Serif text (titles,
  % lyrics etc) that includes Chinese will likely fall back to
  % Japanese fonts which don't support all Simplified hanzi.
  % This brings back 2.18's behaviour on 2.20+:
  #(define fonts
    (set-global-fonts
     #:roman "Source Serif Pro,Source Han Serif SC,Times New Roman,Arial Unicode MS"
     #:factor (/ staff-height pt 20)
    ))
"""
    if has_lyrics: r += r"""
  % Might need to enforce a minimum spacing between systems, especially if lyrics are below the last staff in a system and numbers are on the top of the next
  system-system-spacing = #'((basic-distance . 7) (padding . 5) (stretchability . 1e7))
  score-markup-spacing = #'((basic-distance . 9) (padding . 5) (stretchability . 1e7))
  score-system-spacing = #'((basic-distance . 9) (padding . 5) (stretchability . 1e7))
  markup-system-spacing = #'((basic-distance . 2) (padding . 2) (stretchability . 0))
"""
    r += "}\n" # end of \paper block

    r += r"""
%% 2-dot and 3-dot articulations
#(append! default-script-alist
   (list
    `(two-dots
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,#{ \markup \override #'(font-encoding . latin1) \center-align \bold ":" #})
           (padding . 0.20)
           (avoid-slur . inside)
           (direction . ,UP)))))
#(append! default-script-alist
   (list
    `(three-dots
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,#{ \markup \override #'(font-encoding . latin1) \center-align \bold """+'"'+three_dots+'"'+r""" #})
           (padding . 0.30)
           (avoid-slur . inside)
           (direction . ,UP)))))
"two-dots" =
#(make-articulation 'two-dots)

"three-dots" =
#(make-articulation 'three-dots)

\layout {
  \context {
    \Score
    scriptDefinitions = #default-script-alist
  }
}

note-mod =
#(define-music-function
     (text note)
     (markup? ly:music?)
   #{
     \tweak NoteHead.stencil #ly:text-interface::print
     \tweak NoteHead.text
        \markup \lower #0.5 \sans \bold #text
     \tweak Rest.stencil #ly:text-interface::print
     \tweak Rest.text
        \markup \lower #0.5 \sans \bold #text
     #note
   #})"""
    if re.search(r"(\s|^)(angka|Indonesian)(\s|$)",inDat): r += r"""
note-mod-angka = #(define-music-function (text note) (markup? ly:music?)
   #{ \tweak NoteHead.stencil #ly:text-interface::print
     \tweak NoteHead.text \markup \lower #0.5 \bold #text
     \tweak Rest.stencil #ly:text-interface::print
     \tweak Rest.text \markup \lower #0.5 \bold #text
     #note #})
"""
    if inner_beams_below: r += r"""
#(define (flip-beams grob)
   (ly:grob-set-property!
    grob 'stencil
    (ly:stencil-translate
     (let* ((stl (ly:grob-property grob 'stencil))
            (centered-stl (ly:stencil-aligned-to stl Y DOWN)))
       (ly:stencil-translate-axis
        (ly:stencil-scale centered-stl 1 -1)
        (* (- (car (ly:stencil-extent stl Y)) (car (ly:stencil-extent centered-stl Y))) 0) Y))
     (cons 0 -0.8))))
"""
# Draw grace curve according to start and end mark.
# Modify from https://lists.gnu.org/archive/html/lilypond-user/2015-01/msg00142.html
    r += r"""
%%=======================================================
#(define-event-class 'jianpu-grace-curve-event 'span-event)

#(define (add-grob-definition grob-name grob-entry)
   (set! all-grob-descriptions
         (cons ((@@ (lily) completize-grob-entry)
                (cons grob-name grob-entry))
               all-grob-descriptions)))

#(define (jianpu-grace-curve-stencil grob)
   (let* ((elts (ly:grob-object grob 'elements))
          (refp-X (ly:grob-common-refpoint-of-array grob elts X))
          (X-ext (ly:relative-group-extent elts refp-X X))
          (refp-Y (ly:grob-common-refpoint-of-array grob elts Y))
          (Y-ext (ly:relative-group-extent elts refp-Y Y))
          (direction (ly:grob-property grob 'direction RIGHT))
          (x-start (* 0.5 (+ (car X-ext) (cdr X-ext))))
          (y-start (+ (car Y-ext) %g))
          (x-start2 (if (eq? direction RIGHT)(+ x-start 0.5)(- x-start 0.5)))
          (x-end (if (eq? direction RIGHT)(+ (cdr X-ext) 0.2)(- (car X-ext) 0.2)))
          (y-end (- y-start 0.5))
          (stil (ly:make-stencil `(path 0.1
                                        (moveto ,x-start ,y-start
                                         curveto ,x-start ,y-end ,x-start ,y-end ,x-start2 ,y-end
                                         lineto ,x-end ,y-end))
                                  X-ext
                                  Y-ext))
          (offset (ly:grob-relative-coordinate grob refp-X X)))
     (ly:stencil-translate-axis stil (- offset) X)))

#(add-grob-definition
  'JianpuGraceCurve
  `(
     (stencil . ,jianpu-grace-curve-stencil)
     (meta . ((class . Spanner)
              (interfaces . ())))))

#(define jianpu-grace-curve-types
   '(
      (JianpuGraceCurveEvent
       . ((description . "Used to signal where curve encompassing music start and stop.")
          (types . (general-music jianpu-grace-curve-event span-event event))
          ))
      ))

#(set!
  jianpu-grace-curve-types
  (map (lambda (x)
         (set-object-property! (car x)
           'music-description
           (cdr (assq 'description (cdr x))))
         (let ((lst (cdr x)))
           (set! lst (assoc-set! lst 'name (car x)))
           (set! lst (assq-remove! lst 'description))
           (hashq-set! music-name-to-property-table (car x) lst)
           (cons (car x) lst)))
    jianpu-grace-curve-types))

#(set! music-descriptions
       (append jianpu-grace-curve-types music-descriptions))

#(set! music-descriptions
       (sort music-descriptions alist<?))


#(define (add-bound-item spanner item)
   (if (null? (ly:spanner-bound spanner LEFT))
       (ly:spanner-set-bound! spanner LEFT item)
       (ly:spanner-set-bound! spanner RIGHT item)))

jianpuGraceCurveEngraver =
#(lambda (context)
   (let ((span '())
         (finished '())
         (current-event '())
         (event-start '())
         (event-stop '()))
     `(
       (listeners
        (jianpu-grace-curve-event .
          ,(lambda (engraver event)
             (if (= START (ly:event-property event 'span-direction))
                 (set! event-start event)
                 (set! event-stop event)))))

       (acknowledgers
        (note-column-interface .
          ,(lambda (engraver grob source-engraver)
             (if (ly:spanner? span)
                 (begin
                  (ly:pointer-group-interface::add-grob span 'elements grob)
                  (add-bound-item span grob)))
             (if (ly:spanner? finished)
                 (begin
                  (ly:pointer-group-interface::add-grob finished 'elements grob)
                  (add-bound-item finished grob)))))
        (inline-accidental-interface .
          ,(lambda (engraver grob source-engraver)
             (if (ly:spanner? span)
                 (begin
                  (ly:pointer-group-interface::add-grob span 'elements grob)))
             (if (ly:spanner? finished)
                 (ly:pointer-group-interface::add-grob finished 'elements grob))))
        (script-interface .
          ,(lambda (engraver grob source-engraver)
             (if (ly:spanner? span)
                 (begin
                  (ly:pointer-group-interface::add-grob span 'elements grob)))
             (if (ly:spanner? finished)
                 (ly:pointer-group-interface::add-grob finished 'elements grob)))))
       
       (process-music .
         ,(lambda (trans)
            (if (ly:stream-event? event-stop)
                (if (null? span)
                    (ly:warning "No start to this curve.")
                    (begin
                     (set! finished span)
                     (ly:engraver-announce-end-grob trans finished event-start)
                     (set! span '())
                     (set! event-stop '()))))
            (if (ly:stream-event? event-start)
                (begin
                 (set! span (ly:engraver-make-grob trans 'JianpuGraceCurve event-start))
                 (set! event-start '())))))
       
       (stop-translation-timestep .
         ,(lambda (trans)
            (if (and (ly:spanner? span)
                     (null? (ly:spanner-bound span LEFT)))
                (ly:spanner-set-bound! span LEFT
                  (ly:context-property context 'currentMusicalColumn)))
            (if (ly:spanner? finished)
                (begin
                 (if (null? (ly:spanner-bound finished RIGHT))
                     (ly:spanner-set-bound! finished RIGHT
                       (ly:context-property context 'currentMusicalColumn)))
                 (set! finished '())
                 (set! event-start '())
                 (set! event-stop '())))))
       
       (finalize
        (lambda (trans)
          (if (ly:spanner? finished)
              (begin
               (if (null? (ly:spanner-bound finished RIGHT))
                   (set! (ly:spanner-bound finished RIGHT)
                         (ly:context-property context 'currentMusicalColumn)))
               (set! finished '())))))
       )))

jianpuGraceCurveStart =
#(make-span-event 'JianpuGraceCurveEvent START)

jianpuGraceCurveEnd =
#(make-span-event 'JianpuGraceCurveEvent STOP)
%%===========================================================
""" % {3.5: -0.2, 2.5: +0.32}[grace_height]
    return r+"\n%{ The jianpu-ly input was:\n" + inDat.strip().replace("%}","%/}")+"\n%}\n\n"

def score_start():
    ret = "\\score {\n"
    if midi: ret += "\\unfoldRepeats\n"
    ret += r"<< "
    if not notehead_markup.noBarNums and not midi: ret += ("\\override Score.BarNumber #'break-visibility = #center-visible\n\\override Score.BarNumber #'Y-offset = -1\n\\set Score.barNumberVisibility = #(every-nth-bar-number-visible %d)" % bar_number_every)
    return ret
bar_number_every = 5 # TODO customise?  (anyway don't leave it numbering at start of system, doesn't work well in jianpu+lyrics)

def score_end(**headers):
    ret = ">>\n"
    if headers:
        # since about Lilypond 2.7, music must come
        # before the header block if it's per-score
        ret += r"\header{"+'\n'
        for k,v in headers.items(): ret+=k+'="'+v+'"\n'
        ret += "}\n"
    layoutExtra = ""
    if not lyric_size == staff_size:
        from math import log
        lSize = log(lyric_size/staff_size)*6/log(2)
        if lSize > 3: sys.stderr.write("WARNING: potential layout problems; consider increasing j2ly_staff_size to be closer to j2ly_lyric_size\n") # TODO: is 3 a good threshold for this warning?  (need to check different Lilypond versions)
        layoutExtra=r" \override Lyrics.LyricText.font-size = #"+("+" if lSize>=0 else "")+str(lSize)+" "
    if notehead_markup.noIndent: layoutExtra += ' indent = 0.0 '
    if notehead_markup.raggedLast: layoutExtra += ' ragged-last = ##t '
    if notehead_markup.noBarNums: layoutExtra += r' \context { \Score \remove "Bar_number_engraver" } '
    if midi: ret += r"\midi { \context { \Score tempoWholesPerMinute = #(ly:make-moment 84 4)}}" # will be overridden by any \tempo command used later
    else: ret += r"\layout{"+layoutExtra+r"""
  \context {
    \Global
    \grobdescriptions #all-grob-descriptions
  }
  \context {
    \Score
    \consists \jianpuGraceCurveEngraver % for spans
  }
""" + "}"
    return ret + " }"

def uniqName():
    global uniqCount
    r = str(uniqCount) ; uniqCount += 1
    return r.translate((letters*5)[:256])
def jianpu_voice_start(isTemp=0):
    if not isTemp and maxBeams >= 2: stemLenFrac = "0.5" # sometimes needed if the semiquavers occur in isolation rather than in groups (TODO do we need to increase this for 3+ beams in some cases?)
    else: stemLenFrac = "0"
    voiceName = uniqName()
    r = (r"""\new Voice="%s" {"""%voiceName)
    r += r"""
    \override Beam #'transparent = ##f"""
    if not_angka:
        r +=r"""
        \override Stem #'direction = #UP
        \override Tie #'staff-position = #-2.5
        \tupletDown"""
        stemLenFrac=str(0.4+0.2*max(0,maxBeams-1))
    else: r += r"""
    \override Stem #'direction = #DOWN
    \override Tie #'staff-position = #2.5
    \tupletUp
    \tieUp"""
    r += (r"""
    \override Stem #'length-fraction = #%s
    \override Beam #'beam-thickness = #0.1
    \override Beam #'length-fraction = #0.5
    %s
    \override Voice.Rest #'style = #'neomensural %% this size tends to line up better (we'll override the appearance anyway)
    \override Accidental #'font-size = #-4
    \override TupletBracket #'bracket-visibility = ##t""" %
          (stemLenFrac,
           r"\override Beam.after-line-breaking = #flip-beams" if inner_beams_below else ""
           ))
    r += "\n"+r"""\set Voice.chordChanges = ##t %% 2.19 bug workaround""" # LilyPond 2.19.82: \applyOutput docs say "called for every layout object found in the context Context at the current time step" but 2.19.x breaks this by calling it for ALL contexts in the current time step, hence breaking our WithStaff by applying our jianpu numbers to the 5-line staff too.  Obvious workaround is to make our function check that the context it's called with matches our jianpu voice, but I'm not sure how to do this other than by setting a property that's not otherwise used, which we can test for in the function.  So I'm 'commandeering' the "chordChanges" property (there since at least 2.15 and used by Lilypond only when it's in chord mode, which we don't use, and if someone adds a chord-mode staff then it won't print noteheads anyway): we will substitute jianpu numbers for noteheads only if chordChanges = #t.
    return r+"\n", voiceName
def jianpu_staff_start(inst=None,withStaff=False):
    # (we add "BEGIN JIANPU STAFF" and "END JIANPU STAFF" comments to make it easier to copy/paste into other Lilypond files)
    if withStaff: inst = None # we'll put the label on the 5-line staff (TODO: use StaffGroup or something?)
    if not_angka: r=r"""
%% === BEGIN NOT ANGKA STAFF ===
    \new RhythmicStaff \with {"""
    else: r=r"""
%% === BEGIN JIANPU STAFF ===
    \new RhythmicStaff \with {
    \consists "Accidental_engraver" """
    if inst: r += 'instrumentName = "'+inst+'"'
    if withStaff: r+=r"""
   %% Limit space between Jianpu and corresponding-Western staff
   \override VerticalAxisGroup.staff-staff-spacing = #'((minimum-distance . 7) (basic-distance . 7) (stretchability . 0))
""" # (whether this is needed or not depends on Lilypond version; 2.22 puts more space than 2.18,2.20.  Must set higher than 5, which sometimes gets collisions between beams in 2.20)
    r+=r"""
    %% Get rid of the stave but not the barlines:
    \override StaffSymbol #'line-count = #0 %% tested in 2.15.40, 2.16.2, 2.18.0, 2.18.2, 2.20.0 and 2.22.2
    \override BarLine #'bar-extent = #'(-2 . 2) %% LilyPond 2.18: please make barlines as high as the time signature even though we're on a RhythmicStaff (2.16 and 2.15 don't need this although its presence doesn't hurt; Issue 3685 seems to indicate they'll fix it post-2.18)
    $(add-grace-property 'Voice 'Stem 'direction DOWN)
    $(add-grace-property 'Voice 'Slur 'direction UP)
    $(add-grace-property 'Voice 'Stem 'length-fraction 0.5)
    $(add-grace-property 'Voice 'Beam 'beam-thickness 0.1)
    $(add-grace-property 'Voice 'Beam 'length-fraction 0.3)
    $(add-grace-property 'Voice 'Beam 'after-line-breaking flip-beams)
    $(add-grace-property 'Voice 'Beam 'Y-offset %.1f)
    $(add-grace-property 'Voice 'NoteHead 'Y-offset %.1f)
    }
    { """ % (grace_height, grace_height)
    j,voiceName = jianpu_voice_start()
    r += j+r"""
    \override Staff.TimeSignature #'style = #'numbered
    \override Staff.Stem #'transparent = ##t
    """
    return r, voiceName
def jianpu_staff_end():
     # \bar "|." is added separately if there's not a DC etc
    if not_angka: return "} }\n% === END NOT ANGKA STAFF ===\n"
    else: return "} }\n% === END JIANPU STAFF ===\n"
def midi_staff_start():
    return r"""
%% === BEGIN MIDI STAFF ===
    \new Staff { \new Voice="%s" {""" % (uniqName(),)
def midi_staff_end(): return "} }\n% === END MIDI STAFF ===\n"
def western_staff_start(inst=None):
    r = r"""
%% === BEGIN 5-LINE STAFF ===
    \new Staff """
    if inst: r += r'\with { instrumentName = "'+inst+'" } '
    voiceName = uniqName()
    return (r+r"""{
    \override Score.SystemStartBar.collapse-height = #11 %% (needed on 2.22)
    \new Voice="%s" {
    #(set-accidental-style 'modern-cautionary)
    \override Staff.TimeSignature #'style = #'numbered
    \set Voice.chordChanges = ##f %% for 2.19.82 bug workaround
""" % (voiceName,)), voiceName
def western_staff_end(): return "} }\n% === END 5-LINE STAFF ===\n"

def lyrics_start(voiceName):
    return r'\new Lyrics = "I%s" { \lyricsto "%s" { ' % (uniqName(),voiceName)
def lyrics_end(): return "} }"

inner_beams_below = True # Use stencil reflection to invert Lilypond's normal beam positioning (like in David Zhang's jianpu10a.ly) - more accurately reflects jianpu typography but can result in octave dots being too far down because beam spacing is done per system not per beam
dashes_as_ties = True # Implement dash (-) continuations as invisible ties rather than rests; sometimes works better in awkward beaming situations
use_rest_hack = True # Implement some short rests as notes (and if there are lyrics, creates temporary voices so the lyrics miss them); sometimes works better for beaming (at least in 2.15 through 2.24)
if __name__=="__main__" and '--noRestHack' in sys.argv: # TODO: document
    use_rest_hack=False ; sys.argv.remove('--noRestHack')
assert not (use_rest_hack and not dashes_as_ties), "This combination has not been tested"

def errExit(msg):
    if __name__=="__main__":
        sys.stderr.write("Error: "+msg+"\n")
        sys.exit(1)
    else: raise Exception(msg)
def scoreError(msg,word,line):
    if len(word)>60: word=word[:50]+"..."
    msg += " %s in score %d" % (word,scoreNo)
    if len(line)>600: line=line[:500]+"..."
    if not word in line: pass # above truncations caused problems
    elif "xterm" in os.environ.get("TERM",""): # use xterm underline escapes
        msg += "\n"+re.sub(r"(\s|^)"+re.escape(word)+r"(?=\s|$)",lambda m:m.group(1)+"\x1b[4m"+word+"\x1b[m",line)
    elif re.match('[ -~]*$',line): # all ASCII: we can underline the word with ^^s
        msg += "\n"+line+"\n"+re.sub('[^^]',' ',re.sub(r"(\s|^)"+re.escape(word)+r"(?=\s|$)",lambda m:m.group(1)+'^'*(len(word)),line))
    else: # don't try to underline the word (at least not without ANSI): don't know how the terminal will handle character widths
        msg += "\nin this line: "+line
    errExit(msg)

placeholders = {
    # for accidentals and word-fitting to work
    # (we make them relative to the actual key later
    # so that MIDI pitches are correct)
    '0':'r',
    '1':'c',
    '2':'d',
    '3':'e',
    '4':'f',
    '5':'g',
    '6':'a',
    '7':'b',
    'x':'c',
    '-':'r'}

def addOctaves(octave1,octave2):
    octave2=octave2.replace(">","'").replace("<",",") # so it can be used with a base-octave change
    while octave1:
        if octave1[0] in "'>": # go up
            if ',' in octave2: octave2 = octave2[:-1]
            else: octave2 += "'"
        else: # , or < : go down
            if "'" in octave2: octave2 = octave2[:-1]
            else: octave2 += ","
        octave1=octave1[1:]
    return octave2

class NoteheadMarkup:
  def __init__(self,graceType=None):
      self.initOneScore()
      self.graceType = graceType
  def initOneScore(self):
      self.barLength = 64 ; self.beatLength = 16 # in 64th notes
      self.barPos = self.startBarPos = F(0)
      self.inBeamGroup = self.lastNBeams = self.onePage = self.noBarNums = self.noIndent = self.raggedLast = self.separateTimesig = self.withStaff = 0
      self.keepLength = 0
      self.last_octave = self.base_octave = ""
      self.current_accidentals = {} # used to predict whether Lilypond will draw the accidental or not, for beam spacing purposes
      self.barNo = 1
      self.tuplet = (1,1)
      self.last_figures = None
      self.last_was_rest = False
      self.notesHad = []
      self.unicode_approx = []
      self.rplacNextIfStillInBeam = None
      self.graceType = None
      self.current_chord = None
  def endScore(self):
      if self.barPos == self.startBarPos: pass
      elif os.environ.get("j2ly_sloppy_bars",""): sys.stderr.write("Wrong bar length at end of score %d ignored (j2ly_sloppy_bars set)\n" % scoreNo)
      elif self.startBarPos and not self.barPos: errExit("Score %d should end with a %g-beat bar to make up for the %g-beat anacrusis bar.  Set j2ly_sloppy_bars environment variable if you really want to break this rule." % (scoreNo,self.startBarPos/self.beatLength,(self.barLength-self.startBarPos)/self.beatLength)) # this is on the music theory syllabi at about Grade 3, but you can get up to Grade 5 practical without actually covering it, so we'd better not expect all users to understand "final bar does not make up for anacrusis bar"
      else: errExit("Incomplete bar at end of score %d (%g beats)" % (scoreNo,self.barPos*1.0/self.beatLength))
  def setTime(self,num,denom):
      self.barLength = int(64*num/denom)
      if denom>4 and num%3==0: self.beatLength = 24 # compound time
      else: self.beatLength = 16
  def setAnac(self,denom,dotted):
      self.barPos = F(self.barLength)-F(64)/denom
      if dotted: self.barPos -= F(64)/denom/2
      if self.barPos<0: errExit("Anacrusis is longer than bar in score %d" % scoreNo) # but anacrusis being exactly equal to bar is OK: we'll just interpret that as no anacrusis
      self.startBarPos = self.barPos
  def wholeBarRestLen(self): return {96:"1.",48:"2.",32:"2",24:"4.",16:"4",12:"8.",8:"8"}.get(self.barLength,"1") # TODO: what if irregular?
  def baseOctaveChange(self,change):
      self.base_octave = addOctaves(change,self.base_octave)
  def __call__(self,figures,nBeams,dots,octave,accidental,tremolo,word,line):
    # figures is a chord string of '1'-'7', or 'x' or '0' or '-'
    # nBeams is 0, 1, 2 .. etc (number of beams for this note)
    # dots is "" or "." or ".." etc (extra length)
    # octave is "", "'", "''", "'''", ",", ",," or ",,,"
    # accidental is "", "#", "b"
    # tremolo is "" or ":32"
    # word,line is for error handling
    if len(figures)>1:
        if accidental and not_angka: scoreError("Accidentals in chords not yet implemented in Indonesian not-angka mode:",word,line)
        if '0' in figures: scoreError("Can't have rest in chord:",word,line)
        if 'x' in figures: scoreError("Can't have percussion beat in chord:",word,line)
    self.notesHad.append(figures)

    isChord = len(figures)>1
    if isChord:
        chord_ret,octave,placeholder_chord = chordNotes_markup(re.sub('[qsdh.]','',word)) # word w/out durations
        if not midi and not western: placeholder_chord = "c"
    else: # not isChord
        placeholder_chord = placeholders[figures]
    
    invisTieLast = dashes_as_ties and self.last_figures and figures=="-" and not self.last_was_rest
    self.last_was_rest = (figures=='0' or (figures=='-' and self.last_was_rest))
    aftrLastNonDash = tieEnd = ""
    add_cautionary_accidental = False
    if invisTieLast: # (so figures == "-")
        if self.barPos==0 and not midi and not western and not self.last_figures=="x":
            # dash over barline: write as new note
            figures = self.last_figures
            aftrLastNonDash = r'\=JianpuTie('
            tieEnd = r'\=JianpuTie)'
            add_cautionary_accidental = self.last_accidental
            tremolo = self.last_tremolo
        else:
            if self.barPos==0 and not midi and not western and not self.last_figures=="x": sys.stderr.write("Warning: jianpu barline-crossing tie won't be done right because your Lilypond version is older than 2.20\n")
            if self.barPos==0: tremolo = self.last_tremolo
        if self.current_chord: # a chord is currently in progress, and we're extending it with a tie
            isChord = True
            chord_ret,octave,placeholder_chord = chordNotes_markup(re.sub('[qsdh.]','',self.current_chord))
            if not midi and not western: placeholder_chord = "c"
        else: # not a chord, so we can assume len(self.last_figures)==1
            placeholder_chord = placeholders[self.last_figures]
            octave = self.last_octave # for MIDI or 5-line
            accidental = self.last_accidental # ditto
    else: # not invisTieLast
        if not isChord: octave=addOctaves(octave,self.base_octave)
        if not octave in [",,,",",,",",","","'","''","'''"]: scoreError("Can't handle octave "+octave+" in",word,line)
        self.last_octave = octave
        self.last_tremolo = tremolo
        if isChord: self.current_chord = word
        else: self.current_chord = None
    if not figures=="-": self.last_figures = figures
    if not isChord and not accidental in ["","#","b"]: scoreError("Can't handle accidental "+accidental+" in",word,line)
    self.last_accidental = accidental

    ret = ""
    if self.barPos==0 and self.barNo > 1:
        ret += "| " # barline in Lilypond file: not strictly necessary but may help readability
        if self.onePage and not midi: ret += r"\noPageBreak "
        ret += "%{ bar "+str(self.barNo)+": %} "
    if not octave in self.current_accidentals: self.current_accidentals[octave] = [""]*7
    if nBeams==None: # unspecified
        if self.keepLength:
            nBeams = self.lastNBeams
        else: nBeams = 0
    if figures=="-" or all('1'<=figure<='7' and not accidental==self.current_accidentals[octave][int(figure)-1] for figure in list(figures)) and nBeams > self.lastNBeams: leftBeams = nBeams # beam needs to fit under the new accidental (or the dash which might be slightly to the left of where digits are), but if it's no more than last note's beams then we'll hang it only if in same beat.  (TODO: the current_accidentals logic may need revising if other accidental styles are used, e.g. modern-cautionary, although then would need to check anyway if our \consists "Accidental_engraver" is sufficient)
    # TODO: if figures=="0" then that might be typeset a bit to the left as well (because it's also a rest), however extending the line TOO far left in this case could be counterproductive
    elif self.inBeamGroup:
        if nBeams < self.lastNBeams: leftBeams = nBeams
        else: leftBeams = self.lastNBeams
    else: leftBeams = 0
    if leftBeams: assert nBeams, "following logic assumes if (leftBeams or nBeams) == if nBeams"
    aftrlast0 = ""
    if not nBeams and self.inBeamGroup:
        if not self.inBeamGroup=="restHack":
            aftrlast0 = "] "
        self.inBeamGroup = 0
    length = 4 ; b = 0 ; toAdd = F(16) # crotchet
    while b < nBeams: b,length,toAdd = b+1,length*2,toAdd/2
    toAdd0 = toAdd
    for _ in dots:
        toAdd0 /= 2 ; toAdd += toAdd0
    toAdd_preTuplet = toAdd
    if not self.tuplet[0]==self.tuplet[1]:
        toAdd = toAdd*self.tuplet[0]/self.tuplet[1]
    if nBeams and not midi and not western: # must set these unconditionally regardless of what we think their current values are (Lilypond's own beamer can change them from note to note)
        if not_angka:
            leftBeams=nBeams
            if (self.barPos+toAdd)%self.beatLength == 0: nBeams = 0
        ret += (r"\set stemLeftBeamCount = #%d"+"\n") % leftBeams
        ret += (r"\set stemRightBeamCount = #%d"+"\n") % nBeams
        if not_angka: nBeams = leftBeams
    need_space_for_accidental = False
    for figure in list(figures):
        if '1'<=figure<='7':
            if not accidental==self.current_accidentals[octave][int(figure)-1]:
                need_space_for_accidental = True
            self.current_accidentals[octave][int(figure)-1] = accidental # TODO: not sensible (assumes accidental applies to EVERY note in the chord, see above)
    inRestHack = replaceLast = 0
    if not midi and not western:
        if ret: ret = ret.rstrip()+"\n" # try to keep the .ly code vaguely readable
        if octave=="''" and not invisTieLast: ret += r"  \once \override Score.TextScript.outside-staff-priority = 45" # inside bar numbers etc
        if isChord and not figures=="-":
            ret += chord_ret
        elif figures=="-":
            if not_angka: figureDash=u"."
            else: figureDash=u"\u2013"
            if not type(u"")==type(""):
                figureDash=figureDash.encode('utf-8')
            ret += (r' \note-mod-angka "' if not_angka else r' \note-mod "')+figureDash+'" '
        else: # single, non-dash note
            s = str(figures)
            if not_angka and accidental:
                u338,u20e5=u"\u0338",u"\u20e5" # TODO: the \ looks better than the / in default font
                if not type("")==type(u""): u338,u20e5=u338.encode('utf-8'),u20e5.encode('utf-8')
                s += {'#':u338,'b':u20e5}[accidental]
            ret += (r' \note-mod-angka "' if not_angka else r' \note-mod "')+s+'" '
        if self.rplacNextIfStillInBeam and leftBeams and nBeams: replaceLast = self.rplacNextIfStillInBeam # didn't need the rest-hack here after all
        self.rplacNextIfStillInBeam = None
        if placeholder_chord == "r" and use_rest_hack and nBeams and not (leftBeams and not not_angka):
            placeholder_chord = "c"
            # C to work around diagonal-tail problem with
            # some isolated quaver rests in some Lilypond
            # versions (usually at end of bar); new voice
            # so lyrics miss it as if it were a rest:
            if has_lyrics and not self.withStaff: # (OK if self.withStaff: lyrics will be attached to that instead)
                self.rplacNextIfStillInBeam = ret
                ret = jianpu_voice_start(1)[0]+ret
                inRestHack = 1
                if self.inBeamGroup and not self.inBeamGroup=="restHack": aftrlast0 = "] "
    if placeholder_chord.startswith("<"): ret += placeholder_chord  # chord in western or midi
    elif not isChord or figures.startswith("-"): # single note or rest
        ret += placeholder_chord
        if midi or western or not not_angka: ret += {"":"", "#":"is", "b":"es"}[accidental]
        if not placeholder_chord=="r": ret += {"":"'","'":"''","''":"'''","'''":"''''",",":"",",,":",",",,,":",,"}[octave] # for MIDI + Western, put it so no-mark starts near middle C
        if add_cautionary_accidental: ret += "!"
    ret += ("%d" % length) + dots
    if self.rplacNextIfStillInBeam: self.rplacNextIfStillInBeam += ("r%d" % length) + dots + '['
    if tremolo:
        if midi or western:
            if placeholder_chord.startswith("<") and len(placeholder_chord.split())==4:
                previous,n1,n2,gtLenDot = ret.rsplit(None,3)
                previous=previous[:-1] # drop <
                ret = r"%s\repeat tremolo %d { %s32 %s32 }" % (previous,int(toAdd_preTuplet/4),n1,n2)
            else: ret += tremolo
        elif lilypond_minor_version()>=22:
            if dots: ret += r"""_\tweak outside-staff-priority ##f ^\tweak avoid-slur #'inside _\markup {\with-dimensions #'(0 . 0) #'(2.8 . 2.1) \postscript "1.6 -0.2 moveto 2.6 0.8 lineto 1.8 -0.4 moveto 2.8 0.6 lineto 2.0 -0.6 moveto 3.0 0.4 lineto stroke" } %{ requires Lilypond 2.22+ %} """
            else: ret += r"""_\tweak outside-staff-priority ##f ^\tweak avoid-slur #'inside _\markup {\with-dimensions #'(0 . 0) #'(2.5 . 2.1) \postscript "1.1 0.4 moveto 2.1 1.4 lineto 1.3 0.2 moveto 2.3 1.2 lineto 1.5 0.0 moveto 2.5 1.0 lineto stroke" } %{ requires Lilypond 2.22+ %} """
        elif dots: ret += r"""_\tweak outside-staff-priority ##f ^\tweak avoid-slur #'inside _\markup {\with-dimensions #'(0 . 0) #'(2.8 . 2.6) \postscript "1.4 1.6 moveto 2.4 2.6 lineto 1.6 1.4 moveto 2.6 2.4 lineto 1.8 1.2 moveto 2.8 2.2 lineto stroke" } %{ requires Lilypond 2.20 %} """
        else: ret += r"""_\tweak outside-staff-priority ##f ^\tweak avoid-slur #'inside _\markup {\with-dimensions #'(0 . 0) #'(2.5 . 2.6) \postscript "1.1 1.6 moveto 2.1 2.6 lineto 1.3 1.4 moveto 2.3 2.4 lineto 1.5 1.2 moveto 2.5 2.2 lineto stroke" } %{ requires Lilypond 2.20 %} """
    # Octave dots:
    if not midi and not western and not '-' in figures:
      if not nBeams:
          oDict = {",":r"-\tweak #'Y-offset #-1.2 ",
                   ",,":r"-\tweak #'Y-offset #-2 ",
                   ",,,":r"-\tweak #'Y-offset #-2.7 ",
                }
          ret += oDict.get(octave,"")
      elif self.graceType:
          oDict = {",":r"-\tweak #'Y-offset #%.1f " % (grace_height-1-nBeams*0.3),
                   ",,":r"-\tweak #'Y-offset #%.1f " % (grace_height-1.6-nBeams*0.3),
                   ",,,":r"-\tweak #'Y-offset #%.1f " % (grace_height-2-nBeams*0.3),
                }
          ret += oDict.get(octave,"")
      # Ugly fix for grace dot positions
      x_offset=0.6
      if self.graceType: x_offset=0.4
      oDict = {"":"",
            "'":"^.",
            "''":r"-\tweak #'X-offset #%.1f ^\two-dots " % x_offset,
            "'''":r"-\tweak #'X-offset #%.1f ^\three-dots " % x_offset,
            ",":r"-\tweak #'X-offset #%.1f _. " % x_offset,
            ",,":r"-\tweak #'X-offset #%.1f _\two-dots " % x_offset,
            ",,,":r"-\tweak #'X-offset #%.1f _\three-dots " % x_offset}
      if not_angka: oDict.update({
              "'":r"-\tweak #'extra-offset #'(0.4 . 2.7) -\markup{\bold .}",
              "''":r"-\tweak #'extra-offset #'(0.4 . 3.5) -\markup{\bold :}",
              "'''":r"-\tweak #'extra-offset #'(0.4 . 4.3) -\markup{\bold "+three_dots+"}",
              })
      ret += oDict[octave]
    if nBeams and (not self.inBeamGroup or (self.inBeamGroup=="restHack" and not replaceLast) or inRestHack) and not midi and not western:
        # We need the above stemLeftBeamCount, stemRightBeamCount override logic to work even if we're an isolated quaver, so do this:
        ret += '['
        self.inBeamGroup = 1
    self.barPos += toAdd
    if self.graceType and self.barPos == self.barLength:
        is_isolated_note = ret.endswith("[")
        if is_isolated_note:
            # Lilypond doesn't like isolated beamed notes in \grace
            # so introduce a skip note for it to beam to.
            # Putting the skip note BEFORE the grace note or AFTER the afterGrace note
            # might help if aligning jianpu with 5-line staves.
            if self.graceType == "before":
                ret = r"s%d [ \jianpuGraceCurveEnd %s" % (length,ret.replace("[",""))
            else:
                ret += r" \jianpuGraceCurveEnd s%d" % length
        else:
            ret = r" \jianpuGraceCurveEnd " + ret 
    # sys.stderr.write(accidental+figure+octave+dots+"/"+str(nBeams)+"->"+str(self.barPos)+" ") # if need to see where we are
    if self.barPos > self.barLength: errExit("(notesHad=%s) barcheck fail: note crosses barline at \"%s\" with %d beams (%d skipped from %d to %d, bypassing %d), scoreNo=%d barNo=%d (but the error could be earlier)" % (' '.join(self.notesHad),figures,nBeams,toAdd,self.barPos-toAdd,self.barPos,self.barLength,scoreNo,self.barNo))
    if self.barPos%self.beatLength == 0 and self.inBeamGroup: # (self.inBeamGroup is set only if not midi/western)
        # jianpu printouts tend to restart beams every beat
        # (but if there are no beams running anyway, it occasionally helps typesetting to keep the logical group running, e.g. to work around bugs involving beaming a dash-and-rest beat in 6/8) (TODO: what if there's a dash-and-rest BAR?  [..]-notated beams don't usually work across barlines
        ret += ']'
        self.inBeamGroup = 0 # DON'T reset lastNBeams here (needed for start-of-group accidental logic)
    elif inRestHack and self.inBeamGroup:
        ret += ']'
        self.inBeamGroup = "restHack"
    self.lastNBeams = nBeams
    beamC = u'\u0333' if nBeams>=2 else u'\u0332' if nBeams==1 else u""
    self.unicode_approx.append({'#':u"\u266f",'b':u"\u266d"}.get(0 if invisTieLast else accidental,u"")+(u"-" if invisTieLast else figures[-1:])+beamC+(u"" if invisTieLast else (u'\u0323' if "," in octave else u'\u0307' if "'" in octave else u""))+u''.join(c+beamC for c in dots)+(u"" if self.inBeamGroup else u" ")) # (NB inBeamGroup is correct only if not midi and not western)
    if self.barPos == self.barLength:
        self.unicode_approx[-1]=self.unicode_approx[-1].rstrip()+u'\u2502'
        self.barPos = 0 ; self.barNo += 1
        self.current_accidentals = {}
    if invisTieLast:
        if midi or western:
            b4last, aftrlast = "", " ~"
            if tremolo and placeholder_chord.startswith("<"):
                aftrlast = "" # can't tie this kind of tremolo as of Lilypond 2.24 (get warning: Unattached TieEvent)
        # elif not figures=='-': 
        #     b4last,aftrlast = r"\once \override Tie #'transparent = ##t \once \override Tie #'staff-position = #0 "," ~"
        else:
            b4last, aftrlast = "", ""
    else: b4last,aftrlast = "",""
    if figures=="x" and western: ret = r"\once \override NoteHead.style = #'cross \once \override NoteHead.no-ledgers = ##t " + ret
    if inRestHack: ret += " } " # end temporary voice for the "-" (non)-note
    elif tieEnd: ret += ' '+tieEnd # end of JianpuTie curve
    return aftrLastNonDash,figures=='-',b4last,replaceLast,aftrlast0+aftrlast,ret, need_space_for_accidental, nBeams,octave

def parseNote(word,origWord,line):
    if word==".": word = "-" # (for not angka, TODO: document that this is now acceptable as an input word?)
    word = word.replace("8","1'").replace("9","2'")
    if type(u"")==type(""): word = word.replace(u"\u2019","'")
    else: word=word.replace(u"\u2019".encode('utf-8'),"'")
    if "///" in word: tremolo,word=":32",word.replace("///","",1)
    else: tremolo = ""
    if not re.match(r"[0-7x.,'cqsdh\\#b-]+$",word): # unrecognised stuff in it: flag as error, rather than ignoring and possibly getting a puzzling barsync fail
        scoreError("Unrecognised command",origWord,line)
    figures = ''.join(re.findall('[01234567x-]',word))
    dots = "".join(c for c in word if c==".")
    nBeams = ''.join(re.findall(r'[cqsdh\\]',word))
    if re.match(r"[\\]+$",nBeams): nBeams=len(nBeams) # requested by a user who found British note-length names hard to remember; won't work if the \ is placed at the start, as that'll be a Lilypond command, so to save confusion we won't put this in the docstring
    elif nBeams:
        try: nBeams = list("cqsdh").index(nBeams)
        except ValueError: scoreError("Can't calculate number of beams from "+nBeams+" in",origWord,line)
    else: nBeams=None # unspecified
    octaves = re.findall("'+|,+",word)
    # chords of course accept multiple octaves
    if len(octaves)>1 and len(figures) == 1: scoreError("Multiple octaves should not applied to a single note:",origWord,line)
    if octaves: octave = octaves[0]
    else: octave = ""
    accidental = "".join(c for c in word if c in "#b")
    if len(figures) > 1: # octave + accidental dealt with separately BUT still need to keep one for the beaming and need_space_for_accidental logic (TODO actually current_accidentals needs rewriting for chords, but this works in most cases for now)
        accidental = accidental[:1]
    return figures,nBeams,dots,octave,accidental,tremolo

def write_docs():
    # Write an HTML or Markdown version of the doc string
    def htmlify(l):
        if "--html" in sys.argv:
            return re.sub('([hdDs]emi)',r'\1&shy;',l.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")).replace("approximation","approx&shy;imation")
        else: return l
    inTable = 0 ; justStarted=1
    for line in __doc__.split("\n"):
        if line.startswith("#") or not line.strip(): continue
        if ":" in line and line.split(":",1)[1].strip():
            toGet,shouldType = line.split(":",1)
            if not inTable:
                if "--html" in sys.argv:
                    print ("<table border>") # "<tr><th>To get:</th><th>Type:</th></tr>"
                else: print ("")
                inTable = 1
            if re.match(r".*[A-Za-z]\)$",shouldType):
                shouldType,note = shouldType.rsplit("(",1)
                note = " ("+note
            else: note = ""
            if "--html" in sys.argv: print ("<tr><td>"+htmlify(toGet.strip())+"</td><td><kbd>"+htmlify(shouldType.strip())+"</kbd>"+htmlify(note)+"</td>")
            else: print (toGet.strip()+": `"+shouldType.strip()+"`"+note+"\n")
        else:
            if "--markdown" in sys.argv: print ("")
            elif inTable: print ("</table>")
            elif not justStarted: print ("<br>")
            inTable=justStarted=0
            print (htmlify(line))
    if inTable and "--html" in sys.argv: print ("</table>")

def getInput0():
  inDat = []
  for f in sys.argv[1:]:
    if f.endswith(".mxl"): inDat.append(re.sub(r"<[?]xml.*?/container>\s*","",getoutput("unzip -qc "+quote(f)).replace("application/vnd.recordare.musicxml","").strip(),flags=re.DOTALL))
    else:
      try:
        try: inDat.append(open(f,encoding="utf-8").read()) # Python 3: try UTF-8 first
        except: inDat.append(open(f).read()) # Python 2, or Python 3 with locale-default encoding in case it's not UTF-8
      except: errExit("Unable to read file "+f)
  if inDat: return inDat
  if not sys.stdin.isatty():
    return [fix_utf8(sys.stdin,'r').read()]
  # They didn't give us any input.  Try to use a
  # file chooser.  If that fails, just print the
  # help text.
  if os.path.exists('/usr/bin/osascript'):
    f = os.popen("osascript -e $'tell application \"System Events\"\\nactivate\\nset f to choose file\\nend tell\\nPOSIX path of f'").read().rstrip()
    if f:
      try: return [open(f,encoding="utf-8").read()]
      except: return [open(f).read()]
  write_help() ; raise SystemExit

def write_help():
  write_version()
  sys.stderr.write("\n".join(l for l in __doc__.split("\n") if l.strip() and not l.startswith("#"))+"\n")
def write_version():
  versions = [] # output the biggest (might not be 1st listed)
  for l in __doc__.split("\n"):
      if l.startswith("# v"): versions.append((float(l[len("# v"):l.index(' ',len("# v"))]),l.replace("#","jianpu-ly",1)+"\n\n"))
  sys.stderr.write(max(versions)[1])

def get_input():
  inDat = getInput0()
  for i in xrange(len(inDat)):
    if inDat[i].startswith('\xef\xbb\xbf'):
      inDat[i] = inDat[i][3:]
    if inDat[i].startswith(r'\version'): errExit("jianpu-ly does not READ Lilypond code.\nPlease see the instructions.")
    elif inDat[i].startswith("<?xml"):
        inDat[i] = xml2jianpu(inDat[i])
  return " NextScore ".join(inDat)

def xml2jianpu(x):
    from xml.parsers.expat import ParserCreate
    xmlparser = ParserCreate()
    ret = [] ; dat = ["",""]
    partList=[""];time=["4","4"];tempo=["4","60"]
    note=[[""]*10];naturalType=[""];note1=["C"]
    tSig=[None,0];prevChord=[None]
    types={"64th":"h","32nd":"d","16th":"s","eighth":"q","quarter":"","half":" -","whole":" - - -"}
    typesDot={"64th":"h.","32nd":"d.","16th":"s.","eighth":"q.","quarter":".","half":" - -","whole":" - - - - -"}
    typesMM={"64th":"64","32nd":"32","16th":"16","eighth":"8","quarter":"4","half":"2","whole":"1"}
    quavers={"64th":0.125,"32nd":0.25,"16th":0.5,"eighth":1,"quarter":2,"half":4,"whole":8}
    def s(name,attrs): dat[0],dat[1]="",attrs.get("type","")
    def c(data): dat[0] += data
    def e(name):
        d0 = dat[0].strip()
        if name in ['work-title','movement-title']: ret.append('title='+d0)
        elif name=='creator' and dat[1]=="composer": ret.append('composer='+d0)
        elif name=="part-name" or name=="instrument-name": partList[-1]=d0
        elif name=="score-part": partList.append("")
        elif name=="part": # we're assuming score-partwise
            if partList:
                ret.append('instrument='+partList[0])
                del partList[0]
            ret.append("WithStaff NextPart")
        elif name=="fifths":
            if d0.startswith('-'): naturalType[0]='#'
            else: naturalType[0]='b'
            key = ["Gb","Db","Ab","Eb","Bb","F","C","G","D","A","E","B","F#"][int(d0)+6]
            note1[0]=key[0]
            ret.append("1="+key)
        elif name=="beats": time[0]=d0
        elif name=="beat-type": time[1]=d0
        elif name=="time":
            tSig[0] = len(ret) # so anacrusis logic can come back and add to this
            tSig[1] = 0 # count quavers in 1st bar
            ret.append("/".join(time))
        elif name=="backup" or name=="forward": errExit("MusicXML import: multiple voices per part not implemented")
        elif name=="measure" and not tSig[0]==None:
            if not tSig[1]==int(time[0])*8/int(time[1]): ret[tSig[0]]+=","+{0.5:"16",0.75:"16.",1:"8",1.5:"8.",2:"4",3:"4.",4:"2",6:"2.",8:"1",12:"1."}[tSig[1]] # anacrusis
            tSig[0]=None
        elif name=="beat-unit": tempo[0]=typesMM.get(name,"4")
        elif name=="beat-minute": tempo[1]=d0
        elif name=="metronome": ret.append("=".join(tempo))
        elif name=="step": note[0][0]=d0
        elif name=="rest": note[0][0]="r"
        elif name=="octave": note[0][1]=int(d0)
        elif name=="accidental": note[0][2]={"flat":"b","sharp":"#","natural":naturalType[0]}.get(d0,"") # TODO: what if it's natural-ing something that wasn't sharp or flat in the key signature
        elif name=="type": note[0][3]=d0
        elif name=="dot": note[0][4]=1
        elif name=="slur": note[0][5]={"start":"(","stop":")"}[dat[1]]
        elif name=="tie": note[0][6]={"start":"~","stop":""}[dat[1]]
        elif name=="actual-notes": note[0][7]=d0
        elif name=="tuplet": note[0][8]=dat[1]
        elif name=="chord": note[0][9]=True
        elif name=="note":
            step,octave,acc,nType,dot,slur,tie,tuplet,tState,chord = note[0]
            note[0]=[""]*10
            if step=="r": r="0"
            else:
                dTone=ord(step[0])-ord(note1[0])+7*(octave-4)
                if step[0] < 'C': dTone += 7
                r=str((dTone%7)+1)
                while dTone<0:
                    r+="," ; dTone+=7
                while dTone>6:
                    r+="'" ; dTone-=7
            if chord:
                ret[prevChord[0]] += r ; return
            if tState=="start": ret.append(tuplet+"[")
            if not tSig[0]==None: # we're counting the length of the first bar, for anacrusis
                tSig[1] += quavers[nType]
                if dot: tSig[1] += quavers[nType]/2.0
            if dot: d=typesDot
            else: d = types
            r += acc+d[nType]+' '
            prevChord[0]=len(ret)
            ret.append(r[:r.index(' ')]+' '+tie+' '+slur+r[r.index(' '):])
            if tState=="stop": ret.append("]")
    xmlparser.StartElementHandler = s
    xmlparser.CharacterDataHandler = c
    xmlparser.EndElementHandler = e
    xmlparser.Parse(x,True)
    return '\n'.join(ret)

def fix_utf8(stream,mode):
    if type("")==type(u""): # Python 3: please use UTF-8 for Lilypond, even if the system locale says something else
        import codecs
        if mode=='r': return codecs.getreader("utf-8")(stream.buffer)
        else: return codecs.getwriter("utf-8")(stream.buffer)
    else: return stream

def fix_fullwidth(t):
    if type(u"")==type(""): utext = t
    else: utext = t.decode('utf-8')
    r = []
    for c in utext:
        if 0xff01<=ord(c)<=0xff5e: r.append(unichr(ord(c)-0xfee0))
        elif c==u'\u201a': r.append(",") # sometimes used as comma (incorrectly)
        elif c==u'\uff61': r.append(".")
        else: r.append(c)
    utext = u"".join(r)
    if type(u"")==type(""): return utext
    else: return utext.encode('utf-8')

def graceNotes_markup(notes,isAfter,harmonic=False):
    if lilypond_minor_version()<22: errExit("grace notes requires Lilypond 2.22+, we found 2."+str(lilypond_minor_version()))
    thinspace = u'\u2009'
    if not type("")==type(u""): thinspace = thinspace.encode('utf-8')
    notes = grace_octave_fix(notes) # ensures octaves come before notes
    notemark = NoteheadMarkup(graceType="after" if isAfter else "before")
    # Calculate length of grace section and tell
    # NoteheadMarkup that's the "bar length", so it
    # ends the beams at the end of it for us
    notemark.barLength = 0
    curLen = 4 # default semiquaver, in 64th notes
    for n in notes:
        curLen = {'q':8,'s':4,'d':2,'h':1}.get(n,curLen)
        if '0'<=n<='9': 
            notemark.barLength += curLen
            curLen = 4 # reset after each note
    notemark.beatLength = notemark.barLength
    accidental = ""
    beams = 2 # default semiquaver
    figure = ""
    octave = ""
    mr = []
    if isAfter: mr.append(r"\once \override Score.JianpuGraceCurve.direction = #LEFT ")
    mr.append(r"\jianpuGraceCurveStart ")
    for i in xrange(len(notes)):
        n = notes[i]
        if n=='#':
            accidental = "#"
        elif n=='b': 
            accidental = "b"
        elif n=="'":
            if i and notes[i-1]==notes[i]: continue
            if notes[i:i+3]=="'''": octave = "'''"
            elif notes[i:i+2]=="''": octave = "''"
            else: octave = "'"
        elif n==',':
            if i and notes[i-1]==notes[i]: continue
            if notes[i:i+3]==",,,": octave = ",,,"
            elif notes[i:i+2]==",,": octave = ",,"
            else: octave = ","
        elif n in 'qsdh': beams = '*qsdh'.index(n)
        else:
            # number should be the last char of a note
            figure = n
            mr.append(notemark(figure, beams, "", octave, accidental, "", "", "")[5])
            if harmonic: mr[-1]+=r" \flageolet " # deal with harmonic articulations
            accidental = ""
            beams = 2 # reset after each note
            figure = ""
            octave = ""
    mr = ''.join(mr)
    offset = "-2.5 . 0" if isAfter else "-0.5 . -0.5"
    return mr
def grace_octave_fix(notes): return re.sub(
        "(.*)([1-7])([^1-7]+)$",
        lambda m:grace_octave_fix(m.group(1))+m.group(3)+m.group(2),
        notes.replace("8","1'").replace("9","2'")) # ensures 8ves, durations and accidentals come before main notes, not after
def gracenotes_western(notes):
    # for western and MIDI staffs
    notes = grace_octave_fix(notes)
    nextAcc = "" ; next8ve = "'" ; current_accidentals = [0]*7
    r = []
    duration = 16
    for i in xrange(len(notes)):
        n = notes[i]
        if n=='#': nextAcc = "is"
        elif n=='b': nextAcc = "es"
        elif n=="'":
            if i and notes[i-1]==notes[i]: continue
            if notes[i:i+3]=="'''": next8ve = "''''"
            elif notes[i:i+2]=="''": next8ve = "'''"
            else: next8ve = "''"
        elif n==',':
            if i and notes[i-1]==notes[i]: continue
            if notes[i:i+3]==",,,": next8ve = ",,"
            elif notes[i:i+2]==",,": next8ve = ","
            else: next8ve = ""
        elif n in 'qsdh': duration = {'q':8, 's':16, 'd':32, 'h':64}[n]
        else:
            if not n in placeholders: continue # TODO: errExit ?
            r.append(placeholders[n]+nextAcc+next8ve+str(duration))
            nextAcc = "" ; next8ve = "'"
    return ' '.join(r)
def chordNotes_markup(notes):
    notes = grace_octave_fix(notes) # ensures octaves come before notes
    accidental = ""
    figure = ""
    octave = ""
    sortKey = 0
    dNotes = []
    mr = []
    
    for i in xrange(len(notes)):
        n = notes[i]
        if n=='#':
            accidental = "#"
            sortKey += 0.5
        elif n=='b': 
            accidental = "b"
            sortKey -= 0.5
        elif n=="'":
            if i and notes[i-1]==notes[i]: continue
            if notes[i:i+3]=="'''": 
                octave = "'''"
                sortKey += 22
            elif notes[i:i+2]=="''": 
                octave = "''"
                sortKey += 15
            else: 
                octave = "'"
                sortKey += 8
        elif n==',':
            if i and notes[i-1]==notes[i]: continue
            if notes[i:i+3]==",,,": 
                octave = ",,,"
                sortKey -= 22
            elif notes[i:i+2]==",,": 
                octave = ",,"
                sortKey -= 15
            else: 
                octave = ","
                sortKey -= 8
        else:
            # number should be the last char of a note
            if n not in '01234567' : continue
            figure = n
            if int(n) == 0: sortKey = 0
            else: sortKey += int(n)
            dNotes.append({
                'sortKey':sortKey,
                'figure':figure,
                'octave':octave,
                'accidental':accidental})
            accidental = ""
            figure = ""
            octave = ""
            sortKey = 0
    dNotes.sort(key=lambda element:element['sortKey'])
    placeholder_chord= "< "
    for f in dNotes:
        placeholder_chord += placeholders[f['figure']]+{"":"", "#":"is", "b":"es"}[f['accidental']]
        if "," in f['octave']: placeholder_chord += f['octave'][:-1]+" "
        else: placeholder_chord += f['octave']+"' "
    placeholder_chord += ">"

    # skip the bottom octave dots
    # as the they are dealed with markups outside.
    bottom_octave = top_octave = ""
    if "," in dNotes[0]['octave']:
        bottom_octave = dNotes[0]['octave']
        dNotes[0]['octave'] = ""

    # let's put octaves inside chord
    offsets = {"'":1,
        "''":1.6,
        "'''":2.2,
        ",":1,
        ",,":1.6,
        ",,,":2.2}
    oDict = {"":"",
        "'":"^.",
        "''":r"-\tweak #'X-offset #0.6 ^\two-dots ",
        "'''":r"-\tweak #'X-offset #0.6 ^\three-dots ",
        ",":r"-\tweak #'X-offset #0.6 _. ",
        ",,":r"-\tweak #'X-offset #0.6 _\two-dots ",
        ",,,":r"-\tweak #'X-offset #0.6 _\three-dots "}
    ret = "< "
    baseline = 0
    for f in dNotes:
        # octaves below rises the baseline
        if ',' in f['octave']: baseline += offsets[f['octave']]
        if baseline > 0:
            ret += r"\tweak #'Y-offset #%.1f " % baseline
        ret += (r'\note-mod-angka "' if not_angka else r'\note-mod "')+f['figure']+'" '+placeholders[f['figure']]+{"":"", "#":"is", "b":"es"}[f['accidental']]
        if "," in f['octave']: ret += f['octave'][:-1]+" "
        else: ret += f['octave']+"' "
        if "," in f['octave']: ret += r"\tweak #'Y-offset #%.1f " % (baseline -0.1 - 1.2 * offsets[f['octave']])
        elif "'" in f['octave']: ret += r"\tweak #'Y-offset #%.1f " % (baseline + 1.6 + 0.02 * offsets[f['octave']])
        ret += oDict[f['octave']]+" "
        baseline += 2
        if "'" in f['octave']: baseline += offsets[f['octave']]
    ret += ">"
    return ret,bottom_octave,placeholder_chord

def getLY(score,headers=None,have_final_barline=True):
   if not headers: headers = {} # Python 2 persists this dict if it's in the default args
   lyrics = []
   notehead_markup.initOneScore()
   out = [] ; maxBeams = 0
   need_final_barline = False
   repeatStack = [] ; lastPtr = 0
   lastNonDashPtr = 0
   rStartP = None
   escaping = inTranspose = 0
   aftrnext = defined_jianpuGrace = defined_JGR = None
   aftrnext2 = None
   isInHarmonic = False
   for line in score.split("\n"):
    line = fix_fullwidth(line).strip()
    line=re.sub(r"^%%\s*tempo:\s*(\S+)\s*$",r"\1",line) # to provide an upgrade path for jihuan-tian's fork
    if line.startswith("LP:"):
        # Escaped LilyPond block.  Thanks to James Harkins for this suggestion.
        # (Our internal barcheck does not understand code in LP blocks, so keep it to complete bars.)
        escaping = 1
        if len(line)>len("LP:"): out.append(line[3:]+"\n") # remainder of current line
    elif line.startswith(":LP"):
        escaping = 0
        if line.replace(":LP","").strip(): sys.stderr.write("Warning: current implementation ignores anything after :LP on same line\n") # TODO
    elif escaping:
        out.append(line+"\n")
    elif not line: pass
    elif line.startswith("L:") or line.startswith("H:"):
        # lyrics
        do_hanzi_spacing = line.startswith("H:")
        line = line[2:].strip()
        toAdd = ""
        if line and '1' <= line[0] <= '9' and (line[1]=='.' or asUnicode(line)[1]==u"\uff0e"):
            # a verse number
            toAdd = r'\set stanza = #"%s." ' % line[:1]
            if line[1]=='.': line=line[2:]
            elif not type(line)==type(u""): line=line[4:] # for utf-8 full-width dot in Python 2
            else: line = line[2:] # for full-width dot in Python 3
            line = line.strip()
        if do_hanzi_spacing: # this is not 100% perfect...
            l2 = [r"\override LyricText #'self-alignment-X = #LEFT "] # for overhanging commas etc to work
            if toAdd:
                l2.append(toAdd) ; toAdd = ""
            needSpace = 0
            for c in list(asUnicode(line)):
                is_hanzi = (0x3400 <= ord(c) < 0xa700) # TODO: also cover those outside the BMP?  but beware narrow Python builds
                is_openquote = c in u"\u2018\u201c\u300A"
                if needSpace and (is_hanzi or is_openquote):
                    l2.append(' ') ; needSpace = 0
                    if is_openquote: # hang left
                        l2.append(r"\once \override LyricText #'self-alignment-X = #CENTER ") # or RIGHT if there's no punctuation after
                if is_hanzi: needSpace=1
                if c=="_": needSpace=0 # TODO: document this: separate hanzi with _ to put more than one on same note
                else: l2.append(c)
            line = u"".join(l2)
            if not type("")==type(u""): line = line.encode('utf-8') # Python 2
        lyrics.append(toAdd+re.sub("(?<=[^- ])- "," -- ",line).replace(" -- "," --\n"))
    elif re.match(r"\s*[A-Za-z]+\s*=",line):
        # Lilypond header (or guitar chords)
        hName,hValue = line.split("=",1)
        hName,hValue = hName.strip().lower(),hValue.strip()
        if not headers.get(hName,hValue)==hValue:
            if hName=='instrument': missing='NextPart or NextScore'
            else: missing='NextScore'
            errExit("Changing header '%s' from '%s' to '%s' (is there a missing %s?)" % (hName,headers[hName],hValue,missing))
        headers[hName] = hValue
    else:
        line=re.sub('(?<= )[_^]"[^" ]* [^"]*"(?= |$)',lambda m:m.group().replace(' ',chr(0))," "+line)[1:] # multi-word text above/below stave
        for word in line.split():
            word=word.replace(chr(0)," ")
            if word in ["souyin","harmonic","up","down","bend","tilde"]: word="Fr="+word # (Fr= before these is optional)
            if re.match("[16]=[#b][A-Ga-g]$",word): word=word[:2]+word[3]+word[2] # somebody wrote a key name backwards (bE instead of Eb), we can fix that here
            # -----------------------------------
            # Start of main 'switch' on each word
            # -----------------------------------
            if word.startswith('%'): break # a comment
            elif word == "Harm:":
                isInHarmonic = True
            elif word==":Harm":
                isInHarmonic = False
            elif re.match("[1-468]+[.]*=[1-9][0-9]*$",word): out.append(r'\tempo '+word) # TODO: reduce size a little?
            elif re.match("[16]=[A-Ga-g][#b]?$",word): #key
                # Must use \transpose because \transposition doesn't always work.
                # However, don't use \transpose if printing - it adds extra accidentals to the rhythm staff.
                # So we have to do separate runs of \layout and \midi (hence the outer loop).
                notehead_markup.unicode_approx.append(u''+re.sub('(?<!=)b$',u'\u266d',word.replace('#',u'\u266f')).upper()+u' ')
                if midi or western:
                    if inTranspose: out.append('}')
                    if word[0]=="6": transposeFrom = "a"
                    else: transposeFrom = "c"
                    transposeTo = word[word.index('=')+1:].replace("#","is").replace("b","es").lower()
                    if midi and transposeTo[0] in "gab": transposeTo += ','
                    out.append(r"\transpose c "+transposeTo+r" { \key c \major ") # so that MIDI or Western pitches are correct
                    inTranspose = 1
                else: out.append(r'\mark \markup{%s}' % word.replace("b",r"\flat").replace("#",r"\sharp"))
            elif word.startswith("Fr="):
              finger = word.split("=")[1]
              finger = {
                  "0": u"\u5b80",
                  "1": u"\u4e00", "2": u"\u4e8c",
                  "3": u"\u4e09", "4": u"\u56db",
                  "souyin": u"\u4e45", # jiu3
                  "harmonic": u"\u25cb", # white circle: TODO: can we use Lilypond's ^\flageolet command (not in a \finger{}) which doesn't require a font with 25CB in it? or would that get wrong size? (can be tweaked)
                  "up": u"\u2197", # NE arrow
                  "down": u"\u2198", # SE arrow
                  "bend": u"\u293b", # bottom arc anticlockwise arrow
                  "tilde": u"\u223c", # full-width tilde.  Could also use U+1D008 "Byzantine musical symbol syrmatiki" but that (a) won't display on macOS (as of 12.6) and (b) needs special consideration for old versions of Python 2 on narrow Unicode builds
                  }.get(finger, finger)
              if not type("")==type(u""): finger = finger.encode('utf-8') # Python 2
              out.append(r'\finger \markup { \fontsize #-4 "%s" } ' % finger)
            elif re.match("letter[A-Z]$",word):
                out.append(r'\mark \markup { \box { "%s" } }' % word[-1]) # TODO: not compatible with key change at same point, at least not in lilypond 2.20 (2nd mark mentioned will be dropped)
            elif re.match(r"R\*[1-9][0-9]*$",word):
                if not western: out.append(r"\set Score.skipBars = ##t \override MultiMeasureRest #'expand-limit = #1 ") # \compressFullBarRests on Lilypond 2.20, \compressEmptyMeasures on 2.22, both map to \set Score.skipBars
                out.append(r"R"+notehead_markup.wholeBarRestLen()+word[1:])
            elif re.match("[1-9][0-9]*/[1-468]+(,[1-9][0-9]*[.]?)?$",word): # time signature
                if ',' in word: # anacrusis
                    word,anac = word.split(",",1)
                else: anac=""
                if notehead_markup.separateTimesig and not midi: out.append(r'\mark \markup{'+word+'}')
                out.append(r'\time '+word)
                num,denom = word.split('/')
                notehead_markup.setTime(int(num),int(denom))
                if anac:
                    if anac.endswith("."): # e.g. 2.
                        a2 = anac[:-1] ; anacDotted = 1
                    else: a2,anacDotted = anac,0
                    notehead_markup.setAnac(int(a2),anacDotted)
                    out.append(r'\partial '+anac)
            elif word=="OnePage":
                if notehead_markup.onePage: sys.stderr.write("WARNING: Duplicate OnePage, did you miss out a NextScore?\n")
                notehead_markup.onePage=1
            elif word=="KeepOctave": pass # undocumented option removed in 1.7, no effect
            elif word=="KeepLength": # TODO: document this.  If this is on, you have to use c in a note to go back to crotchets.
                notehead_markup.keepLength=1
            elif word=="NoBarNums":
                if notehead_markup.noBarNums: sys.stderr.write("WARNING: Duplicate NoBarNums, did you miss out a NextScore?\n")
                notehead_markup.noBarNums=1
            elif word=="NoIndent":
                if notehead_markup.noIndent: sys.stderr.write("WARNING: Duplicate NoIndent, did you miss out a NextScore?\n")
                notehead_markup.noIndent=1
            elif word=="RaggedLast":
                if notehead_markup.raggedLast: sys.stderr.write("WARNING: Duplicate Raggedlast, did you miss out a NextScore?\n")
                notehead_markup.raggedLast=1
            elif word=="SeparateTimesig":
                if notehead_markup.separateTimesig: sys.stderr.write("WARNING: Duplicate SeparateTimesig, did you miss out a NextScore?\n")
                notehead_markup.separateTimesig=1
                out.append(r"\override Staff.TimeSignature #'stencil = ##f")
            elif word in ["angka","Indonesian"]:
                global not_angka
                if not_angka: sys.stderr.write("WARNING: Duplicate angka, did you miss out a NextScore?\n")
                not_angka = True
            elif word=="WithStaff":
                if notehead_markup.withStaff: sys.stderr.write("WARNING: Duplicate WithStaff, did you miss out a NextScore?\n")
                notehead_markup.withStaff=1
            elif word=="PartMidi": pass # handled in process_input
            elif word=="R{":
                repeatStack.append((1,notehead_markup.barPos,0,len(out)))
                if out: out[-1]=re.sub(r' \\bar "|."$',"",out[-1]) # in case starting after a Fine
                out.append(r'\repeat volta 2 {')
            elif re.match("R[1-9][0-9]*{$",word):
                times = int(word[1:-1])
                repeatStack.append((1,notehead_markup.barPos,times-1,len(out)))
                if out: out[-1]=re.sub(r' \\bar "|."$',"",out[-1])
                out.append(r'\repeat percent %d {' % times)
            elif word=="}":
                numBraces,oldBarPos,extraRepeats,rStartP = repeatStack.pop()
                out.append("}"*numBraces)
                # Re-synchronise so bar check still works if percent is less than a bar:
                newBarPos = notehead_markup.barPos
                while newBarPos < oldBarPos: newBarPos += notehead_markup.barLength
                # newBarPos-oldBarPos now gives the remainder (mod barLength) of the percent section's length
                if numBraces==1: notehead_markup.barPos = (notehead_markup.barPos + (newBarPos-oldBarPos)*extraRepeats) % notehead_markup.barLength
                # TODO: update barNo also (but it's used only for error reports)
            elif word=="A{":
                out[rStartP] = out[rStartP].replace('percent','volta') # for time-bars with 3 or more times, you can say R3{ ... } A{ ... } (TODO document this)
                repeatStack.append((2,notehead_markup.barPos,0,rStartP))
                out.append(r'\alternative { {')
            elif word=="|" and repeatStack and repeatStack[-1][0]==2:
                out.append("} {") # separate repeat alternates (if the repeatStack conditions are not met i.e. we're not in an A block, then we fall through to the undocumented use of | as barline check below)
                numBraces,oldBarPos,extraRepeats,rStartP = repeatStack.pop()
                notehead_markup.barPos = oldBarPos
                repeatStack.append((numBraces,oldBarPos,extraRepeats+1,rStartP))
                out[rStartP] = out[rStartP].replace(('volta %d ' % (extraRepeats+1)),('volta %d ' % (extraRepeats+2))) # ensure there's enough repeats for the alternatives
            elif word.startswith("\\") or word.startswith('^\\') or word.startswith('_\\') or word in ["(",")","~","->","|"] or word.startswith('^"') or word.startswith('_"'):
                # Lilypond command, \p, ^"text", barline check (undocumented, see above), etc
                if word=="~" and not midi and not western and lastNonDashPtr < lastPtr: # tie from the number, not the last dash
                    out.insert(lastNonDashPtr+1,r'\=JianpuTie(')
                    lastPtr += 1
                    aftrnext2 = r'\=JianpuTie)'
                elif out and "afterGrace" in out[lastPtr]:
                    # apply to inside afterGrace in midi/western
                    out[lastPtr] = out[lastPtr][:-1] + word + " }"
                else:
                    out.append(word)
                    if word=="~" and not midi and not western and lastNonDashPtr < lastPtr: sys.stderr.write("Warning: jianpu long-note tie won't be done right because your Lilypond version is older than 2.20\n")
            elif re.match(r"[1-9][0-9]*\[$",word):
                # tuplet start, e.g. 3[
                fitIn = int(word[:-1])
                i=2
                while i<fitIn: i*=2
                if i==fitIn: num=int(fitIn*3/2)
                else: num=int(i/2)
                out.append("\\times %d/%d {" % (num,fitIn))
                notehead_markup.tuplet = (num,fitIn)
            elif word==']': # tuplet end
                out.append("}")
                notehead_markup.tuplet = (1,1)
            elif re.match(r"g\[[#b',1-9qsdh]+\]$",word):
                if midi or western: out.append(r"\grace { " + gracenotes_western(word[2:-1]) + " }")
                else: out.append(r"\grace { " + graceNotes_markup(word[2:-1],0,isInHarmonic) + " }")
            elif re.match(r"\[[#b',1-9,q,s,d,h]+\]g$",word):
                if midi or western: out[lastPtr] = r" \afterGrace { " + out[lastPtr] + " } { " + gracenotes_western(word[1:-2]) + " }"
                else: out[lastPtr] = r" \afterGrace { " + out[lastPtr] + " } { " + graceNotes_markup(word[1:-2],1,isInHarmonic) + " }"
            elif word=="Fine":
                need_final_barline = False
                out.append(r'''\once \override Score.RehearsalMark #'break-visibility = #begin-of-line-invisible \once \override Score.RehearsalMark #'self-alignment-X = #RIGHT \mark "Fine" \bar "|."''')
            elif word=="DC":
                need_final_barline = False
                out.append(r'''\once \override Score.RehearsalMark #'break-visibility = #begin-of-line-invisible \once \override Score.RehearsalMark #'self-alignment-X = #RIGHT \mark "D.C. al Fine" \bar "||"''')
            else: # note (or unrecognised)
                word0 = word
                baseOctaveChange = "".join(c for c in word if c in "<>")
                if baseOctaveChange:
                    notehead_markup.baseOctaveChange(baseOctaveChange)
                    word = "".join(c for c in word if not c in "<>")
                    if not word: continue # allow just < and > by itself in a word
                figures,nBeams,dots,octave,accidental,tremolo = parseNote(word,word0,line)
                need_final_barline = True
                aftrLastNonDash,isDash,b4last,replaceLast,aftrlast,this,need_space_for_accidental,nBeams,octave = notehead_markup(figures,nBeams,dots,octave,accidental,tremolo,word0,line)
                if replaceLast: out[lastPtr]=replaceLast
                if b4last: out[lastPtr]=b4last+out[lastPtr]
                if aftrlast: out.insert(lastPtr+1,aftrlast)
                if aftrLastNonDash: out.insert(lastNonDashPtr+1,aftrLastNonDash)
                lastPtr = len(out)
                if not isDash: lastNonDashPtr = len(out)
                out.append(this)
                if aftrnext2:
                    out.append(aftrnext2)
                    aftrnext2 = None
                if aftrnext:
                    if need_space_for_accidental: aftrnext = aftrnext.replace(r"\markup",r"\markup \halign #2 ",1)
                    out.append(aftrnext)
                    aftrnext = None
                if not_angka and "'" in octave: maxBeams=max(maxBeams,len(octave)*.8+nBeams)
                else: maxBeams=max(maxBeams,nBeams)
                if isInHarmonic and not midi and not western and not figures=='-': out[-1]+=r" \flageolet "
   if notehead_markup.barPos == 0 and notehead_markup.barNo == 1: errExit("No jianpu in score %d" % scoreNo)
   if notehead_markup.inBeamGroup and not midi and not western and not notehead_markup.inBeamGroup=="restHack": out[lastPtr] += ']' # needed if ending on an incomplete beat
   if inTranspose: out.append("}")
   if repeatStack: errExit("Unterminated repeat in score %d" % scoreNo)
   if escaping: errExit("Unterminated LP: in score %d" % scoreNo)
   notehead_markup.endScore() # perform checks
   if have_final_barline and need_final_barline and not midi: out.append(r'\bar "|."')
   i=0
   while i < len(out)-1:
       while i<len(out)-1 and out[i].startswith(r'\mark \markup{') and out[i].endswith('}') and out[i+1].startswith(r'\mark \markup{') and out[i+1].endswith('}'):
           # merge time/key signatures
           nbsp = u'\u00a0'
           if not type(u"")==type(""): # Python 2
               nbsp = nbsp.encode('utf-8')
           out[i]=out[i][:-1]+nbsp+' '+out[i+1][len(r'\mark \markup{'):]
           del out[i+1]
       i += 1
   for i in xrange(len(out)-1):
       if not out[i].endswith('\n'):
           if '\n' in out[i] or len(out[i])>60:
               out[i] += '\n'
           else: out[i]+=' '
   out = ''.join(out)
   if midi or western: # collapse/combine tied notes into longer notes (even in MIDI, for 2-note tremolo extension)
       for numNotes,dot,result in [
               (4,r"\.","1."), # in 12/8, 4 dotted crotchets = dotted semibreve
               (4,"","1"), # 4 crotchets = semibreve
               (3,"","2."), # 3 crotchets = dotted minim
               (2,r"\.","2."), # in 6/8, 2 dotted crotchets = dotted minim
               (2,"","2")]: # 2 crotchets = minim
           out = re.sub("(?P<note>[^<][^ ]*|<[^>]*>)4"+dot+r"((?::32)?) +~(( \\[^ ]+)*) "+" +~ ".join(["(?P=note)4"+dot]*(numNotes-1)),r"\g<1>"+result+r"\g<2>\g<3>",out)
           if dot: chkLen=6
           else: chkLen = 4
           out = re.sub(r"\\repeat tremolo "+str(chkLen)+r" { (?P<note1>[^ ]+)32 (?P<note2>[^ ]+)32 } +~(( \\[^ ]+)*) "+" +~ ".join(["< (?P=note1) (?P=note2) >4"+dot]*(numNotes-1)),r"\\repeat tremolo "+str(chkLen*numNotes)+r" { \g<1>32 \g<2>32 }\g<3>",out)
           out = out.replace(" ".join(["r4"+dot]*numNotes),"r"+result)
       out = re.sub(r"(\\repeat tremolo [^{]+{ [^ ]+)( [^}]+ })(( +\\[^b][^ ]*)+)",r"\g<1>\g<3>\g<2>",out) # dynamics need to attach inside the tremolo (but \bar doesn't)
       out = re.sub(r"(%\{ bar [0-9]*: %\} | \\major ) *r(?=[^ ]* [| ]* (?:\\noPageBreak )?%\{ bar|\\bar)",r"\g<1>R",out)
       out = out.replace(r"\new RhythmicStaff \with {",r"\new RhythmicStaff \with { \override VerticalAxisGroup.default-staff-staff-spacing = #'((basic-distance . 6) (minimum-distance . 6) (stretchability . 0)) ") # don't let it hang too far up in the air
   if not_angka: out=out.replace("make-bold-markup","make-simple-markup")
   return out,maxBeams,lyrics,headers

def process_input(inDat):
 global unicode_mode
 unicode_mode = not not re.search(r"\sUnicode\s"," "+inDat+" ")
 if unicode_mode: return get_unicode_approx(re.sub(r"\sUnicode\s"," "," "+inDat+" ").strip())+"\n"
 ret = []
 global scoreNo, western, has_lyrics, midi, not_angka, maxBeams, uniqCount, notehead_markup
 uniqCount = 0 ; notehead_markup = NoteheadMarkup()
 scoreNo = 0 # incr'd to 1 below
 western = False
 find_grace_height(inDat)
 for score in re.split(r"\sNextScore\s"," "+inDat+" "):
  if not score.strip(): continue
  scoreNo += 1
  has_lyrics = not not re.search("(^|\n)[LH]:",score) # The occasional false positive doesn't matter: has_lyrics==False is only an optimisation so we don't have to create use_rest_hack voices.  It is however important to always detect lyrics if they are present.
  parts = [p for p in re.split(r"\sNextPart\s"," "+score+" ") if p.strip()]
  for midi in [False,True]:
   not_angka = False # may be set by getLY
   if scoreNo==1 and not midi: ret.append(all_scores_start(inDat)) # now we've established non-empty
   separate_score_per_part = midi and re.search(r"\sPartMidi\s"," "+score+" ") and len(parts)>1 # TODO: document this (results in 1st MIDI file containing all parts, then each MIDI file containing one part, if there's more than 1 part)
   for separate_scores in [False,True] if separate_score_per_part else [False]:
    headers = {} # will accumulate below
    for partNo,part in enumerate(parts):
     if partNo==0 or separate_scores:
         ret.append(score_start())
     out,maxBeams,lyrics,headers = getLY(part,headers,partNo==0 or separate_scores) # assume 1st part doesn't have 'tacet al fine'
     if notehead_markup.withStaff and notehead_markup.separateTimesig: errExit("Use of both WithStaff and SeparateTimesig in the same piece is not yet implemented")
     if len(parts)>1 and "instrument" in headers:
         inst = headers["instrument"]
         del headers["instrument"]
     else: inst = None
     if "chords" in headers:
         if "frets" in headers:
             frets = headers["frets"]
             assert frets in ["guitar","ukulele","mandolin"]
             fretsInc = r'\include "predefined-'+frets+'-fretboards.ly"\n'
             if not fretsInc in ret: ret.insert(1,fretsInc) # after all-scores-start
             del headers["frets"]
         else: frets = None
         ret.append(r'\new ChordNames { \chordmode { '+headers["chords"]+' } }')
         if frets: ret.append(r'\new FretBoards { '+('' if frets=='guitar' else r'\set Staff.stringTunings = #'+frets+'-tuning')+r' \chordmode { '+headers["chords"]+' } }')
         del headers["chords"]
     if midi:
       ret.append(midi_staff_start()+" "+out+" "+midi_staff_end())
     else:
       staffStart,voiceName = jianpu_staff_start(inst,notehead_markup.withStaff)
       ret.append(staffStart+" "+out+" "+jianpu_staff_end())
       if notehead_markup.withStaff:
           western=True
           staffStart,voiceName = western_staff_start(inst)
           ret.append(staffStart+" "+getLY(part,have_final_barline=False)[0]+" "+western_staff_end())
           western = False
       if lyrics: ret.append("".join(lyrics_start(voiceName)+l+" "+lyrics_end()+" " for l in lyrics))
     if partNo==len(parts)-1 or separate_scores:
       ret.append(score_end(**headers))
 ret = "".join(r+"\n" for r in ret)
 if lilypond_minor_version() >= 24: ret=re.sub(r"(\\override [A-Z][^ ]*) #'",r"\1.",ret) # needed to avoid deprecation warnings on Lilypond 2.24
 return ret

def get_unicode_approx(inDat):
    if re.search(r"\sNextPart\s"," "+inDat+" "): errExit("multiple parts in Unicode mode not yet supported")
    if re.search(r"\sNextScore\s"," "+inDat+" "): errExit("multiple scores in Unicode mode not yet supported")
    # TODO: also pick up on other not-supported stuff e.g. grace notes (or check for unicode_mode when these are encountered)
    global notehead_markup, western, midi, uniqCount, scoreNo, has_lyrics, not_angka, maxBeams
    notehead_markup = NoteheadMarkup()
    western = midi = not_angka = False
    has_lyrics = True # doesn't matter for our purposes (see 'false positive' comment above)
    uniqCount = 0 ; scoreNo = 1
    getLY(inDat,{})
    u=u''.join(notehead_markup.unicode_approx)
    if u.endswith(u'\u2502'): u=u[:-1]+u'\u2551'
    return u

try: from shlex import quote
except:
    def quote(f): return "'"+f.replace("'","'\"'\"'")+"'"

def write_output(outDat):
    if sys.stdout.isatty():
      if unicode_mode:
        if sys.platform=='win32' and sys.version_info() < (3,6):
          # Unicode on this console could be a problem
          print ("""
For Unicode approximation on this system, please do one of these things:
(1) redirect output to a file,
(2) upgrade to Python 3.6 or above, or
(3) switch from Microsoft Windows to GNU/Linux""")
          return
      else: # normal Lilypond
        # They didn't redirect our output.
        # Try to be a little more 'user friendly'
        # and see if we can put it in a temporary
        # Lilypond file and run Lilypond for them.
        # New in jianpu-ly v1.61.
        if len(sys.argv)>1: fn=os.path.split(sys.argv[1])[1]
        else: fn = 'jianpu'
        if os.extsep in fn: fn=fn[:-fn.rindex(os.extsep)]
        fn += ".ly"
        import tempfile
        cwd = os.getcwd()
        os.chdir(tempfile.gettempdir())
        print("Outputting to "+os.getcwd()+"/"+fn)
        o = open(fn,'w')
        fix_utf8(o,'w').write(outDat)
        o.close()
        pdf = fn[:-3]+'.pdf'
        try: os.remove(pdf) # so won't show old one if lilypond fails
        except: pass
        cmd = lilypond_command()
        if cmd:
            cmd += ' -dstrokeadjust' # if will be viewed on-screen rather than printed, and it's not a Retina display
            os.system(cmd+" "+quote(fn))
            if sys.platform=='darwin':
                os.system("open "+quote(pdf))
            elif sys.platform.startswith('win'):
                import subprocess
                subprocess.Popen([quote(pdf)],shell=True)
            elif hasattr(shutil,'which') and shutil.which('evince'): os.system("evince "+quote(pdf))
        os.chdir(cwd) ; return
    fix_utf8(sys.stdout,'w').write(outDat)

def main():
    if "--html" in sys.argv or "--markdown" in sys.argv:
        return write_docs()
    if '--help' in sys.argv or '-h' in sys.argv or '/?' in sys.argv: return write_help()
    if '--version' in sys.argv or '-v' in sys.argv or '/v' in sys.argv: return write_version()
    inDat = get_input()
    out = process_input(inDat) # <-- you can also call this if importing as a module
    write_output(out)

if __name__=="__main__": main()
