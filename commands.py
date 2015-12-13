# -*- coding: utf-8 -*-
import os
import fourchan_json
import random
import string
import re
import time
import requests
import praw
#from hackn import HN

user_agent = ("get_random_post from subreddit for IRC")
r = praw.Reddit(user_agent=user_agent)
#hn = HN()

class tcol:
        NORMAL = "\u000f"
        BOLD = "\u0002"
        UNDERLINE = "\u001f"
        REVERSE = "\u0016"
        WHITE = "\u00030"
        BLACK = "\u00031"
        DARK_BLUE = "\u00032"
        DARK_GREEN = "\u00033"
        RED = "\u00034"
        BROWN = "\u00035"
        GREEN = "\u00039"


def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    xfile = open(file_name)
    xfile.seek(random_point)
    c = xfile.read(1)
    s = ""
    while c != ".":
        c = xfile.read(1)

    xfile.read(1)
    c = xfile.read(1)
    while c == ".":
        xfile.read(1)
    while c != ".":
        if c != "\n":
            if c != "\r":
                s += c
            else:
                s += " "
        else:
            s += " "
        c = xfile.read(1)
    s += c
    c = xfile.read(1)
    s += c
    while c == ".":
        s += c
        c = xfile.read(1)
    s.replace("- ", " ")
    s = re.sub('\s+', ' ', s)
    return s


def getuser(ircmsg):
    return ircmsg.split(":")[1].split('!')[0]


_command_dict = {}


def command(name):
    # The decorator appending all fn's to a dict
    def _(fn):
        # Decorators return an inner function whom we
        # pass the function.
        _command_dict[name] = fn
    return _


def nothing(args):
    return ""


def get_command(name):
    # Explicity over implicity?
    # Fuck that

    # We just lower the string.
    # and check later its upper cased
    if name.lower() in _command_dict:
        return _command_dict[name.lower()]
    else:
        return nothing


def twitter(args):
    if type(args) is not str:
        tweet = " ".join(args["args"])
        sendmsg = args["sendmsg"]
        channel = args["channel"]
    else:
        tweet = args
    r = requests.post("http://carta.im/tweetproxy/", data={'tweet': tweet})
    if "200" in r.text:
        return ":DDD brought to you by @proxytwt"
    else:
        return ":( pls fix me ;-;"


@command("tweet")
def tweet(args):
    return twitter(args)

@command("shitpost")
def shitposting(args):  # almost entirely automated shitposting
    if " ".join(args["args"]) == "| tweet":
        directory = os.path.dirname(__file__)
        with open(directory + "/shitpost.txt", 'r') as twit:
            shitpost = twit.read()[0:140]
        return twitter(shitpost)

    shitpost = fourchan_json.get_random_post(args)
    shitpost = shitpost.split("\x0f")
    res_shitpost = []
    for l in shitpost:
        if l.strip().startswith(">"):
            l = tcol.DARK_GREEN + l
        res_shitpost.append(l)
    shitpost = "\x0f".join(res_shitpost)

    if args["command"].isupper():
        shitpost = shitpost.upper()
    directory = os.path.dirname(__file__)
    with open(directory + "/shitpost.txt", 'w') as tweet:
        tweet.write(shitpost)
    return shitpost

@command("le")
def reddit(args):
    new_args = args["args"]

    subreddit = "linuxcirclejerk"
    if new_args:
        subreddit = new_args[0]

    rando_list = []

    while True:
        try:
            subr = r.get_random_submission(subreddit)
        except: pass
        finally: break

    if not subr:
        reddit(args)

    if not subr.comments and not subr.selftext:
        reddit(args)

    if subr.comments:
        subr.replace_more_comments(limit=None, threshold=0)
    else:
        return subr.selftext

    flat_comments = praw.helpers.flatten_tree(subr.comments)

    rando_list.append(subr.selftext)
    for comment in flat_comments:
        if comment.body:
            rando_list.append(comment.body)
    if rando_list:
        if len(rando_list) < 2:
            reddit(args)
    if not rando_list:
        reddit(args)
    choice_post = None
    while not choice_post:
        choice_post = random.choice(rando_list).replace('\n', ' ')

    #if len(choice_post) > 500:
     #   return choice_post[:480] + " " + subr.short_link
    #else:
    return choice_post

#@command("hn")
#def hackernews(args):

#    comments = []

 #   for story in hn.get_stories(story_type='newest', limit=120):
  #      for comment in story.get_comments():
  #          comments.append(comment.body)

   # comment = random.choice(comments)

   # return comment.replace('\n', ' ')


