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
        'Expression': '["do"] . "caterpillars" . "know" . [("that" | "if")] . "they" . ["will"] . "become" . ("a butterfly" | "butterflies") . ("when" | "while") . "they" . ["are"] . ("make" | "making") . "their" . "cocoon"',
        'Result': { 'Intent' : 'CONFIRM' },
        'SpokenResponse': 'Yes.',
        'SpokenResponseLong': 'Yes they do know.',
        'WrittenResponse': 'Yes.',
        'WrittenResponseLong': 'Yes they do know.'
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
