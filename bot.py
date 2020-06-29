import re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from github import get_user_stats, checkAccount, save_json
import base64
from time import sleep


tf = open('token.txt', 'r')
TOKEN = tf.read()

NAME, EMAIL, GENDER, BRANCH, YEAR, HOSTEL, HOSTELADDR, CLUBS, GITHUB, LANG, PHOTO, BIO, QUERY, QUESTION, UPLOAD = range(15)

SaveInfo = dict()


def hello(update, context):
    update.message.reply_text('Hello! {}'.format(update.message.from_user.first_name))


def start(update, context):
    update.message.reply_text(
        '{} Please start conversation with me by typing /intro '.format(update.message.from_user.first_name))


def getInfo(update, context):
    update.message.reply_text(
        'Hi! My name is Exodus.'
        'Send /cancel to stop this interaction.\n\n'
        'What\'s your name ?')

    return NAME


def username(update, context):
    user = update.message.from_user
    username = update.message.text
    SaveInfo.update({'Fullname': username})
    update.message.reply_text('Nice to meet you {}. \nNow Please, provide your email-id.'.format(user.first_name))

    return EMAIL


def email(update, context):
    gen_kb = [['Male', 'Female', 'Others']]
    user = update.message.from_user
    SaveInfo.update({'Email': update.message.text})
    update.message.reply_text('Nice to meet you {}. \nNow Please, provide your gender.'.format(user.first_name),
                              reply_markup=ReplyKeyboardMarkup(gen_kb, one_time_keyboard=True, resize_keyboard=True))

    return GENDER


def gender(update, context):
    branch_kb = [['CSE', 'ME', 'EE', 'ECE', 'CE']]
    gen = update.message.text
    SaveInfo.update({'Gender': gen})
    update.message.reply_text(
        'In which branch you are currently studying? ',
        reply_markup=ReplyKeyboardMarkup(branch_kb, one_time_keyboard=True, resize_keyboard=True)
    )

    return BRANCH


def branch(update, context):
    year_kb = [['1st', '2nd', '3rd', '4th']]
    SaveInfo.update({'Branch': update.message.text})
    update.message.reply_text('Awesome! \n'
                              'Now tell me, in which year you are studying?',
                              reply_markup=ReplyKeyboardMarkup(year_kb, one_time_keyboard=True, resize_keyboard=True))

    return YEAR


def year(update, context):
    hostel_kb = [['Yes', 'No']]
    SaveInfo.update({'Year': update.message.text})
    update.message.reply_text('Are you staying in college hostel ?',
                              reply_markup=ReplyKeyboardMarkup(hostel_kb, one_time_keyboard=True, resize_keyboard=True))
    return HOSTEL


def isHostel(update, context):
    is_hostel = update.message.text
    if is_hostel == 'Yes':
        update.message.reply_text('Please provide the hostel number and room number in which you are staying.\n'
                                  'Eg: B.H 8, Room: 401', )
        return HOSTELADDR
    else:
        SaveInfo.update({'Hostel': None})
        update.message.reply_text('Ok! Moving on....')
        sleep(1)
        update.message.reply_text('Nice!\n\nIn which other clubs you are currently a member or wanna be a member\n'
                                'Speak Truth, the admins will eventually know, so no hiding! '
                                'Write \'None\' if not any'
    )
    
    return CLUBS


def hostelAddr(update, context):
    hstelAddr = update.message.text
    if hstelAddr is not None:
        SaveInfo.update({'Hostel': hstelAddr})
    update.message.reply_text('Ok! Moving on....')
    sleep(1)
    update.message.reply_text('Nice!\n\nIn which other clubs you are currently a member or wanna be a member\n'
                                'Speak Truth, the admins will eventually know, so no hiding! \n\n'
                                'Write \'None\' if not any'
    )
    
    return CLUBS
    