@command("cybhelp")
def halp(args):
    user = getuser(args["raw"])
    string = user + ", sending you a private message of my commands.\n"
    args["sendmsg"](user, "ur a faget")
    return string


@command("interject")
def interjection(args):  # I'd just like to interject for a moment
    str = ("I'd just like to interject for moment. What you're referring to as "
              "Linux, is in fact, GNU/Linux, or as I've recently taken to calling it,"
              " GNU plus Linux. pastebin.com/2YxSM4St\n")
    return str


@command("git")
def git(args):
    str = "https://github.com/cybits/cybot What are we going to do on the repo? waaaah fork =3\n"
    return str
@command("reminder")
def reminder(args):  # today, I will remind them
    return ('Remember to fix your posture :D http://gateway.ipfs.io/ipfs/QmR91KZ77KMg1h8HqBTxtHNZiWCECiXhHkTR7coVqyyFvF/posture.jpg\n')

@command("memearrows")
def memearrows(args):  # >implying you can triforce
    str = ("Meme arrows are often used to preface implications or feels. See "
              "also: implying, feel.\n")
    return str


@command("int")
def intensifies(args):  # [python intensifies]
    if args["args"]:
        ret = "[" + " ".join(args["args"]) + " intensifies]\n"
    else:
        ret = "[no argument intensifies]\n"
    if args["command"].isupper():
        return ret.upper()
    else: return ret


# TODO: Use for something
def hello(user):  # This function responds to a user that inputs "Hello cybits"
    # random.randint(0, 5)
    str = ("are you even cyb, " + user + "?\n")
    return str


@command("ayylmao")
def ayylmao(args):
    import time
    sendmsg = args["sendmsg"]
    line = ('ABDUCTION: INCOMING')

    ayylien = ["       .-""""-.        .-""""-.    ",
               "      /        \      /        \   ",
               "     /_        _\    /_        _\  ",
               "    // \      / \\  // \      / \\ ",
               "    |\__\    /__/|  |\__\    /__/| ",
               "     \    ||    /    \    ||    /  ",
               "      \        /      \        /   ",
               "       \  __  /        \  __  /    ",
               "        '.__.' ayy lmao '.__.'     "]


    ircmsg = args["raw"]
    user = ircmsg.split(":")[1].split('!')[0]
    channel = args["channel"]
    sendmsg(channel, line)
    for lines in ayylien:
        sendmsg(user, lines)
        time.sleep(1)
   # ayy lmao
   # Doing all the logic inside the function
   # Since sendmsg wont post empty strings.
    return ""

@command("feel")
def feel(args):  # >tfw
    import time
    sendmsg = args["sendmsg"]
    line = ('"tfw no gf" is an abbreviated expression for "that feeling [I get] '
              'when [I have] no girlfriend" often used in online discussions and '
              'comments.')

    feelguy  = ["░░░░░░░▄▀▀▀▀▀▀▀▀▀▀▄▄░░░░░░░░░",
                "░░░░▄▀▀░░░░░░░░░░░░░▀▄░░░░░░░",
                "░░▄▀░░░░░░░░░░░░░░░░░░▀▄░░░░░",
                "░░█░░░░░░░░░░░░░░░░░░░░░▀▄░░░",
                "░▐▌░░░░░░░░▄▄▄▄▄▄▄░░░░░░░▐▌░░",
                "░█░░░░░░░░░░░▄▄▄▄░░▀▀▀▀▀░░█░░",
                "▐▌░░░░░░░▀▀▀▀░░░░░▀▀▀▀▀░░░▐▌░",
                "█░░░░░░░░░▄▄▀▀▀▀▀░░░░▀▀▀▀▄░█░",
                "█░░░░░░░░░░░░░░░░▀░░░▐░░░░░▐▌",
                "▐▌░░░░░░░░░▐▀▀██▄░░░░░░▄▄▄░▐▌",
                "░█░░░░░░░░░░░▀▀▀░░░░░░▀▀██░▀▄",
                "░▐▌░░░░▄░░░░░░░░░░░░░▌░░░░░░█",
                "░░▐▌░░▐░░░░░░░░░░░░░░▀▄░░░░░█",
                "░░░█░░░▌░░░░░░░░▐▀░░░░▄▀░░░▐▌",
                "░░░▐▌░░▀▄░░░░░░░░▀░▀░▀▀░░░▄▀░",
                "░░░▐▌░░▐▀▄░░░░░░░░░░░░░░░░█░░",
                "░░░▐▌░░░▌░▀▄░░░░▀▀▀▀▀▀░░░█░░░",
                "░░░█░░░▀░░░░▀▄░░░░░░░░░░▄▀░░░",
                "░░▐▌░░░░░░░░░░▀▄░░░░░░▄▀░░░░░",
                "░▄▀░░░▄▀░░░░░░░░▀▀▀▀█▀░░░░░░░",
                "▀░░░▄▀░░░░░░░░░░▀░░░▀▀▀▀▄▄▄▄▄"]


    ircmsg = args["raw"]
    user = ircmsg.split(":")[1].split('!')[0]
    channel = args["channel"]
    sendmsg(channel, line)
    for lines in feelguy:
        sendmsg(user, lines)
        time.sleep(1)
    # Doing all the logic inside the function
    # Since sendmsg wont post empty strings.
    return ""

