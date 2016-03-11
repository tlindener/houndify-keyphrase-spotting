def getClientMatches():
    return [
      {
        'Expression': '"hello there"',
        'Result': { 'Intent' : 'WAVE' },
        'SpokenResponse': 'Ay boo',
        'SpokenResponseLong': 'Ay boo thang',
        'WrittenResponse': 'Ay boo',
        'WrittenResponseLong': 'Ay boo thang'
      },
      {
        'Expression': '[("do"| "the")] . "caterpillars" . "know" . [("that" | "if")] . "they" . ["will"] . "become" . ("a butterfly" | "butterflies") . ("when" | "while") . "they" . ["are"] . ("make" | "making") . "their" . "cocoon"',
        'Result': { 'Intent' : 'CONFIRM' },
        'SpokenResponse': 'Yes.',
        'SpokenResponseLong': 'Yes. I know because I am a butterfly.',
        'WrittenResponse': 'Yes.',
        'WrittenResponseLong': 'Yes. I know because I am a butterfly.'
      },
      {
        'Expression': '["when"] . "caterpillars" . "make" . "their" . "cocoon" . "do". "they" . "know" . ("that" | "if") . "they" . ["will"] . "become" . ("a butterfly" | "butterflies")',
        'Result': { 'Intent' : 'CONFIRM' },
        'SpokenResponse': 'Yes.',
        'SpokenResponseLong': 'Yes. I know because I am a butterfly.',
        'WrittenResponse': 'Yes.',
        'WrittenResponseLong': 'Yes. I know because I am a butterfly.'
      },
      {
        'Expression': '"do you" . ("like" | "enjoy") . ["to eat"] . "ice cream"',
        'Result': { 'Intent' : 'CONFIRM' },
        'SpokenResponse': 'Yes.',
        'SpokenResponseLong': 'Yes. Especially chocolate.',
        'WrittenResponse': 'Yes.',
        'WrittenResponseLong': 'Yes. Especially chocolate.'
      }
    ]
