from difflib import get_close_matches
from recommendations import recommendations, recommendation_list, get_course_names

courses = recommendations['course']['options']

greeting = '''Hello %s, my name is MyCI. I am a chatbot that can help you find recommendations around campus with the help of other students.
/menu to get the menu'''

myci_menu = '''Hello %s
/addpreference to add courses to your preference list
/remove to remove a course from your list
/display to display your current preferences
/recommend to ask request course recommendation
/points to check your current points
/cancel to stop the chat'''

greeting1 = '''Hello %s, Welcome back. Type in the courses that you would like to add to your preference list'''

# pending course confirmations for users
pending = {}


def start_model(ctx):
    reply = greeting % (ctx.user.name)
    ctx.reply(reply)
    ctx.user.set_state('modeling')
    ctx.reply(recommendations['course']['question'])


def start_addpreference(ctx):
    reply = greeting1 % (ctx.user.name)
    ctx.reply(reply)
    ctx.user.set_state('modeling')


def start_displaypreference(ctx):
    if len(ctx.user.preferences['course']) > 0:
        reply = '''Your preferences list consists of %s \n''' % get_course_names(ctx.user.preferences['course'])
    else:
        reply = '''You do not have any preferences in your list'''
    ctx.reply(reply)


def start_points(ctx):
    reply = '''You have %d points in your account''' % (ctx.user.incentive)
    ctx.reply(reply)
    reply1 = '''Hey!!! The good news for you is you can claim your points for printer credits or a coffee voucher. 100 points would be equivalent to 5 euro credits.'''
    ctx.reply(reply1)


def start_removepreference(ctx):
    ctx.reply('Type in the course name you wish to remove from your preferences')
    ctx.user.set_state('updating')


def start_menu(ctx):
    reply = myci_menu % (ctx.user.name)
    ctx.reply(reply)


def handle_model(ctx):
    user_id = ctx.user.id
    if user_id in pending.keys():
        if pending[user_id] in ctx.user.preferences['course']:
            reply = '`%s` already exists in your preference list.' % (
            pending[user_id] + ' ' + courses[pending[user_id]])
        else:
            closest = get_close_matches(ctx.message, ['yes', 'no'], cutoff=0)[0]
            if closest == 'yes':
                reply = 'Added `%s` to your preferences.' % (pending[user_id] + ' ' + courses[pending[user_id]])
                ctx.user.save_preference('course', pending[user_id])
            else:
                reply = 'Did not add `%s` to your preferences.' % (pending[user_id] + ' ' + courses[pending[user_id]])
        ctx.reply(reply)
        del pending[user_id]
        ctx.user.set_state('idle')
    else:
        closest = get_close_matches(ctx.message, [code + ' ' + courses[code] for code in courses], cutoff=0)[0]
        reply = "Did you mean the course: `%s`" % closest
        coursecode = closest.split(' ')[0]
        ctx.reply(reply)
        pending[user_id] = coursecode


def handle_update(ctx):
    user_id = ctx.user.id
    if user_id in pending.keys():
        if pending[user_id] in ctx.user.preferences['course']:
            closest = get_close_matches(ctx.message, ['yes', 'no'], cutoff=0)[0]
            if closest == 'yes':
                reply = 'Deleted `%s` from your preferences.' % (pending[user_id] + ' ' + courses[pending[user_id]])
                ctx.user.del_preference('course', pending[user_id])
            else:
                reply = 'Sorry we did not find any other courses with this keyword'
        else:
            reply = 'Cannot delete `%s` as it does not exists in your preference list.' % (
            pending[user_id] + ' ' + courses[pending[user_id]])
        ctx.user.set_state('idle')
        ctx.reply(reply)
        del pending[user_id]
    else:
        closest = get_close_matches(ctx.message, [code + ' ' + courses[code] for code in courses], cutoff=0)[0]
        reply = "Did you mean the course: `%s`" % closest
        coursecode = closest.split(' ')[0]
        ctx.reply(reply)
        pending[user_id] = coursecode


def recommendation_list():
    res = ""
    for r in recommendations:
        res += '`%s`\n' % recommendations[r]['name']
    return res