@command("wake")
def wake(args):
    return "(can't wake up)"


# TODO: Use this for something
def autointerject(args):  # making sure users don't forget the GNU
    str1 = ("I'd just like to interject for moment. What you're referring to as Linux, is in fact, "
            "GNU/Linux - further messages sent privately.\n")

    str2 = ("I'd just like to interject for moment. What you're referring to as Linux, is "
            "in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux "
            "is not an operating system unto itself, but rather another free component of a fully"
            " functioning GNU system made useful by the GNU corelibs, shell utilities and vital "
            "system components comprising a full OS as defined by POSIX.\n"
            "Many computer users run a modified version of the GNU system every day, "
            "without realizing it. Through a peculiar turn of events, the version of GNU "
            "which is widely used today is often called Linux, and many of its users are not"
            " aware that it is basically the GNU system, developed by the GNU Project.\n"
            "There really is a Linux, and these people are using it, but it is just a "
            "part of the system they use. Linux is the kernel: the program in the system "
            "that allocates the machine's resources to the other programs that you run. "
            "The kernel is an essential part of an operating system, but useless by "
            "itself; it can only function in the context of a complete operating "
            "system.\n"
            "Linux is normally used in combination with the GNU operating system: the "
            "whole system is basically GNU with Linux added, or GNU/Linux. All the "
            "so-called Linux distributions are really distributions of GNU/Linux!\n")

    return str1, str2


@command("implying")
def implying(args):  # >implying this needs a comment
    return ('>implying is used in a mocking manner to challenge an "implication" '
            'that has been made, or sometimes it can be simply used as a joke in '
            'itself.\n')


@command("lit")
def sentence(args):  # This function grabs a random sentence from a txt file and posts it to the channel
    directory = os.path.dirname(__file__)
    directory = directory + os.path.join("/texts/books/")
    line = directory + os.path.join(random.choice(os.listdir(directory)))
    return get_random_line(line) + "\n"
    # return get_random_line(random.choice(os.listdir("/home/polaris/PycharmProjects/cybot/texts/"))) + "\n"

@command("guinea")
def guinea(args):
    directory = os.path.dirname(__file__)
    guinea = directory + os.path.join("/texts/other/guinea.txt")
    return random.choice(list(open(guinea)))

@command("checkem")
def checkem(args):
    not_dubs = random.randint(0, 99)
    return str(not_dubs).zfill(2)

@command("terry")
def terry(args):  # Grabs a random Terry quote from the 9front list
    directory = os.path.dirname(__file__)
    terry = directory + os.path.join("/texts/other/terry.txt")
    return random.choice(list(open(terry)))

@command("rob")
def pike(args):
    directory = os.path.dirname(__file__)
    pike = directory + os.path.join("/texts/other/rob.txt")
    return random.choice(list(open(pike)))

@command("gene")
def ray(args):
    directory = os.path.dirname(__file__)
    ray = directory + os.path.join("/texts/other/timecube.txt")
    return random.choice(list(open(ray)))

@command("linus")
def torv(args):
    directory = os.path.dirname(__file__)
    torv = directory + os.path.join("/texts/other/linus.txt")
    return random.choice(list(open(torv)))

@command("rms")
def stallman(args):
    directory = os.path.dirname(__file__)
    richard = directory + os.path.join("/texts/other/stallman.txt")
    return random.choice(list(open(richard)))

@command("eightball")
def eight(args):
    directory = os.path.dirname(__file__)
    eight = directory + os.path.join("/texts/other/eightball.txt")
    return random.choice(list(open(eight)))

@command("triforce")
def coolt(args):
    sendmsg = args["sendmsg"]
    spaces1 = random.randint(1,5)
    spaces2 = random.randint(1,3)
    string1 = (" "*spaces1 + ("▲"))
    string2 = (" "*spaces2 + ("▲ ▲"))
    return string1, string2