def otherClubs(update, context):
    club = update.message.text
    if club == 'None':
        SaveInfo.update({'Other Clubs': None})
        update.message.reply_text('Nice!\n\nNow provide your github account link. '
                                    'A github account url looks like this:\n'
                                    'https://github.com/<your-username> \n'
                                    'If you don\'t provide any, you aren\'t be allowed to join CODEX. '
                                    'So, if you don\'t have an account, go create one right now! and then write it down. \n'
                                    'Click Here: https://github.com/join')
        return GITHUB
    else:
        SaveInfo.update({'Other Clubs': club})
        update.message.reply_text('Nice!\n\nNow provide your github account link. '
                                    'A github account url looks like this:\n'
                                    'https://github.com/<your-username> \n'
                                    'If you don\'t provide any, you aren\'t be allowed to join CODEX. '
                                    'So, if you don\'t have an account, go create one right now! and then write it down. \n'
                                    'Click Here: https://github.com/join')
        return GITHUB


def github(update, context):
    lang_kb = [['C', 'Java', 'Python', 'Javascript'], ['Go', 'Ruby', 'HTML', 'PHP', 'R']]
    
    name_provided = SaveInfo.get('Fullname')
    github_url = str(update.message.text)
    
    if github_url.count('github.com/') == 1 and checkAccount(name_provided, github_url) :
        SaveInfo.update({'GitHub': github_url})
        
        username = str((re.search(r'(\w+)$', github_url)).group(1))
        github_bio = get_user_stats(username, 'bio')
        github_comp = get_user_stats(username, 'company')
        
        if github_bio != None:
            update.message.reply_text('Your GitHub Bio: {} \nThat\'s Awesome!'.format(github_bio))
            sleep(1)
        if github_comp != None:
            update.message.reply_text('You are currently working in : {} \nKeep up the good work there!'.format(github_comp))
            sleep(1)
        update.message.reply_text('Now, this the most important stuff. '
                                  'Which programming language you love to code mostly ? \n'
                                  'send /skip if you don\'t know any.',
                                  reply_markup=ReplyKeyboardMarkup(lang_kb, one_time_keyboard=True,
                                                                   resize_keyboard=True)
                                  )

        return LANG
    else:
        SaveInfo.update({'GitHub': None})
        update.message.reply_text('You didn\'t provide your github account link or didn\'t provide your name properly when I asked you first.\n'
                                  'Why are you so dumb? \n'
                                  'That\'s fine I won\'t ask for it again.\n\n'
                                  'The admins will deal with you later. \n'                                  
                                  'Now, this the most important stuff. \n'
                                  'Which programming language you love to code mostly ? \n'
                                  'send /skip if you don\'t know any.',
                                  reply_markup=ReplyKeyboardMarkup(lang_kb, one_time_keyboard=True,
                                                                   resize_keyboard=True)
                                  )

        return LANG


def lang(update, context):
    
    SaveInfo.update({'Language': update.message.text})
    update.message.reply_text('Well! that\'s a nice choice!\n\n'
                              'Now can you send me a photo of yours ?\n'
                              'So that next time we meet I can recognize you.'
                              'send /skip if you don\'t want',
                              reply_markup=ReplyKeyboardRemove()
                              )

    return PHOTO


def skip_lang(update, context):
    
    SaveInfo.update({'Language': None})
    update.message.reply_text('Hey!! that\'s so dumb \n'
                              'Now can you send me a photo of yours ?\n'
                              'So that next time we meet I can recognize you. '
                              'send /skip if you don\'t want',
                              reply_markup=ReplyKeyboardRemove()
                              )

    return PHOTO


def photo(update, context):
    
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('photo.jpg')
    update.effective_message.reply_text('Processing your image....')
    with open("photo.jpg", "rb") as imageFile:
        imgstr = str(base64.b64encode(imageFile.read()))
        SaveInfo.update({'UserImageArray': imgstr})
    update.message.reply_text('Gorgeous! Now, tell me something about yourself, \n'
                              'send /skip if you don\'t want to.')

    return BIO


