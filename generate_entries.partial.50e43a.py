#!/usr/bin/env python3
"""Generate new Heritage Parlor entries from 6 source books."""

import json

# Existing titles for deduplication (lowercase)
EXISTING_TITLES = {
    'a deal in apples', 'a post-office perplexity', 'a puzzling legacy', 'acting proverbs',
    'acting rhymes', 'adjectives', "aesop's mission", 'all fours (seven up)', 'alphabet games',
    'animal vegetable or mineral', 'auction bridge', 'authors', 'baccarat', 'backgammon',
    'battledore and shuttlecock', 'beggar my neighbor', 'beggar your neighbor extended', 'bezique',
    'bezique (rubicon)', 'birds fly', 'bishops on a chessboard', "blind man's buff",
    "blind man's wand", 'blind postman', 'blowing out the candle', 'bob cherry', 'bottle imps',
    'bouts rimés', 'bridge', 'buff says baff', 'buying presents', 'buzz', 
    'canfield (klondike solitaire variant)', 'capping verses', 'carrying fire in the hands',
    'cassino', 'cat and mouse', "cat's cradle", 'centennial (dice racing)', 'charades', 'chess',
    'chinese pictures (water trick)', 'clairvoyant', 'coin through the handkerchief',
    'coin to orange', 'commerce', 'commit (stops)', 'conquian (coon can)', 'consequences',
    'consequences (extended)', 'conveyances', 'crambo', 'cribbage', 'cribbage (four-hand)',
    'cribbage (three-hand)', 'cross questions and crooked answers', 'cup and ball',
    'cup and ball (bilboquet)', 'cupid is coming', 'definitions', 'dice (chuck-a-luck)',
    'digital roots', 'dominoes (block game)', 'draughts (checkers)', 'draughts (checkers) variants',
    'drop the handkerchief', 'dumb crambo', 'dumb motions', 'earth air fire water', 'ecarte',
    'egg through table', 'euchre', 'famous people', 'faro', 'finding a chosen card by mathematics',
    'finding the ring', 'fire eating', 'flying', 'forcing a card', 'forfeits', 'fox and geese',
    'fox and geese (board)', 'fox and geese (outdoor, snowy)', 'french roll', 'frog in the middle',
    'gin rummy', 'going to jerusalem', 'green gravel', 'guess four thought-of cards', 'halma',
    'hand (coddem)', 'happy families', 'hearts', 'honey pots', 'hot boiled beans', 'hot cockles',
    'how do you like your neighbour?', 'how where and when', 'how, when, and where?',
    'huckle buckle beanstalk', 'hunt the ring', 'hunt the slipper', 'hunt the whistle',
    'i apprenticed my son', 'i love my love', 'i suspect you', 'indiscriminate charity',
    'invisible writing revealed', "jack's alive", 'knaves (polignac)', 'knucklebones',
    'knucklebones (jacks)', 'loo', 'lost and found', 'lotto (bingo)', 'magic music',
    'magic writing', 'magical music', 'merry thought', 'mixed-up poetry',
    "mr. o'callaghan's party", 'musical chairs', 'my master bids you do as i do',
    'napoleon (nap)', "nine men's morris", 'noughts and crosses (tic-tac-toe)', 'odd man out',
    'old maid', 'oranges and lemons', 'pairs', 'patience (klondike solitaire)', 'personations',
    'piquet', 'poker (draw)', 'pope joan', 'pope joan (full rules)', 'postal chess (correspondence chess)',
    "postman's knock", 'proverbs', 'punch and judy', 'puss in the corner', 'red-cap and black-cap',
    'reversi (othello)', 'riddles competition', 'ring through the handkerchief', 'ring through the table',
    'rummy (basic)', 'russian gossip', 'schimmel', 'second sight act', 'shadow buff',
    'shouting proverbs', 'simon says', 'slate games (birds beasts fishes)', 'snap',
    'snip snap snorum', 'speculation', 'spelicans', 'spelicans (pick-up sticks)', 'spelling bee',
    'spinning the plate', 'spoil five (five fingers)', 'square money', 'string through the neck',
    'tableau vivant', 'telegrammes', 'telegrams', 'telling the hour on a pocket watch',
    'the adventurers', 'the age puzzle', 'the archery puzzle', "the artists' menagerie",
    'the ascending card', 'the barrel of beer', 'the beanfeast puzzle', 'the bleeding thumb',
    'the broken chessboard', 'the buried treasure', 'the butterfly trick', 'the button puzzle',
    'the card puzzle', 'the cardboard puzzle', "the carpenter's puzzle", 'the christmas boxes',
    'the circle puzzle', "the clerk of oxenford's puzzle", 'the clock puzzle',
    'the coin and tumbler trick', 'the coin in the bread', 'the comic concert', 'the compasses puzzle',
    'the converted miser', "the cook's puzzle", 'the cups and balls', "the curious housekeeper's puzzle",
    'the cushion dance', 'the cut string restored', "the cyclists' feast", 'the cylinder puzzle',
    'the dancing sailor figure', 'the dissected square', "the dissection of viereck's square",
    'the divided garden', 'the domino trick', 'the dorcas society puzzle', "the dutchmen's wives",
    'the egg and handkerchief', 'the egg bag', 'the eight queens', 'the electric bell',
    'the elements', 'the family coach', 'the fare box puzzle', "the farmer's fence",
    "the farmer's puzzle", "the farmer's sheep", 'the farmyard', 'the farmyard concert',
    'the feather', 'the fifteen puzzle', 'the fishing puzzle', "the fly's tour", 'the flying shilling',
    'the forbidden letter', 'the fountain puzzle', 'the four elements',
    'the four elements (cassells)', 'the four frogs', 'the four kings together by cut',
    "the friar's puzzle", 'the gallery of animals', 'the gallery of statues', 'the game of animals',
    'the game of conversation', 'the game of proverbs', 'the garden puzzle',
    "the grandmother's necklace", "the haberdasher's puzzle", 'the handcuffs',
    'the hat trick production', 'the hat-peg puzzle', "the host's puzzle", 'the huntsman',
    'the indian sand trick', 'the inexhaustible bottle', 'the interrupted letters',
    'the jolly miller', "the junior clerk's puzzle", "the knight's puzzle", "the landlord's puzzle",
    'the linking rings', 'the lost number', 'the magic answer', 'the magic cover vanish',
    'the magic mill', 'the magic mill trick', 'the magic music box', 'the magic rings',
    'the magic rings of paper', 'the magic square (order 3)', 'the magic sword card catch',
    'the magic wand', 'the magic wand coin vanish', 'the magic wand production',
    "the man of law's puzzle", 'the memory game', "the merchant's puzzle", "the miller's puzzle",
    "the millionaire's perplexity", "the minister's cat", "the minstrel's puzzle",
    "the miser's puzzle", 'the monk and the pilgrim', "the monk's puzzle", 'the mouse and the cat',
    'the mutilated chessboard', 'the mysterious addition of coins', 'the mysterious funnel',
    'the newspaper game', 'the nine counters', 'the noughts and crosses tournament',
    "the nun's puzzle", 'the nuns puzzle', 'the obedient ball', 'the obedient coin (heads and tails)',
    'the object game', 'the old soldier', 'the paper dart competition', 'the paper pellet mind-reading',
    "the pardoner's puzzle", 'the passe-passe bottle and glass', 'the patchwork quilt',
    'the perplexed cellarman', 'the pigs of widow green', "the ploughman's puzzle", 'the popgun',
    'the pork butcher', "the prisoner's escape", 'the prisoners in a row',
    "the problem of the governor's wife", 'the puzzle of the doctor of physic',
    "the puzzle of the squire's yeoman", 'the puzzles of domenico rosario',
    'the puzzles of the black knight', 'the puzzling money-boxes', "the puzzlists' holiday",
    "the quaker's meeting", 'the resting wand', "the reve's puzzle", 'the rising cards (hair method)',
    'the river crossing problem', "the rook's tour", 'the row of halfpence', 'the schoolmaster',
    'the sculptor', 'the sea king', 'the see-saw puzzle', "the shipman's puzzle",
    'the shunting puzzle', 'the skipper and the sea-serpent', 'the snail puzzle',
    "the sompnour's puzzle", 'the spanish nobleman', 'the spelling game', 'the spider and the fly',
    "the spider's web puzzle", 'the square puzzle', "the squire's puzzle",
    "the squire's puzzle (word arithmetic)", 'the stage coach', 'the staircase puzzle',
    "the tapiser's puzzle", 'the three cups', 'the three prisoners', 'the three-card trick',
    'the torn and restored card', 'the torn card restored (simple)', "the traveler's alphabet",
    "the traveller's rhyme", 'the travelling alphabet', 'the two aeroplanes',
    'the vanishing glass of water', 'the vanishing knot', "the weaver's puzzle",
    'the whist trick with prepared pack', "the widow's legacy", "the wife of bath's riddles",
    "the witch's spell", 'thought reading', 'throwing the smile', 'towers of hanoi', 'trades',
    'trussed fowls', 'twenty questions', 'twirl the trencher', 'vingt-et-un (pontoon)',
    'vingt-et-un (twenty-one)', 'whist', 'whist (solo whist)', 'winking'
}