@command("booty")
def booty(args):
    return "( ͡° ͜ʖ ͡°)"


@command("shrug")
def shrug(args):
    return "¯\_(ツ)_/¯"

@command("denko")
def denko(args):
    return "(´･ω･`)"


@command("cute")
def cute(args):
    user = getuser(args["raw"])
    args = args["args"]
    if len(args) < 1:
        cutelist = ["✿◕ ‿ ◕✿", "❀◕ ‿ ◕❀", "(✿◠‿◠)",
                    "(◕‿◕✿) ", "( ｡◕‿◕｡)", "(◡‿◡✿)",
                    "⊂◉‿◉つ ❤", "{ ◕ ◡ ◕}", "( ´・‿-) ~ ♥",
                    "(っ⌒‿⌒)っ~ ♥", "ʕ´•ᴥ•`ʔσ”", "(･Θ･) caw",
                    "(=^･ω･^)y＝", "ヽ(=^･ω･^=)丿", "~(=^･ω･^)ヾ(^^ )",
                    "| (•□•) | (❍ᴥ❍ʋ)", "ϞϞ(๑⚈ ․̫ ⚈๑)∩", "ヾ(･ω･*)ﾉ",
                    "▽・ω・▽ woof~", "(◎｀・ω・´)人(´・ω・｀*)", "(*´・ω・)ノ(-ω-｀*)",
                    "(❁´ω`❁)", "(＊◕ᴗ◕＊)", "{´◕ ◡ ◕｀}", "₍•͈ᴗ•͈₎",
                    "(˘･ᴗ･˘)", "(ɔ ˘⌣˘)˘⌣˘ c)", "(⊃｡•́‿•̀｡)⊃", "(´ε｀ )♡",
                    "(◦˘ З(◦’ںˉ◦)♡", "( ＾◡＾)っ~ ❤ Leper",
                    "╰(　´◔　ω　◔ `)╯", "(*･ω･)", "(∗•ω•∗)", "( ◐ω◐ )"]
    else:
        args = " ".join(args)
        cutelist = ["(✿◠‿◠)っ~ ♥ " + args, "⊂◉‿◉つ ❤ " + args, "( ´・‿-) ~ ♥ " + args,
                    "(っ⌒‿⌒)っ~ ♥ " + args, "ʕ´•ᴥ•`ʔσ” BEARHUG " + args,
                    user + " ~(=^･ω･^)ヾ(^^ ) " + args, user + " (◎｀・ω・´)人(´・ω・｀*) " + args,
                    user + " (*´・ω・)ノ(-ω-｀*) " + args,
                    user + " (ɔ ˘⌣˘)˘⌣˘ c) " + args,
                    "(⊃｡•́‿•̀｡)⊃ U GONNA GET HUGGED " + args, args + " (´ε｀ )♡",
                    user + " (◦˘ З(◦’ںˉ◦)♡ " + args, "( ＾◡＾)っ~ ❤ " + args]
    return random.choice(cutelist)

@command("bots")
def bots(args):
    return "Reporting in! [Python] Try .cybhelp for commands."

@command("spikehog")
def spikehog(args):
    directory = os.path.dirname(__file__)
    spikehog = directory + os.path.join("/texts/other/spikehog.txt")
    return random.choice(list(open(spikehog)))

@command("hackers")
def hackers(args):
    directory = os.path.dirname(__file__)
    hackers = directory + os.path.join("/texts/other/hackers.txt")
    return random.choice(list(open(hackers)))

@command("noided")
def noided(args):
    directory = os.path.dirname(__file__)
    noided = directory + os.path.join("/texts/other/grips.txt")
    return random.choice(list(open(noided)))

@command("just")
def just(args):
	return "DO IT", "JUST DO IT", "DON'T LET YOUR DREAMS BE DREAMS", "YESTERDAY YOU SAID TOMORROW", "SO JUST-", "DO IT", "MAKE YOUR DREAMS COME TRUE", "JUST-DO IT", "YES YOU CAN", "JUST DO IT", "If you are tired of starting over, stop giving up", "*flexes*"

@command("spooky")
def spooky(args):
    directory = os.path.dirname(__file__)
    spook = directory + os.path.join("/texts/other/spooks")
    return random.choice(list(open(spook)))

def breaklines(str):  # This function breaks lines at \n and sends the split lines to where they need to go
    strarray = string.split(str, "\n")
    return strarray
