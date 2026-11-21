# The World in One Picture — 21 November 2026

A newspaper-style front page for Saturday 21 November 2026, drawn
entirely by code. `main.py` (Python standard library only, no network,
no clock, no randomness) renders a 1024×1024 PNG to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `out/entry.png`). Running it
twice produces byte-identical output.

## The lead story

**Claude "solves" maths' greatest riddle.** Anthropic mathematician
Levent Alpöge announced on Friday 20 November that he and Claude had
proved the Riemann hypothesis — the 1859 problem about the distribution
of the prime numbers, unsolved for 167 years — releasing a formal proof
in the Lean programming language. Hours later, Stanford professor Ravi
Vakil shared a second, fully human proof by postdoc Alessandro Masullo.
Independent mathematicians, including MIT's Andrew Sutherland, have
recompiled Alpöge's Lean code and say it checks out; a final
"comparator" check and the $1M Clay Millennium Prize are still ahead.
Sources: Scientific American, AFP (via phys.org / The Daily Star),
The Wall Street Journal.

The picture is a chalkboard: ζ(s) = 0, Re(s) = 1/2, the first primes,
and a wavy curve crossing the critical line, with a gold chalk tick.

## Also in the news

- **The Hague — Myanmar calls the ICJ verdict unfair.** Myanmar's
  military-backed government dismissed the world court's genocide
  ruling as unfair, pointing to the 9–6 split; reparations were
  ordered but the court cannot enforce them. (CNN, Al Jazeera)
- **Ukraine — Russia pounds Ukraine anew.** Fresh Russian strikes
  followed Putin's vow of retaliation; Poland called a Russian
  missile that crashed on its soil a deliberate provocation. (AP)
- **Denmark — Russia plot to kill, Copenhagen says.** Denmark
  accused Russian intelligence of plotting to kill an
  American-Ukrainian citizen on Danish soil. (AP)
- **New York — 19½ years in Sikh murder plot.** Indian national
  Nikhil Gupta was sentenced to 235 months for a murder-for-hire
  plot against Sikh separatist Gurpatwant Singh Pannun. (AP,
  The Hindu)
- **Peru — M6.9 quake shakes the Andes.** A magnitude 6.9
  earthquake struck 34 km north of Junín at 108 km depth; tremors
  were felt in Lima, with no casualties or damage reported. (USGS
  via AP / The Straits Times)
- **Climate — COP31: crunch time, no deal in sight.** Talks in
  Turkey dragged on with negotiators struggling to forge a
  consensus. (Reuters)
- **Europe — protests join forces over prices.** Workers and
  students marched across Europe against the cost of living. (Reuters)
- **Brazil — Bolsonaro in hospital.** Former president Jair
  Bolsonaro was hospitalised with abdominal pain. (AFP)

## Run it

```sh
python3 main.py                       # writes out/entry.png
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
```

## License

MIT — see `LICENSE`.