def make_id(title):
    """Convert title to kebab-case id."""
    import re
    s = title.lower()
    s = re.sub(r"['\",()!?]", '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s

def is_duplicate(title):
    """Check if title already exists."""
    return title.lower().strip() in EXISTING_TITLES

all_entries = []

# ============================================================
# GOMME VOL. I (1894) - Traditional Games of England Vol. I
# ============================================================
gomme1_entries = [
    {
        "title": "Accroshay",
        "category": "folk-game",
        "subcategory": "jumping-game",
        "tags": ["jumping", "children", "street-game", "Victorian"],
        "difficulty": "beginner",
        "players": "3+",
        "equipment": ["cap or small article"],
        "family_friendly": True,
        "original_description": "A cap or small article is placed on the back of a stooping boy by other boys, each in turn jumping over him. The first as he jumps says 'Accroshay,' the second 'Ashotay,' the third 'Assheflay,' and the last 'Lament, lament, Leleeman's war.' The boy who knocks off the article in jumping must take the place of the stooper.",
        "modern_description": "One player stoops down while others take turns leaping over their back, each calling out their special word in sequence: 'Accroshay,' 'Ashotay,' 'Assheflay,' and finally 'Lament, lament, Leleeman's war.' A small object is balanced on the stooping player's back. Any jumper who knocks off the object must become the new stooper. A lively, vocal jumping game perfect for outdoor play.",
        "fun_fact": "This game is one of many Victorian 'leapfrog' variants with nonsense rhymes; the chanted words may be corrupted French phrases, hinting at the cross-Channel travel of folk games.",
        "image_prompt": "Victorian street scene, group of boys in caps and breeches taking turns leaping over a stooping boy, cobblestone alley, late afternoon light, energetic and playful, circa 1890s."
    },
    {
        "title": "All a Row",
        "category": "folk-game",
        "subcategory": "marching-game",
        "tags": ["singing", "marching", "rhyme", "children", "ring-game"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "A marching game for very little children, who follow each other in a row while singing: 'All a row, a bendy bow, / Shoot at a pigeon and kill a crow; / Shoot at another and kill his brother; / Shoot again and kill a wren, / And that'll do for gentlemen.'",
        "modern_description": "Children line up one behind another and march in a row while chanting the rhyme together. The game is simple enough for toddlers and is primarily an exercise in cooperative movement and memorizing a fun rhyme. Leadership can rotate so each child gets a turn at the front of the line.",
        "fun_fact": "This is one of the simplest surviving British folk games, recorded across many counties; its nonsensical shooting verse likely descends from Tudor-era archery practice rhymes.",
        "image_prompt": "Watercolor illustration of five small Victorian children marching in a line through a sunny garden, arms swinging, the smallest at the back, flowers and hedgerow behind them, soft pastoral style."
    },
    {
        "title": "All in the Well",
        "category": "folk-game",
        "subcategory": "throwing-game",
        "tags": ["throwing", "marbles", "buttons", "children", "outdoor"],
        "difficulty": "beginner",
        "players": "3+",
        "equipment": ["wooden peg", "button", "marbles or buttons for stakes"],
        "family_friendly": True,
        "original_description": "A circle termed the 'well' is drawn on the ground with a wooden peg in the centre and a button balanced on top. Players give items—buttons or marbles—for a short stick to throw at the peg. If the button flies out of the circle, the thrower wins double the value of the stakes.",
        "modern_description": "Draw a circle on the ground and plant a short peg in the middle. Balance a button or coin on top of the peg. Players take turns throwing a stick at the peg from a set distance; if the button lands outside the circle, the thrower wins double their stake. If not, the stakes remain for the next round. First player to a target number of winnings is the champion.",
        "fun_fact": "A variant of this game played at Newcastle Races used three pegs arranged in a triangle, each topped with a penknife or copper coin—evidence that folk games freely adapted to local fairs and festivals.",
        "image_prompt": "Victorian children clustered around a small chalk circle in a park, one child preparing to throw a stick at a wooden peg, others watching intently, buttons and marbles scattered on the ground nearby, ink-and-wash illustration."
    },
    {
        "title": "All the Boys in Our Town",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "ring-game", "partner-choosing", "courtship", "children"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Children form a ring with one child in the centre. After the first verse is sung, a child from the ring joins the one in the centre. The rest sing additional verses while the pair act out the words—pairing off like sweethearts—as directed by the song: 'All the boys in our town / Shall lead a happy life, / Except 'tis ——, and he wants a wife.'",
        "modern_description": "Players stand in a circle with one child in the middle. The ring sings the opening verse, substituting a child's real name. A child from the ring joins the centre child, and together they act out the romantic verse—bowing, linking arms, or miming a wedding. The first centre child rejoins the ring, and the game continues with the new centre child choosing a partner.",
        "fun_fact": "This partner-choosing game is found with nearly identical verses across Hampshire, Yorkshire, and Scotland, showing how folk games spread along trade and migration routes.",
        "image_prompt": "Victorian children in a flower-strewn meadow, forming a ring and singing, a small boy and girl in the center bowing to each other shyly, the surrounding children clapping, warm summer day, colored woodcut style."
    },
    {
        "title": "Alligoshee",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "partner-game", "arm-linking", "skipping", "children"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Children form pairs with arms linked behind them. They skip forward then back while singing the first four lines; at the last line—'Turn the bridle over my knee'—they turn about without loosing hands: 'Betsy Blue came all in black... / Alligoshi, alligoshee, / Turn the bridle over my knee.'",
        "modern_description": "Pair up with a partner and link arms behind each other's backs. Skip forward together for four counts, then backward for four, in time with the song. At the last line, both partners turn outward simultaneously without letting go. The game continues with a new verse as the pair finds their rhythm. The challenge is to keep the arm-link intact through all the turning.",
        "fun_fact": "The word 'Alligoshee' appears to be pure nonsense vocalization, a common feature in British folk game refrains designed to be memorable and easy for small children to chant.",
        "image_prompt": "Two Victorian girls in pinafores and boots, arms linked behind their backs, skipping joyfully across a village green, other children watching and clapping, church steeple visible in the background, pen and ink illustration."
    },
    {
        "title": "Angel and Devil",
        "category": "folk-game",
        "subcategory": "guessing-game",
        "tags": ["guessing", "role-play", "colours", "children", "dramatic"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "One player is the Angel, one the Devil, and one the Minder. The Minder secretly assigns colours to the other children. The Angel knocks; a dialogue follows, and if the Angel guesses a child's colour correctly, that child is led away to the Angel's side. The Devil then repeats the process, trying to claim children for the other team.",
        "modern_description": "Assign roles: one Angel, one Devil, and one Minder. The Minder whispers a colour name to each remaining player and remembers all assignments. The Angel knocks and asks for children by colour; correct guesses claim that child for the Angel's team. Then the Devil takes a turn. Alternate rounds until all children are claimed; the team with more players wins. The Minder must keep all assignments secret.",
        "fun_fact": "Angel-and-Devil games appear across Europe under many names and are thought to reflect medieval morality plays simplified into children's entertainment.",
        "image_prompt": "Victorian parlor, three children in costume—one with paper wings as Angel, one with a cape as Devil, one as the Minder—other children lined up against the wall, candlelit room, theatrical and dramatic atmosphere."
    },
    {
        "title": "Auntieloomie",
        "category": "folk-game",
        "subcategory": "dancing-game",
        "tags": ["singing", "dancing", "ring-game", "kissing", "children"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Children join hands and dance in a circle using a front step, back step, and side step round an imaginary Maypole, singing: 'Can you dance the Auntieloomie? / Yes, I can; yes, I can.' The dance culminates in a kissing round.",
        "modern_description": "Players hold hands in a circle and practice a simple three-step folk-dance pattern: step forward, step back, and step sideways around the circle. All sing the question-and-answer verse together. The game builds into a merry, whirling dance, and tradition dictates that the final verse ends with partners kissing or simply bowing to each other.",
        "fun_fact": "'Auntieloomie' is almost certainly a corruption of some older local term; games with nonsense names like this were widespread in Scotland and northern England as the 19th century drew the old Maypole dances indoors.",
        "image_prompt": "Scottish village children dancing in a ring around a flower-garlanded post, holding hands, faces flushed and laughing, cottage and rolling hills in the background, watercolor in warm earth tones."
    },
    {
        "title": "Babbity Bowster",
        "category": "folk-game",
        "subcategory": "dancing-game",
        "tags": ["singing", "dancing", "courtship", "handkerchief", "Scotland"],
        "difficulty": "intermediate",
        "players": "6+",
        "equipment": ["handkerchief or bolster"],
        "family_friendly": True,
        "original_description": "At the end of a country ball, a boy dances before the girls while singing 'Wha learned you to dance? / Babbity Bowster brawly?' He throws a handkerchief onto a selected girl, who must fight playfully to avoid a kiss. She then takes the handkerchief and sings the second verse, throwing it to a boy and pursuing him back. Pairs form a line and dance like Sir Roger de Coverley.",
        "modern_description": "This traditional Scottish country-dance game starts with one player dancing alone before a line of the opposite group, singing the verse about Babbity Bowster. The handkerchief is tossed onto a chosen partner, who must be 'caught' for a kiss. The new holder sings the next verse and throws the handkerchief, reversing roles. Play continues until all have partnered up and the group forms a grand pair-dance.",
        "fun_fact": "Babbity Bowster was historically played as the last game at Scottish weddings and harvest feasts; a real bolster was originally used, giving the game its name—'bowster' being an old Scots word for bolster.",
        "image_prompt": "Highland ball room, late evening, Scottish couple in tartan dancing while others clap in a line, a handkerchief mid-air between them, candlelight and fiddle player visible in the background, warm Georgian-era illustration."
    },
    {
        "title": "Badger the Bear",
        "category": "folk-game",
        "subcategory": "chasing-game",
        "tags": ["rough-play", "outdoor", "teamwork", "role-play", "Victorian"],
        "difficulty": "intermediate",
        "players": "5+",
        "equipment": ["string or rope", "handkerchiefs or soft items to throw"],
        "family_friendly": True,
        "original_description": "One player is the Bear, on hands and knees and held by a string. A Keeper defends the Bear from the other players, who attack by pelting him with caps and handkerchiefs tied on strings. A player may only strike when the Keeper cries 'My Bear is free!' A striker who moves too early becomes the Bear.",
        "modern_description": "One player crouches as the Bear and is connected to another player (the Keeper) by a rope. The remaining players try to tag or lightly bop the Bear with soft items while the Keeper works to block and defend. The Keeper calls 'My Bear is free!' to signal a valid strike window. Anyone who strikes outside the signal must swap and become the Bear. The game rewards quick reflexes from attackers and clever guarding from the Keeper.",
        "fun_fact": "Bear-baiting games like this one were folk echoes of the real blood sport of bear-baiting, which was outlawed in Britain in 1835; children transformed the cruel spectacle into a boisterous playground game.",
        "image_prompt": "Victorian schoolyard, a boy crouching on all fours as the Bear while another defends him with arms spread wide, several children preparing to throw caps, autumn leaves on the ground, brick school building behind, energetic pen-and-ink sketch."
    },
    {
        "title": "Ball and Bonnets",
        "category": "folk-game",
        "subcategory": "chasing-game",
        "tags": ["ball", "chasing", "caps", "outdoor", "boys"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": ["ball", "caps or bonnets"],
        "family_friendly": True,
        "original_description": "Caps and bonnets are set in a row on the ground. A player throws a ball into one from a distance. The owner of that cap must run while the others chase until caught. The person caught then throws the ball. Any player who accumulates six stones in their cap receives 'buns'—light blows with the ball against the wall.",
        "modern_description": "Arrange all players' caps in a row on the ground. Players take turns throwing a ball from a set distance to land it in a cap. Whoever's cap the ball lands in must run, and all others chase. When caught, the caught player takes their turn throwing next. A running count of 'hits' is kept with pebbles in each cap; reaching six means facing a playful penalty.",
        "fun_fact": "This game and its close relative 'Ball in the Decker' were extremely popular in northern English schoolyards throughout the 1800s; teachers reportedly despaired at the number of hats damaged in play.",
        "image_prompt": "Victorian street with a row of flat caps laid on cobblestones, one boy winding up to throw a rubber ball, three boys poised to sprint, terraced houses lining the street, energetic late-afternoon scene."
    },
    {
        "title": "Banger",
        "category": "folk-game",
        "subcategory": "throwing-game",
        "tags": ["buttons", "throwing", "betting", "boys", "outdoor"],
        "difficulty": "beginner",
        "players": "2+",
        "equipment": ["buttons or coins", "wall"],
        "family_friendly": True,
        "original_description": "A button is laid near a wall. Other players snap their own buttons against the wall. Scoring depends on span distance or direct hits, with one to four points awarded. The first player to reach an agreed number of points wins all the staked buttons.",
        "modern_description": "One player places a button near a wall as the target. Players take turns snapping or flicking their buttons against the wall, scoring points based on how close their button lands to the target or whether they manage a direct hit. After each round, points are tallied (one point for close, four for a hit). First to the agreed total wins everyone's staked buttons. A simple game of skill that rewards a steady flicking finger.",
        "fun_fact": "Button-snapping games were enormously popular throughout the 18th and 19th centuries because buttons served as the small-denomination currency of childhood—winning meant accumulating a prized collection.",
        "image_prompt": "Two Victorian boys in waistcoats crouching near a brick wall, one flicking a button with thumb and forefinger, several buttons scattered on the ground between them, concentration on their faces, cobblestone street."
    },
    {
        "title": "Barbarie, King of the",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "role-play", "team-game", "drama", "breaking-through"],
        "difficulty": "intermediate",
        "players": "8+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Two children join hands as a fortress. A King stands at a distance with soldiers behind him. The soldiers surround the fortress and the two sides sing alternately: 'O will you surrender... / To the King of the Barbarie?' Soldiers try to break the clasped hands; the King finally succeeds, and his troop bursts through.",
        "modern_description": "Two players form a linked-hands 'fortress.' A player chosen as King leads a group of soldiers who surround the fortress. The two sides trade sung verses challenging each other. After the song, the soldiers attempt to break through the clasped fortress hands. The King has one special attempt to break through the gate. Once breached, the soldiers rush through; new fortress holders are chosen for the next round.",
        "fun_fact": "This game is related to the widespread 'Barca/Barcelona' group of games found across France, Spain, and Britain—its name likely refers to the Barbary Coast and reflects Elizabethan-era stories of pirates and sieges.",
        "image_prompt": "Victorian children outdoors, two forming a gate with linked hands while a group storms toward them singing, one child as 'King' leads the charge, summer afternoon, trees and a stone wall in the background, woodcut illustration."
    },
    {
        "title": "Barley-break",
        "category": "folk-game",
        "subcategory": "chasing-game",
        "tags": ["chasing", "couples", "team-game", "historical", "outdoor"],
        "difficulty": "intermediate",
        "players": "6",
        "equipment": ["marked ground area"],
        "family_friendly": True,
        "original_description": "Six players in three couples. The ground is divided into three compartments, the middle one called 'Hell.' The couple in Hell tries to catch players from the end zones; they cannot separate until a catch is made. Caught players swap to Hell. The last couple remaining in Hell loses.",
        "modern_description": "Six players pair up into three couples. Mark out three equal zones; the middle zone is 'Hell.' The couple in Hell joins hands and tries to catch players who dash between the two outer zones. The Hell couple cannot split apart until they make a catch. Caught pairs swap into Hell. This continues until one unlucky couple has been in Hell the longest—they are the losers. Strategy involves timing dashes to stretch and split the Hell couple.",
        "fun_fact": "Barley-break is one of England's oldest documented games, described by Sir Philip Sidney in the 1580s and mentioned by numerous Elizabethan poets; it was typically played by mixed groups of young men and women at harvest time.",
        "image_prompt": "Elizabethan-style illustration of three couples playing in a barley field, one couple in the center zone reaching to catch a fleeing pair, golden wheat in the background, warm harvest-festival atmosphere."
    },
    {
        "title": "Bedlams (Relievo)",
        "category": "folk-game",
        "subcategory": "chasing-game",
        "tags": ["chasing", "team-game", "den", "outdoor", "Victorian"],
        "difficulty": "intermediate",
        "players": "6+",
        "equipment": ["chalk for drawing den"],
        "family_friendly": True,
        "original_description": "Sides are picked; a chalk square called the 'Den' is drawn. A 'Tenter' guards the Den with one foot inside. Fielders run to a distance, shout 'Relievo!' and are pursued back to the Den. If a fielder breaks through untouched and calls 'Relievo,' all prisoners are freed.",
        "modern_description": "Draw a chalk square as the Den. One team is the fielders, the other guards. The chief guard (Tenter) must keep one foot in the Den at all times. Fielders dash away from the Den and call 'Relievo!' to taunt pursuers. Guards chase; tagged fielders go to jail inside the Den. A free fielder who manages to reach the Den and shout 'Relievo!' without being tagged frees all prisoners instantly. Play until all fielders are captured.",
        "fun_fact": "Relievo (also Relievo, Prisoner's Base, or Bedlams) was declared illegal in the streets of London by a statute of Edward III in 1332, suggesting it was already ancient and caused chaos in public thoroughfares.",
        "image_prompt": "Victorian park scene with chalk square drawn on path, one boy guarding the Den with other boys as prisoners inside, a free boy sprinting toward them arms raised to shout Relievo, afternoon sun, pen and ink with wash."
    },
    {
        "title": "Bell-horses",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "marching", "counting", "children", "procession"],
        "difficulty": "beginner",
        "players": "3+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Players form trains, one behind another, and march and sing: 'Bell-horses, bell-horses, what time of day? / One o'clock, two o'clock, three, and away!' At the word 'away,' all run or scatter, then reform for the next verse with a higher count.",
        "modern_description": "Players line up in a 'train' with hands on the shoulders of the person in front. The group marches together chanting the verse, counting up one hour with each round. When the final word 'away' is sung, everyone breaks the chain and scatters, then quickly reforms the train to start again at the next hour. A perfect game for young children learning to count.",
        "fun_fact": "Bell-horses was traditionally sung to the rhythm of horses' hooves and trotting—many Victorian nursery rhymes were paced to common transport sounds that every child in the era would have heard daily.",
        "image_prompt": "Four small children in a line with hands on each other's shoulders marching through a garden path singing, flowers bordering the path, warm sunlight, simple watercolor illustration in nursery-book style."
    },
    {
        "title": "Betsy Bungay",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "carrying", "partner-game", "rough-play", "children"],
        "difficulty": "beginner",
        "players": "3",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Two children cross hands to form a 'sedan chair.' A third child sits on their clasped hands. They sing 'Hi, Betsy Bungay, all day on Sunday; / You're the lock and I'm the key, / All day on Monday'—then unclasp their hands, dropping the seated child.",
        "modern_description": "Two players face each other and cross their wrists, gripping each other's wrists to form a seat. A third player carefully sits on the clasped hands and holds onto the bearers' shoulders. The trio sings the Betsy Bungay verse together. At the last line, the two bearers release their grip simultaneously, gently lowering the seated player. Take turns being the one carried.",
        "fun_fact": "The 'sedan chair' hand-grip appears in countless folk games across Britain and Ireland; before wheeled vehicles were common, being carried in a chair was a symbol of wealth and status that children loved to mimic.",
        "image_prompt": "Three Victorian children outdoors, two facing each other with wrists crossed forming a seat, a smaller child balanced on their arms grinning, all singing, village green setting, pastel illustration."
    },
    {
        "title": "Bingo",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "ring-game", "spelling", "children", "dog"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Children form a ring with one in the centre. They dance and sing the famous verse, and the centre child points to players at each letter: 'The farmer's dog lay on the barn floor / And Bingo was his name-O! / B-I-N-G-O, B-I-N-G-O, B-I-N-G-O, / And Bingo was his name-O!' The pointed-at player for a wrong letter must swap to the centre.",
        "modern_description": "Players stand in a circle with one child in the middle. Everyone sings the Bingo verse together, and with each letter (B-I-N-G-O) the centre player points to someone in the ring. If the pointed-at player correctly calls out their letter on cue, the game continues. A miss means that player must take their turn in the center. A variant has players progressively clapping in place of each letter as it is gradually silenced.",
        "fun_fact": "The Bingo song predates the lottery game of the same name by at least a century; the earliest recorded versions appear in Scottish and northern English folk collections from the 1780s.",
        "image_prompt": "Circle of Victorian children on a village green, one child in the center pointing outward, all mouths open in song, sunny afternoon, the child being pointed at looking delighted, warm watercolor illustration."
    },
    {
        "title": "Bird-apprentice",
        "category": "folk-game",
        "subcategory": "guessing-game",
        "tags": ["guessing", "birds", "chasing", "two-teams", "children"],
        "difficulty": "beginner",
        "players": "8+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Two parallel rows of children face each other. The first row secretly chooses bird names for each member. The second row calls out bird names; when the first row's matching member is named, both rows run to swap places. Any player caught must carry the catcher on their back.",
        "modern_description": "Divide into two equal rows facing each other. Row A secretly whispers a different bird name to each player. Row B takes turns calling out bird names. When a player from Row A hears their bird called, all players make a dash to swap rows. Anyone tagged during the crossing must give the tagger a piggyback ride before the next round. Birds that aren't called stay put. Play until all birds have been named.",
        "fun_fact": "This game is closely related to the French game 'Qui a peur du loup?' and was used by Victorian schoolteachers as a way of teaching children the names of common British birds.",
        "image_prompt": "Two rows of Victorian schoolchildren facing each other in a sunny schoolyard, one child from the left row mid-sprint across the gap, hands outstretched, others about to follow, school building in the background."
    },
    {
        "title": "Black Man's Tig",
        "category": "folk-game",
        "subcategory": "chasing-game",
        "tags": ["chasing", "rope", "chain-game", "outdoor", "children"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": ["rope tied to a gate or pole"],
        "family_friendly": True,
        "original_description": "A rope is tied to a gate or pole. One player holds the free end and tries to catch another. Anyone captured joins the chain by holding hands with the catcher; they help catch the rest. The game ends when all players have been caught and form one long chain.",
        "modern_description": "Attach a rope to a fixed post. The first catcher holds the rope's free end and chases others. When someone is tagged, they join hands with the catcher, lengthening the chain. The chain must stay connected as it tries to encircle and tag the remaining free players. The last person caught wins the right to be the first catcher in the next game.",
        "fun_fact": "Chain-tag games of this type appear across Britain, North America, and Australia under many names; the connecting element (rope, hands, or cloth strip) serves to handicap the catchers and give free runners a sporting chance.",
        "image_prompt": "Victorian children in a park, a chain of four holding hands stretching to surround a laughing free runner, rope attached to an iron park railing at one end, autumn trees in the background, lively pen-and-ink sketch."
    },
    {
        "title": "Black Thorn",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "catching", "two-teams", "dialogue", "children"],
        "difficulty": "intermediate",
        "players": "8+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Two sides stand opposite each other, one against a wall. They sing a challenge-and-response dialogue: 'Blackthorn! / Butter-milk and barley-corn; / How many geese have you to-day?' After the verses are exchanged, both sides rush to catch players from the opposite team. The last player caught joins the winning team.",
        "modern_description": "Divide into two equal groups facing each other about ten paces apart. Groups take turns chanting lines of the Blackthorn dialogue, each reply growing more taunting. On the final verse, everyone dashes across to catch members of the opposing team before they can reach a safe zone. Caught players join the capturing team. Play continues until one side has everyone.",
        "fun_fact": "The 'Blackthorn' dialogue is among the oldest documented in British folk games—similar challenge rhymes appear in medieval manuscript collections, showing how such games preserved archaic language for centuries.",
        "image_prompt": "Two groups of Victorian children facing each other on a village green, mouths open mid-chant, about to spring into a chase, stone wall behind one group, hedgerows on either side, dramatic and energetic composition."
    },
    {
        "title": "Blind Bell",
        "category": "folk-game",
        "subcategory": "blindfold-game",
        "tags": ["blindfold", "chasing", "bell", "children", "outdoor"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": ["blindfolds", "small bell"],
        "family_friendly": True,
        "original_description": "All players are blindfolded except one, the 'Bell,' who rings a small bell while evading everyone. The blindfolded players try to catch the Bell player by following the sound. When caught, the caught player takes the bell, has their blindfold removed, and the catcher is blindfolded instead.",
        "modern_description": "Blindfold all players except one who holds a ringing bell. The Bell player moves around a defined space, ringing to attract and confuse the blindfolded chasers. The blindfolded players must navigate by sound only to tag the Bell player. When tagged, the successful catcher removes their blindfold and becomes the new Bell; the old Bell is blindfolded. A wonderful exercise in listening and spatial awareness.",
        "fun_fact": "Variations of this game were used in Victorian parlors as 'scientific' experiments in how humans navigate by sound alone, often discussed in popular science magazines of the era.",
        "image_prompt": "Victorian parlor, five children in white blindfolds reaching with arms outstretched, one child in the center ringing a brass bell and grinning, soft lamplight, ornate wallpaper, warm and playful atmosphere."
    },
    {
        "title": "Blind Man's Stan",
        "category": "folk-game",
        "subcategory": "blindfold-game",
        "tags": ["blindfold", "stick", "eggs", "skill", "outdoor"],
        "difficulty": "intermediate",
        "players": "3+",
        "equipment": ["blindfold", "stick", "small objects to balance on ground"],
        "family_friendly": True,
        "original_description": "A blindfolded player must slap the ground three times with a stick, trying to strike small 'bird eggs' (pebbles or similar items) placed on the ground. Other players may mislead the blindfolded one about where the targets are.",
        "modern_description": "Place several small pebbles or objects (representing eggs) on the ground in a cluster. Blindfold one player and hand them a stick. Spin them gently three times, then let them swing the stick three times at ground level trying to hit the pebbles. Other players may call out misleading directions. Count how many objects are hit—the player with the highest count across several turns wins.",
        "fun_fact": "This game and similar 'blind stick' games were precursors to the piñata tradition; the combination of blindfolding and striking an unseen target appears in folk celebrations across many cultures simultaneously.",
        "image_prompt": "Victorian country garden, a blindfolded child swinging a stick at pebbles on the grass, two other children pointing in wrong directions to mislead them, laughing, stone garden wall behind, bright afternoon."
    },
    {
        "title": "Booman",
        "category": "folk-game",
        "subcategory": "dramatic-game",
        "tags": ["singing", "dramatic", "funeral", "ring-game", "children"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": ["flowers (optional)"],
        "family_friendly": True,
        "original_description": "One player lies as the Booman while the ring of children circles round with boys raising and lowering hands like ringing bells and girls weeping. They carry him to a pretend grave, strew flowers, and sing: 'Dill doule for Booman... / Where shall we bury him? / Dig his grave...' Then a new Booman takes their place.",
        "modern_description": "One player lies still on the ground as the 'Booman' (the dead man). The others circle, boys mimicking bell-ringing with raised arms and girls pretending to weep, all singing the funeral verse. The group mimes carrying the Booman to a pretend grave, strewing flowers (or petals), and saying farewell. Then the Booman springs up and someone else lies down. A dramatic and theatrical game that lets children act out an elaborate story.",
        "fun_fact": "Booman games preserve ancient folk rituals of mock-burial that were common at spring festivals across Celtic Britain; the singing and 'resurrection' at the end links the game to pre-Christian seasonal rebirth ceremonies.",
        "image_prompt": "Circle of Victorian children around a child lying on the grass, the others in poses of mock grief, some with flowers, one boy with arms raised like a bell-ringer, soft green meadow setting, charming and slightly melancholy watercolor."
    },
    {
        "title": "Boss-out (Marbles)",
        "category": "folk-game",
        "subcategory": "marbles-game",
        "tags": ["marbles", "aim", "outdoor", "boys", "skill"],
        "difficulty": "beginner",
        "players": "2+",
        "equipment": ["marbles"],
        "family_friendly": True,
        "original_description": "One player bowls a marble as a mark. The next player bowls to hit it or to come within a hand-span of it. A hit wins the mark marble; otherwise players alternate until someone wins. This is one of the simplest forms of Victorian marble combat.",
        "modern_description": "Player one rolls a marble along the ground as the target. Player two rolls their marble trying either to hit the target marble directly (winning it immediately) or to land within a hand-span of it. If neither succeeds, continue alternating. A direct hit always wins the target. If after several rounds a player's marble lands a hand-span or less away, they win on the next successful close-up shot. Simplest of the Victorian marble-battle games.",
        "fun_fact": "The 'span' measurement—the width of a hand from pinky to thumb—was the universal Victorian unit for marble proximity disputes; arguments about whether a marble 'spanned' were reportedly the most common cause of schoolyard arguments.",
        "image_prompt": "Two Victorian boys kneeling on a dirt schoolyard, one mid-flick shooting a marble toward another marble on the ground, faces intent, other marbles scattered around, brick school building wall behind, pen and ink."
    },
    {
        "title": "Bridgeboard",
        "category": "folk-game",
        "subcategory": "marbles-game",
        "tags": ["marbles", "board", "holes", "scoring", "children"],
        "difficulty": "beginner",
        "players": "2+",
        "equipment": ["board with numbered holes", "marbles"],
        "family_friendly": True,
        "original_description": "A board about one foot by four inches with squares or holes numbered irregularly is laid at ground level at the edge of a wall. Players bowl marbles trying to pass them through a hole; if successful, they win the number of marbles denoted by that hole. A marble that misses is lost to the board owner.",
        "modern_description": "Prop up a small board with several numbered arches or holes cut into its base. Players take turns rolling marbles from a set distance, aiming to pass their marble through one of the holes. Successfully threading a hole wins that many marbles from the house. Failing to hit any hole means losing your marble to the house player. The board owner can make a profit by setting the odds cleverly.",
        "fun_fact": "Bridgeboard was a fixture at Victorian street fairs and school gates; enterprising children would build their own boards from scrap timber and run them as tiny gambling enterprises for marbles.",
        "image_prompt": "Victorian street corner, a boy kneeling with a marble board propped against a wall, numbered holes along the base, another boy taking aim from a chalk line, small crowd of children watching, cobblestones."
    },
    {
        "title": "Buck, Buck",
        "category": "folk-game",
        "subcategory": "guessing-game",
        "tags": ["guessing", "riding", "fingers", "outdoor", "boys"],
        "difficulty": "beginner",
        "players": "3+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "One player stoops and the rider sits on their back, holding up some fingers. The stooper must guess 'Buck, buck, how many horns do I hold up?' Wrong guesses mean the stooper must carry the rider again. Correct guess swaps roles. Variants include post-and-stooper lines where a rider leaps back-to-back asking the count.",
        "modern_description": "One player (the Buck) bends over and a second player sits lightly on their back holding up some fingers. The Buck must guess 'how many horns?' If wrong, they carry the rider again. If right, they swap roles. In a line variant, several players stoop while a rider leaps from back to back asking each stooper the riddle; any wrong guess means the rider starts fresh from the beginning.",
        "fun_fact": "Buck Buck is found in nearly identical form in ancient Roman children's games described by the poet Horace, making it one of the oldest continuously played games in Western history.",
        "image_prompt": "Victorian schoolyard, one boy bent over with another sitting on his back holding up fingers, the stooping boy peering over his shoulder to guess, other boys watching and laughing, chalk drawings on the school wall behind."
    },
    {
        "title": "Bull in the Park",
        "category": "folk-game",
        "subcategory": "breaking-game",
        "tags": ["ring-game", "breaking-through", "chasing", "outdoor", "children"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "One child stands in the centre circle as the Bull. Asking 'Where's the key of the park?' each child in the ring replies 'Ask next-door,' except the last child who answers 'Get out the way you came in.' The Bull then dashes at the ring's hands trying to break through; whoever the Bull catches becomes the new Bull.",
        "modern_description": "Players stand in a circle holding hands with one player (the Bull) in the center. Going around the ring, the Bull asks each player 'Where's the key of the park?' Each player replies 'Ask next-door' until the last, who answers 'Get out the way you came in!' The Bull then charges at any weak point in the ring, trying to break through the linked hands. The player whose grip breaks and lets the Bull through becomes the new Bull.",
        "fun_fact": "The 'Bull in the Ring' theme connects to ancient agricultural games played at cattle fairs; the image of a bull escaping an enclosure was both familiar and thrilling to Victorian children who grew up around livestock.",
        "image_prompt": "Victorian children in a park forming a tight hand-holding circle, one determined child in the center charging toward the weakest point, other children straining to hold their grip, green park with iron railings behind, dynamic illustration."
    },
]

# Add Gomme 1 entries
for e in gomme1_entries:
    if not is_duplicate(e['title']):
        entry_id = make_id(e['title'])
        e['id'] = entry_id
        e['slug'] = entry_id
        e['source_book'] = "The Traditional Games of England, Scotland, and Ireland, Vol. I"
        e['source_author'] = "Alice Bertha Gomme"
        e['source_year'] = 1894
        e['source_url'] = "https://www.gutenberg.org/ebooks/41727"
        all_entries.append(e)

print(f"After Gomme Vol 1: {len(all_entries)} entries")

# ============================================================
# GOMME VOL. II (1898) - Traditional Games Vol. II
# ============================================================
gomme2_entries = [
    {
        "title": "Oats and Beans and Barley",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "ring-game", "farming", "partner-choosing", "marriage-game"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Players form a ring with one child in the centre who mimes farming actions as the ring walks round singing: 'Oats and beans and barley grow! / Does you or I or anyone know / How oats and beans and barley grow?' At 'Open the ring and take one in,' the centre child chooses a partner. The ring then sings the marriage formula.",
        "modern_description": "One child stands in the center of a ring of players who walk around singing. At specific words, everyone mimes sowing seed, stamping a foot, clapping hands, and turning around. When the verse reaches 'open the ring and take one in,' the center child picks a partner from the ring. The pair stands together while everyone sings a wedding blessing. The first center child rejoins the ring and the new partner becomes the chooser.",
        "fun_fact": "This game is recorded in more than 18 regional variants across England and Scotland, making it one of the most widely distributed folk games in British tradition; it preserves the language and gestures of medieval strip-farming.",
        "image_prompt": "Children in a ring in a barley field, one child in the center miming sowing seeds, the ring moving slowly clockwise, singing, golden crop and rolling hills in the background, pastoral watercolor illustration."
    },
    {
        "title": "Old Roger is Dead",
        "category": "folk-game",
        "subcategory": "dramatic-game",
        "tags": ["singing", "dramatic", "ring-game", "death", "apples", "children"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "A ring forms around 'Roger' lying in the centre. The ring sings verses while different children step in to play an apple tree and an old woman picking apples. Roger then jumps up and chases the old woman, knocking her out: 'Old Roger is dead... / apple tree over his head... / Old woman a-picking 'em up... / Roger jumped up and gave her a knock... / hipperty hop.'",
        "modern_description": "One child plays Roger and lies still in the center. The ring walks around singing. When the apple tree verse comes, one child enters and raises their arms as branches. At the old woman verse, another child enters and mimes picking apples. At the climax, Roger leaps up and 'bumps' the apple-picker gently, who then hops away comically. Three new players take the roles in the next round.",
        "fun_fact": "Old Roger is Dead is one of Britain's most widespread folk songs with over a dozen documented regional variants; scholars believe it preserves an ancient harvest-spirit narrative where the dead grain spirit revives to chase away autumn.",
        "image_prompt": "Ring of Victorian children around a boy lying on the grass, one child with arms raised as the apple tree, another pretending to pick apples, the 'dead' boy about to leap up, autumn orchard setting, charming book illustration style."
    },
    {
        "title": "Old Dame",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "counting", "chasing", "role-play", "time"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": ["stool"],
        "family_friendly": True,
        "original_description": "One child (the Old Dame) sits on a stool while others march round in file, asking the time. The Dame answers with an increasing hour from one to eleven; at twelve she cries they'll be hanged! All run and the Dame chases; whoever is caught becomes the new Dame. In Yorkshire: 'I'll away to t'beck... It's one, and you'll be hanged at two.'",
        "modern_description": "One player sits on a chair or stool as the Old Dame. The others march in a circle and sing, asking the Dame what time it is. The Dame answers with progressively higher numbers—one o'clock, two o'clock, and so on. At twelve o'clock, the Dame jumps up and shouts a warning, and everyone runs. Whoever the Dame catches first becomes the new Dame. A counting game with a delightful surprise ending.",
        "fun_fact": "Old Dame is the British counterpart to 'What's the Time, Mr Wolf?' and has been collected across Yorkshire, Suffolk, and East Anglia; some versions extend the dialogue to include fetching firewood, lighting a kettle, and feeding chickens.",
        "image_prompt": "Victorian parlor, one child sitting imperiously on a chair as the Old Dame, others marching around her in single file singing, tension on their faces as the count nears twelve, fireplace and dark wallpaper behind."
    },
    {
        "title": "Old Soldier",
        "category": "folk-game",
        "subcategory": "forfeit-game",
        "tags": ["forfeit", "role-play", "avoidance", "wordplay", "Victorian"],
        "difficulty": "intermediate",
        "players": "5+",
        "equipment": ["walking stick (optional)"],
        "family_friendly": True,
        "original_description": "One player acts as an old soldier limping with a stick, begging garments. He asks 'Have you got anything to give an old soldier?' The challenged player must answer without using Yes, No, Nay, Black, White, or Grey—taboo words that trigger a forfeit. The soldier walks lame and fires rapid questions to catch players off guard.",
        "modern_description": "One player limps around as the Old Soldier, approaching each player in turn with begging questions. The answering player must respond sensibly without using the forbidden words: Yes, No, Nay, Black, White, or Grey. Any slip means a forfeit (a small task or penalty). The Soldier tries to trick players with fast, confusing questions. The last player to remain clean-spoken wins.",
        "fun_fact": "Forbidden-word games appear in documents from ancient Greece through medieval Europe; the 'taboo words' in Victorian versions were usually chosen to be extremely common words, making avoidance genuinely difficult.",
        "image_prompt": "Victorian drawing room, one boy in a battered tricorn hat and cape limping with a stick, approaching a girl seated on a chair who is trying to answer carefully, other children watching eagerly for mistakes, candlelit evening."
    },
    {
        "title": "Obadiah",
        "category": "folk-game",
        "subcategory": "cumulative-game",
        "tags": ["cumulative", "memory", "action", "chain-game", "East Anglia"],
        "difficulty": "intermediate",
        "players": "5+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Players stand in a row. The head child says 'My son Obadiah is going to be married, twiddle your thumbs.' All twiddle thumbs. The next adds 'Fall on one knee'—all do so, still twiddling. Instructions stack up; as the last child repeats the first instruction, the first falls onto the next, all collapsing like ninepins.",
        "modern_description": "Players stand in a row and a leader announces the first action: 'My son Obadiah is going to be married, twiddle your thumbs.' Everyone does so. Moving down the line, each player adds a new action while all previous actions are maintained simultaneously. Actions stack until everyone is twiddling thumbs, standing on one knee, shaking their head, and more—when the cascade of actions becomes impossible, all collapse in hilarious failure.",
        "fun_fact": "This cumulative action game is unique to East Anglia and is closely related to 'Solomon Says'—the collapse-like-ninepins ending is a rare physical comedic climax found in very few other folk games.",
        "image_prompt": "Row of Victorian children in increasingly awkward poses—twiddling thumbs, on one knee, head shaking—the leftmost about to collapse onto the next, all struggling to maintain multiple actions simultaneously, comic illustration."
    },
    {
        "title": "Oliver, Oliver, Follow the King",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "ring-game", "naming", "courtship", "children"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "A ring moves round singing 'Oliver, Oliver, follow the King!' then curtseys or bobs down. The last player in line names their sweetheart. The ring continues singing, inserting the named children: 'Jim Burguin wants a wife... Nelly he kissed... made a pudding... wedding-day...'",
        "modern_description": "Players move in a ring and sing the verse. At the curtsey, all bow or dip. The last player in line names a real or imaginary sweetheart. The ring incorporates these names into the ongoing song, adding verses about the named couple kissing, making pudding, and setting a wedding day. The game gathers characters as it goes, becoming a comically elaborate romance narrative.",
        "fun_fact": "This game appears closely related to 'All the Boys' and 'Down in the Valley'—the naming and courtship pattern is typical of 'kissing ring' games that let children safely practice social pairing within a community context.",
        "image_prompt": "Victorian children in a flower-garlanded ring, all dipping in a curtsey, one girl at the back whispering a name into another's ear, smiling faces, sunny village green, illustrated in the manner of Kate Greenaway."
    },
    {
        "title": "Paddy from Home",
        "category": "folk-game",
        "subcategory": "ring-passing-game",
        "tags": ["guessing", "ring-passing", "string", "hiding", "children"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": ["string", "small ring"],
        "family_friendly": True,
        "original_description": "Players hold a long loop of string with a small ring threaded onto it. They pass the ring secretly from hand to hand while the centre child tries to guess who holds it. The group sings: 'Paddy from home has never been... travels along the railway.'",
        "modern_description": "Thread a small ring onto a large loop of string. Everyone except one player holds the loop. The ring is secretly slid from hand to hand behind cupped palms, hidden from the guesser in the center. The group sings the Paddy verse to distract the guesser. The center player must point to who they think holds the ring at any moment; a correct guess swaps roles.",
        "fun_fact": "Ring-on-string passing games are documented from ancient Rome (where a ring was passed to predict the future bride's name) through every century of European history—the 'railway' in this Victorian version updates a very old game.",
        "image_prompt": "Circle of Victorian children holding a string loop, all concentrating on secretly passing a small ring, one child in the center watching intently for the telltale movement of the hidden ring, parlor setting."
    },
    {
        "title": "Peg-in-the-Ring",
        "category": "folk-game",
        "subcategory": "top-game",
        "tags": ["tops", "spinning", "ring", "outdoor", "boys"],
        "difficulty": "intermediate",
        "players": "3+",
        "equipment": ["spinning tops", "chalk circle"],
        "family_friendly": True,
        "original_description": "A chalk circle is drawn; players must spin their top inside the circle without the top exhausting or stepping outside. If a top fails to stay spinning inside the ring, it is left for others to peg with their own tops. Calls of 'One a penny! Two a penny! Three a penny, good as any!' signal which stake is being played.",
        "modern_description": "Draw a large chalk circle on a flat surface. Players take turns spinning their tops inside the ring. A top must keep spinning without crossing the boundary. Any top that stops or rolls out is left in the ring as a target—other players try to strike the stationary top with their own spinning top. The owner of a struck top loses it. Last player with a top wins.",
        "fun_fact": "Peg-top and ring games were so popular in Victorian England that specialist top-makers sold tops with iron pegs designed specifically for combat spinning; a well-balanced top was a treasured possession.",
        "image_prompt": "Victorian schoolyard, chalk circle on the ground with two spinning tops inside, boys in caps watching intently, one winding up his top on a string to launch, sunny morning, brick wall behind."
    },
    {
        "title": "Pi-cow",
        "category": "folk-game",
        "subcategory": "castle-assault-game",
        "tags": ["chasing", "castle", "foraging", "teams", "signal"],
        "difficulty": "intermediate",
        "players": "8+",
        "equipment": ["marked territory"],
        "family_friendly": True,
        "original_description": "Half the players keep the castle; the others forage. A sentinel calls 'Pee-ku' to alert castle defenders of approaching foragers. If a forager enters the castle without capture, he calls 'The hole's won!' and the guards yield. Captured foragers switch sides. The game can also be played as Hide and Seek.",
        "modern_description": "Divide into defenders and foragers. Designate a 'castle' area. Foragers try to infiltrate the castle without being tagged; a lookout in the castle calls 'Pee-ku!' when they spot an approaching forager, alerting the guards. A forager who reaches the castle's center and shouts 'The hole's won!' wins the round and the defenders must concede. Tagged foragers switch teams. Play until one team has everyone.",
        "fun_fact": "Pi-cow is a survival of the ancient 'King of the Castle' game family; the sentinel's warning cry 'Pee-ku' is likely derived from 'peek-a-boo,' giving us a direct etymological link between a baby game and a complex team sport.",
        "image_prompt": "Victorian children in a park, some crouching behind a stone wall as the castle, one acting as lookout with hand over eyes, others crawling through tall grass trying to infiltrate, tense and stealthy atmosphere."
    },
    {
        "title": "Pinny Show",
        "category": "folk-game",
        "subcategory": "peep-show",
        "tags": ["peep-show", "performance", "flowers", "pin-admission", "Victorian"],
        "difficulty": "beginner",
        "players": "2+",
        "equipment": ["framed paper with viewing slit", "flowers", "glass", "pins"],
        "family_friendly": True,
        "original_description": "A small show is constructed with flowers or colors arranged under glass, framed in paper with a viewing slit. Admission is charged in pins—a pin to peep. The showman cries: 'A pin to see the poppet-show, / All manner of colours oh! / See the ladies all below.'",
        "modern_description": "Build a tiny show box from a shoe box with a small viewing hole. Arrange flowers, colored paper scraps, or small figures inside, lit through a hole in the top. The showman charges one pin for each peep. Viewers look through the slit and see a miniature arranged scene. A charming entrepreneurial game for children who want to create as well as play.",
        "fun_fact": "The pinny show was the Victorian child's equivalent of the cinema—peep-show boxes were enormously popular throughout the 18th and 19th centuries, and their miniature dramas introduced thousands of children to the concept of a theatrical stage.",
        "image_prompt": "Victorian girl kneeling by a small decorated box on the ground, another girl stooping to peer through a slit in the side, colorful flowers visible inside through the top opening, sunny afternoon, charming illustration."
    },
    {
        "title": "Poor Mary Sits A-weeping",
        "category": "folk-game",
        "subcategory": "singing-game",
        "tags": ["singing", "ring-game", "weeping", "partner-choosing", "marriage"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "One player sits weeping in the centre of the ring. The ring sings and asks why she weeps. She names a reason—sweetheart lost, father dead. She is told to choose a lover, be married, and kiss. Documented in twenty regional variants: 'Poor Mary sits a-weeping, a-weeping, a-weeping... on a bright summer's day.'",
        "modern_description": "One player sits in the center of the ring pretending to cry. The ring moves around singing and asking why Mary weeps. When prompted, Mary names what she weeps for. The ring then instructs her to 'choose a lover from the ring'—she picks someone, they meet in the center, and the verse ends with them bowing or kissing. The chosen partner becomes the new center player.",
        "fun_fact": "This game is documented in more than 20 regional versions with names including Sally, Sarah, Nellie, and Jennie—showing how folk songs absorb local names while preserving their essential ritual structure over centuries.",
        "image_prompt": "Victorian children's ring game, one girl sitting center stage with face buried in hands, the circling children singing with gestures, sunny green lawn, Kate Greenaway-style illustration with bonnets and pinafores."
    },
    {
        "title": "Pize Ball",
        "category": "folk-game",
        "subcategory": "ball-game",
        "tags": ["ball", "batting", "rounders", "teams", "outdoor"],
        "difficulty": "intermediate",
        "players": "8+",
        "equipment": ["ball", "bats", "marked bases"],
        "family_friendly": True,
        "original_description": "Sides of six face off; each side has marks (bases) and tuts. A batter at home pizes (strikes) the ball and runs to the tut; if hit by the thrown ball while running, they are 'burnt' and out. A precursor to modern rounders and baseball.",
        "modern_description": "Set up a home base and one or more running stations (tuts). The batter hits the ball and runs to the tut before the fielders can retrieve the ball and throw it to hit the runner. A runner hit by the ball while running between bases is out. Teams rotate after a set number of outs. This direct ancestor to rounders and baseball preserves the original British fielding-and-batting format.",
        "fun_fact": "Pize Ball is one of the earliest documented batting-and-running games in British records; its direct relationship to modern baseball was first argued by scholars in the 1990s, lending this Victorian schoolyard game unexpected historical significance.",
        "image_prompt": "Victorian village green, one child at bat striking a ball, two children in the field chasing it, another running to a chalk mark on the grass, excited crowd of children watching from the boundary, summer afternoon."
    },
    {
        "title": "Plum Pudding",
        "category": "folk-game",
        "subcategory": "marbles-game",
        "tags": ["marbles", "shooting", "aim", "outdoor", "boys"],
        "difficulty": "beginner",
        "players": "2+",
        "equipment": ["marbles"],
        "family_friendly": True,
        "original_description": "A row of marbles is set up at a taw (shooting) mark. Players shoot from a distance to knock marbles out of the row; each marble knocked out is kept. Play continues until all marbles are won.",
        "modern_description": "Line up an agreed number of marbles in a row at one end. Players take turns shooting their shooter marble (the taw) from a line at the opposite end, trying to knock marbles out of the row. Any marble dislodged from its position is won by the shooter. Play until the row is empty; whoever has collected the most marbles wins.",
        "fun_fact": "Plum Pudding was one of the most popular marble games in Victorian Britain because it required no circle-drawing or complex setup—just a row of marbles and a clear shot, making it ideal for any flat surface.",
        "image_prompt": "Four Victorian boys crouching in a row on a cobbled street, a line of marbles visible at the far end, one boy squinting and taking aim with his shooter, other marbles already claimed in a small pile beside him."
    },
    {
        "title": "Pitch and Toss",
        "category": "folk-game",
        "subcategory": "coin-game",
        "tags": ["coins", "tossing", "chance", "boys", "betting"],
        "difficulty": "beginner",
        "players": "2+",
        "equipment": ["coins or lead discs"],
        "family_friendly": True,
        "original_description": "Players throw lead pitchers or coins to a mark; whoever lies closest piles the others' coins and tosses them. Heads showing face-up are won. The closest coin gets first toss rights; others follow by proximity. Scores are kept by freed status and button payments.",
        "modern_description": "Set a mark on the ground. Players take turns throwing a coin toward the mark. The player whose coin lands closest picks up all coins, stacks them, and tosses them into the air. All coins landing heads-up are won by the tosser; tails go back to their owners. Remaining tails are tossed by the next closest player, and so on. Simple, social, and entirely based on chance.",
        "fun_fact": "Pitch and Toss has been recorded under various names across Britain since at least the 17th century and was so pervasive that the Metropolitan Police Act of 1839 specifically prohibited it in London's public streets.",
        "image_prompt": "Victorian alley, three boys in caps crouched over a chalked mark on the stone pavement, coins scattered on the ground, one boy mid-toss flipping a stack of pennies into the air, gaslight casting long shadows."
    },
]

for e in gomme2_entries:
    if not is_duplicate(e['title']):
        entry_id = make_id(e['title'])
        e['id'] = entry_id
        e['slug'] = entry_id
        e['source_book'] = "The Traditional Games of England, Scotland, and Ireland, Vol. II"
        e['source_author'] = "Alice Bertha Gomme"
        e['source_year'] = 1898
        e['source_url'] = "https://www.gutenberg.org/ebooks/41728"
        all_entries.append(e)

print(f"After Gomme Vol 2: {len(all_entries)} entries")

# ============================================================
# CARROLL - The Game of Logic (1887)
# ============================================================
carroll_entries = [
    {
        "title": "The Game of Logic",
        "category": "board-game",
        "subcategory": "logic-game",
        "tags": ["logic", "syllogisms", "counters", "diagram", "Lewis Carroll", "educational"],
        "difficulty": "advanced",
        "players": "1-2",
        "equipment": ["cardboard diagram (smaller 2x2 and larger 3-attribute)", "4 red counters", "5 grey counters"],
        "family_friendly": True,
        "original_description": "The player uses a cardboard diagram divided into four compartments (x, x', y, y') and nine counters—four red for 'SOME' and five grey for 'NO'—to represent logical propositions about any chosen Universe (Cakes, Animals, etc.). By placing counters on the diagram according to two premisses, one reads off the logical conclusion. 'Red on a compartment: SOME things are there; grey: NONE are there.' The larger diagram adds a middle term (m) to allow full syllogisms.",
        "modern_description": "Choose a Universe—say, Cakes. Assign two attributes to the diagram's axes (new/not-new, nice/not-nice). Each of two given logical statements is 'drawn' on the larger diagram using counters. Grey counters mark compartments proved empty; red counters mark compartments known to have occupants. Transfer the result to the smaller diagram and read off the conclusion. Can be played solo (check your answers against the book's key) or with a partner who challenges you with premiss pairs. The game teaches formal logic through tactile play.",
        "fun_fact": "Lewis Carroll invented this board game in 1886 while trying to make Aristotelian logic accessible to his child friends; the book includes 101 amusing conversational extracts from real life translated into syllogism form, including gems like 'All pigs are fat; No skeletons are fat' concluding 'All pigs are not-skeletons.'",
        "image_prompt": "Victorian study table with a small cardboard diagram divided into four squares, red and grey counters arranged on it, Lewis Carroll's Game of Logic book open beside it, quill pen and ink bottle nearby, soft candlelight, detailed realistic illustration."
    },
]

for e in carroll_entries:
    if not is_duplicate(e['title']):
        entry_id = make_id(e['title'])
        e['id'] = entry_id
        e['slug'] = entry_id
        e['source_book'] = "The Game of Logic"
        e['source_author'] = "Lewis Carroll"
        e['source_year'] = 1887
        e['source_url'] = "https://www.gutenberg.org/ebooks/4763"
        all_entries.append(e)

print(f"After Carroll: {len(all_entries)} entries")

# ============================================================
# THE SOCIABLE (1858)
# ============================================================
sociable_entries = [
    # Acting Proverbs
    {
        "title": "When the Cat's Away the Mice Will Play",
        "category": "parlor-game",
        "subcategory": "acting-game",
        "tags": ["acting", "proverbs", "servants", "drama", "charades"],
        "difficulty": "intermediate",
        "players": "6+",
        "equipment": ["simple props (optional)"],
        "family_friendly": True,
        "original_description": "Servants named Patrick, Bridget, Bob, and Mehitable throw a party while their masters are away. Chaos ensues: guests arrive, a hat is smashed, Bob eats all the refreshments, a thief is caught, and the masters return to dismiss them all. The audience watches this miniature comedy and guesses the proverb being enacted.",
        "modern_description": "Players act out a scripted parlor comedy in which household servants misbehave while their employers are away. The scene builds to a chaotic climax—unexpected guests, mishaps, and a hasty cleanup—before the 'masters' return. The audience guesses the proverb illustrated. Players can improvise the specific mishaps while keeping the general arc of the story intact.",
        "fun_fact": "Victorian acting proverbs were considered the most sophisticated form of parlor theater; households that excelled at them were praised in social columns, and popular scenario books like The Sociable sold thousands of copies to eager amateur performers.",
        "image_prompt": "Victorian servants' hall, four children dressed as servants in the middle of a chaotic party, one eating from a platter, one with a smashed hat, another hiding something behind their back, warm candlelight, comic illustration."
    },
    {
        "title": "It Never Rains But It Pours",
        "category": "parlor-game",
        "subcategory": "acting-game",
        "tags": ["acting", "proverbs", "fortune", "drama", "Victorian"],
        "difficulty": "intermediate",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Paul Smithers is beset by creditors demanding rent, dinner being denied, and letters returned unopened. Then fortune turns: he receives a job offer, an overdue payment, and a story accepted for publication. The audience watches his extreme reversal of luck and guesses 'It Never Rains But It Pours.'",
        "modern_description": "One player acts as the put-upon protagonist facing a cascade of misfortunes—each new caller brings worse news. Then the scene flips: three pieces of excellent fortune arrive in rapid succession. The contrast between gloom and elation must be played broadly enough that the audience can recognize the proverb. Ends with the protagonist in jubilation.",
        "fun_fact": "This proverb, first recorded in 1726, was a favorite of Victorian parlor players precisely because its dramatic reversal structure gave actors a clear two-act narrative in miniature.",
        "image_prompt": "Victorian parlor, dejected man at a table with bills and letters, three other players representing creditors demanding payment, then in the right half of the illustration the same man beaming as three messengers bring good news."
    },
    {
        "title": "Honor Among Thieves",
        "category": "parlor-game",
        "subcategory": "acting-game",
        "tags": ["acting", "proverbs", "brigands", "romance", "drama"],
        "difficulty": "intermediate",
        "players": "3+",
        "equipment": ["miniature portrait prop (optional)"],
        "family_friendly": True,
        "original_description": "Brigand Cordobello robs Alice Vane of her possessions but, honor-bound, returns her miniature portrait as promised. The scene illustrates the unexpected chivalry possible even among robbers. The audience guesses 'Honor Among Thieves.'",
        "modern_description": "One player acts as the brigand, another as the victim. The brigand takes various 'stolen' items but then pauses, honor-struck, at a portrait locket. He returns it with a bow. The scene should convey moral complexity and end on a surprisingly dignified note. Other players watch and guess the proverb.",
        "fun_fact": "The proverb 'Honor among thieves' dates to at least the 17th century; Victorian parlor dramatizations often used it to explore questions of moral ambiguity in a way that polite conversation wouldn't permit.",
        "image_prompt": "Victorian drawing room converted to a mountain hideout, a dramatic brigand in a cloak holding a miniature portrait, pausing before returning it to a startled young woman, other players as fellow brigands watching from the shadows."
    },
    # Dramatic Charades
    {
        "title": "Phantom Charade",
        "category": "parlor-game",
        "subcategory": "dramatic-charade",
        "tags": ["charades", "acting", "word-parts", "guessing", "Victorian"],
        "difficulty": "intermediate",
        "players": "4+",
        "equipment": ["simple props"],
        "family_friendly": True,
        "original_description": "A dramatic charade on the word PHANTOM (PHAN-TOM). Scene one (PHAN/FAN): an office scene where clerk Tom returns a lost fan to its owner. Scene two (TOM): romance ensues between Tom and Ellen Reeves. The audience guesses the full word from the two acted syllables.",
        "modern_description": "Divide the players into actors and audience. The actors perform two short scenes: the first acting out a word or sound that represents the first syllable (FAN), the second scene showing something that sounds like the second syllable (TOM). Finally, a third scene combines both. The audience must deduce that the two syllables combine into PHANTOM. Dramatics are encouraged!",
        "fun_fact": "Dramatic charades were distinguished from acting charades by their requirement for actual scripted dialogue rather than pure mime—this form of parlor entertainment became so fashionable in the 1850s-70s that dedicated scenario books sold better than many novels.",
        "image_prompt": "Victorian parlor stage setup, one group of children acting an office scene with a fan prop, audience of three children guessing on chairs, velvet curtain pulled back, gaslight chandelier above, theatrical and elegant."
    },
    {
        "title": "Contest Charade",
        "category": "parlor-game",
        "subcategory": "dramatic-charade",
        "tags": ["charades", "riddles", "suitors", "competition", "guessing"],
        "difficulty": "intermediate",
        "players": "4+",
        "equipment": ["bandbox prop (optional)"],
        "family_friendly": True,
        "original_description": "A charade on CONTEST (CON-TEST). Two suitors, Beauchamp and Sparks, compete for Ada Lockitt's hand via a series of conundrums (CON) and then a practical test (TEST). The scene ends with a winner and the audience guessing the compound word.",
        "modern_description": "Act out two scenes: first, one character poses riddles (CONS = puzzles/conundrums) to rivals competing for a prize. Second scene, a practical TEST is given to prove worthiness. The audience must hear both syllable-scenes and identify that they combine into CONTEST. Works best with a confident performer for each scene.",
        "fun_fact": "Competition-themed charades were particularly popular because Victorian society was deeply interested in formal contests; the word 'contest' itself was richly evocative to a generation that followed debating societies, athletic races, and examination results avidly.",
        "image_prompt": "Victorian parlor, two boys in waistcoats competing before a girl seated judge, one solving a riddle with a scroll, the other opening a bandbox, audience of children watching from chairs, theatrical atmosphere."
    },
    # Acting Charades / Pantomimes
    {
        "title": "Sweepstakes Charade",
        "category": "parlor-game",
        "subcategory": "acting-charade",
        "tags": ["charades", "mime", "comedy", "pantomime", "Victorian"],
        "difficulty": "intermediate",
        "players": "5+",
        "equipment": ["props for chimney sweep and donkey race scenes"],
        "family_friendly": True,
        "original_description": "A pantomime charade on SWEEPSTAKES (SWEEP-STAKES). Scene one: Little Sweep enters the wrong chimney and finds his mother. Scene two: a donkey race for sweepstakes prizes. The audience guesses the compound word from the two acted parts.",
        "modern_description": "Prepare two short mime scenes without dialogue. The first depicts a small chimney sweep getting into comic misadventures (SWEEP). The second mimics a chaotic animal race with prizes at stake (STAKES). Both scenes are performed back to back, and the audience must combine the two words to guess SWEEPSTAKES. Encourage over-the-top physical comedy.",
        "fun_fact": "Drawing-room pantomimes became fashionable in the 1840s-1860s as a family-friendly alternative to the increasingly bawdy professional pantomime theater; The Sociable's pantomime section was widely reprinted in American parlor game books.",
        "image_prompt": "Victorian parlor stage, one child blacked with soot as Little Sweep emerging from behind a cardboard chimney, another child riding a hobby horse in a race, audience laughing, simple stage curtain behind the actors."
    },
    # Games of Action
    {
        "title": "Fagots",
        "category": "parlor-game",
        "subcategory": "action-game",
        "tags": ["chasing", "pairs", "circles", "weaving", "action"],
        "difficulty": "beginner",
        "players": "8+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Players form a double circle, each inner player paired with an outer. A catcher pursues a runner in and out of the paired players. The runner may duck inside any pair to safety, causing the outer member of that pair to become the new runner who must dash out before being caught.",
        "modern_description": "Form pairs, each pair standing front-to-back in two concentric circles. One player is the chaser, one is the runner. The runner dodges between and around pairs trying to duck in front of one. When the runner ducks in, the person now at the back of that pair becomes the new runner and must immediately sprint away. A catcher who tags a runner before they can duck in wins, and roles reverse.",
        "fun_fact": "Fagots is an early cousin of modern 'Link Tag' and 'Partner Tag'—the double-circle structure is thought to derive from the old English morris-dance ring formations adapted for parlor play.",
        "image_prompt": "Victorian parlor, two rings of children standing in pairs, one child ducking between pairs as another chases from behind, laughter and chaos, bright gaslit room, piano visible in the corner."
    },
    {
        "title": "Wolf and Hind",
        "category": "parlor-game",
        "subcategory": "action-game",
        "tags": ["chasing", "role-play", "children", "nature", "line-game"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "One player is the Wolf, another the Hind. The Hind's fawns stand in a line behind her, each holding the waist of the child in front. The Wolf tries to catch the last fawn in the line while the Hind spreads her arms to block, steering the line to protect them.",
        "modern_description": "One player is the Wolf, one is the Hind (the lead defender). All other players are fawns, forming a line by holding the waist of the person in front. The Wolf tries to grab the last fawn in the line. The Hind at the front must spread her arms and maneuver the line to keep the Wolf from reaching the tail. If the Wolf catches the last fawn, that fawn becomes the Wolf.",
        "fun_fact": "Wolf and Hind is found in almost identical form in French (Loup et Brebis), Spanish, and Italian folk game collections—its appearance in The Sociable suggests it traveled to the United States with European immigrants by 1858.",
        "image_prompt": "Victorian parlor with furniture pushed aside, a child as Wolf reaching around a line of laughing children, the Hind at the front with arms spread blocking the Wolf, all mid-chase and breathless, warm room with a large fireplace."
    },
    {
        "title": "Copenhagen",
        "category": "parlor-game",
        "subcategory": "action-game",
        "tags": ["string", "slapping", "circle", "speed", "Victorian"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": ["long string loop"],
        "family_friendly": True,
        "original_description": "Players stand in a circle, each holding a long loop of string that lies on the floor. One player in the center holds the middle of the string. On a signal, the center player jerks the string. Each player must quickly lift their section; anyone who is too slow and gets their hand slapped by the string must swap to the center.",
        "modern_description": "Form a circle with all players holding a large loop of string resting on the floor. One player stands in the center and grips the string at its midpoint. At any moment, the center player yanks the string upward. Players on the circle must jerk their section of string up before it slaps their hands. Whoever gets caught takes the center. A fast, unpredictable game of reflexes.",
        "fun_fact": "Copenhagen was reportedly brought to North America by Danish sailors and adopted enthusiastically by American parlor game books in the mid-19th century; The Sociable is one of its earliest American appearances in print.",
        "image_prompt": "Victorian parlor, six children standing in a circle each holding a large string loop on the floor, one child in the center beginning to yank the string upward, the others scrambling to lift their sections, bright and energetic scene."
    },
    {
        "title": "Ribbons",
        "category": "parlor-game",
        "subcategory": "action-game",
        "tags": ["ribbons", "decision", "speed", "parlor", "Victorian"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": ["ribbon or string pieces for each player"],
        "family_friendly": True,
        "original_description": "Each player holds a ribbon. A leader gives commands to pull or let go on the count of three. Players who obey incorrectly—pulling when they should let go, or vice versa—pay a forfeit. The speed of the commands and the need to listen carefully make this a challenging memory-and-reflex game.",
        "modern_description": "Give each player a short ribbon to hold between both hands, taut. A caller announces either 'Pull!' or 'Let go!' Players must do the opposite of what is called—pull when told 'Let go!' and release when told 'Pull!' Anyone who follows the literal command rather than the reverse pays a small forfeit. The caller speeds up commands to increase confusion.",
        "fun_fact": "Ribbons is an example of a 'do the opposite' game—a cognitive exercise that Victorian psychologists considered an excellent test of mental discipline; teachers used variants as classroom attention exercises.",
        "image_prompt": "Victorian drawing room, six children each holding a short ribbon taut between their hands, one child calling commands, some players pulling, some dropping their ribbon in confusion, all in good humor, evening by firelight."
    },
    {
        "title": "Cotton Flies",
        "category": "parlor-game",
        "subcategory": "action-game",
        "tags": ["cotton", "blowing", "competition", "children", "parlor"],
        "difficulty": "beginner",
        "players": "3+",
        "equipment": ["tuft of cotton or feather"],
        "family_friendly": True,
        "original_description": "A floating tuft of cotton or a feather is placed in the center of the group. Players must blow it to keep it in the air, directing it away from themselves. Whoever lets it touch them or land on their side pays a forfeit.",
        "modern_description": "Drop a small piece of cotton wool or a lightweight feather into the center of the seated group. Players blow at it to direct it toward others. Whoever lets it land on them or in front of them pays a small forfeit. Players may not use their hands—only breath. The game is deceptively active and surprisingly tiring as everyone puffs furiously.",
        "fun_fact": "Cotton Flies was considered an ideal invalid's game in the Victorian era—it could be played seated, required no physical exertion beyond breathing, and could amuse bedridden patients for considerable stretches.",
        "image_prompt": "Victorian parlor, five children seated in a circle leaning forward and blowing vigorously at a small white tuft of cotton floating between them, faces red with effort, comfortable armchairs and a fireplace in the background."
    },
    # Memory Games
    {
        "title": "Field of Cloth of Damask",
        "category": "parlor-game",
        "subcategory": "memory-game",
        "tags": ["memory", "trades", "story-telling", "accumulating", "Victorian"],
        "difficulty": "intermediate",
        "players": "4+",
        "equipment": ["spinning top (optional)"],
        "family_friendly": True,
        "original_description": "A 'plum pudding' (spinning top or ball) is sent around. Each player in turn continues a story by naming a trade and miming it. All players must maintain all previous trades simultaneously while adding a new one. Forgetting or confusing the sequence results in a forfeit.",
        "modern_description": "Players sit in a circle. The first player names a trade (e.g., tailor) and mimes it. The second player must mime the first trade and add their own. Each successive player repeats all previous trades in order and adds a new one. Anyone who forgets a trade or performs them in the wrong order pays a forfeit. The game becomes progressively hilarious as the list of mimed trades grows impossible to maintain.",
        "fun_fact": "This accumulative mime game is a Victorian refinement of the ancient 'I packed my bag' memory structure, with the trades theme reflecting Victorian society's intense interest in craft and guild identity.",
        "image_prompt": "Victorian parlor, seven adults and children seated in a ring, each in a different comic mime pose representing a different trade—one sewing, one hammering, one measuring fabric—all simultaneously, laughter and chaos."
    },
    {
        "title": "Flour Merchant",
        "category": "parlor-game",
        "subcategory": "word-avoidance-game",
        "tags": ["word-avoidance", "flour", "forbidden-words", "forfeit", "Victorian"],
        "difficulty": "intermediate",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Players take turns asking the flour merchant for flour. The Merchant must avoid saying any forbidden words (typically 'yes,' 'no,' 'black,' 'white'). The questioner tries every trick to make the Merchant slip up. An error means a forfeit.",
        "modern_description": "One player is the Flour Merchant. All others take turns approaching to 'buy flour,' asking rapid-fire questions designed to trick the Merchant into saying the forbidden words. The Merchant must answer every question sensibly while avoiding the taboo vocabulary. A successful merchant with no slips wins; each slip earns a forfeit. Rotate the Merchant role.",
        "fun_fact": "Word-avoidance games based around a merchant or shopkeeper character appear in English literature as early as the 15th century; The Sociable version is notable for making 'flour' the commercial conceit, likely a pun on 'flower' and thus the forbidden word trap.",
        "image_prompt": "Victorian kitchen setting, child wearing apron as the Flour Merchant behind a small table, another child leaning forward with a sly expression asking trick questions, others watching for errors, bags of flour in the background."
    },
    {
        "title": "Cross Purposes",
        "category": "parlor-game",
        "subcategory": "word-game",
        "tags": ["questions", "answers", "mismatching", "absurdity", "Victorian"],
        "difficulty": "beginner",
        "players": "6+",
        "equipment": ["paper and pencils (optional)"],
        "family_friendly": True,
        "original_description": "Each player whispers an answer to the player on their right, who passes it on. Meanwhile, a different question is whispered from the left. When the mismatched question-and-answer pairs are read aloud in sequence, the nonsensical results produce great hilarity.",
        "modern_description": "Each player simultaneously writes (or whispers) a question on one piece of paper and an answer on another. Papers are shuffled and randomly paired. Each pair is then read aloud as a matching Q&A: 'What is your favorite sport?' paired with 'A purple elephant' produces absurdist comedy. An elegant, zero-preparation game that scales easily.",
        "fun_fact": "Cross Purposes is the Victorian ancestor of the modern party game Cards Against Humanity and Consequences—the principle of randomly pairing unrelated statements to produce comedy has proven universally appealing across two centuries.",
        "image_prompt": "Victorian parlor, circle of players each whispering to their neighbor while another whispers in their other ear, confusion on their faces, one person reading aloud from a slip of paper to general laughter, evening fireplace scene."
    },
    {
        "title": "Story Play",
        "category": "parlor-game",
        "subcategory": "word-game",
        "tags": ["story", "collaborative", "whispering", "absurdity", "Victorian"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": ["paper and pencils (optional)"],
        "family_friendly": True,
        "original_description": "Each player is assigned a key word. A story is told and whenever the storyteller pauses, the next player in sequence must immediately say their word—correctly placed or not. The resulting narrative is a hilarious mixture of sense and nonsense.",
        "modern_description": "Assign each player a word before the story starts. A storyteller narrates a tale and pauses at random points. Whoever's turn it is must insert their word immediately into the story at that point, whether or not it makes grammatical or logical sense. The storyteller must then continue from whatever word was just inserted. Stories devolve into glorious nonsense.",
        "fun_fact": "Story Play is a precursor to the Surrealist technique of 'exquisite corpse' writing, developed in the 1920s—the Victorian parlor game clearly inspired later artistic experiments with random collaborative narrative.",
        "image_prompt": "Victorian parlor, a storyteller gesturing dramatically with one hand pausing to look expectantly at a child who blurts out a word, others listening with anticipatory grins, lamplight casting warm shadows, bookshelves behind."
    },
    {
        "title": "Dutch Concert",
        "category": "parlor-game",
        "subcategory": "music-game",
        "tags": ["music", "instruments", "imitation", "leader", "Victorian"],
        "difficulty": "beginner",
        "players": "5+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Each player is assigned a musical instrument to imitate vocally or with gestures. A leader directs the 'orchestra' by pointing. When pointed at, each player must perform their instrument; when the leader changes point, that player must immediately switch. The goal is chaotic, simultaneous 'music' from the whole group.",
        "modern_description": "Assign each player a different instrument to mime and sound-imitate (e.g., violin, drum, tuba). A conductor points at players one by one or in groups. Pointed-at players must immediately begin playing their instrument mimetically. When the conductor switches their point, the old player stops and the new one starts. The conductor can point at the whole group for a full-orchestra crescendo.",
        "fun_fact": "Dutch Concert takes its name from the Victorian slang 'Dutch' meaning chaotic or confused—the game deliberately produces a cacophony, and its name is an ironic jab at the idea of an orderly concert.",
        "image_prompt": "Victorian parlor, seven people each miming different musical instruments with exaggerated gestures—one bowing a violin, one beating drums, one blowing a tuba—all looking at a child conductor with a ruler baton, hilarious chaos."
    },
    {
        "title": "Thus Says Grand Mufti",
        "category": "parlor-game",
        "subcategory": "action-game",
        "tags": ["imitation", "gestures", "leader", "attention", "Victorian"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "A leader performs gestures and says 'Thus says Grand Mufti—do this' when a gesture must be copied, and 'Thus says Grand Mufti—do so' when it must not. Players must imitate only the 'do this' commands. Wrong responses earn forfeits.",
        "modern_description": "One player is the Grand Mufti and performs various gestures—patting the head, winking, crossing arms. When they say 'Thus says Grand Mufti—do this!' everyone must copy immediately. When they say 'do so' instead, nobody should copy. The Mufti tries to trick players by varying the commands unpredictably and mixing gestures. Anyone copying a 'do so' command pays a forfeit.",
        "fun_fact": "Grand Mufti is the Victorian parlor counterpart of 'Simon Says,' with an exotic Ottoman title that was fashionable in an era of intense European curiosity about the Islamic world.",
        "image_prompt": "Victorian parlor, a child in a makeshift turban as the Grand Mufti performing an elaborate gesture, other players copying earnestly, one child caught in the wrong motion looking embarrassed, elegant drawing room setting."
    },
    {
        "title": "What Is My Thought Like?",
        "category": "parlor-game",
        "subcategory": "guessing-game",
        "tags": ["guessing", "comparisons", "wit", "analogy", "Victorian"],
        "difficulty": "intermediate",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "One player thinks of a person or object and asks each other player 'What is my thought like?' Each player gives a comparison, then the thinker reveals the thought. Each player must then justify their comparison, however absurd it seemed—the wittiest justification wins.",
        "modern_description": "One player thinks of any person, object, or concept and writes it down secretly. They ask each other player in turn 'What is my thought like?' Players give quick comparisons: 'like a wet boot,' 'like Tuesday,' 'like a sleeping cat.' The secret is revealed, and now each player must explain how their comparison fits. 'My wet boot is like the Queen because both get walked on respectfully.' The most inventive explanation wins the round.",
        "fun_fact": "This game was considered one of the best wit-sharpening exercises in Victorian parlor culture; skill at unexpected analogies was a prized social accomplishment, and the game appears in dozens of 19th-century etiquette and entertainment guides.",
        "image_prompt": "Victorian drawing room, one person whispering something written on a card to themselves, others calling out fanciful comparisons with gestures, the room full of animated discussion, evening party atmosphere."
    },
    {
        "title": "Lawyer",
        "category": "parlor-game",
        "subcategory": "word-game",
        "tags": ["word-game", "proxy", "confusion", "answers", "Victorian"],
        "difficulty": "intermediate",
        "players": "5+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "Each player has a 'Lawyer' who must answer all questions addressed to their client. When someone addresses Player A, Player A's Lawyer answers instead. The questioner may ask the Lawyer any trick question about their client. If the Lawyer is caught off guard or answers for the wrong person, they pay a forfeit.",
        "modern_description": "Assign a Lawyer to each player at the start. When anyone addresses you directly, your Lawyer must intercept and answer for you—you say nothing. The questioner may address questions rapidly to different people to confuse the Lawyers about who they represent. If you (the client) accidentally answer your own question, or if your Lawyer answers for the wrong client, a forfeit is owed.",
        "fun_fact": "Lawyer parlor games satirized the legal profession's reputation for speaking on others' behalf; the Victorian middle classes found great amusement in mock-legal proceedings, which also appear in Charles Dickens's early sketches.",
        "image_prompt": "Victorian parlor, one child in a makeshift lawyer's wig standing protectively next to another child, intercepting a question from a third player who is pointing accusingly, others watching the legal drama unfold, bookshelves of law volumes behind."
    },
    {
        "title": "Consequences",
        "category": "parlor-game",
        "subcategory": "writing-game",
        "tags": ["writing", "folded-paper", "absurdity", "collaborative", "Victorian"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": ["paper", "pencils"],
        "family_friendly": True,
        "original_description": "Each player writes a romantic or social story in parts—a name, a meeting place, what he said, what she said, and the consequence—folding and passing the paper between each contribution so no one sees what has been written before. The resulting absurd stories are read aloud to general hilarity.",
        "modern_description": "Give each player a long strip of paper. All write a man's name at the top, fold it over to hide the writing, and pass to the left. Next write 'met [a woman's name]' and fold and pass. Then 'He said...' then 'She said...' then 'And the consequence was...' and 'And what the world said was...' Unfold and read complete stories aloud. The random combinations produce comic narrative masterpieces.",
        "fun_fact": "The Sociable includes one of the earliest published descriptions of Consequences in America (1858); the game was later adopted by the Surrealists in Paris in the 1920s and rechristened 'exquisite corpse,' directly inspiring Dadaist and Surrealist poetry.",
        "image_prompt": "Victorian parlor, several players each bent over paper writing in secret, one person in the act of folding their paper to hide the writing before passing it left, expressions of mischievous concentration, evening lamplight."
    },
    {
        "title": "Proverbs (Guessing Game)",
        "category": "parlor-game",
        "subcategory": "guessing-game",
        "tags": ["proverbs", "guessing", "questions", "embedded-answers", "Victorian"],
        "difficulty": "intermediate",
        "players": "5+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "One player leaves the room while the others agree on a proverb. When the player returns, they ask each person in turn any question; each player must answer so that their reply contains one word of the proverb in order. After asking all players, the questioner must name the proverb.",
        "modern_description": "A player leaves the room while everyone agrees on a proverb (e.g., 'A rolling stone gathers no moss'). The player returns and asks each person a question. Each player must give a natural-sounding answer that contains their assigned proverb word—'A' 'rolling' 'stone' 'gathers' 'no' 'moss' distributed across six players' answers. The guesser must identify the proverb from those hidden words.",
        "fun_fact": "This embedded-word proverb game requires extraordinary creativity to disguise proverb words in natural conversation; skilled Victorian players reportedly chose obscure proverbs with unusual words to make the guesser's task nearly impossible.",
        "image_prompt": "Victorian parlor, one player re-entering the room to face a lineup of five smiling players who each hold a secret word, the questioner walking down the line asking each one in turn, faces of suppressed amusement, candlelit evening scene."
    },
    {
        "title": "Characters (Who Am I?)",
        "category": "parlor-game",
        "subcategory": "guessing-game",
        "tags": ["guessing", "historical", "characters", "clues", "Victorian"],
        "difficulty": "intermediate",
        "players": "4+",
        "equipment": ["cards with names written on them (optional)"],
        "family_friendly": True,
        "original_description": "One player thinks of a historical figure and gives increasingly specific clues. Others ask yes-or-no questions to identify the figure. As clues narrow the field from broad era to specific country to individual deeds, the guesser must identify who is being impersonated.",
        "modern_description": "One player chooses a famous historical person. Other players ask yes-or-no questions: 'Were you alive before 1800?' 'Were you a ruler?' 'Did you rule in Europe?' The clue-giver may also volunteer one clue per round. Players get one guess per round. Whoever correctly names the historical figure takes the next turn as the mystery character.",
        "fun_fact": "Victorian 'Who Am I?' games served as informal history lessons; children who played them regularly were expected to know figures from ancient Rome through recent British history, and the game's difficulty was adjusted to the knowledge level of the players.",
        "image_prompt": "Victorian library, one child standing with a card held to their forehead showing 'Julius Caesar,' others seated around gesturing and calling out yes-or-no questions, busts and portraits on the shelves behind, scholarly atmosphere."
    },
    {
        "title": "Scissors Crossed or Not Crossed",
        "category": "parlor-game",
        "subcategory": "catch-game",
        "tags": ["trick", "catch", "scissors", "observation", "Victorian"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": ["pair of scissors"],
        "family_friendly": True,
        "original_description": "A pair of scissors is passed around the circle. Each player receives them and passes them on, declaring 'I pass these scissors crossed' or 'uncrossed.' The key is that the declaration should match whether the passer's legs are crossed—not the position of the scissors. Those who know the trick watch as new players puzzle over the scissors' position.",
        "modern_description": "Pass a pair of scissors around the circle. As you receive and pass them, declare 'I pass these scissors crossed' or 'uncrossed.' The real rule—kept secret from newcomers—is that the declaration should describe the position of your own legs, not the scissors. Knowing players watch the newcomers' confusion as they try every combination of scissors positions, oblivious to the actual criterion.",
        "fun_fact": "Scissors Crossed or Not Crossed is one of the most enduring Victorian 'trick' parlor games; it works precisely because the scissors are such an obvious red herring that players rarely think to look at the passer's legs.",
        "image_prompt": "Victorian parlor circle, one player passing scissors to the next with a mysterious smile declaring 'crossed,' the recipient examining the scissors thoroughly puzzled while knowing players exchange amused glances, evening gaslight."
    },
    {
        "title": "Pigeon Flies",
        "category": "parlor-game",
        "subcategory": "action-game",
        "tags": ["attention", "lifting-finger", "birds", "trick", "children"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": ["table or flat surface"],
        "family_friendly": True,
        "original_description": "All players place a finger on the table. A leader calls out the names of various creatures—'Pigeon flies! Eagle flies! Cat flies! Fish flies!' Players must lift their finger only for real flying creatures and keep it down for non-flyers. Anyone lifting at a non-flyer pays a forfeit.",
        "modern_description": "Everyone places one finger flat on the table. The caller shouts the names of various creatures with 'flies!' appended. Players must quickly decide: lift their finger if the creature genuinely flies, keep it down if it doesn't. The caller tries to build a rhythm with real fliers, then suddenly calls 'Pig flies!' or 'Elephant flies!' to catch inattentive players. Speed and trickery are essential.",
        "fun_fact": "Pigeon Flies appears in French parlor manuals as 'Oiseau vole' and is documented across Europe from the 17th century onwards—the Victorian American version is essentially unchanged from its French cousin imported with Huguenot immigrants.",
        "image_prompt": "Victorian parlor, six players seated around a table each with one finger pressed to the surface, one child calling out a word with theatrical gestures, two players have mistakenly lifted their fingers and look mortified, candlelight."
    },
    {
        "title": "Witch (The And Game)",
        "category": "parlor-game",
        "subcategory": "catch-game",
        "tags": ["trick", "witch", "and", "catch", "Victorian"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": ["various small objects"],
        "family_friendly": True,
        "original_description": "One player, the Witch, lays out several objects. She says 'I touched such-and-such, and such-and-such.' Players must guess which object she actually touched. The secret is that she always touched the last object mentioned before the word 'and.' Those who know the secret watch newcomers guess in vain.",
        "modern_description": "Lay six to ten small objects on a table. One player (the Witch) secretly selects one object and then says 'I touched the apple, and the pencil, and the key.' Other players must guess which object was touched. The real rule (secret from newcomers) is that the Witch always touched whichever object came immediately before the final 'and' in their sentence. Knowing players watch with amusement.",
        "fun_fact": "The Witch game illustrates how Victorian parlor games often served as miniature lessons in linguistic attention—the word 'and' is so commonplace that listeners almost never register it as a meaningful signal.",
        "image_prompt": "Victorian parlor table covered with small objects—a key, a thimble, a pencil, a coin—one child pointing accusingly as the Witch, another player staring at the objects in total confusion, knowing players smiling behind their hands."
    },
    # Forfeits
    {
        "title": "Laughing Gamut",
        "category": "parlor-game",
        "subcategory": "forfeit-game",
        "tags": ["forfeits", "laughing", "contagion", "musical-scale", "children"],
        "difficulty": "beginner",
        "players": "4+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "The player redeeming a forfeit must laugh up and down the musical scale—Ha! He! Hi! Ho! Hu!—proceeding from do to sol and back, each note a different syllable of laughter. Any failure to maintain pitch or sequence earns additional forfeits.",
        "modern_description": "The forfeit-payer stands and laughs their way through a musical scale using the syllables Ha, He, Hi, Ho, Hu—one for each note from low to high and back. The effect is so absurd that the performer usually cannot maintain composure, and the audience's laughter makes the performance even harder to complete. A classic Victorian ice-breaker forfeit.",
        "fun_fact": "Laughing Gamut is considered one of the most effective 'contagious laughter' games ever devised—Victorian physicians wrote about its ability to produce genuine uncontrollable laughter as evidence of laughter's automatic and contagious nature.",
        "image_prompt": "Victorian parlor, one child standing stiffly attempting to laugh in musical scale notation—Ha He Hi Ho Hu—while the seated audience bursts into genuine uncontrolled laughter, evening firelight, warm and joyful scene."
    },
    {
        "title": "Dot and Carry One",
        "category": "parlor-game",
        "subcategory": "forfeit-game",
        "tags": ["forfeits", "hopping", "ankle", "physical", "Victorian"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": [],
        "family_friendly": True,
        "original_description": "The player paying a forfeit must hold one ankle and hop on the other foot around the room without losing their balance or releasing the held ankle. Named for the arithmetic term of 'dot and carry one' used when adding columns of numbers.",
        "modern_description": "Grab one ankle with the same-side hand and hop on the other foot all the way around the room (or to a designated point and back). Any stumble, ankle release, or loss of balance requires starting again. The charming name comes from Victorian arithmetic class where 'dot and carry one' meant writing the units digit and carrying the tens.",
        "fun_fact": "This forfeit is named after the phrase 'dot and carry one' from Victorian school arithmetic—it was considered doubly amusing because it punished the mathematical dunce by making them enact the very action their schoolwork described.",
        "image_prompt": "Victorian parlor, one child hopping on one foot while clutching their ankle, face concentrated with effort, other children watching and counting aloud, a path of chairs forming the circuit to hop around, lamplight."
    },
    # Puzzles from The Sociable
    {
        "title": "Card Chain Puzzle",
        "category": "puzzle",
        "subcategory": "paper-puzzle",
        "tags": ["paper", "cutting", "chain", "craft", "Victorian"],
        "difficulty": "beginner",
        "players": "1",
        "equipment": ["single playing card", "scissors"],
        "family_friendly": True,
        "original_description": "A single playing card is cut in a specific pattern of interlocking cuts so that it unfolds into a continuous paper chain large enough to pass over a person's body. The challenge is in discovering the exact cutting pattern.",
        "modern_description": "Take a standard playing card. Make a series of alternating cuts from each long edge without cutting all the way through—like fringing both sides in an interlocking pattern. At the short ends, cut along the fold lines to join the strip into a loop. When carefully opened, the card expands into a chain ring large enough to step through. A wonderful puzzle of how area can be redistributed by cutting.",
        "fun_fact": "This paper-cutting puzzle was already ancient by 1858 when The Sociable published it; Martin Gardner traced it to 17th-century German paper-cutting traditions, and it remains a popular mathematics-class demonstration of topology.",
        "image_prompt": "Victorian parlor table, a playing card with precise scissor cuts being gently pulled open to form a large paper chain ring, hands holding the delicate paper, scissors and other cards visible nearby, amazed child watching."
    },
    {
        "title": "Blind Abbot and Monks Puzzle",
        "category": "puzzle",
        "subcategory": "arithmetical-puzzle",
        "tags": ["arithmetic", "monks", "rows", "counting", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["pencil and paper", "counters"],
        "family_friendly": True,
        "original_description": "A Blind Abbot counts 9 monks per row when he checks his monastery. Monks rearrange themselves so no matter which direction the Abbot counts the rows, he always counts 9—but the actual number of monks present varies from 18 to 36. How do they manage this deception?",
        "modern_description": "Arrange counters in a 3x3 grid with four in each corner and one on each side edge for a total of 24. Each row of three sums to 9 in both directions. Now rearrange the counters so that each row still sums to 9 but you have used more or fewer total counters. The puzzle requires understanding that corner counters are counted twice—once in each direction. Multiple valid arrangements exist.",
        "fun_fact": "The Blind Abbot puzzle is one of the oldest recreational number puzzles in European history, appearing in 9th-century manuscripts by Alcuin of York and remaining popular through the Victorian era—a lifespan of nearly a thousand years.",
        "image_prompt": "Victorian illustration of a medieval monastery courtyard, monks rearranging themselves in rows while a blindfolded Abbot counts on his fingers, ornate stone arches in the background, comic and mathematical atmosphere."
    },
    {
        "title": "Christians and Turks River Puzzle",
        "category": "puzzle",
        "subcategory": "river-crossing-puzzle",
        "tags": ["river-crossing", "logic", "Christians", "Turks", "boat"],
        "difficulty": "advanced",
        "players": "1",
        "equipment": ["pencil and paper", "counters"],
        "family_friendly": True,
        "original_description": "Fifteen Christians and fifteen Turks are at sea in a boat that can only hold a few at a time. To save the ship, half must be thrown overboard. They are placed in a circle and every ninth person is cast out. By clever arrangement, all fifteen Turks are eliminated and all Christians survive. Which positions ensure this?",
        "modern_description": "Arrange 30 tokens in a circle and count off every ninth token to remove it. Before you start, you must arrange the 15 Christians (one color) and 15 Turks (another color) so that every ninth token removed is always a Turk. The solution requires a specific starting arrangement. Try it first with small numbers to discover the pattern, then attempt the full 30-person puzzle.",
        "fun_fact": "This puzzle is at least 1,400 years old and appears in virtually every European puzzle collection from medieval manuscripts through Victorian books; different versions replace Christians and Turks with any two groups depending on the political climate of the era.",
        "image_prompt": "Victorian puzzle book illustration, 30 figures arranged in a circle on a stormy boat deck, alternating between two groups marked by hats, a counted sequence marked in pencil, sea and storm clouds in the background."
    },
    {
        "title": "Practicable Orchard Puzzle",
        "category": "puzzle",
        "subcategory": "geometric-puzzle",
        "tags": ["geometry", "trees", "rows", "orchard", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["pencil and paper"],
        "family_friendly": True,
        "original_description": "Plant 16 trees in an orchard such that they form 10 rows of 4 trees each. This requires the trees to be arranged in a non-rectangular pattern—a classical points-in-lines problem from Victorian puzzle collections.",
        "modern_description": "On paper, place 16 dots (trees) so that you can draw 10 straight lines, each passing through exactly 4 of the dots. The solution requires a star or overlapping square configuration—straight rows and rectangular grids won't work. Try different configurations on graph paper. Hint: look for ways to use diagonal lines as well as horizontal and vertical ones.",
        "fun_fact": "The orchard puzzle family—where trees must be arranged in overlapping rows—became one of the defining puzzle types of the 19th century; Victorian puzzle books competed to find the most trees in the most rows, leading to increasingly complex solutions.",
        "image_prompt": "Victorian gentleman's puzzle journal open to an orchard diagram, dots representing trees connected by ruled lines showing 10 rows of 4, a pencil resting on the page, ornate pen-and-ink border, Victorian desk."
    },
    {
        "title": "Market Woman's Puzzle",
        "category": "puzzle",
        "subcategory": "arithmetical-puzzle",
        "tags": ["arithmetic", "apples", "sale", "loss", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["pencil and paper"],
        "family_friendly": True,
        "original_description": "A market woman sells apples at three for a penny and then at two for a penny; she ends up losing money despite apparently selling at an average price. The puzzle reveals why the average of rates is not the same as the rate of the average—an early introduction to the harmonic mean.",
        "modern_description": "A woman has 30 apples she sells at 3 for 1¢, then gets 30 more and sells them at 2 for 1¢. She expects the same as selling 60 apples at 5 for 2¢. But when you calculate both scenarios, she actually earns less using the two-batch method. Calculate both totals to find the discrepancy and explain why the 'average rate' isn't the same as the actual average price.",
        "fun_fact": "This puzzle illustrates what mathematicians now call the 'harmonic mean problem' or 'speed-average fallacy'; the same error causes drivers to miscalculate fuel economy when they average miles per gallon on different road types.",
        "image_prompt": "Victorian market scene, a woman at a stall selling apples, pennies on the counter, puzzle equations floating above in Victorian script: 30 apples at 3 for 1¢, then 30 at 2 for 1¢, surprised expression as she counts her earnings."
    },
    {
        "title": "Nine Digits Magic Square",
        "category": "puzzle",
        "subcategory": "arithmetical-puzzle",
        "tags": ["magic-square", "arithmetic", "nine", "digits", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["pencil and paper"],
        "family_friendly": True,
        "original_description": "Arrange the nine digits (1-9) in a 3x3 grid so that every row, column, and diagonal adds up to 15. This classic magic square puzzle challenges players to find the single valid arrangement and its rotations.",
        "modern_description": "Draw a 3x3 grid and fill it with the digits 1 through 9 (each used once) so that every row, every column, and both main diagonals all add to 15. Only one fundamental solution exists (plus rotations and reflections). Start by finding what the center must be, then work outward. Check all eight sums when you think you have it.",
        "fun_fact": "The 3x3 magic square summing to 15 is known as the Lo Shu in Chinese mathematics, where it appears in legend dating to around 2200 BC—making this puzzle perhaps the oldest still-practiced mathematical recreation in human history.",
        "image_prompt": "Victorian puzzle book page showing a completed 3x3 magic square with digits 1-9, arrows indicating each row, column, and diagonal summing to 15, Victorian decorative border, candlelit study with quill and inkwell."
    },
    # Science / Parlor Magic from The Sociable
    {
        "title": "Thaumatrope",
        "category": "scientific-recreation",
        "subcategory": "optical-illusion",
        "tags": ["optical", "spinning", "illusion", "persistence-of-vision", "Victorian"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["cardstock card", "two strings or a pencil"],
        "family_friendly": True,
        "original_description": "A cardstock disc has different images on each side—a bird on one side and an empty cage on the other. When spun rapidly by twisting the attached strings, the spinning disc causes both images to appear simultaneously: the bird appears inside the cage.",
        "modern_description": "Cut a circle from cardboard and draw an image on each side—perhaps a fish on one side and an empty fishbowl on the other. Attach a string to each side or mount on a pencil. Spin the disc rapidly by rolling the pencil between your palms or twisting and releasing the strings. The rapid alternation of the two images creates the optical illusion of a combined picture: the fish inside the bowl.",
        "fun_fact": "The Thaumatrope was patented in 1826 by John Ayrton Paris and became a Victorian sensation; the name combines Greek words for 'wonder' and 'turning.' It was one of the first devices to exploit persistence of vision—the same principle that makes cinema possible.",
        "image_prompt": "Victorian child's hands spinning a cardstock disc on twisted strings, one side showing a bird, the other showing an empty cage, the spinning motion blurring into a combined image of bird-in-cage, parlor light, simple elegant illustration."
    },
    {
        "title": "Boomerang Card",
        "category": "scientific-recreation",
        "subcategory": "physics-experiment",
        "tags": ["card", "spinning", "return", "physics", "Victorian"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["playing card or stiff card"],
        "family_friendly": True,
        "original_description": "A playing card is held vertically between thumb and forefinger and spun sharply into the air with a flick. When thrown with the correct spin and angle, the card curves through the air in an arc and returns to the thrower—a miniature boomerang effect.",
        "modern_description": "Hold a playing card vertically by one short edge. Throw it sharply forward with a strong backspin flick of the wrist. When done correctly, the aerodynamic lift created by the spinning card causes it to curve upward, slow, and then travel back in a gentle arc toward you. Experiment with different angles and spin amounts to perfect the return. Physics in action with no special equipment needed.",
        "fun_fact": "The boomerang card trick was used by Victorian science teachers to demonstrate the Magnus Effect—the same aerodynamic principle that causes curveball pitches in baseball and the banana kick in soccer.",
        "image_prompt": "Victorian drawing room, a child releasing a playing card with a sharp flick of the wrist, the card's curved flight path shown with dotted lines arcing away and returning, other children watching with amazed expressions."
    },
    {
        "title": "Magic Tumbler",
        "category": "scientific-recreation",
        "subcategory": "physics-experiment",
        "tags": ["water", "card", "air-pressure", "inverted-glass", "Victorian"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["glass", "water", "stiff card"],
        "family_friendly": True,
        "original_description": "Fill a tumbler to the brim with water, lay a playing card over the top, and invert it. The water remains in the inverted glass, apparently defying gravity, held in place by atmospheric pressure acting upward against the card.",
        "modern_description": "Fill a glass completely with water. Place a stiff card (a playing card works perfectly) flat over the mouth of the glass. Holding the card in place, carefully turn the glass upside down over a sink. Remove your hand from the card—the water will not fall out. Atmospheric pressure pushing up on the card is greater than the downward force of the water. A classic physics demonstration that never fails to astonish.",
        "fun_fact": "This demonstration of atmospheric pressure has been a staple of scientific education since Torricelli's experiments in 1643; it appears in virtually every Victorian science-for-youth book as a way of making the invisible force of air pressure dramatically visible.",
        "image_prompt": "Victorian science demonstration, a child's hands carefully inverting a water-filled glass with a card over the mouth, the card holding the water in the upside-down glass, amazed onlookers, parlor table with water drips below as precaution."
    },
    {
        "title": "Balanced Coin on Cork",
        "category": "scientific-recreation",
        "subcategory": "physics-experiment",
        "tags": ["balance", "cork", "coin", "gravity", "center-of-mass"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["cork", "coin", "pin or needle"],
        "family_friendly": True,
        "original_description": "A coin is balanced on the point of a needle or pin stuck into a cork, then the cork is placed on a rounded surface. By adjusting the coin's exact position, the center of gravity falls below the pivot point, making the coin spin stably and self-right when disturbed.",
        "modern_description": "Stick a pin point-up through a cork. Balance a coin on the pin point (a notch in the coin edge helps). Place the cork on a smooth rounded surface. When the coin is tilted, it swings back to center and can even be spun. The secret is that the coin's center of gravity (weighted by the size of the coin below the pivot) is below the pin point, creating pendulum-like stability.",
        "fun_fact": "This experiment was used throughout the 19th century to explain center-of-gravity and tightrope walking—circus programs would often reproduce the explanation from parlor science books to explain how acrobats maintain balance.",
        "image_prompt": "Victorian parlor table, a coin spinning perfectly balanced on a pin stuck into a cork resting on a rounded candlestick top, amazed child watching, physics demonstration atmosphere, soft evening light."
    },
    {
        "title": "Revolving Serpent",
        "category": "scientific-recreation",
        "subcategory": "physics-experiment",
        "tags": ["heat", "convection", "spiral", "paper", "serpent"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["thin paper", "scissors", "thread", "candle"],
        "family_friendly": True,
        "original_description": "A spiral is cut from thin paper into a serpent shape. When suspended by a thread above a candle flame (not touching it), the rising hot air from the flame rotates the paper serpent continuously.",
        "modern_description": "Cut a circle of tissue paper into a spiral coil, cutting from the edge toward the center. Suspend the spiral by a thread attached to the center. Hold the spiral above (but not touching) a lit candle. The hot air rising from the flame will rotate the paper serpent slowly and continuously. The longer the spiral, the more dramatic the rotation. A beautiful demonstration of convection currents.",
        "fun_fact": "The revolving serpent is one of the safest and most visually spectacular heat-convection demonstrations; it remains a standard science-class experiment today and appears in toy form as 'wind spirals' hung above radiators in contemporary homes.",
        "image_prompt": "Victorian parlor, a paper spiral hanging from a string above a candle flame, slowly rotating as rising hot air spins it, child watching fascinated, the serpent shape clearly visible, warm candlelight illuminating the delicate paper."
    },
    # Board Games from The Sociable
    {
        "title": "Agon (Queen's Guards)",
        "category": "board-game",
        "subcategory": "strategy-game",
        "tags": ["strategy", "hexagonal", "queen", "guards", "Victorian"],
        "difficulty": "intermediate",
        "players": "2",
        "equipment": ["hexagonal board", "14 pieces per player"],
        "family_friendly": True,
        "original_description": "Each player has 7 pieces—one Queen and six Guards. The goal is to maneuver the Queen to the center hexagon and surround her with all six Guards before the opponent does so. Pieces move one space at a time along hexagonal lines. An elegant Victorian strategy game.",
        "modern_description": "Set up a hexagonal board with the Queen on a starting edge hex and Guards nearby. On each turn, move one piece one step along any hexagonal edge. To win, place your Queen in the very center hex and surround her with all six Guards in the six adjacent center hexes. Opponent pieces can be displaced by moving a piece to their hex, forcing them back to the outer ring. The game rewards careful coordination of all seven pieces.",
        "fun_fact": "Agon is thought to be one of the first games specifically designed for a hexagonal board; it was invented in France around 1842 and became popular across Europe through the second half of the 19th century, appearing in several American parlor game books.",
        "image_prompt": "Victorian parlor table, a hexagonal game board with colored game pieces arranged on it, two players in Victorian dress studying the board with concentration, rule book beside them, evening lamplight, elegant drawing room."
    },
    {
        "title": "Corsair (Peg Solitaire Variant)",
        "category": "board-game",
        "subcategory": "peg-puzzle",
        "tags": ["solitaire", "pegs", "leaping", "patience", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["peg solitaire board"],
        "family_friendly": True,
        "original_description": "A variant of Peg Solitaire (the 33-hole board) with a specific starting position designed to produce a satisfying pattern when completed. The Corsair starts with specific holes empty and the goal is to remove all but one peg through jumping sequences.",
        "modern_description": "Start with a standard peg solitaire board. Set up the Corsair starting position by removing specific pegs from their starting positions as described. Pegs jump over adjacent pegs (horizontally or vertically) into empty holes, removing the jumped peg. The goal is to finish with exactly one peg remaining in a specific target hole. Each starting position produces a unique puzzle difficulty.",
        "fun_fact": "Peg solitaire variants were among the most-published puzzle forms in Victorian Britain; The Sociable lists several including Corsair, Curate, and Triplet, each offering a different challenge level on the same physical board.",
        "image_prompt": "Victorian parlor, a wooden peg solitaire board with a specific pattern of wooden pegs, one hand reaching to make a jump, diagram of the starting position in an open book beside the board, focused solitary player."
    },
    {
        "title": "American Bagatelle",
        "category": "parlor-game",
        "subcategory": "tabletop-game",
        "tags": ["bagatelle", "spinner", "pins", "scoring", "Victorian"],
        "difficulty": "beginner",
        "players": "2+",
        "equipment": ["bagatelle board with spinner and pins"],
        "family_friendly": True,
        "original_description": "A tabletop game with a spinning top or ball launcher that propels a marble or ball into a field of scoring pins. The ball ricochets off pins, and whatever numbered pocket or zone it finally rests in is the player's score. First to an agreed total wins.",
        "modern_description": "Set up the American Bagatelle board—a tabletop landscape of numbered scoring pockets and upright pin obstacles. Launch the ball using the spinner or plunger and watch it bounce among the pins before coming to rest in a scoring zone. Record the score and pass to the next player. The skill lies in controlling the launch direction and force to aim for high-value pockets.",
        "fun_fact": "American Bagatelle was the direct forerunner of the modern pinball machine; the spring-loaded plunger and pin-field configuration of today's arcade pinball is directly descended from Victorian parlor bagatelle tables.",
        "image_prompt": "Victorian parlor, a ornate wooden bagatelle table with a green felt surface dotted with brass pins and numbered scoring cups, a child launching a marble with the spring mechanism, others keeping score on a chalkboard behind."
    },
]

for e in sociable_entries:
    if not is_duplicate(e['title']):
        entry_id = make_id(e['title'])
        e['id'] = entry_id
        e['slug'] = entry_id
        e['source_book'] = "The Sociable, or, One Thousand and One Home Amusements"
        e['source_author'] = "Various"
        e['source_year'] = 1858
        e['source_url'] = "https://archive.org/details/cu31924080786779"
        all_entries.append(e)

print(f"After The Sociable: {len(all_entries)} entries")

# ============================================================
# HOFFMANN - Puzzles Old and New (1893)
# ============================================================
hoffmann_entries = [
    # Dexterity puzzles
    {
        "title": "The Pick-Me-Up Puzzle",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "marble", "spiral", "box", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["cylindrical box with spiral incline inside", "marble"],
        "family_friendly": True,
        "original_description": "A cylindrical box contains a spiral incline and a marble. The challenge is to work the marble up and down the spiral incline steadily, without jerking, so that it travels the full length of the hidden path inside the box. No explicit solution is given—practice and a very steady hand are the only guides.",
        "modern_description": "Tilt and rotate a cylindrical box to coax an internal marble along an unseen spiral ramp. The marble must travel smoothly without jerking, which would send it off the ramp. The path is invisible, so the player must deduce the spiral's progress from the sound and feel of the marble's movement. An elegant exercise in patience and tactile sensitivity.",
        "fun_fact": "Dexterity puzzles like the Pick-Me-Up were among the best-selling toys of the 1880s-90s; the cylindrical box with internal maze was a direct ancestor of the modern labyrinth ball toy.",
        "image_prompt": "Victorian gentleman's study, a polished wooden cylindrical box being carefully tilted in a man's hands, his face concentrated, hearing the marble rolling inside the invisible spiral, other puzzle boxes on the shelf behind."
    },
    {
        "title": "The Planet Puzzle",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "marbles", "orbits", "tray", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["tray with circular grooves representing planetary orbits", "marbles"],
        "family_friendly": True,
        "original_description": "A tray is engraved with concentric circular grooves representing planetary orbits. Marbles must be maneuvered from the tray's edge into their correct orbital positions without crossing tracks. The puzzle requires steady tilting and minute control of each marble's speed.",
        "modern_description": "A flat tray contains several concentric circular grooves. Place marbles at the edge and maneuver them by tilting the tray so each marble finds and stays in its designated orbital groove. Marbles tend to roll across grooves when given too much momentum. The skill is in imparting just enough motion to settle each marble into its target orbit without disturbing the others already placed.",
        "fun_fact": "The Planet Puzzle reflected the Victorian fascination with astronomy; it was sold at scientific instrument shops alongside telescopes and was considered educational as well as entertaining.",
        "image_prompt": "Victorian parlor table, a wooden tray with concentric circular grooves containing three small marbles being carefully steered into orbits by a tilting hand, astronomical prints of the solar system on the wall behind."
    },
    {
        "title": "The Matrimonial Chair",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "marble", "chair", "box", "trick"],
        "difficulty": "advanced",
        "players": "1",
        "equipment": ["small box with screen and chair figure inside", "marble"],
        "family_friendly": True,
        "original_description": "A box contains a miniature chair figure and marbles representing characters. The object is to seat one marble in the chair without touching it directly. The solution is to isolate the marble, tilt the box, and fillip the bottom sharply to make the marble jump over an internal screen and land on the chair.",
        "modern_description": "A small box has a divider screen and a target seat or cup inside. A marble must be coaxed over the screen and into the 'chair' without being pushed directly. The technique involves tilting the box to position the marble against the screen, then sharply tapping or flipping the bottom of the box to bounce the marble over the top of the screen and into the target position. Extremely satisfying when mastered.",
        "fun_fact": "The Matrimonial Chair is named with Victorian wit—'getting the marble in the chair' was a metaphor for getting a reluctant bachelor to finally commit to marriage, a popular theme in drawing-room humor of the era.",
        "image_prompt": "Victorian puzzle box interior cutaway showing a tiny carved chair and a marble, hands tilting the box at a precise angle, the marble airborne over an internal screen, delicate mechanical illustration, Victorian engineering aesthetic."
    },
    {
        "title": "Bouci-Boula",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "glass-bulb", "pellets", "separation", "color"],
        "difficulty": "advanced",
        "players": "1",
        "equipment": ["double glass bulb with mixed red and white pellets inside"],
        "family_friendly": True,
        "original_description": "A glass toy consisting of two conjoined bulbs contains a mixture of red and white pellets. The player must separate them by color—all red in one bulb, all white in the other—using only gravity and tilting, without any mechanism to sort them directly.",
        "modern_description": "Tilt all pellets into one bulb. Then, by gentle tapping and precise tilting, cause the pellets to sort themselves by color through their different rolling tendencies or through groups. Transfer small groups of same-color pellets at a time, using the narrow neck between bulbs as a filter. An almost meditative puzzle requiring extraordinary patience and observation of how pellets naturally cluster.",
        "fun_fact": "Bouci-Boula puzzles were imported from France in the 1870s-80s and sold at premium prices as drawing-room curiosities; the name is nonsense French invented to give the puzzle a fashionable Parisian sound.",
        "image_prompt": "Victorian dressing table, a glass double-bulb toy held in elegant hands, mixed red and white pellets visible inside, the player tilting it to separate colors, gaslight reflecting in the glass, refined and contemplative atmosphere."
    },
    {
        "title": "The Coin and Card Puzzle",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "coin", "card", "fillip", "physics"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["playing card", "coin"],
        "family_friendly": True,
        "original_description": "Balance a playing card horizontally on one finger. Place a coin flat on top of the card. The challenge is to remove the card without disturbing the coin—which must remain balanced on the finger. The solution is to fillip (flick) the edge of the card sharply so it flies away while the coin stays.",
        "modern_description": "Balance a playing card on one upright finger. Place a coin flat on top of the balanced card. Using the other hand's middle finger (snapped sharply), flick the edge of the card in a fast horizontal stroke. The card flies away cleanly while the coin drops straight down onto the finger it was resting above—inertia keeps the coin from moving sideways. A reliable physics trick.",
        "fun_fact": "This trick demonstrates Newton's First Law of Motion—an object at rest stays at rest unless acted upon by a force. Victorian science teachers used it to explain inertia, and it remains one of the cleanest classroom physics demonstrations.",
        "image_prompt": "Victorian parlor table, one hand balancing a playing card horizontally on a finger with a coin on top, the other hand's finger tensed to flick the card away, an expression of focused concentration, soft light."
    },
    {
        "title": "The Egg and Card Puzzle",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "egg", "card", "ring", "inertia", "physics"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["wine glass half filled with water", "playing card", "small ring", "egg"],
        "family_friendly": True,
        "original_description": "A wine-glass is half filled with water. A playing card is balanced on the glass's rim. A small ring is balanced on the card. An egg is balanced on the ring. The challenge is to remove the card and ring without disturbing the egg—which must fall into the glass of water. Solution: fillip the ring horizontally.",
        "modern_description": "Fill a wine glass halfway. Place a flat card over the top. Balance a small metal ring on the card. Place an egg upright in the ring. Now flick the ring horizontally with a fast snap, which also drags the card. Both card and ring fly away, and the egg drops straight down into the glass of water—its inertia preventing it from following the horizontal motion of the ring and card.",
        "fun_fact": "The egg-and-glass inertia trick appears in almost every Victorian science book under various names; it is a spectacular demonstration of inertia because the egg's relatively large mass makes the result unmistakably dramatic.",
        "image_prompt": "Victorian dining table, a wine glass with water, a card balanced on it, a ring on the card, an egg on the ring—all in a precarious tower—one hand poised with finger to flick the ring, expectant faces watching."
    },
    # Mechanical Puzzles
    {
        "title": "The Barrel and Ball",
        "category": "puzzle",
        "subcategory": "mechanical-puzzle",
        "tags": ["mechanical", "barrel", "ball", "hidden-mechanism", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["boxwood barrel puzzle with marble larger than the hole"],
        "family_friendly": True,
        "original_description": "A boxwood barrel contains a marble or ball apparently too large to pass through the hole in the side. The challenge is to remove the ball without breaking the barrel. The secret: the base is a plug that unscrews when the pestle/ball and plug are gripped together and turned.",
        "modern_description": "Examine the barrel carefully from all angles. The ball appears impossibly large for the hole. Try every possible manipulation—pushing, pulling, turning—before discovering that gripping the ball, the visible plug, and the barrel body together and rotating allows the hidden base plug to unscrew, releasing the ball. A satisfying puzzle because the solution involves understanding that what appears to be decoration is actually a functional element.",
        "fun_fact": "Hidden-mechanism container puzzles were enormously popular gifts in Victorian Britain; the tradition of puzzle boxes and secret-opening containers goes back to Japanese puzzle boxes of the Edo period, which began entering European markets in the 1860s.",
        "image_prompt": "Victorian study table, a polished boxwood barrel puzzle with a marble visible through the side hole, hands examining it carefully from all angles, other wooden puzzle boxes arranged on a shelf behind, afternoon light."
    },
    {
        "title": "The Cage and Ball",
        "category": "puzzle",
        "subcategory": "mechanical-puzzle",
        "tags": ["mechanical", "cage", "ball", "turning", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["turned wooden cage with marble enclosed inside"],
        "family_friendly": True,
        "original_description": "A turned wooden cage appears to have a marble enclosed inside that cannot be removed—the gaps between bars are too small. The secret is that one of the wooden pillars forming the cage can be rotated and withdrawn, opening a gap large enough to release the marble.",
        "modern_description": "Examine the cage puzzle's wooden bars carefully. Try turning and pulling each bar. One pillar turns in its socket and can be drawn upward, leaving a gap through which the marble can pass. Replace the pillar and the cage appears completely solid again. The puzzle works because all pillars look identical, hiding which one is the secret hinge.",
        "fun_fact": "Cage-and-ball puzzles have been made by lathe-turners as demonstrations of woodworking skill since at least the 17th century; 'impossible bottles'—ships or balls inside glass bottles—are their modern equivalent.",
        "image_prompt": "Victorian craftsman's workshop, a beautifully turned wooden cage with a marble visible inside, hands turning one of the pillars to withdraw it, woodworking tools on the bench behind, lathe in the background, warm wood-chip smell implied."
    },
    {
        "title": "The Captive Sixpence",
        "category": "puzzle",
        "subcategory": "mechanical-puzzle",
        "tags": ["mechanical", "coin", "box", "gravity", "trick"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["small brass box with hidden ball mechanism"],
        "family_friendly": True,
        "original_description": "A small box contains a sixpence beneath a depressible top. The top cannot be depressed to release the coin because a hidden ball inside the box blocks the mechanism. The solution is to invert the box so the ball rolls away from the mechanism, then depress the top to release the coin.",
        "modern_description": "The box appears to have a top that should release the trapped coin when pressed, but it won't move. The secret is that inverting the box causes an internal ball to roll to the opposite end, clearing the locking mechanism. While the box is inverted, press the top (now the bottom) to free the coin. A charming puzzle that teaches spatial reasoning about internal mechanisms.",
        "fun_fact": "Captive-coin puzzles were popular Victorian birthday gifts for children; they combined the excitement of a hidden coin with the puzzle of releasing it, making them doubly rewarding.",
        "image_prompt": "Victorian boy holding a small brass puzzle box upside down with one hand while pressing the base with the other finger, a sixpence just beginning to emerge from the opened mechanism, expression of triumph, parlor firelight."
    },
    {
        "title": "The Magic Rings (Hoffmann)",
        "category": "puzzle",
        "subcategory": "wire-puzzle",
        "tags": ["wire-rings", "rings", "linking", "unlinking", "Victorian"],
        "difficulty": "advanced",
        "players": "1+",
        "equipment": ["set of interlocked metal rings"],
        "family_friendly": True,
        "original_description": "A set of metal rings appears to be permanently interlinked. The challenge is to separate them without cutting or bending. The solution depends on correctly identifying a spring-opening ring and the sequence in which the rings must be manipulated to disengage all links without obvious force.",
        "modern_description": "Study all the rings carefully—some may appear identical but one has a hidden spring joint. Find the sequence of moves that opens one ring, threads it through another, and ultimately separates the linked chain. The puzzle rewards methodical exploration rather than brute force. Each ring pair has a specific trick to disengage; rushing causes re-entanglement.",
        "fun_fact": "Metal ring puzzles date to ancient China where they appear in the first century BC; Cardano described a wire ring puzzle in 1550, and Hoffman's 1893 version represents nearly 2000 years of continuous puzzle tradition.",
        "image_prompt": "Victorian puzzle table, a set of interlinked silver metal rings laid out, one player's hands carefully separating two rings using the correct sequence of moves, expression of intense concentration, puzzle books open to ring diagrams behind."
    },
    {
        "title": "The Switchback",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "tube", "shots", "positioning", "tilting"],
        "difficulty": "advanced",
        "players": "1",
        "equipment": ["bent tube with three depressions", "three steel shots (balls)"],
        "family_friendly": True,
        "original_description": "A bent or curved tube has three inner depressions and contains three steel shots. The challenge is to maneuver all three shots simultaneously into their correct depressions—one shot in each hollow—by tilting and turning the tube. Getting the third shot into place without dislodging the first two is the supreme challenge.",
        "modern_description": "Hold the curved tube and tilt it to roll the steel shots along the inside. The depressions are sized so a shot can rest in each. Start with the tube inverted to roll shots into the two outer depressions, then gradually tilt the tube right-side-up to allow the third shot to settle into the central depression without disturbing the others. Requires progressive fine-motor skill.",
        "fun_fact": "The Switchback's name came from the Victorian term for a roller-coaster railway with reversing segments; the tubes' inner curves and the balls' path were thought to mimic the thrilling up-and-down motion of the fairground attraction.",
        "image_prompt": "Victorian child carefully tilting a curved brass tube between careful fingers, three small silver balls visible inside the transparent tube, two already resting in depressions, the third rolling toward the last hollow, focused expression."
    },
    {
        "title": "The Five Horseshoes Puzzle",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["horseshoes", "pellets", "dexterity", "positioning", "Victorian"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["brass box with five horseshoe shapes", "five pellets"],
        "family_friendly": True,
        "original_description": "A brass box contains five horseshoe-shaped channels and five small pellets. The goal is to maneuver one pellet into each horseshoe channel simultaneously by tilting the box. The curved shape of each horseshoe means pellets can roll into or out of position as the box is tilted.",
        "modern_description": "Tilt the brass box to roll pellets across its surface. Each horseshoe-shaped channel curves open at one end, making it easy to roll a pellet in but possible for it to roll out again as the box tilts. The challenge is to settle all five pellets in their five horseshoes simultaneously—correcting one tends to dislodge another. Patience and tiny precise tilts are the key.",
        "fun_fact": "Horseshoe-themed dexterity puzzles were especially popular in mid-Victorian England, when horse racing was the most-watched sport in the country and horseshoe imagery appeared on everything from pub signs to parlor toys.",
        "image_prompt": "Brass box puzzle viewed from above showing five horseshoe-shaped channels, five small silver pellets, two already settled in horseshoes, three still rolling, hands tilting the box at the edges, Victorian gentlemen's study background."
    },
    {
        "title": "The Maze Puzzle Box",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["maze", "pellets", "box", "navigation", "dexterity"],
        "difficulty": "intermediate",
        "players": "1",
        "equipment": ["box with internal maze", "pellets"],
        "family_friendly": True,
        "original_description": "A flat box contains a maze with five pellets that must all be guided into the central compartment through the maze's path. The maze's walls prevent direct movement—pellets must navigate a winding route. Only certain combinations of tilts will navigate the path correctly.",
        "modern_description": "Tilt the maze box to roll pellets through the winding internal path toward the center. The maze walls keep pellets on track but also block wrong turns. Start with one pellet and follow it through to the center, then return the box to the start position for the second pellet. Each pellet shares the same path, so once the route is memorized the challenge becomes doing all five in sequence.",
        "fun_fact": "Maze dexterity puzzles were advertised in Victorian catalogs as training for 'patience and perseverance'—virtues the Victorian middle class considered essential to professional success, making toy mazes both entertainment and character education.",
        "image_prompt": "Victorian puzzle box with a glass top showing the maze interior, a silver pellet visible mid-route through the winding paths, hands tilting the box, other pellets waiting at the start position, afternoon light."
    },
    # Match and Wire Puzzles
    {
        "title": "The Magic Square Match Puzzle",
        "category": "puzzle",
        "subcategory": "match-puzzle",
        "tags": ["matches", "squares", "removal", "spatial", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["12 or more matchsticks"],
        "family_friendly": True,
        "original_description": "Twelve matches are arranged to form a pattern of four squares sharing sides. The challenge is to remove exactly five matches while ensuring that exactly three perfect squares remain. The solution requires choosing which five matches to remove such that three non-overlapping squares survive.",
        "modern_description": "Lay out matches to form a 2x2 grid of four squares (using 12 matches total, with shared sides). Remove exactly 5 matches. The resulting arrangement must show exactly 3 complete squares—no partial squares count. There are several valid solutions; the challenge is finding any one of them by systematic trial and elimination.",
        "fun_fact": "Match puzzles became popular in the 1880s when safety matches became widely available and cheap; they were the first disposable puzzle medium and led directly to the 20th-century tradition of matchstick puzzle books.",
        "image_prompt": "Victorian parlor table, twelve matchsticks arranged in a grid of four squares, five removed matchsticks set aside, the remaining matches forming exactly three complete squares, a puzzle book open nearby with the challenge written out."
    },
    {
        "title": "The Puzzle Purse",
        "category": "puzzle",
        "subcategory": "paper-puzzle",
        "tags": ["paper", "purse", "rings", "folding", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["paper", "rings or coins"],
        "family_friendly": True,
        "original_description": "A paper purse is folded in a specific way with rings inside. The challenge is to open the purse and remove the rings without tearing the paper or forcing any of the rings. The folding creates a trap that seems to make removal impossible through normal means.",
        "modern_description": "Fold a sheet of paper into a purse shape with a specific layering sequence that traps small rings inside. The purse can be opened along one edge without seemingly releasing the rings. The solution requires understanding the topology of the fold—the rings must be worked out through a specific sequence of refolding and threading that reverses the trapping configuration.",
        "fun_fact": "Puzzle purses were fashionable love-tokens in the 17th and 18th centuries, where the correct unfolding sequence revealed a hidden message; by Victorian times they had evolved into pure puzzles, losing their romantic function.",
        "image_prompt": "Victorian parlor table, an ornate folded paper purse with two small metal rings visible inside, hands carefully examining the fold structure trying to work the rings free without tearing, Victorian decorative paper with floral pattern."
    },
    {
        "title": "The Problem of Money (Leap-Frog Coins)",
        "category": "puzzle",
        "subcategory": "counter-puzzle",
        "tags": ["coins", "leap-frog", "counter", "sequence", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["10 half-dimes or small coins"],
        "family_friendly": True,
        "original_description": "Ten half-dimes are laid in a row. Each coin must leap over exactly two others (a single leap over two) to land on a third. By choosing the correct sequence of leaps, all coins can be paired up in five groups of two. The puzzle is to find the correct sequence of moves.",
        "modern_description": "Place 10 small coins in a row with small gaps between them. On each move, pick up one coin and leap it over exactly two others (not one, not three), then place it on the next coin, forming a stack of two. After five moves, you should have five stacks of two coins. The challenge is finding the correct sequence since many attempted orderings lead to dead ends.",
        "fun_fact": "Leap-frog coin puzzles are a subset of 'peg solitaire' logic—the Victorian puzzle-solving community, centered around journals like The Strand Magazine, regularly competed to find the minimum number of moves for such puzzles.",
        "image_prompt": "Victorian parlor table with ten small coins in a row, one coin mid-air being moved to stack on another two positions away, a pencil-drawn diagram of the move sequence beside the coins, concentrated player's hands."
    },
    {
        "title": "The Gordian Knot Puzzle",
        "category": "puzzle",
        "subcategory": "wire-puzzle",
        "tags": ["wire", "knot", "untangling", "topology", "Victorian"],
        "difficulty": "advanced",
        "players": "1+",
        "equipment": ["complex wire or string puzzle in a knotted configuration"],
        "family_friendly": True,
        "original_description": "A complex arrangement of wire or cord appears to be hopelessly tangled or knotted. The challenge is to untangle it entirely without cutting. The solution requires understanding the topology of the tangle and manipulating loops in a specific sequence—there is always a path through the apparent chaos.",
        "modern_description": "Study the wire configuration carefully, looking for where loops pass over or under each other. In wire topological puzzles, there is always a sequence of moves that untangles the apparent knot—though finding the sequence requires visualizing the structure three-dimensionally. Work slowly, reversing any move that tightens the tangle. The answer often requires making it temporarily look worse before it improves.",
        "fun_fact": "The name references the legendary Gordian Knot of Greek myth, cut by Alexander the Great—Victorian puzzle makers used the name to evoke the idea of a puzzle so complex it seems to require a divine solution, while the actual solution was elegantly simple.",
        "image_prompt": "Victorian gentleman's hand holding a complex wire puzzle that appears hopelessly tangled, a diagram in an open puzzle book showing the starting configuration, other untangled wire puzzles in a glass jar on the desk behind."
    },
    {
        "title": "The Drover's Puzzle",
        "category": "puzzle",
        "subcategory": "arithmetical-puzzle",
        "tags": ["arithmetic", "sheep", "counting", "riddle", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["pencil and paper"],
        "family_friendly": True,
        "original_description": "A drover sells sheep from a flock on a series of days, each day selling half the remaining flock plus half a sheep extra. After five or six such days, the flock is exactly exhausted. The puzzle asks: how many sheep did he start with? The answer reveals the elegant pattern of doubling in the solution.",
        "modern_description": "Work backwards: on the last day, the drover sells exactly one sheep (half of one, plus half a sheep). So the day before he had 2. The day before that, he had 4. Continuing backwards: 8, 16, 32, 64... The starting number is 2 to the power of however many days he sold sheep. The 'half a sheep extra' ensures no fractional sheep at any stage—a clever arithmetic construction.",
        "fun_fact": "The Drover's Puzzle belongs to the 'half-plus-half-extra' family of arithmetic riddles that appear in Indian, Chinese, and Arab mathematical texts a thousand years before Hoffmann published his collection.",
        "image_prompt": "Victorian country road, a drover in a smock leading a flock of sheep through a gate, each subsequent gate showing fewer sheep until one remains, illustrated like a strip of mathematical panels, pastoral and whimsical."
    },
    {
        "title": "Three Gentlemen and Servants River Crossing",
        "category": "puzzle",
        "subcategory": "river-crossing-puzzle",
        "tags": ["river-crossing", "logic", "servants", "boat", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["pencil and paper", "tokens"],
        "family_friendly": True,
        "original_description": "Three gentlemen each accompanied by a jealous servant must cross a river using a boat that holds only two. No gentleman can be left with another's servant unless his own servant is present. The puzzle is to devise the crossing sequence that gets all six across while observing this constraint.",
        "modern_description": "Mark six tokens: three gentlemen (G1, G2, G3) and three servants (S1, S2, S3). The boat holds two. G1 may not be alone with S2 or S3 (and similarly for others). Map out a crossing sequence—it takes at least 11 one-way trips. This constraint-satisfaction puzzle rewards systematic enumeration of valid states.",
        "fun_fact": "River-crossing puzzles have been studied since the 8th century when Alcuin of York posed the Farmer, Fox, Chicken, and Grain problem; the Jealous Husbands variant appeared in the 13th century and is a classic of recreational mathematics.",
        "image_prompt": "Victorian puzzle book illustration of a river with a rowboat, six figures divided into three pairs waiting on the bank, a sequence diagram showing the crossing steps, ink illustration with decorative Victorian border."
    },
    {
        "title": "The Dotting Puzzle",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "letters", "pellets", "i-dots", "box"],
        "difficulty": "advanced",
        "players": "1",
        "equipment": ["box with word 'Indivisibility' inscribed", "5 pellets"],
        "family_friendly": True,
        "original_description": "A flat box has the word 'Indivisibility' inscribed across its base, and five small pellets must be positioned to rest on the five dots of the five letter i's in the word. The difficulty is that tilting to position one pellet over an i-dot dislodges pellets already placed on other i-dots.",
        "modern_description": "Tilt the box carefully to roll a pellet over each of the five i-dots in 'Indivisibility.' The letters are positioned so that the i-dots are not all aligned—moving one pellet to its i-dot requires careful angling that risks disturbing previously placed pellets. Work from one end of the word to the other in sequence, making the smallest possible corrective tilts.",
        "fun_fact": "'Indivisibility' was chosen as the word because it contains five i's and has a pleasing irony—the word meaning 'cannot be split' is used in a game where splitting your attention is the key challenge.",
        "image_prompt": "Close-up of a Victorian puzzle box with the word INDIVISIBILITY engraved on the base, five tiny silver pellets, two already resting on i-dots, hands making a precise micro-tilt to position a third, magnified detail view."
    },
    {
        "title": "The Spider and Flies Puzzle",
        "category": "puzzle",
        "subcategory": "dexterity-puzzle",
        "tags": ["dexterity", "spider", "flies", "mercury", "tray"],
        "difficulty": "advanced",
        "players": "1",
        "equipment": ["tray with spider web design", "mercury globule or colored pellets representing flies"],
        "family_friendly": True,
        "original_description": "A tray is decorated as a spider web with a spider at center and colored spots representing flies around the web. A mercury globule (or substitute colored pellet) must be maneuvered to each matching colored spot before being guided to the spider at center—all in one continuous path without retracing.",
        "modern_description": "Tilt the tray to roll the mercury globule or pellet along the web paths. The web's structure means there are fewer valid routes than it first appears. Visit each colored fly spot (matching by color to the globule) before bringing the globule to rest at the center spider. Planning the path in advance avoids dead ends—some routes can't reach all spots without doubling back.",
        "fun_fact": "Mercury-globule dexterity puzzles were sold in apothecary-style packaging in the 1880s as 'scientific toys'; their use of actual liquid mercury would be considered far too hazardous by modern standards, making surviving Victorian examples extremely rare.",
        "image_prompt": "Victorian scientific toy: a glass-covered tray printed with a spider web design, a silvery mercury globule visible on the web, colored spots around the edges, the spider waiting at center, elegant brass frame, collector's item appearance."
    },
    {
        "title": "The Fifteen Puzzle (Hoffmann)",
        "category": "puzzle",
        "subcategory": "sliding-puzzle",
        "tags": ["sliding", "tiles", "fifteen", "sequence", "Victorian"],
        "difficulty": "advanced",
        "players": "1",
        "equipment": ["15-tile sliding puzzle in a 4x4 frame"],
        "family_friendly": True,
        "original_description": "Fifteen numbered tiles are placed in a 4x4 frame with one space empty. Tiles can slide into the empty space but cannot be lifted. The puzzle is to arrange the tiles in numerical order 1-15 from top-left to bottom-right, leaving the empty space at bottom-right. Many scrambled starting positions are impossible to solve.",
        "modern_description": "Slide numbered tiles one at a time into the empty space to rearrange them from their scrambled starting position into numerical order (1-15, left-to-right, top-to-bottom). The challenge is planning multiple moves ahead, as each move affects all future options. Whether a given scrambled arrangement can be solved depends on its parity—half of all scrambled positions are mathematically unsolvable.",
        "fun_fact": "The 15 Puzzle caused a worldwide craze in 1880 when Sam Loyd offered $1,000 for the solution to the impossible 14-15 swap position—knowing it was mathematically unsolvable. Newspapers devoted columns to the puzzle and office workers neglected their duties to work on it.",
        "image_prompt": "Victorian desk with a small 4x4 sliding puzzle in a wooden frame, numbered tiles in a scrambled configuration, one space empty, a newspaper clipping about the puzzle visible beside it, gentleman's hands about to make a move."
    },
    {
        "title": "Arithmetical Puzzle of the Ages",
        "category": "puzzle",
        "subcategory": "arithmetical-puzzle",
        "tags": ["arithmetic", "ages", "algebra", "deduction", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["pencil and paper"],
        "family_friendly": True,
        "original_description": "A classic Victorian number puzzle: a man's age is expressed in relation to other family members with clues like 'my son is one-third my age, and in eight years he will be half my age.' The solver must use simultaneous equations to deduce all ages. A charming introduction to algebraic thinking.",
        "modern_description": "Set up the age-relationship equations from the clues given. For example: if a father is three times the son's age now, and in 12 years the father will be twice the son's age, set up: F=3S and F+12=2(S+12). Solve to find F=36, S=12. Victorian puzzle books had dozens of these charming age puzzles of escalating complexity, from two-person to five-person family situations.",
        "fun_fact": "Age puzzles were the most popular category in Victorian puzzle periodicals because they felt like real-life problems rather than abstract mathematics—a reader could imagine actually needing to work out a relative's age from such clues.",
        "image_prompt": "Victorian family portrait setting, a puzzle scroll beside it showing algebraic equations for father, mother, son, daughter ages, a quill pen solving the simultaneous equations step by step, candlelit study."
    },
    {
        "title": "The Anchored Cane Puzzle",
        "category": "puzzle",
        "subcategory": "mechanical-puzzle",
        "tags": ["mechanical", "cane", "cord", "button-hole", "rope-puzzle"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["walking cane with cord through button hole"],
        "family_friendly": True,
        "original_description": "A loop of cord passes through the button-hole of a coat and its two ends are tied to a walking cane, one at each end. The challenge is to remove the cane from the button-hole without untying the cord or cutting anything. The solution involves looping the cord through the button-hole in the correct sequence.",
        "modern_description": "Thread the loop through the button-hole and tie the cane across the ends outside. To free the cane, push a large loop of the cord through the button-hole from behind, bring this loop up over the cane, and draw it back through the button-hole. This reverses the topology of the entanglement and slides the cane free. Practice with a coat button-hole and a pencil first.",
        "fun_fact": "Coat button-hole string puzzles were extremely popular as pocket puzzles in the Victorian era—a gentleman could produce one from his own coat at any moment to challenge a companion during a carriage ride or between courses at dinner.",
        "image_prompt": "Victorian tailored coat on a stand, a walking cane connected by a loop of cord through the front button-hole, a man's hand beginning to thread the loop in the correct unlocking sequence, detailed illustration of the cord path."
    },
    {
        "title": "Counter Puzzle: Segregation",
        "category": "puzzle",
        "subcategory": "counter-puzzle",
        "tags": ["counters", "sorting", "color-separation", "moves", "Victorian"],
        "difficulty": "intermediate",
        "players": "1+",
        "equipment": ["black and white counters or coins", "row of spaces"],
        "family_friendly": True,
        "original_description": "A row of alternating black and white counters (e.g., six of each) must be rearranged so all blacks are together and all whites are together in the minimum number of moves. Each move slides a pair of adjacent counters (without separating them) to any open position. The puzzle tests planning and visual thinking.",
        "modern_description": "Place 12 counters in alternating colors: B-W-B-W-B-W-B-W-B-W-B-W. Slide pairs of adjacent counters (which may be same-color or mixed) to any gap created by their movement. Aim to reach B-B-B-B-B-B-W-W-W-W-W-W in the fewest moves. The optimal solution requires only 3 moves of pairs. A satisfying puzzle of spatial foresight.",
        "fun_fact": "Counter-segregation puzzles were used by Victorian mathematics teachers to introduce the concept of sorting algorithms long before computers existed; the minimum-move solution is essentially an early version of what computer scientists now call an 'optimal swap sort.'",
        "image_prompt": "Victorian puzzle table, a row of alternating black and white draughts pieces, an arrow showing a pair being slid to a new position, a sequence of diagrams showing the three-move solution, pencil notation beside them."
    },
    {
        "title": "The Tournament Puzzle",
        "category": "puzzle",
        "subcategory": "match-puzzle",
        "tags": ["matches", "triangles", "tournament", "spatial", "Victorian"],
        "difficulty": "beginner",
        "players": "1+",
        "equipment": ["matchsticks"],
        "family_friendly": True,
        "original_description": "Six matchsticks are arranged to form four equilateral triangles using all six sticks—not arranged flat, but in three dimensions. The secret is that a three-dimensional tetrahedron uses all six matches as its six edges, creating four triangular faces.",
        "modern_description": "Take exactly six matchsticks. Arrange them so they form four perfect equilateral triangles simultaneously, using every match as an edge. The flat arrangement seems impossible (you'd need more matches for four separate triangles). The solution is to build a tetrahedron—a triangular pyramid—where each face is a triangle and each edge is one match. The puzzle collapses when you stop thinking in two dimensions.",
        "fun_fact": "This matchstick tetrahedron puzzle was one of the first 'think outside the box' problems documented in puzzle literature; it explicitly teaches that spatial assumptions (we assumed 2D) are the enemy of creative problem-solving.",
        "image_prompt": "Victorian puzzle illustration: on the left, an impossible arrangement of 6 matches in 2D attempting four triangles; on the right, a tetrahedron showing the elegant 3D solution, arrows indicating the insight moment, decorative border."
    },
]

for e in hoffmann_entries:
    if not is_duplicate(e['title']):
        entry_id = make_id(e['title'])
        e['id'] = entry_id
        e['slug'] = entry_id
        e['source_book'] = "Puzzles Old and New"
        e['source_author'] = "Professor Louis Hoffmann"
        e['source_year'] = 1893
        e['source_url'] = "https://archive.org/details/puzzlesoldnew00hoff"
        all_entries.append(e)

print(f"After Hoffmann: {len(all_entries)} entries")

# ============================================================
# MAGICIAN'S OWN BOOK (1862)
# ============================================================
magician_entries = [
    # Sleight of Hand
    {
        "title": "The Flying Dime",
        "category": "magic-trick",
        "subcategory": "coin-trick",
        "tags": ["coin", "vanish", "handkerchief", "hat", "sleight-of-hand"],
        "difficulty": "advanced",
        "players": "Performer + audience",
        "equipment": ["3 dimes", "2 handkerchiefs", "hat", "needle and thread"],
        "family_friendly": True,
        "original_description": "Borrow two handkerchiefs; place two dimes (actually showing only two, hiding a third) into one handkerchief in a hat; secretly sew a third dime into the second handkerchief. A spectator holds the second handkerchief—the dime appears to vanish from it and all three are found in the hat. A hidden needle and thread in the performer's cuff enables the secret stitch.",
        "modern_description": "Secretly palm one extra coin before the trick begins. Show two handkerchiefs and two visible coins. Using a pre-threaded needle hidden in your cuff, quickly sew the secret extra coin into the second handkerchief as you fold it. Drop the two visible coins into the hat inside the first handkerchief. Have an audience member hold the second handkerchief by two corners—the sewn coin is invisible. Shake the handkerchief; the coin seems to vanish. Unfold the first handkerchief to reveal three coins in the hat.",
        "fun_fact": "The Flying Dime appears in The Magician's Own Book (1862), one of the most influential magic books in American history; it was purchased by a young Ehrich Weiss, who would later perform under the name Harry Houdini.",
        "image_prompt": "Victorian stage magician in evening dress holding a handkerchief aloft before an amazed drawing-room audience, a top hat on the table beside them, coins gleaming in the lamplight, dramatic performance pose."
    },
    {
        "title": "The Beads and Strings",
        "category": "magic-trick",
        "subcategory": "string-trick",
        "tags": ["string", "beads", "rope", "vanish", "sleight-of-hand"],
        "difficulty": "intermediate",
        "players": "Performer + 2 audience members",
        "equipment": ["two strings", "several large beads"],
        "family_friendly": True,
        "original_description": "Beads are threaded on two twisted strings tied at their ends. Despite spectators pulling on each end, the beads come off easily—apparently passing through the string. The method: the strings are secretly crossed at the center; a center bead is passed over the hidden juncture and the loops slipped out under cover of the performer's hand.",
        "modern_description": "Thread three or four large beads onto two strings twisted together. Have two audience members each hold one end of the string pair. The beads appear to be held fast on the strings. Under the cover of a magical gesture, cross the strings at their center, slip the key bead over the cross-point, and release the hidden loops. The beads slide free apparently through the solid string.",
        "fun_fact": "The Beads and Strings effect is one of the oldest recorded rope tricks in Western magic literature, appearing in 16th-century conjuring manuscripts; it works because our instinct to assume two separate strings never crosses our mind when they are twisted together.",
        "image_prompt": "Victorian drawing room, a performer threading large wooden beads on two twisted strings held by spectators at each end, one bead mid-motion sliding impossibly off the string, Victorian audience leaning forward in amazement."
    },
    {
        "title": "Ring Through Handkerchief",
        "category": "magic-trick",
        "subcategory": "ring-trick",
        "tags": ["ring", "handkerchief", "vanish", "rod", "sleight-of-hand"],
        "difficulty": "advanced",
        "players": "Performer + audience",
        "equipment": ["handkerchief", "fake wire ring", "real borrowed ring", "rod or wand"],
        "family_friendly": True,
        "original_description": "A borrowed ring vanishes from a tied handkerchief and appears on a rod held by spectators. The method uses a fake sharpened wire ring that can be pulled through the handkerchief fabric; the real ring is secretly slipped onto the rod, which spectators are already holding.",
        "modern_description": "Before the trick, secretly place the real borrowed ring onto a wand that spectators will hold. Show a duplicate fake ring (a ring-shaped wire that unbends). Wrap it in the handkerchief making sure spectators feel a ring shape inside. Make the pass—draw the wire ring out through the fabric (leaving a small hole closed by the fabric's stretch). Reveal the handkerchief empty; have spectators examine their wand, where the 'borrowed' ring has appeared.",
        "fun_fact": "Ring vanish-and-travel tricks like this one are considered the oldest documented class of magic trick; ancient texts from Egypt and Rome describe ring vanishing acts performed at public gatherings over two thousand years ago.",
        "image_prompt": "Victorian parlor, a performer dramatically shaking an empty handkerchief while two seated spectators discover a golden ring threaded onto the wand they have been holding the entire time, expressions of total astonishment."
    },
    {
        "title": "The Magic Bond",
        "category": "magic-trick",
        "subcategory": "escape-trick",
        "tags": ["string", "hand", "escape", "sleight-of-hand", "loop"],
        "difficulty": "intermediate",
        "players": "Performer + audience",
        "equipment": ["length of string or cord"],
        "family_friendly": True,
        "original_description": "A string is arranged in a loop around the performer's hand in a way that appears to securely bind it. When the performer pulls the string, it slips off entirely in a way that seems impossible. The secret lies in the specific initial arrangement of the string over the fingers which creates a self-releasing configuration.",
        "modern_description": "Loop the string around your hand using the specific arrangement: pass the string over the back of the hand, around the thumb, under the palm, and over specific fingers in sequence. When done correctly, pulling both string ends causes all loops to release simultaneously in a single smooth motion, leaving your hand completely free. Have an audience member first examine the bound hand to confirm it looks genuinely tied.",
        "fun_fact": "Escape-from-rope tricks were the bread-and-butter of Victorian conjurors—before Houdini elevated the escape act to spectacle, rope-release was considered a parlor curiosity. These tricks fascinated Houdini from his reading of The Magician's Own Book as a boy.",
        "image_prompt": "Victorian performer holding out a hand apparently bound by rope, audience leaning in to verify it's tied, the performer's other hand poised to pull the string end, theatrical gaslight illumination, drawing room setting."
    },
    {
        "title": "The Old Man and His Chair",
        "category": "magic-trick",
        "subcategory": "string-trick",
        "tags": ["string", "figures", "finger-play", "storytelling", "children"],
        "difficulty": "intermediate",
        "players": "Performer",
        "equipment": ["string loop"],
        "family_friendly": True,
        "original_description": "A string is manipulated through specific finger-loop sequences while the performer narrates a story. The string takes on the shapes of candles, a chair, scissors, and finally a policeman's staff—one figure flowing into the next as the story progresses. A complete narrative told entirely through finger-string figures.",
        "modern_description": "Loop a string over both hands and manipulate it through a series of precisely described finger moves that produce each figure in the story: candles (two upright loops), a chair (a flat seat between vertical back loops), scissors (an X-cross between finger loops), and a staff (a single diagonal). The story—about an old man preparing for bed—gives cues for each transformation. A captivating performance for children.",
        "fun_fact": "String figure storytelling traditions exist on every inhabited continent; the Victorian parlor version of the Old Man and Chair is a European adaptation of finger-string art found in Indigenous traditions from Alaska to Polynesia.",
        "image_prompt": "Victorian performer's hands forming elaborate shapes with a loop of string, the current figure showing a chair formed from string against a gaslit drawing room background, a child audience member watching entranced, hands magnified for clarity."
    },
    {
        "title": "The Magic Handcuffs",
        "category": "magic-trick",
        "subcategory": "escape-trick",
        "tags": ["handc