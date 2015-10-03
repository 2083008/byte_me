import sqlite3

data = sqlite3.connect('db.sqlite3')
c=data.cursor()

tweets = [ 'Happy birthday mum',
'Happy go lucky, me',
"I'm gonna chib ye",
'I am Ron Burgandy',
"I have no face",
"Time to set this alight",
"I hate my cat Tilly!",
"If I were a monkey",
"eleven is the age to be",
"David Cameron's pig #Disgusting",
"David Cameron = #Disgustsme",
"Who do you think you are David Cameron",
"I wish I could fly",
"Glasgow Uni looks like Hogwarts", 
"The Hackathon is on fire",
"That fire looks pure nasty #fire #Iloveshoes",
"Someone shut up that pig #noise",
"fed my teacup pig #getawayDavidCameron",
"January though, am I right?",
"JJ, it's over!",
"Sean the sheep for PM"]

postcodes = [ "G1", "G3","G11","G22","G1","G10","G60","G60","G27",
              "G41", "G5", "G5", "G17", "G21", "G56", "G36", "G5" "G5",
              "G11", "G23"]

times = [ 1443895125, 1443895432, 1443894908,
          1443895265, 1443895198, 1443895342,
          1443895785, 1443896522,
          1443895444, 1443899231,
          1443895987, 1443895128,
          1443895721, 1443895198,
          1443894367, 1443895143,
          1443895121, 1443895111,
          1443890876, 1443896789]

for i in range(0,19):
    c.execute("INSERT INTO hackathon_tweet VALUES (?,?,?,?,?,?)",(postcodes[i],tweets[i], times[i], '',0,0))
data.commit()

    