def skip_photo(update, context):
    
    SaveInfo.update({'UserImageArray': None})
    update.message.reply_text('Now, tell me something about yourself, \n'
                              'send /skip if you don\'t want to.')

    return BIO


def bio(update, context):
    isQuery_kb = [['Yes', 'No']]
    user = update.message.from_user
    SaveInfo.update({'Bio': update.message.text})
    update.message.reply_text('Do you have any query related to our CODEX club? \n\nYou can ask me, the admins will answer you later.', 
                                reply_markup=ReplyKeyboardMarkup(isQuery_kb, one_time_keyboard=True, resize_keyboard=True))
    
    return QUERY


def skip_bio(update, context):
    query_kb = [['Yes', 'No']]
    user = update.message.from_user
    SaveInfo.update({'Bio': None})
    update.message.reply_text('Do you have any query related to our CODEX ?',
                                reply_markup=ReplyKeyboardMarkup(query_kb, one_time_keyboard=True, resize_keyboard=True))
    
    return QUERY


def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    SaveInfo.clear
    return ConversationHandler.END


def isquery(update, context):
    query = update.message.text
    user = update.message.from_user
    if query != 'Yes':
        filename = str(user.first_name) + str(user.last_name)
        SaveInfo.update({'query': None})
        
        update.message.reply_text(
            'It was pleasure talking with you, {}\n\nStay well, Stay Safe!! \nHave a nice day!'.format(user.first_name))
        
        save_json(filename, SaveInfo)
        return UPLOAD
    else:
        update.message.reply_text('What do you wanna know ?')
        return QUESTION


def question(update, context):
    user = update.message.from_user
    filename = str(user.first_name) + str(user.last_name)
    SaveInfo.update({'query': update.message.text})
    update.message.reply_text('Your query has been saved successfully. \nThe admins will later get onto you, if they want.')
    update.message.reply_text(
            'It was pleasure talking with you, {}\n\nStay well, Stay Safe!! \nHave a nice day!'.format(user.first_name))
    save_json(filename, SaveInfo)
    return UPLOAD


# this function is not uploading the file , but exits the conversation correctly
def uploadJson(update, context):
    Chatbot = Bot
    chat = update.effective_chat
    user = update.message.from_user
    filename = filename = str(user.first_name) + str(user.last_name) + '.json'
    Chatbot.sendDocument(chat_id=chat.id, document=open(filename, 'rb'))
    SaveInfo.clear

    return ConversationHandler.END


def bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add conversation handler with the states PHOTO, BRANCH, YEAR, LANG
    conv_handler = ConversationHandler(

        # define entry points from where your conversation will proceed
        entry_points=[CommandHandler('intro', getInfo)],

        # define the various states/stages through which your conversation will proceed
        states={

            NAME: [MessageHandler(Filters.text, username)],

            EMAIL: [MessageHandler(Filters.text, email)],

            GENDER: [MessageHandler(Filters.regex('^(Male|Female|Others)$'), gender)],

            BRANCH: [MessageHandler(Filters.regex('^(CSE|ME|EE|ECE|CE)$'), branch)],

            YEAR: [MessageHandler(Filters.regex('^(1st|2nd|3rd|4th)$'), year)],
            
            HOSTEL: [MessageHandler(Filters.regex('^(Yes|No)$'), isHostel)],
            HOSTELADDR: [MessageHandler(Filters.text, hostelAddr)],

            CLUBS: [MessageHandler(Filters.text, otherClubs)],
            
            GITHUB: [MessageHandler(Filters.text, github)],

            LANG: [MessageHandler(Filters.regex('^(C|Java|Python|HTML|Go|Ruby|Haskell|PHP|R)$'), lang),
                   CommandHandler('skip', skip_lang)],

            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],

            BIO: [MessageHandler(Filters.text, bio), CommandHandler('skip', skip_bio)],

            QUERY: [MessageHandler(Filters.regex('^(Yes|No)$'), isquery)],

            QUESTION: [MessageHandler(Filters.text, question)],

            UPLOAD: [CommandHandler('upload', uploadJson)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    bot()
