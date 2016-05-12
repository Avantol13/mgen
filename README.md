Music Generator
===============
 > By: Alexander VanTol

Generates randomized musical compositions based on probabilities.

Overview
--------

1. /mingus (not my code, see [this](https://github.com/bspaans/python-mingus))
2. /music_generator (my code)
    - choice.py *||||| Makes choices based on probabilities in a style*
    - convert.py *|||| Converts my stuff to mingus stuff and vice-versa*
    - create.py *||||| The magic happens here. Contains the MusicGenerator class*
    - style.py *|||||| Contains the Style class which defines probabilities*
    - time.py *||||||| Handles note and bar musical timing math stuff*
3. /output (where the generated stuff goes)
4. /styles (holds cfg files for different styles)
5. lilypond-2.18.2-1.mingw.exe (program for PDF generation)
    - This one's for Windows (works with Windows 10)
    - See [here](http://lilypond.org/download.html) for alternate downloads
6. MidiPlayW7.exe (a free midi player, see [here](http://www.chrishills.org.uk/midiplay/))

        TODO: Add link to documentation
See documentation [here]().
